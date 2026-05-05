"""
╔══════════════════════════════════════════════════════════╗
║         BriefForge — Content Intelligence Platform       ║
║   Single-file Flask app. Run: python briefforge.py       ║
║   Then open: http://localhost:5000                       ║
╚══════════════════════════════════════════════════════════╝

Install deps first:
    pip install flask flask-cors requests beautifulsoup4 numpy pandas scikit-learn openpyxl cloudscraper
    pip install spacy && python -m spacy download en_core_web_sm   (optional, for entity extraction)
"""

# ═══════════════════════════════════════════════════════════
#  EMBEDDED HTML (served at GET /)
# ═══════════════════════════════════════════════════════════
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>BriefForge — Content Intelligence</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<style>
:root{
  --ink:#0d0d0d; --paper:#f5f0e8; --cream:#ede8df; --gold:#c8a84b;
  --gold-lt:#e8d48a; --rust:#c44b2b; --teal:#1a6b60; --teal-lt:#2a9b8c;
  --muted:#7a7060; --border:#d0c8b8; --card:#faf7f2;
  --serif:'Playfair Display',serif; --sans:'Syne',sans-serif; --mono:'DM Mono',monospace;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--sans);background:var(--paper);color:var(--ink);min-height:100vh;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;z-index:0;opacity:.035;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  pointer-events:none}

/* ── Layout ── */
.wrap{position:relative;z-index:1;max-width:1120px;margin:0 auto;padding:0 28px}

/* ── Header ── */
header{border-bottom:2px solid var(--ink);padding:24px 0 18px;display:flex;align-items:center;gap:16px}
.logo-box{width:46px;height:46px;background:var(--ink);border-radius:5px;display:grid;place-items:center;flex-shrink:0}
.logo-box svg{width:26px;height:26px}
.logo-text h1{font-family:var(--serif);font-size:26px;font-weight:900;letter-spacing:-.5px;line-height:1}
.logo-text p{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--muted);margin-top:3px}
.hdr-right{margin-left:auto;display:flex;align-items:center;gap:10px}
.hdr-badge{font-family:var(--mono);font-size:9px;letter-spacing:2px;text-transform:uppercase;border:1px solid var(--border);padding:4px 10px;border-radius:2px;color:var(--muted)}

/* ── Hero ── */
.hero{padding:52px 0 38px;display:grid;grid-template-columns:1fr 320px;gap:40px;align-items:center;border-bottom:1px solid var(--border)}
.hero h2{font-family:var(--serif);font-size:clamp(36px,5vw,56px);font-weight:900;line-height:1.07;letter-spacing:-1px}
.hero h2 em{font-style:italic;color:var(--teal)}
.hero p{margin-top:14px;font-size:14px;color:var(--muted);line-height:1.75;max-width:460px}
.feat-cards{display:flex;flex-direction:column;gap:10px}
.feat-card{background:var(--cream);border:1px solid var(--border);border-radius:6px;padding:12px 16px;display:flex;align-items:center;gap:12px}
.feat-dot{width:9px;height:9px;border-radius:50%;flex-shrink:0}
.feat-dot.gold{background:var(--gold)} .feat-dot.teal{background:var(--teal)} .feat-dot.rust{background:var(--rust)}
.feat-lbl{font-size:10px;color:var(--muted);font-family:var(--mono);letter-spacing:.5px}
.feat-val{font-size:13px;font-weight:700;margin-top:2px}

/* ── Form ── */
.form-sec{padding:44px 0 28px}
.sec-head{display:flex;align-items:center;gap:12px;margin-bottom:26px}
.sec-num{width:26px;height:26px;background:var(--ink);color:var(--paper);border-radius:50%;font-family:var(--mono);font-size:11px;display:grid;place-items:center;flex-shrink:0}
.sec-head h3{font-family:var(--serif);font-size:22px;font-weight:700}

label{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);font-weight:600;display:block;margin-bottom:7px}
.hint{font-size:9px;letter-spacing:0;text-transform:none;color:var(--muted);margin-left:6px}
input[type=text],input[type=url]{font-family:var(--mono);font-size:13px;background:var(--card);border:1.5px solid var(--border);border-radius:6px;padding:11px 13px;color:var(--ink);transition:border-color .2s;width:100%}
input[type=text]:focus,input[type=url]:focus{outline:none;border-color:var(--teal);box-shadow:0 0 0 3px rgba(26,107,96,.1)}
input::placeholder{color:#b0a898}

.kw-wrap{margin-bottom:22px}
.url-section{margin-bottom:6px}
.url-rows{display:flex;flex-direction:column;gap:8px;margin-bottom:8px}
.url-row{display:flex;gap:8px;align-items:center}
.url-row input{flex:1}
.btn-icon{width:36px;height:36px;border:1.5px solid var(--border);border-radius:6px;background:var(--card);cursor:pointer;display:grid;place-items:center;color:var(--muted);transition:all .15s;flex-shrink:0}
.btn-icon:hover{border-color:var(--rust);color:var(--rust);background:#fff5f5}
.btn-add{font-family:var(--sans);font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;border:1.5px dashed var(--border);background:transparent;border-radius:6px;padding:9px 16px;cursor:pointer;color:var(--muted);width:100%;transition:all .15s}
.btn-add:hover{border-color:var(--teal);color:var(--teal)}

.form-actions{margin-top:26px;display:flex;gap:12px;align-items:center}
.btn-primary{font-family:var(--sans);font-size:13px;font-weight:700;letter-spacing:1px;text-transform:uppercase;background:var(--ink);color:var(--paper);border:none;border-radius:6px;padding:13px 30px;cursor:pointer;transition:all .2s;display:flex;align-items:center;gap:8px}
.btn-primary:hover:not(:disabled){background:var(--teal);transform:translateY(-1px);box-shadow:0 4px 16px rgba(26,107,96,.25)}
.btn-primary:disabled{opacity:.45;cursor:not-allowed}
.btn-ghost{font-family:var(--sans);font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;background:transparent;color:var(--muted);border:1.5px solid var(--border);border-radius:6px;padding:13px 22px;cursor:pointer;transition:all .15s}
.btn-ghost:hover{border-color:var(--ink);color:var(--ink)}

/* ── Error ── */
.err{background:#fef2f2;border:1.5px solid #fca5a5;border-radius:7px;padding:13px 18px;color:#b91c1c;font-size:12px;font-family:var(--mono);margin:14px 0;display:none}

/* ── Progress ── */
#prog-area{display:none;margin:28px 0;background:var(--ink);border-radius:10px;padding:22px;color:var(--paper)}
.prog-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.prog-title{font-family:var(--mono);font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.6}
.prog-pct{font-family:var(--mono);font-size:22px;font-weight:500;color:var(--gold-lt)}
.prog-track{height:4px;background:rgba(255,255,255,.12);border-radius:2px;overflow:hidden;margin-bottom:14px}
.prog-fill{height:100%;background:linear-gradient(90deg,var(--teal-lt),var(--gold-lt));border-radius:2px;transition:width .45s ease;width:0%}
.log-box{font-family:var(--mono);font-size:11px;line-height:1.85;opacity:.7;max-height:130px;overflow-y:auto}
.log-box span{display:block}

/* ── Results ── */
#results{display:none;padding-bottom:80px}
.res-hdr{display:flex;align-items:flex-start;justify-content:space-between;padding:30px 0 22px;border-top:2.5px solid var(--ink)}
.res-kw{font-family:var(--serif);font-size:30px;font-weight:900;line-height:1.15}
.res-kw small{display:block;font-family:var(--sans);font-size:11px;font-weight:400;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:4px}
.btn-export{font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;background:var(--gold);color:var(--ink);border:none;border-radius:6px;padding:11px 20px;cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:7px;white-space:nowrap}
.btn-export:hover{background:var(--gold-lt);transform:translateY(-1px)}

/* ── Metrics ── */
.metrics{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:28px}
.metric{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:16px 14px}
.metric .ml{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:5px;font-family:var(--mono)}
.metric .mv{font-family:var(--serif);font-size:20px;font-weight:700}
.metric.hi{background:var(--teal);border-color:var(--teal)}
.metric.hi .ml,.metric.hi .mv{color:#fff}

/* ── Tabs ── */
.tabs{display:flex;border-bottom:1px solid var(--border);margin-bottom:20px}
.tab{font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;padding:11px 18px;border:none;background:transparent;cursor:pointer;color:var(--muted);border-bottom:2.5px solid transparent;margin-bottom:-1px;transition:all .15s}
.tab.on{color:var(--ink);border-bottom-color:var(--ink)}
.pane{display:none}.pane.on{display:block}

/* ── Panel ── */
.panel{background:var(--card);border:1px solid var(--border);border-radius:10px;overflow:hidden;margin-bottom:16px}
.ph{background:var(--cream);border-bottom:1px solid var(--border);padding:13px 20px;display:flex;align-items:center;justify-content:space-between}
.ph h4{font-size:11px;letter-spacing:2px;text-transform:uppercase;font-weight:700;display:flex;align-items:center;gap:8px}
.badge{font-family:var(--mono);font-size:9px;background:var(--border);padding:2px 7px;border-radius:9px;color:var(--muted)}

/* ── Terms table ── */
.tt{width:100%;border-collapse:collapse}
.tt thead tr{background:rgba(0,0,0,.025)}
.tt th{font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);padding:9px 16px;text-align:left;font-weight:600;border-bottom:1px solid var(--border)}
.tt td{padding:8px 16px;font-family:var(--mono);font-size:12px;border-bottom:1px solid rgba(0,0,0,.04)}
.tt tr:last-child td{border-bottom:none}
.tt tr:hover td{background:rgba(26,107,96,.04)}
.sbar{display:inline-block;height:4px;background:var(--teal);border-radius:2px;vertical-align:middle;margin-right:6px}
.sval{font-size:10px;color:var(--muted)}
.pdots{display:flex;gap:3px;align-items:center}
.pdot{width:6px;height:6px;border-radius:50%}
.pdot.f{background:var(--teal);opacity:.8} .pdot.e{background:var(--border)}

/* ── Headings ── */
.two-col{display:grid;grid-template-columns:3fr 2fr;gap:16px}
.hlist{padding:8px 0}
.hi{display:flex;align-items:flex-start;gap:10px;padding:9px 18px;border-bottom:1px solid rgba(0,0,0,.04);transition:background .12s}
.hi:last-child{border-bottom:none}
.hi:hover{background:rgba(26,107,96,.04)}
.hbadge{font-family:var(--mono);font-size:8px;font-weight:500;padding:2px 6px;border-radius:3px;flex-shrink:0;text-transform:uppercase;letter-spacing:1px;margin-top:1px}
.hbadge.h1{background:var(--ink);color:var(--paper)}
.hbadge.h2{background:var(--teal);color:#fff}
.hbadge.h3{background:var(--border);color:var(--muted)}
.htxt{font-size:12px;flex:1;line-height:1.45;text-transform:capitalize}
.hcnt{font-family:var(--mono);font-size:10px;color:var(--muted);white-space:nowrap;flex-shrink:0}

/* ── Entities ── */
.chips{display:flex;flex-wrap:wrap;gap:7px;padding:14px}
.chip{display:flex;align-items:center;gap:5px;background:var(--cream);border:1px solid var(--border);border-radius:20px;padding:5px 12px;font-size:11px;font-family:var(--mono);cursor:default;transition:all .12s}
.chip:hover{background:var(--teal);color:#fff;border-color:var(--teal)}
.chip .cn{font-size:9px;opacity:.55}

/* ── Competitors ── */
.clist{}
.ci{display:flex;align-items:center;gap:12px;padding:13px 18px;border-bottom:1px solid rgba(0,0,0,.04)}
.ci:last-child{border-bottom:none}
.ci-info{flex:1;overflow:hidden}
.ci-title{font-size:12px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:2px}
.ci-url{font-family:var(--mono);font-size:10px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ci-words{font-family:var(--serif);font-size:18px;font-weight:700;text-align:right;flex-shrink:0}
.ci-words small{display:block;font-family:var(--sans);font-size:8px;letter-spacing:1px;text-transform:uppercase;color:var(--muted);font-weight:400}

/* ── Spinner ── */
@keyframes spin{to{transform:rotate(360deg)}}
.spin{width:14px;height:14px;border:2px solid rgba(255,255,255,.3);border-top-color:#fff;border-radius:50%;animation:spin .7s linear infinite}

/* ── Fade ── */
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
.fu{animation:fadeUp .35s ease forwards}

/* ── Scroll ── */
::-webkit-scrollbar{width:3px}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}

/* ── Responsive ── */
@media(max-width:820px){
  .hero{grid-template-columns:1fr}
  .metrics{grid-template-columns:repeat(2,1fr)}
  .two-col{grid-template-columns:1fr}
}
@media(max-width:500px){
  .wrap{padding:0 16px}
  .metrics{grid-template-columns:1fr 1fr}
}
</style>
</head>
<body>
<div class="wrap">

<!-- Header -->
<header>
  <div class="logo-box">
    <svg viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="3" width="14" height="2" rx="1" fill="#f5f0e8"/>
      <rect x="2" y="8" width="22" height="2" rx="1" fill="#f5f0e8"/>
      <rect x="2" y="13" width="18" height="2" rx="1" fill="#f5f0e8"/>
      <rect x="2" y="18" width="10" height="2" rx="1" fill="#f5f0e8"/>
      <circle cx="21" cy="20" r="4" fill="#c8a84b"/>
      <path d="M19.5 20 L21 21.5 L23 18.5" stroke="#0d0d0d" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
  <div class="logo-text">
    <h1>BriefForge</h1>
    <p>Content Intelligence Platform</p>
  </div>
  <div class="hdr-right">
    <span class="hdr-badge">Anti-Block · v2.1</span>
  </div>
</header>

<!-- Hero -->
<section class="hero">
  <div>
    <h2>Data-driven briefs.<br/><em>Competitor-proof</em> content.</h2>
    <p>Scrape top-ranking competitor pages with anti-block technology, extract TF-IDF terms, entity patterns &amp; heading structures — then export a production-ready content brief.</p>
  </div>
  <div class="feat-cards">
    <div class="feat-card">
      <div class="feat-dot gold"></div>
      <div><div class="feat-lbl">Term Extraction</div><div class="feat-val">TF-IDF · n-grams (1–3)</div></div>
    </div>
    <div class="feat-card">
      <div class="feat-dot teal"></div>
      <div><div class="feat-lbl">Anti-Block</div><div class="feat-val">CloudScraper + UA Rotation</div></div>
    </div>
    <div class="feat-card">
      <div class="feat-dot rust"></div>
      <div><div class="feat-lbl">Export</div><div class="feat-val">Multi-sheet XLSX</div></div>
    </div>
  </div>
</section>

<!-- Form -->
<section class="form-sec">
  <div class="sec-head">
    <div class="sec-num">1</div>
    <h3>Configure Your Brief</h3>
  </div>

  <div class="kw-wrap">
    <label for="kw">Target Keyword</label>
    <input type="text" id="kw" placeholder="e.g. best crm software for small business"/>
  </div>

  <div class="url-section">
    <label>Competitor URLs <span class="hint">(min 2 · max 10)</span></label>
    <div class="url-rows" id="url-rows">
      <div class="url-row">
        <input type="url" placeholder="https://competitor1.com/page"/>
        <button class="btn-icon" onclick="rmUrl(this)" title="Remove">
          <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M1.5 1.5l10 10M11.5 1.5l-10 10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
        </button>
      </div>
      <div class="url-row">
        <input type="url" placeholder="https://competitor2.com/page"/>
        <button class="btn-icon" onclick="rmUrl(this)" title="Remove">
          <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M1.5 1.5l10 10M11.5 1.5l-10 10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
        </button>
      </div>
      <div class="url-row">
        <input type="url" placeholder="https://competitor3.com/page"/>
        <button class="btn-icon" onclick="rmUrl(this)" title="Remove">
          <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M1.5 1.5l10 10M11.5 1.5l-10 10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
        </button>
      </div>
    </div>
    <button class="btn-add" onclick="addUrl()">+ Add another URL</button>
  </div>

  <div class="err" id="err"></div>

  <div class="form-actions">
    <button class="btn-primary" id="gen-btn" onclick="generate()">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      Generate Brief
    </button>
    <button class="btn-ghost" onclick="resetAll()">Clear</button>
  </div>
</section>

<!-- Progress -->
<div id="prog-area">
  <div class="prog-hdr">
    <span class="prog-title">⚙ Processing…</span>
    <span class="prog-pct" id="pct">0%</span>
  </div>
  <div class="prog-track"><div class="prog-fill" id="pfill"></div></div>
  <div class="log-box" id="logbox"></div>
</div>

<!-- Results -->
<section id="results">
  <div class="res-hdr">
    <div class="res-kw">
      <small>Content Brief For</small>
      <span id="res-kw-text">—</span>
    </div>
    <button class="btn-export" onclick="doExport()">
      <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M6.5 1v7.5M4 6l2.5 2.5L9 6M1 10v.5A1.5 1.5 0 002.5 12h8A1.5 1.5 0 0012 10.5V10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      Export XLSX
    </button>
  </div>

  <!-- Metrics -->
  <div class="metrics" id="metrics"></div>

  <!-- Tabs -->
  <div class="tabs">
    <button class="tab on" onclick="goTab('terms',this)">Must-Include Terms</button>
    <button class="tab" onclick="goTab('hdgs',this)">Headings</button>
    <button class="tab" onclick="goTab('ents',this)">Entities</button>
    <button class="tab" onclick="goTab('comps',this)">Competitors</button>
  </div>

  <!-- Terms -->
  <div class="pane on" id="pane-terms">
    <div class="panel">
      <div class="ph"><h4>TF-IDF Ranked Terms <span class="badge" id="terms-cnt">—</span></h4>
        <small style="font-size:10px;color:var(--muted);font-family:var(--mono)">sorted by avg score</small></div>
      <table class="tt"><thead><tr>
        <th>#</th><th>Term / Phrase</th><th>Score</th><th>Relevance</th><th>Pages</th>
      </tr></thead><tbody id="tbody"></tbody></table>
    </div>
  </div>

  <!-- Headings -->
  <div class="pane" id="pane-hdgs">
    <div class="two-col">
      <div class="panel">
        <div class="ph"><h4>H2 Suggestions <span class="badge" id="h2-cnt">—</span></h4></div>
        <div class="hlist" id="h2-list"></div>
      </div>
      <div class="panel">
        <div class="ph"><h4>H3 Suggestions <span class="badge" id="h3-cnt">—</span></h4></div>
        <div class="hlist" id="h3-list"></div>
      </div>
    </div>
  </div>

  <!-- Entities -->
  <div class="pane" id="pane-ents">
    <div class="panel">
      <div class="ph"><h4>Named Entities to Mention <span class="badge" id="ent-cnt">—</span></h4></div>
      <div class="chips" id="ent-chips"></div>
    </div>
  </div>

  <!-- Competitors -->
  <div class="pane" id="pane-comps">
    <div class="panel">
      <div class="ph"><h4>Competitor Analysis</h4></div>
      <div class="clist" id="comp-list"></div>
    </div>
  </div>
</section>

</div><!-- /wrap -->

<script>
// ── state ──────────────────────────────────────────────────
let jobId = null, timer = null;

// ── URL rows ───────────────────────────────────────────────
function addUrl(){
  const rows = document.getElementById('url-rows');
  if(rows.children.length >= 10){alert('Max 10 URLs'); return;}
  const d = document.createElement('div');
  d.className = 'url-row';
  d.innerHTML = `<input type="url" placeholder="https://competitor.com/page"/>
    <button class="btn-icon" onclick="rmUrl(this)" title="Remove">
      <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M1.5 1.5l10 10M11.5 1.5l-10 10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
    </button>`;
  rows.appendChild(d);
}
function rmUrl(btn){
  const rows = document.getElementById('url-rows');
  if(rows.children.length <= 2) return;
  btn.closest('.url-row').remove();
}
function getUrls(){
  return [...document.querySelectorAll('#url-rows input')]
    .map(i=>i.value.trim()).filter(Boolean);
}

// ── tabs ───────────────────────────────────────────────────
function goTab(name, btn){
  document.querySelectorAll('.tab').forEach(b=>b.classList.remove('on'));
  document.querySelectorAll('.pane').forEach(p=>p.classList.remove('on'));
  btn.classList.add('on');
  document.getElementById('pane-'+name).classList.add('on');
}

// ── error ──────────────────────────────────────────────────
function showErr(m){const e=document.getElementById('err'); e.textContent=m; e.style.display='block';}
function hideErr(){document.getElementById('err').style.display='none';}

// ── generate ───────────────────────────────────────────────
async function generate(){
  hideErr();
  const kw = document.getElementById('kw').value.trim();
  const urls = getUrls();
  if(!kw) return showErr('Please enter a target keyword.');
  if(urls.length < 2) return showErr('Please enter at least 2 competitor URLs.');

  const btn = document.getElementById('gen-btn');
  btn.disabled = true;
  btn.innerHTML = '<div class="spin"></div> Generating…';

  document.getElementById('results').style.display = 'none';
  const pa = document.getElementById('prog-area');
  pa.style.display = 'block'; pa.classList.add('fu');
  setProg(0, []);

  try {
    const r = await fetch('/api/generate', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({keyword: kw, urls})
    });
    // ← key fix: check content-type before parsing JSON
    const ct = r.headers.get('content-type') || '';
    if(!ct.includes('application/json')){
      const txt = await r.text();
      throw new Error('Server returned non-JSON:\n' + txt.slice(0,200));
    }
    const data = await r.json();
    if(data.error) throw new Error(data.error);
    jobId = data.job_id;
    timer = setInterval(poll, 1800);
  } catch(e){
    showErr(e.message);
    resetBtn();
  }
}

// ── poll ───────────────────────────────────────────────────
async function poll(){
  if(!jobId) return;
  try {
    const r = await fetch('/api/status/'+jobId);
    const ct = r.headers.get('content-type') || '';
    if(!ct.includes('application/json')){
      clearInterval(timer);
      showErr('Unexpected server response. Is Flask running on port 5000?');
      resetBtn(); return;
    }
    const d = await r.json();
    setProg(d.progress, d.log || []);
    if(d.status === 'done'){ clearInterval(timer); renderBrief(d.brief); }
    else if(d.status === 'error'){ clearInterval(timer); showErr(d.error || 'Unknown error'); resetBtn(); }
  } catch(e){
    clearInterval(timer);
    showErr('Connection lost. Make sure Flask is running: python briefforge.py');
    resetBtn();
  }
}

// ── progress ───────────────────────────────────────────────
function setProg(pct, logs){
  document.getElementById('pfill').style.width = pct+'%';
  document.getElementById('pct').textContent = pct+'%';
  const box = document.getElementById('logbox');
  box.innerHTML = logs.map(l=>`<span>${esc(l)}</span>`).join('');
  box.scrollTop = box.scrollHeight;
}

// ── render ─────────────────────────────────────────────────
function renderBrief(b){
  document.getElementById('prog-area').style.display = 'none';
  const res = document.getElementById('results');
  res.style.display = 'block'; res.classList.add('fu');

  document.getElementById('res-kw-text').textContent = b.keyword;

  // metrics
  const mdata = [
    {l:'Recommended Words', v: b.recommended_word_count, hi:true},
    {l:'Average Words',     v: b.avg_competitor_words.toLocaleString()},
    {l:'Median Words',      v: b.median_competitor_words.toLocaleString()},
    {l:'Min Words',         v: b.min_competitor_words.toLocaleString()},
    {l:'Max Words',         v: b.max_competitor_words.toLocaleString()},
  ];
  document.getElementById('metrics').innerHTML =
    mdata.map(m=>`<div class="metric${m.hi?' hi':''}"><div class="ml">${m.l}</div><div class="mv">${m.v}</div></div>`).join('');

  // terms
  const terms = b.must_include_terms || [];
  const maxS = terms[0]?.score || 1;
  document.getElementById('terms-cnt').textContent = terms.length;
  document.getElementById('tbody').innerHTML = terms.slice(0,40).map((t,i)=>{
    const bw = Math.max(6, Math.round((t.score/maxS)*72));
    const dots = Array.from({length: b.competitor_count},(_,di)=>
      `<span class="pdot ${di<t.pages?'f':'e'}"></span>`).join('');
    return `<tr>
      <td style="color:var(--muted);font-size:10px">${i+1}</td>
      <td style="font-weight:600">${esc(t.term)}</td>
      <td><span class="sbar" style="width:${bw}px"></span><span class="sval">${t.score}</span></td>
      <td><span class="sbar" style="width:${bw}px;background:var(--gold)"></span></td>
      <td><div class="pdots">${dots}</div></td>
    </tr>`;
  }).join('');

  // headings
  const hdgs = b.headings || {};
  renderH('h2', hdgs.h2||[], 'h2-list','h2-cnt');
  renderH('h3', hdgs.h3||[], 'h3-list','h3-cnt');

  // entities
  const ents = b.key_entities || [];
  document.getElementById('ent-cnt').textContent = ents.length;
  document.getElementById('ent-chips').innerHTML = ents.length
    ? ents.map(e=>`<div class="chip">${esc(e.entity)}<span class="cn">×${e.count}</span></div>`).join('')
    : '<p style="padding:14px;color:var(--muted);font-size:12px;font-family:var(--mono)">Install spaCy en_core_web_sm for entity extraction.</p>';

  // competitors
  document.getElementById('comp-list').innerHTML = (b.competitors||[]).map(c=>`
    <div class="ci">
      <div class="ci-info">
        <div class="ci-title">${esc(c.title||'Untitled')}</div>
        <div class="ci-url">${esc(c.url)}</div>
      </div>
      <div class="ci-words">${c.words.toLocaleString()}<small>words</small></div>
    </div>`).join('');

  resetBtn();
  res.scrollIntoView({behavior:'smooth', block:'start'});
}

function renderH(lvl, data, listId, cntId){
  document.getElementById(cntId).textContent = data.length;
  document.getElementById(listId).innerHTML = data.length
    ? data.map(([h,c])=>`<div class="hi">
        <span class="hbadge ${lvl}">${lvl.toUpperCase()}</span>
        <span class="htxt">${esc(h)}</span>
        <span class="hcnt">${c}×</span>
      </div>`).join('')
    : `<p style="padding:14px;color:var(--muted);font-size:12px">No ${lvl.toUpperCase()} headings found.</p>`;
}

// ── export ─────────────────────────────────────────────────
function doExport(){
  if(jobId) window.location.href = '/api/export/'+jobId;
}

// ── reset ──────────────────────────────────────────────────
function resetAll(){
  document.getElementById('kw').value = '';
  document.querySelectorAll('#url-rows input').forEach(i=>i.value='');
  document.getElementById('results').style.display='none';
  document.getElementById('prog-area').style.display='none';
  hideErr(); resetBtn();
}
function resetBtn(){
  const btn=document.getElementById('gen-btn');
  btn.disabled=false;
  btn.innerHTML='<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg> Generate Brief';
}
function esc(s){ return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
</script>
</body>
</html>"""

# ═══════════════════════════════════════════════════════════
#  PYTHON BACKEND
# ═══════════════════════════════════════════════════════════
import re, sys, time, random, threading, json, io, traceback, uuid
from collections import Counter

import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ── Jobs store ─────────────────────────────────────────────
jobs = {}

# ── Anti-block UA pool ─────────────────────────────────────
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
]

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://duckduckgo.com/",
    "https://search.yahoo.com/",
]

def rand_headers():
    return {
        "User-Agent": random.choice(UA_POOL),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,en-GB;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": random.choice(REFERERS),
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
    }

# ── Fetch with 3-layer anti-block chain ────────────────────
def fetch_page(url, logf):
    from bs4 import BeautifulSoup
    import requests

    html = None

    # Layer 1: cloudscraper (Cloudflare bypass)
    try:
        import cloudscraper
        sc = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False},
            delay=3,
        )
        sc.headers.update(rand_headers())
        r = sc.get(url, timeout=22)
        if r.status_code == 200 and len(r.text) > 300:
            html = r.text
            logf(f"  ✅ Fetched (cloudscraper): {url[:70]}")
    except Exception as e:
        logf(f"  ⚠️  cloudscraper: {e}")

    # Layer 2: requests + session + random UA
    if not html:
        try:
            sess = requests.Session()
            sess.headers.update(rand_headers())
            r = sess.get(url, timeout=20, allow_redirects=True)
            if r.status_code == 200 and len(r.text) > 300:
                html = r.text
                logf(f"  ✅ Fetched (requests): {url[:70]}")
            else:
                logf(f"  ⚠️  HTTP {r.status_code}: {url[:70]}")
        except Exception as e:
            logf(f"  ⚠️  requests: {e}")

    # Layer 3: Google cache fallback
    if not html:
        try:
            gc_url = f"https://webcache.googleusercontent.com/search?q=cache:{url}"
            r = requests.get(gc_url, headers=rand_headers(), timeout=15)
            if r.status_code == 200 and len(r.text) > 300:
                html = r.text
                logf(f"  ✅ Fetched (Google cache): {url[:70]}")
        except Exception:
            pass

    if not html:
        logf(f"  ❌ Could not fetch: {url[:70]}")
        return None

    # Parse HTML
    try:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script","style","nav","footer","header","aside","noscript","iframe"]):
            tag.decompose()

        headings = {}
        for lv in range(1, 7):
            tags = soup.find_all(f"h{lv}")
            if tags:
                headings[f"h{lv}"] = [t.get_text(strip=True) for t in tags if t.get_text(strip=True)]

        meta = soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
        meta_desc = meta.get("content", "") if meta else ""
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        raw = soup.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", raw).strip()
        words = len(re.findall(r"\b\w+\b", text))

        return {"url": url, "text": text, "headings": headings,
                "word_count": words, "title": title, "meta_desc": meta_desc}
    except Exception as e:
        logf(f"  ❌ Parse error: {e}")
        return None


# ── Brief generation ───────────────────────────────────────
def make_brief(pages, keyword, logf):
    from sklearn.feature_extraction.text import TfidfVectorizer

    texts = [p["text"] for p in pages]
    wcs   = [p["word_count"] for p in pages]

    logf("🔬 Running TF-IDF analysis…")
    vec = TfidfVectorizer(ngram_range=(1,3), stop_words="english", max_features=1000)
    M   = vec.fit_transform(texts)
    feats   = vec.get_feature_names_out()
    avg_sc  = M.mean(axis=0).A1
    doc_fr  = (M > 0).sum(axis=0).A1
    thresh  = max(1, len(texts) * 0.35)

    terms = [
        {"term": feats[i], "score": round(float(avg_sc[i]),4), "pages": int(doc_fr[i])}
        for i in avg_sc.argsort()[::-1]
        if doc_fr[i] >= thresh and avg_sc[i] > 0.004
    ][:60]

    logf("📐 Analysing headings…")
    hdg_data = {}
    for lv in ["h1","h2","h3"]:
        pool = []
        for p in pages: pool.extend(p["headings"].get(lv, []))
        hdg_data[lv] = [[h, c] for h, c in Counter(x.lower().strip() for x in pool).most_common(20)]

    logf("🏷️  Extracting entities…")
    ents = []
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        raw_ents = []
        SKIP = {"CARDINAL","ORDINAL","DATE","TIME","PERCENT","MONEY","QUANTITY"}
        for p in pages:
            doc = nlp(p["text"][:60000])
            raw_ents.extend(
                (e.text.strip(), e.label_) for e in doc.ents
                if len(e.text.strip()) > 1 and e.label_ not in SKIP
            )
        labels = dict(raw_ents)
        ents = [{"entity":e,"count":c,"type":labels.get(e,"")}
                for e,c in Counter(x[0] for x in raw_ents).most_common(35)]
    except Exception as e:
        logf(f"  ℹ️  Entities skipped ({e})")

    competitors = [
        {"url": p["url"], "title": p.get("title",""), "words": p["word_count"],
         "h2s": len(p["headings"].get("h2",[]))}
        for p in pages
    ]

    return {
        "keyword": keyword,
        "recommended_word_count": f"{int(np.percentile(wcs,25))}–{int(np.percentile(wcs,75))}",
        "avg_competitor_words":    int(np.mean(wcs)),
        "median_competitor_words": int(np.median(wcs)),
        "min_competitor_words":    int(np.min(wcs)),
        "max_competitor_words":    int(np.max(wcs)),
        "competitor_count":        len(pages),
        "competitors":             competitors,
        "must_include_terms":      terms,
        "headings":                hdg_data,
        "key_entities":            ents,
    }


# ── Background worker ──────────────────────────────────────
def worker(job_id, urls, keyword):
    def logf(m): jobs[job_id]["log"].append(m)
    try:
        jobs[job_id]["status"] = "running"
        pages, total = [], len(urls)
        for i, url in enumerate(urls):
            logf(f"🌐 [{i+1}/{total}] {url}")
            jobs[job_id]["progress"] = int((i / total) * 62)
            p = fetch_page(url, logf)
            if p:
                pages.append(p)
                logf(f"  📄 {p['word_count']:,} words · {len(p['headings'].get('h2',[]))} h2s")
            time.sleep(random.uniform(1.2, 2.8))

        if len(pages) < 2:
            raise ValueError(f"Only {len(pages)} page(s) fetched successfully — need at least 2.")

        jobs[job_id]["progress"] = 66
        brief = make_brief(pages, keyword, logf)
        jobs[job_id]["brief"]    = brief
        jobs[job_id]["status"]   = "done"
        jobs[job_id]["progress"] = 100
        logf(f"✅ Done! {len(brief['must_include_terms'])} terms · {len(brief['key_entities'])} entities")
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"]  = str(e)
        logf(f"❌ {e}")
        traceback.print_exc()


# ═══════════════════════════════════════════════════════════
#  ROUTES
# ═══════════════════════════════════════════════════════════

@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data    = request.get_json(force=True, silent=True) or {}
    urls    = [u.strip() for u in data.get("urls", []) if u.strip()]
    keyword = data.get("keyword", "").strip()

    if len(urls) < 2:
        return jsonify({"error": "Provide at least 2 competitor URLs."}), 400
    if not keyword:
        return jsonify({"error": "Keyword is required."}), 400

    jid = str(uuid.uuid4())
    jobs[jid] = {"status":"queued","progress":0,"log":[],"brief":None,"error":None}
    t = threading.Thread(target=worker, args=(jid, urls, keyword), daemon=True)
    t.start()
    return jsonify({"job_id": jid})


@app.route("/api/status/<jid>")
def api_status(jid):
    job = jobs.get(jid)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({
        "status":   job["status"],
        "progress": job["progress"],
        "log":      job["log"][-25:],
        "brief":    job["brief"],
        "error":    job["error"],
    })


@app.route("/api/export/<jid>")
def api_export(jid):
    job = jobs.get(jid)
    if not job or not job.get("brief"):
        return jsonify({"error": "No brief found"}), 404

    b   = job["brief"]
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        # Summary
        pd.DataFrame({
            "Field": ["Keyword","Recommended Word Count","Avg Words","Median Words","Min","Max","Competitors"],
            "Value": [b["keyword"],b["recommended_word_count"],b["avg_competitor_words"],
                      b["median_competitor_words"],b["min_competitor_words"],b["max_competitor_words"],b["competitor_count"]]
        }).to_excel(w, sheet_name="Summary", index=False)

        # Competitors
        if b.get("competitors"):
            pd.DataFrame(b["competitors"]).to_excel(w, sheet_name="Competitors", index=False)

        # Terms
        if b.get("must_include_terms"):
            pd.DataFrame(b["must_include_terms"]).to_excel(w, sheet_name="Must-Include Terms", index=False)

        # Headings
        for lv in ["h1","h2","h3"]:
            rows = b.get("headings",{}).get(lv,[])
            if rows:
                pd.DataFrame(rows, columns=["heading","count"]).to_excel(
                    w, sheet_name=f"{lv.upper()} Suggestions", index=False)

        # Entities
        if b.get("key_entities"):
            pd.DataFrame(b["key_entities"]).to_excel(w, sheet_name="Key Entities", index=False)

    buf.seek(0)
    fn = "brief_" + re.sub(r"[^\w]","_", b["keyword"])[:40] + ".xlsx"
    return send_file(buf,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True, download_name=fn)


@app.route("/health")
def health():
    return jsonify({"ok": True, "jobs": len(jobs)})


# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("\n" + "═"*56)
    print("  BriefForge is running!")
    print("  Open your browser: http://localhost:5000")
    print("═"*56 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
