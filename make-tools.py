#!/usr/bin/env python3
"""Builds rep/index.html, partner/index.html and territory/index.html from one template.
Run from the web root after editing copy below. Deal Check and Pipeline Check are hand-written."""
import json, os, re

BUILD = '2026-10-07.1100'
TOOLS = [
    ('For sellers', '/deal/', 'Deal Check', 'Before you put it in commit'),
    ('For sellers', '/quota/', 'Quota Check', 'The day the number lands'),
    ('For sellers', '/territory/', 'Territory Check', 'Month one in a new patch'),
    ('For sellers', '/discount/', 'Discount Check', 'When they ask you to sharpen the pencil'),
    ('For sellers', '/commission/', 'Commission Check', 'When it closes'),
    ('For managers', '/pipeline/', 'Pipeline Check', 'Quarterly, before the review'),
    ('For managers', '/rep/', 'Rep Check', 'When a rep is worrying you'),
    ('For managers', '/partner/', 'Partner Check', 'Before you renew the partnership'),
    ('For managers', '/olr/', 'OLR Check', 'Review season'),
    ('Any meeting', '/brief/', 'Brief Check', 'When someone in the room can say no'),
]

def menu(current):
    groups, last = [], None
    for g, h, n, d in TOOLS:
        if g == 'QuotaBird': continue
        if g != last: groups.append([g, []]); last = g
        groups[-1][1].append(f'<a href="{h}"{" class=\"current\"" if h == current else ""}>{n}</a>')
    cols = ''.join(f'<div class="menu-g"><div class="menu-group">{g}</div>{"".join(items)}</div>' for g, items in groups)
    foot = '<div class="menu-foot"><a href="/">Home</a><a href="/notes/">Field Notes</a><a href="/#about">About Mark</a></div>'
    return f'<details class="menu"><summary><span class="chip">Tools ▾</span></summary><div class="menu-list">{cols}{foot}</div></details>'



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
<meta property="og:title" content="{t['name']}: {t['h1']}">
<meta property="og:description" content="{t['ogdesc']}">
<meta property="og:site_name" content="QuotaBird">
<meta property="og:image" content="https://quotabird.com/card-{t['slug']}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{t['name']}: {t['h1']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t['name']}: {t['h1']}">
<meta name="twitter:description" content="{t['ogdesc']}">
<meta name="twitter:image" content="https://quotabird.com/card-{t['slug']}.jpg">
<meta name="twitter:image:alt" content="{t['name']}: {t['h1']}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#F9FCFF">
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
    <p class="startnote">5 taps · about a minute · nothing stored</p>
    <p class="pillars">{' · '.join(q['n'].title() for q in t['questions'])}</p></div>
</div>

{bands}{mark}<section class="band" id="faq" aria-labelledby="faq-h">
  <div class="band-inner">
    <h2 id="faq-h">Questions</h2>
{faq_html}  </div>
</section>

<footer class="sitefoot">
  <p>{t['name']} is one of the free <a href="/">QuotaBird</a> tools by
    <a href="https://www.linkedin.com/in/markflournoy/" target="_blank" rel="noopener">Mark Flournoy</a>.</p>
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
    desc='Is it the rep, the patch, a skill gap or an effort gap? Five questions for sales managers. No names, nothing stored.',
    ogdesc='Before you write them up, figure out what you inherited. Five questions, one minute, no names.',
    h1='Before you write them up, figure out what you inherited.',
    dek='Five questions that separate a rep problem from a territory, skill or effort problem wearing a performance costume. For managers. No names.',
    cta='Check my rep',
    questions=[
        dict(k='patch', n='PATCH', q='Could a good rep make this number in this territory, on this plan?'),
        dict(k='customers', n='CUSTOMERS', q='Do customers choose to spend time with them? Do they get called back?'),
        dict(k='pipeline', n='PIPELINE', q="Is there pipeline that exists only because they're here?"),
        dict(k='craft', n='CRAFT', q="When they're in front of a customer, can they actually sell?"),
        dict(k='will', n='WILL', q='Are they still trying to win?'),
    ],
    bands=[
        ('how', 'Five questions, in this order', '''    <p class="lede">The first question a new manager asks is usually "what's wrong with these reps?" The better one
      is "what exactly did I inherit?" The order below is the order to think in.</p>
    <p><strong>PATCH: Could a good rep make this number here?</strong> Territory, account quality, installed base,
      the quota, the comp plan, the competitive situation, who has had the patch before. If three people have
      failed in the same patch, you probably do not have three bad reps. Look here first, and be honest, because
      nothing you do to the rep matters if the answer is no.</p>
    <p><strong>CUSTOMERS: Do customers choose them?</strong> Not meeting count. Five real customer conversations beat
      fifteen calendar entries. Do customers call back, take the next step, introduce them upward? The weird rep
      who skips internal meetings but has customers calling her may be worth more than the polished one with
      immaculate CRM hygiene and no pull.</p>
    <p><strong>PIPELINE: What exists because they're here?</strong> Separate inherited and renewal business from what
      they created. Ask where the pipeline came from, how old it is, whether it is moving, and what customer
      evidence makes it real. A seller can look fine today and leave a crater for next year.</p>
    <p><strong>CRAFT: Can they actually sell?</strong> Prospect, run discovery, understand the customer's business,
      qualify, get to power, build urgency, get through procurement, close. This is the question that separates
      <em>can't do it</em> from <em>isn't doing it</em>, and those are completely different management problems. One
      you coach. The other you manage.</p>
    <p><strong>WILL: Are they still trying to win?</strong> Energy, ownership, follow-through, coachability. A rep who
      has decided the year is over stops doing the things that would have saved it. The activity goes first, then
      the pipeline, then the rep.</p>'''),
        ('buckets', 'Four kinds of problem, and the one that isn\'t', '''    <p><strong>Good rep, bad situation.</strong> Fix the situation: the patch, the number, or the plan.</p>
    <p><strong>Good rep, skill gap.</strong> Coach them. Name the skill and work it, one deal at a time.</p>
    <p><strong>Capable rep, effort gap.</strong> Manage them. Expectations in writing, with dates.</p>
    <p><strong>Wrong rep, reasonable situation.</strong> Start the process. Waiting does not make it kinder.</p>
    <p><strong>They're fine.</strong> Leave them alone. Do not invent a management problem because they do not love
      one-on-ones. Figure out what visibility you actually need and let them sell.</p>
    <p>The mistake this tool exists to prevent is spending six months coaching a territory problem, or redesigning a
      territory to avoid dealing with a performance problem. The manager's first job is not to make everybody look
      alike. It is to figure out which differences matter to selling and which do not.</p>
    <p>Do not decide who is good and who is bad in your first few weeks. Sit with each rep and go through five real
      opportunities. Listen to how they describe the customer. You will learn more in that ninety minutes than in
      a month of dashboards, and every one of those five deals can go through <a href="/deal/">Deal Check</a> while
      you sit there.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. The five answers are scored in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your answers. Nothing else leaves the page unless you choose to share a result.'),
        ("Why does it never ask the rep's name?", 'Because it does not need it, and because a tool that stores judgments about named people is a different kind of tool. Run it, have the conversation, and nothing about it is written down anywhere.'),
        ('What do the verdicts mean?', "<strong>They're fine:</strong> leave them alone. <strong>The situation:</strong> good rep, bad patch, number or plan; fix that. <strong>Coach them:</strong> good rep, skill gap. <strong>Manage them:</strong> capable rep, effort gap; expectations and dates. <strong>Wrong rep:</strong> reasonable situation, wrong person. <strong>Not sure:</strong> too many sort-ofs; sit in five of their deals and run it again."),
        ('Why is PATCH the first question?', 'Because the order you ask in is the order you think in. A manager who starts with the territory, the number and the plan makes different decisions for the next six months than one who starts with the rep\'s calendar.'),
        ('Can I run it on myself?', 'Yes, and sellers should. If the patch answer is no, <a href="/territory/">Territory Check</a> makes that case to your manager with the sizing behind it.'),
    ],
    config='''CheckTool({
  slug: 'rep', name: 'Rep Check', url: 'https://quotabird.com/rep/',
  questions: [
    { k: 'patch',     n: 'PATCH',     q: 'Could a good rep make this number in this territory, on this plan?' },
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
      return { label: "They're fine", cls: 'ready', attack: 'Leave them alone.', sub: "Don't invent a management problem because they don't love one-on-ones. Decide what visibility you actually need and let them sell." };
    if (no('patch'))
      return { label: 'The situation', cls: 'prove', attack: 'Good rep, bad situation.', sub: 'Nobody makes a number in a patch that cannot produce one. Fix the territory, the number or the plan. Writing them up fixes none of them.' };
    if (no('craft') && no('will'))
      return { label: 'Wrong rep', cls: 'dont', attack: 'Reasonable situation, wrong person.', sub: "They can't and they've stopped trying. Start the process. Waiting does not make it kinder, for them or for the team." };
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
    pipeline: 'What have they created this year that they did not inherit?',
    craft: 'Have you watched them run a customer meeting?',
    will: 'Have you asked them whether they still want to do this?',
  },
  moves: {
    patch: 'Size the patch yourself before the next one-on-one. If it cannot produce the number, say so up the chain.',
    customers: 'Ask which three customers would take their call tomorrow, then call one.',
    pipeline: 'Split their pipeline into inherited and created. Put the created number on paper.',
    craft: 'Sit in their next two customer meetings. Say nothing. Watch.',
    will: 'Ask them directly, this week, whether they still want to do this. Listen to the answer.',
  },
  noMove: 'Nothing. Tell them the forecast looks good and ask what they need from you.',
  handoff: (s) => s.label === 'The situation'
    ? { overline: 'It is the patch', text: 'Send them Territory Check. It makes the case for them, with the sizing, without the argument.', href: '/territory/', label: 'Check my territory' }
    : { overline: 'Before you decide anything', text: "Sit with them and run their five biggest deals through Deal Check. Listen to how they answer. You'll know more in ninety minutes than in a month of dashboards.", href: '/deal/', label: 'Check my deal' },
  mark: { title: (s) => 'Not sure it\\'s ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I have inherited the team nobody wanted, coached a territory problem for six months before I figured it out, and kept a misfit who turned out to be the best seller on the floor. Send me one line. No names." },
  dm: (s) => `Mark, ran a rep through Rep Check. Verdict: ${s.label.toLowerCase()}. Weakest answer was ${s.weak.n.toLowerCase()}. Not sure I've got the right problem. Worth 20 minutes?`,
});''',
)

# ────────────────────────────── PARTNER CHECK ──────────────────────────────
PARTNER = dict(
    slug='partner', name='Partner Check',
    title='Partner Check: Is This Partnership Real?',
    desc='Five questions that separate a partner who sells with you from a logo on a slide. For partner managers. One minute, nothing stored.',
    ogdesc='Before you renew the partnership, test it. Five questions, one minute, no names.',
    h1='Before you renew the partnership, test it.',
    dek='Five questions that separate a partner who sells with you from a logo on a slide. For partner managers and anyone who owns a co-sell number. No names.',
    cta='Check my partner',
    questions=[
        dict(k='sourced', n='SOURCED', q="Have they brought you an opportunity you didn't find yourself?"),
        dict(k='accounts', n='ACCOUNTS', q='Is there a named account both sides are working right now?'),
        dict(k='owner', n='OWNER', q='Does someone on their side carry a number that includes you?'),
        dict(k='plan', n='PLAN', q='Is there a co-sell plan with dates on it, not a deck?'),
        dict(k='pull', n='PULL', q='Would they call you if you stopped calling them?'),
    ],
    bands=[
        ('how', 'The five questions, and what each one disproves', '''    <p class="lede">Everybody gets along. There have been plenty of meetings, maybe a joint slide deck. The question
      is whether anyone can point to the account where the two companies are actually trying to win something together.</p>
    <p><strong>SOURCED: Have they brought you anything?</strong> A partner who has never handed you an opportunity
      you did not already have is a partner you are working for. One sourced deal is worth a year of joint webinars.</p>
    <p><strong>ACCOUNTS: Is there a named account, right now?</strong> Not a target list. A customer, a requirement,
      two sellers who know each other's names. If nobody can name one, the partnership exists on a slide.</p>
    <p><strong>OWNER: Does someone on their side get paid when you win?</strong> Partnerships run on comp plans, not
      goodwill. If nobody at the partner carries a number that includes you, your deals are a favor, and favors do
      not scale.</p>
    <p><strong>PLAN: Is there a plan with dates?</strong> A deck says what the partnership could be. A plan says three
      accounts, two dates, and who owns each one. If it does not fit on a page, it is a deck.</p>
    <p><strong>PULL: Would they call you first?</strong> Stop calling for two weeks and see what happens. A real
      partner notices. The rest of them were waiting for you to do the work.</p>'''),
        ('verdicts', 'Four kinds of partner', '''    <p><strong>Real.</strong> Deals are moving with both names on them. Feed it.</p>
    <p><strong>All talk.</strong> Lots of activity, no deals. Everybody is busy and nothing closes. Most
      partnerships live here, and most of them never leave.</p>
    <p><strong>Neighbors.</strong> You get along. That is all that is happening.</p>
    <p><strong>Logo swap.</strong> They are on your slide, you are on theirs, and that is the partnership. Stop
      spending time on it and say so.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. The five answers are scored in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your answers. Nothing else leaves the page unless you choose to share a result.'),
        ('Does this work for the partner running it on me?', 'Yes, and that is the best use. Run it on each other, compare, and the gap between the two verdicts is the conversation you should have been having.'),
        ('What about a partner that is strategic but not producing yet?', 'Then the answer to SOURCED and ACCOUNTS is no, and the tool will say so. Strategic is what people call a partnership before it has produced anything. The question is how long you are willing to say it.'),
        ('Can I use it on a distributor or an SI?', 'Yes. The questions do not care which direction the paper flows. They care whether anyone on the other side is accountable for a deal with your name on it.'),
    ],
    config='''CheckTool({
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
    return { label: 'Logo swap', cls: 'dont', attack: "They're on your slide. You're on theirs.", sub: 'That is the whole partnership. Say so, and put the time somewhere that produces.' };
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
    owner: 'Find out whose comp plan includes you. If the answer is nobody, that is the problem.',
    plan: 'Replace the deck with one page: three accounts, two dates, one owner each.',
    pull: 'Stop calling for two weeks. See what happens.',
  },
  noMove: 'Keep doing what you are doing, and write down why it works before someone changes it.',
  handoff: (s) => s.total >= 55
    ? { overline: 'Is there a deal inside this partnership?', text: 'Run it through Deal Check. A real partner deal survives the same five questions any deal does.', href: '/deal/', label: 'Check my deal' }
    : { overline: 'How much of your number is leaning on them?', text: 'If this partner is in your coverage math, the math is wrong. Pipeline Check shows you by how much.', href: '/pipeline/', label: 'Check my pipeline' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I led partner sales teams at AWS for six years and sat on the other side of the table before that. I have seen every version of the partnership that looks great in the QBR and produces nothing. Send me one line. No partner names." },
  dm: (s) => `Mark, ran a partner through Partner Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. Not sure what to do with it. Worth 20 minutes?`,
});''',
)

# ────────────────────────────── TERRITORY CHECK ──────────────────────────────
TERRITORY = dict(
    slug='territory', name='Territory Check',
    title='Territory Check: Can This Patch Make the Number?',
    desc='Can the patch make the number, or are you being asked to grow where nobody could? Five questions for sellers. Nothing stored.',
    ogdesc='Before you sign up for the number, test the territory. Five questions, one minute, no account names.',
    h1='Before you sign up for the number, test the territory.',
    dek='Five questions that tell you whether the patch can make the number, or whether you are being asked to grow where nobody could. For sellers. No account names.',
    cta='Check my territory',
    questions=[
        dict(k='spend', n='SPEND', q='Is there enough addressable spend in the territory to make the number twice over?'),
        dict(k='accounts', n='ACCOUNTS', q="Can you name ten accounts you'd expect to buy this year?"),
        dict(k='base', n='BASE', q='Is there existing business to grow, not just logos to win?'),
        dict(k='access', n='ACCESS', q='Do you have a way in: relationships, partners, contract vehicles?'),
        dict(k='history', n='HISTORY', q='Has anyone made this number in this territory before?'),
    ],
    bands=[
        ('how', 'The five questions, and what each one disproves', '''    <p class="lede">A quota is a claim about a territory. Before you accept it, check whether the territory agrees.</p>
    <p><strong>SPEND: Is the money there twice over?</strong> Agency budgets, program lines, contract ceilings.
      If the total addressable spend is not at least double the number, you are not selling, you are hoping for
      share you have no reason to expect.</p>
    <p><strong>ACCOUNTS: Can you name ten?</strong> Not a list from the CRM. Ten accounts you personally expect to
      buy this year, with a reason for each. If you cannot get to ten, your manager should hear that in January,
      not October.</p>
    <p><strong>BASE: Is there anything to grow?</strong> A territory with installed base has a floor. A territory that
      is all new logos has a ceiling and no floor. Know which one you have, and put the inherited number on paper
      so nobody counts it twice.</p>
    <p><strong>ACCESS: Can you get in the door?</strong> A relationship, a partner who owns the account, a contract
      vehicle they already buy through. One route per account. Without one, the account is a name.</p>
    <p><strong>HISTORY: Has anyone done it?</strong> Find the last person who had the patch. If nobody has ever made
      this number here, you are the experiment, and you should be paid like one.</p>'''),
        ('now', 'What to do with the verdict', '''    <p>A bad territory verdict is not an excuse. It is a document. Take it to your manager in the first month, with
      the sizing behind it, and ask for one of three things: a different patch, a different number, or a different
      plan for how the gap gets filled. Managers respect the seller who does the math in January. They have no
      patience for the one who discovers it in Q4.</p>
    <p>A good verdict is worse news. The number is there. Now it is on you.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. The five answers are scored in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your answers. Nothing else leaves the page unless you choose to share a result.'),
        ('Is this just a way to argue about quota?', 'It is a way to argue about quota with evidence instead of feelings, which is the only version of that argument anyone has ever won.'),
        ('What if I am new and do not know the territory yet?', 'Then most answers will be sort of, and the verdict will say so. Run it again in 60 days. The gap between the two runs is what you learned.'),
        ('What about the coverage math?', 'That is the other tool. Once you know the territory can produce, <a href="/pipeline/">Pipeline Check</a> tells you how much pipeline it has to produce.'),
    ],
    config='''CheckTool({
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
    if (total >= 55) return { label: 'Thin', cls: 'proof', attack: 'It can be done. Not by accident.', sub: 'The territory will not carry you. Every account needs a plan.' };
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
    spend: 'Size the patch: agency budgets, program lines, contract ceilings. One page.',
    accounts: "Write the ten. If you can't get to ten, tell your manager now.",
    base: 'Separate inherited from created. Put the inherited number on paper.',
    access: 'Map one route per account: a relationship, a partner, or a vehicle.',
    history: 'Find the last person who had the patch. Buy them coffee.',
  },
  noMove: 'Build the plan for the ten accounts. The territory is not the problem.',
  handoff: (s) => s.total >= 55
    ? { overline: 'Now the coverage math', text: 'The territory can produce. Pipeline Check tells you how much it has to.', href: '/pipeline/', label: 'Check my pipeline' }
    : { overline: 'Take it to your manager', text: "Their version of this question is Rep Check, and its first question is the patch. Send them that with your sizing.", href: '/rep/', label: 'Check my rep' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I have inherited the patch nobody could grow and handed one out by mistake. If the verdict is bad, I can help you make the case. If it's good, I can help you make the plan. One line. No account names." },
  dm: (s) => `Mark, ran my territory through Territory Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. Want to make the case to my manager and not sure how. Worth 20 minutes?`,
});''',
)

OLR = dict(
    slug='olr', name='OLR Check',
    title='OLR Prep: Will Your Case Survive Calibration? | OLR Check',
    desc="Five questions that test the case you're making for a rep in OLR, then the room grills you. No names, no ratings, nothing stored.",
    ogdesc='Before you walk into OLR, test your case. Five questions, then the room grills you. No names, no ratings.',
    h1='Before you walk into OLR, test your case.',
    dek='Five questions that separate a case the room will accept from a story it will take apart. For managers with a rep to defend in calibration. No names, no ratings.',
    cta='Check my case',
    questions=[
        dict(k='receipts', n='RECEIPTS', q='Can you name three things they delivered this year, each with a number on it?'),
        dict(k='ownership', n='OWNERSHIP', q="For the biggest one, can you say what wouldn't have happened without them?"),
        dict(k='scope', n='SCOPE', q='Can you explain why that was work at their level, not strong execution a level down?'),
        dict(k='how', n='HOW', q="For every leadership principle you'll cite, do you have one specific example?"),
        dict(k='next', n='NEXT', q="Can you name the harder thing you'd hand them next year, and why?"),
    ],
    bands=[
        ('room', 'What the room is actually testing', '''    <p class="lede">The hardest part of a talent review is not the form. It is explaining a human being in sixty
      seconds to managers who don't know them, and having the explanation survive their questions.</p>
    <p>Every calibration room runs the same way: you propose, they probe, the evaluation moves if you can't hold it.
      The managers across the table are not hostile. They just haven't seen your rep's year, so all they can test is
      your case. A case is receipts, ownership, scope, behavior and next scope. Everything else is adjectives.</p>
    <p><strong>RECEIPTS: Three things, each with a number.</strong> Amazon's own self-review now asks for three to five
      accomplishments with measurable outcomes. If you can't name three with a number on them, the room hears "had a
      good year," and "had a good year" loses to anyone who brought a spreadsheet.</p>
    <p><strong>OWNERSHIP: What wouldn't have happened without them?</strong> The first question in any room is how much of
      the outcome belongs to this person versus the team, the partner, or the market. If you can answer that in one
      sentence for the biggest win, the rest of the case is easier.</p>
    <p><strong>SCOPE: Their level, not the level below.</strong> "Strong L5 execution" is the polite way a room says no to
      an L6 case. What made the problem their-level sized: the ambiguity, the number of teams, the absence of a
      playbook, the decisions nobody else was going to make?</p>
    <p><strong>HOW: One example per principle.</strong> Leadership principles are behavioral standards, not compliments.
      The room will ask for the example. If you'll cite four principles, bring four examples, and drop the ones you
      can't back.</p>
    <p><strong>NEXT: The harder thing.</strong> Potential is not "I think she's a future VP." It is the problem you would
      hand them next year that you wouldn't have handed them last year, and what they've already done that makes you
      sure. Scope, complexity, or impact, growing.</p>'''),
        ('bias', 'Check yourself before the room does', '''    <p class="lede">The case that fails in calibration is usually a good rep with a manager who brought impressions.</p>
    <p><strong>Recency.</strong> How much of your judgment comes from the last sixty days?</p>
    <p><strong>Visibility.</strong> Would you reach the same conclusion if this person weren't in your meetings every week?</p>
    <p><strong>Halo.</strong> Remove their biggest win. What does the rest of the year look like?</p>
    <p><strong>Horns.</strong> Remove their worst month. Same question.</p>
    <p><strong>Style.</strong> Are you evaluating impact, or whether they communicate the way you do?</p>
    <p><strong>Context.</strong> Did a reorg, a manager change, a leave, or a territory change alter what could reasonably
      be delivered? Say so first, before someone else does.</p>
    <p>This tool grades your case, never your rep. It will not tell you a rating, predict one, or suggest one, and it
      never asks for a name. What it will do is ask the questions the room is going to ask, before the room does.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. The five answers are scored in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your answers. Nothing else leaves the page unless you choose to share a result.'),
        ('Does it predict a rating?', 'No, and it never will. It grades the quality of your case: ready, not yet, a story, or no receipts. Your organization already has machinery for the rating. What it does not have is a rehearsal.'),
        ('What is OLR?', "Organization and Leadership Review: Amazon's annual talent review, where managers propose an evaluation for each of their people and then defend it in calibration with other managers, alongside promotion and development decisions. OLR Check is the rehearsal for the defending part."),
        ('Is this only for Amazon?', 'OLR is Amazon\'s name for it, and that is where most of the people who use these tools have sat. But every calibration room asks the same five things, whatever the company calls it. Read "leadership principle" as your organization\'s behavioral standard and the tool works the same.'),
        ('What does Grill me do?', 'It plays the room. Three hard questions about your weakest answer, one at a time, and you say honestly whether you can answer each. If you cannot answer two of three about ownership, that case is not ready, and better to learn that here than across the table.'),
        ('Why does it never ask the rep\'s name?', 'Because it does not need it, and because a tool that stores judgments about named people is a different kind of tool. Run it, fix the case, and nothing about it is written down anywhere.'),
    ],
    config='''CheckTool({
  slug: 'olr', name: 'OLR Check', url: 'https://quotabird.com/olr/',
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
    if (total >= 55) return { label: 'Not yet', cls: 'proof', attack: 'Your conclusion may be right. You have not documented enough to defend it.', sub: 'One more receipt on the weakest answer and this holds.' };
    if (total >= 35) return { label: 'A story', cls: 'prove', attack: "You're telling a story. The room wants receipts.", sub: 'Adjectives and impressions where outcomes, examples and artifacts should be.' };
    return { label: 'No receipts', cls: 'dont', attack: 'This will not survive the first question.', sub: "It may still be a good rep. It isn't a case yet." };
  },
  askedBy: 'The room will ask',
  grill: {
    receipts: 'What are the three, with the numbers?',
    ownership: 'How much of that outcome belongs to them versus the team around them?',
    scope: 'What specifically makes that their-level work rather than strong execution a level down?',
    how: 'Give me the example for that principle.',
    next: 'What would you give them next year that you would not have given them last year?',
  },
  grillSet: {
    receipts: ['You said they had a strong year. Which three things, and what were the numbers?', 'Remove the biggest win. What does the rest of the year look like?', 'Which of those three would still be true if the market had gone the other way?'],
    ownership: ['What happened that would not have happened without them?', 'Who else touched that outcome, and what did they contribute?', "If I asked the partner or the customer who drove it, whose name would they say?"],
    scope: ['What made this their-level work rather than strong execution one level down?', 'How many teams did they have to move without authority over any of them?', 'What decision did they make that nobody had made before?'],
    how: ['Give me the example for the first principle you are citing.', 'And the second one. Different example.', 'Which principle would you drop because you cannot back it, and why did it get in the draft?'],
    next: ['What harder problem have they already shown they can handle?', 'Where did they grow scope without being asked?', 'What feedback did they get this year, and what observable behavior changed?'],
  },
  grillBy: 'The room', grillLabel: 'Grill my case', fixLabel: 'Before the room',
  grillLines: { clean: 'Your case would survive.', one: 'Your case would mostly survive. One hole left.', bad: 'Your case would not survive.', cleanSub: 'Three questions from the room, three answers. Say the weakest receipt first.' },
  fix: {
    receipts: 'Write the three things down, each with its number, before you write anything else. If you cannot get to three, the case is the problem, not the rep.',
    ownership: 'For the biggest win, write one sentence starting "Without them, ...". If you cannot finish it, find the win where you can.',
    scope: 'Write what made the problem their-level sized: the teams, the ambiguity, the missing playbook, the decision nobody else would make.',
    how: 'Cut every principle you cannot attach an example to. A case with two backed principles beats one with six adjectives.',
    next: 'Name the harder assignment you would give them and the thing they already did that makes you sure. Potential is evidence, not a feeling.',
  },
  moves: {
    receipts: 'Write the three things, each with its number. If you cannot get to three, that is the finding.',
    ownership: 'Write one sentence beginning "Without them, ..." for the biggest win.',
    scope: 'Write what made it their-level work: teams moved, ambiguity, no playbook, the decision nobody else would make.',
    how: 'Cut every principle without an example. Keep the ones you can prove.',
    next: 'Name next year\\'s harder assignment and the evidence that says they can carry it.',
  },
  noMove: 'Put the weakest receipt first when you present. The room respects a case that leads with its own soft spot.',
  handoff: (s) => s.total >= 75
    ? { overline: 'The case is ready. Is the year set up?', text: "Next year's case starts now. Is the rep in a patch that can produce one? Rep Check asks that first.", href: '/rep/', label: 'Check my rep' }
    : { overline: 'The fastest receipt', text: 'A deal you watched them run. Sit in their next customer meeting and run it through Deal Check together. That is evidence for both of you.', href: '/deal/', label: 'Check my deal' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I have written the case that got taken apart in the room and the one that held, and the difference was never the rep. Send me one line about the case. No names, no ratings." },
  dm: (s) => `Mark, ran a rep's OLR case through OLR Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. OLR is coming and I'm not sure it holds. Worth 20 minutes?`,
  dmGrill: (s, missed) => `Mark, ran a rep's OLR case through OLR Check and could not answer ${missed} of the room's 3 ${s.weak.n.toLowerCase()} questions. Verdict was ${s.label.toLowerCase()}. Want to tell me what you'd go fix first?`,
});''',
)

BRIEF = dict(
    slug='brief', name='Brief Check',
    title='Brief Check: Will Your Brief Survive the Room?',
    desc="Five questions about the doc, deck or QBR you're about to present, then the room grills you. Nothing uploaded, nothing stored.",
    ogdesc="What's the question you're hoping nobody asks? Brief Check finds it before the meeting does.",
    h1="What's the question you're hoping nobody asks?",
    dek='Brief Check finds it before the meeting does. Five questions about the doc, the deck or the QBR you are about to present. Nothing uploaded.',
    cta='Check my brief',
    questions=[
        dict(k='point', n='POINT', q='Can you say in one sentence what you want them to decide, and why now?'),
        dict(k='receipts', n='RECEIPTS', q="For the three claims the argument depends on, do you have evidence that isn't your own team's opinion?"),
        dict(k='alternative', n='ALTERNATIVE', q='Have you dealt with the most credible other option, including doing nothing?'),
        dict(k='hole', n='HOLE', q='Do you know the weakest assumption in your own argument, and who in the room will find it?'),
        dict(k='ask', n='ASK', q='Is it completely clear what you need from them today, and who owns the next step?'),
    ],
    bands=[
        ('how', 'The room is not attacking the document', '''    <p class="lede">It is attacking the assumptions underneath it. Every brief that dies in a meeting dies the same way:
      somebody asks the question the author was hoping nobody would.</p>
    <p><strong>POINT: One sentence, and why now.</strong> If you cannot say what you want the room to decide in one
      sentence, the brief does not have a point yet, it has a topic. And "why now" is the second half of the
      sentence, because a room that agrees with you and does nothing has not agreed with you.</p>
    <p><strong>RECEIPTS: Evidence for the three claims it depends on.</strong> Not every claim. The three that, if
      false, take the recommendation down with them. Data, customer evidence, financials, documented behavior. And
      at least one piece that did not come from your own team, because the room discounts everything that did.</p>
    <p><strong>ALTERNATIVE: The other option, including nothing.</strong> This is where most executive documents
      fall apart. Why this instead of doing nothing? Why build instead of buy? Why us instead of them? If the brief
      does not answer the alternative someone in the room already prefers, that person will answer it for you.</p>
    <p><strong>HOLE: Your own weakest assumption, and who will find it.</strong> The most important question in the
      tool. If you know where the soft spot is, you can lead with it, and a room respects a brief that names its own
      risk. If you don't, somebody whose incentives differ from yours will find it, and they will not be gentle.</p>
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
    <p><strong>The skeptic.</strong> Whoever in the room is accountable for something you are not. They know
      something you don't. Find out what before the meeting.</p>
    <p>The brief lives in your head, not in a file. Nothing is uploaded, nothing is stored, and the tool never sees
      a word of the document. It only asks whether you could answer for it.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. The five answers are scored in your browser. No account, no upload, no API call. The site counts page views with Google Analytics and never sends your answers. Nothing else leaves the page unless you choose to share a result.'),
        ('What counts as a brief?', 'Anything you are about to argue for in front of people who can say no: a narrative doc, a strategy deck, a QBR, an account plan, a proposal, an investment memo, a capture review, or a recommendation you will make out loud. If it has a point and an ask, it is a brief.'),
        ('Is this only for sales?', 'No. It started with sales reviews, and the sales leader is one of the sharks. But a six-pager in front of a VP dies exactly the way a QBR does: on the question the author hoped nobody would ask.'),
        ('What does Grill me do?', 'It plays the room. Pick who is across the table, and it asks three of their questions about your weakest answer, one at a time. You say honestly whether you could answer. Better to find the hole here than in the meeting.'),
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
    if (total >= 75) return { label: 'Room ready', cls: 'ready', attack: 'Your argument is clear and the claims have receipts.', sub: 'Lead with the hole. A room respects a brief that names its own risk.' };
    if (total >= 55) return { label: 'A fight', cls: 'proof', attack: "Your recommendation may be sound. You've left an opening.", sub: 'They will find it. Better you find it first.' };
    if (total >= 35) return { label: 'Shark food', cls: 'prove', attack: "You're relying on assumptions, vague impact, or an unclear ask.", sub: 'The room will not argue with you. It will just move on.' };
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
  grillBy: 'The room', grillLabel: 'Grill my brief', fixLabel: 'Before the meeting',
  grillLines: { clean: 'Your brief would survive.', one: 'Your brief would mostly survive. One hole left.', bad: 'Your brief would not survive.', cleanSub: 'Three questions, three answers. Lead with the hole anyway.' },
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
  noMove: 'Lead with the hole. Say your weakest assumption out loud in the first minute; the room will spend the rest of the meeting on your terms.',
  handoff: (s) => s.total >= 75
    ? { overline: 'If the brief is about a deal', text: 'The room will ask whether the deal underneath it is real. Deal Check is that question.', href: '/deal/', label: 'Check my deal' }
    : { overline: 'If the brief is about the number', text: 'Vague impact usually means the coverage math is missing. Pipeline Check puts a number on it.', href: '/pipeline/', label: 'Check my pipeline' },
  mark: { title: (s) => 'Stuck on the ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I have written the doc that got shredded and the one that got funded, and the difference was always one question I hadn't asked myself. Send me one line about the brief. No document, no company name." },
  dm: (s) => `Mark, ran a brief through Brief Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is the ${s.weak.n.toLowerCase()}. Meeting is coming and I'm not sure it holds. Worth 20 minutes?`,
  dmGrill: (s, missed) => `Mark, ran a brief through Brief Check and could not answer ${missed} of the room's 3 questions about the ${s.weak.n.toLowerCase()}. Verdict was ${s.label.toLowerCase()}. Want to tell me what you'd go fix first?`,
});''',
)

for t in (REP, PARTNER, TERRITORY, OLR, BRIEF):
    os.makedirs(t['slug'], exist_ok=True)
    html = page(t)
    assert '—' not in html and '–' not in html, t['slug']
    open(f"{t['slug']}/index.html", 'w').write(html)
    print(t['slug'], len(html))


# ────────────────────────────── FIELD NOTES ──────────────────────────────
# Short reads in Mark's voice. Each ends with the tool that does the math.
# Add a note here, run the script, commit notes/<slug>/index.html.
NOTES = [
    dict(slug='3x-is-a-win-rate', title='3X is a win rate in disguise',
         dek='Everybody plans to it. Almost nobody asks where it came from.',
         body='''    <p class="lede">Three times the number in qualified pipeline is the coverage rule most sales organizations
      plan to. Almost nobody asks where it came from.</p>
    <p>It came from a win rate. If a third of the qualified pipeline due in a period closes, 3X covers the number
      exactly. So 3X is a 33% win rate written down without saying so.</p>
    <p>Here's why that matters. A team that wins 20% of what it qualifies needs 5X. A team that wins half needs
      2X. If your team wins 20% and plans to 3X, the forecast is wrong on day one, and nobody finds out until the
      quarter is mostly gone.</p>
    <p>The other word doing a lot of work is <em>qualified</em>. Coverage only counts pipeline that would survive a
      hard question about the customer, the money, the person you're talking to, the path to a purchase order and
      the reason it happens now. Everything else in the CRM is a conversation.</p>
    <h3>Here's a simple way to tell</h3>
    <p>Take your qualified win rate for the last four quarters. Divide one by it. That's your coverage number, not
      three. Then count only the pipeline you'd defend in a review, and hold it up against that.</p>''',
         tool=('/pipeline/', 'Pipeline Check', 'does both in about a minute, and shows the 3X line and yours on the same bar.')),
    dict(slug='why-not-bant-or-meddic', title="Why I don't start with BANT or MEDDIC",
         dek="They're useful when you're working a deal. The trouble is the moment before that.",
         body='''    <p class="lede">I've used both, and plenty of versions of both. They're useful when you're working a deal.
      The trouble is the moment before that.</p>
    <p>Over the years, most questionable deals I've seen broke in one of five places. Nobody at the customer had
      said out loud that they wanted it. The money didn't have a name. We hadn't met anyone who could make it
      happen. Nobody knew how they'd actually buy it. And nothing was forcing it this year.</p>
    <p>BANT gets you close, but its need is usually something the seller diagnosed, and its timeline is a date in
      the CRM rather than a reason anything happens. It also skips the biggest federal question: how does a
      purchase order actually appear? Contract vehicle, contracting office, acquisition lead time. That's the
      timeline.</p>
    <p>MEDDIC, or MEDDPICC depending on who taught it to you, is more sophisticated, and that's exactly why it
      solves a different problem. A seller can spend forty-five minutes deciding whether somebody counts as an
      economic buyer. Five plain questions are a cross-examination, not a worksheet. They run before that debate is
      worth having.</p>
    <p class="lede">MEDDIC helps you work the deal. The five questions help you decide whether you've earned the
      right to call it one.</p>''',
         tool=('/deal/', 'Deal Check', 'is the five questions, with the arithmetic done and the question your manager will ask.')),
    dict(slug='three-people-same-patch', title='If three people failed in the same patch',
         dek="You probably don't have three bad reps.",
         body='''    <p class="lede">If three people have failed in the same patch, you probably don't have three bad reps.</p>
    <p>The first question most new managers ask is what's wrong with these reps. The better one is what exactly did
      I inherit. The order you ask in is the order you think in, and it decides what you do for the next six
      months.</p>
    <p>Start with the patch. Territory, account quality, installed base, the quota, the comp plan, who had it
      before. If a good rep couldn't make the number there, nothing you do to the person matters. Fix the patch,
      fix the number, or fix the plan.</p>
    <p>Then the person, in this order. Do customers choose to spend time with them? Is there pipeline that exists
      only because they're here? When they're in front of a customer, can they actually sell? Are they still
      trying to win? The third question is the one most managers skip, and it's the one that separates can't from
      isn't. One you coach. The other you manage.</p>
    <p>Watch out for the rep you'd write off first. The one who skips internal meetings but has customers calling
      back may be worth more than the polished one with perfect CRM hygiene and no pull.</p>
    <h3>Before you decide anything</h3>
    <p>Sit with them and go through five real opportunities. Listen to how they describe the customer. You'll learn
      more in ninety minutes than in a month of dashboards.</p>''',
         tool=('/rep/', 'Rep Check', 'asks the patch first and the person second, and tells you which problem you have.')),
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
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#F9FCFF">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#101418">
<link rel="stylesheet" href="/site.css">
<script src="/analytics.js" defer></script>
'''
NOTE_TAIL = '''<footer class="sitefoot">
  <p>Field Notes are part of <a href="/">QuotaBird</a>, a shelf of free tools by
    <a href="https://www.linkedin.com/in/markflournoy/" target="_blank" rel="noopener">Mark Flournoy</a>.</p>
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
    html = note_head(n['title'], n['dek'], url) + f'''<script type="application/ld+json">
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

idx = note_head('Field Notes', 'Short reads on things everybody in tech sales says that deserve a second look.', 'https://quotabird.com/notes/') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note">
  <h1>Field Notes</h1>
  <p class="dek">Short reads on things everybody in tech sales says that deserve a second look. Each one ends with a
    tool that does the math.</p>
  ''' + note_list() + '''
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL
os.makedirs('notes', exist_ok=True)
open('notes/index.html', 'w').write(idx)
print('notes', len(NOTES))

# ────────────────────────────── HOME ──────────────────────────────
# The home page source lives in home.src.html; this fills in the note list and build stamp.
home = open('home.src.html').read().replace('__NOTES__', note_list()).replace('__BUILD__', BUILD)
open('index.html', 'w').write(home)

# ────────────────────────────── CALCULATORS (Quota, Discount, Commission) ──────────────────────────────
# Rebuilt from the old Fedmo tools: Is My Quota Crazy?, They Want a Discount, Commissions Take-Home.
CALCS = [
 dict(slug='quota', name='Quota Check',
  title='Quota Check: Is My Quota Crazy?',
  desc='Your quota against your on-target earnings. Multiples under 3 and over 10 both mean something. Free, in your browser, nothing stored.',
  ogdesc='Is my quota crazy? Base, variable and quota in, a straight answer out.',
  h1='Is my quota crazy?', dek='Base salary, target variable and the number they handed you. We\'ll tell you where the plan sits against what\'s normal, and what it asks of your patch.',
  fields=[dict(id='base',kind='money',label='Base salary',example='$90K'),dict(id='variable',kind='money',label='Target variable at 100%',example='$90K'),
          dict(id='quota',kind='money',label='Your quota for the year',example='$1.2M'),dict(id='closed',kind='money',label='What you closed last year',example='',placeholder='$0 (optional)')],
  card=dict(headline=['Is my quota crazy?',''],dek='Your number against your on-target earnings, and what it asks of your patch.',pillars=['OTE','MULTIPLE','VARIABLE','GROWTH']),
  bands=[('how','What the multiple means','''    <p class="lede">Divide your quota by your on-target earnings. That one number tells you more about the plan than the plan will.</p>
    <p>Somewhere between 4 and 6 is the usual range for mid-market SaaS and cloud reps: the company expects to pay you roughly a fifth of what you bring in. Below 3 is unusual, and usually means a ramp quota, an overlay role, or a plan with a catch in it. Six to eight is enterprise at a big CSP, and it needs a strong pipeline behind it. Eight to ten is strategic and named-account territory, where you'll need three to four times coverage and a patch that can produce it. Above ten, the plan is asking the territory for something it may not have.</p>
    <p>The second number that matters is variable as a share of OTE. Under 40% and the quota matters less than it looks; over 60% and it's most of your pay, so treat it like one. And if you closed last year, the growth the new number implies is the honest measure of how much harder this year is.</p>
    <p>None of this says the number is wrong. It says where it sits. Whether the patch can produce it is <a href="/territory/">Territory Check</a>, and how much pipeline it takes is <a href="/pipeline/">Pipeline Check</a>.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The arithmetic runs in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your numbers. Nothing else leaves the page unless you choose to share a result.'),
       ('Where do the ranges come from?','Years of looking at comp plans at cloud providers, SaaS companies and their partners. They are typical ranges, not rules, and roles differ: an overlay or a ramp quota can be low and correct, and a strategic account role can be high and still fair.'),
       ('What if my variable is a bonus, not commission?','Use the target amount at 100% attainment either way. The tool cares about how much of your pay depends on the number, not what the plan calls it.')],
  config='''CalcTool({
  slug: 'quota', name: 'Quota Check', url: 'https://quotabird.com/quota/',
  fields: [{ id: 'base', kind: 'money' }, { id: 'variable', kind: 'money' }, { id: 'quota', kind: 'money' }, { id: 'closed', kind: 'money' }],
  compute(v) {
    if (!(v.base > 0 && v.variable > 0 && v.quota > 0)) return null;
    const ote = v.base + v.variable, mult = v.quota / ote, share = v.variable / ote, X = mult.toFixed(1) + '×';
    const pct = (r) => Math.round(r * 100) + '%';
    const money = (n) => n >= 1e6 ? '$' + (n / 1e6).toFixed(2).replace(/\\.?0+$/, '') + 'M' : n >= 1e3 ? '$' + Math.round(n / 1e3) + 'K' : '$' + Math.round(n);
    let t;
    if (mult < 3) t = ['Low', 'proof', `Quota is ${X} OTE. That's unusually low: a ramp, an overlay, or a plan with a catch in it.`, 'Read the plan twice. Low multiples usually come with a condition.'];
    else if (mult <= 4) t = ['Favorable', 'ready', `Quota is ${X} OTE, below the usual 4 to 6.`, 'Common in SMB, commercial and brand-new patches. Enjoy it while it lasts.'];
    else if (mult <= 6) t = ['Standard', 'ready', `Quota is ${X} OTE, inside the usual 4 to 6.`, "The number is fair. Whether the patch can produce it is a different question."];
    else if (mult <= 8) t = ['A stretch', 'proof', `Quota is ${X} OTE, above the usual range.`, 'Normal for enterprise at a big CSP, and it needs a strong pipeline behind it.'];
    else if (mult <= 10) t = ['Aggressive', 'prove', `Quota is ${X} OTE. Strategic and named-account territory.`, "You'll need 3 to 4X coverage and a patch that can produce it."];
    else t = ['Crazy', 'dont', `Quota is ${X} OTE. The plan is asking the patch for something it may not have.`, 'Check the territory before you sign, and get the sizing in writing.'];
    const growth = v.closed > 0 ? (v.quota - v.closed) / v.closed : null;
    const rows = [['On-target earnings', money(ote)], ['Quota ÷ OTE', X], ['Variable share of OTE', pct(share)]];
    if (growth != null) rows.push(['Growth over what you closed', (growth >= 0 ? '+' : '') + pct(growth), growth > .3 ? 'v-no' : '']);
    const note = share < .4 ? 'Variable is under 40% of OTE. You are paid mostly to show up, and the quota matters less than it looks.' : share > .6 ? 'Variable is over 60% of OTE. The quota is most of your pay. Treat it like one.' : '';
    return { label: t[0], cls: t[1], attack: t[2], sub: t[3], big: X, rows, note, mult, share, growth, ote, quota: v.quota };
  },
  handoff: (s) => ({ overline: 'Now the coverage math', text: `At 3X you'd need about ${(s.quota * 3 / 1e6).toFixed(1)}M of qualified pipeline to cover it. Your win rate will say more.`.replace('about ', 'about $'), href: `/pipeline/#t=${Math.round(s.quota)}&y=cy`, label: 'Check my pipeline' }),
  mark: { title: () => 'Is the plan sane?', body: "I'm Mark. I've been handed the crazy number and handed one out by mistake. If the multiple is off, I can help you make the case. If it's fair, I can help you make the plan. One line, no company name, no dollar figures." },
  dm: (s) => `Mark, ran my comp plan through Quota Check. Quota is ${s.big} OTE and variable is ${Math.round(s.share * 100)}% of OTE${s.growth != null ? ', ' + Math.round(s.growth * 100) + '% over what I closed last year' : ''}. Not sure it's sane. Worth 20 minutes?`,
  bookNote: (s) => `Quota Check: ${s.big} OTE, variable ${Math.round(s.share * 100)}% of OTE, ${s.label.toLowerCase()}.`,
});'''),
 dict(slug='discount', name='Discount Check',
  title='Discount Check: What a Discount Costs You',
  desc='They want a discount. See what it costs in your commission and the company\'s margin before you say yes. Free, in your browser, nothing stored.',
  ogdesc='They want a discount. Here is exactly what it costs you before you sharpen the pencil.',
  h1='They want a discount.', dek='List price, the discount they\'re asking for, your margin and your rate. We\'ll show what it costs you and what it costs the company, before you agree to anything.',
  fields=[dict(id='list',kind='money',label='Full list price',example='$500K'),dict(id='disc',kind='pct',label='Discount they want',example='15%'),
          dict(id='margin',kind='pct',label="Company gross margin",example='40%'),dict(id='rate',kind='pct',label='Your commission rate',example='8%')],
  card=dict(headline=['They want a discount.',''],dek='What it costs you in commission, and the company in margin, before you say yes.',pillars=['PRICE','DISCOUNT','MARGIN','YOUR CUT']),
  bands=[('how','A discount is a purchase','''    <p class="lede">Every point off the price buys something. The question is whether you got it.</p>
    <p>Up to about 5% is normal negotiation. Nobody remembers it. Between 5 and 15% is meaningful, and it should buy something specific: a signature date, a larger scope, a reference, a multi-year term. Above 15% you are paying for a decision, so make sure a decision is what you're getting, this quarter, in writing. Above 25%, you're usually paying to be liked, and the customer will remember the number, not the gesture.</p>
    <p>Two things sellers forget. The discount comes out of your commission at exactly the same rate it comes out of revenue, so a 15% discount is a 15% pay cut on that deal. And it comes out of the company's margin much faster than 15%: cost of goods doesn't move, so every dollar off the price is a dollar off the margin.</p>
    <p>Before you discount at all, ask whether the objection is the price or the deal. A discount fixes exactly one of those. <a href="/deal/">Deal Check</a> tells you which one you have.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The arithmetic runs in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your numbers. Nothing else leaves the page unless you choose to share a result.'),
       ('How is the new margin calculated?','Cost of goods stays the same when the price drops, so the margin after discount is one minus cost divided by the discounted price. That is why a 15% discount on a 40% margin leaves about 29%, not 25%.'),
       ('What if I don\'t know the company margin?','Leave it at the example and read the commission rows only. The margin rows are for the conversation with your manager; the commission row is the one that is about you.')],
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
    if (v.disc <= .05) t = ['Normal', 'ready', 'Inside normal negotiation range.'];
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
  handoff: { overline: 'Before you discount', text: 'Is it the price, or the deal? A discount fixes exactly one of those.', href: '/deal/', label: 'Check my deal' },
  mark: { title: () => 'Stuck on the price?', body: "I'm Mark. Most of the discounts I've watched given away bought nothing but a warmer feeling. If you're being asked to sharpen the pencil, send me one line about why. No customer names, no dollar figures." },
  dm: (s) => `Mark, ran a discount through Discount Check. ${Math.round(s.disc * 100)}% off costs me ${Math.round(s.disc * 100)}% of my commission${s.newMargin != null ? ' and takes margin from ' + Math.round(s.margin * 100) + '% to ' + Math.round(s.newMargin * 100) + '%' : ''}. Not sure it's worth it. Worth 20 minutes?`,
  bookNote: (s) => `Discount Check: ${Math.round(s.disc * 100)}% off${s.newMargin != null ? ', margin ' + Math.round(s.margin * 100) + '% to ' + Math.round(s.newMargin * 100) + '%' : ''}, ${s.label.toLowerCase()}.`,
});'''),
 dict(slug='commission', name='Commission Check',
  title='Commission Check: Your Take-Home on a Deal',
  desc='Deal size and commission rate in, what you actually take home out, after a realistic withholding estimate. Free, in your browser, nothing stored.',
  ogdesc='It closed. Here is roughly what you actually take home.',
  h1='It closed. What do I actually take home?', dek='Deal size, your rate, and how you\'re paid. A planning estimate of the check after withholding, not tax advice.',
  fields=[dict(id='deal',kind='money',label='Deal size',example='$500K'),dict(id='rate',kind='pct',label='Your commission rate',example='8%'),
          dict(id='profile',kind='choice',label='How you are paid',example='w2',options=[('w2','W-2 (~30%)'),('high','High bracket (~40%)'),('1099','1099 (~20%)')])],
  card=dict(headline=['It closed.','What do I take home?'],dek='A planning estimate of the check after withholding, in about ten seconds.',pillars=['DEAL','RATE','WITHHELD','TAKE-HOME']),
  bands=[('how','Why the check is smaller than the math','''    <p class="lede">Gross commission is the number in the plan. Take-home is the number in your account. They are further apart than most sellers expect the first time.</p>
    <p>A standard W-2 payout typically has about 30% withheld between federal, state and payroll taxes; a high-bracket earner is closer to 40%; a 1099 contractor has nothing withheld and should set aside roughly 20% or more themselves. These are planning estimates. Your actual rate depends on your state, your filing status and what else you earned this year, and supplemental wages are often withheld at a flat rate that gets reconciled at tax time.</p>
    <p>Use it to plan, not to argue with payroll. And once you know what a deal pays, the more useful question is whether the plan behind it is sane: <a href="/quota/">Quota Check</a>.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The arithmetic runs in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your numbers. Nothing else leaves the page unless you choose to share a result.'),
       ('Is this tax advice?','No. The withholding percentages are planning estimates. Your actual rate depends on your state, filing status and total income for the year. For anything that matters, ask an accountant.'),
       ('What about accelerators and clawbacks?','Enter the rate that applies to this deal. If your plan has accelerators above quota, use the accelerated rate; if it has clawbacks, remember the take-home is provisional until the clawback window closes.')],
  config='''CalcTool({
  slug: 'commission', name: 'Commission Check', url: 'https://quotabird.com/commission/',
  fields: [{ id: 'deal', kind: 'money' }, { id: 'rate', kind: 'pct' }, { id: 'profile', kind: 'choice', example: 'w2' }],
  compute(v) {
    if (!(v.deal > 0 && v.rate > 0)) return null;
    const money = (n) => n >= 1e6 ? '$' + (n / 1e6).toFixed(2).replace(/\\.?0+$/, '') + 'M' : n >= 1e3 ? '$' + Math.round(n / 1e3).toLocaleString() + 'K' : '$' + Math.round(n).toLocaleString();
    const tax = { w2: .30, high: .40, '1099': .20 }[v.profile] ?? .30;
    const gross = v.deal * v.rate, withheld = gross * tax, net = gross - withheld;
    return { label: 'Take-home', cls: 'ready', big: money(net), attack: `You keep about ${Math.round((1 - tax) * 100)} cents of every commission dollar on this deal.`,
      sub: 'A planning estimate, not tax advice.', rows: [['Gross commission', money(gross)], ['Withheld, about', money(withheld), 'v-no'], ['Take-home, about', money(net)]], keep: 1 - tax };
  },
  handoff: { overline: 'Is the plan sane?', text: 'Now that you know what a deal pays, check the number it has to cover.', href: '/quota/', label: 'Check my quota' },
  mark: { title: () => 'Questions about the plan?', body: "I'm Mark. Comp plans are where sellers find out what the company actually wants. If yours doesn't add up, send me one line. No company name, no dollar figures." },
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
        return f'        <label class="tf"><span class="tf-label">{f["label"]}</span><input id="{f["id"]}" type="text" inputmode="{mode}" autocomplete="off"{val}{ph}></label>\n'
    fields = ''.join(field(f) for f in t['fields'])
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
<meta property="og:title" content="{t['name']}: {t['h1']}">
<meta property="og:description" content="{t['ogdesc']}">
<meta property="og:site_name" content="QuotaBird">
<meta property="og:image" content="https://quotabird.com/card-{t['slug']}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{t['name']}: {t['h1']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t['name']}: {t['h1']}">
<meta name="twitter:description" content="{t['ogdesc']}">
<meta name="twitter:image" content="https://quotabird.com/card-{t['slug']}.jpg">
<meta name="twitter:image:alt" content="{t['name']}: {t['h1']}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#F9FCFF">
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
<script src="../analytics.js" defer></script>
</head>
<body class="wide-page">

<div class="wrap wide">
  <header class="appbar"></header>
  <div id="screen" class="calc-screen">
    <span class="overline tool-name">{t['name']}</span>
    <h1>{t['h1']}</h1>
    <p class="dek">{t['dek']} <span id="exnote">These are example numbers; type yours over them.</span></p>
    <div class="calc">
      <form class="calc-in" id="f" autocomplete="off" novalidate>
{fields}      </form>
      <div class="calc-out" id="out" aria-live="polite"></div>
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
  <p>{t['name']} is one of the free <a href="/">QuotaBird</a> tools by
    <a href="https://www.linkedin.com/in/markflournoy/" target="_blank" rel="noopener">Mark Flournoy</a>.</p>
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


# ────────────────────────────── SHARED CHROME ──────────────────────────────
# Every page gets the same header and the same About section, from one source.
MARK_SRC = open('partials/mark.html').read()
def root_of(path):
    if path == '404.html': return '/'
    return '../' * path.count('/')
def utm_of(path):
    return 'home' if path == 'index.html' else path.split('/')[0]
def current_of(path):
    return '/' if path == 'index.html' else '/' + path.rsplit('/', 1)[0] + '/'
def header(path):
    b = root_of(path)
    ask = '/#ask' if path in ('404.html',) else '#ask'
    return f'''<header class="appbar">
    <a class="logo" href="/" aria-label="QuotaBird, home"><picture><source srcset="{b}logo-dark.svg" media="(prefers-color-scheme: dark)"><img class="brandmark" src="{b}logo.svg" alt="" width="39" height="34"></picture> QuotaBird</a>
    <nav class="topnav" aria-label="Site">
      <a class="toplink" href="/notes/">Field Notes</a>
      <a class="toplink" href="/#about">About</a>
      <a class="chip chip-ask" href="{ask}">Ask Mark</a>
      {menu(current_of(path) if not path.startswith('notes/') else '/notes/')}
    </nav>
  </header>'''
def chrome(path):
    s = open(path).read()
    # preload the one font every page uses, so headlines don't flash in a fallback face
    if 'rel="preload" href="/inter.woff2"' not in s:
        s = s.replace('<meta name="viewport"', '<link rel="preload" href="/inter.woff2" as="font" type="font/woff2" crossorigin>\n<meta name="viewport"', 1)
    s = re.sub(r'<header class="appbar">.*?</header>', lambda m: header(path), s, count=1, flags=re.S)
    ask = '/#ask' if path == '404.html' else '#ask'
    if 'class="foot-nav"' not in s:
        s = s.replace('<footer class="sitefoot">', f'<footer class="sitefoot">\n  <p class="foot-nav"><a href="/">Tools</a><a href="/notes/">Field Notes</a><a href="/#about">About</a><a href="{ask}">Ask Mark</a></p>', 1)
    if path != '404.html':
        mark = MARK_SRC.replace('{ROOT}', root_of(path)).replace('{UTM}', utm_of(path))
        s = re.sub(r'<section class="band" id="(?:about|mark)"[^>]*>.*?</section>\n*', lambda m: mark, s, count=1, flags=re.S)
    open(path, 'w').write(s)
PAGES = ['index.html', 'deal/index.html', 'pipeline/index.html'] + [f'{t["slug"]}/index.html' for t in (REP, PARTNER, TERRITORY, OLR, BRIEF)] \
        + [f'{c["slug"]}/index.html' for c in CALCS] + ['notes/index.html'] + [f'notes/{n["slug"]}/index.html' for n in NOTES] + ['404.html']
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

# ── sitemap, from the same page list ──
_urls = [p for p in PAGES if p != '404.html']
def _loc(p): return 'https://quotabird.com/' + ('' if p == 'index.html' else p[:-len('index.html')])
def _pri(p): return '1.0' if p == 'index.html' else '0.6' if p.startswith('notes/') and p != 'notes/index.html' else '0.8'
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{_loc(p)}</loc><lastmod>{BUILD[:10]}</lastmod><priority>{_pri(p)}</priority></url>\n' for p in _urls) + '</urlset>\n')
print('sitemap', len(_urls), 'urls')
