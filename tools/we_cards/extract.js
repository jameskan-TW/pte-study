// 從 WE_論點總表.html 抽 37 題 DATA＋ZH，輸出 tools/we_cards/data.json（三分鐘卡產生器的輸入）
const fs=require('fs'),path=require('path'),vm=require('vm');
const root=path.join(__dirname,'..','..');
const html=fs.readFileSync(path.join(root,'WE_論點總表.html'),'utf8');
const m=html.match(/<script>([\s\S]*)<\/script>/);
const stub={appendChild(){},addEventListener(){},innerHTML:'',style:{},classList:{add(){},toggle(){}},querySelectorAll:()=>[],setAttribute(){}};
const ctx={document:{getElementById:()=>({...stub}),createElement:()=>({...stub}),querySelectorAll:()=>[]},console,location:{hash:''}};
vm.createContext(ctx);vm.runInContext(m[1],ctx);
const DATA=vm.runInContext('DATA',ctx),ZH=vm.runInContext('ZH',ctx);
const out=DATA.map(d=>({o:d.o,n:d.n,t:d.t,en:d.en,stance:d.stance,p2zh:d.p2zh,p3zh:d.p3zh,es:d.es,zh:ZH[d.n]||null,mistakes:d.mistakes||null})).sort((a,b)=>a.o-b.o);
fs.writeFileSync(path.join(__dirname,'data.json'),JSON.stringify(out,null,1));
console.log('wrote',out.length);
