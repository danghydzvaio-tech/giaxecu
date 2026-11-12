(() => {
  'use strict';
  const VERSION = 'glass-2';
  if (window.__avGlass?.version === VERSION) {
    window.__avGlass.refresh();
    return;
  }
  window.__avGlass?.destroy();

  const $ = s => document.querySelector(s);
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const main = $('[data-testid="stMain"]') || document.scrollingElement;
  const pageScroll = main === document.scrollingElement;
  const scrollTarget = pageScroll ? window : main;
  const app = $('.stApp') || document.body;
  const bar = document.createElement('div');
  const glow = document.createElement('div');
  bar.className = 'av-scroll-progress';
  glow.className = 'av-page-glow';
  bar.setAttribute('aria-hidden', 'true');
  glow.setAttribute('aria-hidden', 'true');
  document.body.append(bar);
  app.prepend(glow);

  let frame = 0, refreshTimer = 0, observer;
  const observed = new WeakSet();
  const shown = new WeakSet();
  const revealTimers = new Set();
  const targets = '.hero, .sample-gallery, .st-key-input-card, .st-key-result-card, .st-key-reference-card, .st-key-about-card, .page-footer';

  function show(element) {
    if (shown.has(element)) return;
    element.classList.add('av-reveal-visible');
    shown.add(element);
    const delay = parseFloat(element.style.getPropertyValue('--reveal-delay')) || 0;
    const timer = setTimeout(() => {
      element.classList.remove('av-reveal-pending');
      element.style.removeProperty('--reveal-delay');
      revealTimers.delete(timer);
    }, reduced.matches ? 0 : 850 + delay);
    revealTimers.add(timer);
  }
  function observeSections() {
    if (reduced.matches || !('IntersectionObserver' in window)) {
      document.querySelectorAll('.av-reveal-pending').forEach(show);
      return;
    }
    if (!observer) observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        show(entry.target);
        observer.unobserve(entry.target);
      });
    }, { root: pageScroll ? null : main, threshold: .04, rootMargin: '0px 0px -24px' });
    document.querySelectorAll(targets).forEach(section => {
      // Stagger the existing grid and text without wrapping native widgets.
      const children = [...section.querySelectorAll('.sample-car, .hero h1, .hero p, .badges')];
      [section, ...children].forEach((element, index) => {
        if (observed.has(element) || shown.has(element)) return;
        observed.add(element);
        element.style.setProperty('--reveal-delay', `${Math.min(index, 5) * 120}ms`);
        element.classList.add('av-reveal-pending');
        observer.observe(element);
      });
    });
  }

  function paintScroll() {
    frame = 0;
    const y = main.scrollTop;
    const available = main.scrollHeight - main.clientHeight;
    const progress = available > 0 ? Math.min(1, Math.max(0, y / available)) : 0;
    // Read scroll metrics first; batch the visual writes in this frame.
    bar.style.setProperty('--scroll-progress', progress);
    glow.style.setProperty('--glow-offset', `${reduced.matches ? 0 : Math.min(140, y * .08)}px`);
  }
  function scheduleScroll() {
    if (!frame) frame = requestAnimationFrame(paintScroll);
  }
  function refresh() {
    clearTimeout(refreshTimer);
    refreshTimer = setTimeout(() => {
      observeSections();
      scheduleScroll();
    }, 80);
  }
  function resize() {
    scheduleScroll();
  }
  function motionChanged() {
    if (reduced.matches) document.querySelectorAll('.av-reveal-pending').forEach(show);
    else observeSections();
    scheduleScroll();
  }
  // Streamlit replaces sections after predictions and gallery/brand changes.
  const mutations = new MutationObserver(refresh);
  mutations.observe(main, { childList: true, subtree: true });
  const sizes = new ResizeObserver(resize);
  sizes.observe(main);
  const content = $('[data-testid="stMainBlockContainer"]');
  if (content) sizes.observe(content);
  scrollTarget.addEventListener('scroll', scheduleScroll, { passive: true });
  window.addEventListener('resize', resize, { passive: true });
  reduced.addEventListener('change', motionChanged);
  window.__avGlass = {
    version: VERSION, refresh,
    destroy() {
      clearTimeout(refreshTimer);
      revealTimers.forEach(clearTimeout);
      cancelAnimationFrame(frame);
      mutations.disconnect(); sizes.disconnect(); observer?.disconnect();
      scrollTarget.removeEventListener('scroll', scheduleScroll);
      window.removeEventListener('resize', resize);
      reduced.removeEventListener('change', motionChanged);
      bar.remove(); glow.remove();
      document.querySelectorAll('.av-reveal-pending').forEach(element => {
        element.classList.remove('av-reveal-pending');
        element.classList.add('av-reveal-visible');
      });
      delete window.__avGlass;
    }
  };
  document.fonts?.ready.then(resize);
  refresh();
})();
