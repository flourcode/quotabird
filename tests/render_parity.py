import random, json, asyncio
from playwright.async_api import async_playwright
random.seed(3)
CHECKS=['rep','deal']   # Nov 11: the other question checks were folded into host pages
CALCS={'quota-case':'basis=saas&lastyear=8000000&runrate=9000000&pipeline=6000000&win=25&quota=12000000',
 'commit':'commit=3000000&term=36&elapsed=14&used=900000&monthly=70000',
 'quota':None,'discount':None,'pay':None,'commission':None}   # offer was redesigned on purpose; parity.mjs fuzzes it
async def text(page, sel):
    # the math and the verdict copy, not the Mark card (its copy changes on purpose, the numbers never do)
    return await page.evaluate(f"(()=>{{const e=document.querySelector('{sel}');if(!e)return '';const c=e.cloneNode(true);c.querySelectorAll('.mark-card').forEach(x=>x.remove());document.body.appendChild(c);const t=c.innerText;c.remove();return t}})()")
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(); fails=0; n=0
        await pg.route('**/*', lambda r: r.abort() if 'localhost' not in r.request.url else r.continue_())
        for slug in CHECKS:
            for _ in range(12):
                code=''.join(random.choice('ysn') for _ in range(5))
                out=[]
                for port in (8801,8802):
                    await pg.goto(f'http://localhost:{port}/{slug}/#{code}'); await pg.wait_for_timeout(250)
                    out.append(await text(pg,'#screen'))
                n+=1
                if out[0]!=out[1] or len(out[0])<40:
                    fails+=1; print('CHECK DIFF',slug,code,len(out[0]),len(out[1]))
        # calculators: read the default hash from the page's own fields, then random variants
        for slug in CALCS:
            await pg.goto(f'http://localhost:8801/{slug}/'); await pg.wait_for_timeout(200)
            fields=await pg.evaluate("Array.from(document.querySelectorAll('#f input[id]')).map(i=>i.id)")
            for _ in range(10):
                qs='&'.join(f'{f}={random.choice([0,1,5,12,25,40,250000,1200000,3500000])}' for f in fields)
                out=[]
                for port in (8801,8802):
                    await pg.goto(f'http://localhost:{port}/{slug}/#{qs}'); await pg.wait_for_timeout(250)
                    out.append((await text(pg,'#out'))+'|'+(await text(pg,'#out2')))
                n+=1
                if out[0]!=out[1]: fails+=1; print('CALC DIFF',slug,qs)
        for qs in ['t=10000000&p=32000000&w=20&s=500000&n=8&y=fy','t=5000000&p=8000000&w=25&y=cy&c=1950000&b=1200000']:
            out=[]
            for port in (8801,8802):
                await pg.goto(f'http://localhost:{port}/pipeline/#{qs}'); await pg.wait_for_timeout(300)
                out.append(await text(pg,'#out')+await text(pg,'#out2'))
            n+=1
            if out[0]!=out[1]: fails+=1; print('PIPE DIFF',qs)
        print(f'render parity: {n} comparisons, {fails} differences'); await b.close()
asyncio.run(main())
