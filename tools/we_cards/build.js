// 用法：node tools/we_cards/build.js [題號...] → 產 cards.html，再用 Chrome 印成 WE_三分鐘卡.pdf
// 不給題號＝37 題全產（每題都要有 ann/{題號}.json 且驗證通過）
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const { DIR, SLOTS, LINE, strip, load, loadAnn, validate } = require('./lib');

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const md = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
const arrows = s => md(s).replace(/→/g, '<span class="ar">→</span>').replace(/｜/g, '<span class="ar">｜</span>');

// 在格內文字標紅：每個片語找第一個「字邊界完整」且不重疊的位置
function mark(txt, hls) {
  const iv = [];
  const isL = c => /[A-Za-z]/.test(c || '');
  hls.forEach(h => {
    let from = 0;
    while (true) {
      const i = txt.indexOf(h, from); if (i < 0) break;
      const j = i + h.length;
      const okL = !isL(h[0]) || !isL(txt[i - 1]), okR = !isL(h[h.length - 1]) || !isL(txt[j]);
      if (okL && okR && !iv.some(([a, b]) => i < b && j > a)) { iv.push([i, j]); break; }
      from = i + 1;
    }
  });
  iv.sort((a, b) => a[0] - b[0]);
  let out = '', p = 0;
  iv.forEach(([a, b]) => { out += esc(txt.slice(p, a)) + '<mark>' + esc(txt.slice(a, b)) + '</mark>'; p = b; });
  return out + esc(txt.slice(p));
}

function card(d, a) {
  const e = d.es, sl = a.slots || {}, ok = new Set(a.ok || []);
  let rows = '', sec = '';
  SLOTS.forEach(([k, s, name]) => {
    if (e[k] === undefined) return;
    if (s !== sec) { rows += `<tr class="sec"><td colspan="3">${s}</td></tr>`; sec = s; }
    let txt = strip(e[k]);
    if (k === 'subj' && e.modal) txt += ' ' + e.modal;
    if (k === 'result' && e.able) txt = e.able + ' ' + txt;
    const v = sl[k], hl = v ? v.hl || [] : [];
    const w = [ok.has(k) ? '<span class="ok">一次過</span>' : '', v ? md(v.w) : ''].filter(Boolean).join('　');
    rows += `<tr class="${hl.length ? '' : 'calm'}"><td class="k">${name}</td><td class="s">${mark(txt, hl)}</td><td class="w">${w}</td></tr>`;
  });
  const c = a.chain, ln = LINE[d.n[0]] || '';
  const drilled = d.mistakes && d.mistakes.rules ? '🎯 逐格練過' : '📌 舊錯題本';
  const spell = (a.spell || []).map(([r, ...w]) => `<span>${esc(r)}${w.map(x => ' <s>' + esc(x) + '</s>').join('')}</span>`).join('');
  return `<section class="page"><div class="fit">
<div class="head"><h1><span class="no">#${d.o}</span>${esc(d.t)}</h1><div class="meta"><span class="ln l${d.n[0]}">${ln}</span>　總表 ${d.n}　${drilled}</div></div>
<div class="prompt">${esc(d.en)}</div>
<div class="timer">3 分鐘：30 秒看思路 → 2 分鐘掃 18 格（只盯紅字）→ 30 秒念最下面三個最該盯</div>
<h2>思路</h2>
<div class="stance">立場：${md(c.stance)}</div>
<table class="chain">
<tr><td>P1</td><td>${arrows(c.p1)}</td></tr>
<tr><td>P2 讓步</td><td>${arrows(c.p2)}</td></tr>
<tr><td>P3 主論</td><td>${arrows(c.p3)}</td></tr>
<tr><td>P4</td><td>${arrows(c.p4)}</td></tr>
</table>
<h2>18 格：紅字＝你在這題錯過的地方</h2>
<table class="slots"><tr><th>格</th><th>這題的寫法</th><th>提醒</th></tr>${rows}</table>
<h2>這題最該盯的${a.top3.length === 3 ? '三' : '兩'}個</h2>
<div class="top3 n${a.top3.length}">${a.top3.map(t => `<div><b class="tt">${md(t.t)}</b>${md(t.b)}</div>`).join('')}</div>
${spell ? `<div class="spell">拼字：${spell}</div>` : ''}
</div></section>`;
}

const CSS = fs.readFileSync(path.join(DIR, 'card.css'), 'utf8');
const D = load(), want = process.argv.slice(2).map(Number);
const list = D.filter(d => !want.length || want.includes(d.o));
const pages = list.map(d => {
  const a = loadAnn(d.o), e = validate(d, a);
  if (e.length) { console.error('#' + d.o + ' 驗證失敗：\n  ' + e.join('\n  ')); process.exit(1); }
  return card(d, a);
});
const html = `<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><title>WE 三分鐘卡</title><style>${CSS}</style></head><body>
${pages.join('\n')}
<script>
// 每頁超出 A4 就縮字，直到塞進一頁
document.querySelectorAll('.page').forEach(p=>{const f=p.querySelector('.fit'),cs=getComputedStyle(p),room=(p.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom))*0.98;let s=9.2;while(f.scrollHeight>room&&s>6.6){s-=.2;f.style.fontSize=s+'pt'}});
</script></body></html>`;
const out = path.join(DIR, 'cards.html');
fs.writeFileSync(out, html);
const pdf = path.join(DIR, '..', '..', want.length ? `WE_三分鐘卡_${want.join('_')}.pdf` : 'WE_三分鐘卡.pdf');
execFileSync('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ['--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=5000', '--print-to-pdf=' + pdf, 'file://' + out], { stdio: 'ignore' });
const n = (fs.readFileSync(pdf).toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
console.log(`${list.length} 題 → ${path.basename(pdf)}，${n} 頁`);
