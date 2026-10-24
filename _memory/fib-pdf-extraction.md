---
name: fib-pdf-extraction
description: 如何從 ptefighter 機經 PDF 程式化擷取題目與答案（FIB 下拉題等）
metadata: 
  node_type: memory
  type: project
  originSessionId: 1c38d699-b9d8-464b-af2b-d9a2fe6b40e7
---

ptefighter 機經 PDF（如 `FIB-RW_2026-06-06.pdf`）的可靠擷取法，給未來同類 PDF 用：

- **正確答案＝文中與選項表用「黃色高亮」標記的字**。用 PyMuPDF（`fitz`）抓 `get_drawings()` 裡 fill 顏色 `(1.0,1.0,0.0)` 的 `re` 矩形，矩形內的字就是答案。橘色 `(0.95,0.68,0.24)` 是 #id 徽章、棕紅 `(0.77,0.34,0.23)` 是標籤，**不是答案**，要排除。
- PDF 有「灰(0xC4C4C4)＋黑」雙層疊印（防拷），每個字會重複出現，需逐行 collapse 連續重複 token。
- 內容頁從 page index 16 起（前面是多頁目錄）。題目標題行格式 `N. Title #08xxxx`；`num`(目錄序號) 與 `id`(題庫號) **不同步**，一律以 id＋blanks 內容對齊，別照 num 假設。
- 選項表：每列開頭是空格編號，後接 4 個選項；黃色那格＝答案。**罩門**：選項若是 2×2 換行排版或含連字號多字詞（low-calorie），純文字單行偵測會漏列（約 5% 空格）。多字詞選項會被拆成 token。
- **補漏靠視覺**：漏列的題目把該頁渲染成 PNG（`get_pixmap`），交給子代理用 Read 看圖、照黃色高亮讀出完整選項表，可達 100% 覆蓋（2026-06 用此補滿 92 題、+133 空格 → 2373 空格全到）。文章內答案有時表格格沒上黃、但內文有黃，以內文為準。
- 工具鏈：`pdftotext`(MinGW，純文字)＋PyMuPDF(座標/高亮)。Windows python311 全路徑＋`PYTHONIOENCODING=utf-8`；原始 txt 用 `errors='replace'`（有 0xb7 中點）。

成品流程見 [[pte-sync-setup]]：擷取→清理 JSON→分批平行子代理產逐空格拆解→組 HTML。2026-06 已用此法做出 `FIB-RW_拆解.html`（532 題逐空格拆解）。
