---
name: pte-sync-setup
description: PTE-Study-Hub 如何在 Mac 與 Windows 兩台電腦間同步
metadata: 
  node_type: memory
  type: project
  originSessionId: 6e2eaaea-1dc7-4cd5-a617-9b9beb138d70
  modified: 2026-08-12T07:53:06.818Z
---

PTE-Study-Hub 用 GitHub 當兩台電腦的同步中心，倉庫 github.com/jameskan-TW/pte-study。

- **Mac**：`/Users/nn/Documents/claude/pte-study`（SSH，port 443 已設好）
- **Windows**：`C:\Users\james\OneDrive\文件\Claude-workspace\projects\PTE-Study-Hub`（HTTPS）

維持同步的規則：**開工先 `git pull`、收工 `git add -A && commit && push`**。任一台落後就 pull 補回來。

**注意事項：**
- Windows 倉庫在 OneDrive 裡，OneDrive 會同步 `.git`，偶爾會搶檔。若出現鎖檔錯誤，考慮把倉庫搬到 OneDrive 外（如 `C:\Users\james\dev\pte-study`）。
- 別再用「從雲端手動下載一份副本」的做法看最新內容——那只會造成分歧、分不清哪份是真的。一律 `git pull`。
- 2026-06-17 曾發生 Windows clone 落後 26 個 commit（停在 6/10），同時旁邊放了一份 Google Drive 下載副本（CRLF）造成混淆，已 pull 追上並刪除副本。
- `.claude/launch.json` 是兩台共用的檔：2026-08-12 起分成兩組設定——Windows 用 `pte-study`（python）、Mac 用 `pte-study-mac`（python3＋Mac 路徑）。**不要把它改回單一設定**，改單一組就會弄壞另一台的 preview。

**2026-10-24 起：練習進度記憶改放 repo `_memory/`**（James 出差五天要在 Mac 接續）。auto-memory 每台各自一份、Mac 看不到 Windows 寫的，所以把全部記憶檔複製進 repo `_memory/`，CLAUDE.md 開頭有說明：開工先讀 `_memory/MEMORY.md`，進度有變直接改 `_memory/` 並 commit；本機 auto-memory 只是副本。
