import os, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
PAGES = ROOT / 'pages'
DOCS = ROOT / 'docs'

COLOR = {
  'ink': '#0E1116',
  'paper': '#F3F6FA',
  'cream': '#EAF0F7',
  'card': '#FFFFFF',
  'blue': '#0B3B8C',
  'blue2': '#062554',
  'silver': '#9FB2C7',
  'teal': '#0D9488',
}

SITE_TITLE = '宁德时代｜交互式分析展示（Demo）'

NAV = [
  ('首页', 'index.html', 'home'),
  ('战略', 'section-strategy.html', 'strategy'),
  ('产品', 'section-products.html', 'products'),
  ('技术', 'section-tech.html', 'tech'),
  ('研究', 'section-research.html', 'research'),
]

SEARCH = []

def ensure_dirs():
  for d in [ASSETS / 'css', ASSETS / 'js', ASSETS / 'svg', PAGES, DOCS]:
    d.mkdir(parents=True, exist_ok=True)

def write(path: Path, content: str):
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(content, encoding='utf-8')

def svg_logo():
  return f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120' role='img' aria-label='CATL-inspired mark'>
  <defs>
    <linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>
      <stop offset='0' stop-color='{COLOR['blue']}'/>
      <stop offset='1' stop-color='{COLOR['blue2']}'/>
    </linearGradient>
  </defs>
  <circle cx='60' cy='60' r='52' fill='url(#g)' stroke='{COLOR['silver']}' stroke-width='4'/>
  <path d='M34 70h52' stroke='{COLOR['paper']}' stroke-width='4' stroke-linecap='round'/>
  <path d='M40 52h40' stroke='{COLOR['paper']}' stroke-width='4' stroke-linecap='round'/>
  <circle cx='60' cy='60' r='10' fill='{COLOR['paper']}'/>
  <path d='M30 84h60' stroke='{COLOR['teal']}' stroke-width='3' opacity='0.9'/>
</svg>"""

def css():
  return f"""
:root{{
  --ink:{COLOR['ink']};
  --paper:{COLOR['paper']};
  --cream:{COLOR['cream']};
  --card:{COLOR['card']};
  --blue:{COLOR['blue']};
  --blue2:{COLOR['blue2']};
  --silver:{COLOR['silver']};
  --teal:{COLOR['teal']};
  --border: rgba(14,17,22,.12);
  --border2: rgba(14,17,22,.20);
  --shadow: rgba(12,14,18,.16);
  --r-lg: 22px; --r-md: 16px; --r-sm: 12px;
  --s1: 6px; --s2: 10px; --s3: 16px; --s4: 22px; --s5: 28px; --s6: 38px; --s7: 52px;
  --navh: 70px;
  --tfast: 160ms ease; --tmed: 280ms ease;
  --font-display: "Baskerville", "Didot", "Times New Roman", serif;
  --font-ui: "Avenir Next", "Gill Sans", "Trebuchet MS", sans-serif;
}}
[data-theme='dark']{{
  --ink:#EEF3FA;
  --paper:#0B0F15;
  --cream:#101725;
  --card:#141C2A;
  --border: rgba(238,243,250,.16);
  --border2: rgba(238,243,250,.24);
  --shadow: rgba(0,0,0,.55);
}}
*{{box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{margin:0;color:var(--ink);font-family:var(--font-ui);
  background:
    radial-gradient(1200px 700px at 12% 0%, rgba(11,59,140,.20), transparent 55%),
    radial-gradient(900px 520px at 92% 10%, rgba(13,148,136,.14), transparent 52%),
    linear-gradient(120deg, var(--paper), var(--cream));
  min-height:100vh;
}}
body.is-loading{{opacity:0;}}
body.is-loaded{{opacity:1;transition:opacity 320ms ease;}}
body.is-leaving{{opacity:0;transform:translateY(10px);transition:opacity 220ms ease, transform 220ms ease;}}
a{{color:inherit;text-decoration:none;}}

.page{{min-height:100vh; padding-bottom: calc(var(--navh) + var(--s4));}}

.topbar{{position:sticky;top:0;z-index:20;backdrop-filter: blur(18px);
  background: linear-gradient(180deg, rgba(243,246,250,.95), rgba(243,246,250,.62));
  border-bottom:1px solid var(--border);
}}
[data-theme='dark'] .topbar{{background: linear-gradient(180deg, rgba(11,15,21,.92), rgba(11,15,21,.55));}}
.topbar-inner{{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);padding: var(--s3) var(--s4);}}
.brand{{display:flex;align-items:center;gap:var(--s2);font-family:var(--font-display);letter-spacing:.06em;font-size:1.05rem;}}
.brand .mark{{width:34px;height:34px;}}
.actions{{display:flex;align-items:center;gap:var(--s2);}}
.btn{{padding:10px 14px;border-radius:999px;border:1px solid var(--border2);background:var(--card);
  font-size:.86rem;letter-spacing:.03em;display:inline-flex;align-items:center;gap:8px;
  transition: transform var(--tfast), box-shadow var(--tfast), background var(--tfast);
}}
.btn:hover,.btn:focus-visible{{transform: translateY(-1px); box-shadow: 0 10px 22px var(--shadow); outline:none;}}
.btn.primary{{background: linear-gradient(120deg, var(--blue), var(--blue2)); color:#fff; border:none;}}
.btn.ghost{{background: transparent;}}

.container{{width:min(1040px, 100%); margin:0 auto; padding: var(--s4);}}

.hero{{display:grid;gap:var(--s4);padding: var(--s7) var(--s4) var(--s4);}}
@media (min-width: 780px){{.hero{{grid-template-columns:1.1fr .9fr;align-items:center;}}}}
.h1{{margin:0;font-family:var(--font-display);font-size:clamp(2.1rem, 6vw, 3.8rem);line-height:1.05;}}
.sub{{color: rgba(14,17,22,.72); line-height:1.6; max-width: 680px;}}
[data-theme='dark'] .sub{{color: rgba(238,243,250,.75);}}

.panel{{background:var(--card);border:1px solid var(--border);border-radius:var(--r-lg);padding: var(--s4);box-shadow: 0 18px 34px var(--shadow);}}
.grid{{display:grid;gap:var(--s3);grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r-md);padding: var(--s4);
  box-shadow: 0 10px 22px rgba(12,14,18,.10);
  transition: transform var(--tfast), box-shadow var(--tfast);
  display:grid; gap: var(--s2);
}}
.card:hover{{transform: translateY(-2px); box-shadow: 0 18px 34px var(--shadow);}}

.kicker{{display:inline-flex;gap:6px;align-items:center;padding:4px 10px;border-radius:999px;
  background: rgba(13,148,136,.12); color: var(--teal); font-size:.72rem; letter-spacing:.12em; text-transform:uppercase;
}}
.badge{{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:999px;background: rgba(159,178,199,.18);
  color: var(--blue); font-size:.78rem; letter-spacing:.08em; text-transform:uppercase;
}}

.breadcrumbs{{display:flex;gap:6px;font-size:.78rem;text-transform:uppercase;letter-spacing:.12em;color: rgba(14,17,22,.55);}}
[data-theme='dark'] .breadcrumbs{{color: rgba(238,243,250,.55);}}
.breadcrumbs span::after{{content:'/'; margin-left:6px; color: var(--border2);}}
.breadcrumbs span:last-child::after{{content:'';}}

.list{{margin:0;padding:0;list-style:none;display:grid;gap:var(--s2);}}
.list li{{padding: var(--s2) var(--s3); border:1px solid var(--border); border-radius: var(--r-sm); background: var(--card); display:grid; gap: 6px;}}
.meta{{font-size:.86rem; color: rgba(14,17,22,.62); line-height:1.55;}}
[data-theme='dark'] .meta{{color: rgba(238,243,250,.65);}}

.notice{{padding: var(--s3); border-left: 3px solid var(--teal); background: rgba(13,148,136,.12); border-radius: var(--r-sm);}}

.bottom-nav{{position:fixed; left:0; right:0; bottom:0; height: var(--navh);
  background: rgba(243,246,250,.95); backdrop-filter: blur(18px);
  border-top:1px solid var(--border); display:flex; justify-content:space-around; align-items:center; z-index:25;
}}
[data-theme='dark'] .bottom-nav{{background: rgba(11,15,21,.92);}}
.bottom-nav a{{display:grid; place-items:center; gap:4px; font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; color: rgba(14,17,22,.56);}}
[data-theme='dark'] .bottom-nav a{{color: rgba(238,243,250,.56);}}
.bottom-nav a.active{{color: var(--teal);}}

.search-overlay{{position:fixed; inset:0; background: rgba(8,10,12,.70); display:none; align-items:center; justify-content:center; z-index:30;}}
.search-overlay.active{{display:flex;}}
.search-panel{{width:min(720px, 92%); background: var(--card); border:1px solid var(--border2); border-radius: var(--r-lg);
  padding: var(--s4); box-shadow: 0 18px 34px var(--shadow);
}}
.search-input{{width:100%; padding: 14px 16px; border-radius: var(--r-sm); border:1px solid var(--border2);
  background: transparent; color: inherit; font-size: 1rem;
}}
.search-results{{margin-top: var(--s3); display:grid; gap: var(--s2); max-height: 50vh; overflow:auto;}}
.search-result{{border:1px solid var(--border); border-radius: var(--r-sm); padding: var(--s2) var(--s3); display:grid; gap:4px; background: var(--card);}}
.search-result small{{opacity:.7;}}

.reveal{{animation: rise 620ms ease both;}}
.reveal.d1{{animation-delay: 100ms;}}
.reveal.d2{{animation-delay: 200ms;}}
.reveal.d3{{animation-delay: 300ms;}}
@keyframes rise{{from{{opacity:0; transform: translateY(18px);}} to{{opacity:1; transform: translateY(0);}}}}

@media (prefers-reduced-motion: reduce){{
  *{{transition:none !important; animation:none !important;}}
  html{{scroll-behavior:auto;}}
}}
"""

def js_search_index():
  import json
  return 'window.__SEARCH_INDEX__ = ' + json.dumps(SEARCH, ensure_ascii=False, indent=2) + ';\n'

def js():
  return r"""(() => {
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
"""

def layout(title, page_key, breadcrumbs, body_html, asset_prefix='../assets/', nav_prefix=''):
  nav_html = "".join([f"<a href='{nav_prefix}{u}' data-page='{k}' aria-label='{n}'><span>{n}</span></a>" for n,u,k in NAV])
  bc = ''.join([f"<span>{b}</span>" for b in breadcrumbs])
  return f"""<!DOCTYPE html>
<html lang='zh-CN'>
<head>
  <meta charset='UTF-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1' />
  <title>{title}</title>
  <link rel='stylesheet' href='{asset_prefix}css/style.css' />
</head>
<body data-page='{page_key}'>
  <div class='page'>
    <header class='topbar'>
      <div class='topbar-inner'>
        <a class='brand' href='{nav_prefix}index.html' aria-label='Home'>
          <span class='mark'>{svg_logo()}</span>
          宁德时代 Demo
        </a>
        <div class='actions'>
          <button class='btn ghost' data-search-open aria-label='Open search'>搜索</button>
          <button class='btn' data-theme-toggle aria-pressed='false' aria-label='Toggle dark mode'>深色</button>
        </div>
      </div>
    </header>

    <main class='container'>
      <div class='breadcrumbs'>{bc}</div>
      {body_html}
    </main>

    <footer class='container' style='padding-top:0;'>
      <div class='meta'>本网站为演示站点：内容含【示例内容】/【待核实】标记。<a href='{nav_prefix}about.html'>关于与声明</a></div>
    </footer>
  </div>

  <div class='search-overlay' aria-hidden='true'>
    <div class='search-panel' role='dialog' aria-modal='true' aria-label='Site search'>
      <div style='display:flex;justify-content:space-between;align-items:center;gap:12px;'>
        <strong>站内搜索</strong>
        <button class='btn ghost' data-search-close aria-label='Close search'>关闭</button>
      </div>
      <input class='search-input' type='search' placeholder='搜索：战略 / 产品 / 技术 / 研究…' aria-label='Search site' />
      <div class='search-results'></div>
    </div>
  </div>

  <nav class='bottom-nav' aria-label='Primary'>
    {nav_html}
  </nav>

  <script src='{asset_prefix}js/search-index.js'></script>
  <script src='{asset_prefix}js/site.js'></script>
</body>
</html>"""

def add_search(title, section, url, snippet, tags):
  SEARCH.append({'title':title,'section':section,'url':url,'snippet':snippet,'tags':tags})

def build_pages(asset_prefix='../assets/', nav_prefix=''):
  target = PAGES if asset_prefix.startswith('..') else DOCS

  # Home
  body = f"""
  <section class='hero'>
    <div class='reveal'>
      <div class='badge'>Energy × Reliability × Frontier</div>
      <h1 class='h1'>{SITE_TITLE}</h1>
      <p class='sub'>将“设计目标/分析要求”转为可浏览的四级信息架构：用高级、克制的编辑风格呈现信息，用轻量交互强化可读性与专业可信感。</p>
      <div style='display:flex;gap:10px;flex-wrap:wrap;'>
        <a class='btn primary' href='{nav_prefix}section-strategy.html'>进入战略</a>
        <a class='btn' href='{nav_prefix}section-tech.html'>查看技术</a>
      </div>
    </div>
    <div class='panel reveal d1'>
      <div class='kicker'>方法论</div>
      <h2 style='margin:10px 0 8px;font-family:var(--font-display);'>从“分析报告”到“站点结构”</h2>
      <ul class='list'>
        <li><strong>视觉吸引</strong><div class='meta'>深蓝主色 + 银色信息线条 + 纸感背景</div></li>
        <li><strong>信息传达</strong><div class='meta'>四级结构 + 底部导航 + 全站搜索</div></li>
        <li><strong>情感共鸣</strong><div class='meta'>专业可靠、前沿赋能：不堆砌词藻</div></li>
      </ul>
      <div class='notice meta'>提示：任何公司具体事实/数据/新闻均以【示例内容】或【待核实】标注。</div>
    </div>
  </section>

  <section class='panel reveal d2'>
    <div class='kicker'>目录（四级架构）</div>
    <div class='grid' style='margin-top:12px;'>
      <a class='card' href='{nav_prefix}section-strategy.html'><span class='kicker'>Level 2</span><strong>战略</strong><div class='meta'>定位、叙事、指标框架</div></a>
      <a class='card' href='{nav_prefix}section-products.html'><span class='kicker'>Level 2</span><strong>产品</strong><div class='meta'>产品体系展示（示例结构）</div></a>
      <a class='card' href='{nav_prefix}section-tech.html'><span class='kicker'>Level 2</span><strong>技术</strong><div class='meta'>技术路线（待核实）与表达模板</div></a>
      <a class='card' href='{nav_prefix}section-research.html'><span class='kicker'>Level 2</span><strong>研究</strong><div class='meta'>报告“尽展示”：结构化与可检索</div></a>
    </div>
  </section>
  """
  write(target / 'index.html', layout('首页｜宁德时代 Demo','home',['Home','Index'], body, asset_prefix, nav_prefix))
  add_search('首页｜宁德时代交互式分析展示（Demo）','Home',f'{nav_prefix}index.html','四级结构入口与方法论概览。',['home','index','demo'])

  sections = [
    ('section-strategy.html','strategy','战略｜定位与叙事','把“专业可靠 + 前沿赋能”拆成可落地的信息结构。', [
      ('strategy-positioning.html','定位','定位与叙事骨架','把目标受众与价值主张变成页面语言。'),
      ('strategy-metrics.html','指标','指标体系（结构化）','只给结构，不输出未核实数据。'),
    ]),
    ('section-products.html','products','产品｜体系与场景','以结构展示产品层级与应用场景（示例内容）。', [
      ('products-portfolio.html','体系','产品组合结构（示例）','用层级与卡片承载信息密度。'),
      ('products-detail.html','详情','产品详情页（示例内容）','规格表字段齐全，数值标【待核实】。'),
    ]),
    ('section-tech.html','tech','技术｜路线与可信表达','把技术叙事转成“可读、可检索”的页面模板。', [
      ('tech-architecture.html','架构','技术架构（待核实）','关键模块—作用—边界条件。'),
      ('tech-qa.html','问答','技术常见问题（示例）','把疑问变成可检索条目。'),
    ]),
    ('section-research.html','research','研究｜报告结构化','把分析报告“尽展示”转成多层导航与详情页。', [
      ('research-framework.html','框架','分析框架与风险维度','提供结构与写法模板。'),
      ('research-exec.html','摘要','执行摘要（示例内容）','一屏结论：论点、证据、下一步。'),
    ]),
  ]

  categories=[]
  for file,key,title,desc,cats in sections:
    cards=''.join([f"<a class='card' href='{nav_prefix}{cf}'><span class='kicker'>Level 3</span><strong>{ct}</strong><div class='meta'>{cd}</div></a>" for cf,ct,_,cd in cats])
    body=f"""
    <h1 class='h1' style='font-size:clamp(1.8rem,5vw,3rem);'>{title}</h1>
    <p class='sub'>{desc}</p>
    <section class='panel reveal'><div class='kicker'>Categories</div><div class='grid' style='margin-top:12px;'>{cards}</div></section>
    """
    write(target / file, layout(title,key,['Home',title], body, asset_prefix, nav_prefix))
    add_search(title,'Section',f'{nav_prefix}{file}',desc,[key,'section'])
    for cf,ct,ch1,cd in cats:
      categories.append((cf,key,ch1,cd,file,title))

  details=[
    ('detail-narrative.html','strategy','叙事语言板｜把“可信”写出来',['【示例内容】用“可验证的过程描述”替代夸张形容。','结构：结论→证据→边界→下一步。','语气：克制、专业、可复用。']),
    ('detail-metrics-template.html','strategy','指标模板（结构化）｜不捏造数据',['只展示字段与口径，不给未经来源的数值。','每项含：定义/意义/获取方式/更新频率。','【待核实】数据来源需补充。']),
    ('detail-product-card.html','products','产品卡片模板｜信息密度不压迫',['结构：名称+一句话亮点+3信息点+行动按钮。','规格字段完整，数值标【待核实】。','交互：触控友好、轻阴影。']),
    ('detail-product-detail.html','products','产品详情（示例）｜规格表与场景分区',['分区：概述/技术点/规格/场景/FAQ（示例）。','规格表字段齐全，数值待补。','阅读：短段落+列表+高亮句。']),
    ('detail-tech-brief.html','tech','技术简报（待核实）｜把复杂讲清',['模块—作用—限制—验证方式。','避免炫技：少术语堆叠，多边界与假设。','【待核实】具体参数需来源。']),
    ('detail-risk-list.html','research','风险清单（示例）｜专业可靠表达',['风险：政策/供应/竞争/需求/合规（示例分类）。','每条：触发→影响→预警信号。','强调可追踪与可复用。']),
  ]
  for f,key,h1,bul in details:
    items=''.join([f"<li><strong>要点</strong><div class='meta'>{b}</div></li>" for b in bul])
    body=f"""
    <h1 class='h1' style='font-size:clamp(1.8rem,5vw,3rem);'>{h1}</h1>
    <p class='sub'>Level 4 详情页：承载“报告→站点”的关键模板与结构化要点。</p>
    <section class='panel reveal'><div class='kicker'>Detail</div><ul class='list' style='margin-top:12px;'>{items}</ul><div class='notice meta' style='margin-top:14px;'>涉及公司事实/数据请补充来源；否则保持【示例/待核实】标注。</div></section>
    """
    write(target / f, layout(h1,key,['Home','Detail',h1], body, asset_prefix, nav_prefix))
    add_search(h1,'Detail',f'{nav_prefix}{f}','详情页：模板与要点。',[key,'detail'])

  cat_links={
    'strategy-positioning.html':['detail-narrative.html'],
    'strategy-metrics.html':['detail-metrics-template.html'],
    'products-portfolio.html':['detail-product-card.html'],
    'products-detail.html':['detail-product-detail.html'],
    'tech-architecture.html':['detail-tech-brief.html'],
    'tech-qa.html':[],
    'research-framework.html':['detail-risk-list.html'],
    'research-exec.html':[],
  }

  for cf,key,ch1,cd,parent,parent_title in categories:
    links=cat_links.get(cf,[])
    if links:
      lis=''.join([f"<li><strong>{u}</strong><div class='meta'>进入详情页查看模板与要点。</div><a class='btn' href='{nav_prefix}{u}'>打开详情</a></li>" for u in links])
    else:
      lis="<li><strong>【示例内容】该分类暂展示结构</strong><div class='meta'>你提供分析报告后可替换为可核实文本。</div></li>"
    body=f"""
    <h1 class='h1' style='font-size:clamp(1.8rem,5vw,3rem);'>{ch1}</h1>
    <p class='sub'>{cd}</p>
    <section class='panel reveal'><div class='kicker'>Items</div><ul class='list' style='margin-top:12px;'>{lis}</ul></section>
    """
    write(target / cf, layout(ch1,key,['Home',parent_title,ch1,'Level 3'], body, asset_prefix, nav_prefix))
    add_search(ch1,'Category',f'{nav_prefix}{cf}',cd,[key,'category'])

  about_body="""
  <h1 class='h1' style='font-size:clamp(1.8rem,5vw,3rem);'>关于与声明</h1>
  <p class='sub'>本网站为“报告结构化展示”的交互式 Demo：用于演示信息分层、视觉系统、交互体验与可读性设计。</p>
  <section class='panel reveal'>
    <div class='kicker'>内容政策</div>
    <ul class='list' style='margin-top:12px;'>
      <li><strong>【示例内容】</strong><div class='meta'>为了填充层级结构与交互演示而写的占位内容，不应被当作真实事实。</div></li>
      <li><strong>【待核实】</strong><div class='meta'>需要补充权威来源后才能落地的数据与描述。</div></li>
    </ul>
  </section>
  """
  write(target / 'about.html', layout('关于｜声明','research',['Home','About'], about_body, asset_prefix, nav_prefix))
  add_search('关于与声明','About',f'{nav_prefix}about.html','Demo 声明与示例内容说明。',['about'])


def build_assets():
  write(ASSETS / 'css' / 'style.css', css())
  write(ASSETS / 'js' / 'site.js', js())
  write(ASSETS / 'svg' / 'mark.svg', svg_logo())


def build_pages_root():
  if PAGES.exists():
    shutil.rmtree(PAGES)
  PAGES.mkdir(parents=True, exist_ok=True)
  build_pages(asset_prefix='../assets/', nav_prefix='')


def build_docs():
  if DOCS.exists():
    shutil.rmtree(DOCS)
  DOCS.mkdir(parents=True, exist_ok=True)
  shutil.copytree(ASSETS, DOCS / 'assets')
  build_pages(asset_prefix='assets/', nav_prefix='')


def write_search_index():
  content = js_search_index()
  write(ASSETS / 'js' / 'search-index.js', content)
  write(DOCS / 'assets' / 'js' / 'search-index.js', content)


def readme():
  return """# 宁德时代交互式网站（Demo）\n\n- 纯静态站点，可离线打开\n- 四级页面信息架构（>=17 页）\n- 深色模式（localStorage）、站内搜索、动效与移动端底部导航\n- 不使用外部 CDN/远程字体/外链图片\n\n## 本地查看\n直接打开：`docs/index.html`\n\n## 部署（GitHub Pages）\nPages Source 指向 `main` 分支的 `/docs` 目录。\n\n## 内容说明\n- 标注【示例内容】/【待核实】的部分不代表真实事实，需要你提供报告或权威来源后替换。\n"""


def make_zip():
  zpath = ROOT / 'catl-site.zip'
  if zpath.exists():
    zpath.unlink()
  with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in ['docs','assets','pages','README.md','build.py']:
      base = ROOT / p
      if base.is_file():
        z.write(base, arcname=p)
      else:
        for f in base.rglob('*'):
          if f.is_file():
            z.write(f, arcname=str(f.relative_to(ROOT)))


def main():
  ensure_dirs()
  build_assets()
  build_pages_root()
  build_docs()
  write_search_index()
  write(ROOT / 'README.md', readme())
  make_zip()

if __name__ == '__main__':
  main()
