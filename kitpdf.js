// Prints the three Field Kits to PDF (Letter for the site, A4 copies for checking). Needs the local server on 8765.
const chromium=require('@sparticuz/chromium'),puppeteer=require('puppeteer-core');
(async()=>{const b=await puppeteer.launch({args:chromium.args,executablePath:await chromium.executablePath(),headless:true});
for(const [u,f] of [['/seller/','seller/seller-field-kit'],['/kit/','kit/managers-field-kit'],['/leader/','leader/leader-field-kit']]){
 const pr=await b.newPage();await pr.setRequestInterception(true);pr.on('request',r=>r.url().includes('googletagmanager')?r.abort():r.continue());
 await pr.goto('http://localhost:8765'+u,{waitUntil:'networkidle0'});
 await pr.pdf({path:'/home/claude/work/'+f+'.pdf',format:'Letter',printBackground:true});
 await pr.pdf({path:'/home/claude/shot/'+f.split('/')[1]+'-a4.pdf',format:'A4',printBackground:true});await pr.close();}
await b.close();console.log('kits printed');})();
