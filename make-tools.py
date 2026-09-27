#!/usr/bin/env python3
"""Builds rep/index.html, partner/index.html and territory/index.html from one template.
Run from the web root after editing copy below. Deal Check and Pipeline Check are hand-written."""
import json, os, re

BUILD = '2026-10-27.2100'
TOOLS = [
    ('Your number', '/quota/', 'Quota Check', 'The day the number lands'),
    ('Your number', '/quota-case/', 'Quota Case', 'When you need to push back'),
    ('Your number', '/territory/', 'Territory Check', 'Month one in a new territory'),
    ('Your number', '/commission/', 'Commission Check', 'When it closes'),
    ('Your number', '/discount/', 'Discount Check', 'When they ask you to sharpen the pencil'),
    ('Your team', '/pipeline/', 'Pipeline Check', 'Quarterly, before the review'),
    ('Your team', '/risk/', 'Risk Check', 'When coverage looks fine and you don\'t trust it'),
    ('Your team', '/rep/', 'Rep Check', 'When a rep is worrying you'),
    ('Your team', '/partner/', 'Partner Check', 'Before you renew the partnership'),
    ('Your team', '/olr/', 'Talent Review', 'Review season'),
    ('Your deal', '/deal/', 'Deal Check', 'Before you put it in commit'),
    ('Your deal', '/account/', 'Account Check', 'When you only know one person there'),
    ('Your deal', '/competition/', 'Competition Check', 'When you\'re not sure you\'re ahead'),
    ('Any meeting', '/brief/', 'Brief Check', 'When someone in the room can say no'),
]

def menu(current):
    groups, last = [], None
    for g, h, n, d in TOOLS:
        if g != last: groups.append([g, []]); last = g
        groups[-1][1].append(f'<a href="{h}"{" class=\"current\"" if h == current else ""}>{n}</a>')
    # two balanced columns: groups go left until the left holds at least half the items
    total = sum(len(i) for g, i in groups); left, right, n = [], [], 0
    for g, items in groups:
        (left if n < total / 2 else right).append((g, items)); n += len(items)
    col = lambda gs: '<div class="menu-col">' + ''.join(f'<div class="menu-g"><div class="menu-group">{g}</div>{"".join(items)}</div>' for g, items in gs) + '</div>'
    foot = '<div class="menu-foot"><a href="/">Home</a><a href="/math/">Sales Math</a><a href="/notes/">Field Notes</a><a href="/about/">About</a></div>'
    kit = '<a class="menu-kit" href="/kits/"><span class="pill">Free</span>The Field Kits (PDF)</a>'
    return f'<details class="menu"><summary><span class="chip">Tools ▾</span></summary><div class="menu-list">{kit}{col(left)}{col(right)}{foot}</div></details>'



def page(t):
    faq_html = ''.join(f'''    <details class="exp"><summary>{q}</summary>
      <div class="body">{a}</div></details>
''' for q, a in t['faq'])
    faq_ld = ',\n'.join(json.dumps({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}}) for q, a in t['faq'])
    bands = ''.join(f'''<section class="band" id="{i}">
  <div class="band-inner">
    <h2>{h}</h2>
{body}
  </div>
</section>

''' for i, h, body in t['bands'])
    mark = '<section class="band" id="about"></section>\n\n'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="https://quotabird.com/{t['slug']}/">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="icon" type="image/png" sizes="64x64" href="../favicon.png">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:url" content="https://quotabird.com/{t['slug']}/">
<meta property="og:title" content="{t['name']}: {t.get('ogh1', t['h1'])}">
<meta property="og:description" content="{t['ogdesc']}">
<meta property="og:site_name" content="QuotaBird">
<meta property="og:image" content="https://quotabird.com/card-{t['slug']}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{t['name']}: {t.get('ogh1', t['h1'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t['name']}: {t.get('ogh1', t['h1'])}">
<meta name="twitter:description" content="{t['ogdesc']}">
<meta name="twitter:image" content="https://quotabird.com/card-{t['slug']}.jpg">
<meta name="twitter:image:alt" content="{t['name']}: {t.get('ogh1', t['h1'])}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#FFFFFF">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#101418">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "WebApplication",
      "name": "{t['name']}",
      "url": "https://quotabird.com/{t['slug']}/",
      "applicationCategory": "BusinessApplication",
      "operatingSystem": "Any",
      "description": "{t['desc']}",
      "image": "https://quotabird.com/card-{t['slug']}.jpg",
      "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }},
      "isPartOf": {{ "@type": "WebSite", "name": "QuotaBird", "url": "https://quotabird.com/" }},
      "author": {{ "@id": "https://quotabird.com/#about" }}
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
{faq_ld}
      ]
    }}
  ]
}}
</script>
<link rel="stylesheet" href="../site.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BG9NR9GXQZ"></script>
<script src="../analytics.js" defer></script>
</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
  <div id="screen">
    <span class="overline tool-name">{t['name']}</span>
    <h1>{t['h1']}</h1>
    <p class="dek">{t['dek']}</p>
    <button class="btn btn-primary btn-lg btn-full" id="prep" type="button">{t['cta']}</button>
    <p class="startnote">5 taps · about a minute</p>
    <p class="pillars">{' · '.join(q['n'].title() for q in t['questions'])}</p></div>
</div>

{bands}{mark}<section class="band" id="faq" aria-labelledby="faq-h">
  <div class="band-inner">
    <h2 id="faq-h">Questions</h2>
{faq_html}  </div>
</section>

<footer class="sitefoot">
  <a href="/">QuotaBird</a> is a pile of free sales tools. I built them because they helped me, and maybe they'll help you.
  <p>Not affiliated with the U.S. government or Amazon.</p>
</footer>
<script src="../check.js"></script>
<script>
'use strict';
window.QB_BUILD = '{BUILD}';
{t['config']}
</script>
</body>
</html>
'''

# ────────────────────────────── REP CHECK ──────────────────────────────
REP = dict(
    slug='rep', name='Rep Check',
    title='Rep Check: Is It the Rep or the Territory?',
    desc='Is it the rep, the territory, a skill gap or an effort gap? Five questions for sales managers that look at the territory before the person.',
    ogdesc='Before you write them up, figure out what you inherited. Five questions, one minute, no names.',
    h1='Is it the rep, or the territory?',
    dek='Five questions to tell a rep problem from a territory problem, a skill gap, or somebody who\'s stopped trying.',
    cta='Check my rep',
    questions=[
        dict(k='patch', n='TERRITORY', q='Could a good rep make this number in this territory, on this plan?'),
        dict(k='customers', n='CUSTOMERS', q='Do customers choose to spend time with them? Do they get called back?'),
        dict(k='pipeline', n='PIPELINE', q="Is there pipeline that exists only because they're here?"),
        dict(k='craft', n='CRAFT', q="When they're in front of a customer, can they actually sell?"),
        dict(k='will', n='WILL', q='Are they still trying to win?'),
    ],
    bands=[
        ('how', 'Five questions, in this order', '''    <p class="lede">New managers usually start with "what's wrong with these reps?" I'd start with "what exactly did I inherit?" and go down the list below in order.</p>
    TERRITORY: Could a good rep make this number here? Account quality, installed base, the quota, the comp plan, the competitive situation, who has had the territory before. If three people failed in the same territory, start with the territory. If the answer here is no, nothing you do with the rep is going to matter.
    CUSTOMERS: Do customers choose them? Forget meeting count. Five real customer conversations beat fifteen calendar entries. The weird rep who skips internal meetings but has customers calling her may be doing more selling than the polished one with perfect CRM hygiene.
    PIPELINE: What exists because they're here? Separate inherited and renewal business from what they created. Ask where the pipeline came from, how old it is, whether it's moving, and what customer evidence makes it real. A seller can look fine today and leave nothing behind for next year.
    <p><strong>CRAFT: Can they sell?</strong> Prospect, discover, understand the customer, qualify, get to power, create urgency, get through procurement, close. This is the split between <em>can't do it</em> and <em>isn't doing it</em>. One you coach. The other you manage.</p>
    WILL: Are they still trying to win? Energy, ownership, follow-through, coachability. A rep who has decided the year is over stops doing the things that would have saved it. Usually the activity drops first, and the pipeline follows.'''),
        ('buckets', 'Four kinds of problem, and the one that isn\'t', '''    <p><strong>Good rep, bad situation.</strong> Fix the situation: the territory, the number, or the plan.</p>
    <p><strong>Good rep, skill gap.</strong> Coach them. Name the skill and work it, one deal at a time.</p>
    <p><strong>Capable rep, effort gap.</strong> Manage them. Expectations in writing, with dates.</p>
    <p><strong>Wrong rep, reasonable situation.</strong> Start the process. If they're the wrong rep, six more months won't fix it.</p>
    <p><strong>They're fine.</strong> Leave them alone. Don't invent a management problem because they don't love
      one-on-ones. Figure out what visibility you need and let them sell.</p>
    <p>The thing I'm trying to prevent here is six months of coaching a territory problem, or six months of blaming a territory because you don't want to deal with a rep problem. Figure out which one you've got.</p>
    Don't decide who's good and who's bad in your first few weeks. Sit with each rep and go through five real deals, and listen to how they talk about the customer. You can run each one through <a href="/deal/">Deal Check</a> while you're at it.'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ("Why does it never ask the rep's name?", 'It doesn\'t need one, and I don\'t want a tool that stores opinions about named people. Run it, have the conversation, and nothing gets written down.'),
        ('What do the verdicts mean?', "<strong>They're fine:</strong> leave them alone. <strong>The situation:</strong> good rep, bad territory, number or plan; fix that. <strong>Coach them:</strong> good rep, skill gap. <strong>Manage them:</strong> capable rep, effort gap; expectations and dates. <strong>Wrong rep:</strong> reasonable situation, wrong person. <strong>Not sure:</strong> too many sort-ofs; sit in five of their deals and run it again."),
        ('Why is TERRITORY the first question?', 'Start with the territory and the number before you decide the rep is broken. You\'ll make a different decision.'),
        ('Can I run it on myself?', 'Yes, and sellers should. If the territory answer is no, <a href="/territory/">Territory Check</a> makes that case to your manager with the sizing behind it.'),
    ],
    config='''CheckTool({
  slug: 'rep', name: 'Rep Check', url: 'https://quotabird.com/rep/',
  questions: [
    { k: 'patch',     n: 'TERRITORY',     q: 'Could a good rep make this number in this territory, on this plan?' },
    { k: 'customers', n: 'CUSTOMERS', q: 'Do customers choose to spend time with them? Do they get called back?' },
    { k: 'pipeline',  n: 'PIPELINE',  q: "Is there pipeline that exists only because they're here?" },
    { k: 'craft',     n: 'CRAFT',     q: "When they're in front of a customer, can they actually sell?" },
    { k: 'will',      n: 'WILL',      q: 'Are they still trying to win?' },
  ],
  weights: { patch: 24, customers: 20, pipeline: 20, craft: 20, will: 16 },
  capOnNo: false, count: false,
  // A diagnosis, not a score. The situation is checked before the person.
  verdict(a) {
    const no = (k) => a[k] === 'no', yes = (k) => a[k] === 'yes';
    const K = ['patch','customers','pipeline','craft','will'];
    if (K.every(yes))
      return { label: "They're fine", cls: 'ready', attack: 'Leave them alone.', sub: "Don't invent a management problem because they don't love one-on-ones. Decide what visibility you need and let them sell." };
    if (no('patch'))
      return { label: 'The situation', cls: 'prove', attack: 'Good rep, bad situation.', sub: 'Nobody makes a number in a territory that can\\'t produce one. Fix the territory, the number or the plan before you write anybody up.' };
    if (no('craft') && no('will'))
      return { label: 'Wrong rep', cls: 'dont', attack: 'Reasonable situation, wrong person.', sub: "They can't do it and they've stopped trying. Start the process. Six more months won't help them or the team." };
    if (no('craft'))
      return { label: 'Coach them', cls: 'proof', attack: 'Good rep, skill gap.', sub: "They're trying and it isn't working. Name the skill, sit in their deals, work it one opportunity at a time." };
    if (no('will') || no('customers') || no('pipeline'))
      return { label: 'Manage them', cls: 'prove', attack: 'Capable rep, effort gap.', sub: "They can sell. They aren't. Expectations in writing, with dates, and a conversation about whether they still want this." };
    return { label: 'Not sure', cls: 'proof', attack: "You don't know yet.", sub: 'Too many sort-ofs. Sit with them and go through five real opportunities, then run this again.' };
  },
  askedBy: 'Your VP will ask',
  grill: {
    patch: 'Has anyone ever made this number in that territory?',
    customers: 'Which customers would take their call tomorrow?',
    pipeline: 'What have they created this year that they didn\\'t inherit?',
    craft: 'Have you watched them run a customer meeting?',
    will: 'Have you asked them whether they still want to do this?',
  },
  moves: {
    patch: 'Size the territory yourself before the next one-on-one. If it can\\'t produce the number, say so up the chain.',
    customers: 'Ask which three customers would take their call tomorrow, then call one.',
    pipeline: 'Split their pipeline into inherited and created. Put the created number on paper.',
    craft: 'Sit in their next two customer meetings. Say nothing. Watch.',
    will: 'Ask them directly, this week, whether they still want to do this. Listen to the answer.',
  },
  noMove: 'Nothing. Tell them the forecast looks good and ask what they need from you.',
  handoff: (s) => s.label === 'The situation'
    ? { overline: 'It\\'s the territory', text: 'Send them Territory Check. Do the math before you turn it into a people argument.', href: '/territory/', label: 'Check my territory' }
    : { overline: 'Before you decide anything', text: "Sit with them and run their five biggest deals through Deal Check, and listen to how they answer. Ninety minutes of that beats a month of dashboards.", href: '/deal/', label: 'Check my deal' },
  mark: { title: (s) => 'Not sure it\\'s ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I once spent six months coaching a rep before I figured out it was the territory. Tell me what's going on with yours." },
  dm: (s) => `Mark, ran a rep through Rep Check. Verdict: ${s.label.toLowerCase()}. Weakest answer was ${s.weak.n.toLowerCase()}. Not sure I've got the right problem. Worth 20 minutes?`,
});''',
)

# ────────────────────────────── PARTNER CHECK ──────────────────────────────
PARTNER = dict(
    slug='partner', name='Partner Check',
    title='Partner Check: Is This Partner Doing Anything?',
    desc='Five questions that separate a real partnership from promises: sourced deals, a named account, an owner who gets paid, a plan with dates, and pull.',
    ogdesc='Before you renew the partnership, test it. Five questions, one minute, no names.',
    h1='Is this partner doing anything?',
    dek='Five questions that separate a real partnership from promises.',
    cta='Check my partner',
    questions=[
        dict(k='sourced', n='SOURCED', q="Have they brought you an opportunity you didn't find yourself?"),
        dict(k='accounts', n='ACCOUNTS', q='Is there a named account both sides are working right now?'),
        dict(k='owner', n='OWNER', q='Does someone on their side carry a number that includes you?'),
        dict(k='plan', n='PLAN', q='Is there a co-sell plan with dates on it, not a deck?'),
        dict(k='pull', n='PULL', q='Would they call you if you stopped calling them?'),
    ],
    bands=[
        ('how', 'What a real partner actually does', '''    <p class="lede">Everybody gets along. There have been plenty of meetings, maybe a joint slide deck. The question
      is whether anyone can point to the account where the two companies are actually trying to win something together.</p>
    SOURCED: Have they brought you anything? If they've never handed you a deal you didn't already have, you're working for them. One sourced deal is worth more than a year of joint webinars.
    ACCOUNTS: Is there a named account, right now? Not a target list. A customer, a requirement, two sellers who know each other's names. If nobody can name one, it's a partnership on paper.
    OWNER: Does someone on their side get paid when you win? Partnerships mostly run on comp plans. If nobody at the partner carries a number that includes you, every deal is a favor, and people run out of favors.
    PLAN: Is there a plan with dates? A plan is three accounts, two dates and who owns each one. If it takes a deck to explain, it probably isn't a plan.
    PULL: Would they call you first? Stop calling for two weeks and see what happens. A real partner will notice. Most won't.'''),
        ('verdicts', 'Four kinds of partner', '''    <p><strong>Real.</strong> Deals are moving with both names on them. Feed it.</p>
    All talk. Lots of activity, no deals. Most partnerships end up here and stay here.
    <p><strong>Neighbors.</strong> You get along. That's all that's happening.</p>
    <p><strong>Just promises.</strong> Plenty of meetings and co-branded slides, no deals. Stop
      spending time on it and say so.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('Does this work for the partner running it on me?', 'Yes. Run it on each other and compare answers. Where you disagree is where I\'d start.'),
        ('What about a partner that\'s strategic but not producing yet?', 'Then the answer to SOURCED and ACCOUNTS is no, and the tool will say so. "Strategic" is what people call a partnership before it\'s produced anything.'),
        ('Can I use it on a distributor or an SI?', 'Yes. The questions don\'t care which direction the paper flows. They care whether anyone on the other side is accountable for a deal with your name on it.'),
    ],
    config='''CheckTool({
  aside: (s, a) => ['accounts', 'pull'].some(k => a[k] && a[k] !== 'yes') ? { text: "Selling federal? fedhoo ranks which primes actually pass work to subs and which resellers hold the right vehicles.", href: 'https://fedhoo.com/?utm_source=quotabird&utm_medium=partner&utm_content=verdict', label: 'Find a better route on fedhoo' } : null,
  slug: 'partner', name: 'Partner Check', url: 'https://quotabird.com/partner/',
  questions: [
    { k: 'sourced',  n: 'SOURCED',  q: "Have they brought you an opportunity you didn't find yourself?" },
    { k: 'accounts', n: 'ACCOUNTS', q: 'Is there a named account both sides are working right now?' },
    { k: 'owner',    n: 'OWNER',    q: 'Does someone on their side carry a number that includes you?' },
    { k: 'plan',     n: 'PLAN',     q: 'Is there a co-sell plan with dates on it, not a deck?' },
    { k: 'pull',     n: 'PULL',     q: 'Would they call you if you stopped calling them?' },
  ],
  weights: { sourced: 24, owner: 22, accounts: 20, pull: 18, plan: 16 },
  verdict(a, total) {
    if (total >= 75) return { label: 'Real', cls: 'ready', attack: 'This one is real. Feed it.', sub: 'Protect the time you spend here from the partners below.' };
    if (total >= 55) return { label: 'All talk', cls: 'proof', attack: 'Lots of activity. No deals.', sub: 'Everybody is busy. Nothing closes. Most partnerships live here forever.' };
    if (total >= 35) return { label: 'Neighbors', cls: 'prove', attack: "You get along. That's all that's happening.", sub: 'Pick one account and one date, or stop pretending this is a partnership.' };
    return { label: 'Just promises', cls: 'dont', attack: "Lots of meetings. No deals.", sub: 'That\\'s the whole partnership. Say so, and put the time somewhere that produces.' };
  },
  askedBy: 'Your boss will ask',
  grill: {
    sourced: "What have they brought us that we didn't find ourselves?",
    accounts: "Name one account where we're both working the same deal.",
    owner: 'Who on their side gets paid when we win?',
    plan: "What's on the co-sell plan that has a date on it?",
    pull: 'When did they last call you first?',
  },
  moves: {
    sourced: 'Ask them for one opportunity this month. Their answer is the diagnosis.',
    accounts: 'Pick three accounts, get both sellers on one call, agree who does what by when.',
    owner: 'Find out whose comp plan includes you. If the answer is nobody, that\\'s the problem.',
    plan: 'Replace the deck with one page: three accounts, two dates, one owner each.',
    pull: 'Stop calling for two weeks. See what happens.',
  },
  noMove: 'Keep doing what you\\'re doing, and write down why it works before someone changes it.',
  handoff: (s) => s.total >= 55
    ? { overline: 'Is there a deal inside this partnership?', text: 'Run it through Deal Check. A real partner deal survives the same five questions any deal does.', href: '/deal/', label: 'Check my deal' }
    : { overline: 'How much of your number is leaning on them?', text: 'If this partner is in your coverage math, the math is wrong. Pipeline Check shows you by how much.', href: '/pipeline/', label: 'Check my pipeline' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I spent six years leading federal partner sales teams at AWS, and I sat on the partner side before that. Plenty of partnerships look great in the QBR and never produce anything. Tell me about yours." },
  dm: (s) => `Mark, ran a partner through Partner Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. Not sure what to do with it. Worth 20 minutes?`,
});''',
)

# ────────────────────────────── TERRITORY CHECK ──────────────────────────────
TERRITORY = dict(
    slug='territory', name='Territory Check',
    title='Territory Check: Does This Territory Suck?',
    desc='Can the territory make the number, or are you being asked to grow where nobody could? Five questions for sellers.',
    ogdesc='Before you sign up for the number, test the territory. Five questions, one minute, no account names.',
    h1='Does this territory suck?',
    dek='Five questions before you sign up for a number the territory may not be able to produce.',
    cta='Check my territory',
    questions=[
        dict(k='spend', n='SPEND', q='Is there enough addressable spend in the territory to make the number twice over?'),
        dict(k='accounts', n='ACCOUNTS', q="Can you name ten accounts you'd expect to buy this year?"),
        dict(k='base', n='BASE', q='Is there existing business to grow, not just logos to win?'),
        dict(k='access', n='ACCESS', q='Do you have a way in: relationships, partners, contract vehicles?'),
        dict(k='history', n='HISTORY', q='Has anyone made this number in this territory before?'),
    ],
    bands=[
        ('how', 'What a territory has to have', '''    <p class="lede">Your quota assumes a lot about your territory. Check those assumptions before you sign up for it.</p>
    SPEND: Is the money there twice over? Agency budgets, program lines, contract ceilings. If the total addressable spend isn't at least double the number, you're counting on share you have no real reason to expect.
    <p><strong>ACCOUNTS: Can you name ten?</strong> Not a list from the CRM. Ten accounts you personally expect to
      buy this year, with a reason for each. If you can't get to ten, your manager should hear that in January,
      not October.</p>
    BASE: Is there anything to grow? Installed base gives you something to build on. All new logos means starting from zero every year. Know which one you've got, and put the inherited number on paper so nobody counts it twice.
    ACCESS: Can you get in the door? A relationship, a partner who owns the account, a contract vehicle they already buy through. You need one route per account, or it's just a name on a list.
    <p><strong>HISTORY: Has anyone done it?</strong> Find the last person who had the territory. If nobody has ever made
      this number here, you're the experiment, and you should be paid like one.</p>'''),
        ('now', 'What to do with the verdict', '''    <p>A bad verdict won't get you out of the number, but it will get you a better conversation about it. Take it to your manager in the first month, with the sizing behind it, and ask for one of three things: a different territory, a different number, or a different plan for how the gap gets filled. Doing the math in January goes over a lot better than discovering it in Q4.</p>
    <p>A good verdict means the number's there, which puts it on you.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('Is this just a way to argue about quota?', 'It\'s a way to argue about quota with evidence. I\'ve never seen anyone win that argument on feelings.'),
        ('What if I\'m new and don\'t know the territory yet?', 'Then most answers will be sort of, and the verdict will say so. Run it again in 60 days and compare.'),
        ('What about the coverage math?', 'That\'s the other tool. Once you know the territory can produce, <a href="/pipeline/">Pipeline Check</a> tells you how much pipeline it has to produce.'),
    ],
    config='''CheckTool({
  aside: (s, a) => ['spend', 'access'].some(k => a[k] && a[k] !== 'yes') ? { text: "Selling federal? fedhoo shows what each agency in your territory actually spends, who's winning it, and what's expiring.", href: 'https://fedhoo.com/?utm_source=quotabird&utm_medium=territory&utm_content=verdict', label: 'Look up your territory on fedhoo' } : null,
  slug: 'territory', name: 'Territory Check', url: 'https://quotabird.com/territory/',
  questions: [
    { k: 'spend',    n: 'SPEND',    q: 'Is there enough addressable spend in the territory to make the number twice over?' },
    { k: 'accounts', n: 'ACCOUNTS', q: "Can you name ten accounts you'd expect to buy this year?" },
    { k: 'base',     n: 'BASE',     q: 'Is there existing business to grow, not just logos to win?' },
    { k: 'access',   n: 'ACCESS',   q: 'Do you have a way in: relationships, partners, contract vehicles?' },
    { k: 'history',  n: 'HISTORY',  q: 'Has anyone made this number in this territory before?' },
  ],
  weights: { spend: 24, accounts: 22, access: 20, base: 18, history: 16 },
  verdict(a, total) {
    if (total >= 75) return { label: 'Workable', cls: 'ready', attack: "The number is there. Now it's on you.", sub: 'Which is worse news than you were hoping for.' };
    if (total >= 55) return { label: 'Thin', cls: 'proof', attack: 'It can be done. Not by accident.', sub: 'The territory won\\'t carry you. Every account needs a plan.' };
    if (total >= 35) return { label: 'A stretch', cls: 'prove', attack: "Something structural is wrong, and it isn't you.", sub: 'Take this to your manager in month one, with the sizing behind it.' };
    return { label: 'Nobody could', cls: 'dont', attack: "You're being asked to grow where nobody could.", sub: 'Say so now, with the math. Not in Q4.' };
  },
  askedBy: 'Your manager will ask',
  grill: {
    spend: 'Where is the money in this territory, specifically?',
    accounts: 'Which ten accounts?',
    base: "What's the renewal and expansion number before any new logo?",
    access: 'How are you getting in the door?',
    history: "Who's made this number here before, and how?",
  },
  moves: {
    spend: 'Size the territory: agency budgets, program lines, contract ceilings. One page.',
    accounts: "Write the ten. If you can't get to ten, tell your manager now.",
    base: 'Separate inherited from created. Put the inherited number on paper.',
    access: 'Map one route per account: a relationship, a partner, or a vehicle.',
    history: 'Find the last person who had the territory. Buy them coffee.',
  },
  noMove: 'Build the plan for the ten accounts. The territory isn\\'t the problem.',
  handoff: (s, a) => (s.total >= 55 && a.spend !== 'no')
    ? { overline: 'Now the coverage math', text: (s.total < 75 ? "It's thin, but it might produce." : a.spend === 'yes' ? 'The territory can produce.' : 'The territory can probably produce, if the spend is really there.') + ' Pipeline Check tells you how much it has to.', href: '/pipeline/', label: 'Check my pipeline' }
    : { overline: 'Take it to your manager', text: "Their version of this question is Rep Check, and its first question is the territory. Send them that with your sizing.", href: '/rep/', label: 'Check my rep' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I've inherited the territory nobody could grow, and I've handed one out by mistake. If yours really can't make the number, I can help you make that case to your boss." },
  dm: (s) => `Mark, ran my territory through Territory Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. Want to make the case to my manager and not sure how. Worth 20 minutes?`,
});''',
)

OLR = dict(
    slug='olr', name='Talent Review Check',
    title='Talent Review Check: Can You Defend Your People? (OLR Prep)',
    desc="Five questions that test the assessment you're making for a rep in a talent review (OLR, at Amazon), then the room pressure-tests you.",
    ogdesc='Before you walk into calibration, test your assessment. Five questions, then the room pressure-tests you. No names, no ratings.',
    h1='Can you defend your people?',
    dek='Five questions about your assessment, before the room asks them.',
    cta='Test my assessment',
    questions=[
        dict(k='receipts', n='RECEIPTS', q='Can you name three things they delivered this year, each with a number on it?'),
        dict(k='ownership', n='OWNERSHIP', q="For the biggest one, can you say what wouldn't have happened without them?"),
        dict(k='scope', n='SCOPE', q='Can you explain why that was work at their level, not strong execution a level down?'),
        dict(k='how', n='HOW', q="For every leadership principle you'll cite, do you have one specific example?"),
        dict(k='next', n='NEXT', q="Can you name the harder thing you'd hand them next year, and why?"),
    ],
    bands=[
        ('room', 'What the room is testing', '''    <p class="lede">The form is the easy part of a talent review. The hard part is explaining a human being in sixty
      seconds to managers who don't know them, and having the explanation survive their questions.</p>
    <p>Every calibration room runs the same way: you propose, they probe, and the evaluation moves if you can't hold it. The managers across the table aren't hostile. They just haven't seen your rep's year, so all they can test is your assessment. What holds up in that room is receipts, ownership, scope, behavior and what you'd hand them next. Adjectives get picked apart.</p>
    <p><strong>RECEIPTS: Three things, each with a number.</strong> Amazon's own self-review now asks for three to five
      accomplishments with measurable outcomes. If you can't name three with a number on them, the room hears "had a
      good year," and "had a good year" loses to anyone who brought a spreadsheet.</p>
    <p><strong>OWNERSHIP: What wouldn't have happened without them?</strong> The first question in any room is how much of
      the outcome belongs to this person versus the team, the partner, or the market. If you can answer that in one
      sentence for the biggest win, the rest of the assessment is easier.</p>
    <p><strong>SCOPE: Their level, not the level below.</strong> "Strong L5 execution" is the polite way a room says no to
      an L6 assessment. What made the problem their-level sized: the ambiguity, the number of teams, the absence of a
      playbook, the decisions nobody else was going to make?</p>
    HOW: One example per principle. The room is going to ask for the example. If you're citing four principles, bring four examples, and drop the ones you can't back.
    NEXT: The harder thing. "I think she's a future VP" won't get you far. Say what problem you'd hand them next year that you wouldn't have handed them last year, and what they've already done that makes you sure.'''),
        ('bias', 'Check yourself before the room does', '''    <p class="lede">The review that gets torn apart is usually a decent rep and a manager who brought opinions instead of receipts.</p>
    <p><strong>Recency.</strong> How much of your judgment comes from the last sixty days?</p>
    <p><strong>Visibility.</strong> Would you reach the same conclusion if this person weren't in your meetings every week?</p>
    <p><strong>Halo.</strong> Remove their biggest win. What does the rest of the year look like?</p>
    <p><strong>Horns.</strong> Remove their worst month. Same question.</p>
    <p><strong>Style.</strong> Are you evaluating impact, or whether they communicate the way you do?</p>
    CONTEXT: Did a reorg, manager change, leave or territory change alter what they could reasonably deliver? Say it before somebody else does.
    <p>This grades your assessment, not your rep. It won't give you a rating. It asks the questions the room is going to ask before you get there.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('Does it predict a rating?', 'No, and it never will. It grades whether you can defend the assessment. Your company already has plenty of machinery for the rating.'),
        ('What is OLR?', "OLR is Amazon's annual talent review. Managers bring an assessment of each person and defend it in calibration with other managers. This is practice for the defending part."),
        ('Is this only for Amazon?', 'OLR is Amazon\'s name for it, and that\'s where most of the people who use these tools have sat. But every calibration room asks the same five things, whatever the company calls it. Read "leadership principle" as your organization\'s behavioral standard and the tool works the same.'),
        ('What does Pressure test do?', 'It plays the room. Three hard questions about your weakest answer. If you can\'t answer two of them, the assessment isn\'t ready. Better to find that out here.'),
        ('Why does it never ask the rep\'s name?', 'It doesn\'t need one, and I don\'t want a tool that stores opinions about named people. Run it, fix the assessment, and nothing gets written down.'),
    ],
    config='''CheckTool({
  slug: 'olr', name: 'Talent Review Check', url: 'https://quotabird.com/olr/',
  questions: [
    { k: 'receipts',  n: 'RECEIPTS',  q: 'Can you name three things they delivered this year, each with a number on it?' },
    { k: 'ownership', n: 'OWNERSHIP', q: "For the biggest one, can you say what wouldn't have happened without them?" },
    { k: 'scope',     n: 'SCOPE',     q: 'Can you explain why that was work at their level, not strong execution a level down?' },
    { k: 'how',       n: 'HOW',       q: "For every leadership principle you'll cite, do you have one specific example?" },
    { k: 'next',      n: 'NEXT',      q: "Can you name the harder thing you'd hand them next year, and why?" },
  ],
  weights: { receipts: 26, ownership: 22, scope: 20, how: 16, next: 16 },
  verdict(a, total) {
    if (total >= 75) return { label: 'Ready', cls: 'ready', attack: 'The room can test this. Let it.', sub: 'Bring the receipts in the order you would say them, and say the weakest one first.' };
    if (total >= 55) return { label: 'Not yet', cls: 'proof', attack: 'Your conclusion may be right. You haven\\'t documented enough to defend it.', sub: 'One more receipt on the weakest answer and this holds.' };
    if (total >= 35) return { label: 'A story', cls: 'prove', attack: "You're telling a story. The room wants receipts.", sub: 'Adjectives and impressions where outcomes, examples and artifacts should be.' };
    return { label: 'No receipts', cls: 'dont', attack: 'This won\\'t survive the first question.', sub: "It may still be a good rep. It isn't an assessment yet." };
  },
  askedBy: 'The room will ask',
  grill: {
    receipts: 'What are the three, with the numbers?',
    ownership: 'How much of that outcome belongs to them versus the team around them?',
    scope: 'What specifically makes that their-level work rather than strong execution a level down?',
    how: 'Give me the example for that principle.',
    next: 'What would you give them next year that you wouldn\\'t have given them last year?',
  },
  grillSet: {
    receipts: ['You said they had a strong year. Which three things, and what were the numbers?', 'Remove the biggest win. What does the rest of the year look like?', 'Which of those three would still be true if the market had gone the other way?'],
    ownership: ['What happened that wouldn\\'t have happened without them?', 'Who else touched that outcome, and what did they contribute?', "If I asked the partner or the customer who drove it, whose name would they say?"],
    scope: ['What made this their-level work rather than strong execution one level down?', 'How many teams did they have to move without authority over any of them?', 'What decision did they make that nobody had made before?'],
    how: ['Give me the example for the first principle you\\'re citing.', 'And the second one. Different example.', 'Which principle would you drop because you can\\'t back it, and why did it get in the draft?'],
    next: ['What harder problem have they already shown they can handle?', 'Where did they grow scope without being asked?', 'What feedback did they get this year, and what observable behavior changed?'],
  },
  grillBy: 'The room', grillLabel: 'Pressure test', fixLabel: 'Before the room',
  grillLines: { clean: 'Your assessment would survive.', one: 'Your assessment would mostly survive. One hole left.', bad: 'Your assessment wouldn\\'t survive.', cleanSub: 'Three questions from the room, three answers. Say the weakest receipt first.' },
  fix: {
    receipts: 'Write the three things down, each with its number, before you write anything else. If you can\\'t get to three, the assessment is the problem, not the rep.',
    ownership: 'For the biggest win, write one sentence starting "Without them, ...". If you can\\'t finish it, find the win where you can.',
    scope: 'Write what made the problem their-level sized: the teams, the ambiguity, the missing playbook, the decision nobody else would make.',
    how: 'Cut every principle you can\\'t attach an example to. An assessment with two backed principles beats one with six adjectives.',
    next: 'Name the harder assignment you would give them and the thing they already did that makes you sure. Potential is evidence, not a feeling.',
  },
  moves: {
    receipts: 'Write the three things, each with its number. If you can\\'t get to three, that\\'s the finding.',
    ownership: 'Write one sentence beginning "Without them, ..." for the biggest win.',
    scope: 'Write what made it their-level work: teams moved, ambiguity, no playbook, the decision nobody else would make.',
    how: 'Cut every principle without an example. Keep the ones you can prove.',
    next: 'Name next year\\'s harder assignment and the evidence that says they can carry it.',
  },
  noMove: 'Put the weakest receipt first when you present. It\\'s easier to defend once you\\'ve said it yourself.',
  handoff: (s) => s.total >= 75
    ? { overline: 'The assessment is ready. Is the year set up?', text: "Next year's assessment starts now. Is the rep in a territory that can produce one? Rep Check asks that first.", href: '/rep/', label: 'Check my rep' }
    : { overline: 'The fastest receipt', text: 'A deal you watched them run. Sit in their next customer meeting and go through it with Deal Check afterward.', href: '/deal/', label: 'Check my deal' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I've written glowing reviews that got taken apart in the room, and usually the problem was how I'd made the case. Tell me about yours." },
  dm: (s) => `Mark, ran a rep's talent review assessment through Talent Review Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. OLR is coming and I'm not sure it holds. Worth 20 minutes?`,
  dmGrill: (s, missed) => `Mark, ran a rep's talent review assessment through Talent Review Check and couldn't answer ${missed} of the room's 3 ${s.weak.n.toLowerCase()} questions. Verdict was ${s.label.toLowerCase()}. Want to tell me what you'd go fix first?`,
});''',
)

BRIEF = dict(
    slug='brief', name='Brief Check',
    title='Brief Check: Will Your Brief Survive the Room?',
    desc="Five questions about the doc, deck or QBR you're about to present, then the room pressure-tests you.",
    ogdesc="Will your brief survive the room? Brief Check finds it before the meeting does.",
    h1="Will your brief survive the room?",
    dek='Five questions about the doc, the deck or the QBR, before the meeting asks them.',
    cta='Check my brief',
    questions=[
        dict(k='point', n='POINT', q='Can you say in one sentence what you want them to decide, and why now?'),
        dict(k='receipts', n='RECEIPTS', q="For the three claims the argument depends on, do you have evidence that isn't your own team's opinion?"),
        dict(k='alternative', n='ALTERNATIVE', q='Have you dealt with the most credible other option, including doing nothing?'),
        dict(k='hole', n='HOLE', q='Do you know the weakest assumption in your own argument, and who in the room will find it?'),
        dict(k='ask', n='ASK', q='Is it completely clear what you need from them today, and who owns the next step?'),
    ],
    bands=[
        ('how', 'What the room goes after', '''    <p class="lede">Nobody in that room cares much about your deck. They're going after the assumptions underneath it, and most briefs die when somebody asks the question the author was hoping nobody would.</p>
    POINT: One sentence, and why now. If you can't say what you want the room to decide in one sentence, you don't have a point yet. Put the why-now in the same sentence, too. A room can agree with you and still do nothing.
    <p><strong>RECEIPTS: Evidence for the three claims it depends on.</strong> Not every claim. The three that, if
      false, take the recommendation down with them. Data, customer evidence, financials, documented behavior. And
      at least one piece that didn't come from your own team, because the room discounts everything that did.</p>
    ALTERNATIVE: What else could they do, including nothing? Why this instead of waiting? Why build instead of buy? Why you instead of them? Somebody in the room already likes another answer. Deal with it before they do.
    <p><strong>HOLE: Your own weakest assumption, and who will find it.</strong> If you know the weak spot, say it before somebody else does. If you don't, somebody whose incentives differ from yours will find it, and they won't be gentle.</p>
    <p><strong>ASK: What you need today, and who owns what next.</strong> A shocking number of decks survive thirty
      slides and end with no decision. Is this an FYI, a discussion, a recommendation or a decision? What resource,
      commitment or approval do you need before you leave the room? Who owns the next action, by when?</p>'''),
        ('sharks', 'Who is in the room', '''    <p class="lede">The questions change with the chair. After the verdict, pick who is across the table and
      the tool asks what they would ask.</p>
    <p><strong>Finance.</strong> What does it cost, what does it return, what is the downside case, and which single
      assumption drives most of the economics.</p>
    <p><strong>The executive.</strong> Why are you telling me this, what is the decision, why now, and what are you
      asking me to do.</p>
    <p><strong>The tech leader.</strong> What has to be true for this to work, what is the hardest dependency,
      and what are you hand-waving.</p>
    <p><strong>The sales leader.</strong> Has a customer actually said they want this, who pays, who decides, and
      what is stopping the deal today.</p>
    <p><strong>The skeptic.</strong> Whoever in the room is accountable for something you're not. They know
      something you don't. Find out what before the meeting.</p>
    <p>You don't upload anything, and the tool never sees the document. It just asks whether you could answer for it.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('What counts as a brief?', 'Anything you\'re about to argue for in front of people who can say no: a narrative doc, a strategy deck, a QBR, an account plan, a proposal, an investment memo, a capture review, or a recommendation you will make out loud. If it has a point and an ask, it\'s a brief.'),
        ('Is this only for sales?', 'No. It started with sales reviews, and the sales leader is one of the sharks. But a six-pager in front of a VP dies exactly the way a QBR does: on the question the author hoped nobody would ask.'),
        ('What does Pressure test do?', 'It plays the room. Pick who\'s across the table, and it asks three of their questions about your weakest answer, one at a time. You say honestly whether you could answer.'),
    ],
    config='''CheckTool({
  slug: 'brief', name: 'Brief Check', url: 'https://quotabird.com/brief/',
  questions: [
    { k: 'point',       n: 'POINT',       q: 'Can you say in one sentence what you want them to decide, and why now?' },
    { k: 'receipts',    n: 'RECEIPTS',    q: "For the three claims the argument depends on, do you have evidence that isn't your own team's opinion?" },
    { k: 'alternative', n: 'ALTERNATIVE', q: 'Have you dealt with the most credible other option, including doing nothing?' },
    { k: 'hole',        n: 'HOLE',        q: 'Do you know the weakest assumption in your own argument, and who in the room will find it?' },
    { k: 'ask',         n: 'ASK',         q: 'Is it completely clear what you need from them today, and who owns the next step?' },
  ],
  weights: { point: 24, receipts: 22, hole: 20, alternative: 18, ask: 16 },
  verdict(a, total) {
    if (total >= 75) return { label: 'Room ready', cls: 'ready', attack: 'Your argument is clear and the claims have receipts.', sub: 'Lead with the hole. Say the weak spot before somebody else does.' };
    if (total >= 55) return { label: 'A fight', cls: 'proof', attack: "Your recommendation may be sound. You've left an opening.", sub: 'They will find it. Better you find it first.' };
    if (total >= 35) return { label: 'Shark food', cls: 'prove', attack: "You're relying on assumptions, vague impact, or an unclear ask.", sub: 'The room won\\'t argue with you. It will just move on.' };
    return { label: 'No point', cls: 'dont', attack: "There isn't a decision in this brief yet.", sub: 'Find the one sentence first. Everything else is formatting.' };
  },
  askedBy: 'The room will ask',
  grill: {
    point: "You have twenty seconds. What's the point?",
    receipts: 'Where did that number come from?',
    alternative: "Why shouldn't we just do nothing?",
    hole: "What's the sentence in this brief you hope nobody challenges?",
    ask: 'What exactly do you need from me today?',
  },
  grillSet: {
    point: ["You have twenty seconds. What's the point?", 'I read the whole thing. What exactly are you recommending?', 'If I remember one sentence tomorrow, what should it be?'],
    receipts: ['Where did that number come from? Actual, forecast, modeled, or anecdotal?', "Give me one piece of evidence that didn't come from your own team.", 'Revenue went up. And? Adoption grew. And? Customers asked. And?'],
    alternative: ["Why shouldn't we just do nothing for six months?", "What's the cheapest reasonable alternative, and why is it wrong?", 'What would someone who disagrees with you recommend instead?'],
    hole: ["What's the sentence in this brief you hope nobody challenges?", 'Which assumption, if false, takes the recommendation down with it?', 'Which number are you least confident in?'],
    ask: ['Is this an FYI, a discussion, a recommendation, or a decision?', 'What exactly do you need from me before you leave this room?', 'Who owns the next action, and by when?'],
  },
  sharks: {
    finance:   { name: 'Finance',              qs: { point: ['What does this cost?', "What's the return, and over what period?", "What's the downside case?"], receipts: ['Which assumption drives most of the economics?', 'Is that number actual, forecast, or modeled?', "What's the denominator?"], alternative: ['What does doing nothing cost us?', "What's the cheapest version of this that gets 80% of the value?", 'Why is that not good enough?'], hole: ['Which number would you least like me to check?', 'What happens to the case if that number is half?', 'What did you leave out of the model?'], ask: ['How much, when, and from whose budget?', 'What do you need me to approve today versus later?', 'What can you deliver with half of it?'] } },
    executive: { name: 'The executive',        qs: { point: ['Why are you telling me this?', "What's the decision?", 'Why now?'], receipts: ['Who else believes this besides your team?', 'Has a customer said this, or have we inferred it?', 'How recent is that?'], alternative: ["What's the alternative you're not recommending, and why?", 'Why not wait a quarter?', 'Who else has tried this?'], hole: ["What's the question you're hoping I don't ask?", 'What would make you wrong?', "What's the thing you're least sure of?"], ask: ['What are you asking me to do?', 'What happens if I say no?', 'Who owns this after today?'] } },
    technical: { name: 'The tech leader', qs: { point: ['What has to be true technically for this to work?', "What's the one-line architecture?", 'What are you hand-waving?'], receipts: ['Has this been built, or is this a diagram?', 'What did the prototype actually show?', "What's the failure mode you've seen so far?"], alternative: ['Why build instead of buy?', "What's the boring option, and why not that?", 'What did the last team that tried this learn?'], hole: ["What's the hardest dependency?", "What's the assumption about scale that nobody's tested?", 'What breaks first?'], ask: ['How many people, for how long?', 'What do you need from my team?', "What's the first milestone I can check?"] } },
    sales:     { name: 'The sales leader',     qs: { point: ['What does this do for the number?', 'Which deals does this move, by name?', 'Why this quarter?'], receipts: ['Has a customer actually said they want this?', 'Who pays, and who decides?', "What's stopping the deal today?"], alternative: ["What do we lose if we sell what we've got?", "What's the competitor doing instead?", 'Why not a partner?'], hole: ["Which deal is this really about, and what's its problem?", "What's the customer objection you haven't answered?", "What's the price?"], ask: ['What do you need from sales?', 'When can I put it in a forecast?', 'Who carries the number?'] } },
    skeptic:   { name: 'The skeptic',          qs: { point: ["What's the real reason you want this?", "What problem does this solve that we didn't have last year?", "Whose idea was this, and what do they get?"], receipts: ['What evidence would change your mind?', "What's the best argument against this?", 'Who disagrees, and why are they wrong?'], alternative: ['What did the alternative look like before you wrote it to lose?', 'Why is doing nothing not the answer?', 'What would you recommend if this were someone else\\'s idea?'], hole: ["What's the sentence you hope nobody challenges?", "What's the assumption you haven't been able to prove?", 'What are you not telling this room?'], ask: ['What are you actually asking for?', "What's the smallest commitment that tests this?", 'What will you show us in ninety days?'] } },
  },
  sharkPrompt: "Who's across the table?",
  grillBy: 'The room', grillLabel: 'Pressure test', fixLabel: 'Before the meeting',
  grillLines: { clean: 'Your brief would survive.', one: 'Your brief would mostly survive. One hole left.', bad: 'Your brief wouldn\\'t survive.', cleanSub: 'Three questions, three answers. Lead with the hole anyway.' },
  fix: {
    point: 'Write the one sentence: what you want them to decide, and why now. Put it at the top. If it takes two sentences, you have two briefs.',
    receipts: 'For each of the three load-bearing claims, write where the evidence came from and how old it is. Cut any claim that only your own team believes.',
    alternative: 'Write the alternative someone in the room already prefers, in their words, then why it falls short. Include doing nothing.',
    hole: 'Name the weakest assumption in one line and put it in the brief yourself, with what you would do if it proved false.',
    ask: 'End with a decision box: what you need, from whom, by when, and who owns the next action.',
  },
  moves: {
    point: 'Write the one sentence: what to decide, and why now. Put it first.',
    receipts: 'For the three load-bearing claims, write the source and its date. Cut what only your team believes.',
    alternative: "Write the alternative the room already prefers, in their words, and why it's not enough.",
    hole: 'Name your weakest assumption in the brief before they do.',
    ask: 'End with what you need, from whom, by when, and who owns what next.',
  },
  noMove: 'Say your weakest assumption out loud in the first minute. Then the argument happens on your terms.',
  handoff: (s) => s.total >= 75
    ? { overline: 'If the brief is about a deal', text: 'Somebody\\'s going to ask whether the deal underneath it is real. Deal Check will tell you before they do.', href: '/deal/', label: 'Check my deal' }
    : { overline: 'If the brief is about the number', text: 'Vague impact usually means the coverage math is missing. Pipeline Check puts a number on it.', href: '/pipeline/', label: 'Check my pipeline' },
  mark: { title: (s) => 'Stuck on the ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I've written docs that got shredded and a few that got funded. The bad ones usually had a question I hadn't asked myself. Tell me about yours if you want." },
  dm: (s) => `Mark, ran a brief through Brief Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is the ${s.weak.n.toLowerCase()}. Meeting is coming and I'm not sure it holds. Worth 20 minutes?`,
  dmGrill: (s, missed) => `Mark, ran a brief through Brief Check and couldn't answer ${missed} of the room's 3 questions about the ${s.weak.n.toLowerCase()}. Verdict was ${s.label.toLowerCase()}. Want to tell me what you'd go fix first?`,
});''',
)

# ────────────────────────────── ACCOUNT CHECK ──────────────────────────────
ACCOUNT = dict(
    slug='account', name='Account Check',
    title='Account Check: Do You Know Your Customer?',
    desc='Five questions that tell you whether you know the account or only the opportunity in front of you: mission, money, power, incumbents, how they buy.',
    ogdesc='Do you know your customer? Five questions, one minute, no names.',
    h1='Do you know your customer?',
    dek="Five questions. They'll show you where you're single-threaded.",
    cta='Check my account',
    questions=[
        dict(k='mission', n='MISSION', q='Can you say what this account is trying to get done this year, in their words?'),
        dict(k='money', n='MONEY', q='Do you know where their money comes from and when it moves, beyond your deal?'),
        dict(k='power', n='POWER', q='Have you met someone who matters beyond the deal in front of you?'),
        dict(k='incumbent', n='INCUMBENT', q='Do you know who already owns the relationships, the contracts and the workloads?'),
        dict(k='path', n='PATH', q='Do you know how this account actually buys, and who runs that process?'),
    ],
    bands=[
        ('how', 'Do you know the account, or one deal?', '''    <p class="lede">Deal Check asks whether one opportunity is real. Account Check asks whether you know the customer beyond that deal. You'll find out which one you have the day your contact leaves.</p>
    MISSION: What are they trying to get done? Not what you sell them. What the agency, the program or the business unit has to accomplish this year, in words they'd recognize. If all you can describe is what they're buying from you, you know your deal and not much else.
    MONEY: Where does it come from, beyond your deal? Appropriations, program lines, colors of money, fiscal calendars, the budget office. If you know how their money moves, you hear about deals before they exist. If you only know the money for your deal, you'll probably hear about the next one from a competitor's press release.
    POWER: Who matters beyond this deal? Being single-threaded is the most common way a good account goes quiet. If every conversation runs through one person, you're one promotion or one reorg away from starting over.
    INCUMBENT: Who already owns it? The relationships, contracts and workloads already belong to somebody. Know who, and what they stand to lose, before you call it a competition.
    PATH: How do they actually buy? The contracting office, the vehicles they use, the approvals, the people who run the process. It's usually the same for the next deal, so it's worth learning properly the first time.'''),
        ('verdicts', 'Four kinds of coverage', '''    <p><strong>Mapped.</strong> You know the mission, the money, the people and the process. Now find the next deal
      before anyone else does.</p>
    Half mapped. You know the parts your deal touches. Fill in the gaps before a reorg forces you to.
    One thread. Everything runs through one person, and that's a risk. Get introduced upward and sideways this month.
    <p><strong>A contact.</strong> You know one person. That's not an account yet.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('How is this different from Deal Check?', 'Deal Check is about one opportunity: is it real, will it close. Account Check is about the customer it lives in: do you know enough about them to find the next deal, survive a reorg, or beat the incumbent. I\'ve watched good sellers get blindsided that way, with a real deal in an account they didn\'t really know.'),
        ('Is this only for federal?', 'The questions were written with agencies in mind, where mission, colors of money and contract vehicles are everything. But every enterprise account has a mission, a budget process, an incumbent and a way it buys. Read the words that way and it works the same.'),
    ],
    config='''CheckTool({
  aside: (s, a) => ['incumbent', 'money'].some(k => a[k] && a[k] !== 'yes') ? { text: "Selling federal? fedhoo shows the agency's current contracts, who holds them, and what it spends.", href: 'https://fedhoo.com/?utm_source=quotabird&utm_medium=account&utm_content=verdict', label: 'Look up the agency on fedhoo' } : null,
  slug: 'account', name: 'Account Check', url: 'https://quotabird.com/account/',
  questions: [
    { k: 'mission',   n: 'MISSION',   q: 'Can you say what this account is trying to get done this year, in their words?' },
    { k: 'money',     n: 'MONEY',     q: 'Do you know where their money comes from and when it moves, beyond your deal?' },
    { k: 'power',     n: 'POWER',     q: 'Have you met someone who matters beyond the deal in front of you?' },
    { k: 'incumbent', n: 'INCUMBENT', q: 'Do you know who already owns the relationships, the contracts and the workloads?' },
    { k: 'path',      n: 'PATH',      q: 'Do you know how this account actually buys, and who runs that process?' },
  ],
  weights: { power: 24, money: 22, mission: 20, incumbent: 18, path: 16 },
  verdict(a, total) {
    if (total >= 75) return { label: 'Mapped', cls: 'ready', attack: 'You know the account, not just the deal.', sub: 'Now find the next one before anyone else does.' };
    if (total >= 55) return { label: 'Half mapped', cls: 'proof', attack: 'You know the parts your deal touches.', sub: 'Fill in the gaps before a reorg forces you to.' };
    if (total >= 35) return { label: 'One thread', cls: 'prove', attack: 'Everything runs through one person.', sub: "Everything runs through one person, and that's a risk. Get introduced upward and sideways this month." };
    return { label: 'A contact', cls: 'dont', attack: 'You know one person. That\\'s a contact.', sub: 'Start with the mission and the money. The people are easier to figure out after that.' };
  },
  askedBy: 'Your boss will ask',
  grill: {
    mission: 'What is this account trying to get done this year, in their words?',
    money: 'Where does their money come from, and when does it move?',
    power: 'Who have you met who matters beyond this deal?',
    incumbent: 'Who owns the relationships, the contracts and the workloads today?',
    path: 'How does this account buy, and who runs it?',
  },
  moves: {
    mission: 'Find the strategic plan, the budget justification or the all-hands deck. Read it. Write one sentence.',
    money: 'Find the program line and the fiscal calendar. Know when money moves before it does.',
    power: 'Ask your one contact for one introduction, upward or sideways, this week.',
    incumbent: 'List who owns the contracts and the workloads, and what each would lose if you won.',
    path: 'Find the contracting office and the vehicle they used last time. Ask how the last buy happened.',
  },
  noMove: 'Write it down while you still know it. Reorgs have a way of erasing account knowledge.',
  handoff: (s) => s.total >= 55
    ? { overline: 'Now the deal inside it', text: 'You know the account. Is the opportunity in it real? Deal Check asks the five questions your manager will.', href: '/deal/', label: 'Check my deal' }
    : { overline: 'Before you build the account', text: "Can the territory it sits in make the number at all? Territory Check answers that before you spend a year here.", href: '/territory/', label: 'Check my territory' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I've built accounts starting from one contact, and I've watched \\"mapped\\" accounts fall apart after one reorg. Tell me what you've got and I'll tell you where I'd start." },
  dm: (s) => `Mark, ran an account through Account Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. Not sure where to start. Worth 20 minutes?`,
});''',
)

# ────────────────────────────── RISK CHECK ──────────────────────────────
RISK = dict(
    slug='risk', name='Risk Check',
    title='Risk Check: Are Two Deals Carrying Your Year?',
    desc='Coverage says whether you have enough pipeline. This says how fragile it is: concentration, aging, next steps, timing and creation.',
    ogdesc='Are two deals carrying your year? Five questions, one minute, no deal names.',
    h1='Are two deals carrying your year?',
    dek='Five questions about the shape of your pipeline, not the size.',
    cta='Check my risk',
    questions=[
        dict(k='spread', n='SPREAD', q='Would you still make the number if your biggest deal slipped a quarter?'),
        dict(k='motion', n='MOTION', q='Has every deal in commit moved stage in the last sixty days?'),
        dict(k='next', n='NEXT', q='Does every commit deal have a customer action on the calendar, not just yours?'),
        dict(k='timing', n='TIMING', q='Is at least half of it due before the last month of the period?'),
        dict(k='fresh', n='FRESH', q='Did you create at least a quarter of it this quarter?'),
    ],
    bands=[
        ('how', 'Five ways a covered pipeline falls over', '''    <p class="lede">Pipeline Check asks whether you have enough. This asks whether it would survive a bad week. You can be at 4X and one slipped deal away from missing the year.</p>
    <p><strong>SPREAD: What if the big one slips?</strong> If a third of the number sits in one or two deals, your
      forecast is a bet on one customer's procurement calendar. Managers can't see this in the coverage ratio, which is
      why they ask about it in the review.</p>
    MOTION: Is it moving? A deal that hasn't changed stage in sixty days is parked, whatever stage the CRM says, and parked deals leave the forecast all at once, usually in the last week of the quarter.
    NEXT: Whose calendar is the next step on? If you're the only one who scheduled it, it's a task on your list. You want the customer to have put it on their calendar, and if none of your commit deals have that, I'd worry.
    TIMING: When is it due? If most of the number lands in the last month of the period, you've built a year that only December can save. Federal money makes it worse, because a September close has nowhere to slip.
    FRESH: Are you still creating? Pipeline you inherited or carried over runs out. If a quarter of what you're carrying wasn't created this quarter, next year is already in trouble.'''),
        ('verdicts', 'Four states of a pipeline', '''    <p><strong>Sturdy.</strong> Spread out, moving, with customers on the calendar. Go get the coverage number too.</p>
    Lopsided. There's one weakness, so fix it before the review finds it.
    <p><strong>Fragile.</strong> A slip or a quiet customer takes you off the number. Re-underwrite the commit deals now.</p>
    Looks covered. I wouldn't trust it. Rebuild it from the customers up.'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('I\'m at 4X coverage. Why does this say fragile?', 'Coverage only tells you how much. Four times the number in two deals that haven\'t moved since spring is a lot less than it looks. Run Pipeline Check for the size and this for the shape.'),
        ('Should a manager run this on the team?', 'Yes, deal by deal is even better. They\'re the questions a good forecast call asks anyway, so you might as well answer them first.'),
    ],
    config='''CheckTool({
  slug: 'risk', name: 'Risk Check', url: 'https://quotabird.com/risk/',
  questions: [
    { k: 'spread', n: 'SPREAD', q: 'Would you still make the number if your biggest deal slipped a quarter?' },
    { k: 'motion', n: 'MOTION', q: 'Has every deal in commit moved stage in the last sixty days?' },
    { k: 'next',   n: 'NEXT',   q: 'Does every commit deal have a customer action on the calendar, not just yours?' },
    { k: 'timing', n: 'TIMING', q: 'Is at least half of it due before the last month of the period?' },
    { k: 'fresh',  n: 'FRESH',  q: 'Did you create at least a quarter of it this quarter?' },
  ],
  weights: { spread: 24, next: 22, motion: 20, fresh: 18, timing: 16 },
  verdict(a, total) {
    if (total >= 75) return { label: 'Sturdy', cls: 'ready', attack: 'Spread out, moving, customers on the calendar.', sub: 'Now check the coverage number too. A well-spread pipeline can still be too small.' };
    if (total >= 55) return { label: 'Lopsided', cls: 'proof', attack: 'One weakness, and it\\'s the one the review will find.', sub: 'Fix the weakest answer before someone asks about it.' };
    if (total >= 35) return { label: 'Fragile', cls: 'prove', attack: 'A slip or a quiet customer takes you off the number.', sub: 'Re-underwrite every commit deal this week. Whose calendar is the next step on?' };
    return { label: 'Won\\'t hold', cls: 'dont', attack: 'It looks like coverage, but it\\'s mostly hope.', sub: 'Rebuild it from the customers up, starting with the deals that haven\\'t moved.' };
  },
  askedBy: 'Your boss will ask',
  grill: {
    spread: 'What happens to the number if the big one slips a quarter?',
    motion: 'Which commit deals haven\\'t changed stage since last quarter?',
    next: "Which commit deals have a customer action on the customer's calendar?",
    timing: 'How much of the number lands in the last month?',
    fresh: 'How much of this did you create this quarter?',
  },
  moves: {
    spread: 'Write the number without your biggest deal. That\\'s the plan you\\'re actually running.',
    motion: 'Move every deal that hasn\\'t changed stage in sixty days back a stage, today. Then work the ones that argue.',
    next: 'For each commit deal, get one customer action onto their calendar this week or move it out of commit.',
    timing: 'Pull one deal into an earlier month, or accept that the year is a December bet and tell your manager so.',
    fresh: 'Block two mornings this week for creation. Nothing else fixes a crater.',
  },
  noMove: 'Keep the shape. Now check the size: run the coverage math with your real win rate.',
  handoff: (s) => ({ overline: 'Shape checked. Now the size.', text: 'This checked the shape of your pipeline. Pipeline Check looks at whether there\\'s enough of it.', href: '/pipeline/', label: 'Check my pipeline' }),
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I once forecast a year on two deals and watched both slip the same week. Send me the shape of the pipeline, no customer names or dollars." },
  dm: (s) => `Mark, ran my pipeline through Risk Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. Coverage looks fine and I don't trust it. Worth 20 minutes?`,
});''',
)

# ────────────────────────────── COMPETITION CHECK ──────────────────────────────
COMPETITION = dict(
    slug='competition', name='Competition Check',
    title='Competition Check: Why You and Not Them?',
    desc='Five questions that tell you whether the incumbent, the competitor, or doing nothing is beating you right now.',
    ogdesc='Why you and not them? Five questions, one minute, no names.',
    h1='Why you and not them?',
    dek='Five questions that tell you whether the incumbent, or doing nothing, is beating you.',
    cta='Check my position',
    questions=[
        dict(k='nothing', n='NOTHING', q='Do you know what it costs them to do nothing, in their numbers?'),
        dict(k='switch', n='SWITCH', q='Do you know what it costs them to leave the incumbent, and who feels it?'),
        dict(k='preference', n='PREFERENCE', q='Has the customer told you, unprompted, why they would prefer you?'),
        dict(k='proof', n='PROOF', q='Do you have proof only you can show them: a reference, a pilot, a result?'),
        dict(k='access', n='ACCESS', q='Do you know who at the customer the competitor already owns?'),
    ],
    bands=[
        ('how', 'Where deals really get lost', '''    <p class="lede">Most of the deals I've lost, I lost to nothing. The customer kept what they had, the money went somewhere else, the project waited a year. So this checks whether you're beating nothing before it checks anybody else.</p>
    NOTHING: What happens if they do nothing? If the answer is "not much," doing nothing is free and free usually wins. Sellers skip this because the answer lives in the customer's world, not ours.
    SWITCH: What does leaving cost them? Incumbents mostly win because changing is a pain: retraining, migration, the person whose job is the current system. Know that cost and who carries it, or you'll lose to someone who never showed up to a meeting.
    PREFERENCE: Have they said it? Not "we like your solution." An unprompted reason, in their words, why you instead of the alternative. Until you've heard it, you're one column in their comparison spreadsheet.
    PROOF: What can only you show? A reference they can call, a pilot in their environment, a result at a customer they respect. Anybody can make claims. Something they can check is a lot harder for the incumbent to match.
    ACCESS: Who does the competitor own? Somewhere in the account there's a person the other side has been having lunch with for three years. Find out who, or you'll find out in the loss review.'''),
        ('verdicts', 'Four positions', '''    <p><strong>Preferred.</strong> They've told you why, you can prove it, and you know the cost of nothing. Close.</p>
    In the mix. You're a real option, but so is something else. Find the reason they'd pick you and get it in their words.
    <p><strong>Behind.</strong> The incumbent or the competitor has something you don't: access, proof, or a friend.
      Name it before you spend another quarter here.</p>
    Nothing wins. Doing nothing is beating you. Until it costs them something they can count, they'll keep doing nothing.'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('What if there\'s no competitor?', 'There\'s always one: doing nothing. Most deals that are "uncontested" are lost to the status quo, which is why the first question is about the cost of inaction rather than a named rival. Answer it honestly and the tool will tell you whether nothing is winning.'),
        ('Is this a battlecard?', 'No. Battlecards are about the competitor. This is about the customer: what happens if they do nothing, what switching costs, what they\'ve actually said, what you can prove, and who the other side already knows.'),
    ],
    config='''CheckTool({
  aside: (s, a) => ['switch', 'access'].some(k => a[k] && a[k] !== 'yes') ? { text: "Selling federal? fedhoo shows who holds the incumbent contract, what it's worth, and when it ends.", href: 'https://fedhoo.com/?utm_source=quotabird&utm_medium=competition&utm_content=verdict', label: 'Look up the incumbent on fedhoo' } : null,
  slug: 'competition', name: 'Competition Check', url: 'https://quotabird.com/competition/',
  questions: [
    { k: 'nothing',    n: 'NOTHING',    q: 'Do you know what it costs them to do nothing, in their numbers?' },
    { k: 'switch',     n: 'SWITCH',     q: 'Do you know what it costs them to leave the incumbent, and who feels it?' },
    { k: 'preference', n: 'PREFERENCE', q: 'Has the customer told you, unprompted, why they would prefer you?' },
    { k: 'proof',      n: 'PROOF',      q: 'Do you have proof only you can show them: a reference, a pilot, a result?' },
    { k: 'access',     n: 'ACCESS',     q: 'Do you know who at the customer the competitor already owns?' },
  ],
  weights: { nothing: 24, preference: 22, proof: 20, switch: 18, access: 16 },
  verdict(a, total) {
    if (total >= 75) return { label: 'Preferred', cls: 'ready', attack: "They've told you why, and you can prove it.", sub: 'Close it before the incumbent finds a friend.' };
    if (total >= 55) return { label: 'In the mix', cls: 'proof', attack: "You're a real option. So is something else.", sub: 'Find the reason they would pick you and get it in their words.' };
    if (total >= 35) return { label: 'Behind', cls: 'prove', attack: 'The other side has something you don\\'t.', sub: 'Name it: access, proof, or a friend. Then decide whether to spend another quarter here.' };
    return { label: 'Nothing wins', cls: 'dont', attack: "Doing nothing is beating you, and it isn't even trying.", sub: "Until doing nothing costs them something they can count, they're going to keep doing nothing." };
  },
  askedBy: 'Your boss will ask',
  grill: {
    nothing: 'What does it cost them to do nothing this year?',
    switch: 'What does it cost them to leave what they have, and who takes the hit?',
    preference: 'What did they say, in their words, about why they would pick us?',
    proof: 'What can we show them that the incumbent cannot?',
    access: 'Who does the other side already have in the account?',
  },
  moves: {
    nothing: "Ask the customer what happens if they do nothing this year. Write the number down in their words.",
    switch: 'List what leaving the incumbent costs them and who carries each cost. Then address the person, not the cost.',
    preference: 'Ask one question on the next call: what would make you choose us over the alternative? Then stop talking.',
    proof: 'Line up one reference they can call this month, or one pilot in their environment. Not a deck.',
    access: 'Find out who the competitor knows in the account. Ask your champion; they know.',
  },
  noMove: 'You\\'re preferred. Write down why, in their words, so the reason survives the next reorg.',
  handoff: (s) => s.total >= 55
    ? { overline: 'Now the deal itself', text: 'Where you stand against them is one thing. Whether the deal is real is another, and that\\'s Deal Check.', href: '/deal/', label: 'Check my deal' }
    : { overline: 'Do you know your customer?', text: 'Being behind usually means the other side knows the account better. Account Check finds where.', href: '/account/', label: 'Check my account' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I've lost to incumbents I never saw coming, and to customers who decided to do nothing, more often than I like to admit. Tell me what you're up against." },
  dm: (s) => `Mark, ran a deal through Competition Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. Not sure I'm ahead. Worth 20 minutes?`,
});''',
)

for t in (REP, PARTNER, TERRITORY, OLR, BRIEF, ACCOUNT, RISK, COMPETITION):
    os.makedirs(t['slug'], exist_ok=True)
    html = page(t)
    assert '—' not in html and '–' not in html, t['slug']
    open(f"{t['slug']}/index.html", 'w').write(html)
    print(t['slug'], len(html))


# ────────────────────────────── FIELD NOTES ──────────────────────────────
# Short reads in Mark's voice. Each ends with the tool that does the math.
# Add a note here, run the script, commit notes/<slug>/index.html.
NOTES = [
    dict(slug='prove-the-quota-is-crazy', title='Your quota is crazy. Now prove it.',
         dek="Saying it feels too high has never moved a number. Math sometimes does.",
         body='''    <p class="lede">Saying the quota feels too high has never moved a number. I've watched plenty of managers try.
      What sometimes moves it is math that's hard to wave off.</p>
    <h3>The best time to fight it is the year before</h3>
    <p>If you wait until January to argue about quota, you're already late. The number gets built during planning, by
      people who usually know less about your territory than you do. If you manage a team, get into that room while
      somebody still has the spreadsheet open, and bring what you know:</p>
    <ul>
      <li>Last year's sales, and the monthly and quarterly run rate</li>
      <li>Qualified pipeline, your real win rate, and your average deal size</li>
      <li>Headcount and ramp time. A rep hired in March doesn't sell much until summer.</li>
      <li>The renewal base, and what in it is actually at risk</li>
      <li>What partners brought in last year, as opposed to what they promised</li>
      <li>When your customers' money moves (for federal, that's the fiscal year, not your quarter)</li>
      <li>What changed in the market, and what changed in the territory</li>
    </ul>
    <p>Then ask one question: what has to be true for this number to be reasonable? Make somebody say it out loud.
      Half the time nobody has actually thought about it.</p>
    <h3>If the number is already set</h3>
    <p>Don't walk in upset. Walk in with a model, something like this:</p>
    <div class="bridge">Last year we did $8.2M.<br>Our current run rate gets us to $8.7M.<br>Qualified pipeline supports
      $9.4M at our historical win rate.<br>We lost a rep, added no territory, and the new hire won't be productive
      until Q3.<br>The quota is $12M.<br><b>Show me the bridge.</b></div>
    <p>Then stop talking. Either somebody fills the gap with something real (new territory, a renewal you didn't know
      about, a partner with names attached), or the number moves, or at least everybody knows where it came from. Any of
      those beats signing up quietly and explaining the miss in October.</p>
    <h3>What doesn't work</h3>
    <p>Complaining about it in the team meeting. Telling your boss the reps are upset. Saying "we'll find a way," which I
      used to say, and then spent the year explaining. And don't let anybody close the gap on paper by assuming AI will
      make the reps more productive. It can write the follow-up email. It can't make the customer care.</p>
    <p>If only 20% of the team hits quota year after year, it's probably not a performance problem.</p>''',
         tool=('/quota/', 'Quota Check', 'does the multiple and the implied rate in about ten seconds. Pipeline Check and Territory Check cover the rest of the bridge.')),
    dict(slug='the-number-isnt-changing', title="The number isn't changing. Now what?",
         dek="You made the case. It didn't move. Fine. Now figure out what it takes.",
         body='''    <p class="lede">You brought the bridge, you asked what assumption you were missing, and the answer was some
      version of "the number is the number." Fine. The number's ugly. Now figure out what it requires.</p>
    <h3>Stop relitigating it</h3>
    <p>This is mostly for managers. Once the quota is set and you've made your case, stop arguing about it with the
      team every Monday. They already know it's big. Hearing you complain about it just tells them you don't think it's
      hittable, and they'll believe you.</p>
    <p>A manager's job isn't to complain upward or enforce downward. It's to translate the number in both directions:
      explain to your boss what the territory can actually do, and explain to your team what the number actually
      requires.</p>
    <h3>Work backward</h3>
    <p>Start from the quota and walk it down: required bookings, then the pipeline that takes at your real win rate,
      then how many opportunities that is at your average deal size, then what it means per rep, per month. Keep the
      math simple enough to put on one whiteboard.</p>
    <ul>
      <li>What's already coming in: renewals, run rate, deals that are genuinely late-stage</li>
      <li>What existing accounts can grow into, with names</li>
      <li>What has to come from new logos, and how many that is</li>
      <li>What partners have actually brought in before, not what they promised</li>
      <li>Whether you have the reps to cover it, counting ramp time honestly</li>
    </ul>
    <p>Somewhere in that list is the part nobody can see yet. That's where the plan goes. It's usually new pipeline, and
      it's usually needed earlier than anybody wants to admit.</p>
    <h3>A hard number can still be a fair one</h3>
    <p>Some quotas are crazy. A lot of them are just hard. The difference is whether you can draw a line from where you
      are to the number, even if the line is steep. If you can, it's a plan. If you can't, go back to the bridge.</p>''',
         tool=('/pipeline/', 'Pipeline Check', 'works backward from the quota to the pipeline and deals it takes, per rep and per month.')),
    dict(slug='read-your-comp-plan', title="Before you decide the comp plan sucks, figure out how it pays",
         dek="Most reps read the quota and the OTE and stop. The money is in the rest of it.",
         body='''    <p class="lede">Most people read two lines of a comp plan: the quota and the OTE. Then they decide whether it
      sucks. The part that decides what you actually take home is usually further down.</p>
    <h3>What to read, in order</h3>
    <ul>
      <li><strong>Quota and OTE.</strong> Divide one by the other. That multiple tells you more than either number alone.</li>
      <li><strong>Base and variable split.</strong> The more of your pay that's variable, the more the quota matters.</li>
      <li><strong>Accelerators.</strong> Where they start, and what they pay. Past 100% is where plans are either generous or not.</li>
      <li><strong>Decelerators.</strong> What you get paid below a threshold. Some plans pay nearly nothing under 50%.</li>
      <li><strong>Caps.</strong> Whether there's a ceiling on what you can earn, stated or buried.</li>
      <li><strong>Multipliers.</strong> Extra credit for new logos or certain products. This is where the plan tells you what the company actually wants.</li>
      <li><strong>Crediting and splits.</strong> Who gets credit when two people touch a deal, and what happens to a territory that changes mid-year.</li>
      <li><strong>Clawbacks and payout timing.</strong> When you actually get paid, and what they can take back if a customer leaves.</li>
    </ul>
    <h3>Then decide</h3>
    <p>A plan with a hard quota and real accelerators can be a good plan. A plan with an ordinary quota, a cap and a
      fat decelerator can be a bad one. You won't know which you have until you've read the whole thing.</p>
    <p>None of this is legal or tax advice. If something in the plan doesn't make sense, ask whoever runs comp to walk
      you through it, in writing. If they can't explain it, that's worth knowing too.</p>''',
         tool=('/quota/', 'Quota Check', 'does the multiple and the implied rate. Commission Check shows what a closed deal actually pays you.')),
    dict(slug='3x-is-a-win-rate', title='3X is a win rate in disguise',
         dek='Everybody plans to it. Almost nobody asks where it came from.',
         body='''    <p class="lede">Everybody plans to 3X. Almost nobody asks why.</p>
    <p>3X is just a 33% win rate wearing a nicer shirt. Win a third of qualified pipeline and 3X covers the number.</p>
    <p>If you win 20%, you need 5X. If you win half, you need 2X. Planning to 3X with a 20% win rate is hopium with a spreadsheet.</p>
    <p>The other slippery word is <em>qualified</em>. Count the pipeline you'd defend when somebody starts asking about the customer, money, power, path and why now. The rest is just stuff in the CRM.</p>
    <h3>Do the math</h3>
    <p>Take your qualified win rate for the last four quarters and divide one by it. That's your coverage number. Then count only the pipeline you'd defend in a review.</p>''',
         tool=('/pipeline/', 'Pipeline Check', 'does both in about a minute, and shows the 3X line and yours on the same bar.')),
    dict(slug='why-not-bant-or-meddic', title="Why I don't start with BANT or MEDDIC",
         dek="They're useful when you're working a deal. The trouble is the moment before that.",
         body='''    <p class="lede">I've used both, and plenty of versions of both. They're useful when you're working a deal.
      The trouble is the moment before that.</p>
    <p>I just don't start there.</p>
    <p>BANT gets you close, but its need is usually something the seller diagnosed, and its timeline is a date in
      the CRM rather than a reason anything happens. It also skips the biggest federal question: how does a
      purchase order actually appear? Contract vehicle, contracting office, acquisition lead time. That's the
      timeline.</p>
    <p>MEDDIC, or MEDDPICC depending on who taught it to you, is more sophisticated, which is part of the problem. I've watched sellers spend forty-five minutes deciding whether somebody counts as an economic buyer. The five questions are blunter, and they're meant to come before that debate.</p>
    <p class="lede">I'd save MEDDIC for after the five questions say there's a real deal.</p>''',
         tool=('/deal/', 'Deal Check', 'is the five questions, with the arithmetic done and the question your manager will ask.')),
    dict(slug='three-people-same-patch', title='If three people failed in the same territory',
         dek="You probably don't have three bad reps.",
         body='''    <p class="lede">If three people have failed in the same territory, you probably don't have three bad reps.</p>
    <p>Before you decide the reps are bad, look at what they inherited. If three people failed in the same territory, I'd start with the territory.</p>
    <p>Start with the territory: account quality, installed base, the quota, the comp plan, who had it before. If a good rep couldn't make the number there, nothing you do with the person matters, so fix the territory, the number or the plan first.</p>
    <p>Then the person, in this order. Do customers choose to spend time with them? Is there pipeline that exists
      only because they're here? When they're in front of a customer, can they actually sell? Are they still
      trying to win? The third question is the one most managers skip, and it's the one that separates can't from
      isn't. One you coach. The other you manage.</p>
    <p>Be careful with the rep who annoys you internally but customers keep calling back. They may be doing more selling than the polished rep with perfect CRM hygiene.</p>
    <h3>Before you decide anything</h3>
    <p>Sit with them and go through five real deals. You'll learn more in ninety minutes than a month of dashboards.</p>''',
         tool=('/rep/', 'Rep Check', 'asks the territory first and the person second, and tells you which problem you have.')),
    dict(slug='quota-went-up-did-your-territory', title='Your quota went up 30%. Did your territory?',
         dek='The number moved. Ask what else did.',
         body='''    <p class="lede">The number went up. Before you decide whether you can make it, check whether anything else did.</p>
    <p>When your quota goes up 30%, usually one of three things happened: the territory got bigger, the territory got better, or somebody needed the spreadsheet to add up. You want to know if it's the third one in January, not October.</p>
    <p>Do the boring math first. Divide quota by OTE. Then divide the new number by what you closed last year. That's how much harder the plan is asking the territory to work.</p>
    <p>Then look at the territory the way a stranger would. Has anyone ever made this number in it? What's the addressable spend, and how much of it is already committed to somebody else? If the number went up and the territory didn't, say so early, with the sizing, in writing. It's a lot harder to argue with a number when you've shown your work.</p>''',
         tool=('/quota/', 'Quota Check', 'does the arithmetic in ten seconds, and hands the number to the territory and pipeline checks.')),
    dict(slug='fifteen-percent-off', title='They asked for 15% off. What are you buying with it?',
         dek='A discount is a purchase. The only question is what you got for it.',
         body='''    <p class="lede">Every point off the price is supposed to buy you something. Check whether it did.</p>
    <p>The customer thinks of a discount as something they bought, so I think of it that way too. Up to about 5% off is normal negotiation and nobody remembers it. Between 5 and 15% is real money, and it should buy something specific: a signature date, a bigger scope, a multi-year term, a reference you can use. Above 15% you're paying for a decision, so the decision had better come with it, this quarter, in writing. Above 25%, in my experience, you're paying to be liked, and the customer will remember the number.</p>
    <p>Two things worth knowing before the conversation. The discount comes out of your commission at exactly the
      rate it comes out of revenue, so 15% off is a 15% pay cut on that deal. And it comes out of the company's
      margin faster than that, because the cost of delivering the thing doesn't drop when the price does.</p>
    <p>The question I'd actually ask first: is the objection the price, or the deal? A discount only helps with the price, and usually that's not the real problem.</p>''',
         tool=('/discount/', 'Discount Check', 'shows what the discount costs you and the company before you agree to it.')),
    dict(slug='best-rep-hates-meetings', title='Your best rep hates internal meetings. Is that a problem?',
         dek="Probably not the one you think.",
         body='''    <p class="lede">Every team has one. Skips the pipeline call, answers Slack in bursts, CRM hygiene is a
      disgrace, and customers call her back.</p>
    <p>The manager's instinct is to fix the behavior. Before you do, ask which differences matter to selling and which don't. Do customers choose to spend time with her? Is there pipeline that exists only because she's here? When she's in front of a customer, can she sell? Is she still trying to win? If the answers are yes, what you've got is a visibility problem, and that one's yours to solve.</p>
    <p>Decide what visibility you need. Usually it's less than the process asks for: the five deals that
      matter, a straight answer on where each one stands, and a heads-up before something moves in the forecast.
      Get that, and let her sell. The polished rep with immaculate CRM hygiene and no customer pull is the one who
      should worry you, and he's the one the dashboard likes.</p>
    <p>Standards still apply. It's just that the standard is customers and pipeline, and the meetings are supposed to serve that. If the meetings start costing you customers, change the meetings.</p>''',
         tool=('/rep/', 'Rep Check', 'asks about the customers, the pipeline, the craft and the will before it asks about the calendar.')),
]

def note_head(title, desc, url):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} | QuotaBird</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:site_name" content="QuotaBird">
<meta property="og:image" content="https://quotabird.com/card.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://quotabird.com/card.jpg">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#FFFFFF">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#101418">
<link rel="stylesheet" href="/site.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BG9NR9GXQZ"></script>
<script src="/analytics.js" defer></script>
'''
NOTE_TAIL = '''<footer class="sitefoot">
  <a href="/">QuotaBird</a> is a pile of free sales tools. I built them because they helped me, and maybe they'll help you.
  <p>Not affiliated with the U.S. government or Amazon.</p>
</footer>
<script>
document.addEventListener('click', (e) => { document.querySelectorAll('details.menu[open]').forEach(d => { if (!d.contains(e.target)) d.open = false; }); });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') document.querySelectorAll('details.menu[open]').forEach(d => { d.open = false; d.querySelector('summary').focus(); }); });
</script>
</body>
</html>
'''
def note_list():
    return '<div class="doors">' + ''.join(
        f'<a class="door" href="/notes/{n["slug"]}/"><span><b>{n["title"]}</b><span class="q">{n["dek"]}</span></span><span class="to">Read</span></a>'
        for n in NOTES) + '</div>'

for n in NOTES:
    url = f'https://quotabird.com/notes/{n["slug"]}/'
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": n['title'], "description": n['dek'],
                     "url": url, "image": "https://quotabird.com/card.jpg",
                     "author": {"@type": "Person", "@id": "https://quotabird.com/#about", "name": "Mark Flournoy"},
                     "publisher": {"@type": "Organization", "name": "QuotaBird", "url": "https://quotabird.com/"}}, indent=2)
    href, name, line = n['tool']
    html = note_head(n['title'], n['dek'] + ' A Field Note that ends with ' + n['tool'][1] + ', which ' + n['tool'][2], url) + f'''<script type="application/ld+json">
{ld}
</script>
</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note">
  <span class="overline">Field Note</span>
  <h1>{n['title']}</h1>
{n['body']}
  <div class="card card-accent" style="margin-top:28px;">
    <span class="overline">Try it</span>
    <p class="lede"><a href="{href}">{name}</a> {line}</p>
    <a class="btn btn-primary btn-full" href="{href}" style="margin-top:14px;">Try it</a>
  </div>
  <p style="margin-top:20px;"><a href="/notes/">More field notes</a></p>
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL
    assert '—' not in html and '–' not in html, n['slug']
    os.makedirs(f'notes/{n["slug"]}', exist_ok=True)
    open(f'notes/{n["slug"]}/index.html', 'w').write(html)

idx = note_head('Field Notes', 'Short reads on sales things people repeat without thinking about much. Most end with a tool that does the math.', 'https://quotabird.com/notes/') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note">
  <span class="overline">QuotaBird</span>
  <h1>Field Notes</h1>
  <p class="dek">Short reads on sales things people repeat without thinking about much. Most end with a tool that does the math.</p>
  ''' + note_list() + '''
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL
os.makedirs('notes', exist_ok=True)
open('notes/index.html', 'w').write(idx)
print('notes', len(NOTES))

# ────────────────────────────── QUOTA SHORTS (home strip + /shorts/) ──────────────────────────────
# Snack-size facts. One idea per card, one line under it, a source, and the tool that does the math.
# Every number here is sourced on /quota-by-the-numbers/. Colours are the shelf's.
from html import escape as esc_html
SHORTS = [
    dict(tag='Attainment', num='48', unit='%', fact='of AEs hit quota in 2026.', line='It was 66% in 2022.', src='Bridge Group, 2026', href='/quota/', go='Check my quota', bg='#E07A5F', ink='#2B1B1B'),
    dict(tag='The median', num='$960', unit='K', fact='is the median SaaS quota.', line='On a $200K OTE.', src='Bridge Group, 2026', href='/quota/', go='Check my quota', bg='#F4E1C1', ink='#2B2B2B'),
    dict(tag='The multiple', num='4.6', unit='×', fact='quota to OTE, the median.', line='It was 4.2 two years ago.', src='Bridge Group, 2026', href='/quota/', go='Check my quota', bg='#F2C14E', ink='#1B1B1B'),
    dict(tag='Planning', num='20-30', unit='%', fact="more quota gets handed out than the company needs.", line='Planners over-assign to cover misses.', src='Mostly Metrics', href='/how-quotas-get-built/', go='How quotas get built', bg='#1C3D5A', ink='#FFFFFF'),
    dict(tag='Your boss', num='', unit='', fact='Your boss may be paid on something else.', line='Growth rate, new logos, a strategic product.', src='', href='/how-quotas-get-built/', go='How quotas get built', bg='#C35037', ink='#FFFFFF'),
    dict(tag='Ramp', num='6.2', unit='mo', fact='for a new AE to ramp.', line='A rep hired in March is a fall rep.', src='Bridge Group, 2026', href='/quota-case/', go='Build the bridge', bg='#388073', ink='#FFFFFF'),
    dict(tag='Vacancies', num='', unit='', fact='A vacant territory still has quota.', line="Somebody's carrying it.", src='', href='/quota-case/', go='Build the bridge', bg='#2E2E3A', ink='#F2C14E'),
    dict(tag='Coverage', num='3', unit='X', fact='is a 33% win rate wearing a nicer shirt.', line='Win 20% and you need 5X.', src='The math', href='/pipeline/', go='Check my pipeline', bg='#6C5B7B', ink='#FFFFFF'),
    dict(tag='Cloud', num='', unit='', fact="A commit nobody uses doesn't retire much quota.", line='Cloud quotas count what customers run.', src='Microsoft Partner Center', href='/quota/', go='Check my quota', bg='#9DD2FF', ink='#12324F'),
    dict(tag='Comp', num='1.5-2', unit='×', fact='is what most accelerators pay above quota.', line='Where they start matters more than the rate.', src='Comp plan surveys, 2026', href='/notes/read-your-comp-plan/', go='Read your comp plan', bg='#567E55', ink='#FFFFFF'),
    dict(tag='Federal', num='46', unit='%', fact='of federal AEs say they hit quota.', line='The most of any AE role. SLED is 45%.', src='RepVue, 2026', href='/territory/', go='Check my territory', bg='#264653', ink='#E9C46A'),
]
def _short(s, i):
    src = f'<span class="short-src">{esc_html(s["src"])}</span>' if s['src'] else ''
    num = (f'<span class="short-num">{esc_html(s["num"])}<span class="short-unit">{esc_html(s["unit"])}</span></span>' if s['num'] else '')
    return (f'<a class="short{" has-num" if s["num"] else ""}" href="{s["href"]}" style="--bg:{s["bg"]};--ink:{s["ink"]}" data-short="{i+1}">'
            f'<span class="short-tag">{esc_html(s["tag"])}</span>{num}<span class="short-fact">{esc_html(s["fact"])}</span>'
            f'<span class="short-line">{esc_html(s["line"])}</span><span class="short-foot">{src}<span class="short-go">{esc_html(s["go"])} →</span></span></a>')
def shorts_strip():
    return ('<section class="shorts-band" aria-labelledby="shorts-h"><div class="shorts-head"><h2 id="shorts-h">Quota Shorts</h2>'
            '<a class="shorts-all" href="/shorts/">All of them</a></div>'
            '<div class="shorts-row" role="list">' + ''.join(f'<div role="listitem">{_short(s, i)}</div>' for i, s in enumerate(SHORTS)) + '</div></section>')

# ────────────────────────────── HOME ──────────────────────────────
# The home page source lives in home.src.html; this fills in the note list and build stamp.
home = open('home.src.html').read().replace('__NOTES__', note_list()).replace('__BUILD__', BUILD).replace('<!--shorts-->', shorts_strip())
open('index.html', 'w').write(home)
# Pipeline Check lives at /pipeline/ again (it was the home page until the shelf took over)
os.makedirs('pipeline', exist_ok=True)
open('pipeline/index.html', 'w').write(open('pipeline.src.html').read().replace('__BUILD__', BUILD))

# ────────────────────────────── CALCULATORS (Quota, Discount, Commission) ──────────────────────────────
# Rebuilt from the old Fedmo tools: Is My Quota Crazy?, They Want a Discount, Commissions Take-Home.
CALCS = [
 dict(slug='quota-case', name='Quota Case',
  title='Quota Case: What Has to Be True for This Quota to Work?',
  desc='Build the bridge from last year to this year\'s quota: run rate, pipeline at your real win rate, headcount, one-time deals. Find the gap nobody has explained, and take it to your boss calmly.',
  ogdesc='What has to be true for this quota to work? Last year, run rate, pipeline and headcount in; the bridge and the gap out.',
  h1='What has to be true for this quota to work?', dek='Last year, your run rate, your pipeline and the new number. It builds the bridge and shows you the gap nobody has explained yet.',
  fields=[dict(id='lastyear',kind='money',label='What the team closed last year',example='$8,200,000'),
          dict(id='oneoff',kind='money',label='One-time deals in that number',example='',placeholder='$0 (optional)'),
          dict(id='runrate',kind='money',label='Current run rate, annualized (monthly × 12)',example='$8,700,000'),
          dict(id='pipeline',kind='money',label='Qualified pipeline for this year',example='$37,600,000'),
          dict(id='win',kind='pct',label='Your historical win rate',example='25%'),
          dict(id='repsthen',kind='count',label='Reps last year',example='',placeholder='optional'),
          dict(id='repsnow',kind='count',label='Fully ramped reps now',example='',placeholder='optional'),
          dict(id='quota',kind='money',label='The new number',example='$12,000,000')],
  card=dict(headline=['What has to be true', 'for this quota to work?'],dek='Last year, run rate, pipeline, headcount and the new number. The bridge, and the gap.',pillars=['LAST YEAR','RUN RATE','PIPELINE','THE GAP']),
  bands=[('how','How the bridge works','''    <p class="lede">It takes the better of two views of this year: your run rate at today's headcount, and your qualified pipeline at your real win rate. Whatever's left between that and the new number is the gap somebody needs to explain.</p>
    <p>Take one-time deals out of last year. If a single giant deal made last year's number, building this year's quota on it is how a team ends up at 60% attainment and a lot of meetings about effort.</p>
    <p>If you lost reps or have open territories, put in the headcount. A vacant territory still has quota. That's the problem. And a rep hired in March doesn't sell much until summer, so count them when they're ramped, not when they start.</p>'''),
         ('conversation','Taking it to your boss','''    <p class="lede">Don't walk in upset. Walk in with the bridge and one question: what assumption am I missing?</p>
    <p>Sometimes there's a real answer: new territory, a big renewal you didn't know about, a product launch, partner help with names attached. Then the number's hard but fair, and your job changes to helping the team hit it, which means you stop relitigating it every Monday. Sometimes nobody has an answer. Then at least everybody knows where the number came from, and it's in writing before the year starts.</p>
    <p><a href="/notes/prove-the-quota-is-crazy/">Your quota is crazy. Now prove it.</a> has the longer version, including why the best time to have this fight is the year before.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The math runs right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your numbers, and nothing leaves the page unless you share a result.'),
       ('Is this the company\'s formula?','No. Nobody outside finance has that, and some years nobody inside does either. This is the evidence you have: history, capacity and pipeline. It\'s the part of the conversation you control.'),
       ('What if I don\'t know my win rate?','Count it: of last year\'s qualified deals, how much closed, by value. Or leave pipeline and win rate blank and it\'ll use your run rate alone.'),
       ('Rep or manager?','Either. A manager uses it to take the team\'s number upstairs. A rep can run it on their own territory before the one-on-one where the number gets explained.')],
  config="""CalcTool({
  slug: 'quota-case', name: 'Quota Case', url: 'https://quotabird.com/quota-case/',
  fields: [{ id: 'lastyear', kind: 'money' }, { id: 'oneoff', kind: 'money' }, { id: 'runrate', kind: 'money' }, { id: 'pipeline', kind: 'money' }, { id: 'win', kind: 'pct' }, { id: 'repsthen', kind: 'count' }, { id: 'repsnow', kind: 'count' }, { id: 'quota', kind: 'money' }],
  compute(v) {
    if (!(v.quota > 0 && v.lastyear > 0 && (v.runrate > 0 || (v.pipeline > 0 && v.win > 0)))) return null;
    const money = (n) => { const a = Math.abs(n); return (n < 0 ? '-' : '') + (a >= 1e6 ? '$' + (a / 1e6).toFixed(1).replace(/\\.0$/, '') + 'M' : a >= 1e3 ? '$' + Math.round(a / 1e3) + 'K' : '$' + Math.round(a)); };
    const pct = (r) => Math.round(r * 100) + '%';
    const last = v.lastyear - (v.oneoff || 0);
    const cap = (v.repsthen > 0 && v.repsnow > 0) ? v.repsnow / v.repsthen : 1;
    const run = v.runrate > 0 ? v.runrate * cap : 0;
    const pipe = (v.pipeline > 0 && v.win > 0) ? v.pipeline * v.win : 0;
    const best = Math.max(run, pipe), gap = v.quota - best, share = gap / v.quota, growth = (v.quota - last) / last;
    let t;
    if (gap <= 0) t = ['Supported', 'ready', `The evidence supports ${money(v.quota)}. Hard, maybe, but defensible.`, 'Stop arguing about it with the team and build the plan.'];
    else if (share <= .10) t = ['Tight', 'proof', `${money(gap)} short of what the evidence supports. That's a stretch, not a scandal.`, `Find the ${money(gap)} with names attached, then build the plan.`];
    else if (share <= .25) t = ['Needs a bridge', 'prove', `${money(gap)} of this number that nobody has explained yet.`, 'Ask what has to be true for it to work, and bring the bridge below.'];
    else t = ["Can't see it", 'dont', `${money(gap)}, ${pct(share)} of the number, with nothing in the evidence to fill it.`, 'Take the bridge to your boss before you sign anything.'];
    const rows = [['Last year', money(v.lastyear)]];
    if (v.oneoff > 0) rows.push(['Without one-time deals', money(last)]);
    if (run) rows.push([cap !== 1 ? "Run rate at today's headcount" : 'Current run rate', money(run)]);
    if (pipe) rows.push([`Pipeline at your ${pct(v.win)} win rate`, money(pipe)]);
    rows.push(['The new number', money(v.quota)]);
    rows.push([v.oneoff > 0 ? 'Growth over last year, without one-offs' : 'Growth over last year', (growth >= 0 ? '+' : '') + pct(growth), growth > .25 ? 'v-no' : '']);
    rows.push(['Gap nobody has explained', gap > 0 ? money(gap) : 'None', gap > 0 ? 'v-no' : '']);
    const note = gap > 0 ? `What to say: "Here's last year, here's what we're running at, and here's a ${money(gap)} gap I can't explain. What assumption am I missing?"` : "The number holds up against the evidence. Now it's about the plan.";
    return { label: t[0], cls: t[1], attack: t[2], sub: t[3], big: gap > 0 ? money(gap) : 'Covered', rows, note, gap, quota: v.quota, best, growth, gapm: money(gap), quotam: money(v.quota), bestm: money(best) };
  },
  handoff: (s) => s.gap > 0
    ? { overline: 'Before you take it upstairs', text: 'How to walk in with this, and what to do when they push back.', href: '/notes/prove-the-quota-is-crazy/', label: 'Read the playbook' }
    : { overline: 'Okay. How do we hit it?', text: `Pipeline Check works backward from ${s.quotam} to the pipeline and deals it takes.`, href: `/pipeline/#t=${Math.round(s.quota)}&y=cy`, label: 'Check my pipeline' },
  mark: { title: () => 'Want a second look at the bridge?', body: "I'm Mark. I've taken a bridge like this to my boss and had the number move, and I've had it not move. Either way it was a better conversation than 'this feels high.' Send me the numbers, no company name." },
  dm: (s) => `Mark, ran our quota through Quota Case. The new number is ${s.quotam}, the evidence supports about ${s.bestm}, so a ${s.gap > 0 ? s.gapm : '$0'} gap. Not sure how to take it upstairs. Worth 20 minutes?`,
  bookNote: (s) => `Quota Case: quota ${s.quotam}, evidence supports ${s.bestm}, gap ${s.gap > 0 ? s.gapm : 'none'}.`,
});"""),
 dict(slug='quota', name='Quota Check',
  title='Quota Check: Is My Quota Crazy?',
  desc='Your quota against your on-target earnings, judged by what the number is measured in: new bookings, cloud consumption growth, or a whole book.',
  ogdesc='Is my quota crazy? Base, variable, quota and what it\'s measured in. A straight answer out.',
  h1='Is my quota crazy?', dek='Plug in your base, your variable and the number they handed you to find out.',
  fields=[dict(id='basis',kind='choice',label='What the number is measured in',example='cloud',options=[('saas','New bookings'),('cloud','Cloud consumption growth'),('book','Whole book')]),
          dict(id='base',kind='money',label='Base salary',example='$150,000'),dict(id='variable',kind='money',label='Target variable at 100%',example='$130,000'),
          dict(id='quota',kind='money',label='Your quota for the year',example='$6,000,000'),dict(id='closed',kind='money',label='What you closed last year',example='',placeholder='$0 (optional)')],
  card=dict(headline=['Is my quota crazy?',''],dek='Your number against your on-target earnings, judged by what it\'s measured in.',pillars=['OTE','MULTIPLE','RATE','GROWTH']),
  bands=[('pushback','If the number is crazy','''    <p class="lede">Saying it feels too high won't move it. Bring the math: last year's sales, your run rate, qualified pipeline at your real win rate, headcount and ramp time. Then ask what has to be true for the number to be reasonable.</p>
    <p>Better yet, get into planning the year before, while somebody still has the spreadsheet open. <a href="/notes/prove-the-quota-is-crazy/">Your quota is crazy. Now prove it.</a> walks through it, with an example you can steal.</p>'''),('how','Why the multiple depends on what you sell','''    <p class="lede">Divide your quota by your on-target earnings. That one number tells you a lot about the plan, once you know what the quota is measured in.</p>
    <p>For SaaS reps carrying new bookings, the published benchmarks agree: 4 to 6 times OTE, with 5 as the steady state and enterprise roles a little higher. That range is really a commission rate in disguise. At a 50/50 pay mix and roughly 10% on new ARR, quota works out to about five times OTE. Below 3 is unusual and usually means a ramp, an overlay, or a plan with a condition in it. Above 8 the plan is asking for something the territory may not have.</p>
    <p>Cloud consumption is a different animal, and it's the one most people on this site carry. The number is incremental revenue growth on a book, paid at a fraction of a percent, so the same arithmetic gives 15 to 30 times OTE at a big cloud provider and higher in strategic accounts. A rep carrying a $6M growth target on a $280K OTE is at 21×, and in my experience that's ordinary, not crazy. Whole-book targets (retention plus growth on the full run rate) run higher still, 40 to 80 times OTE, because most of that revenue would have happened anyway.</p>
    <p>The number to watch across all three is the implied rate: your variable divided by your quota. If it's well under what your peers are paid on the same kind of number, the plan is heavier than the multiple alone suggests. And if you closed last year, the growth the new number implies is the real measure of how much harder this year is. Whether the territory can produce it is <a href="/territory/">Territory Check</a>; how much pipeline it takes is <a href="/pipeline/">Pipeline Check</a>.</p>'''),
         ('ranges','The ranges I use','''    <p>These are ranges I've seen across cloud providers, SaaS companies and their partners, not rules, and roles differ. Quota ÷ OTE:</p>
    <p><strong>New bookings.</strong> Under 3: low. 3 to 4: favorable. 4 to 6: standard. 6 to 8: a stretch. 8 to 12: aggressive. Over 12: crazy.</p>
    <p><strong>Cloud consumption growth.</strong> Under 8: low. 8 to 15: favorable. 15 to 30: standard. 30 to 45: a stretch. 45 to 60: aggressive. Over 60: crazy.</p>
    <p><strong>Whole book.</strong> Under 20: low. 20 to 40: favorable. 40 to 80: standard. 80 to 120: a stretch. 120 to 160: aggressive. Over 160: crazy.</p>
    <p>If your plan sits somewhere else and you think the range is wrong, tell me and I'll look at it.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The math runs right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your numbers, and nothing leaves the page unless you share a result.'),
       ('Why does it ask what the number is measured in?','Because the same multiple means different things. A $1.4M new-bookings quota on a $280K OTE is 5× and normal. A $1.4M cloud consumption growth target on the same OTE is 5× and unusually light, because consumption is paid at a fraction of the rate bookings are. Pick the basis your plan actually uses.'),
       ('Where do the ranges come from?','The SaaS range is the published consensus (Bridge Group, RepVue, Pavilion and others put it at 4 to 6× OTE). The cloud and whole-book ranges are what I\'ve seen at cloud providers and their partners, worked back from the commission rates those plans pay. I\'ll change them if enough people tell me their plan sits somewhere else.'),
       ('What if my variable is a bonus, not commission?','Use the target amount at 100% attainment either way. The tool cares about how much of your pay depends on the number, not what the plan calls it.')],
  config="""CalcTool({
  slug: 'quota', name: 'Quota Check', url: 'https://quotabird.com/quota/',
  fields: [{ id: 'basis', kind: 'choice', example: 'cloud' }, { id: 'base', kind: 'money' }, { id: 'variable', kind: 'money' }, { id: 'quota', kind: 'money' }, { id: 'closed', kind: 'money' }],
  compute(v) {
    if (!(v.base > 0 && v.variable > 0 && v.quota > 0)) return null;
    const ote = v.base + v.variable, mult = v.quota / ote, share = v.variable / ote, rate = v.variable / v.quota;
    const X = (mult >= 10 ? Math.round(mult) : mult.toFixed(1)) + '×';
    const pct = (r) => Math.round(r * 100) + '%';
    const ratePct = rate >= .1 ? Math.round(rate * 100) + '%' : (rate * 100).toFixed(rate >= .01 ? 1 : 2) + '%';
    const money = (n) => n >= 1e6 ? '$' + (n / 1e6).toFixed(2).replace(/\\.?0+$/, '') + 'M' : n >= 1e3 ? '$' + Math.round(n / 1e3) + 'K' : '$' + Math.round(n);
    // ranges I've seen, by what the quota is measured in (see the page copy)
    const B = { saas: { name: 'new bookings', cuts: [3, 4, 6, 8, 12] }, cloud: { name: 'cloud consumption growth', cuts: [8, 15, 30, 45, 60] }, book: { name: 'a whole book', cuts: [20, 40, 80, 120, 160] } }[v.basis] || { name: 'cloud consumption growth', cuts: [8, 15, 30, 45, 60] };
    const c = B.cuts, std = c[1] + ' to ' + c[2];
    let t;
    if (mult < c[0]) t = ['Low', 'proof', `Quota is ${X} OTE. For ${B.name} that's unusually low: a ramp, an overlay, or a plan with a condition in it.`, 'Read the plan twice. Low multiples usually come with a catch.'];
    else if (mult < c[1]) t = ['Favorable', 'ready', `Quota is ${X} OTE, below the ${std} I usually see for ${B.name}.`, 'Common in new territories, SMB and commercial. Enjoy it while it lasts.'];
    else if (mult <= c[2]) t = ['Standard', 'ready', `Quota is ${X} OTE, inside the ${std} I usually see for ${B.name}.`, "The number is ordinary. Whether the territory can produce it is a different question."];
    else if (mult <= c[3]) t = ['A stretch', 'proof', `Quota is ${X} OTE, above the ${std} I usually see for ${B.name}.`, 'Normal for enterprise and strategic roles, and it needs a strong pipeline behind it.'];
    else if (mult <= c[4]) t = ['Aggressive', 'prove', `Quota is ${X} OTE, well above the ${std} I usually see for ${B.name}.`, 'Strategic-account territory. You need coverage and a territory that can produce it.'];
    else t = ['Crazy', 'dont', `Quota is ${X} OTE. For ${B.name}, the plan is asking the territory for something it may not have.`, 'Check the territory before you sign, and get the sizing in writing.'];
    const growth = v.closed > 0 ? (v.quota - v.closed) / v.closed : null;
    const rows = [['On-target earnings', money(ote)], ['Quota ÷ OTE', X], ['Implied rate on quota', ratePct], ['Variable share of OTE', pct(share)]];
    if (growth != null) rows.push(['Growth over what you closed', (growth >= 0 ? '+' : '') + pct(growth), growth > .3 ? 'v-no' : '']);
    const note = share < .4 ? 'Variable is under 40% of OTE. You\\'re paid mostly to show up, and the quota matters less than it looks.' : share > .6 ? 'Variable is over 60% of OTE. The quota is most of your pay. Treat it like one.' : '';
    return { label: t[0], cls: t[1], attack: t[2], sub: t[3], big: X, rows, note, mult, share, growth, ote, quota: v.quota, basis: B.name, ratePct };
  },
  handoff: (s) => ({ overline: 'Now the coverage math', text: `At 3X you'd need about $${(s.quota * 3 / 1e6).toFixed(1)}M of qualified pipeline to cover it. Your win rate will say more.`, href: `/pipeline/#t=${Math.round(s.quota)}&y=cy`, label: 'Check my pipeline' }),
  mark: { title: () => 'Is the plan sane?', body: "I'm Mark. I've been handed the crazy number, and I've handed one out by mistake. If yours is off, I can help you make the case to your boss, and if it's fair we can still work out how you'd hit it." },
  dm: (s) => `Mark, ran my comp plan through Quota Check. Quota is ${s.big} OTE on ${s.basis}, implied rate ${s.ratePct}, variable ${Math.round(s.share * 100)}% of OTE${s.growth != null ? ', ' + Math.round(s.growth * 100) + '% over what I closed last year' : ''}. Not sure it's sane. Worth 20 minutes?`,
  bookNote: (s) => `Quota Check: ${s.big} OTE on ${s.basis}, implied rate ${s.ratePct}, ${s.label.toLowerCase()}.`,
});"""),
 dict(slug='discount', name='Discount Check',
  title='Discount Check: How Much Discount Is Too Much?',
  desc='How much discount is too much? See what it costs in your commission and the company\'s margin before you say yes.',
  ogdesc='How much discount is too much? Here is exactly what it costs you before you sharpen the pencil.',
  h1='How much discount is too much?', dek='Plug in the price and the discount to see what it costs you before you say yes.',
  fields=[dict(id='list',kind='money',label='Full list price',example='$500,000'),dict(id='disc',kind='pct',label='Discount they want',example='15%'),
          dict(id='margin',kind='pct',label="Company gross margin",example='40%'),dict(id='rate',kind='pct',label='Your commission rate',example='8%')],
  card=dict(headline=['How much discount is too much?',''],dek='What it costs you in commission, and the company in margin, before you say yes.',pillars=['PRICE','DISCOUNT','MARGIN','YOUR CUT']),
  bands=[('how','A discount is a purchase','''    <p class="lede">Every point off the price is supposed to buy you something. Check whether it did.</p>
    <p>These are rough ranges from my own deals and the ones I've reviewed; yours may differ. Up to about 5% is normal negotiation. Nobody remembers it. Between 5 and 15% is meaningful, and it should buy something specific: a signature date, a larger scope, a reference, a multi-year term. Above 15% you're paying for a decision, so the decision had better come with it, this quarter, in writing. Above 25%, you're usually paying to be liked, and the customer will remember the number.</p>
    <p>Two things sellers forget. The discount comes out of your commission at exactly the same rate it comes out of revenue, so a 15% discount is a 15% pay cut on that deal. And it comes out of the company's margin much faster than 15%: cost of goods doesn't move, so every dollar off the price is a dollar off the margin.</p>
    Before you discount at all, figure out whether the objection is really the price or the deal. A discount only helps with the price. <a href="/deal/">Deal Check</a> can tell you which one you've got.''')],
  faq=[('Does anything I enter leave my device?','No. The math runs right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your numbers, and nothing leaves the page unless you share a result.'),
       ('How is the new margin calculated?','Cost of goods stays the same when the price drops, so the margin after discount is one minus cost divided by the discounted price. That\'s why a 15% discount on a 40% margin leaves about 29%, not 25%.'),
       ('What if I don\'t know the company margin?','Leave it at the example and read the commission rows only. The margin rows are for the conversation with your manager; the commission row is the one that\'s about you.')],
  config='''CalcTool({
  slug: 'discount', name: 'Discount Check', url: 'https://quotabird.com/discount/',
  fields: [{ id: 'list', kind: 'money' }, { id: 'disc', kind: 'pct' }, { id: 'margin', kind: 'pct' }, { id: 'rate', kind: 'pct' }],
  compute(v) {
    if (!(v.list > 0 && v.disc > 0)) return null;
    const pct = (r) => Math.round(r * 100) + '%';
    const money = (n) => { const neg = n < 0; n = Math.abs(n); const t = n >= 1e6 ? '$' + (n / 1e6).toFixed(2).replace(/\\.?0+$/, '') + 'M' : n >= 1e3 ? '$' + Math.round(n / 1e3) + 'K' : '$' + Math.round(n); return (neg ? '-' : '') + t; };
    const discounted = v.list * (1 - v.disc), given = v.list - discounted;
    const commFull = v.list * v.rate, commLost = given * v.rate, commAfter = commFull - commLost;
    const cogs = v.list * (1 - v.margin), newMargin = v.margin > 0 ? Math.max(0, 1 - cogs / discounted) : null;
    let t;
    if (v.disc <= .05) t = ['Normal', 'ready', 'Inside what I would call normal negotiation range.'];
    else if (v.disc <= .15) t = ['Meaningful', 'proof', 'Get something specific for it: a signature date, a bigger scope, a reference.'];
    else if (v.disc <= .25) t = ['Expensive', 'prove', 'This much off should buy a decision this quarter, not a warmer feeling.'];
    else t = ['Giveaway', 'dont', "At this point you're paying to be liked, and they'll remember the number, not the gesture."];
    const attack = v.rate > 0
      ? `A ${pct(v.disc)} discount costs you ${money(commLost)} in commission${newMargin != null ? ` and takes margin from ${pct(v.margin)} to ${pct(newMargin)}` : ''}.`
      : `A ${pct(v.disc)} discount gives away ${money(given)}${newMargin != null ? ` and takes margin from ${pct(v.margin)} to ${pct(newMargin)}` : ''}.`;
    const rows = [['Discounted price', money(discounted)], ['Revenue given away', money(given), 'v-no']];
    if (v.rate > 0) rows.push(['Your commission, full price', money(commFull)], ['Your commission, discounted', money(commAfter)], ['Commission lost', money(commLost), 'v-no']);
    if (newMargin != null) rows.push(['Company margin after', pct(newMargin), newMargin < .15 ? 'v-no' : '']);
    return { label: t[0], cls: t[1], attack, sub: t[2], big: v.rate > 0 ? money(commLost) : money(given), rows, disc: v.disc, margin: v.margin, newMargin, stripText: '' };
  },
  handoff: { overline: 'Before you discount', text: 'Is the problem the price, or the deal? A discount only helps with the price.', href: '/deal/', label: 'Check my deal' },
  mark: { title: () => 'Stuck on the price?', body: "I'm Mark. I've watched a lot of discounts buy absolutely nothing. If somebody's asking you to sharpen the pencil, send me a line about why, no customer names or dollars." },
  dm: (s) => `Mark, ran a discount through Discount Check. ${Math.round(s.disc * 100)}% off costs me ${Math.round(s.disc * 100)}% of my commission${s.newMargin != null ? ' and takes margin from ' + Math.round(s.margin * 100) + '% to ' + Math.round(s.newMargin * 100) + '%' : ''}. Not sure it's worth it. Worth 20 minutes?`,
  bookNote: (s) => `Discount Check: ${Math.round(s.disc * 100)}% off${s.newMargin != null ? ', margin ' + Math.round(s.margin * 100) + '% to ' + Math.round(s.newMargin * 100) + '%' : ''}, ${s.label.toLowerCase()}.`,
});'''),
 dict(slug='commission', name='Commission Check',
  title='Commission Check: Your Take-Home on a Deal',
  desc='Deal size and commission rate in, what you actually take home out, after the share you set aside for taxes.',
  ogdesc='It closed. Here is roughly what you actually take home.',
  h1="It closed. What do I actually keep?", dek='Plug in the deal and your rate to find out, roughly, before the check lands.',
  fields=[dict(id='deal',kind='money',label='Deal size',example='$500,000'),dict(id='rate',kind='pct',label='Your commission rate',example='8%'),
          dict(id='buffer',kind='pct',label='Set aside for taxes',example='30%',presets=[('W-2 ~30%','30%'),('High bracket ~40%','40%'),('1099 ~20%','20%')])],
  card=dict(headline=['It closed.','What do I take home?'],dek='A planning estimate of the check after withholding, in about ten seconds.',pillars=['DEAL','RATE','WITHHELD','TAKE-HOME']),
  bands=[('how','Why the check is smaller than the math','''    <p class="lede">The commission in your plan and the money that hits your account are further apart than most sellers expect, especially the first time.</p>
    <p>The percentage you set aside is a planning buffer, not a withholding rate. For commissions paid separately from salary, the IRS lets employers withhold federal income tax at a flat 22% (up to a million dollars a year), and payroll taxes and state withholding come on top of that, so a W-2 check often lands with roughly 30% gone. High earners tend to owe closer to 40% once the year is reconciled. A 1099 contractor has nothing withheld and should set aside 20% or more. Your real number depends on your state, your filing status and everything else you earned this year, which is why the field is editable.</p>
    <p>Use it to plan, not to argue with payroll. Then ask the better question: is the comp plan itself sane? That's <a href="/quota/">Quota Check</a>.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The math runs right here in your browser. There\'s no account, and nothing goes to a server or your CRM. I count page views with Google Analytics, but it never sees your numbers, and nothing leaves the page unless you share a result.'),
       ('Is this tax advice?','No. It\'s just a planning buffer. Payroll and taxes are messier than this calculator. If the number actually matters, ask an accountant.'),
       ('What about accelerators and clawbacks?','Enter the rate that applies to this deal. If your plan has accelerators above quota, use the accelerated rate; if it has clawbacks, remember the take-home is provisional until the clawback window closes.')],
  config='''CalcTool({
  slug: 'commission', name: 'Commission Check', url: 'https://quotabird.com/commission/',
  fields: [{ id: 'deal', kind: 'money' }, { id: 'rate', kind: 'pct' }, { id: 'buffer', kind: 'pct' }],
  compute(v) {
    if (!(v.deal > 0 && v.rate > 0)) return null;
    const money = (n) => n >= 1e6 ? '$' + (n / 1e6).toFixed(2).replace(/\\.?0+$/, '') + 'M' : n >= 1e3 ? '$' + Math.round(n / 1e3).toLocaleString() + 'K' : '$' + Math.round(n).toLocaleString();
    const tax = v.buffer > 0 ? v.buffer : .30;
    const gross = v.deal * v.rate, aside = gross * tax, net = gross - aside;
    return { label: 'Take-home', cls: 'ready', big: money(net), attack: `Set aside ${Math.round(tax * 100)}% and you keep about ${Math.round((1 - tax) * 100)} cents of every commission dollar on this deal.`,
      sub: 'A planning buffer, not tax advice. Change the percentage to yours.', rows: [['Gross commission', money(gross)], ['Set aside, about', money(aside), 'v-no'], ['Take-home, about', money(net)]], keep: 1 - tax };
  },
  handoff: { overline: 'Is the plan sane?', text: 'Now that you know what a deal pays, check the number it has to cover.', href: '/quota/', label: 'Check my quota' },
  mark: { title: () => 'Questions about the plan?', body: "I'm Mark. Comp plans tell you what the company actually thinks your job is worth. If yours doesn't add up, send me a line about it, and leave out the company name and the dollars." },
  dm: (s) => `Mark, ran a deal through Commission Check. I keep about ${Math.round(s.keep * 100)}% of gross. The question is whether the plan behind it is sane. Worth 20 minutes?`,
  bookNote: (s) => `Commission Check: keeps about ${Math.round(s.keep * 100)}% of gross.`,
});'''),
]

def calc_page(t):
    def field(f):
        if f['kind'] == 'choice':
            chips = ''.join(f'<button class="chip{" on" if v == f["example"] else ""}" data-choice="{f["id"]}" data-v="{v}" type="button">{lab}</button>' for v, lab in f['options'])
            return f'        <div class="tf"><span class="tf-label">{f["label"]}</span><div class="chips" style="margin-top:6px;">{chips}</div></div>\n'
        mode = 'numeric' if f['kind'] == 'count' else 'decimal'
        val = f' value="{f["example"]}"' if f.get('example') else ''
        ph = f' placeholder="{f["placeholder"]}"' if f.get('placeholder') else ''
        out = f'        <label class="tf"><span class="tf-label">{f["label"]}</span><input id="{f["id"]}" type="text" inputmode="{mode}" autocomplete="off"{val}{ph}></label>\n'
        if f.get('presets'):
            out += '        <div class="chips" style="margin:-6px 0 14px;">' + ''.join(f'<button class="chip" data-preset-for="{f["id"]}" data-v="{v}" type="button">{lab}</button>' for lab, v in f['presets']) + '</div>\n'
        return out
    fields = ''.join(field(f) for f in t['fields'])
    faq_html = ''.join(f'''    <details class="exp"><summary>{q}</summary>
      <div class="body">{a}</div></details>
''' for q, a in t['faq'])
    faq_ld = ',\n'.join(json.dumps({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}}) for q, a in t['faq'])
    _mlink = {'quota': 'quota-to-ote', 'discount': 'discount-math', 'commission': 'commission-take-home'}.get(t['slug'])
    if _mlink: t = dict(t, bands=[(t['bands'][0][0], t['bands'][0][1], t['bands'][0][2] + f'\n    <p><a href="/math/{_mlink}/">The full math, with tables and sources →</a></p>')] + t['bands'][1:])
    bands = ''.join(f'''<section class="band" id="{i}">
  <div class="band-inner">
    <h2>{h}</h2>
{body}
  </div>
</section>

''' for i, h, body in t['bands'])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<link rel="preload" href="/inter.woff2" as="font" type="font/woff2" crossorigin>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="https://quotabird.com/{t['slug']}/">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="icon" type="image/png" sizes="64x64" href="../favicon.png">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:url" content="https://quotabird.com/{t['slug']}/">
<meta property="og:title" content="{t['name']}: {t.get('ogh1', t['h1'])}">
<meta property="og:description" content="{t['ogdesc']}">
<meta property="og:site_name" content="QuotaBird">
<meta property="og:image" content="https://quotabird.com/card-{t['slug']}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{t['name']}: {t.get('ogh1', t['h1'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t['name']}: {t.get('ogh1', t['h1'])}">
<meta name="twitter:description" content="{t['ogdesc']}">
<meta name="twitter:image" content="https://quotabird.com/card-{t['slug']}.jpg">
<meta name="twitter:image:alt" content="{t['name']}: {t.get('ogh1', t['h1'])}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#FFFFFF">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#101418">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{ "@type": "WebApplication", "name": "{t['name']}", "url": "https://quotabird.com/{t['slug']}/", "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
      "description": "{t['desc']}", "image": "https://quotabird.com/card-{t['slug']}.jpg", "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }},
      "isPartOf": {{ "@type": "WebSite", "name": "QuotaBird", "url": "https://quotabird.com/" }}, "author": {{ "@id": "https://quotabird.com/#about" }} }},
    {{ "@type": "FAQPage", "mainEntity": [
{faq_ld}
    ] }}
  ]
}}
</script>
<link rel="stylesheet" href="../site.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BG9NR9GXQZ"></script>
<script src="../analytics.js" defer></script>
</head>
<body class="wide-page">

<div class="wrap wide">
  <header class="appbar"></header>
  <div id="screen" class="calc-screen">
    <span class="overline tool-name">{t['name']}</span>
    <h1>{t['h1']}</h1>
    <p class="dek">{t['dek']}</p>
    <div class="calc">
      <div class="calc-out" id="out" aria-live="polite"></div>
      <form class="calc-in" id="f" autocomplete="off" novalidate>
        <p class="startnote fields-note"><span id="exnote">Example numbers. Type yours over them.</span></p>
{fields}      </form>
      <div class="calc-out2" id="out2"></div>
    </div>
  </div>
</div>

<div class="sumbar" id="sumbar" hidden aria-hidden="true"></div>

{bands}<section class="band" id="about"></section>

<section class="band" id="faq" aria-labelledby="faq-h">
  <div class="band-inner">
    <h2 id="faq-h">Questions</h2>
{faq_html}  </div>
</section>

<footer class="sitefoot">
  <a href="/">QuotaBird</a> is a pile of free sales tools. I built them because they helped me, and maybe they'll help you.
  <p>Not affiliated with the U.S. government or Amazon.</p>
</footer>
<script src="../calc.js"></script>
<script>
'use strict';
window.QB_BUILD = '{BUILD}';
{t['config']}
</script>
</body>
</html>
'''
for t in CALCS:
    os.makedirs(t['slug'], exist_ok=True)
    html = calc_page(t)
    assert '—' not in html and '–' not in html, t['slug']
    open(f"{t['slug']}/index.html", 'w').write(html)
    print('calc', t['slug'], len(html))



# ────────────────────────────── SALES MATH LIBRARY ──────────────────────────────
# Citation pages. Rule: the math needs no source; every benchmark needs one, and says where it came from.
# Mark's own ranges are labelled as experience, never as data. No invented statistics.
def _table(head, rows, note=''):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="mtable"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>' + (f'<p class="fine">{note}</p>' if note else '')
def _m(n):
    return f'${n/1e6:.1f}M'.replace('.0M', 'M') if n >= 1e6 else f'${round(n/1e3)}K'
WR = [.10, .15, .20, .25, .30, 1/3, .40, .50]
cov_rows = [[('33%' if abs(w - 1/3) < .001 else f'{round(w*100)}%'), f'{1/w:.1f}X' + (' <strong>(3X)</strong>' if abs(w - 1/3) < .001 else ''), _m(1e6/w), _m(1e7/w)] for w in WR]
RATES = [.005, .01, .02, .05, .10, .115, .15]
q_rows = [[f'{r*100:g}%', *[f'{s/r:.1f}×' if s/r < 10 else f'{round(s/r)}×' for s in (.40, .47, .50)]] for r in RATES]
MARG = [.30, .40, .60, .80]; DISC = [.05, .10, .15, .20, .25]
d_rows = [[f'{round(m*100)}%', *[f'{max(0, 1-(1-m)/(1-d))*100:.0f}%' for d in DISC]] for m in MARG]
c_rows = [[_m(g) if g >= 1e4 else f'${g:,.0f}', f'${g*.22:,.0f}', f'${g*.0765:,.0f}', f'${g*(1-.2965):,.0f}'] for g in (10000, 25000, 50000, 100000)]
MATH = [
 dict(slug='pipeline-coverage', title='How much pipeline do you actually need?',
  dek='Coverage is one divided by your qualified win rate. 3X assumes you win a third.',
  answer='Required pipeline coverage is 1 ÷ your qualified win rate. A 3X coverage ratio assumes a 33% win rate; at 20% you need 5X, at 25% you need 4X.',
  body=f'''    <p>People quote coverage ratios like they're laws. It's just arithmetic. If you close a fraction <em>w</em> of the
      qualified pipeline that's due in a period, the pipeline you need to make a number is the number divided by
      <em>w</em>. Coverage is that divided by the number, which leaves <strong>1 ÷ w</strong>.</p>
    <p>So 3X quietly assumes a 33% win rate. That's right for a team that wins a third of what it qualifies, and off for everyone else.</p>
    <h2>Coverage by win rate</h2>
    {_table(['Qualified win rate', 'Coverage needed', 'Pipeline for a $1M number', 'Pipeline for a $10M number'], cov_rows)}
    <h2>What the ratio assumes</h2>
    Qualified means qualified. If your win rate is based on qualified deals, count qualified pipeline. Mixing that with the whole CRM makes coverage look better than it is.
    <p><strong>Due in the period.</strong> Pipeline that closes next year doesn't cover this year, however real it is.</p>
    Use win rate by dollars, not deal count. Winning 30% of deals doesn't help if they're all the little ones.
    <h2>Worked example</h2>
    <p>A $6M number, a 20% qualified win rate. Coverage needed is 1 ÷ 0.20 = 5X, so the pipeline needed is $30M. A
      seller carrying $18M is at 3X, which looks covered, and is $12M short.</p>''',
  tool=('/pipeline/', 'Pipeline Check', 'runs this with your own number and win rate, and shows the 3X line and yours on one bar.'),
  sources=['The arithmetic on this page needs no source. The 3X convention is widespread in sales planning; this page explains what it assumes rather than endorsing it.']),
 dict(slug='quota-to-ote', title='What your quota-to-OTE ratio really says',
  dek='Quota ÷ OTE is your variable share divided by your commission rate. It\'s a pay rate in disguise.',
  answer='Quota ÷ OTE equals your variable share of OTE divided by your commission rate at 100% attainment. SaaS new-bookings plans cluster around 4×; cloud consumption plans, paid at a fraction of a percent, run far higher by design.',
  body=f'''    <p>Your commission at 100% attainment is your variable pay, and it equals your quota times your rate. Rearrange and
      <strong>quota ÷ OTE = (variable ÷ OTE) ÷ rate</strong>. The multiple everyone argues about is just the pay mix
      divided by the commission rate. Change what the rate is paid on, and the "normal" multiple changes with it.</p>
    <h2>Implied quota ÷ OTE, by rate and pay mix</h2>
    {_table(['Commission rate on quota', '40% variable', '47% variable', '50% variable'], q_rows, 'Each cell is variable share ÷ rate.')}
    <h2>The published SaaS benchmark</h2>
    <p>The most cited primary research on SaaS account executive pay is the Bridge Group's 2024 SaaS AE Metrics &amp;
      Compensation Report, drawn from more than 170 B2B SaaS companies. It puts median on-target earnings at $190K with a
      53:47 base-to-variable split. Summaries of the same report give a median commission rate of 11.5% of bookings and a
      median quota-to-OTE ratio of 4.2×.</p>
    <p>Those numbers check each other: 47% variable divided by an 11.5% rate is 4.1×, within rounding of the reported 4.2×. So the multiple comes straight out of the commission rate.</p>
    <h2>Why cloud and consumption plans look "crazy"</h2>
    <p>Sellers carrying consumption growth at a cloud provider are typically paid a fraction of a percent to a couple of
      percent on their number, not ten. Run that through the formula and the multiple lands at 20 to 50 times OTE, which
      is why a cloud AM compared against the SaaS benchmark looks wildly over-quota when the plan may be ordinary. This
      section is my experience across cloud providers and their partners, not published data; I haven't found a public
      dataset for consumption plans, and I'd rather say so than invent one.</p>''',
  tool=('/quota/', 'Quota Check', 'asks what your number is measured in and judges the multiple against the right range.'),
  sources=['Bridge Group, <a href="https://blog.bridgegroupinc.com/2024-ae-metrics-compensation-benchmark" rel="noopener">2024 SaaS AE Metrics &amp; Compensation Benchmark Report</a>: median OTE $190K, 53:47 split, 170+ companies.',
           'Median 11.5% commission rate and 4.2× quota-to-OTE from that report as summarized by <a href="https://optymyze.com/blog/sales-compensation-benchmarks/" rel="noopener">Optymyze</a> and <a href="https://getcarvd.com/blog/saas-sales-commission-rates" rel="noopener">Carvd</a>; the full report is gated.',
           'Cloud and consumption ranges: the author\'s experience, labelled as such.']),
 dict(slug='discount-math', title='What a discount really costs you and the company',
  dek='Commission falls at the rate of the discount. Margin falls faster, because cost doesn\'t move.',
  answer='A discount cuts your commission by exactly the discount percentage, and cuts gross margin to 1 − (1 − margin) ÷ (1 − discount). A 15% discount on a 40% margin leaves about 29%, not 25%.',
  body=f'''    <p>Two formulas, and the second is the one sellers get wrong.</p>
    Your commission. If you're paid a rate on the price, commission lost = rate × discount × list price. A 15% discount is a 15% pay cut on that deal.
    <p><strong>The company's margin.</strong> The cost of delivering the thing doesn't change when the price does. Margin
      after the discount is <strong>1 − (1 − m) ÷ (1 − d)</strong>, where m is the margin at list and d the discount.
      Every point of discount comes straight out of the margin, and the margin is measured against a smaller price.</p>
    <h2>Gross margin after a discount</h2>
    {_table(['Margin at list', '5% off', '10% off', '15% off', '20% off', '25% off'], d_rows)}
    <p>Read across the 30% row: a 25% discount leaves almost nothing. At high software margins the damage is smaller in
      percentage terms, which is exactly why software discounts get given so casually.</p>
    <h2>Worked example</h2>
    <p>A $500,000 deal at 40% margin, 8% commission, 15% off. The customer saves $75,000. Your commission drops from
      $40,000 to $34,000. The company's margin falls from 40% to 29%, and its gross profit on the deal from $200,000 to
      $125,000, a 37.5% drop for a 15% discount.</p>''',
  tool=('/discount/', 'Discount Check', 'does this for your deal before you agree to anything.'),
  sources=['The arithmetic on this page needs no source.']),
 dict(slug='commission-take-home', title='Why your commission check is smaller than the math',
  dek='Separately paid commissions are withheld at a flat 22% federal, before payroll and state taxes.',
  answer='US employers may withhold federal income tax on separately paid commissions at a flat 22% (37% on supplemental wages above $1 million in a year), plus 7.65% Social Security and Medicare, before any state tax. That\'s withholding, not the tax you finally owe.',
  body=f'''    <p>The IRS treats commissions and bonuses as supplemental wages. When they're paid separately from salary, employers
      can withhold federal income tax at a flat rate instead of running them through the normal tables. Social Security
      and Medicare come out on top, then your state, if it has an income tax.</p>
    <h2>Federal withholding and payroll tax, before state</h2>
    {_table(['Gross commission', 'Federal (22%)', 'Social Security + Medicare (7.65%)', 'Left before state tax'], c_rows,
            'Assumes supplemental wages under $1 million for the year and earnings under the Social Security wage base. Above the wage base, the 6.2% Social Security portion stops; above $200,000 in wages, an extra 0.9% Medicare applies.')}
    <p>That's where the rough 30% figure comes from: 22% plus 7.65% is 29.65% before any state tax. It's why Commission
      Check starts its set-aside at 30% for a W-2 seller.</p>
    <h2>What this calculator doesn't tell you</h2>
    <p>Withholding is just money collected along the way. What you actually owe gets sorted out when you file. This is a planning estimate, not tax advice. If the number matters, ask an accountant.</p>''',
  tool=('/commission/', 'Commission Check', 'estimates your take-home on a deal with a set-aside you can change.'),
  sources=['IRS, <a href="https://www.irs.gov/publications/p15" rel="noopener">Publication 15 (2026), Employer\'s Tax Guide</a>: supplemental wage withholding at 22%, or 37% on supplemental wages above $1 million in the calendar year.',
           'Social Security (6.2%) and Medicare (1.45%, plus 0.9% Additional Medicare Tax above $200,000) are the standard employee payroll tax rates described in the same publication.']),
]
def _cite(p): return f'QuotaBird, "{p["title"]}," quotabird.com/math/{p["slug"]}/ (updated {BUILD[:7]}).'
for p in MATH:
    url = f'https://quotabird.com/math/{p["slug"]}/'
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": p['title'], "description": p['answer'], "url": url,
                     "dateModified": BUILD[:10], "image": "https://quotabird.com/card.jpg",
                     "author": {"@type": "Person", "@id": "https://quotabird.com/#about", "name": "Mark Flournoy"},
                     "publisher": {"@type": "Organization", "name": "QuotaBird", "url": "https://quotabird.com/"}, "isPartOf": {"@type": "CreativeWorkSeries", "name": "QuotaBird Sales Math Library", "url": "https://quotabird.com/math/"}}, indent=2)
    href, name, line = p['tool']
    src = ''.join(f'<li>{s}</li>' for s in p['sources'])
    html = note_head(p['title'], p['answer'], url).replace('| QuotaBird</title>', '| QuotaBird Sales Math</title>') + f'''<script type="application/ld+json">
{ld}
</script>
</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note math">
  <span class="overline"><a href="/math/">Sales Math Library</a></span>
  <h1>{p['title']}</h1>
  <div class="answer"><span class="overline">The short answer</span><p>{p['answer']}</p></div>
{p['body']}
  <div class="card card-accent" style="margin-top:28px;">
    <span class="overline">Run your own</span>
    <p class="lede"><a href="{href}">{name}</a> {line}</p>
    <a class="btn btn-primary btn-full" href="{href}" style="margin-top:14px;">Try it</a>
  </div>
  <h2>Sources</h2>
  <ul class="sources">{src}</ul>
  <p class="fine cite">Cite this page: {_cite(p)}</p>
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL.replace('Field Notes are part of', 'The Sales Math Library is part of')
    assert '—' not in html and '–' not in html, p['slug']
    os.makedirs(f'math/{p["slug"]}', exist_ok=True)
    open(f'math/{p["slug"]}/index.html', 'w').write(html)
_mlist = '<div class="doors">' + ''.join(f'<a class="door" href="/math/{p["slug"]}/"><span><b>{p["title"]}</b><span class="q">{p["dek"]}</span></span><span class="to">Read</span></a>' for p in MATH) + '</div>'
os.makedirs('math', exist_ok=True)
open('math/index.html', 'w').write(note_head('Sales Math Library', 'The arithmetic behind pipeline coverage, quota-to-OTE, discounts and commission, shown step by step, with sources for every benchmark.', 'https://quotabird.com/math/').replace('| QuotaBird</title>', '| QuotaBird</title>') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note">
  <span class="overline">QuotaBird</span>
  <h1>Sales Math Library</h1>
  <p class="dek">The arithmetic behind the checks, shown step by step. The math needs no source; every benchmark has one,
    and anything that's my own experience says so.</p>
  ''' + _mlist + '''
  <p class="fine" style="margin-top:18px;">Coming when I find data I trust: federal sales-cycle lengths by agency and contract vehicle.</p>
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL.replace('Field Notes are part of', 'The Sales Math Library is part of'))
print('math', len(MATH))


# ────────────────────────────── THE MANAGER'S FIELD KIT (/kit/) ──────────────────────────────
# A free printable. Plain voice: a retired sales guy who has signed on to a few dumpster fires.
# No travel theme, no methodology, no email gate. Print CSS turns it into a clean PDF.
KIT_BODY = '''
  <section class="kit-ch" id="k-start">
    <p>I've taken over teams that were doing great, teams that were struggling, and a few that were already on fire
      when I got there. Some I fixed. A couple I made worse before I made them better.</p>
    <p>No management methodology here, and no certification at the end. Just the stuff that kept being useful: figuring out whether the problem is the rep or the territory, getting an honest forecast, knowing if there's really enough pipeline, helping a rep who's struggling, defending your people at review time, and keeping your boss from getting surprised.</p>
    <p>Don't read it front to back. <strong>Find the problem you have this week and start there.</strong> Each chapter
      ends with the worksheet that goes with it.</p>
    <div class="kit-start">
      <p class="kit-start-h">Having a bad week? Start here.</p>
      <ul>
        <li><a href="#k-first">Rep problem</a><span>Chapter 1 or 6</span></li>
        <li><a href="#k-forecast">Forecast problem</a><span>Chapter 3</span></li>
        <li><a href="#k-pipeline">Pipeline problem</a><span>Chapter 4</span></li>
        <li><a href="#k-boss">Boss problem</a><span>Chapter 5</span></li>
        <li><a href="#k-review">Review season</a><span>Chapter 7</span></li>
        <li><a href="#k-alone">High performers</a><span>Chapter 10</span></li>
      </ul>
    </div>
  </section>

  <section class="kit-ch" id="k-first">
    <h2>1. You inherited a team. Don't grade everybody yet.</h2>
    <p>My first mistake as a new manager was deciding pretty quickly who was good and who wasn't. I got a lot of that wrong, mostly because I hadn't looked at their territories yet.</p>
    <p>Before I decide a rep has a performance problem, I want to know whether the territory is any good, what's
      installed already, whether the quota is remotely reasonable, what the last rep did there, what the comp plan
      rewards, and whether there are enough customers who can buy what we sell.</p>
    <p>If three good people failed in the same territory, I start with the territory.</p>
    <p>Then I look at the rep, and I mean the rep, before the CRM. Do customers want to spend time with them? Have they created anything that wouldn't exist without them? Can they sell when they're in the room? Are they still trying?</p>
    <p>The most useful thing I did with a new team was sit with each rep and go through five real deals. Every once in a while, the rep who drives you nuts internally is the one customers keep calling back.</p>
    My first month. Week 1: meet everybody, ask what they'd change. Week 2: size the territories. Week 3: sit in deals and customer calls. Week 4: tell your boss what you found.
    <div class="sheet">
      <h3>Worksheet: Rep diagnostic</h3>
      <p class="sheet-meta">Rep ____________________ &nbsp; Date __________ &nbsp; <span class="sheet-tool">Online: quotabird.com/rep</span></p>
      <div class="mtable"><table class="ws"><thead><tr><th>In this order</th><th>Yes / Sort of / No</th><th>Notes</th></tr></thead><tbody>
        <tr><td>Territory: could a good rep make this number here?</td><td></td><td></td></tr>
        <tr><td>Customers: do they want time with this rep?</td><td></td><td></td></tr>
        <tr><td>Pipeline: is there pipeline only this rep created?</td><td></td><td></td></tr>
        <tr><td>Craft: can they sell in the room?</td><td></td><td></td></tr>
        <tr><td>Will: are they still trying to win?</td><td></td><td></td></tr>
      </tbody></table></div>
      <p class="sheet-foot">Territory is no: fix the situation. Craft is no: coach. Will is no: manage. If both are no in a fair territory, read chapter 6.</p>
    </div>
  </section>

  <section class="kit-ch" id="k-rhythm">
    <h2>2. Keep the 1:1 and the forecast call separate</h2>
    <p>A 1:1 and a forecast call aren't the same meeting. The 1:1 is about the person and the forecast call is about the number, and whenever I mixed them, both got worse.</p>
    <p>My 1:1 was usually thirty minutes, and the rep went first. What are they working on? What's getting in their
      way? What am <em>I</em> doing that's getting in their way? Then we look at one real deal properly.</p>
    <p>I finish with one thing I saw them do well, one thing I'd try differently, and anything I said I'd do. I write down what I committed to and then actually do it, which built more trust than anything else I tried.</p>
    <p>Once a month I'd ask, "If you were running this team, what would you change?" You'll hear things nobody says in
      the staff meeting.</p>
    <p>If people only bring you good news, you'll hear the bad news from your boss first. I want to hear "this deal is slipping" on Monday. If reps keep deals green until Friday, they're afraid of the meeting, and that's usually on the manager.</p>
    <div class="sheet">
      <h3>Worksheet: One-on-one</h3>
      <p class="sheet-meta">Rep ____________________ &nbsp; Date __________</p>
      <p class="sheet-label">Their list: what's in their way, including me</p><div class="lines l3"></div>
      <p class="sheet-label">One deal: customer, money, power, path, now</p><div class="lines l3"></div>
      <p class="sheet-label">One thing they did well, one thing to try</p><div class="lines l2"></div>
      <p class="sheet-label">What I said I'd do, and by when</p><div class="lines l2"></div>
    </div>
  </section>

  <section class="kit-ch" id="k-forecast">
    <h2>3. What commit means</h2>
    <p>To me, commit means the customer could explain how the money gets from them to us, and roughly when. Anything less is a guess. Most shaky deals break in one of five places:</p>
    <div class="mtable"><table><thead><tr><th>Where it breaks</th><th>What I'm really asking</th></tr></thead><tbody>
      <tr><td>Customer</td><td>Do they actually want to solve this?</td></tr>
      <tr><td>Money</td><td>Is there real money attached to it?</td></tr>
      <tr><td>Power</td><td>Are we connected to somebody who can make it happen?</td></tr>
      <tr><td>Path</td><td>Do we know how they actually buy?</td></tr>
      <tr><td>Now</td><td>Why does anything happen this period?</td></tr>
    </tbody></table></div>
    <p>The best forecast question I know is still <strong>"Who told you that?"</strong> Not "what do you think," not "how
      confident are you." Who told you, and when? A named customer and a date beats enthusiasm every time. I've
      forecast plenty of enthusiasm. It has a terrible close rate.</p>
    <p>When a rep and I disagree, I ask which of the five they'd defend to my boss, and we forecast that. Nobody has to lose face.</p>
    <p>One question I ask a lot: what changed? If nothing changed at the customer, the deal didn't move, whatever the CRM says.</p>
    <div class="sheet">
      <h3>Worksheet: Deal inspection</h3>
      <p class="sheet-meta">Deal ____________________ &nbsp; Rep ______________ &nbsp; <span class="sheet-tool">Online: quotabird.com/deal</span></p>
      <div class="mtable"><table class="ws"><thead><tr><th>Question</th><th>Yes / Sort of / No</th><th>Who said so, and when</th></tr></thead><tbody>
        <tr><td>Customer: have they said they want to solve this?</td><td></td><td></td></tr>
        <tr><td>Money: does it have a name and a fiscal year?</td><td></td><td></td></tr>
        <tr><td>Power: have we met who can make it happen?</td><td></td><td></td></tr>
        <tr><td>Path: do we know the vehicle and the approvals?</td><td></td><td></td></tr>
        <tr><td>Now: what makes it happen this period?</td><td></td><td></td></tr>
      </tbody></table></div>
      <p class="sheet-foot">I only call it commit with five answers I'd defend to my boss.</p>
    </div>
  </section>

  <section class="kit-ch" id="k-pipeline">
    <h2>4. Pipeline has two jobs</h2>
    <p>Managers usually ask, "Do we have enough pipeline?" I'd ask one more: will it survive your champion leaving? Different question.</p>
    <p><strong>Enough.</strong> The 3X rule everybody repeats assumes roughly a 33% win rate. The math is simple:
      coverage needed is one divided by your win rate. Use your own team's qualified win rate.</p>
    <div class="mtable kit-small"><table><thead><tr><th>Win rate</th><th>Coverage needed</th></tr></thead><tbody>
      <tr><td>15%</td><td>6.7X</td></tr><tr><td>20%</td><td>5.0X</td></tr><tr><td>25%</td><td>4.0X</td></tr>
      <tr><td>33%</td><td>3.0X</td></tr><tr><td>40%</td><td>2.5X</td></tr>
    </tbody></table></div>
    <p><strong>Sturdy.</strong> A team can have 4X coverage and still be in trouble. So I also ask what happens if our
      biggest deal slips, whether the commit deals are moving, whether each one has a next step the customer
      owns, how much is back-loaded into the last month, and whether we're creating new pipeline or just aging the old
      stuff.</p>
    <p>Run the forecast once without your biggest deal. That's the plan I'd manage.</p>
    <div class="sheet">
      <h3>Worksheet: Team pipeline</h3>
      <p class="sheet-meta">Quarter __________ &nbsp; Date __________ &nbsp; <span class="sheet-tool">Online: quotabird.com/pipeline</span></p>
      <div class="mtable"><table class="ws wide"><thead><tr><th>Rep</th><th>Number</th><th>Qualified pipeline</th><th>Win rate</th><th>Coverage needed (1 ÷ win rate)</th><th>Coverage now</th><th>Biggest deal</th></tr></thead><tbody>
        <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      </tbody></table></div>
      <p class="sheet-foot">If one deal is carrying a big chunk of the number, know exactly what happens if it moves.</p>
    </div>
  </section>

  <section class="kit-ch" id="k-boss">
    <h2>5. Your boss mostly wants fewer surprises</h2>
    <p>Early on I kept sending my boss more information, when mostly they just didn't want to be surprised.</p>
    <p>My update fits on one page: the number (commit, best case, gap), what changed and why, what worries me, what I'm
      doing about it, and one ask with a date. Or "nothing this week." And I lead with the bad news. "Heads up before
      this shows up in the CRM" beats letting your boss discover it.</p>
    <p>I learned another one the expensive way. When somebody above me handed me a number I couldn't see, I used to
      say, "We'll find a way." Sometimes we did. Sometimes I spent the rest of the year explaining that sentence. Now
      I'd say, "Here's what I can commit to with what we have. Here's what would have to be true to get to your
      number." Then I show the math. Longer version: <a href="/notes/prove-the-quota-is-crazy/">quotabird.com/notes/prove-the-quota-is-crazy</a></p>
    <div class="sheet">
      <h3>Worksheet: The five-minute boss update</h3>
      <p class="sheet-meta">Week of __________</p>
      <div class="mtable"><table class="ws"><tbody>
        <tr><td>Commit</td><td></td></tr><tr><td>Best case</td><td></td></tr><tr><td>Gap</td><td></td></tr>
      </tbody></table></div>
      <p class="sheet-label">What changed, and why</p><div class="lines l2"></div>
      <p class="sheet-label">Biggest risk</p><div class="lines l2"></div>
      <p class="sheet-label">What I'm doing about it</p><div class="lines l2"></div>
      <p class="sheet-label">What I need from you, and by when</p><div class="lines l1"></div>
    </div>
  </section>

  <section class="kit-ch" id="k-rep">
    <h2>6. Before you write up a rep</h2>
    <p>Four very different problems can produce the same ugly dashboard.</p>
    <div class="mtable"><table><thead><tr><th>Problem</th><th>What it looks like</th><th>What I do</th></tr></thead><tbody>
      <tr><td>Bad situation</td><td>Good rep. Bad territory, quota, accounts or plan.</td><td>Fix the situation.</td></tr>
      <tr><td>Skill</td><td>They're working, customers engage, deals just aren't converting.</td><td>Coach. Sit in the room.</td></tr>
      <tr><td>Effort</td><td>They know how to sell. They're just not doing enough of it.</td><td>Set expectations clearly, in writing, with dates.</td></tr>
      <tr><td>Wrong fit</td><td>Fair territory, enough support, and neither the skill nor the effort is there.</td><td>Now it's a performance conversation.</td></tr>
    </tbody></table></div>
    <p>Before I call it a performance problem, I make sure the rep knows what good looks like next Tuesday, not someday. I spent months once coaching somebody whose territory couldn't have produced the number. I'd like those months back. So would the rep.</p>
    <p class="sheet-tool">The rep diagnostic is in chapter 1. Online: quotabird.com/rep</p>
  </section>

  <section class="kit-ch" id="k-review">
    <h2>7. Review season: bring receipts</h2>
    <p>Nobody in the calibration room saw your rep's whole year. They saw whatever case you brought in. That took me too long to figure out.</p>
    <p>I keep a running note during the year: date, what happened, result. Nothing elaborate. Then I'm not digging through six months of email and Slack in November.</p>
    <p>For each rep I want three meaningful results (with numbers where numbers make sense), what happened because this
      person was there, why the work was at their level, specific examples behind any behavior I'm going to claim, and
      the harder thing I'd trust them with next.</p>
    <p>I say the weakest part of my case first, since they'll find it anyway.</p>
    <p>I also check myself. Am I overweighting the last sixty days? Would I see this person differently if I didn't
      personally like working with them? Take away their biggest win: does my view hold? Take away their worst month:
      same question.</p>
    <div class="sheet">
      <h3>Worksheet: Talent review prep</h3>
      <p class="sheet-meta">Rep ____________________ &nbsp; Level ______ &nbsp; <span class="sheet-tool">Online: quotabird.com/talent-review</span></p>
      <p class="sheet-label">Three results, with numbers where they make sense</p><div class="lines l2"></div>
      <p class="sheet-label">What happened because this person was there</p><div class="lines l1"></div>
      <p class="sheet-label">Why the work was at their level</p><div class="lines l1"></div>
      <p class="sheet-label">Examples behind each behavior I'll claim</p><div class="lines l2"></div>
      <p class="sheet-label">The harder thing I'd trust them with next</p><div class="lines l1"></div>
      <p class="sheet-label">The weakest part of this case, said first</p><div class="lines l1"></div>
    </div>
  </section>

  <section class="kit-ch" id="k-mistakes">
    <h2>8. Things I learned the expensive way</h2>
    <ul class="kit-list">
      Managing the dashboard. The CRM got cleaner and the pipeline stayed flat.
      <li><strong>Saving the deal myself.</strong> Worked great once. Then the rep learned to wait for me.</li>
      <li><strong>Managing the average.</strong> Two reps at 6X and two at 1X isn't a healthy team at 3.5X.</li>
      <li><strong>Forecasting confidence.</strong> Some people sound sure about everything. I don't count that as evidence.</li>
      <li><strong>Waiting to deliver bad news.</strong> I wanted the fix before I told my boss. They'd have preferred the news Monday and the fix Friday.</li>
      <li><strong>Giving everyone the same 1:1.</strong> My best seller and my newest seller needed completely different things from those thirty minutes.</li>
      <li><strong>Discounting the wrong problem.</strong> I approved a discount when the real issue was access to power. We solved a price problem the customer didn't have.</li>
      <li><strong>Talking too much on customer calls.</strong> I thought I was helping the rep. Mostly I was teaching the customer to look at me instead of them.</li>
      Being the answer machine. Eventually people brought me every problem and stopped deciding anything.
    </ul>
  </section>

  <section class="kit-ch" id="k-lines">
    <h2>9. A few lines worth stealing</h2>
    <div class="mtable"><table><thead><tr><th>When</th><th>What I say</th></tr></thead><tbody>
      <tr><td>A shaky deal</td><td>"Who told you that, and when?"</td></tr>
      <tr><td>Moving something out of commit</td><td>"Which part would you defend to my boss?"</td></tr>
      <tr><td>A rep is missing</td><td>"Forget the number for a minute. What's getting in your way?"</td></tr>
      <tr><td>The target from above doesn't match reality</td><td>"Here's what I can commit to with what I have. Here's what has to change to get to that."</td></tr>
      <tr><td>Bad news</td><td>"Heads up before this lands in the CRM."</td></tr>
      <tr><td>A discount request</td><td>"What are we getting for it?"</td></tr>
      <tr><td>A hard performance conversation</td><td>"Here's what good looks like thirty days from now."</td></tr>
      <tr><td>You don't know</td><td>"I don't know. I'll find out by Thursday." Then find out by Thursday.</td></tr>
    </tbody></table></div>
  </section>

  <section class="kit-ch" id="k-alone">
    <h2>10. Managing high performers</h2>
    <p>The easiest way to lose a great seller is to manage them like everybody else. I've done it.</p>
    <p>Mostly, I leave them alone. When customers call them back, they build their own pipeline and they tell me bad
      news before I find it, the system is working. My job is a fair territory, clearing what slows them down, helping
      when they ask, and keeping the rest of the company from improving them to death.</p>
    <p>And don't punish them for being good. The reward for making the number shouldn't be a bigger
      number, three accounts nobody else could handle, and coaching the new hires on their own time.</p>
    <p>Once a quarter I ask three things. What would make this job better? What do you want to be doing in two years?
      What am I asking of you that isn't worth your time? Then I act on at least one answer. Great sellers rarely leave
      over money alone. They leave when nobody noticed they were bored.</p>
  </section>
'''
KIT_CTA = '''
  <section class="kit-cta" aria-labelledby="kit-cta-h">
    <h2 id="kit-cta-h">Sometimes you just need another set of eyes</h2>
    <p>I'm Mark. I spent six years leading federal partner sales teams at AWS, after plenty of years carrying a number myself. If you're staring at a deal, a forecast, a rep problem or a number that doesn't make sense, tell me about it.</p>
    <p class="kit-cta-terms">A free twenty-minute call, no pitch.</p>
    <div class="btn-row kit-cta-row">
      <a class="btn btn-primary btn-lg" id="kitBook" href="https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&amp;utm_medium=kit&amp;utm_content=kit_cta" target="_blank" rel="noopener">Chat with Mark</a>
      <a class="btn btn-lg" href="https://www.linkedin.com/in/markflournoy/" target="_blank" rel="noopener">DM on LinkedIn</a>
    </div>
    <p class="kit-bridge">Used this with your team and found something ugly? That's <a href="/ask/">most of the stuff I help managers with</a>.</p>
    <p class="fine">Or email me: <a href="mailto:mark@quotabird.com">mark@quotabird.com</a>. And if I don't think I can help, I'll tell you.</p>
  </section>
'''
_kit_url = 'https://quotabird.com/kit/'
_kit_desc = "Useful things for the weeks when the number, the team, or both are giving you trouble. A free, printable field kit for sales managers: inheriting a team, one-on-ones, the forecast call, pipeline, your boss, a struggling rep, review season, and the worksheets that go with them."
_kit_ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": "The Manager's Field Kit", "description": _kit_desc, "url": _kit_url, "isAccessibleForFree": True,
                      "dateModified": BUILD[:10], "image": "https://quotabird.com/card-kit.jpg", "author": {"@type": "Person", "@id": "https://quotabird.com/#about", "name": "Mark Flournoy"},
                      "publisher": {"@type": "Organization", "name": "QuotaBird", "url": "https://quotabird.com/"}}, indent=2)
_kit = note_head("The Manager's Field Kit", _kit_desc, _kit_url).replace("| QuotaBird</title>", "| Free Printable | QuotaBird</title>").replace("https://quotabird.com/card.jpg", "https://quotabird.com/card-kit.jpg").replace('<meta name="twitter:card"', '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="The Manager\'s Field Kit: a free, printable field kit for sales managers">\n<meta name="twitter:card"') + f'''<script type="application/ld+json">
{_kit_ld}
</script>
</head>
<body class="kit-page">

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note kit">
  <span class="overline">Free printable</span>
  <h1>The Manager's Field Kit</h1>
  <p class="dek">Useful things for the weeks when the number, the team, or both are giving you trouble.</p>
  <div class="kit-promo kit-hero">
    <div class="kit-thumb" aria-hidden="true">
      <img class="kt-back" src="/kit/preview-2.jpg" alt="" width="480" height="622" decoding="async">
      <img class="kt-front" src="/kit/preview-1.jpg" alt="" width="480" height="622" decoding="async">
    </div>
    <div class="kit-promo-body">
      <span class="pill">Free printable</span>
      <p class="kit-hero-meta">8 pages, prints on letter or A4. Ten short chapters and six worksheets.</p>
      <div class="kit-promo-actions">
        <a class="btn btn-primary btn-lg btn-icon" id="kitBookDl" href="/kit/managers-field-kit.pdf" download>Download the PDF<svg aria-hidden="true" viewBox="0 -960 960 960" width="20" height="20"><path fill="currentColor" d="M480-320 280-520l56-58 104 104v-326h80v326l104-104 56 58-200 200ZM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160H240Z"/></svg></a>
        <button class="btn btn-text" id="kitPrint" type="button">Print this page</button>
      </div>
    </div>
  </div>
{KIT_BODY}
{KIT_CTA}
  <div class="kit-next"><span class="overline">Next</span><p>Want other managers calling you when they've got a mess? <a href="/leader/">The Leadership Field Kit</a> is the one for that.</p></div>
</article>

''' + NOTE_TAIL.replace('Field Notes are part of', "The Manager's Field Kit is part of").replace('</script>\n</body>', """document.getElementById('kitPrint').addEventListener('click', function () { if (window.qbTrack) window.qbTrack('kit_print'); window.print(); });
document.getElementById('kitBook').addEventListener('click', function () { if (window.qbTrack) window.qbTrack('kit_book'); });
</script>
</body>""")
assert '—' not in _kit and '–' not in _kit
os.makedirs('kit', exist_ok=True)
open('kit/index.html', 'w').write(_kit)
print('kit', len(_kit))


LEADER_PAGES = '3'   # set from the rendered PDF; see the handoff
# ────────────────────────────── THE LEADER'S FIELD KIT (/leader/) ──────────────────────────────
# The sibling of the Manager's kit, for managers who want to be the person other managers call.
# Same voice and print rules. No invented career stories: general observations only, so Mark can add his own.
LEADER_BODY = '''
  <section class="kit-ch" id="l-start">
    <p>Eventually running your own team well isn't enough. You want to help other managers, have a say in how things get done, and get pulled into bigger problems.</p>
    <p>I hate the phrase "personal brand." This isn't that. Do good work, figure out what you actually believe, and make the useful parts easy for other people to steal.</p>
    Do enough useful stuff that people mention your name when you're not there.
  </section>

  <section class="kit-ch" id="l-known">
    <h2>1. What do you want to be known for?</h2>
    <p>"Leadership" isn't a thing to be known for. Neither is "strategic." Pick something real: fixing bad territories, building a partner motion, getting new managers productive, selling into federal health.</p>
    <p>Pick one. You can add more later. It should be specific enough that somebody could say, "If you've got a problem with ______, call her."</p>
    <p>If your boss had one sentence to describe you to another leader today, what would it be? If you don't like the sentence, that's the work.</p>
  </section>

  <section class="kit-ch" id="l-receipts">
    <h2>2. Where are your receipts?</h2>
    <p>Nobody remembers your whole year. Keep receipts: date, what you changed, what happened.</p>
    <p>At the next level, "my team hit 112%" is good. Better is something you built that other people started using, or a rep you developed who now runs a team.</p>
  </section>

  <section class="kit-ch" id="l-believe">
    <h2>3. What do you believe that's actually yours?</h2>
    <p>Most good managers have a point of view. A lot of them have never bothered to write it down.</p>
    <p>Write down three things you believe about running a sales team now that you didn't five years ago. They don't need to sound profound. "Most forecast misses are path problems" works. "Communication matters" doesn't.</p>
    <p>Pick the one you'd argue for in a room full of people who disagree. Write that one.</p>
    <div class="sheet">
      <h3>Worksheet: My point of view</h3>
      <p class="sheet-label">Three things I believe now that I didn't five years ago</p><div class="lines l3"></div>
      <p class="sheet-label">The one I'd defend in a room that disagrees</p><div class="lines l1"></div>
      <p class="sheet-label">The evidence I'd bring</p><div class="lines l2"></div>
      <p class="sheet-label">Who disagrees, and where they're partly right</p><div class="lines l2"></div>
    </div>
  </section>

  <section class="kit-ch" id="l-build">
    <h2>4. Build something other managers can borrow</h2>
    <p>If you do something well, write down how you do it and give it away. Your forecast call. Your first thirty days with a new rep. A hiring scorecard. Whatever people keep asking you about.</p>
    <p>It doesn't need to be pretty. It needs to be useful enough that another manager uses it next week.</p>
    <p>Then teach it. Thirty minutes at a leadership meeting, lunch with two newer managers, a session at kickoff. Teaching also tells you pretty quickly whether you actually know it.</p>
  </section>

  <section class="kit-ch" id="l-rooms">
    <h2>5. Get into the right rooms</h2>
    <p>Start close to the work: your boss, your boss's peers, and the leaders you depend on in partners, marketing, finance and customer success. Then go wider.</p>
    <p>The rooms you want are the ones where somebody is making decisions about your world without you: territories, headcount, your team's story, customers, industry stuff. Quota planning is the big one. How to walk in with the math: <a href="/notes/prove-the-quota-is-crazy/">quotabird.com/notes/prove-the-quota-is-crazy</a></p>
    <p>Usually the way in is simple: help somebody who's already in the room. Bring the template, the analysis, or the answer they keep getting asked for.</p>
  </section>

  <section class="kit-ch" id="l-behind">
    <h2>6. Bring people up behind you</h2>
    <p>If your people keep getting promoted, people notice. It's hard to fake that one.</p>
    <p>Know who on your team could run a team. Give them the harder work. Put them in front of your boss. If they get promoted, that goes on your record.</p>
    <div class="sheet">
      <h3>Worksheet: A year from now</h3>
      <p class="sheet-label">I want people to call me when they need help with</p><div class="lines l1"></div>
      <p class="sheet-label">Three things I know unusually well</p><div class="lines l3"></div>
      <p class="sheet-label">One point of view I'm willing to defend</p><div class="lines l1"></div>
      <p class="sheet-label">One thing I could teach other managers</p><div class="lines l1"></div>
      <p class="sheet-label">One useful thing I could publish or share</p><div class="lines l1"></div>
      <p class="sheet-label">Five peers I'd like to know better</p><div class="lines l1"></div>
      <p class="sheet-label">One room I'm not in yet, but should be</p><div class="lines l1"></div>
    </div>
    Don't try to manufacture recognition. Do good work. Leave useful stuff behind. Eventually people start mentioning you before you walk in.
  </section>
'''
LEADER_CTA = '''
  <section class="kit-cta" aria-labelledby="leader-cta-h">
    <h2 id="leader-cta-h">Sometimes you just need another set of eyes</h2>
    <p>I'm Mark. I spent six years leading federal partner sales teams at AWS, after plenty of years carrying a number myself. If you've got something you need to defend to your VP, send it over and we can talk it through.</p>
    <p class="kit-cta-job">If this gets you into one better room, good enough.</p>
    <p class="kit-cta-terms">A free twenty-minute call, no pitch.</p>
    <div class="btn-row kit-cta-row">
      <a class="btn btn-primary btn-lg" id="leaderBook" href="https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&amp;utm_medium=leader&amp;utm_content=leader_cta" target="_blank" rel="noopener">Chat with Mark</a>
      <a class="btn btn-lg" href="https://www.linkedin.com/in/markflournoy/" target="_blank" rel="noopener">DM on LinkedIn</a>
    </div>
    <p class="kit-bridge">Used this with your team and found something ugly? That's <a href="/ask/">most of the stuff I help managers with</a>.</p>
    <p class="fine">Or email me: <a href="mailto:mark@quotabird.com">mark@quotabird.com</a>. And if I don't think I can help, I'll tell you.</p>
  </section>
'''
_ld_url = 'https://quotabird.com/leader/'
_ld_sub = "For managers who want other leaders to call them when they've got a mess."
_ld_desc = "For managers who want other leaders to call them when they've got a mess. A free, printable field kit: what you want to be known for, your point of view, your receipts, what others can borrow, the right rooms, and the people behind you."
_ld_ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": "The Leadership Field Kit", "description": _ld_desc, "url": _ld_url, "isAccessibleForFree": True,
                     "dateModified": BUILD[:10], "image": "https://quotabird.com/card-leader.jpg", "author": {"@type": "Person", "@id": "https://quotabird.com/#about", "name": "Mark Flournoy"},
                     "publisher": {"@type": "Organization", "name": "QuotaBird", "url": "https://quotabird.com/"}}, indent=2)
_DL_ICON = '<svg aria-hidden="true" viewBox="0 -960 960 960" width="20" height="20"><path fill="currentColor" d="M480-320 280-520l56-58 104 104v-326h80v326l104-104 56 58-200 200ZM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160H240Z"/></svg>'
_leader = note_head("The Leadership Field Kit", _ld_desc, _ld_url).replace("| QuotaBird</title>", "| Free Printable | QuotaBird</title>").replace("https://quotabird.com/card.jpg", "https://quotabird.com/card-leader.jpg").replace('<meta name="twitter:card"', '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="The Leadership Field Kit: a free, printable field kit for sales managers who want to lead">\n<meta name="twitter:card"') + f'''<script type="application/ld+json">
{_ld_ld}
</script>
</head>
<body class="kit-page">

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note kit">
  <span class="overline">Free printable</span>
  <h1>The Leadership Field Kit</h1>
  <p class="dek">{_ld_sub}</p>
  <div class="kit-promo kit-hero">
    <div class="kit-thumb" aria-hidden="true">
      <img class="kt-back" src="/leader/preview-2.jpg" alt="" width="480" height="622" decoding="async">
      <img class="kt-front" src="/leader/preview-1.jpg" alt="" width="480" height="622" decoding="async">
    </div>
    <div class="kit-promo-body">
      <span class="pill">Free printable</span>
      <p class="kit-hero-meta">__PAGES__ pages, prints on letter or A4. Six short chapters and two worksheets.</p>
      <div class="kit-promo-actions">
        <a class="btn btn-primary btn-lg btn-icon" href="/leader/leader-field-kit.pdf" download>Download the PDF{_DL_ICON}</a>
        <button class="btn btn-text" id="kitPrint" type="button">Print this page</button>
      </div>
    </div>
  </div>
{LEADER_BODY}
{LEADER_CTA}
</article>

''' + NOTE_TAIL.replace('Field Notes are part of', "The Leadership Field Kit is part of").replace('</script>\n</body>', """document.getElementById('kitPrint').addEventListener('click', function () { if (window.qbTrack) window.qbTrack('leader_print'); window.print(); });
document.getElementById('leaderBook').addEventListener('click', function () { if (window.qbTrack) window.qbTrack('leader_book'); });
</script>
</body>""")
_leader = _leader.replace('__PAGES__', LEADER_PAGES)
assert '—' not in _leader and '–' not in _leader
os.makedirs('leader', exist_ok=True)
open('leader/index.html', 'w').write(_leader)
print('leader kit', len(_leader))


SELLER_PAGES = '4'   # set from the rendered PDF
# ────────────────────────────── THE SELLER'S FIELD KIT (/seller/) ──────────────────────────────
# Bottom rung of the ladder: carry the number. Not sales training; what a working seller reaches for in a bad week.
SELLER_BODY = '''
  <section class="kit-ch" id="s-start">
    <p>Some weeks the customer goes quiet, the number looks worse than it did Monday, and your boss wants an update you don't have. This is for those weeks.</p>
    <p>No sales methodology here. Just the handful of things I reached for when a quarter was going sideways, and a
      few I wish I'd reached for sooner. <strong>Find the problem you have this week and start there.</strong></p>
    <div class="kit-start">
      <p class="kit-start-h">Having a bad week? Start here.</p>
      <ul>
        <li><a href="#s-deal">Is it a real deal?</a><span>Chapter 1</span></li>
        <li><a href="#s-pipe">Not enough pipeline</a><span>Chapter 2</span></li>
        <li><a href="#s-big">One deal carries it</a><span>Chapter 3</span></li>
        <li><a href="#s-thread">Only one contact</a><span>Chapter 4</span></li>
        <li><a href="#s-disc">Discount request</a><span>Chapter 5</span></li>
        <li><a href="#s-quiet">Deal went quiet</a><span>Chapter 6</span></li>
        <li><a href="#s-behind">Behind the number</a><span>Chapter 7</span></li>
        <li><a href="#s-mgr">Your manager</a><span>Chapter 8</span></li>
      </ul>
    </div>
  </section>

  <section class="kit-ch" id="s-deal">
    <h2>1. Is this actually a deal?</h2>
    <p>Most deals that fall out of the forecast were never really in it. They break in one of five places. Has the
      customer said, in their words, that they want to solve this? Does the money have a name: a budget line, a program,
      a fiscal year? Have you met someone who can sign, or just someone who likes you? Do you know how they'll
      actually buy it? And what makes it happen this period instead of next?</p>
    <p>If you can answer all five with a name and a date, you've got a deal. Otherwise it's still a conversation, and I wouldn't forecast it yet.</p>
    <div class="sheet">
      <h3>Worksheet: Deal inspection</h3>
      <p class="sheet-meta">Deal ____________________ &nbsp; Date __________ &nbsp; <span class="sheet-tool">Online: quotabird.com/deal</span></p>
      <div class="mtable"><table class="ws"><thead><tr><th>Question</th><th>Yes / Sort of / No</th><th>Who told me, and when</th></tr></thead><tbody>
        <tr><td>Customer: have they said they want to solve this?</td><td></td><td></td></tr>
        <tr><td>Money: does it have a name and a fiscal year?</td><td></td><td></td></tr>
        <tr><td>Power: have I met who can make it happen?</td><td></td><td></td></tr>
        <tr><td>Path: do I know how they'll buy it?</td><td></td><td></td></tr>
        <tr><td>Now: what makes it happen this period?</td><td></td><td></td></tr>
      </tbody></table></div>
    </div>
  </section>

  <section class="kit-ch" id="s-pipe">
    <h2>2. You don't have enough pipeline</h2>
    <p>Everybody repeats 3X. It assumes you win about a third of what you qualify. The honest version is one divided by
      your own win rate: at 20% you need 5X, at 25% you need 4X.</p>
    <p>If you don't know your win rate, count it. Of the qualified deals you had due last year, how much closed, by value?
      Then count only pipeline that's qualified and due this period against it. Everything else is next year's problem,
      however real it is.</p>
    <div class="sheet">
      <h3>Worksheet: My pipeline math</h3>
      <p class="sheet-meta">Period __________ &nbsp; <span class="sheet-tool">Online: quotabird.com/pipeline</span></p>
      <div class="mtable"><table class="ws"><tbody>
        <tr><td>My number</td><td></td><td>Closed so far</td><td></td></tr>
        <tr><td>Left to close</td><td></td><td>My win rate</td><td></td></tr>
        <tr><td>Coverage I need (1 ÷ win rate)</td><td></td><td>Qualified pipeline due this period</td><td></td></tr>
        <tr><td>Coverage I have</td><td></td><td>The gap</td><td></td></tr>
      </tbody></table></div>
    </div>
  </section>

  <section class="kit-ch" id="s-big">
    <h2>3. Your biggest deal is carrying the quarter</h2>
    <p>Write your forecast without it. That's closer to your real plan, and if it doesn't work, you need a second way to the number now, before the big one slips.</p>
    <p>Then look hard at the big one. Who set the close date, you or the customer? What still has to happen? Two smaller deals you can move are often better than one giant deal you're praying over.</p>
  </section>

  <section class="kit-ch" id="s-thread">
    <h2>4. You're single-threaded</h2>
    <p>If your champion disappeared tomorrow, who at the customer would notice the deal was gone? If the answer is nobody,
      the deal is one reorg away from over.</p>
    <p>Ask your contact for one introduction this week, upward or sideways. Most people will say yes if the introduction makes them look good too.</p>
    <div class="sheet">
      <h3>Worksheet: Account map</h3>
      <p class="sheet-meta">Account ____________________ &nbsp; <span class="sheet-tool">Online: quotabird.com/account</span></p>
      <div class="mtable"><table class="ws"><thead><tr><th>Role</th><th>Name</th><th>Met?</th><th>What they care about</th></tr></thead><tbody>
        <tr><td>Decides</td><td></td><td></td><td></td></tr><tr><td>Pays</td><td></td><td></td><td></td></tr>
        <tr><td>Uses it</td><td></td><td></td><td></td></tr><tr><td>Could block it</td><td></td><td></td><td></td></tr>
        <tr><td>Runs the buying process</td><td></td><td></td><td></td></tr><tr><td>My champion</td><td></td><td></td><td></td></tr>
      </tbody></table></div>
    </div>
  </section>

  <section class="kit-ch" id="s-disc">
    <h2>5. The customer wants a discount</h2>
    <p>A discount should buy you something. What comes back? A signature date, more scope, a longer term, a reference you can
      use. And remember it comes out of your commission at the same rate it comes off the price.</p>
    <p>Before you ask your manager to approve it, ask whether the problem is the price or the deal. A discount fixes price. If the real problem is power, path or timing, it just makes the deal cheaper.</p>
  </section>

  <section class="kit-ch" id="s-quiet">
    <h2>6. The deal has gone quiet</h2>
    <p>Busy and stalled look alike for about a week. Busy looks like short replies and moved meetings. Stalled looks like
      no replies and nobody else at the customer you can call.</p>
    <p>Send one short note that's easy to answer: "Is this still a priority for this quarter, or should I check back in
      January?" A no is useful. Silence for two weeks after that is an answer too.</p>
  </section>

  <section class="kit-ch" id="s-behind">
    <h2>7. You're behind the number</h2>
    <p>Stop treating every deal the same. Three piles: can close, can close with help, can't close this period. Spend your time on the middle pile and tell your manager exactly what help you need.</p>
    <p>And if the number itself is the problem, don't just complain about it. Show your manager the math: <a href="/notes/prove-the-quota-is-crazy/">quotabird.com/notes/prove-the-quota-is-crazy</a></p>
    <div class="sheet">
      <h3>Worksheet: Quarter rescue plan</h3>
      <p class="sheet-meta">Days left __________</p>
      <div class="mtable"><table class="ws"><thead><tr><th>Deal</th><th>What has to happen</th><th>Who does it</th><th>By when</th></tr></thead><tbody>
        <tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr>
      </tbody></table></div>
    </div>
  </section>

  <section class="kit-ch" id="s-mgr">
    <h2>8. Don't make your manager guess</h2>
    <p>Good managers don't need every detail. They need to know what changed, what might go wrong, and where you need help.
      "Still feeling good" isn't an update. "Procurement moved the date two weeks, Sarah told me Thursday, and I need you to
      call her VP" is an update.</p>
    <p>Before the forecast call, try to break your own deals the way your manager will. Which of the five from chapter 1
      would you defend? Ask for help while there's still time to use it: what you need them to do, and by when.</p>
    <div class="sheet">
      <h3>Worksheet: Manager update</h3>
      <p class="sheet-meta">Deal ____________________ &nbsp; Date __________</p>
      <p class="sheet-label">What changed</p><div class="lines l1"></div>
      <p class="sheet-label">Who told me, and when</p><div class="lines l1"></div>
      <p class="sheet-label">What might go wrong</p><div class="lines l1"></div>
      <p class="sheet-label">What I need from you, and by when</p><div class="lines l1"></div>
    </div>
  </section>
'''
SELLER_CTA = '''
  <section class="kit-cta" aria-labelledby="seller-cta-h">
    <h2 id="seller-cta-h">Sometimes you just need another set of eyes</h2>
    <p>I'm Mark. I spent a lot of years carrying a number before I ever managed anybody. If you're staring at a deal, a forecast or a number that doesn't make sense, tell me about it.</p>
    <p class="kit-cta-terms">A free twenty-minute call, no pitch.</p>
    <div class="btn-row kit-cta-row">
      <a class="btn btn-primary btn-lg" id="sellerBook" href="https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&amp;utm_medium=seller&amp;utm_content=seller_cta" target="_blank" rel="noopener">Chat with Mark</a>
      <a class="btn btn-lg" href="https://www.linkedin.com/in/markflournoy/" target="_blank" rel="noopener">DM on LinkedIn</a>
    </div>
    <p class="kit-bridge">Used this with your team and found something ugly? That's <a href="/ask/">most of the stuff I help managers with</a>.</p>
    <p class="fine">Or email me: <a href="mailto:mark@quotabird.com">mark@quotabird.com</a>. And if I don't think I can help, I'll tell you.</p>
  </section>
  <div class="kit-next"><span class="overline">Next</span><p>Running a team? <a href="/kit/">The Manager's Field Kit</a> is the one for that.</p></div>
'''
_sl_url = 'https://quotabird.com/seller/'
_sl_sub = "Useful things for the weeks when the deal, the number, or both are giving you trouble."
_sl_desc = "Useful things for the weeks when the deal, the number, or both are giving you trouble. A free, printable field kit for sellers: is it a real deal, pipeline math, single-threaded deals, discounts, quiet deals, falling behind, and keeping your manager informed."
_sl_ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": "The Seller's Field Kit", "description": _sl_desc, "url": _sl_url, "isAccessibleForFree": True,
                     "dateModified": BUILD[:10], "image": "https://quotabird.com/card-seller.jpg", "author": {"@type": "Person", "@id": "https://quotabird.com/#about", "name": "Mark Flournoy"},
                     "publisher": {"@type": "Organization", "name": "QuotaBird", "url": "https://quotabird.com/"}}, indent=2)
_seller = note_head("The Seller's Field Kit", _sl_desc, _sl_url).replace("| QuotaBird</title>", "| Free Printable | QuotaBird</title>").replace("https://quotabird.com/card.jpg", "https://quotabird.com/card-seller.jpg").replace('<meta name="twitter:card"', '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="The Seller\'s Field Kit: a free, printable field kit for sellers">\n<meta name="twitter:card"') + f'''<script type="application/ld+json">
{_sl_ld}
</script>
</head>
<body class="kit-page">

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note kit">
  <span class="overline">Free printable</span>
  <h1>The Seller's Field Kit</h1>
  <p class="dek">{_sl_sub}</p>
  <div class="kit-promo kit-hero">
    <div class="kit-thumb" aria-hidden="true">
      <img class="kt-back" src="/seller/preview-2.jpg" alt="" width="480" height="622" decoding="async">
      <img class="kt-front" src="/seller/preview-1.jpg" alt="" width="480" height="622" decoding="async">
    </div>
    <div class="kit-promo-body">
      <span class="pill">Free printable</span>
      <p class="kit-hero-meta">__PAGES__ pages, prints on letter or A4. Eight short chapters and five worksheets.</p>
      <div class="kit-promo-actions">
        <a class="btn btn-primary btn-lg btn-icon" href="/seller/seller-field-kit.pdf" download>Download the PDF{_DL_ICON}</a>
        <button class="btn btn-text" id="kitPrint" type="button">Print this page</button>
      </div>
    </div>
  </div>
{SELLER_BODY}
{SELLER_CTA}
</article>

''' + NOTE_TAIL.replace('Field Notes are part of', "The Seller's Field Kit is part of").replace('</script>\n</body>', """document.getElementById('kitPrint').addEventListener('click', function () { if (window.qbTrack) window.qbTrack('seller_print'); window.print(); });
document.getElementById('sellerBook').addEventListener('click', function () { if (window.qbTrack) window.qbTrack('seller_book'); });
</script>
</body>""")
_seller = _seller.replace('__PAGES__', SELLER_PAGES)
assert '—' not in _seller and '–' not in _seller
os.makedirs('seller', exist_ok=True)
open('seller/index.html', 'w').write(_seller)

# ────────────────────────────── FIELD KITS (/kits/): the ladder ──────────────────────────────
def _kitcard(src, pill):
    return src.replace('<span class="pill">Free printable</span>', f'<span class="pill">{pill}</span>')
_kits = note_head('Field Kits', 'Three free printables for the job you have now and the one you\'re growing into: The Seller\'s, The Manager\'s and The Leadership Field Kit.', 'https://quotabird.com/kits/') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
  <div id="screen">
    <span class="overline tool-name">Free printables</span>
    <h1>Field Kits</h1>
    <p class="dek">Three short printables for the job you have now and the one you might want next.</p>
  </div>
</div>

''' + _kitcard(open('partials/seller-card.html').read(), 'Carry the number') + _kitcard(open('partials/kit-card.html').read(), 'Run the team') + _kitcard(open('partials/leader-card.html').read(), 'Beyond your team') + '''<section class="band" id="about"></section>

''' + NOTE_TAIL.replace('Field Notes are part of', 'The Field Kits are part of')
os.makedirs('kits', exist_ok=True)
open('kits/index.html', 'w').write(_kits)
print('seller kit', len(_seller), '| kits index', len(_kits))


# ────────────────────────────── ASK MARK (/ask/): what working with Mark looks like ──────────────────────────────
_ask_url = 'https://quotabird.com/ask/'
_ask_desc = "Got a sales problem that doesn't fit in five questions? A free twenty-minute call with Mark Flournoy to start, then monthly help for managers or a working session with your team. No methodology rollout, no deck."
_ask = note_head('Ask Mark', _ask_desc, _ask_url).replace('| QuotaBird</title>', '| QuotaBird</title>') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note ask">
  <span class="overline">Ask Mark</span>
  <h1>Got a quota problem?</h1>
  <p class="dek">Your quota went up. Your pipeline didn't. Your boss says the number isn't moving. Bring the math, and
    we'll look at what changed, what didn't, and whether you've got a quota problem or a planning problem.</p>

  <div class="ask-cta">
    <a class="btn btn-primary btn-lg" id="askBook" href="https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&amp;utm_medium=ask&amp;utm_content=ask" target="_blank" rel="noopener">Grab 20 minutes</a>
    <a class="ask-alt" href="https://www.linkedin.com/in/markflournoy/" target="_blank" rel="noopener">or DM me on LinkedIn</a>
  </div>
  <ol class="how">
    <li><b>Pick a time.</b> Add one line about what's going on.</li>
    <li><b>I read it before we talk.</b> No deck needed.</li>
    <li><b>Twenty minutes, free.</b> If I can't help, I'll say so in the first five.</li>
  </ol>

  <div class="who ask-me">
    <img src="/mark.jpg" alt="Mark Flournoy" width="96" height="96" loading="lazy" decoding="async">
    <p>I'm Mark. I spent six years leading federal partner sales teams at AWS, after plenty of years carrying a number
      myself. People I've helped have worked at Amazon, Microsoft, Google, Oracle and a lot of smaller companies you've
      probably never heard of.</p>
  </div>

  <h2>What people usually bring me</h2>
  <ul class="ask-list">
    <li>A quota that came from somebody who's never seen your territory.</li>
    <li>A comp plan nobody can explain, including the person who sent it.</li>
    <li>A deal everybody thinks will close, and nobody on the customer side has committed to anything.</li>
    <li>A rep you're not sure about. Or maybe it's the territory.</li>
    <li>A forecast call you're dreading, or a review where you have to defend somebody.</li>
  </ul>

  <h2>If twenty minutes isn't enough</h2>
  <div class="offers">
    <div class="offer">
      <h3>Manager Wingman</h3>
      <p class="offer-when">Monthly</p>
      <p>A couple of calls a month when you need somebody outside the org chart. Bring the rep, the forecast, the ugly deal, or the thing you have to explain to your boss.</p>
      <p class="offer-link"><a href="mailto:mark@quotabird.com?subject=Manager%20Wingman">Ask about Wingman</a></p>
    </div>
    <div class="offer">
      <h3>Team session</h3>
      <p class="offer-when">One session</p>
      <p>I work with your team on pipeline, deals, account planning or a manager workshop, using the same questions as the
        tools. There's usually some arguing.</p>
      <p class="offer-link"><a href="mailto:mark@quotabird.com?subject=Team%20session">Ask about a team session</a></p>
    </div>
  </div>
  <p class="fine ask-price">If we keep going, I'll tell you what it costs before we do anything.</p>

  <p class="ask-foot">Not ready to talk? The <a href="/">tools</a> and the <a href="/kits/">Field Kits</a> are free. Or email
    me at <a href="mailto:mark@quotabird.com">mark@quotabird.com</a>.</p>
</article>

''' + NOTE_TAIL.replace('Field Notes are part of', 'Ask Mark is part of').replace('</script>\n</body>', """document.getElementById('askBook').addEventListener('click', function () { if (window.qbTrack) window.qbTrack('ask_book'); });
</script>
</body>""")
assert '—' not in _ask and '–' not in _ask
os.makedirs('ask', exist_ok=True)
open('ask/index.html', 'w').write(_ask)

# ────────────────────────────── HOW QUOTAS GET BUILT (/how-quotas-get-built/) ──────────────────────────────
_how = note_head('How Quotas Usually Get Built', "Where your sales quota probably came from: last year plus a growth rate, the corporate plan, headcount, territory, overlays. And why your boss may not even be goaled on your number.", 'https://quotabird.com/how-quotas-get-built/') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note">
  <span class="overline">Understand it</span>
  <h1>How quotas usually get built</h1>
  <p class="dek">Nobody hands you the spreadsheet. Here's roughly what's in it.</p>

  <p>Most reps have no idea how their number was made, and a lot of managers only know their half. I can't tell you
    your company's formula. Nobody outside finance can, and some years nobody inside can either. But most of them
    start from the same handful of things.</p>

  <h2>How a big company builds your number</h2>
  <p>At a company the size of AWS, Microsoft or Google, your quota is the last step of a long chain. It usually runs in
    this order:</p>
  <ol class="chain">
    <li><strong>The company number.</strong> Leadership commits to a growth target. Everything after this is that number, divided.</li>
    <li><strong>Capacity.</strong> Finance counts sellers: who's here, who's ramping, who's leaving, and what each seat is supposed to produce.</li>
    <li><strong>Territories.</strong> Accounts get carved up among the seats, including the empty ones.</li>
    <li><strong>Quotas.</strong> The number gets handed down through each layer of management until it reaches you.</li>
    <li><strong>The comp plan.</strong> Last, somebody decides what you get paid for hitting it.</li>
  </ol>
  <p>Your territory and your number are usually settled before anybody asks you about either one.</p>

  <h2>Why the quotas add up to more than the plan</h2>
  <p>Planners over-assign. The quotas across a sales team typically total 20 to 30% more than the company actually
    needs, and more in enterprise, to cover the reps who miss, leave or ramp slowly. If your number feels like it's
    carrying somebody else's, it probably is.</p>

  <h2>Cloud quotas count consumption</h2>
  <p>At the cloud providers, a lot of quota is measured in what customers actually run, month after month, not what they
    sign. Microsoft, for one, ties its field incentives to Azure consumed revenue. A big commit nobody uses doesn't
    retire much quota, which is also why cloud multiples look enormous next to SaaS benchmarks.</p>

  <h2>The calendar matters</h2>
  <p>Amazon and Google plan on the calendar year. Microsoft's fiscal year runs July through June. Either way, next year's
    number is being built months before the year starts, which is the only time a manager can still change it.</p>

  <h2>Where the number usually comes from</h2>
  <ul>
    <li>Last year's revenue, plus a growth rate somebody picked</li>
    <li>The corporate plan: what the company told the board, divided down</li>
    <li>Market assumptions: how big somebody thinks your segment is</li>
    <li>Headcount: the number gets split across however many reps are budgeted, whether the seats are filled or not</li>
    <li>Territory potential, when anybody bothered to size it</li>
    <li>Product priorities: the thing the company needs sold this year</li>
    <li>New business, often carried separately from renewals</li>
    <li>Renewals, which are either counted in your number or quietly aren't</li>
    <li>Management overlays: a little extra added at each level, just in case</li>
  </ul>
  <p>That last one adds up. Every layer pads it a few percent, and by the time it reaches a rep, the number is carrying
    everybody's cushion.</p>

  <h2>Your boss may not be goaled on your number</h2>
  <p>This explains a lot of strange quotas. Your manager's boss might be measured on something else entirely: growth
    rate, new business, a strategic product, bookings, margin, market share, or what partners bring in. If they're paid
    on new logos and your territory is mostly renewals, your number is going to look odd from where you sit, and
    nobody will think to tell you why.</p>
  <p>So ask. "What's our leader actually measured on this year?" is a fair question, and the answer tells you which
    parts of your quota will get attention and which won't.</p>

  <h2>What you can usually find out</h2>
  <ul>
    <li>How your number compares to last year's actuals, yours and the team's</li>
    <li>Whether renewals are in it, and at what rate</li>
    <li>Whether a vacant territory's number got spread across everybody else</li>
    <li>Whether last year included one big deal the plan assumes will happen again</li>
    <li>What the comp plan pays extra for, which tells you what the company actually wants</li>
  </ul>

  <h2>Then decide</h2>
  <p>If the number holds up, build the plan. If it doesn't, bring the math. <a href="/quota/">Quota Check</a> tells you
    how your multiple compares, <a href="/quota-case/">Quota Case</a> builds the bridge from last year to this year, and
    <a href="/notes/prove-the-quota-is-crazy/">Your quota is crazy. Now prove it.</a> covers the conversation. If the
    number isn't moving, <a href="/notes/the-number-isnt-changing/">here's what I'd do instead</a>. The benchmarks are all on
    <a href="/quota-by-the-numbers/">Quota by the numbers</a>.</p>
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL
assert '—' not in _how and '–' not in _how
os.makedirs('how-quotas-get-built', exist_ok=True)
open('how-quotas-get-built/index.html', 'w').write(_how)

# ────────────────────────────── QUOTA SHORTS PAGE (/shorts/) ──────────────────────────────
_sh = note_head('Quota Shorts', 'Quota, pay and attainment in one-minute pieces: who hits quota, how quotas get built, what comp plans pay. Each one sourced, each one linked to the tool that does the math.', 'https://quotabird.com/shorts/') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note shorts-page">
  <span class="overline">Quota Shorts</span>
  <h1>One minute each.</h1>
  <p class="dek">What the data says about quota, one card at a time.</p>
  <div class="shorts-grid" role="list">''' + ''.join(f'<div role="listitem">{_short(s, i)}</div>' for i, s in enumerate(SHORTS)) + '''</div>
  <p class="fine" style="margin-top:22px;">Sources and the full tables are on <a href="/quota-by-the-numbers/">Quota by the numbers</a>.</p>
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL
os.makedirs('shorts', exist_ok=True)
open('shorts/index.html', 'w').write(_sh)

# ────────────────────────────── QUOTA BY THE NUMBERS (/quota-by-the-numbers/) ──────────────────────────────
# Magazine-style "By the Numbers" panel: big stats, donuts and paired bars. Mobile first.
import math as _m
def bn_big(num, unit, cap):
    u = f'<span class="bn-unit">{unit}</span>' if unit else ''
    return f'<div class="bn-big"><div class="bn-num">{num}{u}</div><div class="bn-cap">{cap}</div></div>'
def bn_donut(pct, legend):
    r, w = 46, 20; c = 2 * _m.pi * r; a = c * pct / 100
    svg = (f'<svg viewBox="0 0 120 120" aria-hidden="true"><circle class="ring-b" cx="60" cy="60" r="{r}" fill="none" stroke-width="{w}"/>'
           f'<circle class="ring-line" cx="60" cy="60" r="{r + w/2}" stroke-width="1.5"/><circle class="ring-line" cx="60" cy="60" r="{r - w/2}" stroke-width="1.5"/>'
           f'<circle class="ring-a" cx="60" cy="60" r="{r}" fill="none" stroke-width="{w}" stroke-dasharray="{a:.1f} {c:.1f}" transform="rotate(-90 60 60)"/>'
           f'<text x="60" y="68" text-anchor="middle">{pct}%</text></svg>')
    leg = ''.join(f'<div><span class="bn-sw {k}"></span><b>{v}</b>{t}</div>' for k, v, t in legend)
    return f'<div class="bn-donut">{svg}<div class="bn-legend">{leg}</div></div>'
def bn_bars(rows, scale=100):
    out = []
    for label, series in rows:
        bars = ''.join(f'<div class="bn-bar {k}" style="width:{max(v / scale * 100, 12):.1f}%">{shown}</div>' for k, v, shown in series)
        out.append(f'<div class="bn-stack">{bars}<div class="bn-bar-label">{label}</div></div>')
    return '<div class="bn-bars">' + ''.join(out) + '</div>'

_panel = ('<section class="bynum" aria-labelledby="bn-title"><div class="bn-label">By the Numbers</div>'
  '<h1 class="bn-title" id="bn-title">Quota</h1><div class="bn-kicker">Bridge Group and RepVue data, 2026</div>'
  '<div class="bn-cols"><div>'
  '<div class="bn-sec"><h2 class="bn-h">AEs who hit 100% of quota in 2026</h2>'
  + bn_donut(48, [('a', '48%', 'hit it'), ('b', '52%', "didn't")]) + '</div>'
  '<div class="bn-sec"><h2 class="bn-h">Same question, three different years</h2>'
  + bn_bars([('2026', [('a', 48, '48%')]), ('2024', [('b', 51, '51%')]), ('2022', [('b', 66, '66%')])]) + '</div>'
  '<div class="bn-sec"><h2 class="bn-h">The median SaaS AE</h2><div class="bn-pair">'
  + bn_big('$960', 'K', 'quota') + bn_big('$200', 'K', 'on-target earnings') + bn_big('4.6', '×', 'quota ÷ OTE, up from 4.2× in 2024') + bn_big('53:47', '', 'base to variable') + '</div></div>'
  '<div class="bn-sec"><h2 class="bn-h">How fast each one grows, per year</h2>'
  + bn_bars([('Pay (OTE)', [('a', 4.9, '4.9%')]), ('Quota', [('b', 2.4, '2.4%')])], scale=5) + '</div>'
  '</div><div>'
  '<div class="bn-sec"><h2 class="bn-h">Who says they hit quota</h2>'
  + bn_bars([('Federal AEs', [('a', 46, '46%')]), ('SLED AEs', [('a', 45, '45%')]), ('All AEs', [('b', 42, '42%')]), ('Enterprise AEs', [('b', 41, '41%')])]) +
  '<div class="bn-src">Self-reported on RepVue, September 2026.</div></div>'
  '<div class="bn-sec"><h2 class="bn-h">At the big cloud providers</h2>'
  + bn_bars([('Microsoft SLED AEs', [('a', 67, '67%')]), ('AWS Account Managers', [('a', 64, '64%')]), ('Microsoft Enterprise AEs', [('a', 56, '56%')])]) +
  '<div class="bn-pair" style="margin-top:14px;">' + bn_big('$280', 'K', 'AWS Account Manager OTE') + bn_big('54:46', '', 'AWS Account Manager pay mix') + '</div>'
  '<div class="bn-src">Share who say they hit quota. Self-reported on RepVue, 2026.</div></div>'
  '<div class="bn-sec"><h2 class="bn-h">How plans get built</h2><div class="bn-pair">'
  + bn_big('20-30', '%', 'more quota handed out than the company needs') + bn_big('6.2', 'mo', 'for a new AE to ramp')
  + bn_big('1.5-2', '×', 'typical first accelerator above quota') + bn_big('80', '%', 'of plans use accelerators') + '</div></div>'
  '</div></div></section>')
_num = note_head('Quota by the Numbers', 'Sales quota and comp benchmarks with sources: how many reps hit quota, median quota and OTE, quota-to-OTE, pay mix, ramp, over-assignment, accelerators, and what reps at AWS and Microsoft report.', 'https://quotabird.com/quota-by-the-numbers/') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note numbers">
''' + _panel + '''
  <p>Two different numbers both get called attainment: the share of reps who hit 100%, and the average share of quota reps
    reach. RepVue's average across 246 cloud and software companies was 42.7% in mid-2025. They aren't the same number,
    and people swap them in meetings.</p>
  <p>The cloud provider figures are reps rating their own employers, so treat them as a rough read. Cloud quotas are
    usually measured in consumption growth, which is why their multiples run far higher than SaaS.
    <a href="/how-quotas-get-built/">How quotas get built</a> explains that part; <a href="/quota/">Quota Check</a>
    puts your own multiple next to these.</p>

  <h2>Sources</h2>
  <ul class="sources">
    <li><a href="https://blog.bridgegroupinc.com/2026-ae-compensation-quota-ai-metrics" rel="noopener">Bridge Group, AE Models, Motions and Metrics, 2026</a></li>
    <li><a href="https://blog.bridgegroupinc.com/2024-ae-metrics-compensation-benchmark" rel="noopener">Bridge Group, SaaS AE Metrics and Compensation, 2024</a></li>
    <li><a href="https://www.repvue.com/salaries/account-executive" rel="noopener">RepVue, Account Executive salaries and attainment, 2026</a></li>
    <li><a href="https://www.repvue.com/blog/sales-salary-guide" rel="noopener">RepVue, Sales Salary Guide, 2026</a></li>
    <li><a href="https://www.repvue.com/companies/Amazonwebservices/salaries" rel="noopener">RepVue, Amazon Web Services salaries</a></li>
    <li><a href="https://www.repvue.com/companies/Microsoft/salaries" rel="noopener">RepVue, Microsoft salaries</a></li>
    <li><a href="https://lative.ai/blog/quota-attainment-benchmarks/" rel="noopener">RepVue Cloud Sales Index Q2 2025, as reported by Lative</a></li>
    <li><a href="https://www.mostlymetrics.com/p/your-complete-guide-to-annual-planning" rel="noopener">Mostly Metrics, Annual Planning: Building Sales Capacity</a></li>
    <li><a href="https://learn.microsoft.com/en-us/partner-center/referrals/partner-reported-azure-consumed-revenue" rel="noopener">Microsoft Learn, Partner Reported Azure Consumed Revenue</a></li>
    <li><a href="https://www.prowi.io/en/post/commission-accelerators-guide" rel="noopener">Prowi, Commission accelerators</a></li>
  </ul>
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL
os.makedirs('quota-by-the-numbers', exist_ok=True)
open('quota-by-the-numbers/index.html', 'w').write(_num)


# ────────────────────────────── STUFF I LIKE (/stuff/) ──────────────────────────────
# Mark's books and podcasts. No affiliate links, no links at all: the value is that it's his.
_stuff = note_head('Stuff I Like', "Books and podcasts Mark Flournoy has gotten something from. Some sales, some just because he likes them. Ten books, ten podcasts, one line on each, and no affiliate links.", 'https://quotabird.com/stuff/') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note stuff">
  <span class="overline">QuotaBird</span>
  <h1>Stuff I Like</h1>
  <p class="dek">Some sales. Some just because I like them.</p>

  <h2>Books that made me think</h2>
  <div class="likes">
    <div class="like"><p class="like-t">The Qualified Sales Leader</p><p class="like-by">John McMahon</p><p class="like-why">Probably the one I'd hand to someone managing serious enterprise sellers.</p></div>
    <div class="like"><p class="like-t">Fanatical Prospecting</p><p class="like-by">Jeb Blount</p><p class="like-why">If prospecting is the part of the job you keep finding reasons not to do.</p></div>
    <div class="like"><p class="like-t">Getting to Yes</p><p class="like-by">Roger Fisher, William Ury and Bruce Patton</p><p class="like-why">Negotiating without turning every conversation into a hostage situation.</p></div>
    <div class="like"><p class="like-t">The Little Red Book of Selling</p><p class="like-by">Jeffrey Gitomer</p><p class="like-why">Old-school, occasionally corny, and still right about a surprising amount.</p></div>
    <div class="like"><p class="like-t">How to Say It</p><p class="like-by">Rosalie Maggio</p><p class="like-why">Not really a sales book. Good when you know what you mean but can't find the words.</p></div>
    <div class="like"><p class="like-t">Atomic Habits</p><p class="like-by">James Clear</p><p class="like-why">Because a sales career is mostly boring things done over and over.</p></div>
    <div class="like"><p class="like-t">Meditations</p><p class="like-by">Marcus Aurelius</p><p class="like-why">Two thousand years old and still useful when the forecast call starts getting stupid.</p></div>
    <div class="like"><p class="like-t">Tao Te Ching</p><p class="like-by">Lao Tzu</p><p class="like-why">Forcing things usually makes them worse. That goes for sales, management, meetings, pretty much everything.</p></div>
    <div class="like"><p class="like-t">The Bezos Blueprint</p><p class="like-by">Carmine Gallo</p><p class="like-why">Why Amazon writes and communicates the strange way it does.</p></div>
    <div class="like"><p class="like-t">Amazon Unbound</p><p class="like-by">Brad Stone</p><p class="like-why">Less about selling than understanding how one very large company thinks.</p></div>
  </div>

  <h2>Podcasts I fall asleep to</h2>
  <div class="likes">
    <div class="like"><p class="like-t">The Brutal Truth About Sales &amp; Selling</p><p class="like-by">Brian Burns</p><p class="like-why">Actual selling. Not much incense.</p></div>
    <div class="like"><p class="like-t">Hidden Brain</p><p class="like-by">Shankar Vedantam</p><p class="like-why">People are weird. Helpful to remember when selling to them or managing them.</p></div>
    <div class="like"><p class="like-t">Freakonomics Radio</p><p class="like-by">Stephen J. Dubner</p><p class="like-why">Incentives explain a lot of behavior, including some very stupid sales behavior.</p></div>
    <div class="like"><p class="like-t">Marketplace</p><p class="like-by">American Public Media</p><p class="like-why">Twenty-some minutes and you know enough about the economy to sound less surprised.</p></div>
    <div class="like"><p class="like-t">Pivot</p><p class="like-by">Kara Swisher and Scott Galloway</p><p class="like-why">Tech, business, politics, and two people disagreeing with each other.</p></div>
    <div class="like"><p class="like-t">How to Be a Better Human</p><p class="like-by">TED</p><p class="like-why">Pretty much what it says.</p></div>
    <div class="like"><p class="like-t">The Daily Stoic</p><p class="like-by">Ryan Holiday</p><p class="like-why">Good before certain forecast calls.</p></div>
    <div class="like"><p class="like-t">The Side Hustle Show</p><p class="like-by">Nick Loper</p><p class="like-why">For people who occasionally wonder what else they could build.</p></div>
    <div class="like"><p class="like-t">Radiolab</p><p class="like-by">WNYC</p><p class="like-why">Good stories about things I didn't know I was interested in.</p></div>
    <div class="like"><p class="like-t">Stuff You Should Know</p><p class="like-by">Josh Clark and Chuck Bryant</p><p class="like-why">Has nothing to do with quota. That's partly why I like it.</p></div>
  </div>

  <p class="fine stuff-foot">No links and no affiliate stuff. Your library or podcast app can find them.</p>
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL.replace('Field Notes are part of', 'Stuff I Like is part of')
assert '—' not in _stuff and '–' not in _stuff
os.makedirs('stuff', exist_ok=True)
open('stuff/index.html', 'w').write(_stuff)

# /talent-review/ forwards to Talent Review Check (at /olr/) (the kit prints the universal name; the tool keeps its name)
os.makedirs('talent-review', exist_ok=True)
open('talent-review/index.html', 'w').write('''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Talent review prep | QuotaBird</title>
<meta name="robots" content="noindex"><link rel="canonical" href="https://quotabird.com/olr/">
<meta http-equiv="refresh" content="0; url=/olr/"></head>
<body><p><a href="/olr/">Talent review prep is here.</a></p></body></html>
''')

# ────────────────────────────── ABOUT ──────────────────────────────
os.makedirs('about', exist_ok=True)
open('about/index.html', 'w').write(note_head('About Mark', "Who's behind QuotaBird, the situations he sees most, and how to reach him. Twenty minutes, free, no deck required.", 'https://quotabird.com/about/').replace('<meta property="og:type" content="article">', '<meta property="og:type" content="profile">') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>

<section class="band" id="about"></section>

<section class="band about-kits">
  <div class="band-inner">
    Want something you can print? Three free <a href="/kits/">Field Kits</a>: seller, manager and leader.
  </div>
</section>

<section class="band bird-egg" aria-labelledby="bird-h">
  <div class="band-inner">
    <picture><source srcset="/logo-dark.svg" media="(prefers-color-scheme: dark)"><img src="/logo.svg" alt="" width="48" height="42"></picture>
    <div>
      <h2 id="bird-h">Why the bird?</h2>
      <p>Everybody in sales loves a bluebird. Usually it's just the Quota Bird, dropping off more quota.</p>
    </div>
  </div>
</section>

''' + NOTE_TAIL.replace('Field Notes are part of <a href="/">QuotaBird</a>, a shelf', 'QuotaBird is a shelf'))

# ── the 404 page carries the same shelf as the home page (one copy of the covers, pulled at build time) ──
_home_src = open('home.src.html', encoding='utf-8').read()
_shelf = re.search(r'    <div class="shelf-grid">.*?\n    </div>\n', _home_src, flags=re.S).group(0)
_nf = open('404.html', encoding='utf-8').read()
_nf = re.sub(r'<!--shelf-->.*?<!--/shelf-->', lambda m_: '<!--shelf-->\n' + _shelf + '<!--/shelf-->', _nf, count=1, flags=re.S)
open('404.html', 'w', encoding='utf-8').write(_nf)

# ────────────────────────────── SHARED CHROME ──────────────────────────────
# Every page gets the same header and the same About section, from one source.
MARK_SRC = open('partials/mark.html').read()
MADEBY_SRC = open('partials/made-by.html').read()
KITCARD_SRC = open('partials/kit-card.html').read()
LEADERCARD_SRC = open('partials/leader-card.html').read()
LEADERCARD_PAGES = {'notes/index.html'}
SELLERCARD_SRC = open('partials/seller-card.html').read()
SELLERCARD_PAGES = {'deal/index.html', 'quota/index.html', 'territory/index.html', 'discount/index.html', 'commission/index.html', 'account/index.html', 'competition/index.html'}
KITCARD_PAGES = {'index.html', 'rep/index.html', 'partner/index.html', 'olr/index.html', 'risk/index.html', 'notes/index.html', 'math/index.html'}
def root_of(path):
    if path == '404.html': return '/'
    return '../' * path.count('/')
def utm_of(path):
    return 'home' if path == 'index.html' else path.split('/')[0]
def current_of(path):
    return '/' if path == 'index.html' else '/' + path.rsplit('/', 1)[0] + '/'
def header(path):
    b = root_of(path)
    ask = '/ask/'
    return f'''<header class="appbar">
    <a class="logo" href="/" aria-label="QuotaBird, home"><picture><source srcset="{b}logo-dark.svg" media="(prefers-color-scheme: dark)"><img class="brandmark" src="{b}logo.svg" alt="" width="39" height="34"></picture> QuotaBird</a>
    <nav class="topnav" aria-label="Site">
      {menu(current_of(path) if not path.startswith(('notes/', 'math/', 'kit/', 'leader/', 'seller/', 'kits/', 'ask/', 'stuff/', 'how-quotas-get-built/', 'shorts/', 'quota-by-the-numbers/')) else '/' + path.split('/')[0] + '/')}
      <a class="toplink" href="/kits/">Field Kits</a>
      <a class="toplink" href="/notes/">Field Notes</a>
      <a class="toplink" href="/about/">About</a>
      <a class="chip chip-ask" href="{ask}">Ask Mark</a>
    </nav>
  </header>'''
def chrome(path):
    s = open(path).read()
    # preload the one font every page uses, so headlines don't flash in a fallback face
    if 'rel="preload" href="/inter.woff2"' not in s:
        s = s.replace('<meta name="viewport"', '<link rel="preload" href="/inter.woff2" as="font" type="font/woff2" crossorigin>\n<meta name="viewport"', 1)
    s = re.sub(r'<header class="appbar">.*?</header>', lambda m: header(path), s, count=1, flags=re.S)
    ask = '/ask/'
    nav = f'<p class="foot-nav"><a href="/">Tools</a><a href="/kits/">Field Kits</a><a href="/math/">Sales Math</a><a href="/notes/">Field Notes</a><a href="/stuff/">Stuff I Like</a><a href="/about/">About</a><a href="{ask}">Ask Mark</a></p>'
    s = re.sub(r'\s*<p class="foot-nav">.*?</p>', '', s, count=1, flags=re.S)          # the footer nav is regenerated every build, so every page matches
    s = s.replace('<footer class="sitefoot">', '<footer class="sitefoot">\n  ' + nav, 1)
    if path != '404.html':
        # the full story lives on the About page; every other page gets the short "Made by Mark" card
        src = MARK_SRC if path == 'about/index.html' else MADEBY_SRC
        mark = src.replace('{ROOT}', root_of(path)).replace('{UTM}', utm_of(path))
        if path in KITCARD_PAGES | SELLERCARD_PAGES:   # only pages that get a card injected; /kits/ is made of cards
            s = re.sub(r'\s*<section class="band kit-band[^"]*"[^>]*>.*?</section>', '', s, flags=re.S)   # never let cards accumulate on hand-written pages
        if path in KITCARD_PAGES and 'kit-band' not in mark: mark = KITCARD_SRC + (LEADERCARD_SRC if path in LEADERCARD_PAGES else '') + mark
        elif path in SELLERCARD_PAGES and 'kit-band' not in mark: mark = SELLERCARD_SRC + mark
        s = re.sub(r'<section class="band" id="(?:about|mark)"[^>]*>.*?</section>\n*', lambda m: mark, s, count=1, flags=re.S)
    open(path, 'w').write(s)
PAGES = ['index.html', 'pipeline/index.html', 'deal/index.html', 'about/index.html'] + [f'{t["slug"]}/index.html' for t in (REP, PARTNER, TERRITORY, OLR, BRIEF, ACCOUNT, RISK, COMPETITION)] \
        + [f'{c["slug"]}/index.html' for c in CALCS] + ['notes/index.html'] + [f'notes/{n["slug"]}/index.html' for n in NOTES] + ['math/index.html'] + [f'math/{p["slug"]}/index.html' for p in MATH] + ['kits/index.html', 'seller/index.html', 'kit/index.html', 'leader/index.html', 'ask/index.html', 'stuff/index.html', 'how-quotas-get-built/index.html', 'shorts/index.html', 'quota-by-the-numbers/index.html'] + ['404.html']
for _p in PAGES:
    chrome(_p)
print('chrome', len(PAGES))


# ── Structured data follows the page. The FAQPage JSON-LD on every page is rebuilt
#    from the visible FAQ, so the two cannot drift again. ──
import html as _html, glob as _glob
def sync_faq(path):
    s = open(path).read()
    if 'id="faq"' not in s: return
    faq = s[s.index('<section class="band" id="faq"'):]
    faq = faq[:faq.index('</section>')]
    qa = re.findall(r'<details class="exp"><summary>(.*?)</summary>\s*<div class="body">(.*?)</div></details>', faq, flags=re.S)
    clean = lambda t: _html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', t)).strip())
    ents = [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in qa]
    m2 = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S)
    data = json.loads(m2.group(1))
    for g in data.get('@graph', []):
        if g.get('@type') == 'FAQPage': g['mainEntity'] = ents
    s = s[:m2.start(1)] + '\n' + json.dumps(data, indent=2, ensure_ascii=False) + '\n' + s[m2.end(1):]
    open(path, 'w').write(s)
    print('faq synced', path, len(ents))
for _p in PAGES:
    sync_faq(_p)

# ────────────────────────────── AGENT DISCOVERY: llms.txt and ai-catalog.json ──────────────────────────────
# Both are generated from the same tool list as the site, so they cannot drift.
# llms.txt follows llmstxt.org (H1, blockquote summary, H2 sections of "- [name](url): description").
# ai-catalog.json follows the ARD ai-catalog schema 1.0 (ards-project/ard-spec); each tool is a text/html entry.
DESC = {'/pipeline/': 'Pipeline Check: target, pipeline and win rate in, the gap out. 3X is a rule of thumb; your win rate says what you actually need.',
        '/deal/': 'Deal Check: five questions (customer, money, power, path, now) that separate proof from hopium in a federal deal.'}
for t in (REP, PARTNER, TERRITORY, OLR, BRIEF, ACCOUNT, RISK, COMPETITION): DESC['/' + t['slug'] + '/'] = t['name'] + ': ' + t['desc']
for c in CALCS: DESC['/' + c['slug'] + '/'] = c['name'] + ': ' + c['desc']
QUERIES = {'/quota-case/': ['how to push back on a quota that is too high', 'is my sales quota realistic compared to last year', 'build a quota bridge from last year to this year', 'my quota went up and my territory did not'],
           '/pipeline/': ['do I have enough pipeline to make my number', 'pipeline coverage calculator with my win rate', 'is 3X pipeline coverage enough'],
           '/deal/': ['is my deal real or hopium', 'qualify a federal sales deal before commit', 'what will my manager ask about this deal'],
           '/quota/': ['is my quota crazy', 'quota to OTE ratio for cloud sales', 'is my sales quota fair'],
           '/territory/': ['can my territory make the number', 'is my sales territory viable', 'new territory sizing check'],
           '/discount/': ['what does a discount cost me in commission', 'should I give a 15 percent discount', 'discount impact on margin and commission'],
           '/commission/': ['how much of my commission do I take home', 'commission take home after taxes', 'commission check calculator'],
           '/rep/': ['is it the rep or the territory', 'why is my sales rep underperforming', 'rep problem or territory problem'],
           '/partner/': ['is this partner real or a logo', 'is my channel partner actually selling', 'partner check for co-sell'],
           '/olr/': ['prepare for OLR calibration', 'will my case for a rep survive talent review', 'Amazon OLR prep for managers'],
           '/brief/': ['will my QBR survive the room', 'pressure test my brief before the meeting', 'what question am I hoping nobody asks'],
           '/account/': ['do I know the account or just my contact', 'am I single-threaded in this account', 'federal account check'],
           '/risk/': ['how fragile is my pipeline', 'pipeline concentration and aging risk', '4X coverage but still at risk'],
           '/competition/': ['why would they pick us over doing nothing', 'am I beating the incumbent', 'competitive position check for a deal']}
groups, last = [], None
for g, h, n, d in TOOLS:
    if g != last: groups.append([g, []]); last = g
    groups[-1][1].append((h, n, d))
site = 'https://quotabird.com'
lines = ['# QuotaBird', '', '> Quick reality checks for people who carry a number: thirteen free, one-minute tools for sellers and sales managers (deals, pipeline, quota, territories, partners, reps, reviews), plus short field notes. Everything runs in the browser; nothing is stored. Built by Mark Flournoy, who spent six years leading federal partner sales teams at AWS.', '',
         'The tools are plain web pages. Each asks five questions (yes / sort of / no) or takes a few numbers, then gives a verdict, the question a manager will ask, and one thing to do first. Shared results are encoded in the URL fragment; no accounts, no uploads, no AI.', '']
for g, items in groups:
    lines.append(f'## {g}'); lines.append('')
    for h, n, d in items:
        desc = DESC[h].split(': ', 1)[1]; lines.append(f'- [{n}]({site}{h}): {desc[0].upper() + desc[1:]} ({d[0].lower() + d[1:]}.)')
    lines.append('')
lines += ['## Ask Mark', '', f'- [Ask Mark]({site}/ask/): a free twenty-minute call to start; Manager Wingman (monthly calls for sales managers) and team sessions (pipeline or deal reviews, account planning, manager workshops) if it needs more.', '', '## Stuff I Like', '', f'- [Stuff I Like]({site}/stuff/): ten books and ten podcasts Mark has gotten something from, each with one line on why. No affiliate links.', '']
lines += ['## Free printable', '', f"- [The Manager's Field Kit]({site}/kit/): a free, printable field kit for sales managers: inheriting a team, one-on-ones, the forecast call, pipeline, managing up, a struggling rep, review season, managing high performers, and six worksheets.", f"- [The Seller's Field Kit]({site}/seller/): a free, printable field kit for sellers: is it a real deal, pipeline math, one deal carrying the quarter, single-threaded accounts, discounts, quiet deals, falling behind, and keeping your manager informed.", f"- [The Leadership Field Kit]({site}/leader/): a free, printable field kit for managers who want their influence to travel beyond their team: what to be known for, a point of view, receipts, templates others can borrow, the right rooms, and developing the people behind you.", '', '## Sales Math Library', ''] + [f'- [{p["title"]}]({site}/math/{p["slug"]}/): {p["answer"]}' for p in MATH] + ['', '## Field Notes', ''] + [f'- [{n["title"]}]({site}/notes/{n["slug"]}/): {n["dek"]}' for n in NOTES] + ['', '## About', '', f'- [About Mark]({site}/about/): who is behind the tools, the situations he sees most, and how to book a free twenty-minute call.', '', '## Optional', '', f'- [Sitemap]({site}/sitemap.xml)', f'- [ai-catalog.json]({site}/.well-known/ai-catalog.json): ARD capability manifest listing the same tools.', '']
open('llms.txt', 'w').write('\n'.join(lines))
entries = []
for g, h, n, d in TOOLS:
    slug = h.strip('/')
    entries.append({"identifier": f"urn:air:quotabird.com:tools:{slug}-check", "displayName": n, "type": "text/html", "url": site + h,
                    "description": DESC[h], "tags": [g.lower().replace(' ', '-'), 'sales', 'free', 'no-login'],
                    "capabilities": [n.replace(' ', '')], "representativeQueries": QUERIES[h][:5], "version": BUILD[:10].replace('-', '.'),
                    "updatedAt": BUILD[:10] + 'T00:00:00Z', "metadata": {"runsInBrowser": True, "storesData": False, "usesAI": False, "audience": g}})
catalog = {"specVersion": "1.0", "host": {"displayName": "QuotaBird", "identifier": "https://quotabird.com", "documentationUrl": site + "/llms.txt", "logoUrl": site + "/logo.png"}, "entries": entries}
os.makedirs('.well-known', exist_ok=True)
for path in ['.well-known/ai-catalog.json', 'ai-catalog.json']:
    open(path, 'w').write(json.dumps(catalog, indent=2) + '\n')
print('llms.txt', len('\n'.join(lines)), 'chars | ai-catalog.json entries', len(entries))

# ── sitemap, from the same page list ──
_urls = [p for p in PAGES if p != '404.html']
def _loc(p): return 'https://quotabird.com/' + ('' if p == 'index.html' else p[:-len('index.html')])
def _pri(p): return '1.0' if p == 'index.html' else '0.6' if p.startswith('notes/') and p != 'notes/index.html' else '0.8'
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{_loc(p)}</loc><lastmod>{BUILD[:10]}</lastmod><priority>{_pri(p)}</priority></url>\n' for p in _urls) + '</urlset>\n')
print('sitemap', len(_urls), 'urls')

# ── fingerprinted stylesheet and scripts, so a deploy can never serve stale CSS or JS with new HTML ──
# site.css -> site.<hash>.css (and check.js, calc.js, analytics.js likewise); every page links to the hashed name.
# The plain files stay for editing; only the current hashed copies are kept.
import hashlib as _hl, glob as _g
_ASSETS = {}
for _f in ('site.css', 'check.js', 'calc.js', 'analytics.js'):
    _h = _hl.sha1(open(_f, 'rb').read()).hexdigest()[:8]; _base, _ext = _f.rsplit('.', 1)
    _name = f'{_base}.{_h}.{_ext}'
    for _old in _g.glob(f'{_base}.*.{_ext}'):
        if _old != _name: os.remove(_old)
    open(_name, 'wb').write(open(_f, 'rb').read()); _ASSETS[_f] = _name
for _p in ['index.html', '404.html'] + _g.glob('*/index.html') + _g.glob('*/*/index.html'):
    _s = open(_p, encoding='utf-8').read(); _o = _s
    for _f, _name in _ASSETS.items():
        _s = re.sub(r'((?:href|src)=")((?:\.\./)*|/?)' + re.escape(_f.rsplit('.', 1)[0]) + r'(?:\.[0-9a-f]{8})?\.' + _f.rsplit('.', 1)[1] + '"', lambda mm: mm.group(1) + mm.group(2) + _name + '"', _s)
    if _s != _o: open(_p, 'w', encoding='utf-8').write(_s)
print('assets:', ', '.join(_ASSETS.values()))

# ── share-tag hygiene, run on every built page ──
# 1. LinkedIn wants 100+ characters: a short og/twitter description falls back to the page's search description.
# 2. Share images carry a fingerprint of their contents (card.jpg?v=1a2b3c4d), so a changed card gets a new URL
#    and LinkedIn, which caches images by URL, has to fetch it fresh. Unchanged cards keep their URL.
#    Re-run this build after make-card.py, so the fingerprints match the images.
import hashlib, glob as _glob, html as _h
def _fp(fname):
    try: return hashlib.sha1(open(fname, 'rb').read()).hexdigest()[:8]
    except FileNotFoundError: return None
_short = []
for _p in ['index.html'] + sorted(_glob.glob('*/index.html')) + sorted(_glob.glob('*/*/index.html')) + ['404.html']:
    _s = open(_p, encoding='utf-8').read(); _o = _s
    _meta = re.search(r'<meta name="description" content="([^"]*)"', _s)
    for _tag in ('property="og:description"', 'name="twitter:description"'):
        _m = re.search(r'<meta ' + re.escape(_tag) + r' content="([^"]*)"', _s)
        if _m and len(_h.unescape(_m.group(1))) < 100 and _meta and len(_h.unescape(_meta.group(1))) >= 100:
            _s = _s.replace(_m.group(0), '<meta ' + _tag + ' content="' + _meta.group(1) + '"', 1)
    def _ver(mm):
        f = _fp(mm.group(2)); return mm.group(1) + (f'?v={f}' if f else '')
    _s = re.sub(r'(https://quotabird\.com/(card[\w-]*\.jpg))(?:\?v=[0-9a-f]+)?', _ver, _s)
    if _s != _o: open(_p, 'w', encoding='utf-8').write(_s)
    _d = re.search(r'property="og:description" content="([^"]*)"', _s)
    if _d and len(_h.unescape(_d.group(1))) < 100: _short.append(_p)
print('share descriptions under 100 characters:', _short or 'none')
