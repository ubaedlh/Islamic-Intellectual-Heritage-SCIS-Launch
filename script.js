(() => {
  'use strict';
  const milestones = [...document.querySelectorAll('.milestone')];
  const periods = [...document.querySelectorAll('.period-section')];
  const links = [...document.querySelectorAll('.period-nav a')];
  const progress = document.querySelector('.progress');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('js-motion');
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    }), { rootMargin: '0px 0px 60px 0px' });
    milestones.forEach(item => observer.observe(item));
  }
  let pending = false;
  function update() {
    const height = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = `${height > 0 ? Math.min(100, Math.max(0, scrollY / height * 100)) : 0}%`;
    let active;
    periods.forEach(period => { if (period.getBoundingClientRect().top <= 230) active = period; });
    if (periods.at(-1).getBoundingClientRect().bottom < 80) active = null;
    links.forEach(link => {
      if (active && link.hash === `#${active.id}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    pending = false;
  }
  addEventListener('scroll', () => { if (!pending) { pending = true; requestAnimationFrame(update); } }, { passive: true });
  addEventListener('resize', update);
  update();

  // Static HTML is a readable offline/no-script fallback; JSON is the editable content source.
  fetch('content.json').then(response => {
    if (!response.ok) throw new Error('Content unavailable');
    return response.json();
  }).then(content => {
    document.title = content.title;
    if (content.title !== 'A Brief History of Islamic Education in Singapore') document.querySelector('h1').textContent = content.title;
    document.querySelector('.subtitle').textContent = content.subtitle;
    const intro = document.querySelector('.intro-grid > div');
    intro.replaceChildren(...content.introduction.map(text => {
      const p = document.createElement('p'); p.textContent = text; return p;
    }));
    const closing = document.querySelector('.closing');
    closing.querySelectorAll(':scope > p:not(.eyebrow)').forEach(p => p.remove());
    content.closing.forEach(text => {
      const p = document.createElement('p'); p.textContent = text;
      closing.insertBefore(p, closing.querySelector('a'));
    });
    content.milestones.forEach(item => {
      const card = document.querySelector(`#milestone-${Number(item.id)} .card`);
      if (!card) return;
      for (const [selector, value] of [['.date', item.date], ['.category', item.category], ['h3', item.title], ['.description', item.description]]) card.querySelector(selector).textContent = value;
      if (!item.image) return;
      const url = new URL(item.image, document.baseURI);
      if (!['http:', 'https:', 'file:'].includes(url.protocol)) return;
      const button = document.createElement('button'); button.type = 'button'; button.className = 'image-button';
      button.dataset.caption = item.caption || ''; button.dataset.source = item.source || '';
      const img = document.createElement('img'); img.src = url.href; img.alt = item.imageAlt; img.loading = 'lazy';
      const hint = document.createElement('span'); hint.textContent = 'Tap to enlarge image';
      button.append(img, hint);
      card.querySelector('.image-placeholder').replaceWith(button);
      const info = card.querySelector('details');
      info.querySelectorAll('p').forEach(p => p.remove());
      [item.caption, item.source || 'Source information pending.'].filter(Boolean).forEach(text => { const p = document.createElement('p'); p.textContent = text; info.append(p); });
    });
  }).catch(() => { /* Keep the complete static exhibition when fetch is unavailable. */ });

  // Approved images can be configured in content.json; placeholders never open as archival images.
  const dialog = document.querySelector('.image-dialog');
  let opener;
  document.addEventListener('click', event => {
    const button = event.target.closest('.image-button');
    if (!button) return;
    opener = button;
    const original = button.querySelector('img');
    dialog.querySelector('img').src = original.src;
    dialog.querySelector('img').alt = original.alt;
    dialog.querySelector('.dialog-caption').textContent = button.dataset.caption || '';
    dialog.querySelector('.dialog-source').textContent = button.dataset.source || 'Source information pending.';
    dialog.showModal();
  });
  dialog.querySelector('.close-dialog').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
  dialog.addEventListener('close', () => { dialog.querySelector('img').removeAttribute('src'); opener?.focus(); });
})();
