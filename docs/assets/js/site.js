(() => {
  const doc = document.documentElement;
  const stored = localStorage.getItem('catl-theme');
  if (stored) doc.setAttribute('data-theme', stored);

  const toggle = document.querySelector('[data-theme-toggle]');
  if (toggle) {
    const sync = () => {
      const cur = doc.getAttribute('data-theme') === 'dark';
      toggle.setAttribute('aria-pressed', cur ? 'true' : 'false');
    };
    sync();
    toggle.addEventListener('click', () => {
      const next = doc.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      doc.setAttribute('data-theme', next);
      localStorage.setItem('catl-theme', next);
      sync();
    });
  }

  const overlay = document.querySelector('.search-overlay');
  const openers = document.querySelectorAll('[data-search-open]');
  const closer = document.querySelector('[data-search-close]');
  const input = document.querySelector('.search-input');
  const results = document.querySelector('.search-results');

  const index = (window.__SEARCH_INDEX__ || []).map(x => ({
    ...x,
    hay: `${x.title} ${x.section} ${x.snippet} ${(x.tags||[]).join(' ')}`.toLowerCase()
  }));

  function render(items){
    if (!results) return;
    results.innerHTML = '';
    if (!items.length){
      const d = document.createElement('div');
      d.className='notice';
      d.textContent='没有匹配结果。试试更短的关键词。';
      results.appendChild(d);
      return;
    }
    for (const it of items){
      const a = document.createElement('a');
      a.className='search-result';
      a.href = it.url;
      a.innerHTML = `<strong>${it.title}</strong><small>${it.section}</small><span>${it.snippet}</span>`;
      results.appendChild(a);
    }
  }

  function open(){
    if (!overlay) return;
    overlay.classList.add('active');
    overlay.setAttribute('aria-hidden','false');
    if (input){
      input.value='';
      render(index);
      input.focus();
    }
  }
  function close(){
    if (!overlay) return;
    overlay.classList.remove('active');
    overlay.setAttribute('aria-hidden','true');
  }

  openers.forEach(b => b.addEventListener('click', open));
  if (closer) closer.addEventListener('click', close);
  if (overlay) overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });

  if (input){
    input.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (!q) return render(index);
      render(index.filter(it => it.hay.includes(q)));
    });
  }

  const page = document.body.getAttribute('data-page');
  if (page){
    document.querySelectorAll(`.bottom-nav a[data-page="${page}"]`).forEach(a => a.classList.add('active'));
  }

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.body.classList.add('is-loading');
  window.addEventListener('load', () => {
    document.body.classList.remove('is-loading');
    document.body.classList.add('is-loaded');
  });
  if (!reduced){
    document.querySelectorAll('a[href]').forEach(a => {
      const href = a.getAttribute('href');
      if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) return;
      a.addEventListener('click', (ev) => {
        if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
        ev.preventDefault();
        document.body.classList.add('is-leaving');
        setTimeout(() => location.href = href, 220);
      });
    });
  }
})();
