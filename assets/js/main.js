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
    initGalleryLightbox();
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

/**
 * Visor de galería (lightbox): anterior/siguiente, cierre y navegación con teclado,
 * gestos táctiles y botón Atrás del navegador.
 */
function initGalleryLightbox() {
    const links = Array.prototype.slice.call(document.querySelectorAll('.sf-gallery__link'));

    if (!links.length) {
        return;
    }

    const lang = document.documentElement.getAttribute('lang') === 'en' ? 'en' : 'es';
    const labels = {
        es: { viewer: 'Visor de imágenes', close: 'Cerrar', prev: 'Imagen anterior', next: 'Imagen siguiente' },
        en: { viewer: 'Image viewer', close: 'Close', prev: 'Previous image', next: 'Next image' }
    };
    const t = labels[lang];

    const lightbox = document.createElement('div');
    lightbox.className = 'sf-lightbox';
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-modal', 'true');
    lightbox.setAttribute('aria-label', t.viewer);
    lightbox.hidden = true;

    lightbox.innerHTML =
        '<button type="button" class="sf-lightbox__close" aria-label="' + t.close + '">&times;</button>' +
        '<button type="button" class="sf-lightbox__nav sf-lightbox__nav--prev" aria-label="' + t.prev + '">&lsaquo;</button>' +
        '<figure class="sf-lightbox__figure">' +
            '<img class="sf-lightbox__image" alt="">' +
            '<figcaption class="sf-lightbox__caption"></figcaption>' +
        '</figure>' +
        '<button type="button" class="sf-lightbox__nav sf-lightbox__nav--next" aria-label="' + t.next + '">&rsaquo;</button>';

    document.body.appendChild(lightbox);

    const image = lightbox.querySelector('.sf-lightbox__image');
    const caption = lightbox.querySelector('.sf-lightbox__caption');
    const closeButton = lightbox.querySelector('.sf-lightbox__close');
    const prevButton = lightbox.querySelector('.sf-lightbox__nav--prev');
    const nextButton = lightbox.querySelector('.sf-lightbox__nav--next');

    let current = -1;
    let lastFocused = null;
    let touchStartX = null;
    let touchStartY = null;

    image.addEventListener('load', function () {
        image.classList.remove('is-loading');
    });

    image.addEventListener('error', function () {
        image.classList.remove('is-loading');
    });

    function show(index) {
        current = (index + links.length) % links.length;
        const link = links[current];
        const thumb = link.querySelector('img');

        image.classList.add('is-loading');
        image.src = link.getAttribute('href');
        image.alt = (thumb && thumb.alt) || '';
        caption.textContent = (current + 1) + ' / ' + links.length;

        const single = links.length < 2;
        prevButton.disabled = single;
        nextButton.disabled = single;

        if (links.length > 2) {
            [(current + 1) % links.length, (current - 1 + links.length) % links.length].forEach(function (i) {
                const preload = new Image();
                preload.src = links[i].getAttribute('href');
            });
        }
    }

    function open(index) {
        lastFocused = document.activeElement;
        show(index);
        lightbox.hidden = false;
        document.body.classList.add('sf-lightbox-open');
        history.pushState({ sfLightboxOpen: true }, '');
        closeButton.focus();
    }

    function close(fromPopState) {
        if (lightbox.hidden) {
            return;
        }
        lightbox.hidden = true;
        document.body.classList.remove('sf-lightbox-open');
        image.classList.remove('is-loading');
        image.src = '';
        caption.textContent = '';

        if (!fromPopState && history.state && history.state.sfLightboxOpen) {
            history.back();
            return;
        }

        if (lastFocused && typeof lastFocused.focus === 'function') {
            lastFocused.focus();
        }
    }

    links.forEach(function (link, index) {
        link.addEventListener('click', function (e) {
            if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) {
                return;
            }
            e.preventDefault();
            open(index);
        });
    });

    prevButton.addEventListener('click', function () {
        show(current - 1);
    });

    nextButton.addEventListener('click', function () {
        show(current + 1);
    });

    closeButton.addEventListener('click', function () {
        close();
    });

    lightbox.addEventListener('click', function (e) {
        if (e.target === lightbox) {
            close();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (lightbox.hidden) {
            return;
        }

        if (e.key === 'Escape') {
            e.preventDefault();
            close();
        } else if (e.key === 'ArrowLeft') {
            e.preventDefault();
            show(current - 1);
        } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            show(current + 1);
        } else if (e.key === 'Tab') {
            const focusables = [closeButton, prevButton, nextButton].filter(function (btn) {
                return !btn.disabled;
            });
            if (!focusables.length) {
                return;
            }
            const first = focusables[0];
            const last = focusables[focusables.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        }
    });

    window.addEventListener('popstate', function () {
        close(true);
    });

    lightbox.addEventListener('touchstart', function (e) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    }, { passive: true });

    lightbox.addEventListener('touchend', function (e) {
        if (touchStartX === null) {
            return;
        }
        const dx = e.changedTouches[0].clientX - touchStartX;
        const dy = e.changedTouches[0].clientY - touchStartY;
        if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy)) {
            show(dx > 0 ? current - 1 : current + 1);
        }
        touchStartX = null;
        touchStartY = null;
    }, { passive: true });
}
