# -*- coding: utf-8 -*-
"""抽 FIB 練習題資料 → tools/menu_90/fib.json（給 build_fib.py 組 FIB_練習.html）
- FIB-DD（拖拉）：從 Downloads/FIB-DD_新題在前_2026-11-03.pdf 抽。只取黑色字（灰色是疊印防拷層），
  黃底矩形內的字＝空格答案，文章後面一行一個的字＝選項庫
- FIB-D（下拉）：沿用 FIB-RW_拆解.html（6 月機經逐格拆解：文章＋四選項＋解析）
只收 data.json 裡標「預測」的題。用法：PYTHONIOENCODING=utf-8 python tools/menu_90/extract_fib.py [pdf資料夾]
"""
import fitz, re, json, sys, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]; HERE = pathlib.Path(__file__).resolve().parent
PDF_DIR = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path.home() / 'Downloads')
data = json.loads((HERE / 'data.json').read_text(encoding='utf-8'))
pred_d = {x['id']: x for x in data['FIB-D']}; pred_dd = {x['id']: x for x in data['FIB-DD']}

def yellow(g):
    f = g.get('fill'); return f and abs(f[0] - 1) < .02 and abs(f[1] - 1) < .02 and f[2] < .05

# ---------- FIB-DD ----------
doc = fitz.open(PDF_DIR / 'FIB-DD_新題在前_2026-11-03.pdf')
lines = []
for pno in range(10, doc.page_count):
    p = doc[pno]; ys = [fitz.Rect(g['rect']) for g in p.get_drawings() if yellow(g)]
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            out = []
            for s in l['spans']:
                if s['color'] != 0: continue
                r = fitz.Rect(s['bbox'])
                hit = s['text'].strip() and any((r & y).get_area() > .5 * r.get_area() for y in ys)
                out.append('[[%s]]' % s['text'].strip() if hit else s['text'])
            t = ''.join(out)
            if t.strip(): lines.append(t)
skip = re.compile(r'^(Fill in the Blanks.*|\d{4}/\d\d/\d\d|\d+/\d+|Powered by.*|客服微信.*)$')
lines = [l for l in lines if not skip.match(l.strip())]
qs, cur = [], None
for i, l in enumerate(lines):
    m = re.match(r'^\s*(\d+)\.\s+(.*\S)\s*$', l)
    if m and i + 1 < len(lines) and re.match(r'^\s*#\d{6}', lines[i + 1]):
        cur = {'num': int(m.group(1)), 't': m.group(2), 'body': []}; qs.append(cur); continue
    if cur is None: continue
    m = re.match(r'^\s*#(\d{6})', l)
    if m and 'id' not in cur: cur['id'] = m.group(1); continue
    cur['body'].append(l)
DD, bad = [], []
for q in qs:
    if q.get('id') not in pred_dd: continue
    body = q['body']
    # 選項庫＝文章後面「沒有空格、4 字以內、不以句點結尾」的連續短行（從最後一行往回找）
    k = len(body)
    while k > 0 and '[[' not in body[k - 1] and len(body[k - 1].split()) <= 4 and not body[k - 1].rstrip().endswith('.'):
        k -= 1
    opts = [l.strip() for l in body[k:]]
    text = ''
    for l in body[:k]:
        text += l if (not text or text.endswith(' ') or l.startswith(' ')) else ' ' + l
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\]\]\s*\[\[', ' ', text)          # 跨行被拆成兩段的多字答案（at the / same time）
    text = re.sub(r'\s+([.,;:!?)”’])', r'\1', text)
    parts = re.split(r'\[\[(.*?)\]\]', text)
    ans = parts[1::2]
    for a in ans:                                       # 選項庫裡被換行拆開的多字選項，接回去
        if a in opts: continue
        for s in range(len(opts)):
            for e in range(s + 2, min(s + 4, len(opts)) + 1):
                if ' '.join(opts[s:e]) == a: opts[s:e] = [a]; break
            else: continue
            break
    if not ans or not all(a in opts for a in ans): bad.append((q['id'], ans, opts))
    DD.append({'id': q['id'], 't': q['t'], 'k': 'dd', 'parts': parts, 'opts': opts, 'pg': pred_dd[q['id']]['pg']})

# ---------- FIB-D（拆解頁） ----------
t = (ROOT / 'FIB-RW_拆解.html').read_text(encoding='utf-8')
D = []; seen = set()
for blk in re.split(r'<div class="q" ', t)[1:]:
    qid = re.search(r'<span class="q-id">#(\d{6})</span>', blk).group(1)
    if qid not in pred_d or qid in seen: continue
    seen.add(qid)
    title = html.unescape(re.search(r'<span class="q-title">(.*?)</span>', blk).group(1))
    psg = re.search(r'<div class="passage">(.*?)</div>', blk, re.S).group(1)
    parts = re.split(r'<span class="bk"><b>\d+</b>(.*?)</span>', psg)
    parts = [html.unescape(re.sub(r'<[^>]+>', '', p)) for p in parts]
    psg_nums = [int(x) for x in re.findall(r'<span class="bk"><b>(\d+)</b>', psg)]
    bl = {}
    for b in re.findall(r'<div class="blank">(.*?)\n    </div>', blk, re.S):
        no = int(re.search(r'<span class="bl-no">\D*(\d+)</span>', b).group(1))
        ans = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<span class="bl-ans">(.*?)</span>', b).group(1)))
        ops = re.search(r'<span class="bl-opts">(.*?)</span>\s*</div>', b, re.S).group(1)
        opts = [html.unescape(re.sub(r'<[^>]+>', '', o)).strip() for o in ops.split(' / ')]
        why = b[b.find('</div>', b.find('bl-top')) + 6:].strip()
        bl[no] = {'a': ans, 'o': opts, 'why': why}
    blanks = [bl[n] for n in psg_nums if n in bl]
    if qid == '080037': parts[-1] = parts[-1].split(' revoking causing')[0]   # 拆解頁把選項殘字黏進文章尾
    if qid == '080462': blanks[0]['o'] = ['life-span', 'life-space', 'lifestyle', 'life-cycle']   # 拆解頁連字號選項被拆開
    for i, b in enumerate(blanks):                  # 句首大小寫不同（Through／through）→ 以文章為準
        a = parts[1 + 2 * i] if 1 + 2 * i < len(parts) else b['a']
        b['o'] = [a if o.lower() == a.lower() else o for o in b['o']]; b['a'] = a
        if a not in b['o']: b['o'].insert(0, a)    # 拆解頁漏抓正解選項（#080384 as well as、#080531 build）
    n = len(parts) // 2
    if len(blanks) != n or any(parts[1 + 2 * i] != blanks[i]['a'] for i in range(n)) or any(b['a'] not in b['o'] for b in blanks):
        bad.append((qid, 'D mismatch', n, len(blanks)))
    D.append({'id': qid, 't': title, 'k': 'd', 'parts': parts, 'blanks': blanks, 'pg': pred_d[qid]['pg']})
# 拆解頁（6 月版）沒有的新題，手動從 FIB-D PDF p216 補（黃底＝答案）
MANUAL = [{'id': '080555', 't': 'Communication skills', 'k': 'd', 'parts': [
    'In terms of your own communication skills, it is important to give just as much of your attention to a message you are receiving as to one you are giving. Listening, ', 'for example',
    ', as well as being a method for gathering information, ', 'can convey',
    ' your interest in what the other person is concerned with. This in itself can have a positive effect on your relationship with them and, if you are their manager, their motivation. Asking questions for ', 'clarification',
    ' of the detail of the message can also convey that you have understood the message and that you want to respond to it ', 'appropriately', '.'],
    'blanks': [{'a': 'for example', 'o': ['for example', 'as example', 'in example', 'for instance of'], 'why': ''},
               {'a': 'can convey', 'o': ['is conveying', 'can deliver', 'can convey', 'is able convey'], 'why': ''},
               {'a': 'clarification', 'o': ['explanation', 'clarity', 'clarification', 'clearing'], 'why': ''},
               {'a': 'appropriately', 'o': ['professionally', 'appropriately', 'nice', 'occasionally'], 'why': ''}]}]
for m in MANUAL:
    if m['id'] in pred_d and m['id'] not in seen:
        m['pg'] = pred_d[m['id']]['pg']; D.append(m); seen.add(m['id'])
# 照菜單順序（PDF 順序）排
order = {x['id']: i for i, x in enumerate(data['FIB-D'])}; D.sort(key=lambda q: order[q['id']])
missing = sorted(set(pred_d) - seen)
out = {'D': D, 'DD': DD}
(HERE / 'fib.json').write_text(json.dumps(out, ensure_ascii=False), encoding='utf-8')
print('DD', len(DD), '/', len(pred_dd), 'D', len(D), '/', len(pred_d), 'missing D', missing, 'bad', len(bad))
for b in bad[:15]: print(' ', b)
