---
name: practice-rules-overview
description: PTE 互動練習規則總覽（WE 逐 slot 練法／WE 文法總複習 18 類考法／拼字・SST 關鍵字 5 題一批／FIB 四選一）＋ 2026-10-24 各項接續點。換電腦先讀這份。
metadata:
  type: project
  modified: 2026-10-24
---

# PTE 互動練習規則總覽（2026-10-24 整理，給任何一台電腦的 Claude 開考用）

James 說「對話互動考我」時，照這份做。細節出處：`HANDOFF.md` §5、`CLAUDE.md`「James 的偏好」、本資料夾其他檔。

## 0. 所有練習共通

- **批改格式**：✅／❌ 一行一題；錯的只給改寫路徑（拆音節或逐字母），**不長篇解說，叫他當場重打**，重打對了才下一題。
- **他的罩門要盯**：第三人稱 +s（頭號）、despite 拼錯、單複數／冠詞、漏 r（large／further）、-ing 沒去 e、字母顛倒。
- **訊息錯位防呆**：桌面 app 他的訊息會延遲／重複送達。收到跟上一則一模一樣的答案＝重複，不判分，回「第 N 題（格）還在等」。絕不自問自答。
- 他訊息常有中文錯字（勁量＝盡量、執得＝值得、梗＝更），照語意理解。
- 他打錯**模板句**時：「練默寫卡就好，不進錯題本」。
- 文法／拼字說明他會逐條驗證，不確定就說不確定。

## 1. WE 逐 slot 練法（2026-10-10 定案，「以後都按這個流程」）

題庫＝`WE_論點總表.html` 的 `DATA`（37 題，每題 18 格）。18 格名稱（**用「P幾＋中文名＋編號」稱呼，不要講 conR／does 這種代號**）：

| 段 | 格 |
|---|---|
| P1 | ① 主題 topic／② 反方說 va／③ 我方說 vb |
| P2 讓步 | ④ 承認 con／⑤ 對方的理由 conR／⑥ 如果 cond／⑦ 主詞 subj／⑧ 就能 resA／⑨ 進而 resB／⑩ 難怪 concl |
| P3 主論 | ⑪ 我的主張 stance／⑫ 因為 reason／⑬ James 身分 jv／⑭ James 做了 does／⑮ 所以他能 result／⑯ 換句話說 impl |
| P4 | ⑰ 結論立場 final／⑱ 建議 rec |

動詞形態：⑧ 原形／⑭ +s／⑮ 原形／⑱ 原形。對照頁：`WE_格位速查.html`。

**流程**
1. 開考先貼**完整題目**（DATA 的 `en` 全段）＋立場＋走哪條線（①效率 ②健康減壓 ③視野 ④職涯財務），先帶他過一遍 18 格邏輯線。
2. **一格一格考，一則訊息只出一格並標格號**（這是「5 題一批」的例外，James 明確要求一格一格）。
3. 打錯 → 即時糾錯、立刻重打，不解說。
4. 他質疑某格邏輯、或打出更好的版本 → **換進 DATA**（他的直覺版比範文好背），`ZH` 同步。
5. 練完把當次釐清的**通則**寫進該題 `mistakes.rules`（`[{k,v}]`），逐條拼字／文法不留；拼字罩門另加 `WFD_訂正.html` 的 `VQ` 與 `寫作訂正.html` 的 `BLACKLIST`。
6. 當日紀錄寫進 `tools/menu_oct/gen.py` 的 `LOG`（他點名要記的加 `class="key"` ⭐），重跑 gen.py。
7. 跑 HANDOFF §8 的 node vm 驗證 → commit → push。
8. 結尾一律帶回「家庭和諧」（唯一例外 #24 行銷題）；字數 250 左右；只用最基礎字。

**接續點（2026-10-24）**：W1 收尾 11 題 10/21 全清；有 `rules` 的「已扎實練」9 題：#7 #10 #15 #17 #25 #32 #33 #34 #35。
接下來是十月計畫 **W2：重打錯最多的 14 題，順序 #12 #5 #21 #30 #1 #3 #28 #4 #13 #8 #29 #37 #24 #27**，下一題 **#12**。一天兩題。
W3 起改整篇計時 1 篇／天貼來批改（題目寫死在菜單 D15 起）。
盯梢：take the metro／by metro 冠詞相反、and…keeps、earlier、the ride（見 `we-slot-drill-watchlist.md`）。

## 2. WE 文法總複習（錯誤總回顧）考法

頁面 `WE_文法總複習.html`：37 題 mistakes 跨篇歸 **18 類**，每類有一句話規則＋James 錯句→對句。

**考法**：照類別順序，**每類 5 句一批**；出「他當時的錯句」要他改正，或挖空要他填；5 句一次出、他一次答、一次批改；錯的當場重打。開場**不重講規則**，直接出句子。每批結束歸一句話規則。

18 類順序：
1 s 的方向（第三人稱 +s／複數不加 s）、2 詞性穿錯衣服、3 介系詞固定片語、4 可數泛指漏 s、
**5 可數單數 a／an 不能掉**、6 the 兩方向、7 助動詞／to／crucial that 後原形、8 不可數名詞、
9 固定片語不減字不換字、10 動詞當主詞 -ing、11 and／or、12 leading to／before／for 接名詞、
13 比較級、14 逗號連兩句、15 make／let／help／see＋受詞＋原形、16 時態、17 every／each／there、18 改一個掉一個。

**接續點（2026-10-24 更新）**：10/24 已複考 10/21 錯句並考完第 5–6 批、10/27 考完第 7–14 批，**下次從第 15 批「make／let＋原形」接**，開場先複考 10/24 錯的（見 `we-grammar-review-progress.md`）。以下為 10/21 時的紀錄：10/21 考完第 1–4 批。**下次開場先複考 10/21 錯的**：teach→teaches、pay（不可數，不是 more pays）、pay attention **to**、**in** a better mood、exams、are **worried**、body and **mind**、have little effect **on**。然後從 **第 5 批「a 不能掉」** 開始（earn **a** steady income／with **a** steady income／get **a** promotion and **a** higher income／**a** maximum wage limit／**a** happy employee goes home），接 6 → 18。
詳見 `we-grammar-review-progress.md`。

## 3. 拼字默拼（WFD_訂正 VQ）與 SST 關鍵字

- **5 題一批**：一次給 5 個中文／提示，他一次打 5 個，一次批改；錯的拆音節重打。
- VQ 分兩池：反覆卡 34 張、非反覆池。接續點見 `spelling-drill-progress.md`（下次只考 10/19 錯的 32 字＋反覆卡）。
- SST 關鍵字 95 字清單在 `SST_關鍵字默拼_進度.md`，每天 3–5 個；接續點見 `sst-keyword-drill.md`。

## 4. FIB（閱讀訂正 93 格）

- 四選一，**干擾項放他當時選錯的字**，5 格一批；答錯重考＋換句突襲；每批歸一條規則寫進 gen.py `LOG`／錯格寫進 `WRONG`，重跑 `pack.py`、`quiz.py`。
- 他也可以自己開 `FIB_文法測驗.html` 做；接續點見 `reading-review-progress.md`、`october-plan.md`。

## 5. 每天怎麼開工

James 說「今天 D 幾」→ 開 `讀書菜單_10月.html` 當日欄（D1＝10/5，D28＝11/1）照單執行；說「考 slot」→ §1；說「考文法總複習」→ §2；說「考拼字／SST 單字」→ §3；說「考 FIB」→ §4。
