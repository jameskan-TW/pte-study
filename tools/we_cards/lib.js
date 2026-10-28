// 三分鐘卡共用：格位順序、中文名、讀資料與註解、驗證
const fs = require('fs'), path = require('path');
const DIR = __dirname;

// 顯示順序：[slot key, 段, 中文名＋編號]；modal／able／p1end 併進其他格顯示
const SLOTS = [
  ['topic', 'P1', '① 主題'], ['va', 'P1', '② 反方說'], ['vb', 'P1', '③ 我方說'], ['p1end', 'P1', 'P1 收尾句'],
  ['con', 'P2 讓步', '④ 承認'], ['conR', 'P2 讓步', '⑤ 對方的理由'], ['cond', 'P2 讓步', '⑥ 如果'], ['subj', 'P2 讓步', '⑦ 主詞'],
  ['resA', 'P2 讓步', '⑧ 就能'], ['resB', 'P2 讓步', '⑨ 進而'], ['concl', 'P2 讓步', '⑩ 難怪'],
  ['stance', 'P3 主論', '⑪ 我的主張'], ['reason', 'P3 主論', '⑫ 因為'], ['jv', 'P3 主論', '⑬ 身分（做什麼）'], ['jn', 'P3 主論', '⑬ 身分（在哪）'],
  ['does', 'P3 主論', '⑭ 做了'], ['result', 'P3 主論', '⑮ 所以他能'], ['impl', 'P3 主論', '⑯ 換句話說'],
  ['final', 'P4', '⑰ 結論立場'], ['rec', 'P4', '⑱ 建議'],
];
const KEYS = SLOTS.map(s => s[0]);
const LINE = { '①': '① 效率線', '②': '② 健康減壓線', '③': '③ 視野線', '④': '④ 職涯財務線' };

const strip = s => String(s || '').replace(/<[^>]+>/g, '').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
const load = () => JSON.parse(fs.readFileSync(path.join(DIR, 'data.json'), 'utf8'));
const annPath = o => path.join(DIR, 'ann', o + '.json');
const loadAnn = o => JSON.parse(fs.readFileSync(annPath(o), 'utf8'));

// 回傳錯誤訊息陣列；空陣列＝通過
function validate(d, a) {
  const err = [], m = d.mistakes || {};
  const ids = new Set([...(m.spell || []).map((_, i) => 's' + i), ...(m.grammar || []).map((_, i) => 'g' + i), ...(m.rules || []).map((_, i) => 'r' + i)]);
  if (a.o !== d.o) err.push('o 不符');
  const c = a.chain || {};
  ['stance', 'p1', 'p2', 'p3', 'p4'].forEach(k => { if (!c[k] || typeof c[k] !== 'string') err.push('chain.' + k + ' 缺'); });
  const used = new Set();
  Object.entries(a.slots || {}).forEach(([k, v]) => {
    if (!KEYS.includes(k)) return err.push('未知格 ' + k);
    if (d.es[k] === undefined) return err.push('這題沒有格 ' + k);
    const txt = strip(d.es[k]);
    (v.hl || []).forEach(h => { if (!txt.includes(h)) err.push(`${k} 紅字「${h}」不在格內文字「${txt}」`); });
    if (!v.w) err.push(k + ' 沒有提醒');
    if (/\b(conR|resA|resB|concl|impl|cond|jv|jn|va|vb)\b/.test(v.w || '')) err.push(k + ' 提醒裡出現格位代號');
    (v.src || []).forEach(s => { if (!ids.has(s)) err.push(k + ' src ' + s + ' 不存在'); used.add(s); });
  });
  (a.ok || []).forEach(k => { if (d.es[k] === undefined) err.push('ok 格 ' + k + ' 不存在'); if (a.slots && a.slots[k] && (a.slots[k].hl || []).length) err.push(k + ' 標一次過卻有紅字'); });
  if (!Array.isArray(a.top3) || a.top3.length < 2 || a.top3.length > 3) err.push('top3 要 2–3 個');
  (a.top3 || []).forEach((t, i) => { if (!t.t || !t.b) err.push('top3[' + i + '] 缺 t/b'); (t.src || []).forEach(s => used.add(s)); });
  if (!Array.isArray(a.spell)) err.push('spell 要是陣列');
  (a.spellSrc || []).forEach(s => used.add(s));
  (a.skipped || []).forEach(s => used.add(String(s).split(/[:：\s]/)[0]));
  ids.forEach(id => { if (!used.has(id)) err.push('錯題 ' + id + ' 沒用到也沒列在 skipped'); });
  return err;
}

module.exports = { DIR, SLOTS, KEYS, LINE, strip, load, loadAnn, annPath, validate };
