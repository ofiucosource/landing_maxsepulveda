from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path
import json
import posixpath
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from site_data import about_page, disciplines, home_blocks, milestones, other_workshops, projects, site  # noqa: E402

IMAGE_MANIFEST_PATH = ROOT / "src" / "image_manifest.json"


def load_image_manifest() -> dict:
    if IMAGE_MANIFEST_PATH.exists():
        return json.loads(IMAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


IMAGE_MANIFEST = load_image_manifest()

SPANISH_MONTHS = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


def main() -> None:
    shutil.rmtree(ROOT / "es", ignore_errors=True)
    write_file(ROOT / "index.html", render_redirect())
    write_file(ROOT / ".nojekyll", "")
    write_page("es", render_home_page())
    write_page("es/sobre-max", render_about_page())
    write_page("es/proyectos", render_projects_index())
    for project in projects:
        write_page(f"es/proyectos/{project['slug']}", render_project_detail(project))


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
    <title>{html(site['name'])} | {html(site['title_suffix'])}</title>
</head>
<body>
    <p>Redirigiendo a <a href="es/">/es/</a>.</p>
    <script>window.location.replace('es/');</script>
</body>
</html>
"""


def layout(title: str, body_class: str, current_path: str, content: str, description: str | None = None) -> str:
    description = description or site["description"]
    document_title = f"{site['name']} | {site['title_suffix']}" if title == site["name"] else f"{title} | {site['title_suffix']}"

    base_url = "https://maxsepulvedaartevisual.com"
    canonical = f"{base_url}{current_path}"
    image_url = f"{base_url}/assets/images/max-sepulveda-retrato.png"

    json_ld = f"""{{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{html(site['name'])}",
  "givenName": "Maximiliano",
  "familyName": "Sepúlveda Zúñiga",
  "jobTitle": "Artista visual, artesano y gestor cultural",
  "description": "{attr(description)}",
  "email": "{html(site['email'])}",
  "telephone": "{html(site['phone_link'])}",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "San Vicente de Tagua Tagua",
    "addressCountry": "Chile"
  }},
  "url": "{base_url}",
  "image": "{image_url}",
  "sameAs": [
    "https://www.instagram.com/maxartepopular/",
    "https://www.facebook.com/MaxArteVisual/",
    "https://www.youtube.com/@Warisdey1974",
    "https://mercadocul.cultura.gob.cl/agente-cultural/maxsepulveda/"
  ]
}}"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html(document_title)}</title>
    <meta name="description" content="{attr(description)}">
    <link rel="canonical" href="{canonical}">

    <meta property="og:title" content="{html(document_title)}">
    <meta property="og:description" content="{attr(description)}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{image_url}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">

    <script type="application/ld+json">{json_ld}</script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="icon" href="{asset_url(current_path, 'assets/images/favicon.svg')}" type="image/svg+xml">
    <link rel="stylesheet" href="{asset_url(current_path, 'assets/css/main.css')}">
    <link rel="stylesheet" href="{asset_url(current_path, 'assets/css/prose.css')}">
</head>
<body class="{attr(body_class)} static-site">
    <a href="#contenido" class="skip-link">Saltar al contenido</a>
    <header class="site-header">
        <nav class="nav-container" aria-label="Navegación principal">
            <a href="{page_url(current_path, '/es/')}" class="logo">Max Sepúlveda</a>
            <ul class="nav-menu">
                {nav_item(current_path, '/es/', 'Inicio')}
                {nav_item(current_path, '/es/sobre-max/', 'Sobre Max')}
                {nav_item(current_path, '/es/proyectos/', 'Proyectos')}
            </ul>
            <div class="header-contact">
                <a href="mailto:{html(site['email'])}" class="header-contact__item header-contact__email">{html(site['email'])}</a>
                <a href="tel:{html(site['phone_link'])}" class="header-contact__item header-contact__phone">{html(site['phone'])}</a>
            </div>
            <button class="menu-toggle" aria-label="Menú de navegación" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
        </nav>
    </header>
    <main class="main-content" id="contenido">
        {content if content.strip().startswith('<div class="sf-stack') else f'<div class="sf-stack">{content}</div>'}
    </main>
    <footer class="site-footer">
        <div class="footer-container">
            <div class="footer-grid">
                <div class="footer-info">
                    <p class="footer-brand">{html(site['name'])}</p>
                    <p class="footer-tagline">{html(site['tagline'])}</p>
                </div>
                <div class="footer-contact">
                    <a href="mailto:{html(site['email'])}" class="footer-link">{html(site['email'])}</a>
                    <a href="tel:{html(site['phone_link'])}" class="footer-link">{html(site['phone'])}</a>
                    <span class="footer-location">{html(site['location'])}</span>
                </div>
            </div>
            <p class="footer-copy">&copy; {html(site['year'])} {html(site['name'])}. Todos los derechos reservados.</p>
        </div>
    </footer>
    <script src="{asset_url(current_path, 'assets/js/main.js')}" defer></script>
</body>
</html>
"""


def nav_item(current_path: str, target_path: str, label: str) -> str:
    is_active = current_path == target_path if target_path == "/es/" else current_path.startswith(target_path)
    current = ' aria-current="page"' if is_active else ""
    return f'<li><a href="{page_url(current_path, target_path)}"{current}>{html(label)}</a></li>'


def render_home_page() -> str:
    return layout(
        title=site["name"],
        body_class="home-page",
        current_path="/es/",
        content=render_blocks(home_blocks, "/es/"),
    )


def render_about_page() -> str:
    current_path = "/es/sobre-max/"
    return layout(
        title=about_page["title"],
        body_class="about-page",
        current_path=current_path,
        content=render_blocks(about_page["blocks"], current_path),
        description=about_page.get("description"),
    )


def render_projects_index() -> str:
    current_path = "/es/proyectos/"
    cards = "\n".join(render_project_card(project, 2, current_path) for project in projects)
    other_items = "".join(f"<li>{html(item)}</li>" for item in other_workshops)
    header_image = asset_url(current_path, "assets/images/proyectos-header.jpg")
    content = f"""
<section class="page-header page-header--image">
    <div class="page-header__background" aria-hidden="true" style="background-image: url('{header_image}');"></div>
    <div class="page-header__scrim" aria-hidden="true"></div>
    <div class="container page-header__content">
        <p class="page-header__kicker">Portafolio</p>
        <h1>Proyectos</h1>
        <div class="intro"><p>Una selección de trabajos en arte comunitario, textil, cerámica, investigación patrimonial, circulación internacional y gestión cultural.</p></div>
    </div>
</section>
<section class="projects-section">
    <div class="container">
        <div class="projects-grid">
            {cards}
        </div>
    </div>
</section>
<section class="sf-block sf-block--simple-list">
    <div class="sf-container">
        <div class="sf-section-header">
            <p class="sf-section-header__kicker">Registro</p>
            <h2 class="sf-section-header__title">Otros talleres y residencias</h2>
            <p class="sf-section-header__subtitle">Procesos y residencias de arte colaborativo realizados en distintos territorios.</p>
        </div>
        <ul class="simple-list">{other_items}</ul>
    </div>
</section>"""
    return layout("Proyectos", "projects-index", current_path, content)


def render_project_detail(project: dict) -> str:
    current_path = f"/es/proyectos/{project['slug']}/"
    project_link = ""
    if project.get("live_url"):
        project_link = f'<div class="project-links"><a href="{attr(project["live_url"])}" target="_blank" rel="noopener" class="btn btn-primary">Ver proyecto</a></div>'

    gallery_html = ""
    if project.get("gallery"):
        items = "\n".join(
            f'<figure class="sf-gallery__item"><a href="{asset_url(current_path, img)}" class="sf-gallery__link" target="_blank">{render_image(current_path, img, "")}</a></figure>'
            for img in project["gallery"]
        )
        gallery_html = f'<section class="sf-block sf-block--gallery"><div class="sf-container"><div class="sf-gallery sf-gallery--cols-masonry">{items}</div></div></section>'

    content = f"""
<article class="project-detail">
    <header class="project-header">
        <div class="container">
            <p class="project-header__kicker">Proyecto</p>
            <h1>{html(project['title'])}</h1>
            <p class="summary">{html(project['summary'])}</p>
            <div class="project-meta">
                <time datetime="{project['date']}">{format_date(project['date'])}</time>
                {render_tags(project.get('tags', []), '/es/proyectos/', current_path)}
            </div>
            {project_link}
        </div>
    </header>
    <div class="project-content">
        {render_blocks(project['content'], current_path)}
    </div>
    {gallery_html}
    <footer class="project-footer container">
        <a href="{page_url(current_path, '/es/proyectos/')}" class="btn">&larr; Volver a proyectos</a>
    </footer>
</article>"""
    return layout(project["title"], "project-detail", current_path, content, project["summary"])


def render_blocks(blocks: list[dict], current_path: str) -> str:
    rendered = "\n".join(render_block(block, current_path) for block in blocks)
    return f'<div class="sf-stack">{rendered}</div>'


def render_block(block: dict, current_path: str) -> str:
    block_type = block["type"]
    if block_type == "hero":
        return render_hero(block, current_path)
    if block_type == "text_section":
        return render_text_section(block, current_path)
    if block_type == "portfolio_grid":
        return render_portfolio_grid(block, current_path)
    if block_type == "skills":
        return render_skills(block, current_path)
    if block_type == "discipline_showcase":
        return render_discipline_showcase(block, current_path)
    if block_type == "timeline":
        return render_timeline(block, current_path)
    if block_type == "contact":
        return render_contact(block)
    if block_type == "quote":
        return render_quote(block)
    if block_type == "name_list":
        return render_name_list(block)
    if block_type == "dated_list":
        return render_dated_list(block)
    return ""


def render_hero(block: dict, current_path: str) -> str:
    variant = block.get("variant", "default")
    variant_class = f" sf-block--hero--{variant}" if variant != "default" else ""
    background_class_modifier = " sf-hero--with-background" if block.get("background_image") else ""

    background = ""
    if block.get("background_image"):
        background_class = attr(block.get("background_class", ""))
        background_style = f' style="background-image: url(\'{asset_url(current_path, block["background_image"])}\');"'
        background = f'<div class="sf-hero__background {background_class}" aria-hidden="true"{background_style}></div>'

    cta = ""
    if block.get("cta"):
        cta = f"""<div class="sf-hero__cta"><a href="{site_url(current_path, block['cta']['url'])}" class="btn btn-primary">{html(block['cta']['text'])}</a></div>"""

    portrait = ""
    if block.get("portrait_image"):
        portrait = f'<div class="sf-hero__portrait" role="img" aria-label="{attr(block.get("portrait_alt", block["title"]))}" style="background-image: url(\'{asset_url(current_path, block["portrait_image"])}\');"></div>'

    scroll_cue = ""
    if variant == "minimal":
        scroll_cue = """<a class="sf-hero__scroll" href="#alfareria" aria-label="Bajar al contenido"><span class="sf-hero__scroll-label">Explorar</span><span class="sf-hero__scroll-line" aria-hidden="true"></span></a>"""

    content = f"""<div class="sf-container sf-hero__layout">
        <div class="sf-hero__content">
            <h1 class="sf-hero__title">{html(block['title'])}</h1>
            <p class="sf-hero__subtitle">{html(block['subtitle'])}</p>
            {cta}
        </div>
        {portrait}
    </div>
    {scroll_cue}"""

    return f"""<section class="sf-block sf-block--hero{background_class_modifier}{variant_class}">
    {background}
    {content}
</section>"""


def render_discipline_showcase(block: dict, current_path: str) -> str:
    header = f"""<section class="sf-block sf-block--discipline-intro">
    <div class="sf-container">
        <div class="sf-section-header">
            <p class="sf-section-header__kicker">Max Sepúlveda</p>
            <h2 class="sf-section-header__title">{html(block['title'])}</h2>
            <p class="sf-section-header__subtitle">{html(block['subtitle'])}</p>
        </div>
    </div>
</section>"""
    sections = []
    for index, discipline in enumerate(disciplines, start=1):
        number = f"{index:02d}"
        image_url = asset_url(current_path, discipline["image"])
        panel_variant = discipline.get("panel", "fullbleed")
        if panel_variant == "plate":
            sections.append(
                f"""<section class="sf-block sf-block--discipline-panel discipline-panel--plate" id="{attr(discipline['anchor'])}">
    <div class="discipline-panel__image" aria-hidden="true" style="background-image: url('{image_url}');"></div>
    <div class="discipline-panel__overlay" aria-hidden="true"></div>
    <div class="sf-container discipline-panel__content discipline-panel__content--split">
        <div class="discipline-panel__text-col">
            <p class="discipline-panel__kicker"><span class="discipline-panel__num">{number}</span>Obra y oficio</p>
            <h2 class="discipline-panel__title">{html(discipline['name'])}</h2>
            <p class="discipline-panel__text">{html(discipline['description'])}</p>
        </div>
        <figure class="discipline-panel__plate">
            {render_image(current_path, discipline['image'], discipline['name'])}
        </figure>
    </div>
</section>"""
            )
        else:
            sections.append(
                f"""<section class="sf-block sf-block--discipline-panel" id="{attr(discipline['anchor'])}">
    <div class="discipline-panel__image" aria-hidden="true" style="background-image: url('{image_url}');"></div>
    <div class="discipline-panel__overlay" aria-hidden="true"></div>
    <div class="sf-container discipline-panel__content">
        <p class="discipline-panel__kicker"><span class="discipline-panel__num">{number}</span>Obra y oficio</p>
        <h2 class="discipline-panel__title">{html(discipline['name'])}</h2>
        <p class="discipline-panel__text">{html(discipline['description'])}</p>
    </div>
</section>"""
            )
    return header + "\n" + "\n".join(sections)


def render_text_section(block: dict, current_path: str) -> str:
    title = f'<h2 class="sf-text__title">{html(block["title"])}</h2>' if block.get("title") else ""
    image = ""
    text_class = "sf-text"
    variant = block.get("variant", "default")
    variant_class = f" sf-block--text--{attr(variant)}" if variant != "default" else ""
    if block.get("image"):
        text_class = f'sf-text sf-text--with-image sf-text--image-{attr(block.get("image_position", "right"))}'
        image = f"""<div class="sf-text__image">
                {render_image(current_path, block['image'], block.get('image_alt', block.get('title', 'Imagen')))}
            </div>"""
    return f"""<section class="sf-block sf-block--text{variant_class}">
    <div class="sf-container">
        <div class="{text_class}">
            <div class="sf-text__content">
                {title}
                <div class="sf-text__body prose">{block['content']}</div>
            </div>
            {image}
        </div>
    </div>
</section>"""


def render_portfolio_grid(block: dict, current_path: str) -> str:
    visible = [p for p in projects if p.get("featured")] if block.get("show_featured_only") else projects
    visible = visible[: block.get("max_items", len(visible))]
    cards = "\n".join(render_project_card(p, 3, current_path) for p in visible)
    footer = f'<div class="sf-section-footer"><a href="{page_url(current_path, "/es/proyectos/")}" class="btn btn-outline">Ver todos los proyectos &rarr;</a></div>' if block.get("show_link_to_all") else ""
    return f"""<section class="sf-block sf-block--portfolio-grid">
    <div class="sf-container">
        <div class="sf-section-header">
            <p class="sf-section-header__kicker">Selección</p>
            <h2 class="sf-section-header__title">{html(block['title'])}</h2>
            <p class="sf-section-header__subtitle">{html(block['subtitle'])}</p>
        </div>
        <div class="sf-portfolio-grid projects-grid">
            {cards}
        </div>
        {footer}
    </div>
</section>"""


def render_skills(block: dict, current_path: str) -> str:
    items = "\n".join(render_skill_card(d) for d in disciplines)
    return f"""<section class="sf-block sf-block--skills">
    <div class="sf-container">
        <div class="sf-section-header">
            <h2 class="sf-section-header__title">{html(block['title'])}</h2>
            <p class="sf-section-header__subtitle">{html(block['subtitle'])}</p>
        </div>
        <div class="skills-grid">
            {items}
        </div>
    </div>
</section>"""


def render_skill_card(discipline: dict) -> str:
    icon_html = skill_icon(discipline["icon"])
    return f"""<div class="skill-card">
    <div class="skill-card__icon">{icon_html}</div>
    <h3 class="skill-card__name">{html(discipline['name'])}</h3>
    <p class="skill-card__desc">{html(discipline['description'])}</p>
</div>"""


def render_timeline(block: dict, current_path: str) -> str:
    items = milestones[: block.get("max_items", len(milestones))]
    rendered_items = "\n".join(
        f"""<div class="timeline__item">
    <div class="timeline__dot"></div>
    <div class="timeline__year">{html(m["year"])}</div>
    <h3 class="timeline__title">{html(m["title"])}</h3>
    <p class="timeline__desc">{html(m["description"])}</p>
</div>"""
        for m in items
    )
    return f"""<section class="sf-block sf-block--timeline">
    <div class="sf-container">
        <div class="sf-section-header">
            <h2 class="sf-section-header__title">{html(block['title'])}</h2>
            <p class="sf-section-header__subtitle">{html(block['subtitle'])}</p>
        </div>
        <div class="timeline">
            {rendered_items}
        </div>
    </div>
</section>"""


def render_name_list(block: dict) -> str:
    items = "".join(f"<li>{html(item)}</li>" for item in block["items"])
    return f"""<section class="sf-block sf-block--name-list">
    <div class="sf-container">
        <div class="sf-section-header">
            <h2 class="sf-section-header__title">{html(block['title'])}</h2>
            <p class="sf-section-header__subtitle">{html(block['subtitle'])}</p>
        </div>
        <ul class="name-list">{items}</ul>
    </div>
</section>"""


def render_dated_list(block: dict) -> str:
    items = "".join(
        f"""<li class="dated-list__item"><span class="dated-list__year">{html(item['year'])}</span><span class="dated-list__title">{html(item['title'])}</span></li>"""
        for item in block["items"]
    )
    return f"""<section class="sf-block sf-block--dated-list">
    <div class="sf-container">
        <div class="sf-section-header">
            <h2 class="sf-section-header__title">{html(block['title'])}</h2>
            <p class="sf-section-header__subtitle">{html(block['subtitle'])}</p>
        </div>
        <ul class="dated-list">{items}</ul>
    </div>
</section>"""


def render_contact(block: dict) -> str:
    links = "\n".join(render_social_link(link) for link in block.get("social_links", []))
    phone_html = ""
    if block.get("phone") and block.get("phone_link"):
        phone_html = f'<div class="sf-contact__phone"><a href="tel:{attr(block["phone_link"])}" class="sf-contact__phone-link">{html(block["phone"])}</a></div>'
    return f"""<section class="sf-block sf-block--contact">
    <div class="sf-container">
        <div class="sf-contact">
            <h2 class="sf-contact__title">{html(block['title'])}</h2>
            <p class="sf-contact__text">{html(block['text'])}</p>
            <div class="sf-contact__email"><a href="mailto:{attr(block['email'])}" class="sf-contact__email-link">{html(block['email'])}</a></div>
            {phone_html}
            <div class="sf-contact__social">{links}</div>
        </div>
    </div>
</section>"""


def render_quote(block: dict) -> str:
    author = f'<cite class="sf-quote__author">&mdash; {html(block["author"])}</cite>' if block.get("author") else ""
    source = f'<span class="sf-quote__source">{html(block["source"])}</span>' if block.get("source") else ""
    return f"""<section class="sf-block sf-block--quote">
    <blockquote class="sf-quote">
        <p class="sf-quote__text">{html(block['quote'])}</p>
        <footer class="sf-quote__footer">{author}{source}</footer>
    </blockquote>
</section>"""


def render_project_card(project: dict, heading_level: int, current_path: str) -> str:
    project_url = page_url(current_path, f"/es/proyectos/{project['slug']}/")
    tags = project.get("tags", [])[:3]
    tags_html = f'<p class="project-card__tags">{html(" · ".join(tags))}</p>' if tags else ""
    year = project.get("date", "")[:4]
    year_html = f'<span class="project-card__year">{html(year)}</span>' if year else ""
    img_html = ""
    if project.get("image"):
        img_html = render_image(current_path, project["image"], "")
    return f"""<article class="project-card">
    <a href="{project_url}" class="project-card__link">
        <div class="project-card__media">{img_html}</div>
        <div class="project-card__veil" aria-hidden="true"></div>
        <div class="project-card__body">
            {tags_html}
            <h{heading_level} class="project-card__title">{html(project['title'])}</h{heading_level}>
            <p class="project-card__summary">{html(truncate_words(project['summary'], 18))}</p>
            <span class="project-card__cta">Ver proyecto<span class="project-card__cta-arrow" aria-hidden="true">&rarr;</span></span>
        </div>
        {year_html}
    </a>
</article>"""


def render_tags(tags: list[str], base_path: str, current_path: str) -> str:
    if not tags:
        return ""
    links = "".join(f'<span class="tag">{html(tag)}</span>' for tag in tags)
    return f'<div class="tags">{links}</div>'


def render_social_link(link: dict) -> str:
    return (
        f'<a href="{attr(link["url"])}" class="sf-social-link sf-social-link--{attr(link["platform"])}" '
        f'target="_blank" rel="noopener noreferrer" aria-label="{attr(link["label"])}">{social_icon(link["platform"])}</a>'
    )


def social_icon(platform: str) -> str:
    if platform == "instagram":
        return '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>'
    if platform == "youtube":
        return '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>'
    if platform == "facebook":
        return '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M24 12.073C24 5.405 18.627 0 12 0S0 5.405 0 12.073C0 18.1 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047V9.414c0-3.025 1.792-4.697 4.533-4.697 1.312 0 2.686.236 2.686.236v2.97h-1.513c-1.49 0-1.956.931-1.956 1.886v2.264h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.1 24 12.073z"/></svg>'
    return '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>'


def skill_icon(icon_type: str) -> str:
    icons = {
        "pottery": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M24 6c-6 0-7 4-7 7v4c0 3-2 5-4 6-3 2-5 5-5 8 0 5 5 9 16 11 11-2 16-6 16-11 0-3-2-6-5-8-2-1-4-3-4-6v-4c0-3-1-7-7-7z"/><path d="M17 13h14"/></svg>',
        "ceramic": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M24 6C14 6 10 12 10 20c0 8 4 14 14 14s14-6 14-14c0-8-4-14-14-14z"/><path d="M24 20L14 38"/><path d="M24 20l10 18"/><path d="M18 34l-2 8"/><path d="M30 34l2 8"/></svg>',
        "embroidery": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 40c8-8 12-16 16-16s8 8 16 16"/><path d="M8 8c8 8 12 16 16 16s8-8 16-16"/><path d="M24 24L8 8"/><path d="M24 24l16 16"/><path d="M24 24l-8 16"/><path d="M24 24l8-16"/><path d="M24 24l16-8"/><path d="M24 24L8 32"/></svg>',
        "weaving": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 6v36"/><path d="M40 6v36"/><path d="M8 12h32"/><path d="M8 20h32"/><path d="M8 28h32"/><path d="M8 36h32"/><path d="M18 6v36"/><path d="M30 6v36"/></svg>',
        "batik": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="36" height="36" rx="2"/><path d="M24 6v36"/><path d="M6 24h36"/><circle cx="24" cy="24" r="6"/><circle cx="16" cy="16" r="3"/><circle cx="32" cy="32" r="3"/></svg>',
        "video": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="28" height="28" rx="3"/><path d="M32 20l10-6v20l-10-6"/></svg>',
    }
    return icons.get(icon_type, "")


def parse_date(date_string: str) -> date:
    return date.fromisoformat(date_string)


def format_date(date_string: str) -> str:
    parsed = parse_date(date_string)
    return f"{parsed.day} de {SPANISH_MONTHS[parsed.month - 1]} de {parsed.year}"


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


def render_image(current_path: str, image_path: str, alt: str) -> str:
    """Renderiza <img loading="lazy" width height>, envuelto en <picture> con
    fuente WebP cuando `scripts/optimize_images.py` ya registro esa imagen en
    src/image_manifest.json. Si aun no fue procesada, cae a un <img> simple."""
    normalized = image_path.strip("/")
    meta = IMAGE_MANIFEST.get(normalized)
    src = asset_url(current_path, normalized)
    dims = ""
    if meta and meta.get("width") and meta.get("height"):
        dims = f' width="{meta["width"]}" height="{meta["height"]}"'
    img_html = f'<img src="{src}" alt="{attr(alt)}" loading="lazy"{dims}>'
    if meta and meta.get("webp"):
        webp_path = re.sub(r"\.(jpe?g|png)$", ".webp", normalized, flags=re.IGNORECASE)
        webp_src = asset_url(current_path, webp_path)
        return f'<picture><source srcset="{webp_src}" type="image/webp">{img_html}</picture>'
    return img_html


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
