# pte-study — James 的 PTE 備考網站

James 正在準備 PTE，弱項是 Writing 和拼字。本 repo 是一組純靜態 HTML 學習頁（無框架、無 build），
部署在 GitHub Pages：jameskan-tw.github.io/pte-study（push 後約 1-2 分鐘生效）。

**先讀 `HANDOFF.md`**——那是 WE（Write Essay）工程的單一事實來源，含五大論據、mistakes 資料結構、DATA 提取範本。本檔只補 HANDOFF 沒寫的全局脈絡。

## 檔案地圖（2026-08-07 全站重組後：分「訂正區」和「題庫區」）

**🩺 訂正區（James 自己的錯題，一篇一篇累積，複習價值最高）**

| 檔案 | 用途 |
|------|------|
| `寫作訂正.html` | WE 錯誤一條龍，三分頁（hash 直達）：`#review` 看根因（整篇錯誤＋跨篇趨勢）、`#rewrite` 動手改（錯句重寫）、`#check` 考前掃（5 條自檢）。**拼字黑名單只有這裡一份**（共用 `BLACKLIST` 陣列，①頁尾與③同吃）。新增 WE 訂正就加進這檔的 `DATA` |
| `閱讀訂正.html` | R-FIB／FIB-DD 錯題訂正，目錄制（目錄卡→單篇詳情），根因分類＋自測模式 |
| `WFD_訂正.html` | 聽寫訂正＋要背單字 chips；頁尾 `#vquiz` 是 57 字易錯默拼測驗（原 WFD_易錯單字庫 併入，WFD＋WE 罩門字合一）。新錯字加 `DATA`，新默拼字加 `VQ` |
| `WE_封關卡.html` | 考前模板＋模板專屬罩門（view/and one/吞小字）；文法拼字罩門是按鈕連去寫作訂正③，**不要在這裡重複維護** |

**📚 題庫區（機經背誦）**

| 檔案 | 用途 |
|------|------|
| `index.html` | 入口頁，側欄分 訂正區／題庫區(W/L/R)／攻略筆記（含一份模板句副本，改模板要同步） |
| `WE_論點總表.html` | **主戰場**。37 題範文由檔內 JS `buildEssay()` + `DATA` slot 組出；含模板卡/默寫卡/錯題本 |
| `WE_中文翻譯.html` | 機經原始紀錄（37 題原文＋原始範文），**對照組，不要動** |
| `WE_交接檔.html` | 模板句舊副本，工程用非學習頁（改模板四檔同步：論點總表/中文翻譯模板卡/交接檔/index） |
| `WE_打字練習.html` | 模板盲打計時器（6 分鐘倒數、slot 自動跳過） |
| `SST_中文翻譯.html` | SST 原文＋中文翻譯 |
| `SST_擬答.html` | SST 背誦版擬答（James 定的格式：5 句一句一行、55-60 字、標開頭/論述/結尾、難字≤2 並括號註中文） |
| `SWT_中文翻譯.html` | SWT 179 篇中文翻譯 |
| `WFD_中文翻譯.html` / `wfd_memory_cards.html` | WFD 189 句翻譯／圖像記憶卡 |
| `WFD_填空測驗.html` | 精選 87 句挖空測驗（有「答案模式」開關；曾從 189 句精簡） |
| `WFD_保底字庫.html` | 防漏打技巧頁（跟訂正字庫性質不同，保留獨立） |
| `FIB-RW_拆解.html` | FIB-RW 532 題逐空格拆解（2.4MB，讀取要小心） |
| `FIB-RW_固定搭配速看表.html` / `FIB-RW_介系詞片語_精華版.html` | FIB 搭配／介系詞參考（1.2MB／326KB） |
| `HANDOFF.md` | WE 工程交接檔（工作法、資料結構、驗證流程） |
| `立場盤點_進度.md` | 37 題立場盤點紀錄（四條故事線決策的原始依據） |

**跳轉殼（不要編輯內容，只是保舊書籤）**：`大作文修正.html`→寫作訂正#review、`錯句重寫.html`→#rewrite、`文法自檢卡.html`→#check、`WFD_易錯單字庫.html`→WFD_訂正#vquiz。

## 關鍵決策與原因（程式碼看不出來）

1. **四條故事線取代逐題論點**（2026-06-11 定案）：James 說「逐題記配置完全記不起來」，改成 ①效率、③減壓、④視野、⑤財務 四條固定推論鏈套所有題。**②學業線已除役併入⑤**（讀書→好工作→穩定收入→溫暖的家）。
2. **36/37 題結尾都收「家庭和諧」**：James 的統一記憶錨點，唯一例外 #24 行銷題（主角是公司）。他練新題時常問「怎麼帶回家庭和諧」——這是預設要求。
3. **全面改用最基礎英文**（2026-07 sessions）：模板和論點以外的連接文字原本太難，James 明說「我就用最基礎字去應考」，已把 WE 範文黑色字體全部簡化。SST 擬答同理：他否決了照範文風格，「那太難了」。
4. **範文以 James 直覺版為準**：他練過的題目，範文常換成他自寫版本（比機經版好背）。DATA 已不是機經原版。
5. **字數 250 左右**（200-300 硬範圍），是 James 要求的精簡目標。

## 坑點

- **兩台電腦（Mac＋Windows）用 GitHub 同步**：開工先 pull、收工要 push，不然另一台會 diverge。Mac 路徑 `/Users/nn/Documents/claude/pte-study`，Windows 路徑 `C:/Users/james/OneDrive/文件/Claude-workspace/projects/PTE-Study-Hub`。
- git 一律 `git -C <repo路徑>`（Bash cwd 會跳走，曾差點 amend 錯 repo）；`git add -A` 前先看 status，別掃進無關檔案。
- **SSH 走 port 443**：James 的網路擋 port 22，`~/.ssh/config` 已設 github.com → ssh.github.com:443。push 失敗先想網路。
- 改 `WE_論點總表.html` 後必跑 HANDOFF.md §8 的 node vm 驗證（37 題解析＋buildEssay＋字數）；vm stub 要含 `querySelectorAll`/`setAttribute` 否則默寫卡 IIFE 報錯。
- 大檔（FIB-RW 2.4MB、SWT 800KB）不要整檔 Read，用 grep/python 抽段落。
- SST 翻譯曾有 11 篇因逾時漏翻——批次產出後要清點數量。

## James 的偏好（跟他互動的方式）

- **第一直覺工作法**：需要立場、例子、論述的內容，用問答問他取第一直覺再翻英文。AI 自行生成的論述他背不起來，會被退。
- **怕拼錯字**：所有產出英文用簡單好拼的字、固定片語優先。高級搭配只在他確認背得起來時保留。
- 他常用「對話互動考我」的方式背誦：一句句考他，打錯就「直接讓我再練一遍」（即時糾錯→立刻重打，不要長篇解說）。
- 他的固定罩門（批改時盯）：第三人稱 +s（頭號）、despite 拼錯、單複數/冠詞、漏 r（large/further）、-ing 沒去 e、字母顛倒。
- 說明的文法/拼字內容他會逐條驗證，標錯會被抓。不確定就說不確定。
- 訊息常有中文錯字（「勁量」=盡量、「執得」=值得、「梗」=更），照語意理解即可。
- 模板句他背熟了；他打錯模板句時「練默寫卡就好，不進錯題本」。

## 常用指令

```bash
# 部署 = push 到 main（GitHub Pages 自動發布）
git -C /Users/nn/Documents/claude/pte-study push

# commit 慣例：feat/fix(WE|WFD|SST|FIB):，結尾 Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
# 改 WE 後驗證：HANDOFF.md §8 的 node vm 腳本
```
