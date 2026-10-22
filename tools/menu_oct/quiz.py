# -*- coding: utf-8 -*-
"""
產出 FIB_文法測驗.html（互動測驗：閱讀訂正 47 篇 93 格，一題一張卡）。

用法（repo 根目錄）：
  PYTHONIOENCODING=utf-8 python tools/menu_oct/quiz.py

資料來源（fibdata.py，跟 pack.py 共用）：
  閱讀訂正.html → 挖空句、正解、James 當時錯選、分類、解析
  gen.py WRONG  → 複習卡的中文提示（37 張，對到格就附上）
選項：詞性詞形／時態語態 16 格用下面 OPTS 手挑的四選一（同字族，只有正解合文法）；
其他格是「正解 vs 當時錯選」二選一——那才是真正會掉的陷阱，不亂生干擾項。
改閱讀訂正或 gen.py 後重跑這支（pack.py 也要重跑）。
"""
import io, re, json, os
from fibdata import ROOT, WRONG, FIB

# (篇序, 正解) → 四選一選項；必須含正解＋當時錯選
OPTS = {
    (9, 'dissemination'): ['democratizing', 'dissemination', 'disseminating', 'distributed'],
    (9, 'concerned'):     ['concerning', 'concerned', 'concern', 'concerns'],
    (10, 'exploring'):    ['explored', 'exploring', 'explores', 'explore'],
    (10, 'development'):  ['growing', 'grown', 'development', 'develops'],
    (11, 'exposed'):      ['exposure', 'exposed', 'exposing', 'expose'],
    (14, 'reimagined'):   ['have been reimagining', 'reimagined', 'has reimagined', 'reimagining'],
    (23, 'which'):        ['that', 'which', 'it', 'what'],
    (23, 'there'):        ['that', 'it', 'there', 'this'],
    (24, 'circulated'):   ['are circulated', 'circulated', 'is circulated', 'circulating'],
    (29, 'hereditary'):   ['gene', 'heredity', 'hereditary', 'hereditarily'],
    (30, 'reconstruct'):  ['emerging', 'reconstruct', 'reconstructing', 'reconstruction'],
    (31, 'molecular'):    ['molecule', 'molecular', 'molecules', 'molecularly'],
    (32, 'for'):          ['although', 'for', 'because', 'despite'],
    (35, 'much'):         ['many', 'much', 'lot', 'more'],
    (43, 'extract'):      ['ingredients', 'extract', 'extracted', 'extracting'],
    (47, 'prosper'):      ['be prospered', 'prosper', 'prosperous', 'prosperity'],
}

CARD = {}
for d, rows in WRONG.items():
    for (ai, k, rr, w, m, x) in rows:
        CARD.setdefault((ai, rr.lower()), (d, m, x))

Q, used = [], set()
for f in FIB:
    for n, b in enumerate(f['blanks'], 1):
        key = (f['i'], b['r'])
        opts = OPTS.get(key)
        if opts:
            used.add(key)
            assert b['r'] in opts and b['w'] in opts, key
        card = CARD.get((f['i'], b['r'].lower()))
        Q.append({
            'id': f"{f['i']}-{n}", 'a': f['i'], 't': re.split(r'[（(]', f['t'], maxsplit=1)[0].strip(),
            'ty': f['ty'], 'cat': b['cat'], 'ctx': b['ctx'], 'r': b['r'], 'w': b['w'],
            'why': b['why'], 'opts': opts or [b['r'], b['w']],
            'zh': card[1] if card else '', 'card': f"D{card[0]}｜{card[2]}" if card else '',
        })
assert used == set(OPTS), set(OPTS) - used
assert len(Q) == 93

tpl = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quiz_template.html'), encoding='utf-8').read()
page = tpl.replace('/*__DATA__*/[]', json.dumps(Q, ensure_ascii=False).replace('</', '<\\/'))
dst = ROOT + 'FIB_文法測驗.html'
io.open(dst, 'w', encoding='utf-8', newline='\n').write(page)
print('written', dst, len(page), 'chars;', len(Q), 'Qs,', len(OPTS), '四選一,', sum(1 for q in Q if q['zh']), '附複習卡')
