"""Pull every piece of visible copy on QuotaBird into rows for the wordsmithing workbook.
Run from the build root after make-tools.py. Writes copy_rows.json."""
import re, json, os, glob, html as H
from bs4 import BeautifulSoup

ROWS = []; SEEN = set()
def add(prio, page, where, text, limit=None, note=''):
    t = re.sub(r'\s+([.,;:!?)])', r'\1', re.sub(r'\s+', ' ', H.unescape(text))).strip()
    if len(t) < 2 or not re.search(r'[A-Za-z]', t): return
    key = (page if page != 'Every page' else '*', t)
    if (('*', t) in SEEN) or key in SEEN: return
    SEEN.add(key); ROWS.append(dict(prio=prio, page=page, where=where, text=t, limit=limit, note=note))

# ── the parts of every page: header menu, footer, Made by Mark card ──
def chrome_strings():
    s = BeautifulSoup(open('rep/index.html', encoding='utf-8').read(), 'html.parser')
    mb = s.select_one('section#about')
    if mb:
        for el in mb.select('h2,h3,p'):
            add(2, 'Every page', 'Made by Mark card', el.get_text(' '))
        for a in mb.select('a.btn'): add(2, 'Every page', 'Made by Mark card: button', a.get_text(' '), 18)
    for a in s.select('footer .foot-nav a'): add(9, 'Every page', 'Footer link', a.get_text(' '), 18)
    for p in s.select('footer p:not(.foot-nav)'): add(9, 'Every page', 'Footer line', p.get_text(' '))
    for a in s.select('.menu-kit'): add(9, 'Every page', 'Tools menu: kit row', a.get_text(' '))

# ── JavaScript strings in a tool page: questions, verdicts, next steps, Pressure test ──
JS_STR = r"""(?:'((?:[^'\\]|\\.)*)'|"((?:[^"\\]|\\.)*)"|`((?:[^`\\$]|\\.)*)`)"""
KEYS = {'q': ('Question', 140), 'hint': ('Question: small print under it', None), 'attack': ('Verdict: first line', None),
        'sub': ('Verdict: second line', None), 'overline': ('Next-step card: small label', 40), 'text': ('Next-step card: text', None),
        'why': ('Pressure test: why it matters', None), 'fix': ('Fix for a weak answer', None), 'ask': ('Pressure test question', None),
        'title': ('Card title', 60), 'body': ('Card text', None), 'noMove': ('Result: nothing to fix', None), 'cleanSub': ('Verdict: second line', None)}
def js_strings(page, script, prio):
    # verdict words and the question each belongs to, for context
    for m in re.finditer(r"\{\s*k:\s*'(\w+)',\s*n:\s*'([^']+)',\s*q:\s*" + JS_STR, script):
        q = next(g for g in m.groups()[2:] if g is not None)
        add(prio, page, f'Question ({m.group(2).title()})', q.replace("\\'", "'"), 140, 'Must be answerable with yes, sort of, or no.')
    for m in re.finditer(r"label:\s*'([^']+)',\s*cls:\s*'\w+',\s*attack:\s*" + JS_STR + r",\s*sub:\s*" + JS_STR, script):
        g = m.groups(); word = g[0]
        add(prio, page, f'Verdict word ({word})', word, 14, 'The big word on the result.')
        add(prio, page, f'Verdict "{word}": first line', next(x for x in g[1:4] if x is not None).replace("\\'", "'"))
        add(prio, page, f'Verdict "{word}": second line', next(x for x in g[4:7] if x is not None).replace("\\'", "'"))
    for key, (where, lim) in KEYS.items():
        if key in ('q', 'attack', 'sub'): continue
        for m in re.finditer(r"\b" + key + r":\s*" + JS_STR, script):
            v = next(x for x in m.groups() if x is not None)
            if '${' in v or len(v) < 3: continue
            if key == 'body': add(2, page, 'Card after the result: text', v.replace("\\'", "'")); continue
            add(prio, page, where, v.replace("\\'", "'"), lim)
    for m in re.finditer(r"dm:\s*\(s\)\s*=>\s*`((?:[^`\\]|\\.)*)`", script):
        v = re.sub(r'\$\{[^}]*\}', '{…}', m.group(1))
        add(2, page, 'Message people copy to DM you', v, None, 'Keep each {…}: the tool fills it in (verdict, weakest answer).')
    for m in re.finditer(r"overline:\s*" + JS_STR + r",\s*text:\s*" + JS_STR + r",\s*href:\s*'[^']*',\s*label:\s*" + JS_STR, script):
        g = m.groups(); add(prio, page, 'Next-step card: button', next(x for x in g[6:9] if x is not None), 18)
    for m in re.finditer(r"grillLines:\s*\{([^}]*)\}", script):
        for k, v in re.findall(r"(\w+):\s*'((?:[^'\\]|\\.)*)'", m.group(1)):
            add(prio, page, f'Pressure test result ({k})', v.replace("\\'", "'"))

# ── visible HTML on a page ──
def page_strings(path, page, prio, main_sel='body'):
    s = BeautifulSoup(open(path, encoding='utf-8').read(), 'html.parser')
    for sel in ['header', 'footer', 'section#about', 'section.kit-band', 'script', 'style', 'nav.kit-toc', '.shelf-grid']:
        for el in s.select(sel): el.decompose()
    root = s.select_one(main_sel) or s.body
    for el in root.find_all(['h1', 'h2', 'h3', 'p', 'li', 'summary', 'button', 'a', 'td', 'th', 'span', 'div']):
        cls = ' '.join(el.get('class', []))
        if el.name in ('span', 'div') and not re.search(r'overline|pill|body|kit-hero-meta|like-t|like-by|like-why|bk-|startnote|helped', cls): continue
        if el.name == 'a' and 'btn' not in cls: continue
        if el.name == 'div' and 'body' in cls: where = 'FAQ answer'
        elif el.name == 'summary': where = 'FAQ question'
        elif el.name in ('button', 'a'): where = 'Button'
        elif el.name == 'h1': where = 'Headline'
        elif el.name in ('h2', 'h3'): where = 'Section heading'
        elif 'dek' in cls: where = 'Intro line under the headline'
        elif 'overline' in cls: where = 'Small label above'
        elif el.name in ('td', 'th'): where = 'Table cell'
        elif el.name == 'li': where = 'List item'
        else: where = 'Paragraph'
        if el.find(['p', 'li', 'div', 'h2', 'h3']) and el.name in ('li', 'div'): continue
        add(prio, page, where, el.get_text(' '), 18 if where == 'Button' else None)

# ── the home shelf ──
def shelf():
    s = BeautifulSoup(open('index.html', encoding='utf-8').read(), 'html.parser')
    for el in s.select('.front .tool-name'): add(1, 'Home', 'Small label above the headline', el.get_text(' '), 40)
    for el in s.select('.front h1'): add(1, 'Home', 'Headline', el.get_text(' '), 40)
    for bk in s.select('.bk'):
        lab = bk.select_one('.bk-label').get_text(' ').strip()
        add(1, 'Home', f'Book cover: {lab}', bk.select_one('.bk-title').get_text(' '), 42, 'Has to fit on a small book cover.')
        sub = bk.select_one('.bk-sub')
        if sub: add(1, 'Home', f'Book cover: {lab}, small print', sub.get_text(' '), 90)

TOOLS_Q = ['deal', 'account', 'competition', 'territory', 'risk', 'rep', 'partner', 'olr', 'brief']
TOOLS_C = ['pipeline', 'quota', 'discount', 'commission']
NAMES = {'olr': 'Talent Review', 'deal': 'Deal Check', 'account': 'Account Check', 'competition': 'Competition Check', 'territory': 'Territory Check',
         'risk': 'Risk Check', 'rep': 'Rep Check', 'partner': 'Partner Check', 'brief': 'Brief Check', 'pipeline': 'Pipeline Check',
         'quota': 'Quota Check', 'discount': 'Discount Check', 'commission': 'Commission Check'}

shelf()
page_strings('ask/index.html', 'Ask Mark', 2)
chrome_strings()
for t in TOOLS_Q + TOOLS_C:
    src = open(f'{t}/index.html', encoding='utf-8').read()
    for sc in re.findall(r'<script>\n(.*?)</script>', src, flags=re.S): js_strings(NAMES[t], sc, 3)
    if t in TOOLS_C:
        for f in ('calc.js',): pass
    page_strings(f'{t}/index.html', NAMES[t], 4)
k = open('check.js', encoding='utf-8').read(); js_strings('Every question tool (shared)', k, 3)
c = open('calc.js', encoding='utf-8').read(); js_strings('Every calculator (shared)', c, 3)
# ── Deal and Pipeline write their result screens directly in the page, so read their code for sentences ──
def handwritten(path, page):
    raw = open(path, encoding='utf-8').read(); sc = '\n'.join(re.findall(r'<script>\n(.*?)</script>', raw, flags=re.S))
    for m in re.finditer(r'<h3>(Stuck on[^<]*)</h3>', sc): add(2, page, 'Card after the result: title', re.sub(r'\$\{[^}]*\}', '{…}', m.group(1)), 60)
    for m in re.finditer(r'<h3>Stuck on[^<]*</h3>\s*<p>(.*?)</p>', sc, flags=re.S):
        add(2, page, 'Card after the result: text', re.sub(r'<[^>]+>', '', m.group(1)).replace("\\'", "'"))
    dm = re.search(r'function dmText\(s\) \{\s*return `(.*?)`;\s*\}', sc, flags=re.S)
    if dm:
        t = re.sub(r"\$\{s\.win \? ` and my \$\{[^}]*\} win rate says I need \$\{[^}]*\}` : ''\}", ' and my {…} win rate says I need {…}', dm.group(1))
        add(2, page, 'Message people copy to DM you', re.sub(r'\$\{[^}]*\}', '{…}', t), None, 'Keep each {…}: the tool fills it in.')
    JSR = r"""'((?:[^'\\\n]|\\.)*)'|"((?:[^"\\\n]|\\.)*)"|`((?:[^`\\]|\\.)*)`"""
    for m in re.finditer(JSR, sc):
        v = next(x for x in m.groups() if x is not None)
        parts = [p.strip() for p in re.split(r'<[^>]+>', v) if p.strip()] if m.group(3) is not None else [v]
        for p in parts:
            p = re.sub(r'\$\{[^}]*\}', '{…}', p).replace("\\'", "'").replace('\\n', ' ').replace('&amp;', '&').strip()
            if len(p) < 14 or ' ' not in p or not re.search(r'[a-z]{3}', p): continue
            if re.search(r'[<`;=$]|\$\(|pointer: coarse|querySelector|=>|https?://|^[a-z.-]+( [a-z.-]+)*$', p): continue
            if p[0].islower() and len(p) < 25: continue
            if p.startswith("I'm Mark") or p.startswith('Send me one line'): continue
            if p.startswith('Mark, ran'): add(2, page, 'Message people copy to DM you', p, None, 'Keep each {…}: the tool fills it in.'); continue
            where = ('Fix for a weak answer' if re.match(r'(Get|Ask|Find|Bring) ', p) else
                     'Question, or a Pressure test question' if p.endswith('?') else 'Result screen text')
            add(3, page, where, p, 18 if len(p) <= 18 and ' ' in p and p[0].isupper() and not p.endswith('.') else None,
                'Keep each {…}: the tool fills it in.' if '{…}' in p else '')
handwritten('deal/index.html', 'Deal Check')
handwritten('pipeline/index.html', 'Pipeline Check')
page_strings('home.src.html', 'Home', 5)
page_strings('index.html', 'Home', 5)
page_strings('about/index.html', 'About', 6)
page_strings('stuff/index.html', 'Stuff I Like', 6)
page_strings('kits/index.html', 'Field Kits page', 7)
for d, n in [('seller', "The Seller's Field Kit"), ('kit', "The Manager's Field Kit"), ('leader', 'The Leadership Field Kit')]:
    page_strings(f'{d}/index.html', n, 7, 'article')
page_strings('notes/index.html', 'Field Notes', 8)
for p in sorted(glob.glob('notes/*/index.html')):
    t = BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser').h1.get_text(' ')
    page_strings(p, f'Field Note: {t}', 8, 'article')
page_strings('math/index.html', 'Sales Math', 8)
for p in sorted(glob.glob('math/*/index.html')):
    t = BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser').h1.get_text(' ')
    page_strings(p, f'Sales Math: {t}', 8, 'article')
page_strings('404.html', 'Wrong-turn page (404)', 9)

ORDER = {1: '1 · Home shelf', 2: '2 · Ask Mark and the card after each result', 3: '3 · Questions and verdicts', 4: '4 · Tool pages: intros, explanations, FAQs',
         5: '5 · Home page, rest', 6: '6 · About and Stuff I Like', 7: '7 · Field Kits', 8: '8 · Field Notes and Sales Math', 9: '9 · Everything else'}
for i, r in enumerate(ROWS): r['group'] = ORDER[r['prio']]
ROWS.sort(key=lambda r: (r['prio'], r['page']))
for i, r in enumerate(ROWS): r['id'] = f'QB-{i + 1:04d}'
json.dump(ROWS, open('/home/claude/copy_rows.json', 'w'), indent=1)
from collections import Counter
print(len(ROWS), 'rows'); [print(f'  {n:4}  {g}') for g, n in sorted(Counter(r['group'] for r in ROWS).items())]
