#!/usr/bin/env python3
"""QuotaBird social and email collateral. Run from the repo root: python3 make-social.py
Writes to ./social/ (not deployed). Same fonts, colours and covers as the site and share cards.
  post-*.jpg      1080x1350 portrait images for LinkedIn posts (also fine in email)
  carousel-*.pdf  a swipeable LinkedIn document post, 1080x1350 per slide
  email-signature.png   600x150 strip for an email signature
"""
import io, os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = 'social'; os.makedirs(OUT, exist_ok=True)
SURF = (0xFF, 0xFF, 0xFF); INK = (0x13, 0x16, 0x19); VAR = (0x55, 0x62, 0x70); ACC = (0x0A, 0x71, 0xB1); LINE = (0xDD, 0xE4, 0xEA)
hexc = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
_WOFF = open('gsf.woff2', 'rb').read(); _cache = {}
def font(w, size):
    if (w, size) not in _cache:
        inst = instancer.instantiateVariableFont(TTFont(io.BytesIO(_WOFF)), {'wght': max(300, min(900, w)), 'opsz': max(12, min(72, size))}, inplace=False)
        inst.flavor = None; buf = io.BytesIO(); inst.save(buf); buf.seek(0); _cache[(w, size)] = ImageFont.truetype(buf, size)
    return _cache[(w, size)]
BIRD = Image.open('logo.png').convert('RGBA'); MASK = BIRD.split()[3]

# the shelf's covers, same words and colours as the site
COVERS = {
    'deal': ("Is this even a deal?", '#F6F9FC', '#131619'), 'pipeline': ("Enough pipeline?", '#F6F9FC', '#131619'),
    'quota': ("Is my quota crazy?", '#EAF4FF', '#131619'), 'rep': ("Rep or territory?", '#F6F9FC', '#131619'),
    'partner': ("Is this partner doing anything?", '#F6F9FC', '#131619'), 'discount': ("They want a discount.", '#F6F9FC', '#131619'),
}

def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= width: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]

def cover(im, x, y, bw, key, title_size, sub=None):
    """A book cover, like the site: flat fill, thin outline, title, the bird mark in brand blue, stamp. 3:4."""
    title, bg, ink = COVERS[key]; bh = int(bw * 4 / 3); s = bw / 172
    cv = Image.new('RGBA', (bw, bh), hexc(bg) + (255,)); cd = ImageDraw.Draw(cv)
    bm = MASK.resize((int(bw * .8), int(bw * .8 * MASK.height / MASK.width)), Image.LANCZOS)
    tint = Image.new('RGBA', bm.size, (0x9D, 0xD2, 0xFF, 0)); tint.putalpha(bm.point(lambda a: int(a * .55)))
    cv.alpha_composite(tint, (int(bw * .32), bh - int(bm.height * .9)))
    tf = font(800, title_size); ty = int(18 * s)
    for line in wrap(cd, title, tf, bw - int(34 * s)):
        cd.text((int(17 * s), ty), line, font=tf, fill=hexc(ink)); ty += int(title_size * 1.18)
    if sub:
        sf = font(400, int(title_size * .5)); ty += int(title_size * .35)
        for line in wrap(cd, sub, sf, bw - int(34 * s)):
            cd.text((int(17 * s), ty), line, font=sf, fill=hexc(ink) + (215,)); ty += int(title_size * .66)
    cd.text((int(17 * s), bh - int(26 * s)), 'QUOTABIRD', font=font(700, max(9, int(11 * s))), fill=hexc(ink) + (170,))
    rm = Image.new('L', (bw, bh), 0); ImageDraw.Draw(rm).rounded_rectangle((0, 0, bw - 1, bh - 1), int(14 * s), fill=255)
    im.paste(cv, (x, y), rm)
    ImageDraw.Draw(im).rounded_rectangle((x, y, x + bw - 1, y + bh - 1), int(14 * s), outline=(0xC9, 0xE1, 0xF7) if bg == '#EAF4FF' else (0xDD, 0xE4, 0xEA), width=max(2, int(2 * s)))
    return bh

W, H, M = 1080, 1350, 84
def canvas():
    im = Image.new('RGB', (W, H), SURF); d = ImageDraw.Draw(im)
    b = BIRD.resize((int(52 * BIRD.width / BIRD.height), 52), Image.LANCZOS); im.paste(b, (M, M - 4), b)
    d.text((M + b.width + 16, M + 2), 'QuotaBird', font=font(700, 32), fill=INK)
    return im, d
def footer(d, left, url):
    d.line((M, H - M - 70, W - M, H - M - 70), fill=LINE, width=2)
    d.text((M, H - M - 40), left, font=font(400, 28), fill=VAR)
    uf = font(700, 30); d.text((W - M - d.textlength(url, font=uf), H - M - 42), url, font=uf, fill=ACC)
def save(im, name):
    p = os.path.join(OUT, name); im.save(p, quality=92, optimize=True, subsampling=0); return p

# ── posts ──
def post_shelf():
    im, d = canvas()
    d.text((M, M + 120), 'THE QUOTA LANDED', font=font(700, 26), fill=ACC)
    y = M + 162
    for line in ['Is your quota', 'crazy?']:
        d.text((M - 3, y), line, font=font(800, 84), fill=INK); y += 96
    keys = ['quota', 'pipeline', 'deal', 'rep', 'partner', 'discount']; bw = 236; gap = 25; x0 = (W - 3 * bw - 2 * gap) // 2; y0 = y + 44
    for i, k in enumerate(keys):
        cover(im, x0 + (i % 3) * (bw + gap), y0 + (i // 3) * (int(bw * 4 / 3) + gap), bw, k, 30)
    footer(d, 'Free. A few questions or a few numbers.', 'quotabird.com')
    return save(im, 'post-1-shelf.jpg')

def post_one(key, fname, lines, url, left):
    im, d = canvas(); bw = 480; bh = int(bw * 4 / 3); x = (W - bw) // 2; y = M + 118
    cover(im, x, y, bw, key, 66)
    ty = y + bh + 62
    for i, line in enumerate(lines):
        f = font(800 if i == 0 else 400, 44 if i == 0 else 34); col = INK if i == 0 else VAR
        for l in wrap(d, line, f, W - 2 * M):
            d.text(((W - d.textlength(l, font=f)) // 2, ty), l, font=f, fill=col); ty += int(f.size * 1.3)
        ty += 8
    footer(d, left, url)
    return save(im, fname)

def post_3x():
    im, d = canvas()
    d.text((M, M + 120), 'THE MATH BEHIND 3X', font=font(700, 26), fill=ACC)
    d.text((M - 3, M + 160), '3X is a', font=font(800, 108), fill=INK); d.text((M - 3, M + 282), 'win rate.', font=font(800, 108), fill=INK)
    y = M + 430
    for l in wrap(d, "It quietly assumes you win a third of what you qualify. Win less, and you need more.", font(400, 36), W - 2 * M):
        d.text((M, y), l, font=font(400, 36), fill=VAR); y += 50
    y += 36; rows = [('Win rate', 'Coverage you need'), ('15%', '6.7X'), ('20%', '5.0X'), ('25%', '4.0X'), ('33%', '3.0X'), ('40%', '2.5X')]
    rh = 66
    for i, (a, b) in enumerate(rows):
        yy = y + i * rh; hl = (a == '20%')
        if hl: d.rounded_rectangle((M - 16, yy - 10, W - M + 16, yy + rh - 16), 14, fill=(0xFF, 0xE2, 0xA8))
        f = font(700 if i == 0 else (800 if hl else 500), 26 if i == 0 else 40); col = VAR if i == 0 else INK
        d.text((M, yy + (8 if i == 0 else 0)), a.upper() if i == 0 else a, font=f, fill=col)
        d.text((W - M - d.textlength(b.upper() if i == 0 else b, font=f), yy + (8 if i == 0 else 0)), b.upper() if i == 0 else b, font=f, fill=col)
        if i < len(rows) - 1: d.line((M, yy + rh - 14, W - M, yy + rh - 14), fill=LINE, width=2)
    y2 = y + len(rows) * rh + 20
    d.text((M, y2), 'Planning to 3X with a 20% win rate is', font=font(400, 32), fill=VAR)
    d.text((M, y2 + 44), 'hopium with a spreadsheet.', font=font(800, 32), fill=INK)
    footer(d, 'Coverage = 1 ÷ your win rate', 'quotabird.com/pipeline')
    return save(im, 'post-3-three-x.jpg')

def post_kit():
    im, d = canvas()
    d.text((M, M + 120), 'FREE PRINTABLE', font=font(700, 26), fill=ACC)
    d.text((M - 3, M + 160), "The Manager's", font=font(800, 84), fill=INK); d.text((M - 3, M + 256), 'Field Kit', font=font(800, 84), fill=INK)
    y = M + 380
    for l in wrap(d, "Useful things for the weeks when the number, the team, or both are giving you trouble.", font(400, 34), W - 2 * M):
        d.text((M, y), l, font=font(400, 34), fill=VAR); y += 48
    ph = 500; front = Image.open('kit/preview-1.jpg').convert('RGB'); back = Image.open('kit/preview-2.jpg').convert('RGB')
    pw = int(front.width * ph / front.height); front = front.resize((pw, ph), Image.LANCZOS); back = back.resize((pw, ph), Image.LANCZOS)
    px, py = (W - pw) // 2 - 24, y + 50
    def shadowed(page, angle, x, yy, alpha=70):
        pg = page.convert('RGBA'); sh = Image.new('RGBA', (pg.width + 80, pg.height + 80), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle((40, 48, 40 + pg.width, 48 + pg.height), fill=(0, 0, 0, alpha)); sh = sh.filter(ImageFilter.GaussianBlur(14))
        layer = Image.new('RGBA', sh.size, (0, 0, 0, 0)); layer.alpha_composite(sh); layer.paste(pg, (40, 40)); layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
        im.paste(layer, (x - 40 - (layer.width - sh.width) // 2, yy - 40 - (layer.height - sh.height) // 2), layer)
    shadowed(back, -4, px + 52, py + 18, 45); fr = front.copy(); ImageDraw.Draw(fr).rectangle((0, ph - 10, pw, ph), fill=(0x88, 0xB1, 0xCB)); shadowed(fr, 0, px, py)
    footer(d, '8 pages.', 'quotabird.com/kit')
    return save(im, 'post-6-managers-kit.jpg')

# ── carousel: where deals break ──
def slide(n, total, big, q, line):
    im, d = canvas()
    d.text((W - M - d.textlength(f'{n} / {total}', font=font(600, 26)), M + 12), f'{n} / {total}', font=font(600, 26), fill=VAR)
    d.text((M, M + 190), 'WHERE DEALS BREAK', font=font(700, 28), fill=ACC)
    d.text((M - 5, M + 234), big, font=font(800, 176), fill=INK)
    y = M + 490
    for l in wrap(d, q, font(700, 62), W - 2 * M):
        d.text((M, y), l, font=font(700, 62), fill=INK); y += 78
    y += 50; d.line((M, y, M + 140, y), fill=ACC, width=7); y += 56
    for l in wrap(d, line, font(400, 46), W - 2 * M):
        d.text((M, y), l, font=font(400, 46), fill=VAR); y += 64
    footer(d, 'Deal Check: five questions, a straight answer', 'quotabird.com/deal')
    return im

def carousel():
    total = 7; pages = []
    im, d = canvas(); bw = 470; x = (W - bw) // 2
    d.text((M, M + 130), 'Where deals break', font=font(800, 92), fill=INK)
    for i, l in enumerate(wrap(d, "Most deals that fall out of the forecast were never really in it. They break in one of five places.", font(400, 38), W - 2 * M)):
        d.text((M, M + 262 + i * 54), l, font=font(400, 38), fill=VAR)
    cover(im, x, M + 440, bw, 'deal', 64)
    d.text((W - M - d.textlength('Swipe for the five', font=font(700, 30)), H - M - 40), 'Swipe for the five', font=font(700, 30), fill=ACC)
    d.text((M, H - M - 40), f'1 / {total}', font=font(600, 26), fill=VAR); pages.append(im)
    pages.append(slide(2, total, 'Customer', "Have they said, in their words, that they want to solve this?", "If they haven't said it out loud, it's still your idea."))
    pages.append(slide(3, total, 'Money', "Does the money have a name: a budget line, a program, a fiscal year?", '"They have budget" isn\'t an answer until it has a name.'))
    pages.append(slide(4, total, 'Power', "Have you met someone who can sign, or just someone who likes you?", "Somebody who likes you still can't sign. Ask for the introduction this week."))
    pages.append(slide(5, total, 'Path', "Do you know how they'll actually buy it?", "Procurement adds months. Know the vehicle and the approvals before you forecast."))
    pages.append(slide(6, total, 'Now', "What makes it happen this period instead of next?", "No reason for now means it's next quarter's problem, however real it is."))
    im, d = canvas(); y = M + 200
    for l in wrap(d, "Answer all five with a name and a date, and you've got a deal.", font(800, 64), W - 2 * M):
        d.text((M - 2, y), l, font=font(800, 64), fill=INK); y += 78
    y += 20
    for l in wrap(d, "Otherwise you've got hopium. Just don't forecast it yet.", font(400, 40), W - 2 * M):
        d.text((M, y), l, font=font(400, 40), fill=VAR); y += 56
    y += 70; d.rounded_rectangle((M, y, W - M, y + 250), 28, fill=(0xF1, 0xF5, 0xF8))
    d.text((M + 40, y + 42), 'Deal Check', font=font(800, 44), fill=INK)
    for i, l in enumerate(["Five taps, about a minute.", "No login. No CRM. Nothing your boss can see."]):
        d.text((M + 40, y + 108 + i * 48), l, font=font(400, 32), fill=VAR)
    footer(d, f'{total} / {total}', 'quotabird.com/deal'); pages.append(im)
    p = os.path.join(OUT, 'carousel-where-deals-break.pdf')
    pages[0].save(p, 'PDF', save_all=True, append_images=pages[1:], resolution=144)
    for i, pg in enumerate(pages): pg.save(os.path.join(OUT, f'carousel-slide-{i + 1}.jpg'), quality=90, subsampling=0)
    return p

def signature():
    S = 2; w, h = 600 * S, 150 * S; im = Image.new('RGB', (w, h), SURF); d = ImageDraw.Draw(im)
    b = BIRD.resize((int(40 * S * BIRD.width / BIRD.height), 40 * S), Image.LANCZOS); im.paste(b, (22 * S, 26 * S), b)
    d.text((22 * S + b.width + 10 * S, 30 * S), 'QuotaBird', font=font(700, 22 * S), fill=INK)
    d.text((22 * S, 80 * S), 'A little help with your quota', font=font(400, 17 * S), fill=VAR)
    d.text((22 * S, 106 * S), 'quotabird.com', font=font(700, 17 * S), fill=ACC)
    for i, k in enumerate(['deal', 'pipeline', 'quota', 'rep']):
        cover(im, (292 + i * 74) * S, 22 * S, 62 * S, k, 9 * S)
    im = im.resize((600, 150), Image.LANCZOS); p = os.path.join(OUT, 'email-signature.png'); im.save(p, optimize=True); return p

made = [post_shelf(),
        post_one('deal', 'post-2-deal.jpg', ["Is this even a deal?", "Customer, money, power, path, now. Five taps, a straight answer."], 'quotabird.com/deal', 'Free.'),
        post_3x(),
        post_one('quota', 'post-4-quota.jpg', ["Just got your quota letter?", "Base, variable and the number. Ten seconds to find out if it's crazy."], 'quotabird.com/quota', 'Free.'),
        post_one('rep', 'post-5-rep.jpg', ["Before you write them up.", "Five questions to tell a rep problem from a territory problem."], 'quotabird.com/rep', 'Free.'),
        post_kit(), carousel(), signature()]
for p in made: print(p)
