// 用法：node tools/we_cards/validate.js [題號...]（不給題號＝驗全部已有註解的題）
const fs = require('fs');
const { load, loadAnn, annPath, validate } = require('./lib');
const D = load();
const want = process.argv.slice(2).map(Number);
let bad = 0, n = 0;
D.filter(d => want.length ? want.includes(d.o) : fs.existsSync(annPath(d.o))).forEach(d => {
  if (!fs.existsSync(annPath(d.o))) { console.log('#' + d.o + ' 沒有註解檔'); bad++; return; }
  let a; try { a = loadAnn(d.o); } catch (e) { console.log('#' + d.o + ' JSON 壞掉：' + e.message); bad++; return; }
  const e = validate(d, a); n++;
  if (e.length) { bad++; console.log('#' + d.o + ' ✗\n  ' + e.join('\n  ')); } else console.log('#' + d.o + ' ✓');
});
console.log(`驗了 ${n} 題，${bad} 題有問題`);
process.exit(bad ? 1 : 0);
