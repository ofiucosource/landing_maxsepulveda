"""Mide el peso que cada pagina transfiere en assets locales.

Escanea `index.html` + `es/**/*.html` y suma el tamaño en disco de cada
recurso local referenciado (imagenes, css, js, pdf). Para cada imagen cuenta
una sola representacion: la que un navegador moderno descargaria dentro de
su <picture> (AVIF > WebP > JPEG). Las variantes de srcset son alternativas
de tamaño, no se suman; los enlaces de lightbox (href al original) solo se
cargan al hacer clic y no se cuentan. Las fuentes de Google Fonts son
externas y no se cuentan.

Uso:
    python scripts/measure_site.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PICTURE_PATTERN = re.compile(r"<picture>(.*?)</picture>", re.DOTALL)
SRC_PATTERN = re.compile(r'src="([^"]+)"')
SRCSET_PATTERN = re.compile(r'srcset="([^"]+)"')
HREF_PATTERN = re.compile(r'href="([^"]+)"')
URL_PATTERN = re.compile(r"url\('([^']+)'\)")

LOCAL_PREFIXES = ("assets/images/", "assets/css/", "assets/js/", "assets/pdf/")

EXT_PATTERN = re.compile(r"\.(?:jpe?g|png|webp|avif)$", re.IGNORECASE)
VARIANT_PATTERN = re.compile(r"-(\d+)w\.(?:avif|webp)$", re.IGNORECASE)


def local_ref(token: str) -> str | None:
    for prefix in LOCAL_PREFIXES:
        idx = token.find(prefix)
        if idx != -1:
            return token[idx:]
    return None


def base_stem(ref: str) -> str:
    """assets/images/.../nombre -> assets/images/.../nombre (sin variante ni extension)."""
    return EXT_PATTERN.sub("", VARIANT_PATTERN.sub("", ref))


def first_srcset_entry(srcset: str) -> str:
    part = srcset.split(",")[0].strip()
    match = re.match(r"^(.*\S)\s+\d+w$", part)
    return match.group(1) if match else part


def extract_tokens(text: str) -> set[str]:
    tokens: set[str] = set()
    for pattern in (SRC_PATTERN, SRCSET_PATTERN, HREF_PATTERN, URL_PATTERN):
        for raw in pattern.findall(text):
            parts = raw.split(",") if pattern is SRCSET_PATTERN else [raw]
            for part in parts:
                token = part.strip()
                if pattern is SRCSET_PATTERN:
                    token = re.sub(r"\s+\d+w$", "", token)
                tokens.add(token)
    return tokens


def main() -> None:
    html_files = [ROOT / "index.html"] + sorted((ROOT / "es").rglob("*.html"))
    rows: list[tuple[str, int, int]] = []
    missing: set[str] = set()

    for html_file in html_files:
        text = html_file.read_text(encoding="utf-8")

        choices: dict[str, str] = {}
        for block in PICTURE_PATTERN.findall(text):
            img_match = SRC_PATTERN.search(block)
            if not img_match:
                continue
            ref = local_ref(img_match.group(1).strip())
            if not ref or not ref.startswith("assets/images/"):
                continue
            stem = base_stem(ref)
            if "image/avif" in block:
                choices[stem] = stem + ".avif"
            elif "image/webp" in block:
                choices[stem] = stem + ".webp"
            else:
                choices[stem] = ref

        weighted: set[str] = set()
        for token in extract_tokens(text):
            ref = local_ref(token)
            if not ref:
                continue
            if ref.startswith("assets/images/"):
                weighted.add(choices.get(base_stem(ref), ref))
            else:
                weighted.add(ref)

        total = 0
        for ref in weighted:
            path = ROOT / ref
            if path.exists():
                total += path.stat().st_size
            else:
                missing.add(ref)
        rows.append((html_file.relative_to(ROOT).as_posix(), len(weighted), total))

    rows.sort(key=lambda row: row[2], reverse=True)
    grand_total = 0
    for name, count, size in rows:
        grand_total += size
        print(f"{size / 1024 / 1024:7.2f} MB  {count:3} recursos  {name}")

    print(f"\nSuma del peso por pagina (sin cache): {grand_total / 1024 / 1024:.2f} MB")

    if missing:
        print("\nReferencias sin archivo en disco:")
        for ref in sorted(missing):
            print(f"  - {ref}")
        sys.exit(1)


if __name__ == "__main__":
    main()