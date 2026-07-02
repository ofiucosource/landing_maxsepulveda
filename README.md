# Max Sepúlveda Static

Versión estática en HTML, CSS y JavaScript del sitio Max Sepúlveda. No usa Django, Wagtail, Postgres ni Docker.

## Rutas

- `/`
- `/es/`
- `/es/sobre-max/`
- `/es/proyectos/`
- `/es/proyectos/<slug>/`

## Desarrollo

```bash
python3 scripts/build.py
python3 -m http.server 4173
```

La raíz redirige a `/es/`. La navegación principal solo apunta al contenido español disponible: Inicio, Sobre Max y Proyectos.

## Estructura del repositorio

El sitio público se compone de `index.html`, `es/`, `assets/`, `.nojekyll` y el workflow de GitHub Pages. La fuente editable del sitio vive en `src/site_data.py` y `scripts/build.py`; cualquier cambio de contenido debe hacerse ahí y luego regenerarse con `python3 scripts/build.py`.

Los documentos originales, archivos de referencia, catálogos visuales y fotografías no seleccionadas se mantienen como contexto local fuera del repositorio público, en `_context/`. Esa carpeta está ignorada por git y no forma parte del despliegue.

## Imágenes

Las imágenes que efectivamente usa el sitio se optimizan con `scripts/optimize_images.py` (requiere Pillow: `pip install -r requirements.txt`). Cada vez que agregues o reemplaces fotos en `assets/images/` y las enlaces desde `src/site_data.py`:

```bash
python3 scripts/build.py
python3 scripts/optimize_images.py
python3 scripts/build.py
```

El primer build genera el HTML para que el script detecte qué imágenes están realmente en uso. El script respalda el original intacto en `_context/originals/`, redimensiona y recomprime la imagen en `assets/images/`, genera un `.webp` hermano, y registra ancho/alto en `src/image_manifest.json` (versionado, lo usa `build.py` para emitir `<picture>` con `width`/`height` reales). El segundo build regenera el HTML ya con esos datos. Las imágenes de `assets/images/` que no estén enlazadas en `site_data.py` se mueven automáticamente a `_context/images-unused/` (no se borran).

## GitHub Pages

Los enlaces se generan de forma relativa para funcionar tanto en un dominio raíz como en GitHub Pages de proyecto, por ejemplo `https://usuario.github.io/repositorio/`. El archivo `.nojekyll` evita procesamiento adicional de Jekyll.

La opción recomendada es desplegar con GitHub Actions usando `.github/workflows/pages.yml`. Ese flujo ejecuta el generador y publica `index.html`, `es/`, `assets/` y `.nojekyll` como artefacto estático.
