# The chat as a visitor lives it: leaving for a tool and coming back, an error and a retry, a slow answer,
# a phone's return key, a tool's hand-off, the third-answer offer, and New chat. Needs the site on :8801 and
# the mock Lambda on :8803 (see e2e.py).
import asyncio, os, sys, json, urllib.parse
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
from e2e import setup, BASE, errors

is_ai = lambda u: 'localhost:8803' in u   # the Lambda (the mock, in tests), matched the same way when routing and unrouting
async def reply_count(pg): return await pg.locator('.msg-mark:not(.is-thinking):not(.is-streaming):not(.is-error)').count()
async def wait_replies(pg, n): await pg.wait_for_function(f"document.querySelectorAll('.msg-mark:not(.is-thinking):not(.is-streaming):not(.is-error)').length >= {n}", timeout=12000)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await setup(ctx); pg = await ctx.new_page()
        pg.on('pageerror', lambda e: errors.append(str(e)))

        # 0. the answer arrives as it's written (when the Lambda streams), then settles with Copy
        await pg.goto(BASE + '/ask-mark/'); await pg.evaluate("sessionStorage.clear()"); await pg.reload()
        await pg.fill('#askText', 'My champion at DHS loves us but the CO says no vehicle.'); await pg.click('#askBtn')
        seen = []
        for _ in range(60):
            st = await pg.evaluate("(()=>{const m=[...document.querySelectorAll('.msg-mark')].pop(); return m ? [m.className, m.innerText.length] : null})()")
            if st: seen.append(st)
            if st and 'is-streaming' not in st[0] and 'is-thinking' not in st[0]: break
            await pg.wait_for_timeout(60)
        streaming = [x for x in seen if 'is-streaming' in x[0]]
        grew = len({x[1] for x in streaming}) > 1
        print('0 streaming:', len(streaming), 'frames while writing, grew' if grew else 'arrived whole', '| copy', await pg.locator('.msg-mark .msg-copy').count(), '| chips', await pg.locator('.ask-next .ask-ex').count())
        if os.environ.get('QB_EXPECT_STREAM', '1') == '1': assert grew
        assert await pg.locator('.msg-mark .msg-copy').count() == 1
        await pg.click('#askNew')

        # 1. leave for the tool the chat suggested, come back: the conversation is still there, chips too
        await pg.goto(BASE + '/ask-mark/'); await pg.click('.ask-ex[data-example] >> nth=0'); await wait_replies(pg, 1)
        await pg.click('.ask-next .ask-ex-tool'); await pg.wait_for_url('**/deal/**')
        await pg.go_back(); await pg.wait_for_timeout(500)
        print('1 back from the tool:', await pg.locator('.msg').count(), 'messages,', await pg.locator('.ask-next .ask-ex').count(), 'chips, intro hidden', await pg.locator('.mark-intro').is_hidden())
        assert await pg.locator('.msg').count() == 2 and await pg.locator('.ask-next .ask-ex').count() >= 1

        # 2. home and /ask-mark/ are one conversation
        await pg.goto(BASE + '/'); await pg.wait_for_timeout(400)
        print('2 same conversation on home:', await pg.locator('.msg').count(), 'messages')
        assert await pg.locator('.msg').count() == 2

        # 3. a failed request keeps their words and retries in one tap
        state = {'fail': True}
        async def flaky(route):
            if state['fail']: state['fail'] = False; await route.fulfill(status=503, body=json.dumps({'error': 'The AI is busy right now. Try again in a minute.'}), headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'})
            else: await route.fallback()
        await pg.route(is_ai, flaky)
        await pg.fill('#askText', 'What if the champion leaves?'); await pg.click('#askBtn')
        await pg.wait_for_selector('.msg.is-error .msg-retry', timeout=8000)
        user_bubbles = await pg.locator('.msg-user').count()
        await pg.click('.msg-retry'); await wait_replies(pg, 2)
        print('3 error then retry:', user_bubbles, 'user bubbles kept, now', await reply_count(pg), 'answers, errors left', await pg.locator('.msg.is-error').count())
        assert user_bubbles == 2 and await pg.locator('.msg.is-error').count() == 0
        await pg.unroute(is_ai)

        # 4. a slow answer says so
        async def slow(route): await asyncio.sleep(7); await route.fallback()
        await pg.route(is_ai, slow)
        await pg.fill('#askText', 'And if procurement stalls?'); await pg.click('#askBtn')
        await pg.wait_for_timeout(6600); note = await pg.inner_text('.is-thinking .msg-wait')
        await wait_replies(pg, 3); await pg.unroute(is_ai)
        print('4 slow answer note:', repr(note))
        assert 'Thinking' in note

        # 5. three answers in: the real Mark, once
        real = await pg.locator('.ask-real a').count()
        print('5 offer after the third answer:', real, await pg.get_attribute('.ask-real a', 'href') if real else '')
        assert real == 1

        # 6. New chat forgets it, here and on the other page
        await pg.click('#askNew'); await pg.goto(BASE + '/ask-mark/'); await pg.wait_for_timeout(400)
        print('6 after New chat:', await pg.locator('.msg').count(), 'messages')
        assert await pg.locator('.msg').count() == 0

        # 7. a tool's hand-off folds the numbers under one line
        await pg.goto(BASE + '/quota/'); await pg.fill('#quota', '$9,000,000'); await pg.wait_for_timeout(200); await pg.click('#askMarkBtn'); await wait_replies(pg, 1)
        first = (await pg.inner_text('.msg-user .msg-body > p >> nth=0'))
        print('7 hand-off bubble:', repr(first[:70]), '| folded numbers', await pg.locator('.msg-user details.msg-more').count(), '| open', await pg.locator('.msg-user details.msg-more[open]').count())
        assert await pg.locator('.msg-user details.msg-more').count() == 1
        await pg.screenshot(path='/tmp/claude-0/shots/chatux-handoff.png')
        await ctx.close()

        # 9. the logo starts fresh; one link brings the last conversation back; Back still restores
        ctx2 = await b.new_context(viewport={'width': 1280, 'height': 900}); await setup(ctx2); pg = await ctx2.new_page()
        await pg.goto(BASE + '/'); await pg.click('.ask-ex[data-example] >> nth=0'); await wait_replies(pg, 1)
        label = (await pg.inner_text('#askNew')).strip()
        await pg.goto(BASE + '/quota/'); await pg.click('a.logo'); await pg.wait_for_url(BASE + '/'); await pg.wait_for_timeout(400)
        fresh_msgs = await pg.locator('.msg').count(); prev_shown = await pg.locator('.ask-prev').is_visible(); intro = await pg.locator('.mark-intro').is_visible()
        await pg.click('.ask-prev button'); await pg.wait_for_timeout(300)
        back_msgs = await pg.locator('.msg').count()
        print('9 logo from a tool page:', fresh_msgs, 'messages, intro shown', intro, '| pick-up link', prev_shown, '| after pick-up', back_msgs, 'messages | button says', repr(label))
        assert fresh_msgs == 0 and prev_shown and intro and back_msgs == 2 and label == 'Start over'
        await pg.click('a.logo'); await pg.wait_for_timeout(400)
        print('   logo on the home page itself:', await pg.locator('.msg').count(), 'messages, url', pg.url, ', pick-up link', await pg.locator('.ask-prev').is_visible())
        assert await pg.locator('.msg').count() == 0 and pg.url == BASE + '/'
        await pg.click('.ask-prev button'); await pg.wait_for_timeout(300)
        await pg.click('#askNew'); await pg.wait_for_timeout(200)
        print('   Start over:', await pg.locator('.msg').count(), 'messages, pick-up link', await pg.locator('.ask-prev').is_visible())
        assert await pg.locator('.msg').count() == 0 and await pg.locator('.ask-prev').is_visible()
        await pg.click('.ask-ex[data-example] >> nth=1'); await wait_replies(pg, 1)
        assert not await pg.locator('.ask-prev').is_visible(), 'the link hides once a new conversation starts'
        await pg.screenshot(path='/tmp/claude-0/shots/startover-bar.png', clip={'x': 0, 'y': 0, 'width': 1280, 'height': 420})
        await ctx2.close()

        # 8. on a phone, return makes a new line; the send button sends
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2); await setup(ctx); pg = await ctx.new_page()
        await pg.goto(BASE + '/ask-mark/'); await pg.click('#askText'); await pg.keyboard.type('Two lines'); await pg.keyboard.press('Enter'); await pg.keyboard.type('here'); await pg.wait_for_timeout(300)
        val = await pg.input_value('#askText'); sent = await pg.locator('.msg').count()
        print('8 phone return key:', repr(val), sent, 'messages sent')
        assert '\n' in val and sent == 0
        await pg.tap('#askBtn'); await wait_replies(pg, 1)
        focused = await pg.evaluate("document.activeElement && document.activeElement.id")
        print('   sent with the button; keyboard left down after the answer:', focused != 'askText')
        await ctx.close(); await b.close()
    print('ERRORS', errors)
asyncio.run(main())
