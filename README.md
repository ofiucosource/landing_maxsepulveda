# Max Sepúlveda Static

Versión estática en HTML, CSS y JavaScript del sitio Max Sepúlveda. No usa Django, Wagtail, Postgres ni Docker.

## Rutas

- `/`
- `/es/`
- `/es/proyectos/`
- `/es/proyectos/<slug>/`
- `/es/eventos/`
- `/es/eventos/<slug>/`
- `/es/blog/`
- `/es/blog/<slug>/`

## Desarrollo

```bash
python3 scripts/build.py
python3 -m http.server 4173
```

La raíz redirige a `/es/`. La navegación principal solo apunta al contenido español disponible.

## GitHub Pages

Los enlaces se generan de forma relativa para funcionar tanto en un dominio raíz como en GitHub Pages de proyecto, por ejemplo `https://usuario.github.io/repositorio/`. El archivo `.nojekyll` evita procesamiento adicional de Jekyll.

La opción recomendada es desplegar con GitHub Actions usando `.github/workflows/pages.yml`. Ese flujo ejecuta el generador y publica únicamente `index.html`, `es/`, `assets/` y `.nojekyll` como artefacto estático.