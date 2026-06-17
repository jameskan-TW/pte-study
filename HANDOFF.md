# 交接檔：WE 論點總表個人化工程（給新 session 的 Claude）

> 給 James 的新 session 使用。先整份讀完再開始工作。
> 最後更新：2026-06-11（夜）。本檔是單一事實來源，現狀與下一步都在這。

---

## 1. James 是誰、怎麼跟他工作

- 正在準備 PTE，弱項是 Writing（WE = Write Essay）
- **怕拼錯字**：所有產出的英文用「簡單好拼」的字；固定片語優先（quality time、peace of mind、get along with、lose their temper）；高級搭配只在他確認背得起來時保留
- **第一直覺工作法（最重要）**：凡是需要想像、選立場、舉例的內容，一律用問答方式問他，取他的第一直覺，再翻成英文。不要 AI 自行生成論述塞給他——AI 生成的他背不起來
- 回應用繁體中文、簡潔直接、能用清單就別長篇
- **他會仔細檢查**：列出的文法/拼字說明要正確，他會抓錯（例如他抓出「lage 是漏 r 不是漏 a」「no time spend 是 to+原形不是過去分詞」——都是我先標錯被他糾正）。不確定就說不確定

## 2. Repo 與檔案

- repo：`/Users/nn/Documents/claude/pte-study`（github.com/jameskan-TW/pte-study）
- 部署：GitHub Pages → jameskan-tw.github.io/pte-study（push 後約 1-2 分鐘生效）
- **主戰場：`WE_論點總表.html`**——37 題範文由檔內 JS 模板 `buildEssay()` + 每題 slot（`DATA` 陣列）組出。模板句改一處影響 37 題；slot 改了只影響該題
- `WE_中文翻譯.html`：機經原始紀錄（37 題原文＋原始範文），**當對照組，不要動**
- `WE_交接檔.html`、`index.html`：含同一套模板句的舊副本，模板句改動要四檔同步

### git / 連線注意
- git identity 已設好（james / james.kan.tw@gmail.com）
- 跑 git **一律用 `git -C /Users/nn/Documents/claude/pte-study`**（Bash 工作目錄可能跳回 openfun repo，曾因此差點 amend 錯 repo）
- **`git add -A` 前先看 `git status`**：repo 內可能有別的未提交檔案（例如 SST 翻譯），別把無關檔案掃進 WE 的 commit
- **SSH 走 port 443**：James 的網路擋 port 22，已在 `~/.ssh/config` 設 github.com → ssh.github.com:443。push 失敗先確認是不是網路

## 3. 五大論據（James 個人化推論鏈，已定稿）

| # | 論點句 | 推論鏈 | 終點 |
|---|--------|--------|------|
| ① 效率 | save time and work better（進階 improve efficiency and boost productivity） | finish work faster → spend more quality time with their families → closer and happier | 家人 |
| ② 學業 | achieve outstanding academic performance | good habits such as self-discipline → keep learning and growing → a better future | 個人成長 |
| ③ 壓力(反面) | lead to stress and anxiety | feel upset and angry → lose their temper → hurts family relationships（正面版：feel relaxed and enjoy peace of mind） | 家人 |
| ④ 視野 | gain a broader view of life | learn things they cannot find in books → more interesting and confident when they talk → get along with people from different backgrounds | 個人成長 |
| ⑤ 財務 | a good job and a steady income（進階 financial stability） | do not need to worry about money → enjoy peace of mind → a warm and stable home | 家人 |

記憶法：①③⑤ 終點＝家人；②④ 終點＝個人成長。

## 4. 已完成的工程（全部已 commit + push）

1. 模板句修正（四檔同步）：`captured public attention`／`I firmly believe that`／`counterargument`
2. 五大論據個人化、37 題依主論分五組重排（編號 `①-1`，保留 `原#N`）
3. **37 題立場盤點完成**（在另一個 session 做的，commit `5d9c917`/`a35b3ef`）：37 題已改版成「四條故事線」，立場已審過。**注意：現在 DATA 是這個盤點後的版本，不是最初機經版**
4. 顏色統一（a1-a5 高亮套到論據卡、背誦清單、範文）
5. 題目文字同步機經原文（一字不動，含原文的回憶錯誤）
6. **頁面結構（由上到下＝學習動線）**：
   - 顏色說明
   - 📝 完整模板卡（P1-P4 藍字 + 虛線 slot）
   - ✍️ **模板默寫卡**（藍字遮住可點開、首字母提示、全遮/全開按鈕；內容由完整模板卡 JS 自動複製，永遠同步）
   - ⚠️ Slot 填法注意框（topic 名詞片語／able to 接原形／crucial that 虛擬語氣）
   - 📚 五大論據英文句卡 + 💡 兩個終點記憶法
   - 🔤 關鍵字背誦清單
   - 🗺️ 37 題分類一覽
   - 五組分類範文

## 5. 練習＋錯題本機制（本 session 新增，正在進行）

### 流程（每次 James 貼一篇作文）
1. **只改他自己論點的拼字/文法**，模板句的漏字另外列「練默寫卡就好，不進錯題本」
2. 給三段式回饋：① 拼字表 ② 文法表（❌→✅＋中文說明）③ 修正後完整版
3. 把錯誤寫進該題 DATA 的 `mistakes` 欄（見下），commit push
4. 之後問他要不要把該題範文換成他的直覺版（他常說要——他的直覺通常比機經更貼題）

### `mistakes` 資料結構（加在 entry 的 `es:{...}` 後面、entry 結尾 `}}` 前）
```js
 mistakes:{
  spell:[ {x:'錯字', o:'正字', nt:'可選提示'}, ... ],
  grammar:[ {x:'錯', o:'對', nt:'說明'}, ... ],
  note:'日期＋一句總評'
 }},
```
有 `mistakes` 的題目會自動：① 範文下方顯示紅框「📌 我的錯誤複習區」② 標題列＋一覽表題號前顯示 📌 記號。`renderMistakes()` 與 render 迴圈已寫好，只要加資料。

### James 的固定罩門（四篇歸納，要持續盯）
- **第三人稱 +s**：每篇都犯（spends/shops/studies）← 頭號問題
- **despite**：連兩篇拼成 dispect
- **單複數 / 冠詞**：employee→employees、the government、policies
- **anywhere / anytime**：兩篇混用
- **拼字三模式**：①漏子音前的 r（large/further，中文母語聽不出 r）②-ing 沒去 e（using/evolving）③字母顛倒（people 拼成 poeple）

## 6. 進度（練習 4/37，都有 📌）

| 題 | 練過 | 已改成 James 版本 |
|----|------|------|
| ①-1 大商場（原#6） | ✔ | — |
| ①-3 手機（原#26） | ✔ | ✔ P2 |
| ①-4 工時（原#36） | ✔ | ✔ P2+P3 |
| ②-x 圖書館（原#3，主論已從⑤改②） | ✔ | ✔ P2+P3 |

前四篇都是主論①/②。**下一步建議**：換主論③/④/⑤ 的題目練，讓五條鏈都熟。或 James 想針對拼字罩門做默寫訓練。

## 7. 已教過的兩個策略工具

1. **讓牌口訣**：選論據前列兩欄牌——兩邊都能講的論據送給 P2 讓步，只有我方能講的留給 P3 主論。例：修路 vs 大眾運輸都搶「效率」→ 效率送讓步，主論用大眾運輸獨有的③健康
2. **人設**（注意是「範文人設」反推自立場，不等於 James 本人）：顧家務實上班族。但實務上 James 的真實立場常跟它不同，**以 James 當下直覺為準**

## 8. 技術範本

### 提取 DATA
```js
const html = require('fs').readFileSync('WE_論點總表.html','utf8');
const m = html.match(/<script>([\s\S]*)<\/script>/);
const vm = require('vm');
const stub = { appendChild(){}, addEventListener(){}, innerHTML:'', style:{}, classList:{add(){},toggle(){}}, querySelectorAll:()=>[], setAttribute(){} };
const ctx = { document: { getElementById: ()=>({...stub}), createElement: ()=>({...stub}), querySelectorAll:()=>[] }, console };
vm.createContext(ctx); vm.runInContext(m[1], ctx);
const DATA = vm.runInContext('DATA', ctx);           // 37 筆
const buildEssay = vm.runInContext('buildEssay', ctx); // 組範文
```
（stub 一定要含 `querySelectorAll` 和 `setAttribute`，否則默寫卡的 IIFE 會報錯）

### 改完一定驗證
- 37 題解析正常、`buildEssay()` 組裝正常、字數 ~250（範圍 200-300）
- slot 文法：`then ${subj} can ${resA}` → resA 要原形動詞開頭；`It is crucial that ${rec}` → 原形（虛擬語氣）
- 序列化 DATA 用單引號跳脫、保持欄位順序、entry 間空一行
- 改完 commit 訊息照本 repo 慣例（feat/fix(WE):），結尾 `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`
