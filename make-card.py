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
    headline=['Before you commit it,', 'prove it.'],
    dek='Five questions to separate proof from hopium before your manager does.',
    foot='Built for federal sellers. No login. No CRM.', url='quotabird.com/deal',
    pillars=['CUSTOMER', 'MONEY', 'POWER', 'PATH', 'NOW']),
  'rep': dict(out='card-rep.jpg', wordmark='REP CHECK',
    headline=['Before you write them up,', 'figure out what you inherited.'],
    dek='Is it the rep, the patch, a skill gap, or an effort gap?',
    foot='For sales managers. No names. Nothing stored.', url='quotabird.com/rep',
    pillars=['PATCH', 'CUSTOMERS', 'PIPELINE', 'CRAFT', 'WILL']),
  'partner': dict(out='card-partner.jpg', wordmark='PARTNER CHECK',
    headline=['Before you renew the partnership,', 'test it.'],
    dek='Five questions that separate a partner who sells with you from a logo on a slide.',
    foot='For partner managers. No names. Nothing stored.', url='quotabird.com/partner',
    pillars=['SOURCED', 'ACCOUNTS', 'OWNER', 'PLAN', 'PULL']),
  'territory': dict(out='card-territory.jpg', wordmark='TERRITORY CHECK',
    headline=['Before you sign up for the number,', 'test the territory.'],
    dek='Can the patch make the number, or are you being asked to grow where nobody could?',
    foot='For sellers. No account names. Nothing stored.', url='quotabird.com/territory',
    pillars=['SPEND', 'ACCOUNTS', 'BASE', 'ACCESS', 'HISTORY']),
  'olr': dict(out='card-olr.jpg', wordmark='OLR CHECK',
    headline=['Before you walk into OLR,', 'test your case.'],
    dek='Five questions, then the room grills you. Grades the case, never the rep.',
    foot='For managers with a rep to defend. No names. No ratings.', url='quotabird.com/olr',
    pillars=['RECEIPTS', 'OWNERSHIP', 'SCOPE', 'HOW', 'NEXT']),
  'quota': dict(out='card-quota.jpg', wordmark='QUOTA CHECK', headline=['Is my quota crazy?', ''], dek='Your number against your on-target earnings, and what it asks of your patch.',
    foot='Free. In your browser. Nothing stored.', url='quotabird.com/quota', pillars=['OTE', 'MULTIPLE', 'VARIABLE', 'GROWTH']),
  'discount': dict(out='card-discount.jpg', wordmark='DISCOUNT CHECK', headline=['They want a discount.', ''], dek='What it costs you in commission, and the company in margin, before you say yes.',
    foot='Free. In your browser. Nothing stored.', url='quotabird.com/discount', pillars=['PRICE', 'DISCOUNT', 'MARGIN', 'YOUR CUT']),
  'commission': dict(out='card-commission.jpg', wordmark='COMMISSION CHECK', headline=['It closed.', 'What do I take home?'], dek='A planning estimate of the check after withholding, in about ten seconds.',
    foot='Free. In your browser. Nothing stored. Not tax advice.', url='quotabird.com/commission', pillars=['DEAL', 'RATE', 'WITHHELD', 'TAKE-HOME']),
  'account': dict(out='card-account.jpg', wordmark='ACCOUNT CHECK', headline=['Do you know the account,', 'or just your contact?'], dek="Five questions, then the room grills you. Finds where you're single-threaded.",
    foot='For sellers. No names. Nothing stored.', url='quotabird.com/account', pillars=['MISSION', 'MONEY', 'POWER', 'INCUMBENT', 'PATH']),
  'risk': dict(out='card-risk.jpg', wordmark='RISK CHECK', headline=['4X coverage can still', 'be a house of cards.'], dek='Five questions about the shape of your pipeline, not the size.',
    foot='For sellers and managers. No deal names. Nothing stored.', url='quotabird.com/risk', pillars=['SPREAD', 'MOTION', 'NEXT', 'TIMING', 'FRESH']),
  'competition': dict(out='card-competition.jpg', wordmark='COMPETITION CHECK', headline=['Why you,', 'instead of nothing?'], dek='Five questions that tell you whether the incumbent, or doing nothing, is beating you.',
    foot='For sellers. No names. Nothing stored.', url='quotabird.com/competition', pillars=['NOTHING', 'SWITCH', 'PREFERENCE', 'PROOF', 'ACCESS']),
  'brief': dict(out='card-brief.jpg', wordmark='BRIEF CHECK',
    headline=["What's the question you're", 'hoping nobody asks?'],
    dek='Brief Check finds it before the meeting does. Five questions, then the room grills you.',
    foot='Any doc, deck or QBR. Nothing uploaded. Nothing stored.', url='quotabird.com/brief',
    pillars=['POINT', 'RECEIPTS', 'ALTERNATIVE', 'HOLE', 'ASK']),
}
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
    SURF=(0xF9,0xFC,0xFF); INK=(0x13,0x16,0x19); VAR=(0x55,0x62,0x70); ACC=(0x1D,0xA1,0xF2); SOFT=(0xC2,0xE3,0xFF); ONSOFT=(0x00,0x18,0x2B)
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
    im.save(K['out'], quality=90, optimize=True)
    print(K['out'], os.path.getsize(K['out']), 'bytes'); sys.exit(0)

C = CARDS[sys.argv[1] if len(sys.argv) > 1 else 'home']
HEADLINE, DEK, FOOT, URL, PILLARS = C['headline'], C['dek'], C['foot'], C['url'], C['pillars']

W, H, M = 1200, 630, 72
SURF=(0xF9,0xFC,0xFF); INK=(0x13,0x16,0x19); VAR=(0x55,0x62,0x70); PINK=(0x1D,0xA1,0xF2)
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
hf = font(800, C.get('hsize', 74)); y = M + 104
for line in HEADLINE:
    d.text((M - 3, y), line, font=hf, fill=INK); y += 88
d.text((M, y + 14), DEK, font=font(400, 29), fill=VAR)
cy = y + 84; cx = M; cf = font(700, 25)
for t in PILLARS:
    pw = int(d.textlength(t, font=cf) + 52)
    d.rounded_rectangle((cx, cy, cx + pw, cy + 54), radius=14, fill=PRIMC)
    d.text((cx + 26, cy + 13), t, font=cf, fill=ONPRIMC); cx += pw + 16
fy = H - M - 20
d.text((M, fy), FOOT, font=font(400, 24), fill=VAR)
uf = font(700, 26)
d.text((W - M - d.textlength(URL, font=uf), fy - 2), URL, font=uf, fill=PINK)
im.save(C['out'], quality=90, optimize=True)
print(C['out'], os.path.getsize(C['out']), 'bytes')
