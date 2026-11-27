/* Scroll choreography for Serai Studio sample sites.
   Needs gsap, ScrollTrigger, SplitText (and Lenis on desktop). If any of them
   failed to load, or the visitor prefers reduced motion, the page stays static. */
(function () {
  var H = document.documentElement;
  if (!H.classList.contains('fx')) return;
  if (!window.gsap || !window.ScrollTrigger || !window.SplitText) { H.classList.remove('fx'); return; }
  H.classList.add('pre');
  var safety = setTimeout(function () { H.classList.remove('pre'); }, 2500);

  gsap.registerPlugin(ScrollTrigger, SplitText);
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var desktop = matchMedia('(min-width: 901px) and (pointer: fine)').matches;
  var EASE = 'expo.out';

  /* smooth scrolling on desktop, driven by GSAP's clock so pins stay in sync */
  var lenis = null;
  if (desktop && window.Lenis) {
    lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 0.9 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (ev) {
        var t = $(a.getAttribute('href')); if (!t) return;
        ev.preventDefault(); lenis.scrollTo(t, { offset: -90, duration: 1.4 });
        history.replaceState(null, '', a.getAttribute('href'));
        setTimeout(function () { t.setAttribute('tabindex', '-1'); t.focus({ preventScroll: true }); }, 1400);
      });
    });
    $$('dialog').forEach(function (d) {
      new MutationObserver(function () { d.open ? lenis.stop() : lenis.start(); }).observe(d, { attributes: true, attributeFilter: ['open'] });
    });
  }

  /* header hides on the way down, returns on the way up */
  var nav = $('.nav'), pill = $('.pill');
  if (nav) ScrollTrigger.create({ start: 0, end: 'max', onUpdate: function (s) {
    if (pill && pill.classList.contains('open')) return;
    nav.dataset.hide = (s.direction === 1 && s.scroll() > innerHeight * 0.9) ? '1' : '0';
  } });

  function lines(el) {
    return SplitText.create(el, { type: 'lines', mask: 'lines', linesClass: 'line-in', aria: 'none' }).lines;
  }

  (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () {
    clearTimeout(safety);

    /* 1. arrival: photo settles, headline rises line by line */
    var hero = $('.hero'), media = $('.hero-media'), h1 = $('.hero h1');
    var intro = gsap.timeline({ defaults: { ease: EASE } });
    H.classList.remove('pre');
    if (media) intro.from(media, { scale: 1.1, duration: 2.6 }, 0);
    if (h1) intro.from(lines(h1), { yPercent: 110, duration: 1.3, stagger: 0.07 }, 0.25);
    intro.from($$('.hero .tag, .hero-foot > *'), { y: 32, duration: 1.2, stagger: 0.06 }, 0.6)
         .from($$('.hero .tag, .hero-foot > *'), { autoAlpha: 0, duration: 0.5, ease: 'power1.out', stagger: 0.06 }, 0.6)
         .from(nav, { autoAlpha: 0, y: -20, duration: 1, clearProps: 'transform' }, 0.9);

    /* 2. leaving the hero: the photo shrinks into a rounded card, text lifts away */
    if (hero && media) {
      gsap.timeline({ scrollTrigger: { trigger: hero, start: 'top top', end: '+=' + (desktop ? '70%' : '45%'), scrub: true, pin: desktop, pinSpacing: true } })
        .to(media, { clipPath: 'inset(7% 5% 7% 5% round 28px)', scale: 0.96, ease: 'none' }, 0)
        .to('.hero-in', { yPercent: -18, autoAlpha: 0, ease: 'none' }, 0)
        .to('.scroll-cue', { autoAlpha: 0, ease: 'none' }, 0);
    }

    /* 3. numbers count up */
    $$('.facts b').forEach(function (b) {
      var m = b.textContent.match(/^(\D*)(\d[\d,]*)(.*)$/); if (!m) return;
      var end = +m[2].replace(/,/g, ''), o = { v: end > 1900 && end < 2100 ? end - 60 : 0 };
      gsap.to(o, { v: end, duration: 1.6, ease: 'power3.out', scrollTrigger: { trigger: b, start: 'top 88%', once: true },
        onUpdate: function () { b.textContent = m[1] + Math.round(o.v) + m[3]; } });
    });

    /* 4. section titles rise out of a mask */
    $$('.sec-head h2, .faq h2, .book h2, .contact h2, .gal h2').forEach(function (h) {
      gsap.from(lines(h), { yPercent: 105, duration: 1.1, ease: EASE, stagger: 0.06, scrollTrigger: { trigger: h, start: 'top 85%', once: true } });
    });

    /* 5. story: words fill in as you read, photo eases from a tight crop */
    $$('.big').forEach(function (el) {
      var w = SplitText.create(el, { type: 'words', aria: 'none' }).words;
      gsap.fromTo(w, { opacity: 0.22 }, { opacity: 1, stagger: 0.08, ease: 'none',
        scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 45%', scrub: 0.6 } });
    });
    $$('.story .core img, .o-card .core img').forEach(function (im) {
      gsap.fromTo(im, { scale: 1.35, yPercent: -6 }, { scale: 1.05, yPercent: 6, ease: 'none',
        scrollTrigger: { trigger: im.closest('figure, article') || im, start: 'top bottom', end: 'bottom top', scrub: true } });
    });

    /* 6. list rows come into focus as they cross the middle of the screen */
    if (desktop) $$('.o-list .o-row, .w-list li, .m-group li').forEach(function (r) {
      ScrollTrigger.create({ trigger: r, start: 'top bottom', end: 'bottom top', onUpdate: function () {
        var b = r.getBoundingClientRect(), d = Math.abs(b.top + b.height / 2 - innerHeight * 0.45) / (innerHeight * 0.5);
        r.style.setProperty('--f', Math.max(0.6, 1 - d * d * 0.6).toFixed(3));
      } });
    });

    /* 7. photos: horizontal track on desktop, parallax inside frames on phones */
    var gal = $('.gal'), track = gal && $('.bento', gal);
    if (desktop && track) {
      gal.classList.add('hz');
      var dist = function () { return Math.max(0, track.scrollWidth - innerWidth); };
      gsap.to(track, { x: function () { return -dist(); }, ease: 'none',
        scrollTrigger: { trigger: gal, start: 'center center', end: function () { return '+=' + dist(); }, pin: true, scrub: 0.8, invalidateOnRefresh: true } });
      $$('.core img', track).forEach(function (im) { gsap.set(im, { scale: 1.15 }); });
    } else if (track) {
      $$('.core img', track).forEach(function (im) {
        gsap.fromTo(im, { yPercent: -8, scale: 1.2 }, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: im, start: 'top bottom', end: 'bottom top', scrub: true } });
      });
    }

    /* 8. dark bands open out from a rounded card */
    $$('.exp, .contact').forEach(function (sec) {
      gsap.fromTo(sec, { clipPath: 'inset(0% 4% 0% 4% round 36px)' }, { clipPath: 'inset(0% 0% 0% 0% round 0px)', ease: 'none',
        scrollTrigger: { trigger: sec, start: 'top bottom', end: 'top 35%', scrub: true } });
    });

    /* 9. buttons lean towards the cursor */
    if (desktop) $$('.btn, .mini').forEach(function (b) {
      var x = gsap.quickTo(b, 'x', { duration: 0.4, ease: 'power3' }), y = gsap.quickTo(b, 'y', { duration: 0.4, ease: 'power3' });
      b.addEventListener('mousemove', function (e) { var r = b.getBoundingClientRect(); x((e.clientX - r.left - r.width / 2) * 0.25); y((e.clientY - r.top - r.height / 2) * 0.35); });
      b.addEventListener('mouseleave', function () { x(0); y(0); });
    });

    ScrollTrigger.refresh();
  });
})();
