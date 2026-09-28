#!/usr/bin/env python3
"""OpenGraph share cards (1200x630) and the LinkedIn banner, in Option A: a white page, the tool's question as a
chunky headline, and a result card in its verdict tint (green / yellow / red), exactly as the page shows it.
  python3 make-card.py quota      -> card-quota.jpg        python3 make-card.py home   -> card.jpg
  python3 make-card.py banner     -> linkedin-banner.jpg   python3 make-card.py kit    -> card-kit.jpg
Run from the web root. Needs pillow, fonttools, brotli. Uses inter.woff2 and logo.png so the cards match the pages."""
import io, os, sys
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

CARDS = {
  'home': dict(out='card.jpg', wordmark='QuotaBird',
    headline=["You sure that's", 'enough pipeline?'],
    dek='Put in your win rate and find out.',
    foot='', url='quotabird.com',
    pillars=['TARGET', 'PIPELINE', 'WIN RATE', 'THE GAP']),
  'deal': dict(out='card-deal.jpg', wordmark='DEAL CHECK',
    headline=['Is it real,', 'or is it hopium?'],
    dek='Ask these questions before your manager does.',
    foot='', url='quotabird.com/deal',
    pillars=['CUSTOMER', 'MONEY', 'POWER', 'PATH', 'NOW']),
  'rep': dict(out='card-rep.jpg', wordmark='REP CHECK',
    headline=['Is it the rep,', 'or the territory?'],
    dek='Is it the rep, the territory, a skill gap, or an effort gap?',
    foot='', url='quotabird.com/rep',
    pillars=['TERRITORY', 'CUSTOMERS', 'PIPELINE', 'CRAFT', 'WILL']),
  'partner': dict(out='card-partner.jpg', wordmark='PARTNER CHECK',
    headline=['Is this partner', 'doing anything?'],
    dek='Five questions that separate a real partnership from promises.',
    foot='', url='quotabird.com/partner',
    pillars=['SOURCED', 'ACCOUNTS', 'OWNER', 'PLAN', 'PULL']),
  'territory': dict(out='card-territory.jpg', wordmark='TERRITORY CHECK',
    headline=['Does this', 'territory suck?'],
    dek='Can the territory make the number, or are you being asked to grow where nobody could?',
    foot='', url='quotabird.com/territory',
    pillars=['SPEND', 'ACCOUNTS', 'BASE', 'ACCESS', 'HISTORY']),
  'olr': dict(out='card-olr.jpg', wordmark='TALENT REVIEW CHECK',
    headline=['Can you defend', 'your people?'],
    dek='Five questions, then the room pressure-tests you. Grades the assessment, never the rep.',
    foot='', url='quotabird.com/olr',
    pillars=['RECEIPTS', 'OWNERSHIP', 'SCOPE', 'HOW', 'NEXT']),
  'pipeline': dict(out='card-pipeline.jpg', wordmark='PIPELINE CHECK', headline=["You sure that's", 'enough pipeline?'], dek='3X is a rule of thumb. Put in your win rate and see what you really need.',
    foot='', url='quotabird.com/pipeline', pillars=['TARGET', 'PIPELINE', 'WIN RATE', 'THE GAP']),
  'quota-case': dict(out='card-quota-case.jpg', wordmark='QUOTA CASE', headline=['What has to be true', 'for this quota to work?'], dek='Last year, run rate, pipeline and headcount in. The gap, and what closes it.',
    foot='', url='quotabird.com/quota-case', pillars=['LAST YEAR', 'RUN RATE', 'PIPELINE', 'THE GAP']),
  'quota': dict(out='card-quota.jpg', wordmark='QUOTA CHECK', headline=['Is your quota crazy?', ''], dek='Your number against your on-target earnings, and what it asks of your territory.',
    foot='', url='quotabird.com/quota', pillars=['OTE', 'MULTIPLE', 'VARIABLE', 'GROWTH']),
  'discount': dict(out='card-discount.jpg', wordmark='DISCOUNT CHECK', headline=['How much discount', 'is too much?'], dek='What it costs you in commission, and the company in margin, before you say yes.',
    foot='', url='quotabird.com/discount', pillars=['PRICE', 'DISCOUNT', 'MARGIN', 'YOUR CUT']),
  'commission': dict(out='card-commission.jpg', wordmark='COMMISSION CHECK', headline=['It closed.', "What do you actually keep?"], dek='A planning estimate of the check after withholding, in about ten seconds.',
    foot='Not tax advice.', url='quotabird.com/commission', pillars=['DEAL', 'RATE', 'WITHHELD', 'TAKE-HOME']),
  'account': dict(out='card-account.jpg', wordmark='ACCOUNT CHECK', headline=['Do you know', 'your customer?'], dek="Five questions, then the room pressure-tests you. Finds where you're single-threaded.",
    foot='', url='quotabird.com/account', pillars=['MISSION', 'MONEY', 'POWER', 'INCUMBENT', 'PATH']),
  'risk': dict(out='card-risk.jpg', wordmark='RISK CHECK', headline=['Are two deals', 'carrying your year?'], dek='Five questions about the shape of your pipeline, not the size.',
    foot='', url='quotabird.com/risk', pillars=['SPREAD', 'MOTION', 'NEXT', 'TIMING', 'FRESH']),
  'competition': dict(out='card-competition.jpg', wordmark='COMPETITION CHECK', headline=['Why you', 'and not them?'], dek='Five questions that tell you whether the incumbent, or doing nothing, is beating you.',
    foot='', url='quotabird.com/competition', pillars=['NOTHING', 'SWITCH', 'PREFERENCE', 'PROOF', 'ACCESS']),
  'brief': dict(out='card-brief.jpg', wordmark='BRIEF CHECK',
    headline=['Will your brief', 'survive the room?'],
    dek='Brief Check finds it before the meeting does. Five questions, then the room pressure-tests you.',
    foot='', url='quotabird.com/brief',
    pillars=['POINT', 'RECEIPTS', 'ALTERNATIVE', 'HOLE', 'ASK']),
}

KITCARDS = {
  'seller': dict(out='card-seller.jpg', dir='seller', title=["The Seller's", 'Field Kit'], sub=['Useful things for the weeks when', 'the deal, the number, or both', 'are giving you trouble.'], foot='', url='quotabird.com/seller'),
  'kit': dict(out='card-kit.jpg', dir='kit', title=["The Manager's", 'Field Kit'], sub=['Useful things for the weeks when', 'the number, the team, or both', 'are giving you trouble.'], foot='', url='quotabird.com/kit'),
  'leader': dict(out='card-leader.jpg', dir='leader', title=['The Leadership', 'Field Kit'], sub=['For managers who want to', 'become the person other leaders', 'call when something matters.'], foot='', url='quotabird.com/leader'),
}

# What the result card shows: the page's own default answer (calculators) or a real verdict word (question tools).
TINT = {'green': ('#AAD576', '#0B1215'), 'yellow': ('#FCEC60', '#0B1215'), 'red': ('#FF7F50', '#0B1215'), 'grey': ('#EEF2F8', '#0B1215')}   # Bold: the word is always ink
RESULTS = {   # each result is worded as the answer to the tool's question, exactly as the page says it
  'home':        ('68×', "Yes. It's crazy.", 'Your quota is 68× your OTE. The typical range is 15 to 30.', 'red'),   # a warm, believable result makes people check their own
  'quota':       ('47×', "Close. It's aggressive.", 'Well above the typical 15 to 30 for cloud run rate.', 'yellow'),
  'quota-case':  ('$2.6M', "You've got a gap.", 'Push back with it, or close it with $10.4M of new pipeline.', 'yellow'),
  'discount':    ('$6K', 'This much needs a trade.', 'What 15% off costs you in commission.', 'yellow'),
  'commission':  ('$28K', "That's your take-home.", 'About 70 cents of every commission dollar.', 'green'),
  'pipeline':    ('3.2X', "Not really. You're at risk.", 'A 20% win rate says you need 5X.', 'yellow'),
  'deal':        ('Hopium.', None, 'Weakest: power.', 'red'),
  'rep':         ('The territory.', None, 'Good rep, bad situation.', 'yellow'),
  'partner':     ('Yes. Real work.', None, 'Protect the time you spend here.', 'green'),
  'territory':   ('Yes. Nobody could hit this.', None, 'Say so now, with the math. Not in Q4.', 'red'),
  'olr':         ('No. No receipts.', None, "It may still be a good rep. It isn't an assessment yet.", 'red'),
  'account':     ('Yes. You know the account.', None, 'Now find the next one before anyone else does.', 'green'),
  'risk':        ("Yes. It's fragile.", None, 'Re-underwrite every commit deal this week.', 'yellow'),
  'competition': ("You're behind.", None, 'Weakest: proof.', 'yellow'),
  'brief':       ('No. Shark food.', None, 'Weakest: receipts.', 'yellow'),
}
WHITE, INK, MUT = (255, 255, 255), (0x0B, 0x12, 0x15), (0x4F, 0x5B, 0x66)
_WOFF = open('inter.woff2', 'rb').read(); _cache = {}
def font(w, size):
    key = (w, size)
    if key not in _cache:
        inst = instancer.instantiateVariableFont(TTFont(io.BytesIO(_WOFF)), {'wght': w}, inplace=False)
        inst.flavor = None; buf = io.BytesIO(); inst.save(buf); buf.seek(0); _cache[key] = ImageFont.truetype(buf, size)
    return _cache[key]
def hexc(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= width or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
def fit(d, text, weight, start, width, max_lines, floor=40):
    s = start
    while s > floor:
        f = font(weight, s); lines = wrap(d, text, f, width)
        if len(lines) <= max_lines and all(d.textlength(l, font=f) <= width for l in lines): return f, lines, s
        s -= 2
    f = font(weight, floor); return f, wrap(d, text, f, width), floor
def brand(im, d, x, y, h=48):
    bird = Image.open('logo.png').convert('RGBA'); bw = int(bird.width * h / bird.height); bird = bird.resize((bw, h), Image.LANCZOS)
    im.paste(bird, (x, y), bird); d.text((x + bw + 14, y + int(h * .12)), 'QuotaBird', font=font(700, int(h * .6)), fill=INK)
def result_card(im, d, box, big, word, line, tint, big_lines=2, scale=1.0):
    bg, dark = TINT[tint]; x0, y0, x1, y1 = box; d.rounded_rectangle(box, radius=int(34 * scale), fill=hexc(bg))
    pad = int(38 * scale); w = x1 - x0 - 2 * pad
    f, lines, s = fit(d, big, 900, int((170 if len(big) <= 5 else 104) * scale), w, big_lines, int(56 * scale))
    lf = font(500, int(26 * scale)); wf = font(800, int(40 * scale)); body = wrap(d, line, lf, w)[:4]
    wlines, wf2, ws = ([], None, 0)
    if word: wf2, wlines, ws = fit(d, word, 850, int(46 * scale), w, 2, int(30 * scale))
    hgt = len(lines) * int(s * .98) + int(14 * scale) + len(wlines) * int(ws * 1.12) + (int(10 * scale) if word else 0) + len(body) * int(36 * scale)
    y = y0 + (y1 - y0 - hgt) // 2 - int(8 * scale)          # the result sits in the middle of its card
    for l in lines: d.text((x0 + pad - 4, y), l, font=f, fill=INK); y += int(s * .98)
    y += int(14 * scale)
    for l in wlines: d.text((x0 + pad, y), l, font=wf2, fill=INK); y += int(ws * 1.12)
    if word: y += int(10 * scale)
    for l in body: d.text((x0 + pad, y), l, font=lf, fill=INK); y += int(36 * scale)
def save(im, out):
    im.save(out, quality=90, optimize=True, subsampling=0); print(out, os.path.getsize(out), 'bytes')

arg = sys.argv[1] if len(sys.argv) > 1 else 'home'
if arg == 'banner':
    for sc, out in ((1, 'linkedin-banner.jpg'), (2, 'linkedin-banner@2x.jpg')):
        W, H = 1584 * sc, 396 * sc; im = Image.new('RGB', (W, H), WHITE); d = ImageDraw.Draw(im)
        X = 420 * sc                                   # clear of LinkedIn's profile photo, which covers the lower left
        brand(im, d, X, 58 * sc, 44 * sc)
        f, lines, s = fit(d, 'Is your quota crazy?', 900, 80 * sc, 560 * sc, 2)
        y = 128 * sc
        for l in lines: d.text((X - 2 * sc, y), l, font=f, fill=INK); y += int(s * 1.0)
        d.text((X, y + 10 * sc), "Maybe. Let's do the math.  quotabird.com", font=font(500, 28 * sc), fill=MUT)
        result_card(im, d, (W - 72 * sc - 470 * sc, 42 * sc, W - 72 * sc, H - 42 * sc), '21×', 'Standard', 'Inside the 15 to 30 I usually see.', 'green', scale=sc * .82)
        save(im, out)
    sys.exit(0)

W, H, M = 1200, 630, 64
im = Image.new('RGB', (W, H), WHITE); d = ImageDraw.Draw(im)
brand(im, d, M, M - 6)
LW = 590
if arg in KITCARDS:
    K = KITCARDS[arg]; title = ' '.join(K['title']); label = 'FREE PRINTABLE'; url = K['url']
    pages = {'seller': '7', 'kit': '11', 'leader': '3'}[arg]
    card = (pages + ' pages', 'Free to print', ' '.join(K['sub']), 'grey')
else:
    C = CARDS[arg]; title = ' '.join(x for x in C['headline'] if x).replace("  ", " "); url = C['url']
    label = '' if arg == 'home' else C['wordmark']
    card = RESULTS[arg]
if arg in ('home', 'quota'): title = 'Is your quota crazy?'
y = 150
if label: d.text((M, y), label, font=font(700, 22), fill=MUT); y += 44
f, lines, s = fit(d, title, 900, 84, LW, 3, 48)
for l in lines: d.text((M - 3, y), l, font=f, fill=INK); y += int(s * 1.02)
if arg in ('home', 'quota'): d.text((M, y + 14), "Maybe. Let's do the math.", font=font(500, 30), fill=MUT)
d.text((M, H - M - 28), url, font=font(700, 28), fill=INK)
result_card(im, d, (W - M - 440, M + 20, W - M, H - M - 20), *card, big_lines=1 if arg in KITCARDS else 2)
out = KITCARDS[arg]['out'] if arg in KITCARDS else C['out']
save(im, out)
