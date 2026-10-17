# The hand-off from a tool result to Ask Mark: every result card's button carries the numbers in the fragment,
# the chat sends them once, and the fragment is gone from the address bar. Needs the site on :8801 and the
# mock Lambda on :8803 (see e2e.py).
import asyncio, os, sys, urllib.parse
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
from e2e import setup, BASE, errors
SHOTS = os.environ.get('QB_SHOTS', '/tmp')

async def check_chat(pg, tag):
    await pg.wait_for_selector('.msg-user', timeout=8000)
    await pg.wait_for_selector('.msg-mark:not(.is-thinking)', timeout=10000)
    assert '#' not in pg.url, pg.url
    user = await pg.inner_text('.msg-user .msg-body')
    reply = await pg.inner_text('.msg-mark .msg-body')
    assert 'What would you do with this?' in user, user
    print(f'  {tag}: chat url {pg.url} | first message {len(user)} chars, starts "{user[:60]}" | reply "{reply[:50]}"')
    return user

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2); await setup(ctx)
        pg = await ctx.new_page()
        pg.on('pageerror', lambda e: errors.append(str(e)))
        pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)

        # Quota Check (a calc tool)
        await pg.goto(BASE + '/quota/'); await pg.fill('#quota', '$7,500,000'); await pg.wait_for_timeout(200)
        href = await pg.get_attribute('#askMarkBtn', 'href'); assert href.startswith('/ask-mark/#ask='), href
        seed = urllib.parse.unquote(href.split('#ask=', 1)[1]); assert 'Quota Check' in seed and '$7,500,000' in seed, seed
        print('quota seed:\n' + seed.replace('\n', '\n    '))
        await pg.screenshot(path=f'{SHOTS}/handoff-quota-card.png', full_page=True)
        await pg.click('#askMarkBtn'); await check_chat(pg, 'quota')
        await pg.screenshot(path=f'{SHOTS}/handoff-quota-chat.png', full_page=True)

        # Pipeline Check
        await pg.goto(BASE + '/pipeline/'); await pg.wait_for_timeout(300)
        if not await pg.locator('#askMarkBtn').count():
            await pg.fill('#goal', '$4,000,000'); await pg.fill('#pipe', '$6,000,000'); await pg.wait_for_timeout(300)
        href = await pg.get_attribute('#askMarkBtn', 'href'); seed = urllib.parse.unquote(href.split('#ask=', 1)[1])
        assert 'Pipeline Check' in seed and 'coverage' in seed, seed
        print('pipeline seed:\n' + seed.replace('\n', '\n    '))
        await pg.click('#askMarkBtn'); await check_chat(pg, 'pipeline')

        # Deal Check (five questions)
        await pg.goto(BASE + '/deal/'); await pg.click('#prep', timeout=5000)
        for v in ['yes', 'sort', 'no', 'yes', 'sort']:
            await pg.click(f'.choice[data-v="{v}"]'); await pg.wait_for_timeout(250)
        await pg.wait_for_selector('#askMarkBtn', timeout=5000)
        href = await pg.get_attribute('#askMarkBtn', 'href'); seed = urllib.parse.unquote(href.split('#ask=', 1)[1])
        assert 'Deal Check' in seed and 'Sort of' in seed, seed
        print('deal seed:\n' + seed.replace('\n', '\n    '))
        await pg.click('#askMarkBtn'); await check_chat(pg, 'deal')

        # Rep Check (check.js)
        await pg.goto(BASE + '/rep/'); await pg.click('#prep', timeout=5000)
        for v in ['no', 'no', 'sort', 'yes', 'yes']:
            await pg.click(f'.choice[data-v="{v}"]'); await pg.wait_for_timeout(250)
        await pg.wait_for_selector('#askMarkBtn', timeout=5000)
        href = await pg.get_attribute('#askMarkBtn', 'href'); seed = urllib.parse.unquote(href.split('#ask=', 1)[1])
        assert 'Rep Check' in seed and 'My answers:' in seed, seed
        print('rep seed:\n' + seed.replace('\n', '\n    '))
        await pg.screenshot(path=f'{SHOTS}/handoff-rep-card.png', full_page=True)
        await pg.click('#askMarkBtn'); await check_chat(pg, 'rep')

        # Home: the chat is the hero; an example chip sends and the intro collapses
        await pg.goto(BASE + '/'); await pg.wait_for_timeout(300)
        assert await pg.get_attribute('#askText', 'placeholder') == "What's going on?"
        await pg.click('.ask-ex[data-example] >> nth=2'); await pg.wait_for_selector('.msg-mark:not(.is-thinking)', timeout=10000)
        assert await pg.locator('.mark-intro').is_hidden() and await pg.locator('.ask-next .ask-ex-tool').count() == 1
        print('home: chat in place, intro collapsed, tool chip', await pg.inner_text('.ask-next .ask-ex-tool'))
        # A plain visit still shows the empty chat with chips; a junk fragment is ignored
        await pg.goto(BASE + '/privacy/'); await pg.goto(BASE + '/ask-mark/#ask=x'); await pg.wait_for_timeout(400)
        assert await pg.locator('.msg').count() == 0 and not await pg.locator('#askExamples').is_hidden()
        print('junk fragment ignored, chips shown')
        await b.close()
    print('ERRORS', errors)
asyncio.run(main())
