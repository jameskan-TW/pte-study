# -*- coding: utf-8 -*-
"""90 天讀書菜單產生器（2026-11-05 → 2027-02-02）

James 2026-11-03 定的規則：
- FIB-D（下拉）／FIB-DD（拖拉）／WFD 只練 ptefighter 2026-11-03 機經標「預測」的題；練過的（git 歷史 閱讀訂正／舊菜單出現過的 #id）排到後面複習
- WE 硬背範文 37 篇、兩天一篇（單數天讀懂＋分段背、雙數天默寫＋限時默打），10 月扎實練過的 9 篇排最後
- 每天兩個時段：早上＝文法（FIB＋WFD＋錯題），下午＝WE

資料：data.json（從 Downloads/*_新題在前_2026-11-03.pdf 抽出）＋ WE_論點總表.html 的 DATA。
用法：PYTHONIOENCODING=utf-8 python tools/menu_90/gen.py → 產出 repo 根目錄 讀書菜單_90天.html（不要手改 HTML）
"""
import json, re, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
START = datetime.date(2026, 11, 5)
NDAYS = 90
WE_DAYS = 74          # 37 篇 × 2 天
NEW_DAYS = 75         # 第 76 天起總複習

# WE 順序：十月 W2「錯最多的 14 題」→ 其餘沒扎實練過的（總表序）→ 已扎實練 9 篇
W2 = [12, 5, 21, 30, 1, 3, 28, 4, 13, 8, 29, 37, 24, 27]

data = json.loads((HERE / 'data.json').read_text(encoding='utf-8'))

# ---- WE：從總表抽 o／t／有沒有 rules ----
t = (ROOT / 'WE_論點總表.html').read_text(encoding='utf-8')
i = t.find('const DATA'); body = t[i:t.find('\n];', i)]
WE = {}
for p in re.split(r'\n(?=\{n:)', body)[1:]:
    m = re.match(r"\{n:'([^']*)', o:(\d+), t:'([^']*)'", p)
    WE[int(m.group(2))] = {'o': int(m.group(2)), 'n': m.group(1), 't': m.group(3), 'firm': 'rules:' in p}
assert len(WE) == 37, len(WE)
firm = sorted(o for o, w in WE.items() if w['firm'])
rest = sorted(o for o in WE if o not in W2 and o not in firm)
we_order = W2 + rest + firm
assert sorted(we_order) == list(range(1, 38))

def chunks(lst, sizes):
    out, k = [], 0
    for s in sizes:
        out.append(lst[k:k + s]); k += s
    return out

def spread(lst, ndays):
    """把 lst 盡量平均攤到 ndays 天"""
    q, r = divmod(len(lst), ndays)
    return chunks(lst, [q + (1 if d < r else 0) for d in range(ndays)])

fd_new = [x for x in data['FIB-D'] if not x['done']]
fd_old = [x for x in data['FIB-D'] if x['done']]
fdd_new = [x for x in data['FIB-DD'] if not x['done']]
fdd_old = [x for x in data['FIB-DD'] if x['done']]
w_new = [x for x in data['WFD'] if not x['old']]
w_old = [x for x in data['WFD'] if x['old']]

FD = spread(fd_new, 60)           # D1–60：4 篇／天
FDD = spread(fdd_new, 48)         # D1–48：2 篇／天
WN = spread(w_new, 20)            # D1–20：5 句／天
WO = spread(w_old, 10)            # D21–30：7 句／天（6 月練過的）
FIB_OLD = spread(fd_old + fdd_old, 15)   # D61–75：練過的預測 FIB 再做一次
REV_WE = spread(we_order, NDAYS - NEW_DAYS)  # D76–90：37 篇限時默打一輪

days = []
for d in range(1, NDAYS + 1):
    date = START + datetime.timedelta(days=d - 1)
    am = []
    if d <= 60: am += [{'k': 'fd', **x} for x in FD[d - 1]]
    if d <= 48: am += [{'k': 'fdd', **x} for x in FDD[d - 1]]
    if 61 <= d <= 75: am += [{'k': 'fd' if x['id'].startswith('08') else 'fdd', 'again': 1, **x} for x in FIB_OLD[d - 61]]
    if d <= 20: am += [{'k': 'wfd', **x} for x in WN[d - 1]]
    elif d <= 30: am += [{'k': 'wfd', 'again': 1, **x} for x in WO[d - 21]]
    am.append({'k': 'wrong', 'final': d > NEW_DAYS})
    if d <= WE_DAYS:
        o = we_order[(d - 1) // 2]
        pm = [{'k': 'we', 'step': 1 if d % 2 else 2, **WE[o]}]
    else:
        pm = [{'k': 'we', 'step': 3, **WE[o]} for o in REV_WE[d - NEW_DAYS - 1]] if d > NEW_DAYS else \
             [{'k': 'weall'}]
    days.append({'d': d, 'date': f'{date.month}/{date.day}', 'iso': date.isoformat(),
                 'wd': '一二三四五六日'[date.weekday()], 'am': am, 'pm': pm})

summary = {'fd': len(fd_new), 'fdOld': len(fd_old), 'fdd': len(fdd_new), 'fddOld': len(fdd_old),
           'wNew': len(w_new), 'wOld': len(w_old), 'end': days[-1]['date']}
SYNC = (HERE / 'sync.js').read_text(encoding='utf-8')
html = (HERE / 'template.html').read_text(encoding='utf-8').replace('/*SYNC*/', SYNC)
html = html.replace('/*DAYS*/', json.dumps(days, ensure_ascii=False)).replace('/*SUM*/', json.dumps(summary, ensure_ascii=False))
(ROOT / '讀書菜單_90天.html').write_text(html, encoding='utf-8')
print('ok', summary, 'WE 順序', we_order)

# ---- FIB 練習頁：題目資料 fib.json（extract_fib.py 產）＋菜單排到哪天 ----
fib = json.loads((HERE / 'fib.json').read_text(encoding='utf-8'))
day_of, seq = {}, []
for day in days:
    for it in day['am']:
        if it['k'] in ('fd', 'fdd') and it['id'] not in day_of:
            day_of[it['id']] = day['d']; seq.append(it['id'])
done = {x['id'] for x in data['FIB-D'] + data['FIB-DD'] if x['done']}
qs = {q['id']: dict(q, day=day_of.get(q['id']), done=q['id'] in done) for q in fib['D'] + fib['DD']}
assert set(seq) == set(qs), set(seq) ^ set(qs)
page = (HERE / 'fib_template.html').read_text(encoding='utf-8').replace('/*SYNC*/', SYNC)
page = page.replace('/*FIB*/', json.dumps([qs[i] for i in seq], ensure_ascii=False))
(ROOT / 'FIB_練習.html').write_text(page, encoding='utf-8')
print('FIB_練習.html', len(seq), '篇')
