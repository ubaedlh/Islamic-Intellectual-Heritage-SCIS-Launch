(() => {
  'use strict';
  document.documentElement.classList.add('js-enabled');
  const entries = [...document.querySelectorAll('.milestone')];
  const chapters = [...document.querySelectorAll('.chapter')];
  const links = [...document.querySelectorAll('.chapter-nav a')];
  const pageProgress = document.querySelector('.progress span');
  const historyProgress = document.querySelector('.history-line span');
  const journal = document.querySelector('.journal');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let revealObserver;
  function configureMotion() {
    revealObserver?.disconnect();
    document.documentElement.classList.remove('js-motion');
    if (motion.matches || !('IntersectionObserver' in window)) return;
    document.documentElement.classList.add('js-motion');
    revealObserver = new IntersectionObserver(records => records.forEach(record => {
      if (record.isIntersecting) {
        record.target.classList.add('is-visible');
        revealObserver.unobserve(record.target);
      }
    }), { rootMargin: '0px 0px 80px 0px' });
    entries.forEach(entry => revealObserver.observe(entry));
  }
  configureMotion();
  motion.addEventListener('change', configureMotion);
  const clamp = value => Math.max(0, Math.min(1, value));
  let pending = false;
  function updateProgress() {
    const max = document.documentElement.scrollHeight - innerHeight;
    pageProgress.style.transform = `scaleX(${max > 0 ? clamp(scrollY / max) : 0})`;
    const bounds = journal.getBoundingClientRect();
    historyProgress.style.transform = `scaleY(${clamp((innerHeight * .5 - bounds.top) / bounds.height)})`;
    let active;
    chapters.forEach(chapter => { if (chapter.getBoundingClientRect().top <= 240) active = chapter; });
    if (bounds.bottom < 100) active = null;
    links.forEach(link => {
      if (active && link.hash === `#${active.id}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    pending = false;
  }
  function scheduleUpdate() {
    if (!pending) { pending = true; requestAnimationFrame(updateProgress); }
  }
  addEventListener('scroll', scheduleUpdate, { passive: true });
  addEventListener('resize', scheduleUpdate);
  addEventListener('load', scheduleUpdate);
  document.addEventListener('toggle', scheduleUpdate, true);
  updateProgress();
})();
