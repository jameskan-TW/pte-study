---
name: record-corrections
description: 把 PTE 錯題訂正（閱讀 R-FIB／FIB-DD，之後也會有大作文 WE）整理成 repo 裡的複習頁面。當 James 丟來一份訂正檔（.docx／截圖／PDF），說要「記錄閱讀修正」「加訂正」「整理錯題」「大作文修正」時使用。
---

# 記錄 PTE 錯題訂正

James 會定期丟訂正素材（通常是 ptefighter 網站的答題截圖，貼在 .docx 裡）。
目標：把錯題整理進 repo 的複習頁面，讓他下次能快速認出「做過哪一題、錯在哪、屬於哪種坑」。

**核心原則**：不是列答案，是標出「反覆踩的坑（根因）」。呈現用純文字原文＋標紅，不要做花俏圖表（他明確要求過）。

---

## 目前的產出頁面

| 類型 | 檔案 | 側欄連結 | 狀態 |
|------|------|----------|------|
| 閱讀訂正 | `閱讀訂正.html` | index.html → Reading 下方「🩺 閱讀訂正」 | ✅ 已上線 |
| WFD 訂正 | `WFD_訂正.html` | index.html → 閱讀訂正下方「✍️ WFD 訂正」 | ✅ 已上線（架構，待資料） |
| 大作文修正 | `大作文修正.html` | index.html → Writing 下方「🩺 大作文修正」 | ✅ 已上線 |

新增訂正時**優先 append 到既有頁面的 `DATA` 陣列**，不要重建整頁。

---

## 閱讀訂正流程（已驗證）

### 1. 取出素材
`.docx` 本質是 zip。用 Bash 解開拿圖與文字：
```bash
cp "來源.docx" ./doc.docx
unzip -o -q doc.docx -d doc_extracted
# 題目截圖在 doc_extracted/word/media/image*.png
# 文字解析在 doc_extracted/word/document.xml（用 Python 抽 <w:t> 文字，勿用 jq）
```
用完整 Python 路徑並加 `PYTHONIOENCODING=utf-8`（見全域 CLAUDE.md）。

### 2. OCR 每張截圖（用 Read 工具直接讀圖）
逐張 `Read` `image*.png`。ptefighter 截圖的判讀規則：
- **綠框 + ✓** = 答對的空格 → 記成「已答對」。
- **紅框** = 答錯的空格；正解通常在旁邊用**紅色括號**標出，例如 `tiresome (varied)` 代表「你選 tiresome、正解 varied」。
- 標題列有題名與題號，例如 `Thea Proctor (西婭·普羅克特) #110001`、題型 `FIB-DD`／`R-FIB`。
- ⚠️ **以截圖為準，不要只信 .docx 的文字解析**——實測文字解析漏題、也曾把錯的說成對的（Internet 那篇第 4 格）。務必把每張圖都看過、逐格核對。

### 3. 逐格判「根因類別」（5 類，這是重點）
| key | 名稱 | 判斷訊號 | 例 |
|-----|------|----------|-----|
| `col` | 固定搭配 | 有慣用語／collocation；換個字就不道地 | time slots、grains of sand、orders of magnitude、gas cloud |
| `sem` | 語意精準／線索 | 括號補述、並列詞、上下文語意；選錯是「意思不對」 | ideas↔括號 linguistic ideologies、sharp vs special、blunt and unsubtle |
| `log` | 轉折邏輯 | 句中有 but／however／nevertheless，方向被搞反 | varied（but）、harmless（but）、Nevertheless |
| `pos` | 詞性／詞形 | 該用名詞卻填動名詞、被動要過去分詞、詞形錯 | dissemination（並列名詞）、exposed（can be _）、concerned about |
| `ten` | 時態／語態 | 時態或主被動選錯 | exploring（have been _，主動） |

分不清 `col` 和 `sem` 時：**看得出固定片語 → col；純粹意思對不對 → sem**。

### 4. 寫進 `閱讀訂正.html` 的 DATA 陣列
每篇一個物件。`ok('word')` 標「答對的空格」，`[[n]]` 是第 n 個**錯格**在原文中的位置（依序）：
```js
{ title:"Thea Proctor 西婭·普羅克特", pid:"#110001", type:"FIB-DD",
  text:`... one ${ok('aspect')} of ... It made for a busy and [[1]] life but ...`,
  blanks:[
    { wrong:"tiresome", right:"varied", cat:"log",
      why:`轉折詞 <span class="en">but</span> + 「不是能在家織襪子的人」→ 生活是<b>豐富多采</b>而非厭煩。搭配 <span class="en">a busy and varied life</span>。` },
  ]},
```
規則：
- `text` 用 OCR 出的**完整原文**；答對的空格包 `${ok('...')}`，錯格放 `[[1]] [[2]]…`（順序＝blanks 陣列順序）。
- `why` 是繁中一句話講清楚「為什麼正解對、你的錯在哪」；英文字詞用 `<span class="en">word</span>`、重點用 `<b>`。
- 全對的篇目不進 DATA，改寫進頁面底部 `.done` 那條「已全對」清單。
- 診斷列（弱點統計）與 pill 數字會**自動由 DATA 重算**，不用手改。

### 5. 驗證＋同步
- 用 preview/Browser 開 `閱讀訂正.html`，確認原文、標紅、診斷數字、篩選、自測模式都正常。
- 側欄連結已在 `index.html`（Reading 下方），新增頁面才需要動它。
- Git：**先 `git pull --rebase origin main`**（James 有 Mac／Windows 兩台，遠端常有新 commit），再 commit＋push。commit 訊息用 `feat(Reading): …`。

---

## WFD 訂正流程（頁面已上線，持續 append）

`WFD_訂正.html` 用閱讀訂正同一套引擎，診斷/pill/篩選自動重算。收到聽寫訂正就 append 物件。

類別（依 James 實際錯法定案，5 類）：

| key | 名稱 | 判斷訊號 | 實例 |
|-----|------|----------|------|
| `spell` | 拼字 | 漏／多字母、字母顛倒、難拼字 | mechanics（他四次沒一次對）、mathematics、despite、漏 r |
| `form` | 字尾字形 | 字尾變化、字形選錯 | sometimes 漏 s、classical vs classic、-ing 去 e、過去式 -ed |
| `word` | 多字／漏字 | 多打或漏打整個字（多為功能字） | 多打 be（is considered 被動不用 be）、漏 a/the |
| `s3` | 第三人稱單數 +s | 主詞第三單、動詞漏 s（**頭號罩門**） | he concludes |
| `plural` | 單複數／冠詞 | 名詞該複數沒加 s、冠詞錯 | experiments |

判斷小抄：**字母層級錯 → spell；字尾/字形選錯 → form；整個字多/少 → word**。

DATA 物件格式（`text` 是完整正確句，`[[n]]` 標第 n 個錯字位置；多字/漏字用「你打的短語 → 正確短語」呈現）：
```js
{ title:"Classical mechanics 古典力學", pid:"", type:"WFD",
  text:`[[1]] [[2]] is [[3]] [[4]] as a branch of applied [[5]].`,
  blanks:[
    { wrong:"machenics", right:"mechanics", cat:"spell",
      why:`拼字：<span class="en">me·cha·nics</span>，逐音節確認。` },
    { wrong:"be considered", right:"considered", cat:"word",
      why:`被動 <span class="en">is considered</span>，is + 過去分詞就夠，別多打 be。` },
  ]},
```
`why` 繁中一句話；英文字詞包 `<span class="en">`、重點用 `<b>`。全對的句子不進 DATA。同一句練多次、每次錯不同字 → 彙整成**一張卡**，標出反覆踩的字。

---

## 大作文修正流程（已驗證）

素材：WE（Write Essay）練習後的 AI 批改截圖，紅底/紅字＝被改的地方，旁邊或下一行是修改後版本。用 Read 逐張判讀。

**分類已定案（James 選 5 類完整版）**，`大作文修正.html` 的 CAT key：
| key | 名稱 | 涵蓋 |
|-----|------|------|
| `mech` | 拼字標點 | 拼錯字、標點、大小寫 |
| `gram` | 文法 | 主謂一致、單複數、冠詞 a/the、時態、被動 be+p.p.、動名詞（leading to +Ving） |
| `word` | 用字搭配 | 詞形（responsible→responsibility）、collocation（pay attention to）、介系詞（responsibility for） |
| `stru` | 結構句構 | comma splice、句構斷裂、關係子句、段落/連接詞 |
| `task` | 切題 | 有沒有回應題目、字數、離題 |

`大作文修正.html` 與 `閱讀訂正.html` 用**同一套引擎**：一篇作文＝一個 DATA 物件，`text` 放整篇原文、錯處依序放 `[[1]] [[2]]…`，`blanks` 陣列每筆 `{ wrong:"你寫的", right:"修改後", cat, why }`。診斷列自動抓「最大破口類別」＋「拼字+文法＝基礎準確度」佔比。新增作文就 append 一個物件。

判讀重點（第一篇 2026/08/04 的教訓）：
- **拼字往往是最大破口**（那篇 31 錯裡拼字佔 15）。同一個字重複拼錯要各記一次（累積黑名單）。
- 一個紅字可能同時是拼字＋文法（如 `shuld held`→`should be held`）：拆成兩筆分別記，統計才準。
- 先在頁面 `.good` 區寫一句「做對的地方」（結構/論點通常 OK），焦點放準確度，維持動力。

### 兩軌計錯（2026-08-10 定案，每篇必做）

James 要追蹤「原有的錯誤有沒有在降」，但新題目會帶來新難字，讓總錯數失真（8/07 17 錯 → 8/10 反彈 25 錯，主因是 theoretical/tangible 等新字）。所以每新增一篇 WE 訂正，錯誤要拆成兩軌各自計數：

| 軌 | 名稱 | 涵蓋 | 判斷規則 |
|----|------|------|----------|
| A | **新字錯誤** | 這題才第一次用到的題目專屬難字，拼字或用字錯 | 該字**在本篇之前不在黑名單、也沒在前幾篇出現過** → 算 A（例：theoretical、tangible、prospects） |
| B | **基本錯誤** | 其他全部：常用字/黑名單舊字拼字、文法（+s、冠詞、單複數、Ving）、句構（comma splice）、模板句內任何錯 | 模板句範圍內的錯**一律算 B**（模板背熟了，錯就是基本功）；黑名單已有的字再錯也算 B |

操作：
1. 每筆 blank 判 A/B；A 軌的加欄位 `nv:true`（頁面引擎會忽略未知欄位，無害，但留下機器可讀記號）。
2. 判完把兩個數字寫進三個地方：**回覆 James 的總結**、**commit message**（如 `feat(WE): 訂正第 7 篇 …（基本 12＋新字 6）`）、頁面 `.good` 區那行。
3. **B 軌（基本錯誤）才是進步指標**——回報時以 B 軌趨勢為主，A 軌只提醒把新字收進黑名單。

歷史基準（供比對，第 1～6 篇回溯估算）：

| 篇 | 日期 | 總錯 | 基本(B) | 新字(A) |
|----|------|------|---------|---------|
| 1 父母法律責任 | 8/04 | 31 | ~27 | ~4 |
| 2 蓋路vs大眾運輸 | 8/05 | 21 | ~17 | ~4 |
| 3 信用卡 | 較早 | 28 | ~26 | ~2 |
| 4 延長壽命 | 8/06 | 21 | ~18 | ~3 |
| 5 學業前結婚 | 8/07 | 17 | ~15 | ~2 |
| 6 體驗式學習 | 8/10 | 25 | ~17 | ~8 |

（B 軌實況：27→17→26→18→15→17，比總數平穩，8/10 的反彈大半來自新字。）

### 本篇難字專區（2026-08-10 起，每篇必附）

James 的複習法：「複習每一篇＝複習單字＝複習論點」。每個 WE DATA 物件要有 `vocab` 陣列，渲染在單篇詳情頁 passage 上方（引擎已支援，含自測模式遮英文、點卡翻開）：

```js
vocab:[
  {seg:"開頭"}, {w:"experiential learning",zh:"體驗式學習"},
  {seg:"讓步：效率線"}, {w:"boost productivity",zh:"提高生產力（名詞）"},
  {seg:"主論：理論＋實務"}, {w:"future prospects",zh:"未來前景"},
  {seg:"結尾"}, {w:"tangible",zh:"有形的"},
]
```

規則：
- **字按論證順序排**，用 `{seg:"…"}` 標記段落（開頭／讓步：X線／主論：X線／結尾）——掃一遍 chips 就等於把該篇論點鏈走一遍。seg 名稱盡量帶故事線（效率／減壓／視野／財務／家庭）。
- 收錄「該篇的難字＋關鍵搭配」：A 軌新字必收；模板以外支撐論點的搭配（如 track their spending）也收。zh 註解可帶陷阱提醒（如「不加 the」「名詞」「複數」）。
- 每篇約 10～16 個，別超過 20（超過就不是重點了）。

---

## 別忘的地雷
- OneDrive 同步資料夾放 git，兩台之間 push/pull 前務必先 pull rebase。
- Windows + Git Bash：Python 用完整路徑 + `PYTHONIOENCODING=utf-8`；`jq` 沒裝，JSON 用 Python。
- 輸出一律繁體中文、HTML 格式；沿用頁面既有的 Notion 風格，不另起爐灶。
