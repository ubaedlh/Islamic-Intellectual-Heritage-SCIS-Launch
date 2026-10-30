(() => {
  'use strict';
  const chapters = [...document.querySelectorAll('.chapter')];
  const links = [...document.querySelectorAll('.chapter-nav a')];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // The content remains visible when JavaScript or IntersectionObserver is unavailable.
  if ('IntersectionObserver' in window && !reducedMotion) {
    document.documentElement.classList.add('js-motion');
    const revealObserver = new IntersectionObserver((entries, observer) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      }
    }, { threshold: 0, rootMargin: '0px 0px 40px 0px' });
    chapters.forEach(chapter => revealObserver.observe(chapter));
  }

  let scheduled = false;
  function updateCurrentChapter() {
    const readingLine = Math.min(window.innerHeight * 0.35, 220);
    let current = null;
    for (const chapter of chapters) {
      if (chapter.getBoundingClientRect().top <= readingLine) current = chapter;
    }
    // Stop highlighting after the timeline has left the reading area.
    if (chapters.length && chapters[chapters.length - 1].getBoundingClientRect().bottom < 70) current = null;
    for (const link of links) {
      if (current && link.hash === `#${current.id}`) link.setAttribute('aria-current', 'step');
      else link.removeAttribute('aria-current');
    }
    scheduled = false;
  }
  window.addEventListener('scroll', () => {
    if (!scheduled) {
      scheduled = true;
      window.requestAnimationFrame(updateCurrentChapter);
    }
  }, { passive: true });
  window.addEventListener('resize', updateCurrentChapter);
  updateCurrentChapter();
})();
