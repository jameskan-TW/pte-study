// 跨電腦搬紀錄：匯出成 JSON 檔、匯入時合併（gen.py 把這段塞進菜單頁和 FIB 練習頁）
// 檔案內容 {v, at, fib: fib_prac_v1, menu: menu90_v1}；FIB 每篇留 ts 較新的那次，菜單打勾取聯集
function exportRec() {
  const get = k => { try { return JSON.parse(localStorage.getItem(k) || '{}'); } catch (e) { return {}; } };
  const out = {v: 1, at: Date.now(), fib: get('fib_prac_v1'), menu: get('menu90_v1')};
  const d = new Date(), p = n => String(n).padStart(2, '0');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(out)], {type: 'application/json'}));
  a.download = `PTE紀錄_${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}_${p(d.getHours())}${p(d.getMinutes())}.json`;
  document.body.appendChild(a); a.click(); a.remove();
}
function importRec(input) {
  const f = input.files[0]; if (!f) return;
  const r = new FileReader();
  r.onload = () => {
    let inc; try { inc = JSON.parse(r.result); } catch (e) { alert('這個檔案讀不懂，請選「匯出紀錄」存下來的 PTE紀錄_….json'); return; }
    if (!inc || inc.v !== 1) { alert('這不是 PTE 紀錄檔'); return; }
    const get = k => { try { return JSON.parse(localStorage.getItem(k) || '{}'); } catch (e) { return {}; } };
    const fib = get('fib_prac_v1'), menu = get('menu90_v1');
    let nf = 0, nm = 0;
    Object.entries(inc.fib || {}).forEach(([id, x]) => {
      const c = fib[id];
      if (!c || (x.ts || 0) > (c.ts || 0)) { fib[id] = Object.assign({}, x, {tries: Math.max(x.tries || 0, (c && c.tries) || 0)}); nf++; }
    });
    Object.keys(inc.menu || {}).forEach(k => { if (!menu[k]) { menu[k] = 1; nm++; } });
    try { localStorage.setItem('fib_prac_v1', JSON.stringify(fib)); localStorage.setItem('menu90_v1', JSON.stringify(menu)); }
    catch (e) { alert('瀏覽器不讓存（無痕視窗？），匯入失敗'); return; }
    alert(`匯入完成：FIB 更新 ${nf} 篇、菜單新增打勾 ${nm} 項`);
    location.reload();
  };
  r.readAsText(f); input.value = '';
}
