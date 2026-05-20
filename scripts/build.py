from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path
import posixpath
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from site_data import about, gallery_sections, home_blocks, projects, site  # noqa: E402

LANGUAGES = ["es", "en"]

LANG_CONFIG = {
    "es": {
        "label": "ES",
        "html_lang": "es",
        "nav_home": "Inicio",
        "nav_projects": "Proyectos",
        "nav_about": "Biografía",
        "nav_gallery": "Galería",
        "skip_link": "Saltar al contenido",
        "nav_aria": "Navegación principal",
        "lang_aria": "Idioma",
        "footer_rights": "Todos los derechos reservados.",
        "project_back": "Volver a proyectos",
        "view_project": "Ver proyecto",
        "projects_intro": "<p>Una selección de trabajos en arte comunitario, textil, cerámica, investigación patrimonial y gestión cultural.</p>",
        "about_title": "Biografía",
        "gallery_title": "Galería",
        "gallery_intro": "<p>Una selección curada de cerámica, textiles, bordados, murales colaborativos y procesos de taller.</p>",
    },
    "en": {
        "label": "EN",
        "html_lang": "en",
        "nav_home": "Home",
        "nav_projects": "Projects",
        "nav_about": "Biography",
        "nav_gallery": "Gallery",
        "skip_link": "Skip to content",
        "nav_aria": "Main navigation",
        "lang_aria": "Language",
        "footer_rights": "All rights reserved.",
        "project_back": "Back to projects",
        "view_project": "View project",
        "projects_intro": "<p>A selection of works in community art, textiles, ceramics, heritage research and cultural management.</p>",
        "about_title": "Biography",
        "gallery_title": "Gallery",
        "gallery_intro": "<p>A curated selection of ceramics, textiles, embroidery, collaborative murals and workshop processes.</p>",
    },
}

LANG_ROUTES = {
    "es": {"home": "/es/", "projects": "/es/proyectos/", "about": "/es/biografia/", "gallery": "/es/galeria/"},
    "en": {"home": "/en/", "projects": "/en/projects/", "about": "/en/biography/", "gallery": "/en/gallery/"},
}

SPANISH_MONTHS = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]

ENGLISH_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def t(d: dict | str, lang: str) -> str:
    if isinstance(d, str):
        return d
    return d.get(lang, d.get("es", ""))


def other_lang_path(current_path: str, lang: str) -> str:
    target_lang = "en" if lang == "es" else "es"

    if current_path in [LANG_ROUTES["es"]["home"], LANG_ROUTES["en"]["home"]]:
        return LANG_ROUTES[target_lang]["home"]
    if current_path in [LANG_ROUTES["es"]["about"], LANG_ROUTES["en"]["about"]]:
        return LANG_ROUTES[target_lang]["about"]
    if current_path in [LANG_ROUTES["es"]["gallery"], LANG_ROUTES["en"]["gallery"]]:
        return LANG_ROUTES[target_lang]["gallery"]
    if current_path in [LANG_ROUTES["es"]["projects"], LANG_ROUTES["en"]["projects"]]:
        return LANG_ROUTES[target_lang]["projects"]

    if lang == "es" and current_path.startswith("/es/proyectos/"):
        return current_path.replace("/es/proyectos/", "/en/projects/", 1)
    if lang == "en" and current_path.startswith("/en/projects/"):
        return current_path.replace("/en/projects/", "/es/proyectos/", 1)

    return LANG_ROUTES[target_lang]["home"]


def main() -> None:
    shutil.rmtree(ROOT / "es", ignore_errors=True)
    shutil.rmtree(ROOT / "en", ignore_errors=True)
    sync_gallery_assets()
    write_file(ROOT / "index.html", render_redirect())
    write_file(ROOT / ".nojekyll", "")

    for lang in LANGUAGES:
        routes = LANG_ROUTES[lang]
        page_prefix = lang

        about_suffix = routes["about"].strip("/").split("/", 1)[1]
        projects_suffix = routes["projects"].strip("/").split("/", 1)[1]
        gallery_suffix = routes["gallery"].strip("/").split("/", 1)[1]

        write_page(f"{page_prefix}", render_home_page(lang))
        write_page(f"{page_prefix}/{about_suffix}", render_about_page(lang))
        write_page(f"{page_prefix}/{gallery_suffix}", render_gallery_page(lang))
        write_page(f"{page_prefix}/{projects_suffix}", render_projects_index(lang))
        for project in projects:
            slug_dir = f"{page_prefix}/{projects_suffix}/{project['slug']}"
            write_page(slug_dir, render_project_detail(project, lang))


def sync_gallery_assets() -> None:
    gallery_root = ROOT / "assets" / "images" / "gallery"
    source_root = ROOT / "Fotos Web anterior"
    seen: set[str] = set()

    if not source_root.exists():
        missing = [image["src"] for image in iter_gallery_images() if not (ROOT / image["src"]).exists()]
        if missing:
            raise FileNotFoundError("Missing curated gallery assets: " + ", ".join(missing))
        return

    shutil.rmtree(gallery_root, ignore_errors=True)
    for image in iter_gallery_images():
        if not image.get("source"):
            continue
        source = ROOT / image["source"]
        destination = ROOT / image["src"]
        if image["src"] in seen:
            continue
        seen.add(image["src"])
        if not source.exists():
            raise FileNotFoundError(f"Missing gallery image source: {source}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def iter_gallery_images():
    for item in about.get("visual_story", {}).get("items", []):
        yield item
    for project in projects:
        if project.get("image"):
            yield project["image"]
        for item in project.get("gallery", {}).get("items", []):
            yield item
    for section in gallery_sections:
        for item in section.get("items", []):
            yield item
    for block in home_blocks:
        if block.get("image"):
            yield block["image"]
        if block.get("background_image", {}).get("source"):
            yield block["background_image"]
        for item in block.get("items", []):
            yield item


def write_page(route: str, content: str) -> None:
    directory = ROOT / route
    directory.mkdir(parents=True, exist_ok=True)
    write_file(directory / "index.html", content)


def write_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def render_redirect() -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="0; url=es/">
    <title>{html(site['name'])} | {html(t(site['title_suffix'], 'es'))}</title>
</head>
<body>
    <p>Redirigiendo a <a href="es/">/es/</a>.</p>
    <script>window.location.replace('es/');</script>
</body>
</html>
"""


def layout(title: str, body_class: str, current_path: str, lang: str, content: str, description: str | None = None) -> str:
    config = LANG_CONFIG[lang]
    routes = LANG_ROUTES[lang]
    desc = t(description or site["description"], lang)
    document_title = f"{site['name']} | {t(site['title_suffix'], lang)}" if title == site["name"] else f"{title} | {t(site['title_suffix'], lang)}"

    if lang == "es":
        es_href = page_url(current_path, current_path)
        en_href = page_url(current_path, other_lang_path(current_path, lang))
        es_active = " active"
        en_active = ""
    else:
        es_href = page_url(current_path, other_lang_path(current_path, lang))
        en_href = page_url(current_path, current_path)
        es_active = ""
        en_active = " active"

    return f"""<!DOCTYPE html>
<html lang="{config['html_lang']}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html(document_title)}</title>
    <meta name="description" content="{attr(desc)}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Source+Sans+3:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="icon" href="{asset_url(current_path, 'assets/images/favicon.svg')}" type="image/svg+xml">
    <link rel="stylesheet" href="{asset_url(current_path, 'assets/css/main.css')}">
    <link rel="stylesheet" href="{asset_url(current_path, 'assets/css/prose.css')}">
</head>
<body class="{attr(body_class)} static-site">
    <a href="#contenido" class="skip-link">{config['skip_link']}</a>
    <header class="site-header">
        <nav class="nav-container" aria-label="{config['nav_aria']}">
            <a href="{page_url(current_path, routes['home'])}" class="logo">Max Sepúlveda</a>
            <ul class="nav-menu">
                {nav_item(current_path, routes['home'], config['nav_home'])}
                {nav_item(current_path, routes['projects'], config['nav_projects'])}
                {nav_item(current_path, routes['about'], config['nav_about'])}
                {nav_item(current_path, routes['gallery'], config['nav_gallery'])}
            </ul>
            <div class="language-switcher" aria-label="{config['lang_aria']}">
                <a href="{es_href}" class="lang-link{es_active}" hreflang="es">ES</a>
                <a href="{en_href}" class="lang-link{en_active}" hreflang="en">EN</a>
            </div>
        </nav>
    </header>
    <main class="main-content" id="contenido">
        {content}
    </main>
    <footer class="site-footer">
        <div class="footer-container">
            <p class="footer-brand">{html(site['name'])}</p>
            <p class="footer-tagline">{html(t(site['tagline'], lang))}</p>
            <p class="footer-copy">&copy; {html(site['year'])} {config['footer_rights']}</p>
        </div>
    </footer>
    <script src="{asset_url(current_path, 'assets/js/main.js')}"></script>
</body>
</html>
"""


def nav_item(current_path: str, target_path: str, label: str) -> str:
    is_active = current_path == target_path if target_path in ("/es/", "/en/") else current_path.startswith(target_path)
    current = ' aria-current="page"' if is_active else ""
    return f'<li><a href="{page_url(current_path, target_path)}"{current}>{html(label)}</a></li>'


def render_home_page(lang: str) -> str:
    return layout(
        title=site["name"],
        body_class="home-page",
        current_path=LANG_ROUTES[lang]["home"],
        lang=lang,
        content=f'<div class="sf-stack">{render_blocks(home_blocks, LANG_ROUTES[lang]["home"], lang)}</div>',
    )


def render_about_page(lang: str) -> str:
    current_path = LANG_ROUTES[lang]["about"]
    config = LANG_CONFIG[lang]
    visual_story = render_about_visual_story(about["visual_story"], current_path, lang) if about.get("visual_story") else ""
    sections = "\n".join(
        f"""<section class="about-section">
    <h2>{html(t(sec["title"], lang))}</h2>
    <div class="prose">{t(sec["content"], lang)}</div>
</section>"""
        for sec in about["sections"]
    )
    content = f"""<section class="page-header">
    <div class="container">
        <h1>{config['about_title']}</h1>
        <div class="intro prose prose-wide">{t(about['intro'], lang)}</div>
    </div>
</section>
{visual_story}
<section class="about-sections">
    <div class="container">
        {sections}
    </div>
</section>"""
    return layout(config["about_title"], "about-page", current_path, lang, content)


def render_about_visual_story(section: dict, current_path: str, lang: str) -> str:
    items = "\n".join(render_about_visual_item(item, current_path, lang) for item in section.get("items", []))
    return f"""<section class="about-visuals">
    <div class="container">
        <div class="sf-section-header">
            <h2 class="sf-section-header__title">{html(t(section['title'], lang))}</h2>
            <p class="sf-section-header__subtitle">{html(t(section['description'], lang))}</p>
        </div>
        <div class="about-visuals__grid">
            {items}
        </div>
    </div>
</section>"""


def render_about_visual_item(image: dict, current_path: str, lang: str) -> str:
    src = asset_url(current_path, image["src"])
    return f"""<figure class="about-visuals__item">
    <a href="{src}" class="about-visuals__link">
        <img src="{src}" alt="{attr(t(image['alt'], lang))}" loading="lazy" decoding="async">
    </a>
    <figcaption class="about-visuals__caption">{html(t(image['caption'], lang))}</figcaption>
</figure>"""


def render_gallery_page(lang: str) -> str:
    current_path = LANG_ROUTES[lang]["gallery"]
    config = LANG_CONFIG[lang]
    sections = "\n".join(render_gallery_section(section, current_path, lang) for section in gallery_sections)
    content = f"""<section class="page-header">
    <div class="container">
        <h1>{config['gallery_title']}</h1>
        <div class="intro prose prose-wide">{config['gallery_intro']}</div>
    </div>
</section>
<div class="gallery-page-sections">
    {sections}
</div>"""
    return layout(config["gallery_title"], "gallery-page", current_path, lang, content)


def render_gallery_section(section: dict, current_path: str, lang: str) -> str:
    items = "\n".join(render_gallery_item(item, current_path, lang) for item in section.get("items", []))
    return f"""<section class="sf-block sf-block--gallery">
    <div class="sf-container">
        <div class="sf-section-header">
            <h2 class="sf-section-header__title">{html(t(section['title'], lang))}</h2>
            <p class="sf-section-header__subtitle">{html(t(section['description'], lang))}</p>
        </div>
        <div class="sf-gallery sf-gallery--cols-masonry">
            {items}
        </div>
    </div>
</section>"""


def render_projects_index(lang: str) -> str:
    current_path = LANG_ROUTES[lang]["projects"]
    config = LANG_CONFIG[lang]
    cards = "\n".join(render_project_card(project, 2, current_path, lang) for project in projects)
    content = f"""
<section class="page-header">
    <div class="container">
        <h1>{config['nav_projects']}</h1>
        <div class="intro prose prose-wide">{config['projects_intro']}</div>
    </div>
</section>
<section class="projects-section">
    <div class="container">
        <div class="projects-grid">
            {cards}
        </div>
    </div>
</section>"""
    return layout(config["nav_projects"], "projects-index", current_path, lang, content)


def render_project_detail(project: dict, lang: str) -> str:
    current_path = f"{LANG_ROUTES[lang]['projects']}{project['slug']}/"
    config = LANG_CONFIG[lang]
    project_link = ""
    if project.get("live_url"):
        project_link = f'<div class="project-links"><a href="{attr(project["live_url"])}" target="_blank" rel="noopener" class="btn btn-primary">{config["view_project"]}</a></div>'
    project_link_markup = f"\n            {project_link}" if project_link else ""
    featured = render_featured_image(project["image"], current_path, lang) if project.get("image") else ""
    gallery = render_project_gallery(project["gallery"], current_path, lang) if project.get("gallery") else ""
    content = f"""
<article class="project-detail">
    <header class="project-header">
        <div class="container">
            <h1>{html(t(project['title'], lang))}</h1>
            <p class="summary">{html(t(project['summary'], lang))}</p>
            <div class="project-meta">
                <time datetime="{project['date']}">{format_date(project['date'], lang)}</time>
                {render_tags(project.get('tags', []), LANG_ROUTES[lang]['projects'], current_path, lang)}
            </div>{project_link_markup}
        </div>
    </header>
    {featured}
    <div class="sf-stack project-content">
        {render_blocks(project['content'], current_path, lang)}
    </div>
    {gallery}
    <footer class="project-footer container">
        <a href="{page_url(current_path, LANG_ROUTES[lang]['projects'])}" class="btn">&larr; {config['project_back']}</a>
    </footer>
</article>"""
    return layout(t(project["title"], lang), "project-detail", current_path, lang, content, t(project["summary"], lang))


def render_blocks(blocks: list[dict], current_path: str, lang: str) -> str:
    return "\n".join(render_block(block, current_path, lang) for block in blocks)


def render_block(block: dict, current_path: str, lang: str) -> str:
    block_type = block["type"]
    if block_type == "hero":
        return render_hero(block, current_path, lang)
    if block_type == "text_section":
        return render_text_section(block, current_path, lang)
    if block_type == "media_strip":
        return render_media_strip(block, current_path, lang)
    if block_type == "portfolio_grid":
        return render_portfolio_grid(block, current_path, lang)
    if block_type == "gallery":
        return render_gallery_block(block, current_path, lang)
    if block_type == "contact":
        return render_contact(block, lang)
    if block_type == "quote":
        return render_quote(block, lang)
    return ""


def render_hero(block: dict, current_path: str, lang: str) -> str:
    background = ""
    extra_class = ""
    if block.get("background_image"):
        background_image = block["background_image"]
        background_url = asset_url(current_path, background_image["src"])
        background_position = attr(background_image.get("position", "center"))
        extra_class = " sf-hero--with-background"
        background = f'<div class="sf-hero__background" style="background-image: url(\'{background_url}\'); background-position: {background_position};" aria-hidden="true"></div>'
    background_markup = f"\n    {background}" if background else ""
    return f"""<section class="sf-block sf-block--hero sf-variant--{variant(block.get('variant'))}{extra_class}">{background_markup}
    <div class="sf-container sf-hero__content">
        <h1 class="sf-hero__title">{html(block['title'])}</h1>
        <p class="sf-hero__subtitle">{html(t(block['subtitle'], lang))}</p>
        <div class="sf-hero__cta"><a href="{site_url(current_path, t(block['cta']['url'], lang))}" class="btn btn-primary">{html(t(block['cta']['text'], lang))}</a></div>
    </div>
</section>"""


def render_text_section(block: dict, current_path: str, lang: str) -> str:
    title = f'<h2 class="sf-text__title">{html(t(block["title"], lang))}</h2>' if block.get("title") else ""
    image = ""
    text_classes = "sf-text"
    if block.get("image"):
        position = variant(block.get("image_position", "right"))
        text_classes += f" sf-text--with-image sf-text--image-{position}"
        image = render_inline_image(block["image"], current_path, lang, "sf-text__image")
    title_markup = f"\n                {title}" if title else ""
    image_markup = f"\n            {image}" if image else ""
    return f"""<section class="sf-block sf-block--text sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container">
        <div class="{text_classes}">
            <div class="sf-text__content">{title_markup}
                <div class="sf-text__body prose">{t(block['content'], lang)}</div>
            </div>{image_markup}
        </div>
    </div>
</section>"""


def render_inline_image(image: dict, current_path: str, lang: str, class_name: str) -> str:
    return f"""<figure class="{class_name}">
    <img src="{asset_url(current_path, image['src'])}" alt="{attr(t(image['alt'], lang))}" loading="lazy" decoding="async">
    <figcaption>{html(t(image['caption'], lang))}</figcaption>
</figure>"""


def render_portfolio_grid(block: dict, current_path: str, lang: str) -> str:
    visible_projects = [project for project in projects if project.get("featured")] if block.get("show_featured_only") else projects
    visible_projects = visible_projects[: block.get("max_items", len(visible_projects))]
    cards = "\n".join(render_project_card(project, 3, current_path, lang) for project in visible_projects)
    footer = f'<div class="sf-section-footer"><a href="{page_url(current_path, LANG_ROUTES[lang]["projects"])}" class="btn">{t({"es": "Ver todos los proyectos", "en": "View all projects"}, lang)}</a></div>' if block.get("show_link_to_all") else ""
    return f"""<section class="sf-block sf-block--portfolio-grid sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container">
        <div class="sf-section-header">
            <h2 class="sf-section-header__title">{html(t(block['title'], lang))}</h2>
            <p class="sf-section-header__subtitle">{html(t(block['subtitle'], lang))}</p>
        </div>
        <div class="sf-portfolio-grid projects-grid">
            {cards}
        </div>
        {footer}
    </div>
</section>"""


def render_gallery_block(block: dict, current_path: str, lang: str) -> str:
    items = "\n".join(render_gallery_item(item, current_path, lang) for item in block.get("items", []))
    footer = ""
    if block.get("show_link_to_all"):
        label = t({"es": "Ver galería completa", "en": "View full gallery"}, lang)
        footer = f'<div class="sf-section-footer"><a href="{page_url(current_path, LANG_ROUTES[lang]["gallery"])}" class="btn">{label}</a></div>'
    return f"""<section class="sf-block sf-block--gallery sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container">
        <div class="sf-section-header">
            <h2 class="sf-section-header__title">{html(t(block['title'], lang))}</h2>
            <p class="sf-section-header__subtitle">{html(t(block['subtitle'], lang))}</p>
        </div>
        <div class="sf-gallery sf-gallery--cols-{block.get('columns', 3)}">
            {items}
        </div>
        {footer}
    </div>
</section>"""


def render_media_strip(block: dict, current_path: str, lang: str) -> str:
    items = "\n".join(render_media_strip_item(item, current_path, lang) for item in block.get("items", []))
    return f"""<section class="sf-block sf-block--media-strip sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container">
        <div class="sf-media-strip__header">
            <h2 class="sf-media-strip__title">{html(t(block['title'], lang))}</h2>
            <p class="sf-media-strip__subtitle">{html(t(block['subtitle'], lang))}</p>
        </div>
        <div class="sf-media-strip__grid">
            {items}
        </div>
    </div>
</section>"""


def render_media_strip_item(image: dict, current_path: str, lang: str) -> str:
    return f"""<figure class="sf-media-strip__item">
    <img src="{asset_url(current_path, image['src'])}" alt="{attr(t(image['alt'], lang))}" loading="lazy" decoding="async">
    <figcaption>{html(t(image['caption'], lang))}</figcaption>
</figure>"""


def render_project_gallery(gallery: dict, current_path: str, lang: str) -> str:
    items = "\n".join(render_gallery_item(item, current_path, lang) for item in gallery.get("items", []))
    return f"""<section class="sf-block sf-block--gallery project-gallery">
    <div class="sf-container">
        <div class="sf-section-header">
            <h2 class="sf-section-header__title">{html(t(gallery['title'], lang))}</h2>
        </div>
        <div class="sf-gallery sf-gallery--cols-3">
            {items}
        </div>
    </div>
</section>"""


def render_featured_image(image: dict, current_path: str, lang: str) -> str:
    return f"""<figure class="featured-image project-featured-image">
    <img src="{asset_url(current_path, image['src'])}" alt="{attr(t(image['alt'], lang))}" loading="lazy" decoding="async">
    <figcaption>{html(t(image['caption'], lang))}</figcaption>
</figure>"""


def render_gallery_item(image: dict, current_path: str, lang: str) -> str:
    src = asset_url(current_path, image["src"])
    alt = attr(t(image["alt"], lang))
    caption = html(t(image["caption"], lang))
    return f"""<figure class="sf-gallery__item">
    <a href="{src}" class="sf-gallery__link">
        <img src="{src}" alt="{alt}" loading="lazy" decoding="async">
    </a>
    <figcaption class="sf-gallery__caption">{caption}</figcaption>
</figure>"""


def render_contact(block: dict, lang: str) -> str:
    links = "\n".join(render_social_link(link, lang) for link in block.get("social_links", []))
    return f"""<section class="sf-block sf-block--contact sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container">
        <div class="sf-contact">
            <h2 class="sf-contact__title">{html(t(block['title'], lang))}</h2>
            <p class="sf-contact__text">{html(t(block['text'], lang))}</p>
            <div class="sf-contact__email"><a href="mailto:{attr(block['email'])}" class="sf-contact__email-link">{html(block['email'])}</a></div>
            <div class="sf-contact__social">{links}</div>
        </div>
    </div>
</section>"""


def render_quote(block: dict, lang: str) -> str:
    author = f'<cite class="sf-quote__author">&mdash; {html(block["author"])}</cite>' if block.get("author") else ""
    source_raw = t(block.get("source", ""), lang) if isinstance(block.get("source"), dict) else block.get("source", "")
    source = f'<span class="sf-quote__source">{html(source_raw)}</span>' if source_raw else ""
    return f"""<section class="sf-block sf-block--quote sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container">
        <blockquote class="sf-quote">
            <p class="sf-quote__text">{html(t(block['quote'], lang))}</p>
            <footer class="sf-quote__footer">{author}{source}</footer>
        </blockquote>
    </div>
</section>"""


def render_project_card(project: dict, heading_level: int, current_path: str, lang: str) -> str:
    image = ""
    if project.get("image"):
        link = page_url(current_path, f"{LANG_ROUTES[lang]['projects']}{project['slug']}/")
        src = asset_url(current_path, project["image"]["src"])
        image = f"""<a href="{link}" class="project-card__image-link">
        <img src="{src}" alt="{attr(t(project['image']['alt'], lang))}" loading="lazy" decoding="async">
    </a>"""
    return f"""<article class="project-card">
    {image}
    <div class="project-info">
        <h{heading_level}><a href="{page_url(current_path, f"{LANG_ROUTES[lang]['projects']}{project['slug']}/")}">{html(t(project['title'], lang))}</a></h{heading_level}>
        <p>{html(truncate_words(t(project['summary'], lang), 25))}</p>
        {render_tags(project.get('tags', []), LANG_ROUTES[lang]['projects'], current_path, lang)}
    </div>
</article>"""


def render_tags(tags: dict | list, base_path: str, current_path: str, lang: str) -> str:
    tags_list = tags.get(lang, []) if isinstance(tags, dict) else tags
    if not tags_list:
        return ""
    links = "".join(f'<a href="{page_url(current_path, base_path)}" class="tag">{html(tag)}</a>' for tag in tags_list)
    return f'<div class="tags">{links}</div>'


def render_social_link(link: dict, lang: str) -> str:
    return (
        f'<a href="{attr(link["url"])}" class="sf-social-link sf-social-link--{attr(link["platform"])}" '
        f'target="_blank" rel="noopener noreferrer" aria-label="{attr(t(link["label"], lang))}">{social_icon(link["platform"])}</a>'
    )


def social_icon(platform: str) -> str:
    if platform == "instagram":
        return '<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>'
    return '<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>'


def parse_date(date_string: str) -> date:
    return date.fromisoformat(date_string)


def format_date(date_string: str, lang: str) -> str:
    parsed = parse_date(date_string)
    if lang == "es":
        return f"{parsed.day} de {SPANISH_MONTHS[parsed.month - 1]} de {parsed.year}"
    return f"{ENGLISH_MONTHS[parsed.month - 1]} {parsed.day}, {parsed.year}"


def truncate_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return f"{' '.join(words[:max_words])}..."


def variant(value: str | None) -> str:
    cleaned = re.sub(r"[^a-z0-9-]", "", (value or "default").lower())
    return cleaned or "default"


def html(value: object) -> str:
    return escape(str(value), quote=True)


def attr(value: object) -> str:
    return html(value)


def page_url(current_path: str, target_path: str) -> str:
    return relative_url(current_path, target_path.strip("/"), is_directory=True)


def asset_url(current_path: str, asset_path: str) -> str:
    return relative_url(current_path, asset_path.strip("/"), is_directory=False)


def site_url(current_path: str, url: str) -> str:
    if re.match(r"^[a-z][a-z0-9+.-]*:", url):
        return attr(url)
    return page_url(current_path, url)


def relative_url(current_path: str, target: str, is_directory: bool) -> str:
    current_dir = current_path.strip("/") or "."
    relative = posixpath.relpath(target or ".", current_dir)
    if relative == ".":
        relative = ""
    if is_directory:
        return f"{relative}/" if relative else "./"
    return relative


if __name__ == "__main__":
    main()
