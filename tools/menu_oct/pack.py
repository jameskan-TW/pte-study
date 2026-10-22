# -*- coding: utf-8 -*-
"""
產出 閱讀複習包.html（FIB 總統整：28 天當日紀錄的規則 ＋ 閱讀訂正 47 篇 93 格）。

用法（repo 根目錄）：
  PYTHONIOENCODING=utf-8 python tools/menu_oct/pack.py

資料來源（執行時直接讀，不另存）：
  tools/menu_oct/gen.py → LOG（當日紀錄）、WRONG（複習卡一句中文＋分類解釋）
  閱讀訂正.html         → 47 篇 93 格（挖空句、錯選→正解、分類、解析）
改 gen.py 的 LOG／WRONG 或閱讀訂正後，重跑這支即可。
"""
import io, re, html, os
from fibdata import ROOT, rd, LOG, WRONG, ddate, FIB

CAT = {'col': '固定搭配', 'sem': '語意精準', 'log': '轉折邏輯', 'pos': '詞性詞形', 'ten': '時態語態'}
CIRC = '①②③④⑤⑥'
def short_title(tt): return re.split(r'[（(]', tt, 1)[0].strip()
def esc(s): return html.escape(s, quote=False)

# 複習卡（WRONG）對到格：key = (篇序, 正解)
CARD = {}
for d, rows in WRONG.items():
    for (ai, k, rr, w, m, x) in rows:
        CARD.setdefault((ai, rr), []).append((d, m, x))

# ───────── 3. 組頁 ─────────
out = []
A = out.append

A('<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">')
A('<title>閱讀複習包 — FIB 47 篇 93 格＋28 天規則總統整</title>')
A('''<style>
  body{margin:0;background:#fff;color:#222;font-family:"Noto Sans TC",-apple-system,"Segoe UI",sans-serif;line-height:1.75;font-size:16px}
  main{max-width:720px;margin:0 auto;padding:24px 16px 80px}
  h1{font-size:1.7em;margin:.4em 0 .3em}h2{font-size:1.35em;margin:1.8em 0 .5em;padding-bottom:.2em;border-bottom:1px solid #ddd}h3{font-size:1.1em;margin:1.4em 0 .4em}
  h4{font-size:1em;margin:1em 0 .3em}
  blockquote{margin:.8em 0;padding:.5em 1em;border-left:4px solid #bbb;background:#f6f6f6}
  table{border-collapse:collapse;width:100%;margin:.6em 0;font-size:.95em}
  td,th{border:1px solid #ddd;padding:4px 8px;vertical-align:top;text-align:left}
  th{background:#f3f3f3;font-weight:700}
  td:first-child{white-space:nowrap}
  .en{font-family:Consolas,"Noto Sans TC",monospace;color:#0b4f9c}
  .key{font-weight:800;background:#fff3b0;padding:0 4px;border-radius:3px;margin-right:4px}
  .rule{margin:.9em 0;padding:.6em .9em;border-left:4px solid #e0b000;background:#fffbea}
  .rule .d{font-size:.85em;color:#777;margin-left:6px}
  .log{margin:.6em 0;padding:.4em .9em;border-left:4px solid #bbb;background:#f6f6f6}
  .art{margin:1.2em 0 1.6em}
  .art h3 a{color:inherit;text-decoration:none}.art h3 a:hover{text-decoration:underline}
  .blk{margin:.5em 0 .9em;padding-left:.6em;border-left:3px solid #ddd}
  .ctx{font-family:Consolas,"Noto Sans TC",monospace;font-size:.95em;color:#333}
  .ans{font-weight:700;color:#0b6e4f}.wr{color:#b3261e;text-decoration:line-through;margin-left:4px}
  .cat{font-size:.8em;color:#666;border:1px solid #ccc;border-radius:3px;padding:0 5px;margin-left:6px}
  .why{font-size:.95em;color:#333;margin-top:.2em}
  .card{font-size:.9em;color:#555;margin-top:.2em}
  .toc a{margin-right:12px}
  .bar{position:sticky;top:0;background:#fff;border-bottom:1px solid #ddd;padding:6px 0;margin-bottom:8px;font-size:.9em}
  .bar button{font:inherit;padding:2px 10px;margin-right:8px;cursor:pointer}
  body.hide .ans,body.hide .wr{visibility:hidden}
  body.hide .why,body.hide .card{display:none}
  .hint{color:#888;font-size:.85em}
  @media(max-width:600px){td:first-child{white-space:normal}}
</style></head><body><main>''')

A('<div class="bar"><button onclick="document.body.classList.toggle(\'hide\')">遮／顯示答案與解析</button>'
  '<span class="toc"><a href="#s1">§1 核心規則</a><a href="#s2">§2 當日紀錄</a><a href="#s3">§3 分類索引</a><a href="#s4">§4 逐篇</a></span></div>')
A('<h1>閱讀複習包</h1>')
A(f'<p class="hint">FIB 47 篇 93 格 ＋ 十月菜單 28 天當日紀錄，一頁總統整。產出日 2026-10-17；資料來源是 <a href="閱讀訂正.html">閱讀訂正</a> 和 <a href="讀書菜單_10月.html">十月菜單</a>，改那兩邊後重跑 tools/menu_oct/pack.py。</p>')
A('<blockquote><b>怎麼用</b><br>考前一天：只看 §1 核心規則（黃框），每條一句話判斷法。<br>'
  '平時複習：§1 → §3 分類索引（按「遮答案」自己填，填完再看）→ 錯的格去 §4 看完整解析。<br>'
  '共用動作：<b>先看空格旁邊的介系詞、that、of、a／an，再想意思。</b></blockquote>')

# §1 核心規則
keys, others = [], []
for d in sorted(LOG):
    for item in LOG[d]:
        (keys if 'class="key"' in item else others).append((d, item))
A(f'<h2 id="s1">§1 核心規則（{len(keys)} 條，⭐ 黃框）</h2>')
for d, item in keys:
    A(f'<div class="rule"><span class="d">D{d}・{ddate(d)}</span><br>{item}</div>')

# §2 其餘當日紀錄
A(f'<h2 id="s2">§2 當日紀錄其餘條目（{len(others)} 條：固定搭配、要記的字、文法加練）</h2>')
cur = None
for d, item in others:
    if d != cur:
        A(f'<h3>D{d}・{ddate(d)}</h3>'); cur = d
    A(f'<div class="log">{item}</div>')

# §3 分類索引
A('<h2 id="s3">§3 93 格分類索引</h2>')
A('<p class="hint">按上方「遮答案」後，右欄會隱藏，自己填完再開。篇名可點回閱讀訂正。</p>')
order = ['col', 'sem', 'log', 'pos', 'ten']
for c in order:
    rows = [(f, n, b) for f in FIB for n, b in enumerate(f['blanks'], 1) if b['cat'] == c]
    A(f'<h3>{CAT[c]}（{len(rows)} 格）</h3>')
    A('<table><tr><th>篇</th><th>挖空句</th><th>答案（錯選）</th></tr>')
    for f, n, b in rows:
        A(f'<tr><td><a href="#a{f["i"]}">{f["i"]}</a> {esc(short_title(f["t"]))[:12]} {CIRC[n-1]}</td>'
          f'<td class="ctx">{esc(b["ctx"])}</td>'
          f'<td><span class="ans">{esc(b["r"])}</span>' + (f'<span class="wr">{esc(b["w"])}</span>' if b['w'] else '') + '</td></tr>')
    A('</table>')

# §4 逐篇
A('<h2 id="s4">§4 47 篇逐篇解析</h2>')
for f in FIB:
    A(f'<div class="art" id="a{f["i"]}"><h3><a href="閱讀訂正.html#p{f["i"]}" target="_blank">{f["i"]}. {esc(f["t"])}</a> <span class="cat">{f["ty"]}</span>' + (f' <span class="hint">{esc(f["pid"])}</span>' if f['pid'] else '') + '</h3>')
    for n, b in enumerate(f['blanks'], 1):
        A(f'<div class="blk"><div class="ctx">{CIRC[n-1]} {esc(b["ctx"])}</div>'
          f'<div><span class="ans">{esc(b["r"])}</span>' + (f'<span class="wr">{esc(b["w"])}</span>' if b['w'] else '') + f'<span class="cat">{CAT[b["cat"]]}</span></div>'
          f'<div class="why">{b["why"]}</div>')
        for (d, m, x) in CARD.get((f['i'], b['r']), []):
            A(f'<div class="card">複習卡 D{d}：{esc(m)}｜{esc(x)}</div>')
        A('</div>')
    A('</div>')

A('</main></body></html>')
page = '\n'.join(out)
dst = ROOT + '閱讀複習包.html'
io.open(dst, 'w', encoding='utf-8', newline='').write(page)
print('written', dst, len(page), 'bytes; key rules', len(keys), 'other logs', len(others), 'cards', sum(len(v) for v in CARD.values()))
