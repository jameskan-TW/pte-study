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

## 3. 四大論據（2026-08-21 v3 換血：以 James 12 題實戰句為底，取代六月版）

> **⚠ 2026-08-26 重編號**：舊 ①③④⑤ → 新 **①②③④**（①效率不變、③健康→②、④視野→③、⑤職涯→④）。因舊②學業線除役後編號跳號，James 要求改成連號。全站學習頁（總表、WFD_訂正）已同步；`立場盤點_進度.md`、`WE_中文翻譯.html` 是歷史紀錄保留舊編號。本檔 §4/§6 的歷史敘述亦保留當時編號。

| # | 論點句 | 推論鏈 | 終點 |
|---|--------|--------|------|
| ① 效率 | improve efficiency and boost productivity（James 實戰句；簡版 save time and work better） | save a lot of time → spend more quality time with their families → closer and happier | 家人 |
| ② 健康壓力(反面) | lead to stress and anxiety | feel frustrated and isolated → serious mental health problems → cannot take good care of their families（正面版讓步用：feel relaxed and enjoy peace of mind——peace of mind 只屬②） | 家人 |
| ③ 視野 | learn things they cannot find in books（因果起點，v2 的 broader view 降為第二步） | gain a broader view of life → get along with people from different backgrounds → earn trust and have better future prospects；家庭教育版（父母/品格題）：parents teach good values → honest → earn trust → future prospects | 信任前途（要收家庭借④尾） |
| ④ 職涯財務 | a good job and a steady income（進階 financial stability） | do not need to worry about money → a warm and stable home（兩步收尾；學生題開頭墊 outstanding academic performance） | 家人 |

- 舊②學業線已除役併入職涯線（學生題墊一步 outstanding academic performance）。
- 記憶法：①②④ 收家人；③ 收信任前途。讓步看對方強項：對方省時方便（①）／比較爽（②正面版）／長見識（③）／比較賺（④）；政策題對方沒強項→②反面版（承認我方給人壓力）。
- P4 萬用加分句：I believe that [X] brings more tangible and intangible benefits than drawbacks（地雷拼字 tangible/intangible 已入 WFD_訂正 #vquiz）。
- ② 地雷字 anxiety（曾拼 anxity）、frustrated（曾拼 frustarted）也已入默拼。
- **注意：37 題 DATA 範文與 ZH 速記仍是 v2 鏈的版本**，改版策略＝James 練到哪換到哪（分批），不要一次全改。

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
| ③-3 圖書館（原#3；2026-08-25 舊②學業卡刪除後主論 chip 改標視野線；2026-08-26 重編號後題號 ⑤-3→③-3） | ✔ | ✔ P2+P3 |
| ②-2 醫療長壽（原#8；08/06 首戰 21 錯、09/07 重寫 16 錯） | ✔ | ✔ P2 家庭版 + P3/P4 James 版（2026-09-07） |
| ②-3 平衡工作（原#11；09/07 首戰 15 錯） | ✔ | ✔ 全篇 James 修正版（2026-09-07；範文版曾短暫上線同日換掉） |
| ②-5 氣候面向（原#16；2026-09-08 James 決定「特別記這篇」：照機經範文段落，P2 成因鏈、P3 後果，無讓步；同日首戰 16 錯） | ✔ | ✔ 範文簡化版（老師 0908 改過） |
| ④-6 遲交扣分（原#9；0911 首戰 15 錯，走「公平」論點沒帶家庭；2026-09-12 補記進訂正頁＋mistakes） | ✔ | ✔ P2 車禍版（modal may） |
| ②-8 氣候誰負責（原#25；2026-09-08 與 #16 共用一套環境字：greenhouse gas／cars and factories／hotter summers and more floods／make laws／protect every family） | — | ✔ 共用字版 |

> 2026-09-08 老師看過 WE_訂正定稿 第 6–11 篇（Word 檔 WE_給老師_20260908.docx），改了 5 處已全部同步：②-2 小結補 would；②-3 小結改 put money first and ignore their family；②-4 resB 改 better future prospects；#16/#25 If-then 改 would、James 例子改具體公司事件（firm washed away／factory cut greenhouse gas after a new law）。

> 2026-09-10 老師看過 ③ 視野線三篇範文（Word 檔 WE_給老師_20260910.docx，只放三篇英文全文）。這三題**尚未實戰練習**，是先送範文審閱。改了 4 處已同步：③-1 resB 改 less pressure from money（James 提的，避開 less worry／fewer worries 之爭）、concl 改 never studied abroad、impl 加 and strong confidence（主詞變複數，helps→**help**）；③-2 resB 改 great efficiency and lower costs、impl 改 real talks build。③-3（#37）老師表示不用動。

> 2026-09-12 **第 3 類（沒練過）13 題逐 slot 走查**（James 要一題一題看，走不完隔天續）。已走：#1（conR → real life shows what schools cannot、concl → say they learned from life experience）、#4（stance → the good effects of design are much greater、does → sits in a bright and well-designed office all day）、#9（補記 0911 首戰訂正；P2 換 James 車禍版＋modal may）、#10（does 縮短）、#19（James 說不用換，reason「in a fair way」保留；備用公平句組：everyone follows the same rules → no one gets an unfair advantage）、#21（0912 第二輪 P2 整段重排：con some positive consequences／conR get news in seconds／cond read the news on their phones every day／resA learn what is happening around the world／resB a broader view of life／concl see the information revolution as a big step forward；final it→the information revolution）。#22（0913：does → keeps away from social media on school days、con us→young people）。**#27（0913：va should be taught／resA see how people lived in the past／does puts all his time into main subjects／result 共用 good job and steady income）。**接下來從 #28 起**：#28、#29、#30（先看沒問題）、#33（reason「has a top」→ has a limit）、#35。第 1/2 類的小修 James 未決：#14 vb 缺冠詞 a career、#8 modal have to／concl 去 would、#3 cond need 重複、#31 does family 重複。

> 2026-09-11 **模板風險盤點**（37 題逐篇看 slot 跟題目合不合）。已做：5 處文法小修（#36 topic／#26 va／#1 resA／#27 impl／#6 resB）；#10 失業題改照 #16 走法（P1 反方「失業太難解」、P2 問題嚴重性、P3 職訓解方＋James 朋友例）；#29 年齡限制從「開車 18」改「結婚 25」全套字共用 #14。**待處理清單已全部清掉（同日第二輪，7 處）**：🔴 #35 result 自打臉 `reduce stress, yet still feels the pressure` → `feel relaxed and spend more quality time with his family`，impl 改 `children today have to fight the pressure just to keep a happy family life`（仍收在「更難」立場＋家庭）；🟡 #26 topic → `the impact of the smartphone`；#31 rec → `governments create new jobs for both young people and the whole workforce`（補題目問的兩個對象，去掉語序卡住的 instead）；🟢 #30 stance → `country life is the better choice`（不再 I firmly believe that I prefer）、#17 impl → `laws keep every family safe`（避開與 James 句重複的 peace of mind）、#3 resA → `easily search online databases`（中文速記同步）、#21 impl → `turning off the noise keeps his family in harmony`（承接 James 關手機）。驗證：37 題解析正常、字數 255-291 全在 200-300。

> 2026-09-11（續）**#35 例子改中學生版**：James 說「題目強調孩子，但 slot 跟小孩無關」。模板句 `A pertinent case in point is James` 不能換人，所以把 James 設成中學生（jn 改 `high school`），主詞從頭到尾都是孩子：topic `whether growing up in the 21st century is harder`（一度改短版 `growing up in the 21st century`，James 決定回長版：37 題已有 8 題 whether 開頭，且長句照抄題目字面最穩——**注意 `the 21st century` 的 the 不能漏**）、cond `children study online`、does `faces endless tests and compares himself with his classmates online`、result `get good grades only by giving up his free time`（避開 able to 接負面：改「只能靠犧牲自由時間才做到」）、impl `children in the past never had this much pressure, and less family time hurts family harmony`、final 補 `than in the past`。中文速記同步。272 字。**模板約束備忘**：`he is able to ${result}` 只能接正面能力，負面證據要寫成「只能靠犧牲 X 才做到」或 `able to see how much…`。

> 2026-09-11（續2）**#35 P2/P3 換成與 #26 手機題共用字組**（James 提：「P2 就很方便取得資訊，P3 容易成癮變成讀不好書」）。兩題角色互換、字只背一套：#26 主論=資訊方便／讓步=成癮讀不好書，#35 反過來。#35 新 slot：p2c 3→1、p3c 2→4；con `children today can get information very easily`、conR `a phone puts information and lessons in one device`、resA `save a lot of time and find answers in seconds`、resB `a faster and easier way to learn`；reason `children get addicted to the internet very easily`、does `keeps surfing the internet on his phone every night`、result `focus on his books only after he locks his phone away`（again 用「只有…才…」繞過 able to 的正面約束）、impl `children in the past never had this problem, and poor grades hurt their future and worry the whole family`、rec 改 `use the internet wisely`。中文速記同步。**同日再修（James 兩點）**：① `a phone puts` 改複數 `phones put`——他說「用複數我才不會漏 s」，這招可推廣到所有第三人稱單數陷阱；② 他指出 #26 根本沒有「線上學習」，要求**全抄 #26 的 slot**。最終 #35（274 字）＝ #26 原句角色互換：讓步用 #26 主論字（`smartphones are a very useful tool for children`／`phones put information and lessons in one device`／`finish their homework faster and reach their teachers anytime`），主論用 #26 讓步字（`many young people get addicted to the internet`／`keeps surfing the internet on his phone`／`focus in class`／`poor academic performance`），rec 也抄 `build healthy digital habits`。原本卡在 result（`easily lose focus in class` 是負面，接不了 `he is able to`）——**James 決定特別記這題，改用 unable**：新增 slot 級覆寫 **`es.able`**（做法同 `es.modal`），buildEssay 改 `${T(', ' + (e.able || 'he is able to'))}`，只有 #35 設 `able:'he is unable to'`，其餘 36 題與模板卡藍字都不受影響；result 因此可直接走負面鏈 `focus in class or finish his homework on time`。impl 用 his 承接 James（`hurts his future and his family life`），避開 their 無指涉對象與 worries 的 +s。

> 2026-09-11（續3）**用 `es.able` 掃了一輪同類問題**，找到 #21 大眾媒體題犯一樣的毛病：立場「壞處更大」但例子是 James 晚上關手機→放鬆（示範解方而非壞處）。改成 does `keeps checking the news on his phone all evening`、`able:'he is unable to'`、result `relax at home or talk with his family`、impl 回到②反面鏈 `too much news makes people lose their temper and hurt family relationships`。266 字。同場 James 再改：va/vb/stance 的 `good points／bad points` 太弱 → 照抄題目原文的 **`positive consequences／negative consequences`**（題幹就是 positive and negative consequences）。**通則**：題目自己有給的關鍵名詞就照抄，不要降級成 good/bad points；其他沒有這種字眼的題（#18／#20／#27／#31）維持 good points／bad points 不動。再一改（James 提「P2 也用手機看新聞會不會比較搭」）：P2 讓步改成與 P3 同場景的正反對照——con `people can read the news on their phones anytime`、conR `a phone brings news from around the world in seconds`、cond `people check the news on their phones wisely`（聰明看）vs P3 `keeps checking the news on his phone all evening`（整晚一直看）。274 字。**這招可推廣**：讓步與主論用同一個場景、只換使用方式，背誦量剩一半。掃描結論：其餘負面立場題（#23 電視、#31 工時、#27 古劇）的正面例子邏輯站得住（「做了 X 才有好結果」＝反證），不用改。#12／#4 是描述題硬套辯論框，內容有答到，James 未要求改——維持原狀。

前四篇都是主論①（圖書館現歸③視野組）。**下一步建議**：換主論②/③/④ 的題目練，讓四條鏈都熟。或 James 想針對拼字罩門做默寫訓練。

## 7. 已教過的兩個策略工具

1. **讓牌口訣**：選論據前列兩欄牌——兩邊都能講的論據送給 P2 讓步，只有我方能講的留給 P3 主論。例：修路 vs 大眾運輸都搶「效率」→ 效率送讓步，主論用大眾運輸獨有的②健康
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
- `es.able`（2026-09-11 新增）可覆寫 P3 的 `he is able to`：目前 **#35 與 #21** 設 `able:'he is unable to'`（立場是「壞處大於好處」的題，例子若用 able to 會被迫寫成正面的「解方」，反而削弱立場）；模板卡藍字不受影響。否定句一律用 `unable to A **or** B`（不是 and）
- `es.modal`（2026-09-08 新增）可覆寫 If/then 句的 `can`：#16／#25 環境題設 `modal:'would'`（老師要求假設語氣），其他題不設維持 can；模板卡藍字不受影響
- 序列化 DATA 用單引號跳脫、保持欄位順序、entry 間空一行
- 改完 commit 訊息照本 repo 慣例（feat/fix(WE):），結尾 `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`
