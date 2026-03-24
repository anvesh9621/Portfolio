/* ============================================================
   Portfolio Site — Main JavaScript (Deep Forest Theme)
   ============================================================ */

(function () {
  'use strict';

  const THEME_KEY = 'portfolio-theme';
  const html = document.documentElement;

  // ── Theme helpers ──────────────────────────────────────────
  function getSavedTheme() {
    return localStorage.getItem(THEME_KEY);
  }

  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    const icon = document.getElementById('theme-icon');
    if (icon) {
      icon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
  }

  function toggleTheme() {
    const current = html.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem(THEME_KEY, next);
    applyTheme(next);
  }

  // Apply theme on load: saved preference → system preference → light
  applyTheme(getSavedTheme() || getSystemTheme());

  // Listen for OS-level theme changes (only if no saved pref)
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!getSavedTheme()) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  // ── Expose globally ────────────────────────────────────────
  window.toggleTheme = toggleTheme;

  // ── Navbar scroll effect ───────────────────────────────────
  const navbar = document.querySelector('.navbar');

  function onScroll() {
    if (navbar) {
      if (window.scrollY > 30) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  // ── Mobile Hamburger ───────────────────────────────────────
  const hamburger = document.querySelector('.hamburger');
  const navLinks = document.querySelector('.nav-links');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      const isOpen = navLinks.style.display === 'flex';
      navLinks.style.display = isOpen ? 'none' : 'flex';
      navLinks.style.flexDirection = 'column';
      navLinks.style.position = 'absolute';
      navLinks.style.top = '68px';
      navLinks.style.left = '0';
      navLinks.style.right = '0';
      navLinks.style.background = 'var(--bg)';
      navLinks.style.padding = '1rem 1.5rem';
      navLinks.style.borderBottom = '1px solid var(--border)';
      navLinks.style.zIndex = '999';
    });
  }

  // ── Active nav link ────────────────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ── Auto-hide flash messages ───────────────────────────────
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // ── Intersection Observer for scroll-in animations ─────────
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px',
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll(
    '.project-card, .achievement-card, .skill-category, .stat-card, .expertise-card'
  ).forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(18px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
  });

  // ── Smooth scroll for anchor links ────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // ── Confirm delete dialogs ────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm || 'Are you sure?')) {
        e.preventDefault();
      }
    });
  });

  // ── Tab Navigation for Skills ──────────────────────────────
  window.switchSkillTab = function (slug) {
    // 1. Remove active class from all tabs
    document.querySelectorAll('.skill-tab-btn').forEach(btn => {
      btn.classList.remove('active');
      btn.setAttribute('aria-selected', 'false');
    });
    // 2. Hide all tab contents
    document.querySelectorAll('.skill-tab-content').forEach(content => {
      content.classList.remove('active');
    });

    // 3. Add active class to clicked tab
    const activeTabObj = document.getElementById('tab-' + slug);
    if (activeTabObj) {
      activeTabObj.classList.add('active');
      activeTabObj.setAttribute('aria-selected', 'true');
    }

    // 4. Show corresponding content
    const activeContentObj = document.getElementById('cat-' + slug);
    if (activeContentObj) {
      activeContentObj.classList.add('active');
    }
  };

})();
