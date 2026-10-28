# WE 三分鐘卡：逐題註解規格

每題一張 A4 卡，James 只看 3 分鐘：先看思路，再掃 18 格的紅字，最後念「最該盯的三個」。
卡片由 `build.js` 從兩份資料組出來：

- `data.json`：`extract.js` 從 `WE_論點總表.html` 抽的 37 題（`es`＝18 格英文、`zh`＝中文論點 p1–p4、`stance`、`mistakes`）。**不要改**。
- `ann/{題號}.json`：人工註解，本規格說明怎麼寫。範本：`ann/17.json`（已定稿，照它的口吻和長度）。

## 欄位

```jsonc
{
 "o": 17,                      // 總表序號（data.json 的 o）
 "chain": {                    // 思路：中文，短，用 → 串推論；結尾帶回家庭和諧（#24 例外）
  "stance": "一句立場",
  "p1": "反方：… ｜ 我方：…",
  "p2": "A → B → C → 小結",      // 讓步段的推論鏈
  "p3": "A → B → James 例子 → 結果 → **含義**",   // ** ** 會變粗體，只用在最後的家庭和諧那句
  "p4": "結論 ｜ 建議：…"
 },
 "slots": {                    // 只寫有提醒的格；key 用 data.json 的 es 欄位名
  "conR": {
   "hl": ["follow", "the law"],  // 要標紅的字：必須是該格英文（去 HTML 標籤後）的逐字子字串，大小寫一致
   "w": "提醒：中文短句，≤45 字，可用 **錯誤寫法** ✗ 標他寫錯的樣子",
   "src": ["r9", "r0"]           // 這條提醒根據哪幾筆錯題：s=spell、g=grammar、r=rules，從 0 起算
  }
 },
 "ok": ["topic"],              // 「一次過」的格：只有 mistakes.note 明寫哪些格一次過才填，不確定就留空陣列
 "top3": [                     // 這題最該盯的 2–3 個（錯最多次、跨多格、或 note 點名的罩門）
  {"t": "短標題", "b": "一句說明，用 ⑤⑧ 這種圈號指到格", "src": ["r0"]}
 ],
 "spell": [["正確字", "他拼錯的樣子", "..."]],   // 這題拼錯過的字；只有正確字也可以 ["strict"]
 "spellSrc": ["s0", "s3"],     // spell 用到的錯題 id
 "skipped": ["g4：模板句的錯，練默寫卡就好", "s2：範文已改寫，這個字不在 18 格裡"]  // 沒用到的錯題要列在這裡並說原因
}
```

## 規則（一定要遵守）

1. **只寫 mistakes 裡真的有的錯**。不要自己發明他「可能會錯」的地方。唯一例外：可以在已有提醒的格順手加一句他的通用罩門（第三人稱 +s、a／s、原形），但要短，src 留空。
2. **每一筆錯題（s/g/r）都要被用到**（slots 的 src、top3 的 src、spellSrc）或列在 `skipped` 並說原因。`validate.js` 會檢查。
3. **錯題對不到現在的格**：很多舊題的範文後來換成 James 直覺版，錯題的 `o`（正確寫法）可能已不在任何格裡。
   - 如果同一個字或同一個文法點還在某格裡（例如錯過 every families，現在格裡有 every family）→ 標那格。
   - 如果完全不在了 → 拼字錯可以放進 `spell`（他還是會拼錯）；文法錯列進 `skipped`，寫「範文已改寫」。
   - 錯在模板句（It is generally true that…、A pertinent case in point…、despite the fact that… 這種固定句）→ `skipped`，寫「模板句」。但 despite 拼錯要放進 `spell`。
4. **hl 只標錯過的那幾個字**，不要整句標紅。片語最多 4–5 個字。
5. **提醒用中文、最基礎的說法**，像 `ann/17.json`。不准出現格位代號（conR、resA、impl…），要指格就用 ①–⑱ 圈號。
6. **格的對應**：① topic ② va ③ vb ④ con ⑤ conR ⑥ cond ⑦ subj ⑧ resA ⑨ resB ⑩ concl ⑪ stance ⑫ reason ⑬ jv＋jn ⑭ does ⑮ result ⑯ impl ⑰ final ⑱ rec；`p1end` 是 P1 收尾句（少數題才有）。
7. **chain 從 `zh` 和 `stance`、`p2zh`、`p3zh` 濃縮**，不是照抄：拿掉【】註記和括號英文，每段 ≤60 字。思路要對應現在的 18 格內容（`es`），不是舊版。
8. 文法說明必須正確；不確定就不要寫。

## 驗證與產出

```bash
node tools/we_cards/validate.js 3 5 8     # 驗指定題
node tools/we_cards/build.js 3            # 產單題 PDF 看樣子（WE_三分鐘卡_3.pdf，會自動縮字塞進一頁）
node tools/we_cards/build.js              # 37 題全產 → WE_三分鐘卡.pdf
```
