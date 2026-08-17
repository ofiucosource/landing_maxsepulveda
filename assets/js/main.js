/**
 * Max Sepúlveda — Interacciones del sitio
 * Header con estado de scroll, menú móvil y reveals editoriales.
 */

document.addEventListener('DOMContentLoaded', function () {
    initMobileMenu();
    initActiveNavigation();
    initSmoothScroll();
    initHeaderScrollState();
    initScrollReveals();
});

/**
 * Marca la navegación activa en rutas estáticas
 */
function initActiveNavigation() {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.nav-menu a');

    links.forEach(function (link) {
        if (link.hasAttribute('aria-current')) {
            return;
        }

        const href = new URL(link.getAttribute('href'), window.location.href).pathname;
        const isHome = href.endsWith('/es/') || href.endsWith('/en/') || href.endsWith('/es') || href.endsWith('/en');
        const isActive = isHome ? currentPath === href : currentPath.startsWith(href);

        if (isActive) {
            link.setAttribute('aria-current', 'page');
        }
    });
}

/**
 * Menú móvil
 */
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function () {
            const isOpen = navMenu.classList.toggle('active');
            menuToggle.setAttribute('aria-expanded', String(isOpen));
        });
    }
}

/**
 * Scroll suave para anclas
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');

            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);

                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

/**
 * Header: transparente sobre héroes oscuros, sólido al hacer scroll
 */
function initHeaderScrollState() {
    const header = document.querySelector('.site-header');
    if (!header) {
        return;
    }

    let ticking = false;

    function update() {
        header.classList.toggle('is-scrolled', window.scrollY > 32);
        ticking = false;
    }

    window.addEventListener('scroll', function () {
        if (!ticking) {
            window.requestAnimationFrame(update);
            ticking = true;
        }
    }, { passive: true });

    update();
}

/**
 * Reveals editoriales con IntersectionObserver
 */
function initScrollReveals() {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion || !('IntersectionObserver' in window)) {
        return;
    }

    const revealSelectors = [
        '.sf-section-header',
        '.sf-text',
        '.project-card',
        '.timeline__item',
        '.sf-quote',
        '.sf-contact',
        '.dated-list',
        '.name-list',
        '.simple-list',
        '.sf-gallery__item',
        '.gallery-grid figure',
        '.discipline-panel__content',
        '.project-header .container',
        '.page-header__content'
    ];

    const targets = document.querySelectorAll(revealSelectors.join(','));

    const revealObserver = new IntersectionObserver(function (entries, observer) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px'
    });

    targets.forEach(function (el) {
        el.classList.add('reveal');

        // Escalonado sutil para tarjetas y piezas de galería en grillas
        const parent = el.parentElement;
        if (parent && (parent.classList.contains('projects-grid') || parent.classList.contains('sf-gallery') || parent.classList.contains('gallery-grid'))) {
            const index = Array.prototype.indexOf.call(parent.children, el);
            el.style.setProperty('--reveal-delay', Math.min(index * 70, 350) + 'ms');
        }

        revealObserver.observe(el);
    });
}
