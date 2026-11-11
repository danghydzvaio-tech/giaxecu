(() => {
  'use strict';
  const VERSION = 'nav-1';
  if (window.__avNav?.version === VERSION) {
    window.__avNav.refresh();
    return;
  }
  window.__avNav?.destroy();

  const $ = s => document.querySelector(s);
  const main = $('[data-testid="stMain"]') || document.scrollingElement;
  const pageScroll = main === document.scrollingElement;
  const scrollTarget = pageScroll ? window : main;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = matchMedia('(max-width: 767px)');
  // Keep the mobile dock above Streamlit Cloud's hosting controls.
  const cloud = window.parent !== window && location.hostname.endsWith('.streamlit.app');
  document.documentElement.style.setProperty('--nav-host-inset', cloud ? '46px' : '0px');
  const sectionNames = { valuation: 'Định giá', reference: 'Dữ liệu tham chiếu', about: 'Giới thiệu' };
  let nav, box, indicator, links = [], sections = [];
  let active = 'valuation', hovered = null, focused = null;
  let lastY = main.scrollTop, frame = 0, timer = 0, navigating = 0;
  let spy, sizes, unbind = [];

  // SVG fallback for Streamlit versions that sanitize inline SVG in Markdown.
  const paths = {
    valuation: '<path d="M4 15V9l2-4h12l2 4v6M4 10h16M7 14h.01M17 14h.01M6 15v3M18 15v3"/>',
    reference: '<path d="M4 19V5M4 19h16M8 15v-4M13 15V7M18 15v-6"/>',
    about: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/>',
    brand: '<path d="m3 18 7-12h4l7 12M7 13h10M8 18h8"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>'
  };
  function hydrateIcons() {
    nav.querySelectorAll('[data-icon]').forEach(link => {
      if (link.querySelector('svg') || !paths[link.dataset.icon]) return;
      const iconClass = link.dataset.icon === 'brand' ? 'av-brand-icon' : link.dataset.icon === 'arrow' ? 'av-cta-icon' : 'av-nav-icon';
      link.insertAdjacentHTML('afterbegin', `<svg class="${iconClass}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[link.dataset.icon]}</svg>`);
    });
  }
  function positionIndicator() {
    if (!nav?.isConnected || !indicator) return;
    const id = focused || hovered || active;
    const link = links.find(el => el.dataset.section === id) || links[0];
    if (!link) return;
    const area = box.getBoundingClientRect();
    const rect = link.getBoundingClientRect();
    indicator.style.width = `${rect.width}px`;
    indicator.style.height = `${rect.height}px`;
    indicator.style.transform = `translate3d(${rect.left - area.left + box.scrollLeft}px,${rect.top - area.top + box.scrollTop}px,0)`;
    indicator.classList.add('is-ready');
  }
  function setActive(id) {
    active = id;
    links.forEach(link => {
      if (link.dataset.section === id) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    positionIndicator();
  }
  function syncSpy() {
    if (!sections.length) return;
    const top = pageScroll ? 0 : main.getBoundingClientRect().top;
    const line = top + (mobile.matches ? 48 : 136);
    let id = sections[0].id;
    sections.forEach(section => {
      if (section.getBoundingClientRect().top <= line) id = section.id;
    });
    // A short last section cannot always reach the activation line.
    if (main.scrollHeight - main.clientHeight - main.scrollTop < 8) id = sections.at(-1).id;
    if (id !== active) setActive(id);
  }
  function paint() {
    frame = 0;
    const y = main.scrollTop;
    const delta = y - lastY;
    if (nav && Date.now() > navigating && !nav.querySelector(':focus-visible')) {
      if (mobile.matches || y < 80 || delta < -4) nav.classList.remove('is-compact');
      else if (delta > 4) nav.classList.add('is-compact');
    }
    lastY = y;
    syncSpy();
    positionIndicator();
  }
  function schedule() {
    if (!frame) frame = requestAnimationFrame(paint);
  }
  function navigate(event) {
    const link = event.target.closest('a[href^="#"]');
    if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const id = link.getAttribute('href').slice(1);
    const target = document.getElementById(id);
    if (!target) return;
    event.preventDefault();
    navigating = Date.now() + (reduced.matches ? 0 : 900);
    nav.classList.remove('is-compact');
    if (id in sectionNames) setActive(id);
    const rootTop = pageScroll ? 0 : main.getBoundingClientRect().top;
    const offset = mobile.matches ? 24 : 112;
    const top = id === 'home' ? 0 : main.scrollTop + target.getBoundingClientRect().top - rootTop - offset;
    main.scrollTo({ top: Math.max(0, top), behavior: reduced.matches ? 'instant' : 'smooth' });
    // Preserve the user's focused link; section landmarks remain keyboard targets.
  }
  function listen(element, type, callback) {
    element.addEventListener(type, callback);
    unbind.push(() => element.removeEventListener(type, callback));
  }
  function bind() {
    const next = $('#av-floating-nav');
    if (!next || next === nav) return;
    unbind.forEach(remove => remove());
    unbind = [];
    sizes?.disconnect();
    nav = next;
    box = nav.querySelector('.av-nav-links');
    indicator = nav.querySelector('.av-nav-indicator');
    links = [...nav.querySelectorAll('.av-nav-link')];
    hovered = focused = null;
    hydrateIcons();
    listen(nav, 'click', navigate);
    links.forEach(link => listen(link, 'pointerenter', event => {
      if (event.pointerType !== 'mouse') return;
      hovered = link.dataset.section;
      positionIndicator();
    }));
    listen(box, 'pointerleave', () => { hovered = null; positionIndicator(); });
    listen(nav, 'focusin', event => {
      const keyboard = event.target.matches(':focus-visible');
      focused = keyboard ? event.target.closest('.av-nav-link')?.dataset.section || null : null;
      if (keyboard) nav.classList.remove('is-compact');
      positionIndicator();
    });
    listen(nav, 'focusout', () => requestAnimationFrame(() => {
      focused = nav.contains(document.activeElement) && document.activeElement.matches(':focus-visible') ? document.activeElement.closest('.av-nav-link')?.dataset.section : null;
      positionIndicator();
    }));
    sizes = new ResizeObserver(positionIndicator);
    sizes.observe(box);
    links.forEach(link => sizes.observe(link));
    setActive(active);
  }
  function refresh() {
    clearTimeout(timer);
    timer = setTimeout(() => {
      bind();
      const next = Object.keys(sectionNames).map(id => {
        const element = $(`.st-key-${id}-section`);
        if (element) {
          element.id = id;
          element.setAttribute('role', 'region');
          element.setAttribute('aria-label', sectionNames[id]);
          element.setAttribute('tabindex', '-1');
        }
        return element;
      }).filter(Boolean);
      const hero = $('.hero');
      if (hero) hero.id = 'home';
      if (next.length !== sections.length || next.some((el, i) => el !== sections[i])) {
        spy?.disconnect();
        sections = next;
        spy = new IntersectionObserver(syncSpy, {
          root: pageScroll ? null : main,
          rootMargin: '-112px 0px -45% 0px', threshold: [0, .05, .25]
        });
        sections.forEach(section => spy.observe(section));
      }
      schedule();
    }, 80);
  }
  function resize() {
    if (mobile.matches) nav?.classList.remove('is-compact');
    schedule();
  }
  const mutations = new MutationObserver(refresh);
  mutations.observe(main, { childList: true, subtree: true });
  scrollTarget.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', resize, { passive: true });
  reduced.addEventListener('change', resize);
  window.__avNav = {
    version: VERSION, refresh,
    destroy() {
      clearTimeout(timer); cancelAnimationFrame(frame);
      mutations.disconnect(); spy?.disconnect(); sizes?.disconnect();
      unbind.forEach(remove => remove());
      scrollTarget.removeEventListener('scroll', schedule);
      window.removeEventListener('resize', resize);
      reduced.removeEventListener('change', resize);
      document.documentElement.style.removeProperty('--nav-host-inset');
      delete window.__avNav;
    }
  };
  document.fonts?.ready.then(positionIndicator);
  refresh();
})();
