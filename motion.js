(() => {
  'use strict';
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const ease = 'cubic-bezier(.22,1,.36,1)';
  const nav = document.getElementById('nav');
  const mini = document.querySelector('.mini-logo');
  const heroLogo = document.querySelector('.hero-logo');
  const progress = document.querySelector('.scroll-progress');
  const links = [...document.querySelectorAll('.nav-links a')];
  const sections = links.map(a => document.querySelector(a.getAttribute('href')));
  let scheduled = false;

  function updateScroll() {
    const y = window.scrollY;
    nav.classList.toggle('scrolled', y > 24);
    const compactVisible = heroLogo.getBoundingClientRect().bottom < 100;
    mini.classList.toggle('logo-visible', compactVisible);
    mini.tabIndex = compactVisible ? 0 : -1;
    mini.setAttribute('aria-hidden', String(!compactVisible));
    const maximum = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.transform = `scaleX(${maximum > 0 ? Math.min(1, Math.max(0, y / maximum)) : 0})`;
    let current = -1;
    sections.forEach((section, index) => { if (section.getBoundingClientRect().top <= 160) current = index; });
    if (document.getElementById('contact').getBoundingClientRect().top <= 160) current = -1;
    links.forEach((link, index) => {
      if (index === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    scheduled = false;
  }
  function queueScroll() { if (!scheduled) { scheduled = true; requestAnimationFrame(updateScroll); } }
  window.addEventListener('scroll', queueScroll, { passive: true });
  window.addEventListener('resize', queueScroll, { passive: true });
  updateScroll();

  // Content is visible by default. Progressive enhancement adds motion only
  // when supported and never changes the user's scrolling behaviour.
  const targets = [];
  function reveal(element, delay = 0) {
    if (!element) return;
    element.classList.add('reveal');
    element.style.setProperty('--reveal-delay', `${delay}ms`);
    targets.push(element);
  }
  reveal(document.querySelector('.motto-label'));
  reveal(document.querySelector('.motto h2'), 70);
  reveal(document.querySelector('.motto-copy'), 130);
  document.querySelectorAll('.section').forEach(section => {
    reveal(section.querySelector('.section-label'));
    reveal(section.querySelector('.section-heading'), 70);
  });
  document.querySelectorAll('.services, .pricing-grid').forEach(grid => {
    [...grid.children].forEach((card, index) => {
      const wrapper = document.createElement('div');
      wrapper.className = 'card-reveal';
      grid.insertBefore(wrapper, card);
      wrapper.appendChild(card);
      reveal(wrapper, window.innerWidth > 760 ? index * 100 : 0);
    });
  });
  document.querySelectorAll('.service-bottom, .pricing-foot, .closing-content, .footer-top, .footer-bottom').forEach(el => reveal(el));
  let observer;
  if ('IntersectionObserver' in window && !reducedMotion.matches) {
    document.body.classList.add('motion-ready');
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        if (entry.target.classList.contains('closing-content')) entry.target.parentElement.classList.add('has-entered');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -28px 0px', threshold: 0.06 });
    targets.forEach(el => observer.observe(el));
  } else {
    targets.forEach(el => el.classList.add('is-visible'));
    document.querySelector('.closing').classList.add('has-entered');
  }

  // One restrained, staggered entrance; no continuous animation or parallax.
  const heroElements = ['.hero-kicker', '.hero-logo', '.hero h1', '.hero-sub', '.hero-actions', '.hero-bottom'];
  const heroAnimations = [];
  if (!reducedMotion.matches && window.scrollY < 100 && !location.hash) {
    heroElements.forEach((selector, index) => {
      const el = document.querySelector(selector);
      const frames = selector === '.hero-logo'
        ? [{ opacity: 0, transform: 'translateY(18px) scale(.985)' }, { opacity: 1, transform: 'translateY(0) scale(1)' }]
        : [{ opacity: 0, transform: 'translateY(15px)' }, { opacity: 1, transform: 'translateY(0)' }];
      heroAnimations.push(el.animate(frames, { duration: 950, delay: index * 85, easing: ease, fill: 'backwards' }));
    });
  }
  reducedMotion.addEventListener('change', event => {
    if (!event.matches) return;
    heroAnimations.forEach(animation => animation.cancel());
    observer?.disconnect();
    document.body.classList.remove('motion-ready');
    targets.forEach(el => el.classList.add('is-visible'));
    document.querySelector('.closing').classList.add('has-entered');
    dialog.getAnimations().forEach(animation => animation.finish());
  });
  window.addEventListener('beforeprint', () => {
    targets.forEach(el => el.classList.add('is-visible'));
    document.querySelector('.closing').classList.add('has-entered');
  });

  const dialog = document.getElementById('project-dialog');
  const form = document.getElementById('project-form');
  const status = document.getElementById('form-status');
  let closing = false;
  let returnFocus = null;
  const dialogFrames = [{ opacity: 0, transform: 'translateY(18px) scale(.975)' }, { opacity: 1, transform: 'translateY(0) scale(1)' }];

  document.querySelectorAll('[data-project]').forEach(button => button.addEventListener('click', () => {
    if (dialog.open || closing) return;
    returnFocus = button;
    document.getElementById('plan').value = button.dataset.project;
    status.hidden = true;
    dialog.classList.remove('is-closing');
    dialog.classList.add('opening');
    document.body.style.paddingRight = `${window.innerWidth - document.documentElement.clientWidth}px`;
    document.body.classList.add('modal-open');
    dialog.showModal();
    if (!reducedMotion.matches) {
      dialog.animate(dialogFrames, { duration: 430, easing: ease }).finished.then(() => dialog.classList.remove('opening')).catch(() => {});
    } else dialog.classList.remove('opening');
  }));

  async function closeDialog() {
    if (!dialog.open || closing) return;
    closing = true;
    dialog.classList.remove('opening');
    dialog.classList.add('is-closing');
    if (!reducedMotion.matches) {
      const animation = dialog.animate([{ opacity: 1, transform: 'translateY(0) scale(1)' }, { opacity: 0, transform: 'translateY(10px) scale(.985)' }], { duration: 220, easing: 'cubic-bezier(.4,0,1,1)', fill: 'forwards' });
      try { await animation.finished; } catch (_) {}
      dialog.close();
      animation.cancel();
    } else dialog.close();
    closing = false;
    dialog.classList.remove('is-closing');
  }
  document.querySelector('.close').addEventListener('click', closeDialog);
  dialog.addEventListener('cancel', event => { event.preventDefault(); closeDialog(); });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    document.body.style.paddingRight = '';
    returnFocus?.focus({ preventScroll: true });
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeDialog();
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    const data = new FormData(form);
    const text = `ADOLESCENT STUDIO — PROJECT BRIEF\n\nName: ${data.get('name')}\nEmail: ${data.get('email')}\nPackage: ${data.get('plan')}\n\nAbout the business:\n${data.get('message')}\n\nPrepared using the Adolescent Studio website mockup. This brief has not been sent.\n`;
    const url = URL.createObjectURL(new Blob([text], { type: 'text/plain;charset=utf-8' }));
    const a = document.createElement('a');
    a.href = url;
    a.download = 'adolescent-studio-project-brief.txt';
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
    status.textContent = 'Your brief is ready. Save the downloaded file for your project conversation. Nothing has been sent.';
    status.hidden = false;
    if (!reducedMotion.matches) status.animate([{ opacity: 0, transform: 'translateY(5px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 400, easing: ease });
  });
})();
