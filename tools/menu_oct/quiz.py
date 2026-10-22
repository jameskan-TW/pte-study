# -*- coding: utf-8 -*-
"""
產出 FIB_文法測驗.html（互動測驗：閱讀訂正 47 篇 93 格，一題一張卡）。

用法（repo 根目錄）：
  PYTHONIOENCODING=utf-8 python tools/menu_oct/quiz.py

資料來源（fibdata.py，跟 pack.py 共用）：
  閱讀訂正.html → 挖空句、正解、James 當時錯選、分類、解析
  gen.py WRONG  → 複習卡的中文提示（37 張，對到格就附上）
選項：93 格全部用下面 OPTS 手挑四選一（正解＋當時錯選＋2 個干擾項）。
干擾項原則：語境裡明確錯（文法錯／語意相反／搭配錯），刻意避開放進去也通的同義字
（例：heralded 不放 hailed、ideas 不放 beliefs）。詞性詞形／時態語態 16 格是同字族。
key＝(篇序, 正解)；同篇同正解兩格（#26 domination）用 (篇序, 正解, 當時錯選)。
#25 三格當時是「用猜的」，沒有錯選，改放 3 個干擾項。
改閱讀訂正或 gen.py 後重跑這支（pack.py 也要重跑）。
"""
import io, re, json, os
from fibdata import ROOT, WRONG, FIB

# (篇序, 正解[, 當時錯選]) → 四選一選項；必須含正解＋當時錯選
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
    # ── 以下 77 格 2026-10-22 補：正解, 當時錯選, 干擾×2 ──
    (1, 'so far'):        ['so far', 'until now', 'by far', 'at last'],
    (1, 'challenges'):    ['challenges', 'proves', 'confirms', 'follows'],
    (2, 'slots'):         ['slots', 'duration', 'zones', 'limits'],
    (3, 'grains'):        ['grains', 'sustenance', 'nourishment', 'fertility'],
    (4, 'unsubtle'):      ['unsubtle', 'nuanced', 'subtle', 'polite'],
    (5, 'varied'):        ['varied', 'tiresome', 'quiet', 'idle'],
    (6, 'associated'):    ['associated', 'experimented', 'unrelated', 'attracted'],
    (7, 'ideas'):         ['ideas', 'evidence', 'sounds', 'skills'],
    (8, 'introduction'):  ['introduction', 'exploration', 'removal', 'absence'],
    (9, 'heralded'):      ['heralded', 'concerned', 'ignored', 'limited'],
    (9, 'democratizing'): ['democratizing', 'approaching', 'restricting', 'blocking'],
    (10, 'sharp'):        ['sharp', 'special', 'dull', 'empty'],
    (11, 'Nevertheless'): ['Nevertheless', 'Therefore', 'Moreover', 'Similarly'],
    (11, 'magnitude'):    ['magnitude', 'volume', 'size', 'amount'],
    (12, 'harmless'):     ['harmless', 'harmful', 'toxic', 'deadly'],
    (12, 'concentrated'): ['concentrated', 'condensed', 'diluted', 'scattered'],
    (12, 'cloud'):        ['cloud', 'air', 'stone', 'rain'],
    (13, 'forced'):       ['forced', 'struggling', 'forbidden', 'refused'],
    (15, 'way'):          ['way', 'direction', 'road', 'route'],
    (16, 'illustration'): ['illustration', 'scenario', 'conclusion', 'solution'],
    (16, 'phrase'):       ['phrase', 'sentence', 'word', 'letter'],
    (17, 'tone'):         ['tone', 'standard', 'table', 'record'],
    (17, 'investigation'): ['investigation', 'integration', 'imitation', 'decoration'],
    (18, 'closing'):      ['closing', 'final', 'opening', 'early'],
    (18, 'irrelevant'):   ['irrelevant', 'unimportant', 'important', 'active'],
    (19, 'reduce'):       ['reduce', 'force', 'increase', 'double'],
    (19, 'recent'):       ['recent', 'latest', 'new', 'last'],
    (19, 'force'):        ['force', 'secure', 'prevent', 'delay'],
    (20, 'continent'):    ['continent', 'region', 'country', 'nation'],
    (21, 'classes'):      ['classes', 'disciplines', 'class', 'teachers'],
    (21, 'return'):       ['return', 'review', 'forget', 'refuse'],
    (22, 'utopian'):      ['utopian', 'childhood', 'boring', 'violent'],
    (22, 'childhood'):    ['childhood', 'illusion', 'adulthood', 'politics'],
    (22, 'educational'):  ['educational', 'adults', 'educate', 'educated'],
    (23, 'demanding'):    ['demanding', 'considerable', 'patient', 'loyal'],
    (23, 'fits'):         ['fits', 'adapts', 'fit', 'fitting'],
    (24, 'range'):        ['range', 'immutability', 'stability', 'similarity'],
    (25, 'plateaued'):    ['plateaued', 'improved', 'accelerated', 'expanded'],
    (25, 'equitable'):    ['equitable', 'equity', 'equitably', 'equality'],
    (25, 'bleak'):        ['bleak', 'bright', 'promising', 'rosy'],
    (26, 'domination', 'invasion'):    ['domination', 'invasion', 'friendship', 'approval'],
    (26, 'array'):        ['array', 'group', 'piece', 'lack'],
    (26, 'domination', 'suppression'): ['domination', 'suppression', 'freedom', 'friendship'],
    (27, 'mockup'):       ['mockup', 'structure', 'owner', 'photo'],
    (27, 'promising'):    ['promising', 'encouraging', 'disappointing', 'worrying'],
    (27, 'orbit'):        ['orbit', 'route', 'failure', 'bottom'],
    (28, 'attraction'):   ['attraction', 'approach', 'exam', 'error'],
    (30, 'little'):       ['little', 'converging', 'much', 'few'],
    (30, 'cut in'):       ['cut in', 'cut off', 'cut down', 'cut up'],
    (30, 'converging'):   ['converging', 'cut in', 'diverging', 'separating'],
    (30, 'tone'):         ['tone', 'intonation', 'exercise', 'strength'],
    (31, 'predicts'):     ['predicts', 'foresees', 'doubts', 'denies'],
    (31, 'driving'):      ['driving', 'carrying', 'sales', 'police'],
    (32, 'Thus'):         ['Thus', 'After all', 'Instead', 'Otherwise'],
    (33, 'facilitated'):  ['facilitated', 'prevented', 'blocked', 'limited'],
    (33, 'suggesting'):   ['suggesting', 'proving', 'denying', 'doubting'],
    (34, 'against'):      ['against', 'with', 'for', 'alongside'],
    (34, 'thundered'):    ['thundered', 'praised', 'whispered', 'smiled'],
    (36, 'recommendations'): ['recommendations', 'conjecture', 'discoveries', 'appetites'],
    (36, 'science'):      ['science', 'theme', 'painting', 'meal'],
    (37, 'immune'):       ['immune', 'deducted', 'different', 'distant'],
    (37, 'roots'):        ['roots', 'origins', 'leaves', 'branches'],
    (37, 'little'):       ['little', 'plenty', 'great', 'few'],
    (38, 'so'):           ['so', 'although', 'because', 'unless'],
    (38, 'other'):        ['other', 'these', 'another', 'others'],
    (39, 'adopt'):        ['adopt', 'make', 'hear', 'lose'],
    (39, 'critical'):     ['critical', 'virtual', 'minor', 'false'],
    (40, 'notable'):      ['notable', 'evident', 'blamed', 'punished'],
    (41, 'same'):         ['same', 'idea', 'similar', 'equal'],
    (41, 'such'):         ['such', 'profound', 'so', 'great'],
    (42, 'optimizes'):    ['optimizes', 'polishes', 'wastes', 'hides'],
    (43, 'depth'):        ['depth', 'range', 'age', 'price'],
    (43, 'ingredients'):  ['ingredients', 'components', 'ingredient', 'players'],
    (44, 'radical'):      ['radical', 'deferred', 'traditional', 'familiar'],
    (45, 'utopian'):      ['utopian', 'realistic', 'boring', 'violent'],
    (46, 'locating'):     ['locating', 'copying', 'leaving', 'ignoring'],
    (47, 'principles'):   ['principles', 'regulations', 'principals', 'problems'],
}

CARD = {}
for d, rows in WRONG.items():
    for (ai, k, rr, w, m, x) in rows:
        CARD.setdefault((ai, rr.lower()), (d, m, x))

Q, used = [], set()
for f in FIB:
    for n, b in enumerate(f['blanks'], 1):
        key = (f['i'], b['r'], b['w'])
        if key not in OPTS: key = key[:2]
        opts = OPTS[key]
        used.add(key)
        assert len(opts) == 4 == len({o.lower() for o in opts}) and b['r'] in opts, key
        assert b['w'] in opts or b['w'] == '用猜的', key
        card = CARD.get((f['i'], b['r'].lower()))
        Q.append({
            'id': f"{f['i']}-{n}", 'a': f['i'], 't': re.split(r'[（(]', f['t'], maxsplit=1)[0].strip(),
            'ty': f['ty'], 'cat': b['cat'], 'ctx': b['ctx'], 'r': b['r'], 'w': b['w'],
            'why': b['why'], 'opts': opts,
            'zh': card[1] if card else '', 'card': f"D{card[0]}｜{card[2]}" if card else '',
        })
assert used == set(OPTS), set(OPTS) - used
assert len(Q) == 93

tpl = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quiz_template.html'), encoding='utf-8').read()
page = tpl.replace('/*__DATA__*/[]', json.dumps(Q, ensure_ascii=False).replace('</', '<\\/'))
dst = ROOT + 'FIB_文法測驗.html'
io.open(dst, 'w', encoding='utf-8', newline='\n').write(page)
print('written', dst, len(page), 'chars;', len(Q), 'Qs 全四選一,', sum(1 for q in Q if q['zh']), '附複習卡')
