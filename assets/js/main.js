/**
 * Portfolio Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle (if needed)
    initMobileMenu();

    // Mark active navigation for static pages
    initActiveNavigation();
    
    // Smooth scroll for anchor links
    initSmoothScroll();
});

/**
 * Mark current navigation item on static routes
 */
function initActiveNavigation() {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.nav-menu a');

    links.forEach(function(link) {
        if (link.hasAttribute('aria-current')) {
            return;
        }

        const href = new URL(link.getAttribute('href'), window.location.href).pathname;
        const isActive = href.endsWith('/es/') ? currentPath === href : currentPath.startsWith(href);

        if (isActive) {
            link.setAttribute('aria-current', 'page');
        }
    });
}

/**
 * Initialize mobile menu toggle
 */
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
}

/**
 * Initialize smooth scroll for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
