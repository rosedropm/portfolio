'use strict';
document.documentElement.classList.add('js');
const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
function closeMenu() { nav.classList.remove('is-open'); menu.setAttribute('aria-expanded', 'false'); }
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('is-open', open);
});
nav.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('is-open')) { closeMenu(); menu.focus(); } });
const filterBar = document.querySelector('.filters');
if (filterBar) {
  filterBar.hidden = false;
  const cards = [...document.querySelectorAll('[data-category]')];
  filterBar.addEventListener('click', event => {
    const button = event.target.closest('[data-filter]');
    if (!button) return;
    filterBar.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    const category = button.dataset.filter;
    cards.forEach(card => { card.hidden = category !== 'all' && card.dataset.category !== category; });
    document.querySelector('.filter-status').textContent = `顯示 ${cards.filter(card => !card.hidden).length} 組作品`;
  });
}
const dialog = document.querySelector('#lightbox');
const lightboxImage = document.querySelector('#lightbox-image');
const zooms = [...document.querySelectorAll('.zoom-image')];
let current = 0;
let trigger = null;
function showImage(index) {
  current = (index + zooms.length) % zooms.length;
  const item = zooms[current];
  lightboxImage.src = item.href;
  lightboxImage.alt = item.querySelector('img').alt;
  document.querySelector('#lightbox-original').href = item.href;
  document.querySelector('#lightbox-caption').textContent = item.dataset.caption;
  document.querySelector('#lightbox-count').textContent = `${current + 1} / ${zooms.length}`;
  document.querySelector('#lightbox-prev').disabled = zooms.length < 2;
  document.querySelector('#lightbox-next').disabled = zooms.length < 2;
}
zooms.forEach((item, index) => item.addEventListener('click', event => {
  if (typeof dialog.showModal !== 'function') return;
  event.preventDefault(); trigger = item; showImage(index); dialog.showModal(); document.body.classList.add('no-scroll');
}));
document.querySelector('#lightbox-close').addEventListener('click', () => dialog.close());
document.querySelector('#lightbox-prev').addEventListener('click', () => showImage(current - 1));
document.querySelector('#lightbox-next').addEventListener('click', () => showImage(current + 1));
dialog.addEventListener('close', () => { document.body.classList.remove('no-scroll'); if (trigger) trigger.focus(); });
dialog.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft') { event.preventDefault(); showImage(current - 1); }
  if (event.key === 'ArrowRight') { event.preventDefault(); showImage(current + 1); }
});
dialog.addEventListener('click', event => { if (event.target === dialog) { const r=dialog.getBoundingClientRect(); if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom) dialog.close(); } });
