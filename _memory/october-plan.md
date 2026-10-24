---
name: october-plan
description: 2026-10-05 起的 28 天讀書菜單（讀書菜單_10月.html）：WE 兩題 slot／FIB 93 錯格清帳／W3 整篇計時；下次考試約 11 月初未定
metadata:
  node_type: memory
  type: project
  originSessionId: 65709005-f591-4cd5-ab45-5afc80b85324
  modified: 2026-10-21T15:28:24.308Z
---

2026-10-05 James 定的十月計畫，頁面在 repo `讀書菜單_10月.html`（D1=10/5 … D28=11/1，考試日未定、「大約一個月後」，定了要把 D28 對齊考前一天）。每天約 2.5 小時。

- **WE：一天兩題 slot**（James 要求兩題，他說逐 slot 同時在練文法結構）。W1 收尾 11 題沒練過的：#7 #17 #18 #20 #32 #25 #35 #33 #15 #34 #10——**2026-10-21 全部清完**（總表 37 題全有 mistakes，有 rules 的「已扎實練」9 題）。每題練前先過一遍 18 格邏輯線、James 貼機經範文時借論點補強（#17 #32 做過），他點名的句子／字寫進 rules。接下來照 W2：重打錯最多的 14 題。W2 重打錯最多的 14 題：#12 #5 #21 #30 #1 #3 #28 #4 #13 #8 #29 #37 #24 #27。W3 起改整篇計時 1 篇／天貼我批改。
- **FIB 清帳（James 要求 1–2 週把過去 FIB 錯誤全訂正、同類型不再錯）**：閱讀訂正.html 共 47 篇 93 錯格；sem 37／col 32／log 8 共 77 格沒考過，pos 12／ten 4 其中 9 格 8/13 考過。W1 分 7 批照訂正頁篇序考（5 格一批四選一、干擾項放他當時選錯的字），每批歸一條規則；W2 二輪考錯格＋用 FIB-RW_拆解 冷題驗證每條規則，規則固化成新頁 `閱讀搭配練習.html`（比照 閱讀文法練習.html，**尚未建**）。
- 保溫：WFD／SWT／SST／口說各 5–10 分，Skills Profile 顯示這些已滿格。
- **菜單是逐日明細版（2026-10-05 James 要「打開直接上工」）**：**產生器在 repo `tools/menu_oct/gen.py`＋`template.html`**，改完跑 `PYTHONIOENCODING=utf-8 python tools/menu_oct/gen.py` 重產 `讀書菜單_10月.html`（不要手改 HTML）。2026-10-06 James 要求「每天練文法都要留紀錄、可快速複習」→ 每天 FIB 綠框下有「📇 小字卡」——**2026-10-07 James 改成只留當天複習還錯的格，不要整批**：考完把錯格寫進 gen.py 的 `WRONG = {天: [(閱讀訂正篇序, 空格序), …]}`，WFD 錯字／新規則寫進 `LOG = {天: [HTML…]}`（黃框「📝 當日紀錄」），再重產。每天寫死：口說題型四天一輪、WFD 訂正 5 句（115 句 D1–D23 照序，D24–28 重做多輪句）、默拼 10 字（176 字照序，第二輪先反覆卡／WE罩門；頁內輸入 Enter 判分）、SWT 2 題（#1、#4、#7… stride 3）、SST 1 篇（a1、a3… 隔篇）、FIB 當日篇名。直達連結：`閱讀訂正.html#p{篇序}`、`WFD_訂正.html#w{句序}`、`SWT_練習.html#{num}`、`SST_擬答.html#a{n}`、菜單本身 `#d{天}`。W3 整篇題目也寫死：D15 #12、D16 #5、D17 #21、D18 #30、D19 #1、D20 冷題、D21 驗收 #28、D22 #4、D24 #13、D26 #8。

**Why:** 0929 成績 W64（目標 75）、Skills Profile 最矮是 Extended Writing 與 Multiple-skills Comprehension，所以 WE 整篇與 FIB-RW 是主菜。

**How to apply:** James 開新 session 說「今天 D 幾」或「考 FIB」時，照菜單當日欄執行；FIB 出題遵守 [[interactive-drill-batching]] 5 題一批。相關：[[pte-exam-scores]]、[[reading-review-progress]]。
