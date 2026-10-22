# -*- coding: utf-8 -*-
"""
FIB 共用資料（pack.py 複習包、quiz.py 測驗頁共吃）：
  LOG／WRONG ← gen.py；FIB ← 閱讀訂正.html 的 47 篇 93 格。
"""
import io, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..')) + os.sep
def rd(name): return io.open(ROOT + name, encoding='utf-8').read()

# ───────── 1. 從 gen.py 取 LOG / WRONG（純字典字面值，exec 那一段） ─────────
g = io.open(os.path.join(HERE, 'gen.py'), encoding='utf-8').read()
seg = g[g.find('WRONG = {'):g.find('for day in DAYS:')]
ns = {}
exec(seg, ns)
LOG, WRONG = ns['LOG'], ns['WRONG']
def ddate(d): return f'10/{4+d}' if d <= 27 else '11/1'

# ───────── 2. 從閱讀訂正抽 47 篇 93 格（同 gen.py） ─────────
r = rd('閱讀訂正.html'); i = r.find('const DATA')
arts = re.findall(r'\{ title:"([^"]+)", pid:"([^"]*)", type:"([^"]+)"(.*?)(?=\n  \{ title:|\n\];)', r[i:], re.S)
BLANK_RE = re.compile(r'\{ wrong:"([^"]*)", right:"([^"]*)", cat:"(\w+)"(?:, vocab:"[^"]*")?,\s*why:`(.*?)` \}', re.S)
FIB = []
for k, (title, pid, ty, body) in enumerate(arts):
    bl = [{'w': a, 'r': b, 'cat': c, 'why': d.strip()} for a, b, c, d in BLANK_RE.findall(body)]
    txt = re.search(r'text:`(.*?)`,\s*\n\s*blanks:', body, re.S)
    txt = txt.group(1) if txt else ''
    txt = re.sub(r"\$\{ok\('([^']*)'\)\}", r'\1', txt)
    txt = re.sub(r'\$\{ok\("([^"]*)"\)\}', r'\1', txt)
    sents = re.split(r'(?<=[.!?])\s+', txt.replace('\n', ' '))
    for n, b in enumerate(bl, 1):
        ctx = next((s for s in sents if f'[[{n}]]' in s), '')
        def sub(m):
            kk = int(m.group(1))
            return '____' if kk == n else (bl[kk-1]['r'] if kk-1 < len(bl) else '')
        ctx = re.sub(r'\[\[(\d+)\]\]', sub, ctx)
        if len(ctx) > 230:
            p = ctx.find('____'); a = max(0, p - 110); z = min(len(ctx), p + 120)
            ctx = ('…' if a > 0 else '') + ctx[a:z] + ('…' if z < len(ctx) else '')
        b['ctx'] = ctx
    FIB.append({'i': k+1, 't': title, 'pid': pid, 'ty': ty, 'blanks': bl})
assert len(FIB) == 47 and sum(len(f['blanks']) for f in FIB) == 93
