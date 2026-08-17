"""Optimiza las imagenes que el sitio realmente usa y archiva las que no.

Flujo:
    1. Corre primero `python scripts/build.py` para que `index.html` y
       `es/**/*.html` reflejen el contenido actual de `src/site_data.py`.
    2. Corre `python scripts/optimize_images.py`.

Que hace:
    1. Escanea `index.html` + `es/**/*.html` en busca de toda referencia real
       a `assets/images/...` (src="...", srcset="...", href="...",
       content="...", background-image:url('...')) para construir el set de
       imagenes en uso.
    2. Para cada imagen en uso:
       - Usa el respaldo intacto en `_context/originals/<misma-ruta>` como
         fuente (evita doble compresion); si no existe, usa el archivo actual.
       - La redimensiona (preservando proporcion, sin ampliar) a un limite de
         lado largo segun la carpeta, y la recomprime como JPEG.
       - Genera un `.webp` hermano con la misma imagen ya redimensionada.
       - Genera un `.avif` hermano (tamaño completo) y variantes
         `-480w/-800w/-1200w.avif` para <picture srcset>.
       - Registra ancho/alto/formatos en `src/image_manifest.json`, que
         `scripts/build.py` usa para emitir <picture> con width/height reales.
    3. Mueve cualquier imagen bajo `assets/images/` que NO este en uso a
       `_context/images-unused/<misma-ruta>` (carpeta local, ignorada por
       git). No se borra nada del disco.

Requiere Pillow (ver requirements.txt): pip install -r requirements.txt

Uso:
    python scripts/optimize_images.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / "assets" / "images"
MANIFEST_PATH = ROOT / "src" / "image_manifest.json"
CONTEXT_DIR = ROOT / "_context"
ORIGINALS_DIR = CONTEXT_DIR / "originals"
UNUSED_DIR = CONTEXT_DIR / "images-unused"

RASTER_SUFFIXES = {".jpg", ".jpeg", ".png"}
JPEG_QUALITY = 80
WEBP_QUALITY = 60
AVIF_QUALITY = 50
AVIF_SPEED = 6
VARIANT_WIDTHS = (480, 800, 1200)

SRCSET_PATTERN = re.compile(r'srcset="([^"]+)"')

REF_PATTERNS = [
    re.compile(r'src="([^"]+)"'),
    SRCSET_PATTERN,
    re.compile(r'href="([^"]+)"'),
    re.compile(r'content="([^"]+)"'),
    re.compile(r"url\('([^']+)'\)"),
]

VARIANT_RE = re.compile(r"^(?P<base>.+)-(?P<width>\d+)w$")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="Solo reporta que haria, sin modificar nada")
    args = parser.parse_args()

    if not (ROOT / "es").exists():
        print("No existe 'es/'. Corre primero: python scripts/build.py", file=sys.stderr)
        sys.exit(1)

    used = find_used_images(ROOT)
    stems = used_stems(used)
    print(f"Imagenes en uso detectadas en el HTML generado: {len(used)}")

    manifest: dict[str, dict] = {}
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    total_before = 0
    total_after = 0
    processed = 0
    skipped_missing = 0

    for rel in sorted(used):
        path = ROOT / rel
        if path.suffix.lower() not in RASTER_SUFFIXES:
            continue
        if not path.exists():
            print(f"  [omitido] no existe en disco: {rel}")
            skipped_missing += 1
            continue

        size_before = path.stat().st_size
        if args.dry_run:
            print(f"  [dry-run] {rel}: {size_before / 1024:.0f} KB -> objetivo {target_long_edge(rel)}px lado largo")
            continue

        backup_original(rel, path)
        try:
            width, height, variants = optimize_image(rel, path, target_long_edge(rel))
        except Exception as exc:  # noqa: BLE001 - queremos seguir con el resto de imagenes
            print(f"  [error] {rel}: {exc}", file=sys.stderr)
            continue

        size_after = path.stat().st_size
        webp_path = path.with_suffix(".webp")
        webp_size = webp_path.stat().st_size if webp_path.exists() else 0
        avif_path = path.with_suffix(".avif")
        avif_size = avif_path.stat().st_size if avif_path.exists() else 0
        variant_sizes = sum(
            (path.parent / f"{path.stem}-{w}w.avif").stat().st_size
            for w in variants
            if (path.parent / f"{path.stem}-{w}w.avif").exists()
        )

        manifest[rel] = {
            "width": width,
            "height": height,
            "webp": webp_path.exists(),
            "avif": avif_path.exists(),
            "avif_variants": variants,
        }
        total_before += size_before
        total_after += size_after + webp_size + avif_size + variant_sizes
        processed += 1
        print(
            f"  {rel}: {size_before / 1024:.0f} KB -> {size_after / 1024:.0f} KB "
            f"(webp {webp_size / 1024:.0f} KB, avif {avif_size / 1024:.0f} KB, variantes {variants})"
        )

    if args.dry_run:
        print("\n[dry-run] no se escribio el manifiesto ni se archivo nada.")
        return

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"\nManifiesto actualizado: {MANIFEST_PATH.relative_to(ROOT)} ({len(manifest)} imagenes registradas)")

    archived = archive_unused(used, stems)
    print(f"Imagenes archivadas en _context/images-unused/: {len(archived)}")

    if processed:
        print(
            f"\nProcesadas {processed} imagenes en uso: "
            f"{total_before / 1024 / 1024:.1f} MB -> {total_after / 1024 / 1024:.1f} MB "
            "(incluye JPEG + WebP + AVIF y variantes)"
        )
    if skipped_missing:
        print(f"Advertencia: {skipped_missing} referencias no se encontraron en disco.")

    print("\nListo. Corre 'python scripts/build.py' de nuevo para regenerar el HTML con <picture>/width/height.")


def find_used_images(root: Path) -> set[str]:
    """Escanea el HTML generado y devuelve el set de rutas assets/images/... en uso real."""
    used: set[str] = set()
    html_files = [root / "index.html"] + sorted((root / "es").rglob("*.html"))
    for html_file in html_files:
        if not html_file.exists():
            continue
        text = html_file.read_text(encoding="utf-8")
        for pattern in REF_PATTERNS:
            for raw in pattern.findall(text):
                refs = raw.split(",") if pattern is SRCSET_PATTERN else [raw]
                for ref in refs:
                    if pattern is SRCSET_PATTERN:
                        token = ref.strip().split(" ", 1)[0]
                    else:
                        token = ref.strip()
                    idx = token.find("assets/images/")
                    if idx == -1:
                        continue
                    used.add(token[idx:])
    return used


def used_stems(used: set[str]) -> set[str]:
    """Rutas sin extension, para poder reconocer hermanos (.webp/.avif) y
    variantes (-NNNw.avif) de una imagen en uso."""
    stems = set()
    for rel in used:
        p = Path(rel)
        stems.add((p.parent / p.stem).as_posix())
    return stems


def target_long_edge(rel_path: str) -> int:
    posix = rel_path.replace("\\", "/")
    if re.match(r"^assets/images/(header|header-8|max-sepulveda-hero|perfil|proyectos-header)\.\w+$", posix):
        return 2000
    if posix.startswith("assets/images/disciplinas/"):
        return 1800
    if posix.startswith("assets/images/gallery/"):
        return 1600
    if posix.startswith("assets/images/proyectos/"):
        return 900
    return 1400


def backup_original(rel: str, path: Path) -> None:
    backup_path = ORIGINALS_DIR / rel
    if backup_path.exists():
        return
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)


def open_source(rel: str, path: Path) -> Image.Image:
    """Abre la fuente mas limpia disponible: el respaldo intacto si tiene la
    misma o mayor resolucion que el archivo actual. Si el respaldo es menor
    (p. ej. una version antigua), se usa el archivo actual."""
    original = ORIGINALS_DIR / rel
    if original.exists():
        try:
            with Image.open(original) as candidate:
                if max(candidate.size) >= max(Image.open(path).size):
                    return Image.open(original)
        except Exception:
            pass
    return Image.open(path)


def optimize_image(rel: str, path: Path, max_long_edge: int) -> tuple[int, int, list[int]]:
    raw = open_source(rel, path)
    try:
        im = ImageOps.exif_transpose(raw)
        im.load()
    finally:
        raw.close()
    if im.mode != "RGB":
        im = im.convert("RGB")

    width, height = im.size
    long_edge = max(width, height)
    if long_edge > max_long_edge:
        scale = max_long_edge / long_edge
        new_size = (max(1, round(width * scale)), max(1, round(height * scale)))
        im = im.resize(new_size, Image.LANCZOS)

    if path.suffix.lower() == ".png":
        im.save(path, format="PNG", optimize=True)
    else:
        im.save(path, format="JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    im.save(path.with_suffix(".webp"), format="WEBP", quality=WEBP_QUALITY, method=6)
    im.save(path.with_suffix(".avif"), format="AVIF", quality=AVIF_QUALITY, speed=AVIF_SPEED)

    variants: list[int] = []
    for variant in VARIANT_WIDTHS:
        if variant >= width * 0.8:
            continue
        scale = variant / width
        variant_size = (variant, max(1, round(height * scale)))
        variant_path = path.parent / f"{path.stem}-{variant}w.avif"
        with im.resize(variant_size, Image.LANCZOS) as variant_im:
            variant_im.save(variant_path, format="AVIF", quality=AVIF_QUALITY, speed=AVIF_SPEED)
        variants.append(variant)
    return im.size[0], im.size[1], variants


def archive_unused(used: set[str], stems: set[str]) -> list[str]:
    archived = []
    if not IMAGES_DIR.exists():
        return archived
    for path in sorted(IMAGES_DIR.rglob("*")):
        if path.is_dir():
            continue
        rel_path = path.relative_to(ROOT)
        rel = rel_path.as_posix()
        if rel in used:
            continue
        if path.suffix.lower() in {".webp", ".avif"} and is_keepable(rel_path, stems):
            continue  # hermano o variante de una imagen en uso
        dest = UNUSED_DIR / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(dest))
        archived.append(rel)
    return archived


def is_keepable(rel_path: Path, stems: set[str]) -> bool:
    """Un archivo es mantenible si su tallo (ruta sin extension) coincide con
    una imagen en uso o con una variante '-NNNw' de ella."""
    stem = (rel_path.parent / rel_path.stem).as_posix()
    if stem in stems:
        return True
    match = VARIANT_RE.match(stem)
    return bool(match and match.group("base") in stems)


if __name__ == "__main__":
    main()