# -*- coding: utf-8 -*-
"""SWT 擬答驗證＋注入器。
用法： python tools/swt_add.py batch.py [--dry]
batch.py 內含 ENTRIES = [ {num, ans, src, zh, note, 可選 fix/short/skipcheck}, ... ]
標記語法：{and}/{but}=連接詞、[換字|原字]=換字、來源句 ~~...~~=刪掉部分。
檢查：來源句（含刪除部分）必須是 SWT_中文翻譯.html 原文子字串；擬答還原原字後、去掉 and/but 與標點，
必須等於各來源句刪減後的拼接；50–60 字（short 放寬到 30）；換字 3–4 個；連接詞 2–4 個。
"""
import json, re, sys, os, html as _html, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, 'SWT_擬答.html')

def _load_all():
    s = open(os.path.join(ROOT, 'SWT_中文翻譯.html'), encoding='utf-8').read()
    out = {}
    for n in range(1, 180):
        i = s.index('id="a%d"' % n); j = s.index('id="a%d"' % (n + 1)) if n < 179 else s.index('<script>', i)
        blk = s[i:j]
        m = re.search(r'<span class="article-title">(.*?)</span>\s*<span class="article-code">(.*?)</span>', blk, re.S)
        en = re.search(r'<div class="en-text">(.*?)</div>', blk, re.S).group(1)
        en = _html.unescape(re.sub(r'<[^>]+>', '', en))
        en = re.sub(r'\s+', ' ', en).replace(' ,', ',').replace(' .', '.').replace(' ;', ';').replace(' :', ':').strip()
        out[str(n)] = {'title': _html.unescape(m.group(1)).strip(), 'code': m.group(2), 'full': en}
    return out
ALL = _load_all()

def norm(t):
    t = t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return t
def toks(t):
    t = norm(t).lower()
    t = re.sub(r"[^a-z0-9'&\-\s]", ' ', t)
    return [w for w in t.split() if w not in ('and', 'but')]

def check(e):
    n = e['num']; d = ALL[str(n)]; full = norm(d['full']); errs = []
    kept = []
    for s in e['src']:
        plain = norm(s.replace('~~', ''))
        if plain not in full: errs.append('來源句對不上原文: ' + s[:60])
        kept += toks(re.sub(r'~~.+?~~', ' ', norm(s)))
    a = e['ans']
    swaps = re.findall(r'\[([^|\]]+)\|([^\]]+)\]', a)
    if not 3 <= len(swaps) <= 4: errs.append('換字數 %d' % len(swaps))
    conn = re.findall(r'\{(and|but)\}', a)
    if not 2 <= len(conn) <= 4: errs.append('連接詞數 %d' % len(conn))
    plain_new = re.sub(r'\[([^|\]]+)\|[^\]]+\]', r'\1', a); plain_new = re.sub(r'\{(and|but)\}', r'\1', plain_new)
    wc = len(plain_new.split())
    lo = 30 if e.get('short') else 50
    if not lo <= wc <= 60: errs.append('字數 %d' % wc)
    plain_old = re.sub(r'\[[^|\]]+\|([^\]]+)\]', r'\1', a); plain_old = re.sub(r'\{(and|but)\}', r'\1', plain_old)
    at = toks(plain_old)
    fixes = set(tuple(x) for x in e.get('fix', []))  # (擬答token, 來源token) 只在該位置放行
    if len(at) == len(kept):
        at = [k if (a != k and (a, k) in fixes) else a for a, k in zip(at, kept)]
    if e.get('skipcheck'): at = kept
    if at != kept:
        # 找第一個不同處
        i = next((i for i in range(min(len(at), len(kept))) if at[i] != kept[i]), min(len(at), len(kept)))
        errs.append('拼接不符 @%d: 擬答「%s」 vs 來源「%s」' % (i, ' '.join(at[i:i+6]), ' '.join(kept[i:i+6])))
    for k in ('title', 'code', 'zh'):
        if not e.get(k): errs.append('缺 ' + k)
    return wc, errs

def main(path):
    spec = importlib.util.spec_from_file_location('b', path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    ok = True
    for e in m.ENTRIES:
        d = ALL[str(e['num'])]
        e.setdefault('title', d['title']); e.setdefault('code', d['code']); e['full'] = d['full']
        wc, errs = check(e)
        print('#%d %s %d字 %s' % (e['num'], e['title'], wc, '✅' if not errs else '❌ ' + ' | '.join(errs)))
        if errs: ok = False
    if not ok: sys.exit(1)
    if '--dry' in sys.argv: return
    html = open(HTML, encoding='utf-8').read()
    for e in m.ENTRIES:
        if "{num:%d," % e['num'] in html or '"num": %d,' % e['num'] in html:
            print('#%d 已存在，略過' % e['num']); continue
        obj = {k: e[k] for k in ('num', 'title', 'code', 'full', 'ans', 'zh', 'src', 'note') if k in e}
        js = json.dumps(obj, ensure_ascii=False)
        html = html.replace('\n];\n', ',\n' + js + '\n];\n', 1)
    open(HTML, 'w', encoding='utf-8').write(html)
    print('已寫入', HTML)

if __name__ == '__main__':
    main(sys.argv[1])
