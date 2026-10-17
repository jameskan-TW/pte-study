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
# WRONG[天] = [(閱讀訂正篇序, 關鍵片語挖空, 答案, 當時錯選 or '', 一句中文, '分類｜解釋'), ...]
#   → 該天那批 FIB「複習還錯」的格（按批次歸天，不按實際複習日期）
# （James 2026-10-07：小字卡只留當天複習還錯的；2026-10-10：精簡成只留要背的片語，不放整句；再加一行文法／語意解釋）
WRONG = {
  2: [(10, 'a paradoxical time of ____', 'development', 'growing', 'of 後面接名詞', '文法｜介系詞 of 後面要接名詞 → development；growing 是動名詞，學術文偏好正式名詞'),
      (10, 'very ____ brains', 'sharp', 'special', '腦筋敏銳', '語意｜sharp 專指腦筋快、反應敏捷；special 只是「特別」，沒說到聰明'),
      (11, '____, we understand quite well…', 'Nevertheless', 'Therefore', '前後轉折＝然而', '邏輯｜前句說輻射可怕，後句說其實很清楚安全劑量＝轉折 → Nevertheless；Therefore 是因果（因此）'),
      (11, 'orders of ____', 'magnitude', 'volume', '數量級', '搭配｜orders of magnitude 是固定片語；volume（體積、音量）搭不上'),
      (13, 'be ____ to adapt', 'forced', 'struggling', '被迫適應', '語意｜前面說環境結構改變＝外在壓力 → be forced to（被迫）；be struggling to 是自己掙扎，沒有被逼的意思'),
      (14, 'Jasper Johns ____ iconic imagery', 'reimagined', 'have been reimagining', '跟後面 employed／used 並列，過去式', '文法｜分號串三個人：Rauschenberg employed、Rivers used 都是過去簡單式 → 第一個也用過去式 reimagined'),
      (15, 'make its ____ north', 'way', 'direction', 'make its way＝一路前進', '搭配｜make its way 是固定片語（一路往某方向前進）；make its direction 不是英文說法')],
  3: [(18, "the ____ decades of an artist's life", 'closing', 'final', '人生晚期', '搭配｜the closing years／decades 是講「晚年」的慣用說法；final 意思接近但不是正解'),
      (18, 'an ____ old age', 'irrelevant', 'unimportant', '無足輕重的晚年', '語意｜後面說 Monet「打破」這模式 → 一般藝術家晚年是失去影響力、沒人在乎＝irrelevant；unimportant 太籠統'),
      (18, '____ full of fancy cars', 'outhouses', '', '主屋旁的小屋／車庫（英式）', '語意｜破折號後列舉三種「包袱」：停滿名車的房產、愛喝貴酒、一群要養的人；美式 outhouse 是戶外廁所，這裡不是'),
      (20, 'the African ____', 'continent', 'region', '非洲大陸', '語意｜非洲是一整塊大陸 → continent；region 指大陸裡的一小塊地區'),
      (21, 'students in … ____', 'classes', 'disciplines', '修課的學生；-ss 結尾加 -es', '語意＋文法｜students in … classes＝修某課的學生；disciplines 是抽象學科。學生是複數 → 課也用複數，class 是 -ss 結尾所以加 -es'),
      (21, 'the need to ____ for a second taste', 'return', 'review', '回來再吃一次', '語意｜for a second taste＝再嚐一次 → 要「回來」return；review（評論）接不上'),
      (21, 'doubt the ____ of', 'quality', '', '質疑品質', '搭配｜doubt the quality of＝質疑……的品質；懷疑學生開的餐廳，就是懷疑水準'),
      (21, 'think and ____ teaches them', 'actually', '', '真正教會', '文法＋語意｜空格夾在 and 和動詞 teaches 中間 → 要副詞；跟後面「只讀食譜、沒學到」對比 → 真正教會'),
      (21, "which Taylor's ____ reflects", 'menu', '', '菜單反映理念', '文法＋語意｜reflects 有 s → 主詞是單數名詞；餐廳裡能反映「食材全用」理念的是菜單')],
  4: [(23, 'growth in customer power, ____ makes it necessary', 'which', 'that', '這件事使得……', '文法｜逗號後接補充說明只能用 which（指前面整件事）；that 不能放逗號後'),
      (23, 'within the industry ____ is still uncertainty', 'there', 'that', '業界裡有不確定性', '文法｜____ + is + 名詞、意思是「有」→ there is；within the industry 是介系詞片語不能當主詞，that 沒東西可指'),
      (24, 'the virus ____ mostly in remote locations until recently', 'circulated', 'are circulated', '病毒（以前）主要在偏遠地區流傳', '文法｜三關：主詞 the virus 單數；病毒自己流傳、後面沒有 by → 主動；until recently → 過去式。對照同篇 which is transmitted by mosquito bite（被蚊子傳 → 被動）'),
      (25, 'we ____ some 60 years ago', 'plateaued', '', '（進步）停滯、到頂了', '語意｜plateau 當動詞＝走到高原平台不再往上；前面「進步幾千年」＋後面「不再更安全、還在變差」→ 60 年前就停了。recovered（恢復）方向相反'),
      (25, 'paint a ____ future', 'bleak', '', '描繪出黯淡的前景', '搭配｜paint a bleak future／picture／outlook 是固定說法；線索：前面全是慢性病、車禍死亡、塞車等壞消息'),
      (26, 'external ____ of the past centuries', 'domination', 'invasion', '幾世紀的外來支配', '語意｜of the past centuries＝持續幾百年的狀態 → domination（長期支配）；invasion（入侵）是單次事件，撐不了幾世紀'),
      (26, 'a vibrant ____ of popular movements', 'array', 'group', '一系列活躍的人民運動', '搭配｜an array of＝一系列、各式各樣；group 多指一群人，配 movements 不自然'),
      (26, 'rather than elite and foreign ____', 'domination', 'suppression', '而不是菁英和外國主導', '語意｜rather than 對比「誰說了算」：人民參與 vs 菁英外國主導；首尾呼應開頭 external domination。suppression（鎮壓）是動作，不是在講誰作主'),
      (27, 'lofted an uncrewed ____ of the Dragon capsule', 'mockup', 'structure', '無人的實體模型、樣機', '語意｜uncrewed＋of Dragon capsule → 測試送上去的是樣機，不是真的載人艙；structure（結構）太空泛'),
      (27, 'a ____ development', 'promising', 'encouraging', '有前景的進展', '搭配｜a promising development 是慣用搭配；下文想拿 NASA 合約＝未來可期。encouraging 意思近但不是正解'),
      (27, 'if it reached ____', 'orbit', 'route', '進入軌道', '語意｜第一句 reaching orbit 9 minutes later 就是線索（同篇重複同一個字）；太空飛行成功標準＝進入軌道，route 是路線')],
  5: [(28, 'an ____ for students will be a teaching approach', 'attraction', 'approach', '對學生的吸引點', '語意｜上一句 attract a new supply of students → 同字根 attraction；填 approach 變「一個方法會是一個教學方法」等於沒說'),
      (30, 'and [from it] ____ the original wholeness of thought', 'reconstruct', 'emerging', '重建出原本完整的想法', '文法｜遮掉插入語 from it：and 對齊前面 must take（原形）＋後面接名詞片語＝受詞 → 動詞原形'),
      (30, 'There is ____ difficulty in conversation', 'little', 'converging', '對話時沒什麼困難', '文法＋語意｜修飾名詞 difficulty 要形容詞；後面 because 聽者有無數線索 → 困難很少'),
      (30, 'the listener can ____ at any time', 'cut in', 'cut off', '隨時插話', '文法｜cut in＝插話，不接受詞；cut off＝打斷某人，後面要接人（cut him off）。空格後直接 at any time → cut in'),
      (30, 'overcome … by ____ on ideas from different directions', 'converging', 'cut in', '從不同方向匯聚在想法上', '文法＋搭配｜介系詞 by 後面接動作 → V-ing；converge on＝匯聚、集中在。emerging（浮現）語意不對'),
      (30, 'without benefits of physical ____ and emphasis', 'tone', 'intonation', '語氣和強調', '語意＋搭配｜tone＝語氣、口吻（範圍廣）；intonation＝語調高低（偏技術、範圍窄）。tone and emphasis 常一起出現'),
      (31, 'someone someday is sure to try it, ____ Stephan Schuster', 'predicts', 'foresees', '某某人預測', '文法＋語意｜引述句型「意見, ＿＿＋說話者」→ 填「說」類動詞：predict＝pre 先＋dict 說；foresee＝fore 先＋see 看，是腦中預見不是說出來。主詞單數 → predicts'),
      (32, '____ agrarian parties to be important, … must not be integrated', 'For', 'although', '要讓農民政黨變重要', '文法｜空格後是「誰＋to＋動詞」（to be 不是真動詞，不是完整句子）→ For；although 後面要完整句子（parties are important）'),
      (33, 'Mountains restricted gene flow, while the lower Coast Range ____ gene flow', 'facilitated', 'prevented', '（海岸山脈）促進了基因交流', '邏輯｜while 連兩個不同主角＝對比（而）：前半 restricted → 後半相反 facilitated；同句 genetic corridor（走廊＝讓東西通過）、high vs lower 也在對比'),
      (33, 'did not act as a barrier, ____ owls readily fly over this large river', 'suggesting', 'proving', '顯示貓頭鷹能飛越', '語意｜只觀察到「河沒擋住」→ 只能推測，用語氣弱的 suggest／indicate；prove＝證明，要決定性證據。學術文從觀察推結論選弱語氣')],
}
# LOG[天] = [HTML…]  → 黃框「當日紀錄」（WFD 錯字、新規則等）
LOG = {
  7: ['<span class="key">⭐ 第 7 批要記的字</span><a href="閱讀訂正.html#p42" target="_blank">Smarter organism</a>（0819）這篇錯的不是文法，是<b>字不認識、搭配沒看過</b>——這 6 個先背：<table>'
      '<tr><td><span class="en">employ a strategy</span></td><td>採用策略。employ 這裡＝<b>use</b>，不是雇用；文中 <span class="en">employ sophisticated strategies to look for food</span></td></tr>'
      '<tr><td><span class="en">sophisticated</span></td><td>so·phis·ti·cat·ed＝<b>複雜而高級</b>。形容機器／系統／策略 → 先進、精密；形容人 → 世故有品味。<b>不是 precise（精準）</b>：策略沒有準不準，只有高不高明</td></tr>'
      '<tr><td><span class="en">optimize</span></td><td>op·ti·mize＝最佳化，同組 <span class="en">maximize／improve／enhance</span>。本題錯選 polish（潤飾做好的東西）。文法線索：<span class="en">a way <b>that</b> optimize<b>s</b></span>，that 子句主詞是單數 a way → 動詞 +s，原形選項先刪</td></tr>'
      '<tr><td><span class="en">foraging</span></td><td>覓食（動物找食物）。forage 動詞，-ing 當名詞；＝前面的 <span class="en">look for food</span></td></tr>'
      '<tr><td><span class="en">vice versa</span></td><td>反過來也一樣。兩個字分開寫；<span class="en">twice as likely to turn left as right, and vice versa</span></td></tr>'
      '<tr><td><span class="en">rudimentary</span></td><td>ru·di·men·ta·ry＝初級的、還很基本的。常配 <span class="en">memory／knowledge／skills</span>；本題 <span class="en">a rudimentary memory</span>，後面 <span class="en">being able to remember</span> 就是在解釋它</td></tr>'
      '</table>',
      '<span class="key">⭐ ingredient 還是 component</span>一句話：<b>ingredient＝調出來的材料，component＝裝出來的零件</b>。問自己「這東西是調的還是裝的」：食物／藥／化妝品／配方（混合後分不開）→ <span class="en">ingredient</span>（<span class="en">active ingredients</span>、<span class="en">a secret ingredient</span>、<span class="en">the ingredients of success</span>）；機器／系統／計畫／課程（每塊可拆下來）→ <span class="en">component</span>（<span class="en">computer components</span>、<span class="en">a key component of the plan</span>）。<a href="閱讀訂正.html#p43" target="_blank">Wrinkle cure</a> ③ 錯選 components：化妝品是調出來的，而且 <span class="en">active ingredients</span>＝有效成分是藥品／化妝品固定用語。近親 <span class="en">element</span> 最籠統三種都能用，但選項裡有更專門的字時通常不是答案。',
      '<b>Wrinkle cure 要記的字</b>（<a href="閱讀訂正.html#p43" target="_blank">#43</a>，5 格錯 3）：<table>'
      '<tr><td><span class="en">extract</span></td><td>萃取物（名詞，重音在前 EX-tract）；<span class="en">a patented extract of okra seed</span>。① 錯選 ingredients：<b>a 後面只能接單數</b>，複數字先刪</td></tr>'
      '<tr><td><span class="en">active ingredients</span></td><td>有效成分，in·gre·di·ents。④ 連鎖錯：① 把 ingredients 用掉這格就沒字。<b>先鎖定百分之百確定的固定搭配，剩下的字再分</b></td></tr>'
      '<tr><td><span class="en">commissioned by</span></td><td>由…委託，com·mis·sion（兩個 m 兩個 s）；<span class="en">research commissioned by a cosmetics company</span></td></tr>'
      '<tr><td><span class="en">let alone</span></td><td>更別說…。前面是否定句，後面放更難的事；<span class="en">hard to find studies that…, let alone more comprehensive research</span></td></tr>'
      '<tr><td><span class="en">rigorous</span></td><td>嚴謹的，rig·or·ous（or 不是 our）；<span class="en">rigorous studies／research</span>。<span class="en">Even when</span>＝就算…也，後面填正面形容詞</td></tr>'
      '<tr><td><span class="en">comprehensive</span></td><td>全面的，com·pre·hen·sive；<span class="en">comprehensive research</span></td></tr>'
      '</table>',
      '<b>Rudman 要記的字</b>（<a href="閱讀訂正.html#p44" target="_blank">#44</a>，4 格錯 1）：<table>'
      '<tr><td><span class="en">enjoy progress</span></td><td><b>enjoy＝擁有（好東西），不是享受</b>。<span class="en">enjoy progress／success／a reputation／good health</span>；<span class="en">ancient Greece enjoyed unrivalled progress</span>＝古希臘<b>擁有</b>無人能及的進步。受詞是正面的東西 → 動詞用 enjoy</td></tr>'
      '<tr><td><span class="en">punchline</span></td><td>一個字，punch＋line。原本是笑話最後的「笑點」那句，引申＝<b>出人意料的結論</b>。<span class="en">leads to a radical punchline: …</span>。① 錯選 deferred：形容詞修飾的是 punchline 本身，問「這是什麼樣的結論」，不要被後面 after we leave school 的時間字帶走</td></tr>'
      '</table>',
      '<span class="key">⭐ 文法：while／when／after ＋ V-ing</span>前後<b>主詞相同</b> → 第二個主詞省掉，動詞改 -ing。這個 -ing <b>不是進行式</b>，只是主詞被省略後的動詞長相。'
      '<br>原句 <span class="en">ancient Greece enjoyed progress <b>while failing</b> to teach it</span> ＝ <span class="en">…while <b>ancient Greece failed</b> to teach it</span>（進步很大，<b>卻</b>不教）。'
      '<br><b>讀法</b>：看到 while／when／before／after／although ＋ V-ing，把前半的主詞抄一份塞回去、動詞改回正常。<span class="en">She kept smiling while feeling sad</span> → while <b>she felt</b> sad。'
      '<br><b>限制</b>：主詞不同就不能省，要寫完整 <span class="en">Greece made progress while <b>Rome failed</b> to teach it</span>。'
      '<br><b>FIB 用法</b>：空格在 while／when／after 後面、前面沒有新主詞 → 答案是 -ing，原形和過去式選項先刪。while 兩個意思：「當…時」（<span class="en">read while waiting</span>）、「卻」（前後相反，本題）。',
      '<b>Fingerprint 要記的字</b>（<a href="閱讀訂正.html#p46" target="_blank">#46</a>，3 格錯 1）：<table>'
      '<tr><td><span class="en">forensics</span></td><td>fo·ren·sics＝鑑識科學（CSI 那種），字尾 s 但當單數用；<span class="en">referred to as "fingermarks" in forensics</span>＝在鑑識領域叫指痕</td></tr>'
      '<tr><td><span class="en">impression</span></td><td>im·pres·sion。這裡是<b>實體的印痕</b>（壓出來的痕跡），不是「印象」；<span class="en">leaving behind an impression</span>＝留下一個印痕。press＝壓，im-＝進去</td></tr>'
      '<tr><td><span class="en">contaminating materials</span></td><td>con·tam·i·nate＝污染，-ing 當形容詞（去 e）修飾 materials；<span class="en">colorless contaminating materials such as soap, moisturizer and grease</span>＝肥皂、乳液、油脂這些弄髒手指的東西</td></tr>'
      '<tr><td><span class="en">latent</span></td><td>la·tent＝潛伏的、看不見的；<span class="en">described as "latent" as they are invisible to the naked eye</span>。醫學 <span class="en">latent period</span>＝潛伏期</td></tr>'
      '</table>',
      '<span class="key">⭐ A of B ＝「B 的 A」</span>of 前後<b>倒過來讀</b>：<span class="en">principles of sustainability</span>＝永續<b>的原則</b>、<span class="en">employee of the month</span>＝本月<b>的員工</b>、<span class="en">the depth and number of wrinkles</span>＝皺紋<b>的深度和數量</b>、<span class="en">a large volume of foot traffic</span>＝人潮<b>的大量</b>→大量人潮。'
      '<br><b>FIB 用法</b>：空格在 of 前面 → 先翻成中文「B 的 ___」，問 B 這種東西會有什麼。<a href="閱讀訂正.html#p47" target="_blank">Sustainable transportation</a> ① 錯選 regulations：「永續的規定」講不通，理念沒有規定、有的是<b>原則</b> → <span class="en">principles</span>（prin·ci·<b>ple</b>s；prin·ci·pal 是校長）。regulations 是政府訂的條文，配 <span class="en">regulations on smoking</span>（管什麼用 on）。'],
  10: ['<span class="key">⭐ 今日 8 條規則一句話判斷</span>共用動作：<b>先看空格旁邊的介系詞或 that，再想意思</b>（10/14 考 5 批 26 題錯 4，全是沒先看旁邊）<table>'
      '<tr><td>such／so／形容詞</td><td>that 後面的句子<b>完整</b> → 要 such／so；<b>缺一塊</b> → 填形容詞</td></tr>'
      '<tr><td>such 還是 so</td><td>空格後面是<b>名詞</b> → such；<b>形容詞／副詞</b> → so。有 a 時 such 放 a 前面</td></tr>'
      '<tr><td>much／many to do</td><td>往前找複數名詞，to do 的對象<b>是它</b> → many；不是或沒有 → much</td></tr>'
      '<tr><td>roots／origins</td><td>in 後面是<b>地名、年代</b> → origins；<b>原因、機制、情緒</b> → roots</td></tr>'
      '<tr><td>notable for</td><td>空格後面是 <b>for</b> → notable／famous／known for；evident 不接 for</td></tr>'
      '<tr><td>immune from</td><td>空格後面是 <b>from</b> → immune from＝不受…影響</td></tr>'
      '<tr><td>adopt a voice</td><td>空格後面是 voice／tone／manner／approach 這種<b>「方式」類名詞</b> → adopt，不用 make</td></tr>'
      "<tr><td>the same can't be said for</td><td>前面是 the、後面是 can't be said for → <b>same</b>，做對照轉折</td></tr>"
      '</table>',
       '<b>固定句型</b>：<span class="en">such ＋名詞＋ that ～</span>＝如此…以致於…（GM corn ②，錯選 profound）。<span class="en">viewed with <b>such</b> hostility <b>that</b> they are barely grown</span>。線索在空格<b>後面的 that</b>：前面要有 such／so 領頭，that 子句才有人帶；profound hostility 語意通，但填進去 that 就散掉——考句型不考語意。<b>such vs so</b>：後面接名詞 → such（such hostility／such a mess）；接形容詞或副詞 → so（so strong／so quickly）。<b>做題習慣：空格後有 that 引導的結果子句，先想 such／so，再想形容詞。</b><br><b>那怎麼知道 that 是「以致於」還是「這個…」？</b>把 that 後面的句子單獨拿出來看：<b>缺主詞或受詞</b>（<span class="en">a loud voice that ___ can be heard</span>，缺的就是 voice）→ 關係子句，填形容詞；<b>完整句子什麼都不缺</b>（<span class="en">that they are barely grown in Europe</span>）→ 結果子句，前面必須有 such／so。James 用中文邏輯讀成「這個敵視 that…」很順，但英文關係子句的 that 後面一定要缺一塊。（10/14 考 6 題，只錯這條，重練後過）',
       '''<b>固定句型</b>：<span class="en">the same can't be said for ～</span>＝同樣的話不能套在…身上（GM corn ①，錯選 idea）。前句「幾乎沒人懷疑玉米」→ <span class="en">But <b>the same</b> can't be said for</span> 基改——用來做今昔／彼此對照的轉折。said 前面要接「被說的內容」，the same 才講得通；the idea can't be said 不是英文（idea 搭 expressed／put forward）。同家族：<span class="en">the same goes for ～</span>（…也一樣）、<span class="en">the same is true of ～</span>（…也是如此）。''',
       '<b>固定搭配</b>：<span class="en">notable for ～</span>＝以…著稱（New Zealand ①，錯選 evident）。線索在空格<b>後面的 for</b>：<span class="en">a civilization <b>notable</b> for the brilliance of its art</span>。同家族全接 for：<span class="en">famous／renowned／known／celebrated for</span>，for 後面接「出名的優點」。<span class="en">evident</span>（明顯的）不接 for，固定用法是 <span class="en">It is evident that ～</span>／<span class="en">evident in ～</span>，而且「一個明顯的文明」語意不通。<b>今日第 6 個搭配題失分</b>（immune from／roots in／art as well as a science／adopt a voice／critical need／notable for）——<b>看到空格旁邊有介系詞，先用搭配刷選項，再想意思。</b>',
       '<b>固定搭配</b>：<span class="en">adopt a voice／tone／accent／manner</span>＝刻意採用某種說話方式（Origin of Music ①，錯選 make）。<span class="en">the playful voices mothers <b>adopt</b> when speaking to infants</span>＝媽媽對嬰兒說話時<b>換上</b>的俏皮語調。make a voice 不是英文；make 只跟 <span class="en">make a face</span>（做鬼臉）、<span class="en">make a sound／noise</span>（發出聲音）搭。同款：<span class="en">adopt an approach／a strategy／a policy</span>（採用做法／策略／政策）。<b>記：adopt＝採用、換上；空格後是 voice／tone／approach 這種「方式」類名詞 → adopt。</b>',
       '<b>要記的字</b>：<span class="en">conjecture</span>（con·jec·ture）＝猜想、臆測，名詞；指<b>沒有證據、還沒證實的猜</b>。字根 ject＝丟（<span class="en">project</span> 往前丟、<span class="en">reject</span> 丟回去、<span class="en">inject</span> 丟進去），con＋ject＝把想法丟在一起亂湊 → 猜。固定搭配：<span class="en">pure conjecture</span>（純屬猜測）、<span class="en">a matter of conjecture</span>（還是未知數）。Nutrition 題 ①（錯選 conjecture）：<span class="en">revise our ____ for healthy eating</span>——給大眾「修訂」的是 <span class="en">recommendations</span>（建議），不會去修訂一個猜想；而且答案 recommendations 就在文章最後一句。<b>遇到不認識的選項，先掃全文找重複出現的字，再回頭排除。</b>'],
  5: ['<span class="key">⭐ 重點技巧：插入語先遮掉</span>空格前後有插入的小片語（<span class="en">from it</span>、<span class="en">in fact</span>、<span class="en">for that matter</span>、逗號夾住的一段），先遮掉再判斷詞性。例：<span class="en">must take this line of symbols and [from it] ____ the original wholeness</span> → 遮掉 from it 變 <span class="en">must take … and ____ the original wholeness</span>：① and 前後對齊（take 原形 → 空格也原形）② 空格後接名詞片語＝受詞 → 空格是動詞 → <b>reconstruct</b>。曾被 from 騙成「介系詞後接名詞」。<br>三步驟：① 遮插入語 ② 往前找 and／or／but 對齊 ③ 往後看，後面接名詞 → 空格多半是動詞', '<b>要記的字</b>：<span class="en">hereditary</span>（he·red·i·tar·y）＝遺傳的，形容詞（-ary 字尾常是形容詞：necessary／ordinary）。DNA 題 <span class="en">the ____ material</span>：名詞前要形容詞 → <span class="en">hereditary material</span>＝遺傳物質；gene 是名詞塞不進去（「基因的」要說 <span class="en">genetic</span>／<span class="en">hereditary</span>）；後面 <span class="en">passed down from generation to generation</span> 正是 hereditary 的定義',
      '<b>固定搭配</b>：<span class="en">tone and emphasis</span>＝語氣和強調（wholeness 題 ⑤，錯選 intonation）。tone＝語氣、口吻，範圍廣；intonation＝語調高低起伏，偏技術、範圍窄',
      '<b>引述句型</b>（DNA sequence ①，錯選 foresees）：前面一段意見／預測（不一定有引號）＋逗號＋<b>「說」類動詞＋說話者</b>（人、報告、機構）。<span class="en">…, predicts Stephan Schuster</span>＝Schuster predicts that…（倒裝）。說話者也可在前：<span class="en">…, he says</span>（代名詞幾乎都放前面）。「說」類動詞：<span class="en">says／adds／warns／predicts／argues／notes／explains／suggests</span>，單數加 s；不填「看」類（sees／foresees）。<b>不加 which</b>：<span class="en">"…," warns an expert</span> 的主詞是 an expert；加 which 變「這句話警告了專家」意思反了',
      '<b>固定搭配</b>：<span class="en">a driving force behind ～</span>＝背後的推動力、主導者（DNA sequence ③，錯選 carrying；carrying force 不是英文說法）。例：<span class="en">She is the driving force behind the project.</span>',
      '<b>for someone to do something</b>＝讓某人做某事（Agrarian Parties ①，錯選 although）。空格後面有「誰＋<b>to</b>＋動詞」→ 填 <b>For</b>；後面是完整句子（主詞＋are／worked）才考慮 although。兩種用法：① 句首 <span class="en">For you to pass, you must practise.</span>（要讓你及格，就得練習）② <span class="en">It is hard for me to wake up early.</span>（對我來說早起很難）。對照：<span class="en">For the plan to work</span>（要讓計畫成功）vs <span class="en">Although the plan worked</span>（雖然計畫成功了）'],
  4: ['<b>文法加練（which／there 延伸，18 題錯 3 → 二輪全對）三條判斷</b>：'
      '<br>① <b>it 還是 there</b>：說「有」用 <span class="en">there is/are</span>；評論整件事用 <span class="en">It is no wonder／no surprise／important that…</span>、<span class="en">It seems that ＋句子</span>（no 後面接名詞 surprise，不接 surprising）'
      '<br>② <b>there 的動詞看後面名詞</b>：<span class="en">There seem<b>s</b> to be a problem</span>／<span class="en">There seem to be fewer students</span>；it 永遠單數 → <span class="en">It seem<b>s</b></span>'
      '<br>③ <b>what 還是 which</b>：前面有名詞可指 → which（<span class="en">…, which makes／in which</span>）；沒有 → what（<span class="en">What surprised me most was…</span>＝the thing that）',
      '<b>固定搭配</b>：<span class="en">demanding customers</span>＝要求高的顧客（Integrate Sales ①，錯選 considerable；considerable＝相當大的，不能形容顧客難搞）',
      '<b>主被動＋時態加練</b>（Zika circulated 延伸）：意思決定主被動（主詞自己做 → 主動；被別人做、常有 by → 被動），be＋p.p. 只是被動的長相；時態看線索 Today → 現在、until last year → 過去。不規則動詞：<span class="en">spread → spread → spread</span>（沒有 spreaded）、<span class="en">rise → rose → risen</span>（沒有 rised；rise 不接受詞，不能被動）',
      '<b>過去式 vs 過去完成式</b>：一件過去的事用過去式；兩件過去的事比先後，先發生的那件用 had＋p.p.。<span class="en">until 2020／until recently</span> 只是標結束時間，還是一件事 → 過去式（<span class="en">The virus circulated … until recently</span>）。看到 <span class="en">by the time／when／before ＋過去式</span> 在比先後才想 had＋p.p.（<span class="en">When I arrived, the train had left.</span>）'],
  2: ['<b>WE 兩題 10/7 補練完</b>（#18 員工決策 5 拼字＋11 文法、#20 旅遊 6 拼字＋10 文法，錯題已進 <a href="WE_論點總表.html#q18" target="_blank">總表 #18</a>／<a href="WE_論點總表.html#q20" target="_blank">#20</a> 錯題本）。拼字：slow <span class="en">done</span>→down、<span class="en">knee</span>→keen（改 willing）、<span class="en">hole</span>→whole、<span class="en">conutries</span>、<span class="en">hart</span>→hurt、<span class="en">loose/lose</span>→loss（錯三次）、<span class="en">carelss</span>、<span class="en">toruism</span>、develop<span class="en">ed</span> 掉 -ed。文法三條規則：① 被動要 be＋-ed（should <b>be left</b>／be <b>approved</b>）② make／help＋受詞＋<b>原形</b>，不加 be（makes employees feel…／helps families earn…）③ crucial that 後面原形不加 should。+s 掉 4 次（takes／turns／becomes／helps）。改 James 版：#18 ⑫ willing to work、⑮ 加 work harder；#20 ⑧⑨ become shows for tourists → a loss of real local culture', '<b>要記的字</b>：<span class="en">forerunners</span> ＝ 先驅、前身（fore 前 ＋ runner 跑的人 ＋ s）。<span class="en">All three are considered American forerunners of Pop.</span> 搭配 <span class="en">forerunner of ＋ 名詞</span>、<span class="en">be considered ＋ 名詞</span>（被視為）'],
  1: ['<b>WFD 默拼還錯 2 字</b>：<span class="en">definitive</span>（de·fin·i·tive，0805 就錯過）、<span class="en">available</span>（a·vail·a·ble，-able）——已加進 WFD_訂正 #vquiz 默拼庫，明天先重打'],
}
for day in DAYS:
    if day['d'] in LOG: day['log'] = LOG[day['d']]
    if day['d'] in WRONG and WRONG[day['d']]:
        cards = {}
        for (ai, k, r, w, m, x) in WRONG[day['d']]:
            cards.setdefault(ai, {'i': ai, 't': short_title(FIB[ai-1]['t']), 'items': []})['items'].append({'k': k, 'r': r, 'w': w, 'm': m, 'x': x})
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
