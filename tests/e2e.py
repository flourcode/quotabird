import asyncio, json, sys
from playwright.async_api import async_playwright
BASE='http://localhost:8801'; LAMBDA='lambda-url.us-east-1.on.aws'
errors=[]
async def setup(ctx):
    async def handle(route):
        u=route.request.url
        if LAMBDA in u:
            import urllib.request
            req=urllib.request.Request('http://localhost:8803/', data=route.request.post_data.encode(), method='POST', headers={'Content-Type':'text/plain'})
            try:
                with urllib.request.urlopen(req) as r: body=r.read(); status=r.status
            except urllib.error.HTTPError as e: body=e.read(); status=e.code
            await route.fulfill(status=status, body=body, headers={'Content-Type':'application/json','Access-Control-Allow-Origin':'*'})
        elif 'localhost' in u: await route.continue_()
        else: await route.abort()
    await ctx.route('**/*', handle)
def watch(page, name):
    page.on('console', lambda m: errors.append((name, m.text)) if m.type=='error' and 'net::ERR_FAILED' not in m.text and 'Failed to load resource' not in m.text else None)
    page.on('pageerror', lambda e: errors.append((name, str(e))))
async def run(vw, vh, tag):
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':vw,'height':vh}, device_scale_factor=2); await setup(ctx)
        pg=await ctx.new_page(); watch(pg, tag)
        # 1. pipeline question
        await pg.goto(BASE+'/ask-quotabird/'); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'/home/claude/shots/{tag}-ask-empty.png', full_page=False)
        await pg.click('[data-example*="Am I screwed"]'); await pg.wait_for_selector('#aVerdict', timeout=8000)
        vals=await pg.evaluate("Array.from(document.querySelectorAll('#aForm input')).map(i=>i.id+'='+i.value)")
        verdict=await pg.inner_text('#aVerdict'); print(tag,'pipeline fields',vals); print(tag,'verdict',verdict.replace('\n',' | '))
        await pg.screenshot(path=f'/home/claude/shots/{tag}-ask-pipeline.png', full_page=True)
        await pg.click('#aExplainBtn'); await pg.wait_for_selector('.ask-explain', timeout=8000)
        print(tag,'explain',(await pg.inner_text('.ask-explain')).replace('\n',' | '))
        await pg.screenshot(path=f'/home/claude/shots/{tag}-ask-explain.png', full_page=True)
        link=await pg.get_attribute('#aOut2 .startnote a','href'); print(tag,'full link',link)
        # 2. quota question
        await pg.fill('#askText','They gave me a $1.2M quota, measured on bookings. Is that crazy?'); await pg.click('#askBtn'); await pg.wait_for_selector('#aForm', timeout=8000); await pg.wait_for_timeout(200)
        print(tag,'quota out',(await pg.inner_text('#aOut')).replace('\n',' | '))
        await pg.fill('#af-base','150000'); await pg.fill('#af-variable','150000'); await pg.wait_for_timeout(200)
        print(tag,'quota verdict',(await pg.inner_text('#aOut')).replace('\n',' | '))
        # 3. deal
        await pg.fill('#askText','Is my federal deal real or not?'); await pg.click('#askBtn'); await pg.wait_for_selector('.ask-qs', timeout=8000)
        for k,v in [('customer','yes'),('money','no'),('power','sort'),('path','yes'),('now','sort')]:
            await pg.click(f'[data-choice="{k}"][data-v="{v}"]')
        await pg.wait_for_selector('#aRes .verdict'); await pg.wait_for_timeout(900); print(tag,'deal',(await pg.inner_text('#aRes')).replace('\n',' | ')[:260])
        await pg.screenshot(path=f'/home/claude/shots/{tag}-ask-deal.png', full_page=True)
        # 4. none
        await pg.fill('#askText','what is the weather in Austin'); await pg.click('#askBtn'); await pg.wait_for_selector('.ask-none', timeout=8000)
        print(tag,'none',(await pg.inner_text('.ask-none')).replace('\n',' | '))
        # 5. meeting -> workflow
        await pg.fill('#askText','I have a meeting with the VA CIO next week about claims. Help me prepare.'); await pg.click('#askBtn'); await pg.wait_for_selector('#askOut a.btn-primary', timeout=8000)
        await pg.click('#askOut a.btn-primary'); await pg.wait_for_selector('#wfForm')
        print(tag,'prefill customer',await pg.input_value('#customer'),'| known',(await pg.input_value('#known'))[:50])
        await pg.fill('#objective','agree to a two-week pilot'); await pg.click('#wfBtn'); await pg.wait_for_selector('.wf-out', timeout=8000)
        print(tag,'meeting',(await pg.inner_text('.wf-out')).replace('\n',' | ')[:300])
        await pg.screenshot(path=f'/home/claude/shots/{tag}-meeting.png', full_page=True)
        # 6. account plan
        await pg.goto(BASE+'/account-plan/'); await pg.fill('#account','Veterans Affairs claims office'); await pg.fill('#target','$2,000,000'); await pg.fill('#product','data platform')
        await pg.fill('#win','25%'); await pg.click('[data-choice="fy"][data-v="10"]')
        await pg.fill('#opps','Claims modernization, $750K, March\nData platform renewal, $400K, August\nTraining, $50K')
        await pg.fill('#priorities','They want the claims backlog down this year.')
        await pg.wait_for_timeout(200); print(tag,'plan math',(await pg.inner_text('#wfMath')).replace('\n',' | '))
        await pg.click('#wfBtn'); await pg.wait_for_selector('.wf-out', timeout=8000)
        await pg.screenshot(path=f'/home/claude/shots/{tag}-account-plan.png', full_page=True)
        print(tag,'plan',(await pg.inner_text('.wf-out')).replace('\n',' | ')[:300])
        # 7. update upward
        await pg.goto(BASE+'/update-upward/'); await pg.click('[data-choice="type"][data-v="miss"]'); await pg.fill('#target','$3,000,000'); await pg.fill('#closed','$1,200,000'); await pg.fill('#forecast','$2,600,000')
        await pg.fill('#deals','Northwind, $1.2M, waiting on legal\nContoso, $650K, proposal out'); await pg.fill('#blockers','Northwind legal is slow'); await pg.fill('#asks','A call with their GC')
        await pg.click('#wfBtn'); await pg.wait_for_selector('.wf-out', timeout=8000)
        await pg.screenshot(path=f'/home/claude/shots/{tag}-update.png', full_page=True)
        print(tag,'update',(await pg.inner_text('.wf-out')).replace('\n',' | ')[:400])
        await b.close()
async def main():
    await run(390,844,'phone'); await run(1280,900,'desk')
    print('ERRORS', errors)
asyncio.run(main())
