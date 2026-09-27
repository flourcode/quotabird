#!/usr/bin/env python3
"""Regenerate the 1200x630 OpenGraph cards in the site's own palette and typeface.
  python3 make-card.py deal       -> card.jpg
  python3 make-card.py pipeline   -> card-pipeline.jpg
Run from the web-root folder. Needs: pillow, fonttools, brotli. Uses inter.woff2 so the cards cannot drift from the pages."""
import re, base64, io, os
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

import sys
CARDS = {
  'home': dict(out='card.jpg', wordmark='QuotaBird',
    headline=["You sure that's", 'enough pipeline?'],
    dek='Put in your win rate and find out. Free, in your browser, nothing stored.',
    foot='No login. No certification. Nothing stored.', url='quotabird.com',
    pillars=['TARGET', 'PIPELINE', 'WIN RATE', 'THE GAP']),
  'deal': dict(out='card-deal.jpg', wordmark='DEAL CHECK',
    headline=['Is it real,', 'or is it hopium?'],
    dek='Ask these questions before your manager does.',
    foot='Built for federal sellers. No login. No CRM.', url='quotabird.com/deal',
    pillars=['CUSTOMER', 'MONEY', 'POWER', 'PATH', 'NOW']),
  'rep': dict(out='card-rep.jpg', wordmark='REP CHECK',
    headline=['Is it the rep,', 'or the territory?'],
    dek='Is it the rep, the territory, a skill gap, or an effort gap?',
    foot='For sales managers. No names. Nothing stored.', url='quotabird.com/rep',
    pillars=['TERRITORY', 'CUSTOMERS', 'PIPELINE', 'CRAFT', 'WILL']),
  'partner': dict(out='card-partner.jpg', wordmark='PARTNER CHECK',
    headline=['Is this partner', 'doing anything?'],
    dek='Five questions that separate a real partnership from promises.',
    foot='For partner managers. No names. Nothing stored.', url='quotabird.com/partner',
    pillars=['SOURCED', 'ACCOUNTS', 'OWNER', 'PLAN', 'PULL']),
  'territory': dict(out='card-territory.jpg', wordmark='TERRITORY CHECK',
    headline=['Does this', 'territory suck?'],
    dek='Can the territory make the number, or are you being asked to grow where nobody could?',
    foot='For sellers. No account names. Nothing stored.', url='quotabird.com/territory',
    pillars=['SPEND', 'ACCOUNTS', 'BASE', 'ACCESS', 'HISTORY']),
  'olr': dict(out='card-olr.jpg', wordmark='TALENT REVIEW CHECK',
    headline=['Can you defend', 'your people?'],
    dek='Five questions, then the room pressure-tests you. Grades the assessment, never the rep.',
    foot='For managers with a rep to defend. No names. No ratings.', url='quotabird.com/olr',
    pillars=['RECEIPTS', 'OWNERSHIP', 'SCOPE', 'HOW', 'NEXT']),
  'pipeline': dict(out='card-pipeline.jpg', wordmark='PIPELINE CHECK', headline=["You sure that's", 'enough pipeline?'], dek='3X is a rule of thumb. Put in your win rate and see what you really need.',
    foot='Free. In your browser. Nothing stored.', url='quotabird.com/pipeline', pillars=['TARGET', 'PIPELINE', 'WIN RATE', 'THE GAP']),
  'quota': dict(out='card-quota.jpg', wordmark='QUOTA CHECK', headline=['Is my quota crazy?', ''], dek='Your number against your on-target earnings, and what it asks of your territory.',
    foot='Free. In your browser. Nothing stored.', url='quotabird.com/quota', pillars=['OTE', 'MULTIPLE', 'VARIABLE', 'GROWTH']),
  'discount': dict(out='card-discount.jpg', wordmark='DISCOUNT CHECK', headline=['How much discount', 'is too much?'], dek='What it costs you in commission, and the company in margin, before you say yes.',
    foot='Free. In your browser. Nothing stored.', url='quotabird.com/discount', pillars=['PRICE', 'DISCOUNT', 'MARGIN', 'YOUR CUT']),
  'commission': dict(out='card-commission.jpg', wordmark='COMMISSION CHECK', headline=['It closed.', "What do I actually keep?"], dek='A planning estimate of the check after withholding, in about ten seconds.',
    foot='Free. In your browser. Nothing stored. Not tax advice.', url='quotabird.com/commission', pillars=['DEAL', 'RATE', 'WITHHELD', 'TAKE-HOME']),
  'account': dict(out='card-account.jpg', wordmark='ACCOUNT CHECK', headline=['Do you know', 'your customer?'], dek="Five questions, then the room pressure-tests you. Finds where you're single-threaded.",
    foot='For sellers. No names. Nothing stored.', url='quotabird.com/account', pillars=['MISSION', 'MONEY', 'POWER', 'INCUMBENT', 'PATH']),
  'risk': dict(out='card-risk.jpg', wordmark='RISK CHECK', headline=['Are you winging it', 'this quarter?'], dek='Five questions about the shape of your pipeline, not the size.',
    foot='For sellers and managers. No deal names. Nothing stored.', url='quotabird.com/risk', pillars=['SPREAD', 'MOTION', 'NEXT', 'TIMING', 'FRESH']),
  'competition': dict(out='card-competition.jpg', wordmark='COMPETITION CHECK', headline=['Why you', 'and not them?'], dek='Five questions that tell you whether the incumbent, or doing nothing, is beating you.',
    foot='For sellers. No names. Nothing stored.', url='quotabird.com/competition', pillars=['NOTHING', 'SWITCH', 'PREFERENCE', 'PROOF', 'ACCESS']),
  'brief': dict(out='card-brief.jpg', wordmark='BRIEF CHECK',
    headline=['Will your brief', 'survive the room?'],
    dek='Brief Check finds it before the meeting does. Five questions, then the room pressure-tests you.',
    foot='Any doc, deck or QBR. Nothing uploaded. Nothing stored.', url='quotabird.com/brief',
    pillars=['POINT', 'RECEIPTS', 'ALTERNATIVE', 'HOLE', 'ASK']),
}
if (sys.argv[1] if len(sys.argv) > 1 else '') == 'banner':
    # LinkedIn profile banner, 1584x396 (drawn at 2x). The left third stays clear for the headshot, which overlaps
    # the bottom-left on desktop and is proportionally larger in the mobile app; nothing hugs the top or bottom edge.
    from PIL import ImageFilter
    S = 2; W, H = 1584 * S, 396 * S
    SURF=(0xF9,0xFC,0xFF); INK=(0x13,0x16,0x19); VAR=(0x55,0x62,0x70); ACC=(0x0A,0x71,0xB1)
    woff2 = open('inter.woff2', 'rb').read()
    def font(w, size):
        inst = instancer.instantiateVariableFont(TTFont(io.BytesIO(woff2)), {'wght': w}, inplace=False)
        inst.flavor = None; buf = io.BytesIO(); inst.save(buf); buf.seek(0)
        return ImageFont.truetype(buf, size * S)
    hexc = lambda h: tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
    books = [("Real deal or hopium?", '#1C3D5A', '#FFFFFF'), ("Enough pipeline?", '#F2C14E', '#1B1B1B'),
             ("Crazy quota?", '#E07A5F', '#2B1B1B'), ("Rep or territory?", '#388073', '#FFFFFF')]
    im = Image.new('RGB', (W, H), SURF); d = ImageDraw.Draw(im)
    bird = Image.open('logo.png').convert('RGBA'); mask = bird.split()[3]
    # covers, right side
    cols, gap, bw = 4, 14 * S, 104 * S; bh = int(bw * 4 / 3); x0 = W - 112 * S - cols * bw - (cols - 1) * gap; y0 = (H - bh) // 2
    tf = font(800, 15); lh = 19 * S
    def wrap(text, width):
        words, lines, cur = text.split(), [], ''
        for w_ in words:
            t = (cur + ' ' + w_).strip()
            if d.textlength(t, font=tf) <= width: cur = t
            else: lines.append(cur); cur = w_
        return lines + [cur]
    for i, (title, bg, ink) in enumerate(books):
        x = x0 + i * (bw + gap); y = y0; pad = 20 * S
        sh = Image.new('RGBA', (bw + 2 * pad, bh + 2 * pad), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 5 * S, pad + bw, pad + 5 * S + bh), 6 * S, fill=(0, 0, 0, 60))
        sh = sh.filter(ImageFilter.GaussianBlur(7 * S)); im.paste(sh, (x - pad, y - pad), sh)
        cover = Image.new('RGBA', (bw, bh), hexc(bg) + (255,)); cd = ImageDraw.Draw(cover)
        cd.rectangle((0, 0, 5 * S, bh), fill=tuple(int(v * .86) for v in hexc(bg)) + (255,))
        bm = mask.resize((int(bw * .8), int(bw * .8 * mask.height / mask.width)), Image.LANCZOS)
        tint = Image.new('RGBA', bm.size, hexc(ink) + (0,)); tint.putalpha(bm.point(lambda a: int(a * .13)))
        cover.alpha_composite(tint, (int(bw * .32), bh - int(bm.height * .9)))
        ty = 13 * S
        for line in wrap(title, bw - 24 * S):
            cd.text((12 * S, ty), line, font=tf, fill=hexc(ink)); ty += lh
        cd.text((12 * S, bh - 19 * S), 'QUOTABIRD', font=font(700, 8), fill=hexc(ink) + (170,))
        rm = Image.new('L', (bw, bh), 0); ImageDraw.Draw(rm).rounded_rectangle((0, 0, bw - 1, bh - 1), 6 * S, fill=255)
        im.paste(cover, (x, y), rm)
    # the pitch, middle third
    tx = 575 * S
    lb = bird.resize((int(34 * S * bird.width / bird.height), 34 * S), Image.LANCZOS)
    ty = 92 * S
    im.paste(lb, (tx, ty), lb); d.text((tx + lb.width + 10 * S, ty + 3 * S), 'QuotaBird', font=font(700, 22), fill=INK)
    d.text((tx, ty + 56 * S), 'A LITTLE HELP WITH YOUR QUOTA', font=font(700, 13), fill=ACC)
    d.text((tx - 2 * S, ty + 80 * S), 'Pick the problem', font=font(800, 38), fill=INK)
    d.text((tx - 2 * S, ty + 124 * S), "you've got.", font=font(800, 38), fill=INK)
    d.text((tx, ty + 180 * S), 'quotabird.com', font=font(700, 19), fill=ACC)
    im.save('linkedin-banner@2x.jpg', quality=92, optimize=True, subsampling=0)
    im.resize((1584, 396), Image.LANCZOS).save('linkedin-banner.jpg', quality=92, optimize=True, subsampling=0)
    print('linkedin-banner.jpg (1584x396) and linkedin-banner@2x.jpg (3168x792)'); sys.exit(0)

if (sys.argv[1] if len(sys.argv) > 1 else '') == 'home':
    # The home card is the shelf itself. Drawn at 2x (2400x1260) and saved without chroma subsampling, so
    # LinkedIn's downscaled copies stay sharp and coloured text on coloured covers doesn't smear.
    from PIL import ImageFilter
    S = 2; W, H, M = 1200 * S, 630 * S, 64 * S
    SURF=(0xF9,0xFC,0xFF); INK=(0x13,0x16,0x19); VAR=(0x55,0x62,0x70); ACC=(0x0A,0x71,0xB1)
    woff2 = open('inter.woff2', 'rb').read()
    def font(w, size):
        inst = instancer.instantiateVariableFont(TTFont(io.BytesIO(woff2)), {'wght': w}, inplace=False)
        inst.flavor = None; buf = io.BytesIO(); inst.save(buf); buf.seek(0)
        return ImageFont.truetype(buf, size * S)
    hexc = lambda h: tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
    books = [("Real deal or hopium?", '#1C3D5A', '#FFFFFF'), ("Enough pipeline?", '#F2C14E', '#1B1B1B'),
             ("Crazy quota?", '#E07A5F', '#2B1B1B'), ("Rep or territory?", '#388073', '#FFFFFF'),
             ("Doing anything?", '#F28482', '#2B1B1B'), ("How much is too much?", '#9DD2FF', '#12324F')]
    im = Image.new('RGB', (W, H), SURF); d = ImageDraw.Draw(im)
    bird = Image.open('logo.png').convert('RGBA'); mask = bird.split()[3]
    cols, gap, bw = 3, 18 * S, 172 * S; bh = int(bw * 4 / 3); x0 = W - M - cols * bw - (cols - 1) * gap; y0 = (H - 2 * bh - gap) // 2
    tf = font(800, 24); lh = 29 * S
    def wrap(text, width):
        words, lines, cur = text.split(), [], ''
        for w_ in words:
            t = (cur + ' ' + w_).strip()
            if d.textlength(t, font=tf) <= width: cur = t
            else: lines.append(cur); cur = w_
        return lines + [cur]
    for i, (title, bg, ink) in enumerate(books):
        x = x0 + (i % cols) * (bw + gap); y = y0 + (i // cols) * (bh + gap)
        pad = 24 * S
        sh = Image.new('RGBA', (bw + 2 * pad, bh + 2 * pad), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 6 * S, pad + bw, pad + 6 * S + bh), 7 * S, fill=(0, 0, 0, 60))
        sh = sh.filter(ImageFilter.GaussianBlur(8 * S)); im.paste(sh, (x - pad, y - pad), sh)
        cover = Image.new('RGBA', (bw, bh), hexc(bg) + (255,)); cd = ImageDraw.Draw(cover)
        cd.rectangle((0, 0, 6 * S, bh), fill=tuple(int(v * .86) for v in hexc(bg)) + (255,))
        bm = mask.resize((int(bw * .8), int(bw * .8 * mask.height / mask.width)), Image.LANCZOS)
        tint = Image.new('RGBA', bm.size, hexc(ink) + (0,)); tint.putalpha(bm.point(lambda a: int(a * .13)))
        cover.alpha_composite(tint, (int(bw * .32), bh - int(bm.height * .9)))
        ty = 18 * S
        for line in wrap(title, bw - 34 * S):
            cd.text((17 * S, ty), line, font=tf, fill=hexc(ink)); ty += lh
        cd.text((17 * S, bh - 26 * S), 'QUOTABIRD', font=font(700, 11), fill=hexc(ink) + (170,))
        rm = Image.new('L', (bw, bh), 0); ImageDraw.Draw(rm).rounded_rectangle((0, 0, bw - 1, bh - 1), 7 * S, fill=255)
        im.paste(cover, (x, y), rm)
    lb = bird.resize((int(46 * S * bird.width / bird.height), 46 * S), Image.LANCZOS); im.paste(lb, (M, M - 4 * S), lb)
    d.text((M + lb.width + 14 * S, M + 1 * S), 'QuotaBird', font=font(700, 28), fill=INK)
    d.text((M, M + 96 * S), 'A LITTLE HELP WITH YOUR QUOTA', font=font(700, 17), fill=ACC)
    y = M + 128 * S
    for line in ['Pick the', 'problem', "you've got."]:
        d.text((M - 2 * S, y), line, font=font(800, 62), fill=INK); y += 70 * S
    y += 16 * S
    for line in ['A few questions.', 'A few numbers.', 'A useful answer.']:
        d.text((M, y), line, font=font(400, 25), fill=VAR); y += 34 * S
    d.text((M, H - M - 26 * S), 'quotabird.com', font=font(700, 26), fill=ACC)
    im.save('card.jpg', quality=90, optimize=True, progressive=True, subsampling=0)
    print('card.jpg', im.size, os.path.getsize('card.jpg') // 1024, 'KB'); sys.exit(0)

KITCARDS = {
  'seller': dict(out='card-seller.jpg', dir='seller', title=["The Seller's", 'Field Kit'], sub=['Useful things for the weeks when', 'the deal, the number, or both', 'are giving you trouble.'], foot='4 pages. No email.', url='quotabird.com/seller'),
  'kit': dict(out='card-kit.jpg', dir='kit', title=["The Manager's", 'Field Kit'], sub=['Useful things for the weeks when', 'the number, the team, or both', 'are giving you trouble.'], foot='8 pages. No email.', url='quotabird.com/kit'),
  'leader': dict(out='card-leader.jpg', dir='leader', title=['The Leadership', 'Field Kit'], sub=['For managers who want to', 'become the person other leaders', 'call when something matters.'], foot='3 pages. No email.', url='quotabird.com/leader'),
}
if (sys.argv[1] if len(sys.argv) > 1 else '') in KITCARDS:
    K = KITCARDS[sys.argv[1]]
    # The kit's card shows the pages themselves: text left, the two page previews stacked right.
    from PIL import ImageFilter
    W, H, M = 1200, 630, 72
    SURF=(0xF9,0xFC,0xFF); INK=(0x13,0x16,0x19); VAR=(0x55,0x62,0x70); ACC=(0x0A,0x71,0xB1); SOFT=(0xC2,0xE3,0xFF); ONSOFT=(0x00,0x18,0x2B)
    woff2 = open('inter.woff2', 'rb').read()
    def font(w, size):
        inst = instancer.instantiateVariableFont(TTFont(io.BytesIO(woff2)), {'wght': w}, inplace=False)
        inst.flavor = None; buf = io.BytesIO(); inst.save(buf); buf.seek(0)
        return ImageFont.truetype(buf, size)
    im = Image.new('RGB', (W, H), SURF); d = ImageDraw.Draw(im)
    # pages, right side
    ph = 500; front = Image.open(K['dir'] + '/preview-1.jpg').convert('RGB'); back = Image.open(K['dir'] + '/preview-2.jpg').convert('RGB')
    pw = int(front.width * ph / front.height); front = front.resize((pw, ph), Image.LANCZOS); back = back.resize((pw, ph), Image.LANCZOS)
    px, py = W - M - pw - 24, (H - ph) // 2 - 6
    def shadowed(page, angle, x, y, blur=14, alpha=70):
        pg = page.convert('RGBA'); sh = Image.new('RGBA', (pg.width + 80, pg.height + 80), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle((40, 48, 40 + pg.width, 48 + pg.height), fill=(0, 0, 0, alpha)); sh = sh.filter(ImageFilter.GaussianBlur(blur))
        layer = Image.new('RGBA', sh.size, (0, 0, 0, 0)); layer.alpha_composite(sh); layer.paste(pg, (40, 40))
        layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
        im.paste(layer, (x - 40 - (layer.width - sh.width) // 2, y - 40 - (layer.height - sh.height) // 2), layer)
    shadowed(back, -4, px + 30, py + 14, alpha=45)
    fr = front.copy(); ImageDraw.Draw(fr).rectangle((0, ph - 9, pw, ph), fill=ACC)
    shadowed(fr, 0, px, py)
    # text, left side
    bird = Image.open('logo.png').convert('RGBA'); bh = 46; bw = int(bird.width * bh / bird.height); bird = bird.resize((bw, bh), Image.LANCZOS)
    im.paste(bird, (M, M - 4), bird); d.text((M + bw + 16, M + 1), 'QuotaBird', font=font(700, 28), fill=INK)
    pf = font(700, 22); pt = 'FREE PRINTABLE'; ptw = int(d.textlength(pt, font=pf))
    d.rounded_rectangle((M, M + 84, M + ptw + 36, M + 84 + 44), radius=22, fill=SOFT); d.text((M + 18, M + 94), pt, font=pf, fill=ONSOFT)
    hf = font(800, 64); y = M + 150
    for line in K['title']:
        d.text((M - 2, y), line, font=hf, fill=INK); y += 74
    sf = font(400, 27); y += 18
    for line in K['sub']:
        d.text((M, y), line, font=sf, fill=VAR); y += 38
    fy = H - M - 20
    d.text((M, fy), K['foot'], font=font(400, 24), fill=VAR)
    uf = font(700, 26); d.text((M + int(d.textlength(K['foot'], font=font(400, 24))) + 22, fy - 2), K['url'], font=uf, fill=ACC)
    im.save(K['out'], quality=90, optimize=True, subsampling=0)
    print(K['out'], os.path.getsize(K['out']), 'bytes'); sys.exit(0)

C = CARDS[sys.argv[1] if len(sys.argv) > 1 else 'home']
HEADLINE, DEK, FOOT, URL, PILLARS = C['headline'], C['dek'], C['foot'], C['url'], C['pillars']

W, H, M = 1200, 630, 72
SURF=(0xF9,0xFC,0xFF); INK=(0x13,0x16,0x19); VAR=(0x55,0x62,0x70); PINK=(0x0A,0x71,0xB1)
PRIMC=(0xED,0xF2,0xF7); ONPRIMC=(0x13,0x16,0x19)

woff2 = open('inter.woff2', 'rb').read()
def font(w, size):
    inst = instancer.instantiateVariableFont(TTFont(io.BytesIO(woff2)), {'wght': w}, inplace=False)
    inst.flavor = None; buf = io.BytesIO(); inst.save(buf); buf.seek(0)
    return ImageFont.truetype(buf, size)

im = Image.new('RGB', (W, H), SURF); d = ImageDraw.Draw(im)
bird = Image.open(C.get('mark', 'logo.png')).convert('RGBA')
bh = 52; bw = int(bird.width * bh / bird.height); bird = bird.resize((bw, bh), Image.LANCZOS)
im.paste(bird, (M, M - 4), bird)
d.text((M + bw + 18, M + 2), C['wordmark'], font=font(700, 30), fill=INK)
# the headline and the line under it shrink until their longest line fits the card
hs = C.get('hsize', 74)
while hs > 44 and max(d.textlength(l, font=font(800, hs)) for l in HEADLINE if l) > W - 2 * M: hs -= 2
hf = font(800, hs); y = M + 104
for line in HEADLINE:
    d.text((M - 3, y), line, font=hf, fill=INK); y += int(hs * 1.19)
ds = 29
while ds > 20 and d.textlength(DEK, font=font(400, ds)) > W - 2 * M: ds -= 1
d.text((M, y + 14), DEK, font=font(400, ds), fill=VAR)
cy = y + 84; cx = M; cf = font(700, 25)
for t in PILLARS:
    pw = int(d.textlength(t, font=cf) + 52)
    d.rounded_rectangle((cx, cy, cx + pw, cy + 54), radius=14, fill=PRIMC)
    d.text((cx + 26, cy + 13), t, font=cf, fill=ONPRIMC); cx += pw + 16
fy = H - M - 20
d.text((M, fy), FOOT, font=font(400, 24), fill=VAR)
uf = font(700, 26)
d.text((W - M - d.textlength(URL, font=uf), fy - 2), URL, font=uf, fill=PINK)
im.save(C['out'], quality=90, optimize=True, subsampling=0)
print(C['out'], os.path.getsize(C['out']), 'bytes')
