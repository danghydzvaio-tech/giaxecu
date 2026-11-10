(() => {
  'use strict';
  const VERSION = 'creative-3';
  if (window.__avMotion) {
    if (window.__avMotion.version === VERSION) window.__avMotion.refresh();
    else window.location.reload();
    return;
  }
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  const scroller = $('[data-testid="stMain"]') || document.documentElement;
  const isDocument = scroller === document.documentElement;
  const scrollY = () => isDocument ? window.scrollY : scroller.scrollTop;
  const motion = () => !reduced.matches;
  const desktop = () => fine.matches && innerWidth > 1000;
  const seen = new WeakSet(), counters = new Map();
  const state = {hero:null, collection:null, chars:[], pointer:null, sprites:[], winds:[], distance:0, lastPoint:null, insideCar:false, selected:-1, previewSlot:0, pointerQueued:false};
  let gsap, lenis, ticker, heroContext, listContext, resetTimer, refreshTimer, resizeTimer;
  let open = false, lastY = scrollY(), loaded = 0;

  function load(src) {
    return new Promise(resolve => {
      const script = document.createElement('script'); script.src=src; script.async=true;
      let finished=false;
      const done = ok => {
        if (finished) return; finished=true; loaded++;
        const ratio=Math.min(1,loaded/3), label=$('.av-percent'), bar=$('.av-loader-track i');
        if(label) label.textContent=Math.round(ratio*100)+'%';
        if(bar){bar.style.animation='none';bar.style.transform=`scaleX(${ratio})`;}
        resolve(ok);
      };
      const timer=setTimeout(()=>done(false),3500);
      script.onload=()=>{clearTimeout(timer);done(true);}; script.onerror=()=>{clearTimeout(timer);done(false);};
      document.head.append(script);
    });
  }
  function scrollTo(target) {
    if(!target)return;
    if(lenis && motion())lenis.scrollTo(target,{offset:-100,duration:1.1});
    else {
      const top=target.getBoundingClientRect().top+scrollY()-100-(isDocument?0:scroller.getBoundingClientRect().top);
      (isDocument?window:scroller).scrollTo({top,behavior:motion()?'smooth':'auto'});
    }
  }
  function menu(value) {
    open=value; scroller.classList.toggle('av-menu-open',value);
    $('.av-nav')?.classList.toggle('is-open',value);
    const button=$('.av-menu-button'); button?.setAttribute('aria-expanded',String(value));button?.setAttribute('aria-label',value?'Đóng menu':'Mở menu');
    if(value){$('.av-header')?.classList.remove('is-hidden');lenis?.stop();if(gsap&&motion())gsap.fromTo('.av-nav a',{y:18,opacity:0},{y:0,opacity:1,stagger:.08,duration:.45,clearProps:'all'});}
    else lenis?.start();
    indicator();
  }
  function indicator() {
    const nav=$('.av-nav'), active=$('.av-nav a.is-active'), pill=$('.av-nav-indicator');
    if(!nav||!active||!pill||innerWidth<=1000)return;
    nav.classList.add('has-indicator');
    const a=active.getBoundingClientRect(),n=nav.getBoundingClientRect();
    // Dimensions change only when the active item/layout changes; movement uses transforms.
    pill.style.width=a.width+'px';pill.style.height=a.height+'px';
    if(gsap&&motion())gsap.to(pill,{x:a.left-n.left,y:a.top-n.top,duration:.45,ease:'power3.out',overwrite:true});
    else pill.style.transform=`translate(${a.left-n.left}px,${a.top-n.top}px)`;
  }
  function onScroll() {
    const y=scrollY(),header=$('.av-header'); header?.classList.toggle('is-scrolled',y>35);
    if(!open&&!header?.contains(document.activeElement)&&Math.abs(y-lastY)>4)header?.classList.toggle('is-hidden',y>lastY&&y>220);
    $('.av-top')?.classList.toggle('is-visible',y>400);
    const max=Math.max(1,scroller.scrollHeight-(isDocument?innerHeight:scroller.clientHeight));
    if($('.av-progress'))$('.av-progress').style.transform=`scaleX(${Math.min(1,y/max)})`;
    let active='#home';['#home','#prediction','#data'].forEach(id=>{if($(id)?.getBoundingClientRect().top<190)active=id;});
    let changed=false;
    $$('.av-nav a:not(.av-nav-cta)').forEach(a=>{const current=a.hash===active;if(a.classList.contains('is-active')!==current)changed=true;a.classList.toggle('is-active',current);if(current)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
    if(changed)indicator();lastY=y;
    const visible=state.hero&&state.hero.getBoundingClientRect().bottom>0&&state.hero.getBoundingClientRect().top<innerHeight;
    state.winds.forEach(t=>visible&&!document.hidden?t.play():t.pause());
  }
  function segmentTitle(hero) {
    const heading=$('h1',hero);if(!heading)return;
    heading.setAttribute('aria-label',heading.textContent.replace(/\s+/g,' ').trim());
    const segmenter=typeof Intl.Segmenter==='function'?new Intl.Segmenter('vi',{granularity:'grapheme'}):null;
    $$('.av-title-line',hero).forEach(line=>{
      if(line.dataset.segmented)return;line.dataset.segmented='true';line.setAttribute('aria-hidden','true');
      const text=line.textContent.normalize('NFC');line.replaceChildren();
      text.split(/(\s+)/u).forEach(word=>{
        if(!word)return;if(/^\s+$/u.test(word)){line.append(document.createTextNode(word));return;}
        const wrap=document.createElement('span');wrap.className='av-word';
        const graphemes=segmenter?[...segmenter.segment(word)].map(x=>x.segment):Array.from(word);
        graphemes.forEach(glyph=>{
          const char=document.createElement('span');char.className='char';
          const normal=document.createElement('span'),italic=document.createElement('span');
          normal.className='av-glyph-normal';italic.className='av-glyph-italic';normal.textContent=glyph;italic.textContent=glyph;
          char.append(normal,italic);wrap.append(char);
        });line.append(wrap);
      });
    });
    measureChars();
  }
  function measureChars() {
    if(!state.hero)return;
    const origin=state.hero.getBoundingClientRect();
    state.chars=$$('.char',state.hero).map(el=>{el.style.width='';const r=el.getBoundingClientRect();el.style.width=r.width+'px';return{el,x:r.left-origin.left+r.width/2,y:r.top-origin.top+r.height/2};});
  }
  function count(el, target, finishText, decimals=0) {
    if(!gsap||!motion())return;
    const node=el.firstChild;if(!node||node.nodeType!==3)return;
    const value={n:0};counters.set(el,{value,node,finishText});
    gsap.to(value,{n:target,duration:1.05,ease:'power3.out',onUpdate:()=>{node.data=value.n.toLocaleString(el.classList.contains('av-count')?'vi-VN':'en-US',{minimumFractionDigits:decimals,maximumFractionDigits:decimals});if(!el.classList.contains('av-count')){const m=finishText.match(/^([^\d]*)([\d,.]+)(.*)$/);node.data=m[1]+node.data+m[3];}},onComplete:()=>{node.data=finishText;counters.delete(el);}});
  }
  function hideSprites() {
    state.distance=0;state.lastPoint=null;state.winds.forEach(t=>t.kill());state.winds=[];
    if(gsap&&motion())gsap.to([...state.sprites].reverse(),{scale:0,opacity:0,rotation:-8,duration:.65,stagger:.06,overwrite:true});
  }
  function growSprites(number) {
    if(!gsap||!motion())return;
    state.sprites.slice(0,number).forEach(sprite=>{
      if(sprite.dataset.bloomed==='true')return;sprite.dataset.bloomed='true';
      gsap.to(sprite,{scale:1,opacity:1,rotation:0,duration:.9,ease:'elastic.out(1,0.6)',overwrite:true});
      const visual=$('.av-spark-visual',sprite);
      if(visual)state.winds.push(gsap.fromTo(visual,{rotation:-2},{rotation:2,duration:2.5+Math.random(),yoyo:true,repeat:-1,ease:'sine.inOut'}));
    });
  }
  function resetSprites() {hideSprites();state.sprites.forEach(el=>delete el.dataset.bloomed);}
  function setupHero(hero) {
    heroContext?.revert();resetSprites();state.heroReady=false;state.hero=hero;state.chars=[];state.insideCar=false;
    if(!hero)return;
    segmentTitle(hero);state.sprites=$$('.av-spark',hero);state.sprites.forEach(el=>delete el.dataset.bloomed);
    if(!gsap||!motion())return;
    state.heroReady=true;
    heroContext=gsap.context(()=>{
      gsap.set(state.sprites,{scale:0,opacity:0,rotation:-8});
      const stage=hero.closest('.av-hero-stage');
      if(window.ScrollTrigger&&stage){
        gsap.timeline({scrollTrigger:{trigger:stage,scroller:isDocument?window:scroller,start:'top top',end:()=>'+='+Math.min(hero.offsetHeight,innerHeight),pin:hero,pinSpacing:false,scrub:.7,invalidateOnRefresh:true}})
          .to(hero,{scale:.96,opacity:.6,ease:'none'},0).to($('.av-art',hero),{y:24,ease:'none'},0);
        if(!desktop())window.ScrollTrigger.create({trigger:$('.av-art',hero),scroller:isDocument?window:scroller,start:'top 90%',once:true,onEnter:()=>state.sprites.forEach((el,i)=>gsap.delayedCall(i*.13,()=>growSprites(i+1)))});
      }else if(!desktop())growSprites(state.sprites.length);
      const intro=sessionStorage.getItem('av-creative-intro')?0:.35;
      gsap.from('.av-title-line',{yPercent:105,opacity:0,duration:1,delay:intro,stagger:.08,ease:'power4.out',onComplete:measureChars});
      gsap.from('.av-eyebrow,.av-lead,.av-cta',{y:18,opacity:0,delay:intro+.25,stagger:.1,duration:.8,clearProps:'all'});
      gsap.from('.av-car',{scale:1.1,duration:1.3,delay:intro,ease:'power3.out'});
      $$('.av-count',hero).forEach(el=>count(el,Number(el.dataset.count),el.textContent));
    },hero);
    sessionStorage.setItem('av-creative-intro','1');
    document.fonts?.ready.then(measureChars);
  }
  function setRow(index, showPreview=true) {
    const section=state.collection;if(!section)return;
    const rows=$$('.av-collection-row',section),row=rows[index];
    if(!row)return;
    const changed=state.selected!==index;state.selected=index;
    section.classList.add('is-engaged');if(changed)rows.forEach((el,i)=>el.classList.toggle('is-selected',i===index));
    if(changed)$$('.av-collection-background',section).forEach((layer,i)=>{
      if(gsap&&motion())gsap.to(layer,{opacity:i===index?1:0,duration:.6,ease:'power2.out',overwrite:true});else layer.style.opacity=i===index?'1':'0';
    });
    if(!showPreview||!desktop())return;
    const preview=$('.av-preview');if(!preview)return;
    preview.classList.add('is-visible');
    if(state.previewIndex!==index){
      state.previewIndex=index;
      const images=$$('.av-preview-image img',preview),next=state.previewSlot^1;images[next].src=row.dataset.image;
      if(gsap&&motion()){
        gsap.to(images[state.previewSlot],{opacity:0,scale:1.1,duration:.3,overwrite:true});
        gsap.fromTo(images[next],{yPercent:100,opacity:1,scale:1.05},{yPercent:0,opacity:1,scale:1,duration:.5,ease:'power3.out',overwrite:true});
      }else images.forEach((img,i)=>img.style.opacity=i===next?'1':'0');
      state.previewSlot=next;
    }
    if(gsap&&motion()){if(changed)gsap.to(preview,{scale:1,opacity:1,duration:.3,overwrite:'auto'});}else preview.style.opacity='1';
  }
  function clearRows() {
    const section=state.collection;if(!section)return;
    section.classList.remove('is-engaged');$$('.av-collection-row',section).forEach(el=>el.classList.remove('is-selected'));
    $$('.av-collection-background',section).forEach(el=>{if(gsap&&motion())gsap.to(el,{opacity:0,duration:.6,overwrite:true});else el.style.opacity='0';});
    const preview=$('.av-preview');preview?.classList.remove('is-visible');
    if(gsap&&preview&&motion())gsap.to(preview,{scale:0,opacity:0,duration:.3,overwrite:'auto'});
    if(preview&&!gsap)preview.style.opacity='0';
    $('.av-cursor')?.classList.remove('is-view');state.selected=-1;state.previewIndex=-1;
  }
  function setupCollection(section) {
    listContext?.revert();state.collectionReady=false;state.collection=section;state.selected=-1;
    if(!section||!gsap||!motion())return;
    state.collectionReady=true;
    listContext=gsap.context(()=>{
      gsap.set('.av-preview',{scale:0,opacity:0});
      gsap.set('.av-preview-image img',{opacity:0});
      if(window.ScrollTrigger)gsap.from($$('.av-collection-row',section),{y:24,opacity:0,duration:.75,stagger:.06,ease:'power3.out',clearProps:'transform,opacity',scrollTrigger:{trigger:section,scroller:isDocument?window:scroller,start:'top 85%',once:true}});
    });
  }
  function pointerFrame() {
    state.pointerQueued=false;const p=state.pointer;if(!p)return;
    if(desktop()&&motion()){
      const cursor=$('.av-cursor');if(cursor){cursor.style.opacity='1';cursor.style.transform=`translate(${p.x}px,${p.y}px) scale(${p.target?.closest('button,a')?1.8:1})`;}
      if(state.hero){
        const r=state.hero.getBoundingClientRect();
        state.chars.forEach(c=>c.el.classList.toggle('is-morphed',Math.hypot(p.x-r.left-c.x,p.y-r.top-c.y)<60));
        const art=$('.av-art',state.hero),a=art?.getBoundingClientRect(),inside=a&&p.x>a.left&&p.x<a.right&&p.y>a.top&&p.y<a.bottom;
        if(inside){
          clearTimeout(resetTimer);state.insideCar=true;
          if(state.lastPoint)state.distance+=Math.hypot(p.x-state.lastPoint.x,p.y-state.lastPoint.y);
          state.lastPoint={x:p.x,y:p.y};growSprites(Math.min(state.sprites.length,Math.floor(state.distance/65)));
        }else if(state.insideCar){state.insideCar=false;state.lastPoint=null;resetTimer=setTimeout(resetSprites,2000);}
      }
    }
    const row=p.target?.closest('.av-collection-row');
    if(row&&desktop()){
      setRow(Number(row.dataset.index));$('.av-cursor')?.classList.add('is-view');
      const preview=$('.av-preview');if(preview){
        const width=preview.offsetWidth||260,height=preview.offsetHeight||180;
        const x=Math.max(12,Math.min(innerWidth-width-12,p.x+24)),y=Math.max(12,Math.min(innerHeight-height-12,p.y-height/2));
        const rotation=Math.max(-8,Math.min(8,(p.x-(state.lastPreviewX??p.x))*.12));state.lastPreviewX=p.x;
        if(gsap&&motion())gsap.to(preview,{x,y,rotation,duration:.32,ease:'power3.out',overwrite:'auto'});else preview.style.transform=`translate(${x}px,${y}px)`;
      }
    }else if(state.selected!==-1&&!state.collection?.contains(document.activeElement))clearRows();
  }
  function reveal(el) {
    if(seen.has(el))return;seen.add(el);
    if(gsap&&motion()&&window.ScrollTrigger)gsap.from(el,{y:40,opacity:0,duration:.85,ease:'power3.out',clearProps:'all',scrollTrigger:{trigger:el,scroller:isDocument?window:scroller,start:'top 94%',once:true}});
  }
  function refresh() {
    clearTimeout(refreshTimer);refreshTimer=setTimeout(()=>{
      window.ScrollTrigger?.getAll().forEach(t=>{if(t.trigger&&!t.trigger.isConnected)t.kill(true);});
      const hero=$('.av-hero'),collection=$('.av-collection');
      if(hero!==state.hero||(gsap&&motion()&&!state.heroReady))setupHero(hero);if(collection!==state.collection||(gsap&&motion()&&!state.collectionReady))setupCollection(collection);
      $$('.st-key-prediction-panel,.st-key-result-panel,.st-key-about-panel,[data-av-reveal]').forEach(reveal);
      $$('[data-testid="stMetricValue"]>div').forEach(el=>{if(seen.has(el))return;seen.add(el);const m=el.textContent.match(/^([^\d]*)([\d,.]+)(.*)$/);if(m)count(el,Number(m[2].replaceAll(',','')),el.textContent,(m[2].split('.')[1]||'').length);});
      const result=$('.st-key-result-panel h2');
      if(result&&!$('.av-check',result)){
        scrollTo($('.st-key-result-panel'));result.insertAdjacentHTML('afterbegin','<svg class="av-check" viewBox="0 0 28 28" aria-hidden="true"><circle cx="14" cy="14" r="12"/><path d="m8 14 4 4 8-8"/></svg>');
        $$('[data-av-busy]').forEach(b=>{b.removeAttribute('data-av-busy');b.removeAttribute('aria-busy');});
      }
      lenis?.resize();window.ScrollTrigger?.refresh();indicator();onScroll();
    },90);
  }
  document.addEventListener('pointermove',event=>{
    state.pointer={x:event.clientX,y:event.clientY,target:event.target};
    if(!state.pointerQueued){state.pointerQueued=true;requestAnimationFrame(pointerFrame);}
    const cta=event.target.closest('.av-magnetic');if(cta&&gsap&&motion()&&desktop()){const r=cta.getBoundingClientRect();gsap.to(cta,{x:(event.clientX-r.left-r.width/2)*.1,y:(event.clientY-r.top-r.height/2)*.1,duration:.3,overwrite:true});}
  },{passive:true});
  document.addEventListener('pointerout',event=>{
    if(!event.relatedTarget){$('.av-cursor')?.style.setProperty('opacity','0');if(state.insideCar){state.insideCar=false;resetTimer=setTimeout(resetSprites,2000);}clearRows();}
    const cta=event.target.closest('.av-magnetic');if(cta&&!cta.contains(event.relatedTarget)&&gsap)gsap.to(cta,{x:0,y:0,duration:.5,overwrite:true});
  });
  document.addEventListener('focusin',event=>{const row=event.target.closest('.av-collection-row');if(row)setRow(Number(row.dataset.index),false);});
  document.addEventListener('focusout',()=>setTimeout(()=>{if(!state.collection?.contains(document.activeElement))clearRows();},0));
  document.addEventListener('click',event=>{
    if(event.target.closest('.av-menu-button')){menu(!open);return;}
    const row=event.target.closest('.av-collection-row');if(row){
      const expand=row.getAttribute('aria-expanded')!=='true';
      $$('.av-collection-row').forEach(el=>{const active=el===row&&expand;el.setAttribute('aria-expanded',String(active));$('.av-row-extra',el).hidden=!active;});
      if(expand)setRow(Number(row.dataset.index),false);else clearRows();lenis?.resize();window.ScrollTrigger?.refresh();return;
    }
    const a=event.target.closest('a[href^="#"]');if(a){const id=a.hash;const target=id&&document.getElementById(decodeURIComponent(id.slice(1)));if(target){event.preventDefault();menu(false);scrollTo(target);}}
    const submit=event.target.closest('[data-testid="stFormSubmitButton"] button');if(submit){submit.setAttribute('data-av-busy','');submit.setAttribute('aria-busy','true');setTimeout(()=>{submit.removeAttribute('data-av-busy');submit.removeAttribute('aria-busy');},8000);}
  });
  document.addEventListener('keydown',event=>{
    if(!open)return;if(event.key==='Escape'){menu(false);$('.av-menu-button')?.focus();}
    if(event.key==='Tab'){const items=[$('.av-menu-button'),...$$('.av-nav a')].filter(Boolean),first=items[0],last=items.at(-1);if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}}
  });
  document.addEventListener('invalid',event=>{event.target.classList.add('av-shake');setTimeout(()=>event.target.classList.remove('av-shake'),350);},true);
  (isDocument?window:scroller).addEventListener('scroll',onScroll,{passive:true});
  new MutationObserver(records=>{if(records.some(r=>!r.target.closest?.('.av-hero-stage,.av-preview,.av-collection')&&[...r.addedNodes].some(n=>n.nodeType===1&&!n.classList.contains('pin-spacer'))))refresh();}).observe($('.stMainBlockContainer')||document.body,{childList:true,subtree:true});
  window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{if(innerWidth>1000&&open)menu(false);measureChars();indicator();refresh();},150);});
  document.addEventListener('visibilitychange',onScroll);
  reduced.addEventListener('change',()=>{
    lenis?.destroy();lenis=null;if(ticker)gsap?.ticker.remove(ticker);heroContext?.revert();listContext?.revert();
    state.winds.forEach(t=>t.kill());state.winds=[];
    counters.forEach(({value,node,finishText})=>{gsap?.killTweensOf(value);node.data=finishText;});counters.clear();
    state.chars.forEach(c=>c.el.classList.remove('is-morphed'));$('.av-loader')?.remove();clearRows();state.hero=null;state.collection=null;refresh();
  });
  window.__avMotion={refresh,version:VERSION};
  async function start(){
    if(reduced.matches||sessionStorage.getItem('av-loaded'))$('.av-loader')?.remove();
    if(motion()){
      await load('https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js');gsap=window.gsap;
      if(gsap){
        await Promise.all([load('https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js'),load('https://cdn.jsdelivr.net/npm/lenis@1.3.4/dist/lenis.min.js')]);
        if(window.ScrollTrigger)gsap.registerPlugin(window.ScrollTrigger);
        if(window.Lenis){lenis=new window.Lenis({wrapper:isDocument?window:scroller,content:$('.stMainBlockContainer')||document.body,duration:1.05,smoothWheel:true,syncTouch:false});lenis.on('scroll',()=>window.ScrollTrigger?.update());ticker=time=>lenis?.raf(time*1000);gsap.ticker.add(ticker);}
      }
    }
    const loader=$('.av-loader');if(loader){if(gsap&&motion())gsap.to(loader,{opacity:0,y:-12,duration:.35,onComplete:()=>loader.remove()});else loader.remove();}
    sessionStorage.setItem('av-loaded','1');refresh();
  }
  start().catch(()=>{$('.av-loader')?.remove();refresh();});onScroll();
})();
