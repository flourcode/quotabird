# End to end: run the site on :8801 (python3 -m http.server 8801 from the site root) and
# tests/mockserver.mjs on :8803 (the real Lambda code with canned Gemini answers).
import asyncio, os, urllib.request
from playwright.async_api import async_playwright
BASE = 'http://localhost:8801'; LAMBDA = 'lambda-url.us-east-1.on.aws'; SHOTS = os.environ.get('QB_SHOTS', '/tmp')
errors = []
async def setup(ctx):
    async def handle(route):
        u = route.request.url
        if LAMBDA in u:
            req = urllib.request.Request('http://localhost:8803/', data=route.request.post_data.encode(), method='POST', headers={'Content-Type': 'text/plain'})
            try:
                with urllib.request.urlopen(req) as r: body = r.read(); status = r.status
            except urllib.error.HTTPError as e: body = e.read(); status = e.code
            await route.fulfill(status=status, body=body, headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'})
        elif 'localhost' in u: await route.continue_()
        else: await route.abort()
    await ctx.route('**/*', handle)
async def run(vw, vh, tag):
    async with async_playwright() as p:
        b = await p.chromium.launch(); ctx = await b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=2); await setup(ctx)
        pg = await ctx.new_page()
        pg.on('pageerror', lambda e: errors.append((tag, str(e))))
        pg.on('console', lambda m: errors.append((tag, m.text)) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
        await pg.goto(BASE + '/ask-mark/'); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{SHOTS}/{tag}-askmark-empty.png')
        await pg.click('.ask-ex >> nth=0'); await pg.wait_for_selector('.msg-mark:not(.is-thinking)', timeout=10000); await pg.wait_for_timeout(300)
        print(tag, 'reply', (await pg.inner_text('.msg-mark .msg-body'))[:90].replace('\n', ' '), '| chips', await pg.locator('.ask-next .ask-ex').count(), '| tool', await pg.locator('.ask-next .ask-ex-tool').count(), '| placeholder', await pg.get_attribute('#askText', 'placeholder'))
        await pg.fill('#askText', 'So what do I do this week?'); await pg.click('#askBtn'); await pg.wait_for_function("document.querySelectorAll('.msg-mark:not(.is-thinking)').length === 2", timeout=10000)
        print(tag, 'turns', await pg.locator('.msg').count())
        await pg.screenshot(path=f'{SHOTS}/{tag}-askmark.png', full_page=True)
        await pg.click('#askNew'); print(tag, 'after new', await pg.locator('.msg').count())
        for slug, txt in [('meeting-prep', 'Thursday I meet the HHS deputy CIO about a pilot.'), ('account-plan', 'VA claims office, $2M number, through Carahsoft.'), ('update-upward', '$3M number, $1.2M closed, Northwind stuck in legal.')]:
            await pg.goto(BASE + f'/{slug}/'); await pg.fill('#askText', txt); await pg.click('#askBtn')
            await pg.wait_for_selector('.msg-mark:not(.is-thinking)', timeout=10000); await pg.wait_for_timeout(300)
            print(tag, slug, (await pg.inner_text('.msg-mark .msg-body'))[:70].replace('\n', ' | '), '| copy', await pg.locator('.msg-copy').count(), '| chips', await pg.locator('.ask-next .ask-ex').count(), '| examples', await pg.locator('.ask-ex[data-example]').count())
            await pg.screenshot(path=f'{SHOTS}/{tag}-{slug}.png', full_page=True)
        await b.close()
async def main():
    await run(390, 844, 'phone'); await run(1280, 900, 'desk'); print('ERRORS', errors)
if __name__ == "__main__": asyncio.run(main())
