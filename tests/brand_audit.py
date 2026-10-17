# Brand audit: measures every page type against the design-system rules in HANDOFF.md, in light and dark.
# Needs the site on :8801 and the mock Lambda on :8803 (see e2e.py). Prints one block per page.
import asyncio, json, os, sys
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
from e2e import setup, BASE

PAGES = ['/', '/ask-mark/', '/meeting-prep/', '/update-upward/', '/tools/', '/quota/', '/pipeline/', '/pay/',
         '/deal/', '/rep/', '/notes/', '/notes/the-number-isnt-changing/', '/about/', '/work-with-mark/', '/kits/',
         '/math/', '/privacy/', '/404.html']

AUDIT = r"""
() => {
  const BLUE = 'rgb(124, 192, 245)', BLUEP = ['rgb(102, 179, 239)', 'rgb(147, 203, 247)'];
  const vis = (e) => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 2 && r.height > 2 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05 && r.bottom > 0; };
  const inFold = (e) => e.getBoundingClientRect().top < innerHeight;
  const lum = (c) => { const m = c.match(/[\d.]+/g); if (!m) return null; const [r, g, b] = m.slice(0, 3).map(v => { v = v / 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }); return .2126 * r + .7152 * g + .0722 * b; };
  const alpha = (c) => { const m = c.match(/[\d.]+/g); return m && m.length > 3 ? +m[3] : 1; };
  const bgOf = (e) => { for (let x = e; x; x = x.parentElement) { const b = getComputedStyle(x).backgroundColor; if (alpha(b) > .5) return b; } return getComputedStyle(document.body).backgroundColor; };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); if (x == null || y == null) return 99; return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  const name = (e) => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  const out = { filledInFold: [], blueNotTappable: [], gradients: [], shadows: [], underlinedButtons: [], lowContrast: [], fonts: new Set(), h1: null, radii: {} };
  const all = [...document.querySelectorAll('body *')].filter(vis);
  for (const e of all) {
    const s = getComputedStyle(e);
    out.fonts.add(s.fontFamily.split(',')[0].replace(/"/g, ''));
    const bg = s.backgroundColor;
    const isBlue = bg === BLUE || BLUEP.includes(bg);
    const tappable = e.closest('a, button, summary, label, [role=button]');
    if (isBlue && !tappable && !e.closest('svg') && e.tagName !== 'IMG') out.blueNotTappable.push(name(e));
    if (isBlue && (e.matches('a, button')) && inFold(e)) out.filledInFold.push(name(e) + ' "' + (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 30) + '"');
    if (s.backgroundImage.includes('gradient')) out.gradients.push(name(e));
    if (s.boxShadow !== 'none' && !s.boxShadow.split(/,(?![^(]*\))/).every(x => x.includes('inset'))) out.shadows.push(name(e) + ' ' + s.boxShadow.slice(0, 50));
    if ((e.matches('.btn, button, .ck, .ask-ex, .chip, .msg-tool, .bk') || (e.matches('a') && isBlue)) && s.textDecorationLine.includes('underline') && !e.matches('.linkbtn, .btn-text, .msg-copy, [aria-current], .card-accent .btn:not(.btn-primary), .mark-card .btn:not(.btn-primary)')) out.underlinedButtons.push(name(e) + ' "' + (e.innerText || '').trim().slice(0, 30) + '"');
    for (const k of ['card', 'ck', 'composer-box', 'ask-ex', 'msg-body', 'btn', 'chip', 'banner', 'verdict', 'list', 'mark-card', 'kit-promo']) if (e.classList.contains(k)) (out.radii[k] = out.radii[k] || new Set()).add(s.borderTopLeftRadius);
    const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (own && !e.closest('svg') && !e.closest('.verdict, .hc-out, .sumbar, .short')) {
      const r = ratio(s.color, bgOf(e)); const big = parseFloat(s.fontSize) >= 24 || (parseFloat(s.fontSize) >= 18.66 && +s.fontWeight >= 700);
      if (r < (big ? 3 : 4.5)) out.lowContrast.push(name(e) + ' ' + r.toFixed(2) + ' "' + e.textContent.trim().slice(0, 30) + '"');
    }
  }
  const h = document.querySelector('h1'); if (h && vis(h)) { const s = getComputedStyle(h); out.h1 = `${s.fontSize} ${s.fontWeight} ${s.letterSpacing}`; }
  out.fonts = [...out.fonts]; for (const k in out.radii) out.radii[k] = [...out.radii[k]];
  return out;
}
"""

async def prep(pg, path):
    # put each tool into its result state so the result card is audited too
    if path in ('/deal/', '/rep/'):
        await pg.click('#prep')
        for v in ['yes', 'sort', 'no', 'yes', 'sort']: await pg.click(f'.choice[data-v="{v}"]'); await pg.wait_for_timeout(200)
        await pg.wait_for_timeout(300)

async def main():
    only = sys.argv[1:] or PAGES
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for scheme in ('light', 'dark'):
            ctx = await b.new_context(viewport={'width': 390, 'height': 844}, color_scheme=scheme); await setup(ctx); pg = await ctx.new_page()
            for path in only:
                await pg.goto(BASE + path); await pg.wait_for_timeout(350); await prep(pg, path)
                r = await pg.evaluate(AUDIT)
                flags = {k: v for k, v in r.items() if v and k not in ('fonts', 'h1', 'radii', 'filledInFold')}
                fold = r['filledInFold']
                line = f"[{scheme}] {path}  h1 {r['h1']}  filled-in-fold {len(fold)}"
                if len(fold) > 1: line += ' ' + json.dumps(fold)
                if [f for f in r['fonts'] if f not in ('Inter', 'ui-monospace', 'SFMono-Regular', 'Menlo')]: line += f"  fonts {r['fonts']}"
                print(line)
                for k, v in flags.items(): print(f"    {k}: {v[:6]}")
                if scheme == 'light': print(f"    radii {r['radii']}")
            await ctx.close()
        await b.close()
asyncio.run(main())
