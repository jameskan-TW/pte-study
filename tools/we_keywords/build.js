// WE 關鍵用詞表產生器：讀 tools/we_cards/data.json（先跑 tools/we_cards/extract.js），
// 從總表 ZH 四段摘要裡抽「中文 (英文)」配對＝每題關鍵用詞，標出跨題共用／本題獨有，輸出 WE_關鍵用詞.html
const fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..','..');
const data=require(path.join(root,'tools/we_cards/data.json')).sort((a,b)=>a.o-b.o);
const strip=s=>String(s==null?'':s).replace(/<[^>]+>/g,'').replace(/\s+/g,' ').trim();
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const SLOTS=['topic','va','vb','con','conR','cond','resA','resB','concl','stance','reason','does','result','impl','final','rec'];
const PARA={p1:'P1 開頭',p2:'P2 讓步／原因',p3:'P3 主論＋例子',p4:'P4 結論建議'};

// 每題全文（16 格純文字小寫）→ 算某片語出現在幾題
const fulltext=data.map(q=>SLOTS.map(k=>strip(q.es[k])).join(' | ').toLowerCase());
const norm=s=>s.toLowerCase().replace(/[’']/g,"'").replace(/\s+/g,' ').trim();
const countQ=en=>{const e=norm(en);let n=0;for(const t of fulltext){if(t.includes(e))n++;}return n;};
// 背誦地圖片語庫：用詞裡含片語庫片語的部分標灰底線（已在片語庫背過），整條都被片語庫蓋住＝共用卡
const mapHtml=fs.readFileSync(path.join(root,'WE_背誦地圖.html'),'utf8');
const PHRASES=JSON.parse(mapHtml.match(/const PHRASES = (\[.*?\]);/s)[1]).map(x=>x.en).sort((a,b)=>b.length-a.length);
function markLib(en){
  const low=en.toLowerCase();const taken=new Array(en.length).fill(false);const spans=[];
  for(const ph of PHRASES){const pl=ph.toLowerCase();let i=0;
    while((i=low.indexOf(pl,i))>=0){const j=i+pl.length;
      const okL=i===0||!/[a-z0-9]/.test(low[i-1]),okR=j===low.length||!/[a-z0-9]/.test(low[j]);
      if(okL&&okR&&!taken.slice(i,j).some(Boolean)){for(let k=i;k<j;k++)taken[k]=true;spans.push([i,j]);}
      i=j;}}
  spans.sort((a,b)=>a[0]-b[0]);let out='',pos=0;
  for(const [i,j] of spans){out+=esc(en.slice(pos,i))+'<u>'+esc(en.slice(i,j))+'</u>';pos=j;}
  out+=esc(en.slice(pos));
  const letters=en.replace(/[^A-Za-z]/g,'').length,cov=spans.reduce((a,[i,j])=>a+en.slice(i,j).replace(/[^A-Za-z]/g,'').length,0);
  return {html:out,allLib:letters>0&&cov>=letters*0.9};
}

const DELIM=/[；。：，、【】]|——|→|\)/;
function pairs(txt){
  txt=txt.replace(/【[^】]*】/g,'');
  const out=[];const re=/\(([^()]*[A-Za-z][^()]*)\)/g;let m,last=0;
  while((m=re.exec(txt))){
    const before=txt.slice(0,m.index);
    // 中文提示＝上一個分隔符之後的字
    let seg=before;const parts=before.split(DELIM);seg=parts[parts.length-1];
    seg=seg.replace(/^\s*[—\-→\s]+/,'').replace(/[—\-→\s]+$/,'').trim();
    let role='';const r=seg.match(/^(反方|我方|主題|例|含義|小結|建議|結論|讓步|主論|立場|成因|後果|解方|問題|普遍性)[:：]\s*/);
    if(r){role=r[1];seg=seg.slice(r[0].length);}
    const en=m[1].trim();
    if(/^(may|can|could|would|will|should|must|might)$/i.test(en))continue;   // 單獨情態動詞不算用詞
    out.push({zh:seg,en,role});
  }
  return out;
}

let uniqTotal=0,allTotal=0;
const cards=data.map(q=>{
  const paras=['p1','p2','p3','p4'].map(p=>{
    const ps=pairs(q.zh[p]||'').map(x=>{const n=countQ(x.en);const lib=markLib(x.en);const shared=n>1||lib.allLib;allTotal++;if(!shared)uniqTotal++;return {...x,n,shared,enHtml:lib.html};});
    return {p,ps};
  });
  const nu=paras.reduce((a,b)=>a+b.ps.filter(x=>!x.shared).length,0);
  const na=paras.reduce((a,b)=>a+b.ps.length,0);
  const chips=paras.map(({p,ps})=>`<div class="para"><div class="plabel">${PARA[p]}</div><div class="chips">${ps.map(x=>{
    const cls=x.shared?'s':'u';const tag=x.n>1?`<i class="n" title="另有 ${x.n-1} 題用到同一片語">${x.n}題</i>`:(x.shared?`<i class="n">片語庫</i>`:'');
    const hint=x.en.split(/\s+/).filter(w=>/[A-Za-z0-9]/.test(w)).map(w=>w[0]).join(' ');
    return `<span class="chip ${cls}">${x.role?`<b class="role">${esc(x.role)}</b>`:''}<span class="zh">${esc(x.zh)}</span><span class="en" data-h="${esc(hint)}">${x.enHtml}</span>${tag}</span>`;}).join('')}</div></div>`).join('');
  return `<section class="card" id="q${q.o}" data-n="${esc(q.n)}">
<header><span class="num">#${q.o}</span><span class="code">${esc(q.n)}</span><h2>${esc(q.t)}</h2><span class="cnt" title="獨有／全部">${nu}／${na}</span></header>
<p class="en0">${esc(q.en)}</p>
<p class="stance">立場：${esc(strip(q.stance))}</p>
${chips}
</section>`;
}).join('\n');

const html=`<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WE 關鍵用詞表</title>
<style>
:root{--u:#c0392b;--ub:#fdecea;--s:#7f8c8d;--sb:#f2f3f4;--b:#2c3e50}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 -apple-system,"PingFang TC","Noto Sans TC",sans-serif;color:#222;background:#fafafa}
.top{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid #ddd;padding:8px 12px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.top h1{font-size:17px;margin:0 8px 0 0}.top label{font-size:13px;cursor:pointer;user-select:none}.top .leg{font-size:12px;color:#555;margin-left:auto}
main{max-width:980px;margin:0 auto;padding:12px}
.card{scroll-margin-top:56px;background:#fff;border:1px solid #e3e3e3;border-radius:8px;padding:10px 14px;margin:0 0 14px}
header{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}.num{font-weight:700;color:var(--b)}.code{font-size:12px;color:#888}
h2{font-size:16px;margin:0}.cnt{margin-left:auto;font-size:12px;color:var(--u)}
.en0{font-size:12.5px;color:#666;margin:4px 0}.stance{margin:2px 0 6px;font-size:13.5px;color:var(--b)}
.para{display:flex;gap:8px;align-items:flex-start;margin:4px 0}.plabel{flex:0 0 96px;font-size:12px;color:#555;padding-top:5px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;flex-direction:column;border:1px solid #ddd;border-radius:6px;padding:3px 8px;background:#fff;font-size:13px;line-height:1.3;max-width:100%}
.chip .zh{font-size:11.5px;color:#666}.chip .en{font-weight:600}.chip .role{font-size:10.5px;color:#fff;background:#95a5a6;border-radius:3px;padding:0 4px;align-self:flex-start;margin-bottom:1px;font-style:normal}
.chip.u{border-color:#e6b0aa;background:var(--ub)}.chip.u .en{color:var(--u)}
.chip .en u{text-decoration:none;color:#777;font-weight:500;border-bottom:1px dotted #999}
.chip.s{background:var(--sb);border-color:#e0e0e0}.chip.s .en{color:#555;font-weight:500}.chip .n{font-size:10px;color:#999;font-style:normal}
body.uonly .chip.s{display:none}
body.dict .chip .en{color:transparent;position:relative;user-select:none}body.dict .chip .en::after{content:attr(data-h);color:#aaa;position:absolute;left:0;top:0;letter-spacing:1px;font-weight:400}
body.dict .chip .en u{color:transparent;border-color:transparent}body.dict .chip.open .en u{color:#777;border-color:#999}
body.dict .chip.open .en{color:inherit}body.dict .chip.open .en::after{content:none}body.dict .chip.u.open .en{color:var(--u)}
.toc{font-size:12px;line-height:1.9;margin:0 0 10px}.toc a{margin-right:6px;color:var(--b);text-decoration:none}
@media (max-width:600px){.para{flex-direction:column;gap:2px}.plabel{flex:none;padding:0}}
@media print{.top{display:none}body{background:#fff;font-size:12px}.card{break-inside:avoid;border:none;border-bottom:1px solid #ccc;border-radius:0;padding:4px 0;margin:0 0 6px}.en0{display:none}.chip{padding:1px 5px;font-size:11px}.chip .zh{font-size:9.5px}.toc{display:none}
 body.uonly .chip.s{display:none}}
</style></head><body>
<div class="top"><h1>WE 關鍵用詞表</h1>
<label><input type="checkbox" id="uonly"> 只看本題獨有</label>
<label><input type="checkbox" id="dict"> 默寫（遮英文，點格揭開）</label>
<span class="leg"><span style="color:var(--u)">紅＝只有這題用</span>　灰＝跨題共用／片語庫已收；紅字裡的<u style="color:#777;border-bottom:1px dotted #999;text-decoration:none">灰底線</u>＝片語庫片語，不用再背　共 ${allTotal} 條，獨有 ${uniqTotal}</span></div>
<main>
<p class="toc">${data.map(q=>`<a href="#q${q.o}">#${q.o}</a>`).join('')}</p>
<p style="font-size:13px;color:#555;margin:0 0 10px">每題的用詞來自總表四段中文摘要裡括號標的英文；<b style="color:var(--u)">紅色</b>是只有這一題會用到的字，記住它們＋共用片語（背誦地圖）就能組出整篇。來源：<code>tools/we_keywords/build.js</code> 讀 <code>WE_論點總表.html</code>，改總表後重跑。</p>
${cards}
</main>
<script>
const b=document.body;
for(const id of ['uonly','dict']){const el=document.getElementById(id);try{el.checked=localStorage.getItem('we_kw_'+id)==='1'}catch(e){}
 const f=()=>{b.classList.toggle(id,el.checked);try{localStorage.setItem('we_kw_'+id,el.checked?'1':'0')}catch(e){}};el.addEventListener('change',f);f();}
document.addEventListener('click',e=>{const c=e.target.closest('.chip');if(c&&b.classList.contains('dict'))c.classList.toggle('open');});
</script></body></html>`;
fs.writeFileSync(path.join(root,'WE_關鍵用詞.html'),html);
console.log('wrote WE_關鍵用詞.html',data.length,'題',allTotal,'條，獨有',uniqTotal);
