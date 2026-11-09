(() => {
  'use strict';
  if (window.__avMotion) { window.__avMotion.refresh(); return; }
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  const scroller = $('[data-testid="stMain"]') || document.documentElement;
  const isDocument = scroller === document.documentElement;
  const offset = () => isDocument ? window.scrollY : scroller.scrollTop;
  const limit = () => Math.max(1, scroller.scrollHeight - (isDocument ? innerHeight : scroller.clientHeight));
  let lenis, gsap, ticker, loaded = 0, lastY = offset(), open = false, refreshTimer, observer;
  const seen = new WeakSet();
  const load = src => new Promise(resolve => {
    const el = document.createElement('script'); el.src = src; el.async = true;
    let finished = false;
    const done = ok => {
      if (finished) return; finished = true; loaded += 1;
      const value = Math.min(1, loaded / 3), label = $('.av-percent'), bar = $('.av-loader-track i');
      if (label) label.textContent = Math.round(value * 100) + '%';
      if (bar) { bar.style.animation = 'none'; bar.style.transform = `scaleX(${value})`; }
      resolve(ok);
    };
    const timer = setTimeout(() => done(false), 3500);
    el.onload = () => { clearTimeout(timer); done(true); };
    el.onerror = () => { clearTimeout(timer); done(false); };
    document.head.append(el);
  });
  function menu(value) {
    open = value; scroller.classList.toggle('av-menu-open', value);
    $('.av-nav')?.classList.toggle('is-open', value);
    const button = $('.av-menu-button');
    button?.setAttribute('aria-expanded', String(value));
    button?.setAttribute('aria-label', value ? 'Đóng menu' : 'Mở menu');
    if (value) {
      $('.av-header')?.classList.remove('is-hidden');
      lenis?.stop();
      if (gsap && !reduced.matches) gsap.fromTo('.av-nav a', {y: 18, opacity: 0}, {y: 0, opacity: 1, stagger: .08, duration: .45, clearProps: 'all'});
    } else lenis?.start();
  }
  function scrollTo(target) {
    if (!target) return;
    if (lenis && !reduced.matches) lenis.scrollTo(target, {offset: -92, duration: 1.1});
    else if (isDocument) window.scrollTo({top: target.getBoundingClientRect().top + offset() - 92, behavior: reduced.matches ? 'auto' : 'smooth'});
    else scroller.scrollTo({top: target.getBoundingClientRect().top - scroller.getBoundingClientRect().top + offset() - 92, behavior: reduced.matches ? 'auto' : 'smooth'});
  }
  function onScroll() {
    const y = offset();
    $('.av-header')?.classList.toggle('is-scrolled', y > 35);
    if (!open && !$('.av-header')?.contains(document.activeElement) && Math.abs(y - lastY) > 4) $('.av-header')?.classList.toggle('is-hidden', y > lastY && y > 220);
    $('.av-top')?.classList.toggle('is-visible', y > 400);
    const progress = $('.av-progress'); if (progress) progress.style.transform = `scaleX(${Math.min(1, y / limit())})`;
    let active = '#home';
    ['#home', '#prediction', '#data'].forEach(id => { const el = $(id); if (el && el.getBoundingClientRect().top < 190) active = id; });
    $$('.av-nav a:not(.av-nav-cta)').forEach(a => { const current = a.hash === active; a.classList.toggle('is-active', current); if (current) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current'); });
    lastY = y;
  }
  function reveal(el, delay = 0) {
    if (seen.has(el)) return; seen.add(el);
    if (gsap && window.ScrollTrigger && !reduced.matches) gsap.from(el, {opacity: 0, y: 40, delay, duration: .85, ease: 'power3.out', clearProps: 'all', scrollTrigger: {trigger: el, scroller: isDocument ? window : scroller, start: 'top 93%', once: true}});
  }
  function refresh() {
    clearTimeout(refreshTimer);
    refreshTimer = setTimeout(() => {
      $$('.st-key-prediction-panel, .st-key-result-panel, .st-key-about-panel').forEach(el => reveal(el));
      $$('[data-av-reveal]').forEach((el, i) => reveal(el, i * .1));
      $$('.st-key-result-panel [data-testid="stMetric"]').forEach((el, i) => reveal(el, i * .1));
      $$('[data-testid="stMetricValue"] > div').forEach(el => {
        if (seen.has(el)) return; seen.add(el);
        const text = el.textContent, match = text.match(/^([^\d]*)([\d,.]+)(.*)$/);
        if (!match || !gsap || reduced.matches || !el.firstChild || el.firstChild.nodeType !== 3) return;
        const number = Number(match[2].replaceAll(',', '')), decimals = (match[2].split('.')[1] || '').length;
        const node = el.firstChild, state = {n: 0};
        gsap.to(state, {n: number, duration: .9, ease: 'power2.out', onUpdate: () => { node.data = match[1] + state.n.toLocaleString('en-US', {minimumFractionDigits: decimals, maximumFractionDigits: decimals}) + match[3]; }, onComplete: () => { node.data = text; }});
      });
      const result = $('.st-key-result-panel h2');
      if (result && !$('.av-check', result)) {
        scrollTo($('.st-key-result-panel'));
        result.insertAdjacentHTML('afterbegin', '<svg class="av-check" viewBox="0 0 28 28" aria-hidden="true"><circle cx="14" cy="14" r="12"/><path d="m8 14 4 4 8-8"/></svg>');
        $$('[data-av-busy]').forEach(b => { b.removeAttribute('data-av-busy'); b.removeAttribute('aria-busy'); });
      }
      window.ScrollTrigger?.refresh(); lenis?.resize(); onScroll();
    }, 90);
  }
  document.addEventListener('click', event => {
    if (event.target.closest('.av-menu-button')) { menu(!open); return; }
    const anchor = event.target.closest('a[href^="#"]');
    if (anchor && anchor.hash && $(anchor.hash)) { event.preventDefault(); menu(false); scrollTo($(anchor.hash)); }
    const submit = event.target.closest('[data-testid="stFormSubmitButton"] button');
    if (submit) { submit.setAttribute('data-av-busy', ''); submit.setAttribute('aria-busy', 'true'); setTimeout(() => { submit.removeAttribute('data-av-busy'); submit.removeAttribute('aria-busy'); }, 8000); }
  });
  document.addEventListener('keydown', event => {
    if (!open) return;
    if (event.key === 'Escape') { menu(false); $('.av-menu-button')?.focus(); }
    if (event.key === 'Tab') {
      const items = [$('.av-menu-button'), ...$$('.av-nav a')].filter(Boolean), first = items[0], last = items.at(-1);
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });
  document.addEventListener('invalid', event => { event.target.classList.add('av-shake'); setTimeout(() => event.target.classList.remove('av-shake'), 350); }, true);
  (isDocument ? window : scroller).addEventListener('scroll', onScroll, {passive: true});
  observer = new MutationObserver(records => { if (records.some(r => [...r.addedNodes].some(n => n.nodeType === 1))) refresh(); });
  observer.observe($('.stMainBlockContainer') || document.body, {childList: true, subtree: true});
  window.addEventListener('resize', () => { if (innerWidth > 1000 && open) menu(false); refresh(); });
  reduced.addEventListener('change', () => { lenis?.destroy(); lenis = null; if (ticker) gsap?.ticker.remove(ticker); window.ScrollTrigger?.getAll().forEach(t => t.kill(true)); if (gsap) gsap.set('.av-art, .av-mask>span, [data-av-reveal]', {clearProps: 'all'}); $('.av-loader')?.remove(); refresh(); });
  window.__avMotion = {refresh};
  async function start() {
    const loader = $('.av-loader'), percent = $('.av-percent');
    if (reduced.matches || sessionStorage.getItem('av-loaded')) loader?.remove();
    if (!reduced.matches) {
      await load('https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js');
      gsap = window.gsap;
      if (gsap) {
        await Promise.all([load('https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js'), load('https://cdn.jsdelivr.net/npm/lenis@1.3.4/dist/lenis.min.js')]);
        if (window.ScrollTrigger) gsap.registerPlugin(window.ScrollTrigger);
        if (window.Lenis) {
          lenis = new window.Lenis({wrapper: isDocument ? window : scroller, content: $('.stMainBlockContainer') || document.body, duration: 1.05, smoothWheel: true, syncTouch: false});
          lenis.on('scroll', () => window.ScrollTrigger?.update());
          ticker = time => lenis?.raf(time * 1000); gsap.ticker.add(ticker);
        }
        if (loader?.isConnected) gsap.to(loader, {opacity: 0, y: -12, duration: .35, onComplete: () => loader.remove()});
        const introDelay = loader?.isConnected ? .35 : 0;
        gsap.from('.av-mask>span', {yPercent: 105, opacity: 0, delay: introDelay, stagger: .12, duration: .9, ease: 'power3.out'});
        gsap.from('.av-eyebrow, .av-lead, .av-cta, .av-scroll', {y: 16, opacity: 0, stagger: .1, delay: .2 + introDelay, duration: .8, ease: 'power3.out', clearProps: 'all'});
        gsap.from('.av-car', {scale: 1.1, delay: introDelay, duration: 1.4, ease: 'power3.out'});
        if (window.ScrollTrigger) gsap.to('.av-art', {y: 80, ease: 'none', scrollTrigger: {trigger: '.av-hero', scroller: isDocument ? window : scroller, start: 'top top', end: 'bottom top', scrub: .8}});
        if (fine.matches) {
          const cursor = $('.av-cursor');
          if (cursor) {
            const moveX = gsap.quickTo(cursor, 'x', {duration: .2}), moveY = gsap.quickTo(cursor, 'y', {duration: .2});
            document.addEventListener('pointermove', event => { if (reduced.matches || !fine.matches) return; cursor.style.opacity = '1'; moveX(event.clientX); moveY(event.clientY); gsap.to(cursor, {scale: event.target.closest('a,button') ? 2.5 : 1, duration: .2, overwrite: 'auto'}); });
            document.addEventListener('pointerout', event => { if (!event.relatedTarget) cursor.style.opacity = '0'; });
          }
          $$('.av-magnetic').forEach(button => {
            button.addEventListener('pointermove', event => { if (reduced.matches) return; const r = button.getBoundingClientRect(); gsap.to(button, {x: (event.clientX-r.left-r.width/2)*.12, y: (event.clientY-r.top-r.height/2)*.12, duration: .3, overwrite: 'auto'}); });
            button.addEventListener('pointerleave', () => gsap.to(button, {x: 0, y: 0, duration: .5, ease: 'power3.out'}));
          });
        }
      }
    }
    if (percent) percent.textContent = '100%';
    sessionStorage.setItem('av-loaded', '1'); refresh();
  }
  start().catch(() => { $('.av-loader')?.remove(); refresh(); });
  onScroll();
})();
