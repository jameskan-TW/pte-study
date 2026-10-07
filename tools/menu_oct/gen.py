# -*- coding: utf-8 -*-
"""
產出 讀書菜單_10月.html（28 天逐日明細版）。

用法（repo 根目錄）：
  PYTHONIOENCODING=utf-8 python tools/menu_oct/gen.py

資料來源（執行時直接讀 repo 頁面抽題庫，不另存 JSON）：
  WFD_訂正.html   → 115 句（D1–D23 照序各 5 句，D24–28 重做多輪句）＋ VQ 176 字（10 字一天，第二輪先反覆卡／WE罩門）
  SWT_擬答.html   → 179 題（#1、#4、#7… stride 3，共 56 題）
  SST_擬答.html   → 62 篇（a1、a3… 隔篇取 28 篇）
  閱讀訂正.html   → 47 篇 93 錯格；W1 七批照篇序切，並自動生成每批「快速複習小字卡」（錯選→正解、根因、原句挖空）

每日紀錄：DAYS 裡每天可加 `log`（HTML 字串陣列）——練完當天由 Claude 補上（錯格、新規則），改這個檔再跑一次即可。
"""
import io, json, re, html, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..')) + os.sep
def rd(name): return io.open(ROOT + name, encoding='utf-8').read()

# ───────── 題庫抽取 ─────────
w = rd('WFD_訂正.html'); i = w.find('const DATA'); j = w.find('const VQ')
WFD = [{'i': k+1, 't': e[0], 'd': e[2]} for k, e in enumerate(re.findall(r'\{ title:"([^"]+)", pid:"[^"]*", type:"([^"]+)", date:"([^"]*)"', w[i:j]))]
k2 = w.find('];', j)
VQ = [{'w': a, 'zh': b, 'tag': c} for a, b, c in re.findall(r"\{w:'([^']+)',zh:'([^']*)',tag:'([^']*)'", w[j:k2])]
assert len(WFD) >= 115 and len(VQ) >= 176, (len(WFD), len(VQ))

t = rd('SWT_擬答.html')
swt_titles = {int(m.group(1)): m.group(2) for m in re.finditer(r'"num":\s*(\d+),\s*"title":\s*"([^"]*)"', t)}
swt_titles.update({int(m.group(1)): m.group(2) for m in re.finditer(r"\{num:(\d+), title:'([^']*)'", t)})
assert len(swt_titles) == 179, len(swt_titles)

u = rd('SST_擬答.html')
SST = [(a, int(n), html.unescape(tt)) for a, n, tt in re.findall(r'id="(a\d+)">\s*<div class="art-hdr">\s*<span class="art-num">#(\d+)</span>\s*<span class="art-title">([^<]*)</span>', u)]
assert len(SST) >= 56, len(SST)

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
    FIB.append({'i': k+1, 't': title, 'pid': pid, 'ty': ty, 'blanks': bl,
                'n': sum(b['cat'] in ('sem', 'col', 'log') for b in bl), 'g': sum(b['cat'] in ('pos', 'ten') for b in bl)})
assert len(FIB) == 47 and sum(len(f['blanks']) for f in FIB) == 93

# ───────── 分配 ─────────
N = 28
def short_wfd(tt): return re.split(r'\s(?=[一-鿿（])', tt, 1)[0].strip()
def short_title(tt): return re.split(r'[（(]', tt, 1)[0].strip()[:44]

wfd_days = [WFD[i*5:(i+1)*5] for i in range(23)]  # 新增句（>115）進不了前 23 天，會進 D24–28 重做池（latest 優先）
hard = [x for x in WFD if ('輪' in x['t'] or '次' in x['t'])]
latest = [x for x in reversed(WFD) if x not in hard]
redo = (hard + latest)[:25]
wfd_days += [redo[i*5:(i+1)*5] for i in range(5)]

pri = [v for v in VQ if ('反覆' in v['tag'] or 'WE' in v['tag'])]
rest = [v for v in VQ if v not in pri]
seq = VQ + pri + rest
vq_days = [seq[i*10:(i+1)*10] for i in range(N)]

swt_nums = [1 + 3*k for k in range(56)]
swt_days = [swt_nums[i*2:(i+1)*2] for i in range(N)]
sst_days = [SST[2*i] for i in range(N)]
SPEAK = ['RA 朗讀 3 題', 'RS 複述 10 句', 'DI 描述圖表 2 張', 'RL 複述講座 1 題']

B = [(1,9),(10,16),(17,22),(23,27),(28,33),(34,41),(42,47)]
def fib_batch(a, b):
    fs = [f for f in FIB if a <= f['i'] <= b]
    n = sum(f['n'] for f in fs)
    links = '、'.join(f'<a href="閱讀訂正.html#p{f["i"]}" target="_blank">{html.escape(short_title(f["t"]))}</a>' for f in fs)
    return n, links

DAYS = []
def D(d, date, we, fib, **kw): DAYS.append(dict(d=d, date=date, we=we, fib=fib, **kw))

w1 = [
 ('10/5 一', '新題 ②-1 修路vs大眾運輸（#7，0905 實戰版 slot）、②-6 法律限制行為（#17）'),
 ('10/6 二', '新題 ④-10 員工參與決策（#18）、④-12 欠發達國家觀光（#20）'),
 ('10/7 三', '新題 ②-11 名人隱私（#32）、②-8 氣候誰負責（#25，跟 #16 共用環境字）'),
 ('10/8 四', '新題 ②-13 21 世紀孩子（#35，跟 #26 手機題角色互換）、②-12 最高薪資（#33）'),
 ('10/9 五', '新題 ③-1 海外學習（#15）、③-2 AI 翻譯還要學外語嗎（#34）——視野線兩題同天'),
 ('10/10 六', '新題 ④-7 政府最緊迫問題失業（#10）＋ D1–D3 六題（#7 #17 #18 #20 #32 #25）錯 slot 重打'),
 ('10/11 日', '週複習：D4–D6 五題（#35 #33 #15 #34 #10）錯 slot 重打＋ 11 題 10 秒決策 rapid-fire'),
]
for k, (date, we) in enumerate(w1):
    a, b = B[k]; n, links = fib_batch(a, b)
    extra = '＋ pos／ten 新增 7 格（詞性時態格一併考）＋重驗「and 前後對齊」「光桿 -ing」' if k == 6 else ''
    D(k+1, date, we, f'第 {k+1} 批 {n} 格：{links}{extra}', heavy=(k==5), review=(k==6))

w2 = [
 ('10/12 一', '重打 ②-4 過勞後果（#12，23 錯）、④-5 家長法律責任（#5，23 錯）', '二輪 ①：第 1–4 批答錯的格重考'),
 ('10/13 二', '重打 ②-7 資訊革命（#21，21 錯）、②-10 城鄉（#30，18 錯）', '二輪 ②：第 5–7 批答錯的格重考'),
 ('10/14 三', '重打 ④-1 經驗vs正規教育（#1，18 錯）、④-3 圖書館（#3，18 錯）', '二輪 ③：二輪還錯的再考；Claude 整理 W1 規則清單（每條附例句）'),
 ('10/15 四', '重打 ④-16 舊建築（#28，18 錯）、④-4 建築設計（#4，17 錯）', '冷題驗證 ①：固定搭配類規則各抽 1–2 格新題（<a href="FIB-RW_拆解.html" target="_blank">FIB-RW 拆解</a>）'),
 ('10/16 五', '重打 ④-8 實踐式學習（#13，17 錯）、②-2 醫療長壽（#8，16 錯）', '冷題驗證 ②：語意／同義複述類規則'),
 ('10/17 六', '重打 ②-9 年齡限制（#29，16 錯）、③-3 外語必修（#37，15 錯）', '冷題驗證 ③：邏輯連接＋詞性時態類規則；沒過的規則標紅'),
 ('10/18 日', '重打 ④-14 名聲vs折扣（#24，15 錯）、④-15 古戲劇（#27，15 錯）＋ 14 題 10 秒決策 rapid-fire', '<a href="閱讀搭配練習.html" target="_blank">閱讀搭配練習</a>上線整頁跑一遍；標紅規則再考'),
]
for k, (date, we, fib) in enumerate(w2): D(k+8, date, we, fib, heavy=(k==5), review=(k==6))

full = [('10/19 一', '#12 過勞後果', '#6 大商場'), ('10/20 二', '#5 家長法律責任', '#22 媒體影響年輕人'), ('10/21 三', '#21 資訊革命', '#23 電視陪伴'), ('10/22 四', '#30 城鄉', '#11 平衡工作'), ('10/23 五', '#1 經驗vs正規教育', '#2 學習vs工作')]
for k, (date, q, slot) in enumerate(full):
    pre = '' if k == 0 else '先重寫昨日錯句 → '
    D(k+15, date, f'{pre}整篇計時 20 分：<b>{q}</b>（<a href="WE_論點總表.html" target="_blank">論點總表</a>關掉，寫完整篇貼 Claude 批改）；slot 重打 1 題：{slot}', 'FIB-RW 冷題 10 格（<a href="FIB-RW_拆解.html" target="_blank">拆解頁</a>），錯格歸因', full=True)
D(20, '10/24 六', '先重寫昨日錯句 → 整篇計時 20 分：<b>冷題</b>（37 題以外，由 Claude 當場出題，練現場組句）', '<a href="閱讀搭配練習.html" target="_blank">閱讀搭配練習</a>再跑一遍', full=True, heavy=True)
D(21, '10/25 日', '驗收：Writing 全套計時——SWT 2 題（#170、#173）＋ WE 1 篇 <b>#28 舊建築</b>＋ WFD 10 句，照考試順序；整份貼 Claude', 'FIB-RW 冷題 20 格計時', exam=True)
D(22, '10/26 一', '重寫驗收錯句 → 整篇計時 20 分：<b>#4 建築設計</b>', 'FIB-RW 冷題 10 格', full=True)
D(23, '10/27 二', 'slot 集中重打 3 題：累計 mistakes 最多的 3 題（看論點總表錯題本計數，不寫整篇）', '<a href="閱讀搭配練習.html" target="_blank">閱讀搭配練習</a>＋<a href="閱讀文法練習.html" target="_blank">閱讀文法練習</a>各跑一遍', review=True)
D(24, '10/28 三', '整篇計時 20 分：<b>#13 實踐式學習</b>', 'FIB-RW 冷題 10 格', full=True)
D(25, '10/29 四', '37 題 10 秒決策 rapid-fire 全跑（一題 30 秒：題型／立場／主論線／讓步線）＋特殊題型六型速查', '標紅規則最後一輪', review=True)
D(26, '10/30 五', '整篇計時 20 分：<b>#8 醫療長壽</b>（最後一篇）', 'FIB-RW 冷題 10 格', full=True)
D(27, '10/31 六', '<a href="WE_封關卡.html" target="_blank">WE_封關卡</a>＋<a href="寫作訂正.html#check" target="_blank">寫作訂正 #check</a>＋黑名單全掃', '只看規則表，不做新題', review=True)
D(28, '11/1 日', '休息日：模板盲打 1 回，其他不碰。考試日確定後把這天對齊考前一天', '—', rest=True)
assert len(DAYS) == 28

# ───────── 每日紀錄（練完由 Claude 補） ─────────
# WRONG[天] = [(閱讀訂正篇序, 空格序 1-based), ...]  → 當天「複習還錯」的格，小字卡只留這些
# （James 2026-10-07：小字卡只留當天複習還錯的，不要整批）
WRONG = {
  # 1: [(1, 1), (9, 3)],
}
# LOG[天] = [HTML…]  → 黃框「當日紀錄」（WFD 錯字、新規則等）
LOG = {
  2: ['<b>WE 兩題 10/7 補練完</b>（#18 員工決策 5 拼字＋11 文法、#20 旅遊 6 拼字＋10 文法，錯題已進 <a href="WE_論點總表.html#q18" target="_blank">總表 #18</a>／<a href="WE_論點總表.html#q20" target="_blank">#20</a> 錯題本）。拼字：slow <span class="en">done</span>→down、<span class="en">knee</span>→keen（改 willing）、<span class="en">hole</span>→whole、<span class="en">conutries</span>、<span class="en">hart</span>→hurt、<span class="en">loose/lose</span>→loss（錯三次）、<span class="en">carelss</span>、<span class="en">toruism</span>、develop<span class="en">ed</span> 掉 -ed。文法三條規則：① 被動要 be＋-ed（should <b>be left</b>／be <b>approved</b>）② make／help＋受詞＋<b>原形</b>，不加 be（makes employees feel…／helps families earn…）③ crucial that 後面原形不加 should。+s 掉 4 次（takes／turns／becomes／helps）。改 James 版：#18 ⑫ willing to work、⑮ 加 work harder；#20 ⑧⑨ become shows for tourists → a loss of real local culture'],
  1: ['<b>WFD 默拼還錯 2 字</b>：<span class="en">definitive</span>（de·fin·i·tive，0805 就錯過）、<span class="en">available</span>（a·vail·a·ble，-able）——已加進 WFD_訂正 #vquiz 默拼庫，明天先重打'],
}
for day in DAYS:
    if day['d'] in LOG: day['log'] = LOG[day['d']]
    if day['d'] in WRONG and WRONG[day['d']]:
        cards = {}
        for (ai, bn) in WRONG[day['d']]:
            f = FIB[ai-1]; b = f['blanks'][bn-1]
            cards.setdefault(ai, {'i': ai, 't': short_title(f['t']), 'items': []})['items'].append(b)
        day['cards'] = [cards[k] for k in sorted(cards)]
        day['cardTitle'] = f"D{day['d']} 複習還錯的格"

for k, day in enumerate(DAYS):
    day['sp'] = SPEAK[k % 4]
    day['wfd'] = [{'i': x['i'], 't': short_wfd(x['t'])} for x in wfd_days[k]]
    day['vq'] = [{'w': v['w'], 'zh': v['zh']} for v in vq_days[k]]
    day['swt'] = [{'n': n, 't': swt_titles[n]} for n in swt_days[k]]
    a, n, tt = sst_days[k]
    day['sst'] = {'a': a, 'n': n, 't': tt}

page = io.open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
page = page.replace('/*__DAYS__*/', 'const DAYS=' + json.dumps(DAYS, ensure_ascii=False) + ';')
out = ROOT + '讀書菜單_10月.html'
io.open(out, 'w', encoding='utf-8', newline='').write(page)
print('written', out, len(page), 'bytes; cards W1:', [len(d.get('cards', [])) for d in DAYS[:7]])
