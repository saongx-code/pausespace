// 用法：node render.js specs/xxx.json 輸出資料夾
// 讀一份輪播內容，照 carousel.html 的版型輸出 1080×1350 PNG（01.png、02.png…）
const fs = require('fs'), path = require('path');
const {chromium} = require('playwright');
(async () => {
  const specFile = path.resolve(process.argv[2]);
  const out = path.resolve(process.argv[3] || 'out');
  fs.mkdirSync(out, {recursive: true});
  const spec = JSON.parse(fs.readFileSync(specFile, 'utf8'));
  const proxy = process.env.HTTPS_PROXY ? {server: process.env.HTTPS_PROXY} : undefined;
  const b = await chromium.launch({proxy});
  const p = await b.newPage({viewport: {width: 1200, height: 1500}, deviceScaleFactor: 1});
  await p.addInitScript(s => { window.SPEC = s; }, spec);
  await p.goto('file://' + path.join(__dirname, 'carousel.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const slides = await p.$$('.s');
  for (let i = 0; i < slides.length; i++) await slides[i].screenshot({path: path.join(out, String(i + 1).padStart(2, '0') + '.png')});
  console.log('輸出', slides.length, '張到', out);
  await b.close();
})();
