# 交接檔：WE 論點總表個人化工程（給新 session 的 Claude）

> 給 James 的新 session 使用。先整份讀完再開始工作。
> 日期：2026-06-11。上一個 session 已完成大量改版，本檔案記錄現狀與下一步。

## James 是誰、怎麼跟他工作

- 正在準備 PTE，弱項是 Writing（WE = Write Essay）
- **怕拼錯字**：所有產出的英文用「簡單好拼」的字；固定片語優先（quality time、peace of mind、get along with、lose their temper）；高級搭配只在他確認背得起來時用
- **第一直覺工作法（最重要）**：凡是需要想像、選立場、舉例的內容，一律用問答方式問他，取他的第一直覺，再翻成英文。不要 AI 自行生成論述塞給他——AI 生成的他背不起來
- 回應用繁體中文、簡潔直接
- git identity 已設好（james / james.kan.tw@gmail.com）。跑 git 一律用 `git -C /Users/nn/Documents/claude/pte-study`（工作目錄可能跳回別的 repo，上次因此差點 amend 錯 repo）

## Repo 與檔案

- repo：`/Users/nn/Documents/claude/pte-study`（github.com/jameskan-TW/pte-study，SSH）
- 部署：GitHub Pages → jameskan-tw.github.io/pte-study（push 後約 1-2 分鐘生效）
- **主戰場：`WE_論點總表.html`**——37 題範文由檔內 JS 模板 `buildEssay()` + 每題 slot（`DATA` 陣列）組出。模板句改一處影響 37 題；slot 改了只影響該題
- `WE_中文翻譯.html`：機經原始紀錄（37 題原文＋原始範文），**當對照組，不要動**
- `WE_交接檔.html`、`index.html`：含同一套模板句的舊副本，模板句改動要四檔同步
- 改完 DATA 後驗證方式：用 node vm 載入 `<script>` 內容（stub 掉 document），確認 37 題解析正常、`buildEssay()` 組裝正常、字數 200-300

## 已完成的工程（全部已 commit + push 到 main）

1. **模板句修正**（四檔同步）：`captured public attention`／`I firmly believe that`／`counterargument`
2. **五大論據個人化**：推論鏈全部改成 James 自己想的版本（見下節）
3. **37 題依主論分五組重排**，組內編號 `①-1` 格式，保留 `原#N` 對照
4. **37 題範文 P2/P3 推論鏈全面改寫**成個人化五條鏈
5. **顏色統一**：論據卡、背誦清單與範文同用 a1-a5 彩色高亮
6. **頁面新增**：完整模板卡（P1-P4 + 虛線 slot）、Slot 填法注意框、關鍵字背誦清單、兩個終點記憶法
7. **題目文字同步機經原文**（29 題曾被精簡，已改回一字不動）
8. **個別修正**：⑤-1 最緊迫問題改答「失業」（原機經答早婚太牽強）；③-7 年齡限制明確選「開車、18 歲」

## 五大論據（James 的個人化推論鏈，已定稿）

| # | 論點句 | 推論鏈 |
|---|--------|--------|
| ① 效率 | save time and work better（進階 improve efficiency and boost productivity） | finish work faster → spend more quality time with their families → closer and happier |
| ② 學業 | achieve outstanding academic performance | good habits such as self-discipline → keep learning and growing → leads to a better future |
| ③ 壓力(反面) | lead to stress and anxiety | feel upset and angry → lose their temper over small things → speak rudely to their families / hurts family relationships。正面版：feel relaxed and enjoy peace of mind |
| ④ 視野 | gain a broader view of life | learn things they cannot find in books → more interesting and confident when they talk → get along with people from different backgrounds |
| ⑤ 財務 | a good job and a steady income（進階 financial stability） | do not need to worry about money → enjoy peace of mind → a warm and stable home for the whole family |

記憶法：①③⑤ 終點＝家人；②④ 終點＝個人成長。

## 已教過 James 的兩個工具

1. **口訣**：選論據前列兩欄牌——兩邊都能講的論據送給 P2 讓步（讓步本來就要誇對方），只有我方能講的留給 P3 主論。例：修路 vs 大眾運輸，兩邊都搶「效率」→ 效率送讓步，主論用大眾運輸獨有的「健康③」
2. **人設**（注意：這是「範文的人設」，反推自 37 題立場，**不是 James 本人**）：顧家務實上班族——挺制度、挺文化、挺減壓、科技為了省時陪家人、先立業後成家

## ⚠️ 進行中的任務（新 session 從這裡接手）

**背景**：測驗時發現 James 的真實直覺常跟範文立場相反（他支持小商店、覺得讀書工作難兼顧、覺得名人該接受隱私代價）。診斷：37 題的「立場」還是機經選的，只有「推論鏈」被個人化了。James 決定全部重走。

**任務：37 題立場盤點（從原#1 重新開始，目前 0/37）**

流程：
1. 按**原編號順序**（原#1→#37）一題一題出題：貼題目英文原文＋中文翻譯，問「立場？讓步？主論？」
2. James 的**立場沒有對錯**——只記錄他的答案 vs 範文現有配置，不一致就標記
3. **配法邏輯**（讓步/主論的牌怎麼分）可以給一句提示，用口訣教，保持簡短
4. 每題記錄進度（建議寫進暫存檔，防 context 壓縮丟失）
5. 37 題走完後，逐題處理立場不一致的題目：
   - **預設：改範文配合 James 的立場**（用第一直覺工作法問出他的推論，再改 DATA slot）
   - **例外：James 的立場明顯難寫時**（如名人隱私「同意放棄」結論會很偏激），說明理由讓他自己決定要不要妥協
6. 改範文時維持：模板不動、slot 文法規則（topic 名詞片語／able to 接原形／crucial that 虛擬語氣）、五大論據高亮 `<i class="a1~5">`、簡單好拼用字

**上次測驗的觀察**（重開後僅供參考，不要當成績）：他配論據的能力不錯（古蹟④、筆試③→②都自己配對），弱點在「兩邊搶同一論據時不會讓牌」；立場不一致的題目目前已知：原#32 名人隱私（他：同意放棄）、原#6 商場（他：挺小商店）、原#2 兼顧（他：認為難兼顧）——重走時以新答案為準。

## 提取 DATA 的範本程式

```js
const html = require('fs').readFileSync('WE_論點總表.html','utf8');
const m = html.match(/<script>([\s\S]*)<\/script>/);
const vm = require('vm');
const stub = { appendChild(){}, addEventListener(){}, innerHTML:'', style:{}, classList:{add(){},toggle(){}} };
const ctx = { document: { getElementById: ()=>({...stub}), createElement: ()=>({...stub}) }, console };
vm.createContext(ctx); vm.runInContext(m[1], ctx);
const DATA = vm.runInContext('DATA', ctx); // 37 筆，含 n/o/t/en/stance/p2c/p3c/es
```

改寫 DATA 時用同款序列化（單引號跳脫、保持欄位順序、entry 間空一行），改完跑驗證再 commit。
