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
| 大作文修正 | （待建：建議 `大作文修正.html`） | 建議放 Writing 下方 | ⬜ 尚未建立 |

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

## 大作文修正流程（待補）

之後 James 會給 WE（Write Essay）的批改。建立 `大作文修正.html` 時沿用同一套「根因複習」精神，但類別要換成作文導向，建議草案：

- `grammar` 文法（時態一致、主謂一致、冠詞、單複數）
- `word` 用字／搭配（wrong collocation、中式英文、重複用字）
- `structure` 結構（模板、論點展開、連接詞、段落）
- `mechanics` 拼字／標點／大小寫
- `task` 切題（有沒有回應題目、字數）

每則記：`原句（你寫的）` → `修改後` → `根因類別` → `為什麼`。同樣做診斷統計（哪類最常犯）、篩選、自測模式（藏修改後、自己先改）。
**實際建立時，先問 James 要不要沿用上面的類別，再開工。**

---

## 別忘的地雷
- OneDrive 同步資料夾放 git，兩台之間 push/pull 前務必先 pull rebase。
- Windows + Git Bash：Python 用完整路徑 + `PYTHONIOENCODING=utf-8`；`jq` 沒裝，JSON 用 Python。
- 輸出一律繁體中文、HTML 格式；沿用頁面既有的 Notion 風格，不另起爐灶。
