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

from site_data import events, home_blocks, posts, projects, site  # noqa: E402

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
    write_page("es/proyectos", render_projects_index())
    for project in projects:
        write_page(f"es/proyectos/{project['slug']}", render_project_detail(project))
    write_page("es/eventos", render_events_index())
    for event in events:
        write_page(f"es/eventos/{event['slug']}", render_event_detail(event))
    write_page("es/blog", render_blog_index())
    for post in posts:
        write_page(f"es/blog/{post['slug']}", render_blog_detail(post))


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
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html(document_title)}</title>
    <meta name="description" content="{attr(description)}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Source+Sans+3:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
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
                {nav_item(current_path, '/es/proyectos/', 'Proyectos')}
                {nav_item(current_path, '/es/blog/', 'Blog')}
                {nav_item(current_path, '/es/eventos/', 'Eventos')}
            </ul>
            <div class="language-switcher" aria-label="Idioma">
                <a href="{page_url(current_path, '/es/')}" class="lang-link active" hreflang="es">ES</a>
            </div>
        </nav>
    </header>
    <main class="main-content" id="contenido">
        {content}
    </main>
    <footer class="site-footer">
        <div class="footer-container">
            <p class="footer-brand">{html(site['name'])}</p>
            <p class="footer-tagline">{html(site['tagline'])}</p>
            <p class="footer-copy">&copy; {html(site['year'])} Todos los derechos reservados.</p>
        </div>
    </footer>
    <script src="{asset_url(current_path, 'assets/js/main.js')}"></script>
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
        content=f'<div class="sf-stack">{render_blocks(home_blocks, "/es/")}</div>',
    )


def render_projects_index() -> str:
    current_path = "/es/proyectos/"
    cards = "\n".join(render_project_card(project, 2, current_path) for project in projects)
    content = f"""
<section class="page-header">
    <div class="container">
        <h1>Proyectos</h1>
        <div class="intro prose prose-wide"><p>Una selección de trabajos en arte comunitario, textil, cerámica, investigación patrimonial y gestión cultural.</p></div>
    </div>
</section>
<section class="projects-section">
    <div class="container">
        <div class="projects-grid">
            {cards}
        </div>
    </div>
</section>"""
    return layout("Proyectos", "projects-index", current_path, content)


def render_project_detail(project: dict) -> str:
    current_path = f"/es/proyectos/{project['slug']}/"
    project_link = ""
    if project.get("live_url"):
        project_link = f'<div class="project-links"><a href="{attr(project["live_url"])}" target="_blank" rel="noopener" class="btn btn-primary">Ver proyecto</a></div>'
    content = f"""
<article class="project-detail">
    <header class="project-header">
        <div class="container">
            <h1>{html(project['title'])}</h1>
            <p class="summary">{html(project['summary'])}</p>
            <div class="project-meta">
                <time datetime="{project['date']}">{format_date(project['date'])}</time>
                {render_tags(project.get('tags', []), '/es/proyectos/', current_path)}
            </div>
            {project_link}
        </div>
    </header>
    <div class="sf-stack project-content">
        {render_blocks(project['content'], current_path)}
    </div>
    <footer class="project-footer container">
        <a href="{page_url(current_path, '/es/proyectos/')}" class="btn">&larr; Volver a proyectos</a>
    </footer>
</article>"""
    return layout(project["title"], "project-detail", current_path, content, project["summary"])


def render_events_index() -> str:
    current_path = "/es/eventos/"
    sorted_events = sorted(events, key=lambda event: event["start_date"], reverse=True)
    cards = "\n".join(render_event_card(event, 2, current_path) for event in sorted_events)
    content = f"""
<section class="page-header">
    <div class="container">
        <h1>Eventos</h1>
        <div class="intro prose prose-wide"><p>Exposiciones, residencias, talleres y participaciones que forman parte de la trayectoria de Max Sepúlveda.</p></div>
    </div>
</section>
<section class="events-section">
    <div class="container">
        <div class="events-filter" aria-label="Filtro de eventos">
            <a href="{page_url(current_path, '/es/eventos/')}" class="active">Pasados</a>
        </div>
        <div class="events-list">
            {cards}
        </div>
    </div>
</section>"""
    return layout("Eventos", "events-index", current_path, content)


def render_event_detail(event: dict) -> str:
    current_path = f"/es/eventos/{event['slug']}/"
    date_range = format_date(event["start_date"])
    if event["end_date"] != event["start_date"]:
        date_range = f"{date_range} - {format_date(event['end_date'])}"
    content = f"""
<article class="event-detail">
    <header class="event-header">
        <div class="container">
            <span class="badge badge-past">Evento pasado</span>
            <h1>{html(event['title'])}</h1>
            <p class="summary">{html(event['summary'])}</p>
            <div class="event-meta">
                <div class="event-datetime"><strong>Fecha:</strong> {date_range}</div>
                <div class="event-location"><strong>{html(event['location_name'])}</strong></div>
            </div>
        </div>
    </header>
    <div class="event-body container prose">
        {event['description']}
    </div>
    <div class="event-tags container">
        {render_tags(event.get('tags', []), '/es/eventos/', current_path)}
    </div>
    <footer class="event-footer container">
        <a href="{page_url(current_path, '/es/eventos/')}" class="btn">&larr; Volver a eventos</a>
    </footer>
</article>"""
    return layout(event["title"], "event-detail", current_path, content, event["summary"])


def render_blog_index() -> str:
    current_path = "/es/blog/"
    sorted_posts = sorted(posts, key=lambda post: post["date"], reverse=True)
    cards = "\n".join(render_post_card(post, current_path) for post in sorted_posts)
    content = f"""
<section class="page-header">
    <div class="container">
        <h1>Blog</h1>
        <p class="intro">Notas, registros y reflexiones sobre arte comunitario, oficios textiles, cerámica y gestión cultural.</p>
    </div>
</section>
<section class="posts-section">
    <div class="container">
        <div class="posts-list">
            {cards}
        </div>
    </div>
</section>"""
    return layout("Blog", "blog-index", current_path, content)


def render_blog_detail(post: dict) -> str:
    current_path = f"/es/blog/{post['slug']}/"
    content = f"""
<article class="post-detail">
    <header class="post-header">
        <div class="container">
            <time datetime="{post['date']}">{format_date(post['date'])}</time>
            <h1>{html(post['title'])}</h1>
            <p class="intro">{html(post['intro'])}</p>
            {render_tags(post.get('tags', []), '/es/blog/', current_path)}
        </div>
    </header>
    <div class="post-content">
        {render_blocks(post['body'], current_path)}
    </div>
    <footer class="post-footer container">
        <a href="{page_url(current_path, '/es/blog/')}" class="btn">&larr; Volver al blog</a>
    </footer>
</article>"""
    return layout(post["title"], "blog-post", current_path, content, post["intro"])


def render_blocks(blocks: list[dict], current_path: str) -> str:
    return "\n".join(render_block(block, current_path) for block in blocks)


def render_block(block: dict, current_path: str) -> str:
    block_type = block["type"]
    if block_type == "hero":
        return render_hero(block, current_path)
    if block_type == "text_section":
        return render_text_section(block)
    if block_type == "portfolio_grid":
        return render_portfolio_grid(block, current_path)
    if block_type == "events_list":
        return render_events_list(block, current_path)
    if block_type == "contact":
        return render_contact(block)
    if block_type == "quote":
        return render_quote(block)
    return ""


def render_hero(block: dict, current_path: str) -> str:
    return f"""<section class="sf-block sf-block--hero sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container sf-hero__content">
        <h1 class="sf-hero__title">{html(block['title'])}</h1>
        <p class="sf-hero__subtitle">{html(block['subtitle'])}</p>
        <div class="sf-hero__cta"><a href="{site_url(current_path, block['cta']['url'])}" class="btn btn-primary">{html(block['cta']['text'])}</a></div>
    </div>
</section>"""


def render_text_section(block: dict) -> str:
    title = f'<h2 class="sf-text__title">{html(block["title"])}</h2>' if block.get("title") else ""
    return f"""<section class="sf-block sf-block--text sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container">
        <div class="sf-text">
            <div class="sf-text__content">
                {title}
                <div class="sf-text__body prose">{block['content']}</div>
            </div>
        </div>
    </div>
</section>"""


def render_portfolio_grid(block: dict, current_path: str) -> str:
    visible_projects = [project for project in projects if project.get("featured")] if block.get("show_featured_only") else projects
    visible_projects = visible_projects[: block.get("max_items", len(visible_projects))]
    cards = "\n".join(render_project_card(project, 3, current_path) for project in visible_projects)
    footer = f'<div class="sf-section-footer"><a href="{page_url(current_path, "/es/proyectos/")}" class="btn">Ver todos los proyectos</a></div>' if block.get("show_link_to_all") else ""
    return f"""<section class="sf-block sf-block--portfolio-grid sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container">
        <div class="sf-section-header">
            <h2 class="sf-section-header__title">{html(block['title'])}</h2>
            <p class="sf-section-header__subtitle">{html(block['subtitle'])}</p>
        </div>
        <div class="sf-portfolio-grid projects-grid">
            {cards}
        </div>
        {footer}
    </div>
</section>"""


def render_events_list(block: dict, current_path: str) -> str:
    sorted_events = sorted(events, key=lambda event: event["start_date"], reverse=True)
    visible_events = sorted_events[: block.get("max_items", len(sorted_events))]
    cards = "\n".join(render_compact_event_card(event, current_path) for event in visible_events)
    footer = f'<div class="sf-section-footer"><a href="{page_url(current_path, "/es/eventos/")}" class="btn">Ver todos los eventos</a></div>' if block.get("show_link_to_all") else ""
    return f"""<section class="sf-block sf-block--events-list sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container">
        <div class="sf-section-header">
            <h2 class="sf-section-header__title">{html(block['title'])}</h2>
            <p class="sf-section-header__subtitle">{html(block['subtitle'])}</p>
        </div>
        <div class="sf-events-list events-list">
            {cards}
        </div>
        {footer}
    </div>
</section>"""


def render_contact(block: dict) -> str:
    links = "\n".join(render_social_link(link) for link in block.get("social_links", []))
    return f"""<section class="sf-block sf-block--contact sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container">
        <div class="sf-contact">
            <h2 class="sf-contact__title">{html(block['title'])}</h2>
            <p class="sf-contact__text">{html(block['text'])}</p>
            <div class="sf-contact__email"><a href="mailto:{attr(block['email'])}" class="sf-contact__email-link">{html(block['email'])}</a></div>
            <div class="sf-contact__social">{links}</div>
        </div>
    </div>
</section>"""


def render_quote(block: dict) -> str:
    author = f'<cite class="sf-quote__author">&mdash; {html(block["author"])}</cite>' if block.get("author") else ""
    source = f'<span class="sf-quote__source">{html(block["source"])}</span>' if block.get("source") else ""
    return f"""<section class="sf-block sf-block--quote sf-variant--{variant(block.get('variant'))}">
    <div class="sf-container">
        <blockquote class="sf-quote">
            <p class="sf-quote__text">{html(block['quote'])}</p>
            <footer class="sf-quote__footer">{author}{source}</footer>
        </blockquote>
    </div>
</section>"""


def render_project_card(project: dict, heading_level: int, current_path: str) -> str:
    return f"""<article class="project-card project-card--no-image">
    <div class="project-info">
        <h{heading_level}><a href="{page_url(current_path, f"/es/proyectos/{project['slug']}/")}">{html(project['title'])}</a></h{heading_level}>
        <p>{html(truncate_words(project['summary'], 25))}</p>
        {render_tags(project.get('tags', [])[:4], '/es/proyectos/', current_path)}
    </div>
</article>"""


def render_post_card(post: dict, current_path: str) -> str:
    return f"""<article class="post-item post-item--no-image">
    <div class="post-content">
        <time datetime="{post['date']}">{format_date(post['date'])}</time>
        <h2><a href="{page_url(current_path, f"/es/blog/{post['slug']}/")}">{html(post['title'])}</a></h2>
        <p>{html(post['intro'])}</p>
        {render_tags(post.get('tags', []), '/es/blog/', current_path)}
    </div>
</article>"""


def render_event_card(event: dict, heading_level: int, current_path: str) -> str:
    return f"""<article class="event-card event-card--no-image">
    <div class="event-info">
        {render_date_tile(event['start_date'])}
        <div class="event-details">
            <h{heading_level}><a href="{page_url(current_path, f"/es/eventos/{event['slug']}/")}">{html(event['title'])}</a></h{heading_level}>
            <p class="event-location">{html(event['location_name'])}</p>
            <p>{html(truncate_words(event['summary'], 22))}</p>
        </div>
    </div>
</article>"""


def render_compact_event_card(event: dict, current_path: str) -> str:
    return f"""<article class="event-card event-card--compact">
    {render_date_tile(event['start_date'])}
    <div class="event-details">
        <h3><a href="{page_url(current_path, f"/es/eventos/{event['slug']}/")}">{html(event['title'])}</a></h3>
        <p class="event-summary">{html(truncate_words(event['summary'], 20))}</p>
        <p class="event-location">{html(event['location_name'])}</p>
    </div>
</article>"""


def render_date_tile(date_string: str) -> str:
    parsed = parse_date(date_string)
    month = SPANISH_MONTHS[parsed.month - 1][:3]
    return f'<div class="event-date"><span class="day">{parsed.day:02d}</span><span class="month">{html(month)}</span></div>'


def render_tags(tags: list[str], base_path: str, current_path: str) -> str:
    if not tags:
        return ""
    links = "".join(f'<a href="{page_url(current_path, base_path)}" class="tag">{html(tag)}</a>' for tag in tags)
    return f'<div class="tags">{links}</div>'


def render_social_link(link: dict) -> str:
    return (
        f'<a href="{attr(link["url"])}" class="sf-social-link sf-social-link--{attr(link["platform"])}" '
        f'target="_blank" rel="noopener noreferrer" aria-label="{attr(link["label"])}">{social_icon(link["platform"])}</a>'
    )


def social_icon(platform: str) -> str:
    if platform == "instagram":
        return '<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>'
    return '<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>'


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