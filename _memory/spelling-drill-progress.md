---
name: spelling-drill-progress
description: 拼字默拼練習的進度與接續點（WFD_訂正.html VQ 192 字，分反覆卡／非反覆兩池）
metadata:
  node_type: memory
  type: project
  originSessionId: 9a9e958b-a620-401b-a5a5-1b2b8be8754b
  modified: 2026-10-19T03:22:54.321Z
---

拼字練習的字庫是 `WFD_訂正.html` 的 `VQ` 陣列（**192 筆**，2026-10-19 時；檔頭寫的 57 字是舊數字。python 正則會漏掉 src 用雙引號的行，筆數要用 node eval 才準）。分兩池練：
- **反覆卡**（tag 含 🔴／反覆卡，或 trap 寫「考前必掃」）——2026-10-19 共 34 張
- **其餘非反覆池**——158 字

**進度**：
- 2026-09-15：反覆卡 30 張全掃（錯 14）；非反覆池考到第 37 字。
- 2026-09-16／17（Mac）：非反覆池考到第 69 字 proportion。
- **2026-10-19（Windows）：非反覆池第 70–158 字全掃完，89 字錯 32，全部當場重打過**。非反覆池已完整過一輪。

**下次接續點**：兩池都掃過一輪了。建議下次只考「trap 裡有 1019 錯法」的 32 字＋反覆卡 34 張；trap 標「1019 默拼一次過 ✅」的 57 字考前可跳過。

**1019 升級成反覆卡**：criticised（第 5 次，critic 的 i 變 e）、analyze（第 3 次 y 位置）、articles（第 3 種字尾錯法，定型 c-l-e-s）。

**1019 錯型分析**（不是拼字錯，是詞性／詞形）：
- 詞性錯 7 次：effect→effective、chemical→chemically、various→variety、anxious→anxiety、authority→authoritative、efficiency→efficient、definite→definitive。批改時先看空格前後要什麼詞性。
- be／have 後漏 -ed 繼續犯：transcend（have ____）；第三人稱 +s：provide→provides；反向多 s：appear 答 seems。
- 字義掛不牢、答成同義字：passion（enthusiasm）、electronics（appliances）、stress（frustrated）、seems（appear）、price（prize 第 2 次）。
- 0821 SST 那組（eighth／efficient／enthusiasm）三個全部二度重犯。

**他的固定漏法（批改時盯）**：空格前有 be 動詞（is／are／have been）就漏詞形（concern→concerned、tutorial→tutorials、implement→implemented、transcend→transcended）。口訣：「be 動詞後面不接原形，只接 -ing 或 -ed」。另一組是 -tion 字尾顛倒（foundatoin、preparatoin）。

**available 的發音問題**（1019 他問 i 有沒有發音）：/əˈveɪləbəl/，vail 唸同 veil／mail，ai 合發長音 ei，i 不單獨唸。

記錄慣例：練完把錯法追加到該字 trap 欄位結尾（格式 `；MMDD 拼 xxx——原因`），一次過的標 `；MMDD 默拼一次過 ✅`，次數寫在 tag（如 `🔴反覆卡·5次`）。追加用 python 逐行對 `',src:` 做 replace（**src 有單引號也有雙引號兩種**，regex 要兩種都接），寫完用 node eval 驗證筆數與欄位完整。相關：[[pte-sync-setup]]、[[interactive-drill-batching]]
