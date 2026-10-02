#!/usr/bin/env python3
"""Builds rep/index.html, partner/index.html and territory/index.html from one template.
Run from the web root after editing copy below. Deal Check and Pipeline Check are hand-written."""
import json, os, re

BUILD = '2026-11-07.2100'
TOOLS = [
    ('Your number', '/quota/', 'Quota Check', 'The day the number lands'),
    ('Your number', '/quota-case/', 'Quota Case', 'When you need to push back'),
    ('Your number', '/territory/', 'Territory Check', 'Month one in a new territory'),
    ('Your number', '/discount/', 'Discount Check', 'When they ask you to sharpen the pencil'),
    ('Your pay', '/pay/', 'Pay Check', 'When you want to know what the plan really pays'),
    ('Your pay', '/commission/', 'Commission Check', 'When it closes'),
    ('Your pay', '/comp-plan/', 'Comp Plan Check', 'Before you count on the plan'),
    ('Your pay', '/offer/', 'Offer Check', 'When you have two offers'),
    ('Your team', '/pipeline/', 'Pipeline Check', 'Quarterly, before the review'),
    ('Your team', '/risk/', 'Risk Check', 'When coverage looks fine and you don\'t trust it'),
    ('Your team', '/rep/', 'Rep Check', 'When a rep is worrying you'),
    ('Your team', '/partner/', 'Partner Check', 'Before you renew the partnership'),
    ('Your team', '/olr/', 'Talent Review', 'Review season'),
    ('Your deal', '/deal/', 'Deal Check', 'Before you put it in commit'),
    ('Your deal', '/account/', 'Account Check', 'When you only know one person there'),
    ('Your deal', '/commit/', 'Commit Check', 'When a commit might not burn'),
    ('Your deal', '/federal-readiness/', 'Federal Readiness Check', 'Before you bet on federal'),
    ('Your deal', '/competition/', 'Competition Check', 'When you\'re not sure you\'re ahead'),
    ('Any meeting', '/brief/', 'Brief Check', 'When someone in the room can say no'),
]

def menu(current):
    # Four groups in a two-by-two grid: Your number over Your pay on the left, Your deal over Your team on the right.
    # Brief Check is left out of the menu on purpose (Mark's call, Nov 3); it stays on the home page and at /brief/.
    MENU_SKIP = {'/brief/', '/federal-readiness/'}   # Federal Readiness lives on /federal/ and the home list
    groups, last = {}, []
    for g, h, n, d in TOOLS:
        if h in MENU_SKIP: continue
        if g not in groups: groups[g] = []; last.append(g)
        groups[g].append(f'<a href="{h}"{" class=\"current\"" if h == current else ""}>{n}</a>')
    left = [g for g in ('Your number', 'Your pay') if g in groups]
    right = [g for g in ('Your deal', 'Your team') if g in groups]
    rest = [g for g in last if g not in left + right]          # any future group goes to the shorter column
    for g in rest: (left if sum(len(groups[x]) for x in left) <= sum(len(groups[x]) for x in right) else right).append(g)
    col = lambda gs: '<div class="menu-col">' + ''.join(f'<div class="menu-g"><div class="menu-group">{g}</div>{"".join(groups[g])}</div>' for g in gs) + '</div>'
    wide_html = ''
    foot = '<div class="menu-foot"><a href="/">Home</a><a href="/math/">Sales Math</a><a href="/notes/">Field Notes</a><a href="/about/">About</a><a href="/work-with-mark/">Work with Mark</a></div>'
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
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0B1215">
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
  <p>Questions or security issues: <a href="mailto:mark@quotabird.com">mark@quotabird.com</a></p>
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
    cta='Check your rep',
    questions=[
        dict(k='patch', n='TERRITORY', q='Could a good rep make this number in this territory, on this plan?'),
        dict(k='customers', n='CUSTOMERS', q='Do customers choose to spend time with them? Do they get called back?'),
        dict(k='pipeline', n='PIPELINE', q="Is there pipeline that exists only because they're here?"),
        dict(k='craft', n='CRAFT', q="When they're in front of a customer, can they actually sell?"),
        dict(k='will', n='WILL', q='Are they still trying to win?'),
    ],
    bands=[
        ('how', 'Five questions, in this order', '''    <p class="lede">New managers usually start with "what's wrong with these reps?" Start with "what exactly did I inherit?" instead, and go down the list below in order.</p>
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
    <p>The point is to avoid six months of coaching a territory problem, or six months of blaming a territory because you don't want to deal with a rep problem. Figure out which one you've got.</p>
    Don't decide who's good and who's bad in your first few weeks. Sit with each rep and go through five real deals, and listen to how they talk about the customer. You can run each one through <a href="/deal/">Deal Check</a> while you're at it.'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ("Why does it never ask the rep's name?", 'It doesn\'t need one, and a tool shouldn\'t store opinions about named people. Run it, have the conversation, and nothing gets written down.'),
        ('What do the verdicts mean?', "<strong>They're fine:</strong> leave them alone. <strong>The situation:</strong> good rep, bad territory, number or plan; fix that. <strong>Coach them:</strong> good rep, skill gap. <strong>Manage them:</strong> capable rep, effort gap; expectations and dates. <strong>Wrong rep:</strong> reasonable situation, wrong person. <strong>Not sure:</strong> too many sort-ofs; sit in five of their deals and run it again."),
        ('Why is TERRITORY the first question?', 'Start with the territory and the number before you decide the rep is broken. You\'ll make a different decision.'),
        ('Can I run it on myself?', 'Yes, and sellers should. If the territory answer is no, <a href="/territory/">Territory Check</a> makes that case to your manager with the sizing behind it.'),
    ],
    config='''CheckTool({
  slug: 'rep', answers: {"They're fine": "Neither. They're fine.", "The situation": "The territory.", "Coach them": "The rep: a skill gap.", "Manage them": "The rep: an effort gap.", "Wrong rep": "The rep. Wrong fit.", "Not sure": "Not clear yet."}, name: 'Rep Check', url: 'https://quotabird.com/rep/',
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
    ? { overline: 'It\\'s the territory', text: 'Send them Territory Check. Do the math before you turn it into a people argument.', href: '/territory/', label: 'Check your territory' }
    : { overline: 'Before you decide anything', text: "Sit with them and run their five biggest deals through Deal Check, and listen to how they answer. Ninety minutes of that beats a month of dashboards.", href: '/deal/', label: 'Check your deal' },
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
    cta='Check your partner',
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
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('Does this work for the partner running it on me?', 'Yes. Run it on each other and compare answers. Start where you disagree.'),
        ('What about a partner that\'s strategic but not producing yet?', 'Then the answer to SOURCED and ACCOUNTS is no, and the tool will say so. "Strategic" is what people call a partnership before it\'s produced anything.'),
        ('Can I use it on a distributor or an SI?', 'Yes. The questions don\'t care which direction the paper flows. They care whether anyone on the other side is accountable for a deal with your name on it.'),
    ],
    config='''CheckTool({
  aside: (s, a) => ['accounts', 'pull'].some(k => a[k] && a[k] !== 'yes') ? { text: "Selling federal? fedhoo ranks which primes actually pass work to subs and which resellers hold the right vehicles.", href: 'https://fedhoo.com/?utm_source=quotabird&utm_medium=partner&utm_content=verdict', label: 'Find a better route on fedhoo' } : null,
  slug: 'partner', answers: {"Real": "Yes. Real work.", "All talk": "Mostly talk.", "Neighbors": "Not much.", "Just promises": "No. Just promises."}, name: 'Partner Check', url: 'https://quotabird.com/partner/',
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
    ? { overline: 'Is there a deal inside this partnership?', text: 'Run it through Deal Check. A real partner deal survives the same five questions any deal does.', href: '/deal/', label: 'Check your deal' }
    : { overline: 'How much of your number is leaning on them?', text: 'If this partner is in your coverage math, the math is wrong. Pipeline Check shows you by how much.', href: '/pipeline/', label: 'Check your pipeline' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I spent six years leading federal partner sales teams at Amazon, and I sat on the partner side before that. Plenty of partnerships look great in the QBR and never produce anything. Tell me about yours." },
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
    cta='Check your territory',
    questions=[
        dict(k='spend', n='SPEND', q='Is there enough addressable spend in the territory to make the number twice over?'),
        dict(k='accounts', n='ACCOUNTS', q="Can you name ten accounts you'd expect to buy this year?"),
        dict(k='base', n='BASE', q='Is there existing business to grow, not just logos to win?'),
        dict(k='access', n='ACCESS', q='Do you have a way in: relationships, partners, contract vehicles?'),
        dict(k='history', n='HISTORY', q='Has anyone made this number in this territory before?'),
    ],
    bands=[
        ('how', 'What a territory has to have', '''    <p class="lede">Your quota assumes a lot about your territory. Check those assumptions before you sign up for it.</p>
    SPEND: Is the money there twice over? Spend you can actually sell into, by named account. Selling government: agency budgets, program lines, contract ceilings. If the total addressable spend isn't at least double the number, you're counting on share you have no real reason to expect.
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
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('Is this just a way to argue about quota?', 'It\'s a way to argue about quota with evidence. Nobody wins that argument on feelings.'),
        ('What if I\'m new and don\'t know the territory yet?', 'Then most answers will be sort of, and the verdict will say so. Run it again in 60 days and compare.'),
        ('What about the coverage math?', 'That\'s the other tool. Once you know the territory can produce, <a href="/pipeline/">Pipeline Check</a> tells you how much pipeline it has to produce.'),
    ],
    config='''CheckTool({
  aside: (s, a) => ['spend', 'access'].some(k => a[k] && a[k] !== 'yes') ? { text: "Selling federal? fedhoo shows what each agency in your territory actually spends, who's winning it, and what's expiring.", href: 'https://fedhoo.com/?utm_source=quotabird&utm_medium=territory&utm_content=verdict', label: 'Look up your territory on fedhoo' } : null,
  slug: 'territory', answers: {"Workable": "No. It's workable.", "Thin": "A little. It's thin.", "A stretch": "Mostly, yes.", "Nobody could": "Yes. Nobody could hit this."}, name: 'Territory Check', url: 'https://quotabird.com/territory/',
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
    spend: 'Size the territory: the spend you can actually sell into, account by account. One page.',
    accounts: "Write the ten. If you can't get to ten, tell your manager now.",
    base: 'Separate inherited from created. Put the inherited number on paper.',
    access: 'Map one route per account: a relationship, a partner, or a vehicle.',
    history: 'Find the last person who had the territory. Buy them coffee.',
  },
  noMove: 'Build the plan for the ten accounts. The territory isn\\'t the problem.',
  handoff: (s, a) => (s.total >= 55 && a.spend !== 'no')
    ? { overline: 'Now the coverage math', text: (s.total < 75 ? "It's thin, but it might produce." : a.spend === 'yes' ? 'The territory can produce.' : 'The territory can probably produce, if the spend is really there.') + ' Pipeline Check tells you how much it has to.', href: '/pipeline/', label: 'Check your pipeline' }
    : { overline: 'Take it to your manager', text: "Their version of this question is Rep Check, and its first question is the territory. Send them that with your sizing.", href: '/rep/', label: 'Check your rep' },
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
    cta='Test your assessment',
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
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('Does it predict a rating?', 'No, and it never will. It grades whether you can defend the assessment. Your company already has plenty of machinery for the rating.'),
        ('What is OLR?', "OLR is Amazon's annual talent review. Managers bring an assessment of each person and defend it in calibration with other managers. This is practice for the defending part."),
        ('Is this only for Amazon?', 'OLR is Amazon\'s name for it, and that\'s where most of the people who use these tools have sat. But every calibration room asks the same five things, whatever the company calls it. Read "leadership principle" as your organization\'s behavioral standard and the tool works the same.'),
        ('What does Pressure test do?', 'It plays the room. Three hard questions about your weakest answer. If you can\'t answer two of them, the assessment isn\'t ready. Better to find that out here.'),
        ('Why does it never ask the rep\'s name?', 'It doesn\'t need one, and a tool shouldn\'t store opinions about named people. Run it, fix the assessment, and nothing gets written down.'),
    ],
    config='''CheckTool({
  slug: 'olr', answers: {"Ready": "Yes. You're ready.", "Not yet": "Not yet.", "A story": "Not really. It's a story.", "No receipts": "No. No receipts."}, name: 'Talent Review Check', url: 'https://quotabird.com/olr/',
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
    ? { overline: 'The assessment is ready. Is the year set up?', text: "Next year's assessment starts now. Is the rep in a territory that can produce one? Rep Check asks that first.", href: '/rep/', label: 'Check your rep' }
    : { overline: 'The fastest receipt', text: 'A deal you watched them run. Sit in their next customer meeting and go through it with Deal Check afterward.', href: '/deal/', label: 'Check your deal' },
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
    cta='Check your brief',
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
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('What counts as a brief?', 'Anything you\'re about to argue for in front of people who can say no: a narrative doc, a strategy deck, a QBR, an account plan, a proposal, an investment memo, a capture review, or a recommendation you will make out loud. If it has a point and an ask, it\'s a brief.'),
        ('Is this only for sales?', 'No. It started with sales reviews, and the sales leader is one of the sharks. But a six-pager in front of a VP dies exactly the way a QBR does: on the question the author hoped nobody would ask.'),
        ('What does Pressure test do?', 'It plays the room. Pick who\'s across the table, and it asks three of their questions about your weakest answer, one at a time. You say honestly whether you could answer.'),
    ],
    config='''CheckTool({
  slug: 'brief', answers: {"Room ready": "Yes. It's room-ready.", "A fight": "Maybe. It'll be a fight.", "Shark food": "No. Shark food.", "No point": "No. There's no point yet."}, name: 'Brief Check', url: 'https://quotabird.com/brief/',
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
    ? { overline: 'If the brief is about a deal', text: 'Somebody\\'s going to ask whether the deal underneath it is real. Deal Check will tell you before they do.', href: '/deal/', label: 'Check your deal' }
    : { overline: 'If the brief is about the number', text: 'Vague impact usually means the coverage math is missing. Pipeline Check puts a number on it.', href: '/pipeline/', label: 'Check your pipeline' },
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
    cta='Check your account',
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
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('How is this different from Deal Check?', 'Deal Check is about one opportunity: is it real, will it close. Account Check is about the customer it lives in: do you know enough about them to find the next deal, survive a reorg, or beat the incumbent. Good sellers get blindsided that way, with a real deal in an account they didn\'t really know.'),
        ('Is this only for federal?', 'The questions were written with agencies in mind, where mission, colors of money and contract vehicles are everything. But every enterprise account has a mission, a budget process, an incumbent and a way it buys. Read the words that way and it works the same.'),
    ],
    config='''CheckTool({
  aside: (s, a) => ['incumbent', 'money'].some(k => a[k] && a[k] !== 'yes') ? { text: "Selling federal? fedhoo shows the agency's current contracts, who holds them, and what it spends.", href: 'https://fedhoo.com/?utm_source=quotabird&utm_medium=account&utm_content=verdict', label: 'Look up the agency on fedhoo' } : null,
  slug: 'account', answers: {"Mapped": "Yes. You know the account.", "Half mapped": "Partly.", "One thread": "Barely. One thread.", "A contact": "No. You know one person."}, name: 'Account Check', url: 'https://quotabird.com/account/',
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
    ? { overline: 'Now the deal inside it', text: 'You know the account. Is the opportunity in it real? Deal Check asks the five questions your manager will.', href: '/deal/', label: 'Check your deal' }
    : { overline: 'Before you build the account', text: "Can the territory it sits in make the number at all? Territory Check answers that before you spend a year here.", href: '/territory/', label: 'Check your territory' },
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
    cta='Check your risk',
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
    NEXT: Whose calendar is the next step on? If you're the only one who scheduled it, it's a task on your list. You want the customer to have put it on their calendar, and if none of your commit deals have that, worry.
    TIMING: When is it due? If most of the number lands in the last month of the period, you've built a year that only December can save. Federal wrinkle: a September close has nowhere to slip.
    FRESH: Are you still creating? Pipeline you inherited or carried over runs out. If a quarter of what you're carrying wasn't created this quarter, next year is already in trouble.'''),
        ('verdicts', 'Four states of a pipeline', '''    <p><strong>Sturdy.</strong> Spread out, moving, with customers on the calendar. Go get the coverage number too.</p>
    Lopsided. There's one weakness, so fix it before the review finds it.
    <p><strong>Fragile.</strong> A slip or a quiet customer takes you off the number. Re-underwrite the commit deals now.</p>
    Looks covered. Don't trust it. Rebuild it from the customers up.'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('I\'m at 4X coverage. Why does this say fragile?', 'Coverage only tells you how much. Four times the number in two deals that haven\'t moved since spring is a lot less than it looks. Run Pipeline Check for the size and this for the shape.'),
        ('Should a manager run this on the team?', 'Yes, deal by deal is even better. They\'re the questions a good forecast call asks anyway, so you might as well answer them first.'),
    ],
    config='''CheckTool({
  slug: 'risk', answers: {"Sturdy": "No. It's spread out.", "Lopsided": "Almost. It's lopsided.", "Fragile": "Yes. It's fragile.", "Won't hold": "Yes. It won't hold."}, name: 'Risk Check', url: 'https://quotabird.com/risk/',
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
  handoff: (s) => ({ overline: 'Shape checked. Now the size.', text: 'This checked the shape of your pipeline. Pipeline Check looks at whether there\\'s enough of it.', href: '/pipeline/', label: 'Check your pipeline' }),
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
    cta='Check your position',
    questions=[
        dict(k='nothing', n='NOTHING', q='Do you know what it costs them to do nothing, in their numbers?'),
        dict(k='switch', n='SWITCH', q='Do you know what it costs them to leave the incumbent, and who feels it?'),
        dict(k='preference', n='PREFERENCE', q='Has the customer told you, unprompted, why they would prefer you?'),
        dict(k='proof', n='PROOF', q='Do you have proof only you can show them: a reference, a pilot, a result?'),
        dict(k='access', n='ACCESS', q='Do you know who at the customer the competitor already owns?'),
    ],
    bands=[
        ('how', 'Where deals really get lost', '''    <p class="lede">Most lost deals are lost to nothing. The customer kept what they had, the money went somewhere else, the project waited a year. So this checks whether you're beating nothing before it checks anybody else.</p>
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
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('What if there\'s no competitor?', 'There\'s always one: doing nothing. Most deals that are "uncontested" are lost to the status quo, which is why the first question is about the cost of inaction rather than a named rival. Answer it honestly and the tool will tell you whether nothing is winning.'),
        ('Is this a battlecard?', 'No. Battlecards are about the competitor. This is about the customer: what happens if they do nothing, what switching costs, what they\'ve actually said, what you can prove, and who the other side already knows.'),
    ],
    config='''CheckTool({
  aside: (s, a) => ['switch', 'access'].some(k => a[k] && a[k] !== 'yes') ? { text: "Selling federal? fedhoo shows who holds the incumbent contract, what it's worth, and when it ends.", href: 'https://fedhoo.com/?utm_source=quotabird&utm_medium=competition&utm_content=verdict', label: 'Look up the incumbent on fedhoo' } : null,
  slug: 'competition', answers: {"Preferred": "They prefer you.", "In the mix": "You're in the mix.", "Behind": "You're behind.", "Nothing wins": "Doing nothing is winning."}, name: 'Competition Check', url: 'https://quotabird.com/competition/',
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
    ? { overline: 'Now the deal itself', text: 'Where you stand against them is one thing. Whether the deal is real is another, and that\\'s Deal Check.', href: '/deal/', label: 'Check your deal' }
    : { overline: 'Do you know your customer?', text: 'Being behind usually means the other side knows the account better. Account Check finds where.', href: '/account/', label: 'Check your account' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I've lost to incumbents I never saw coming, and to customers who decided to do nothing, more often than I like to admit. Tell me what you're up against." },
  dm: (s) => `Mark, ran a deal through Competition Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. Not sure I'm ahead. Worth 20 minutes?`,
});''',
)

COMPPLAN = dict(
    slug='comp-plan', name='Comp Plan Check',
    title='Comp Plan Check: Can You Trust This Comp Plan?',
    desc='Five questions that find the red flags in a sales comp plan: crediting, payout timing, upside, clawbacks and mid-year changes.',
    ogdesc='Before you count on the plan, check the fine print. Five questions, about a minute.',
    h1='Can you trust this comp plan?',
    dek='Five questions that find the red flags before your first check does.',
    cta='Check your plan',
    questions=[
        dict(k='credit', n='CREDIT', q='Is it written down who gets credit for a deal, including partner, marketplace and split deals?'),
        dict(k='payout', n='PAYOUT', q='Do you know when each commission gets paid, and does it show up within a quarter of the deal?'),
        dict(k='upside', n='UPSIDE', q='Can you earn above your target without a cap or decelerator taking most of it?'),
        dict(k='clawback', n='CLAWBACK', q='Are clawbacks spelled out, with a time limit on them?'),
        dict(k='changes', n='CHANGES', q="Does the plan say mid-year changes aren't retroactive, and that quota moves when territory does?"),
    ],
    bands=[
        ('how', 'What to look for in a comp plan', '''    <p class="lede">Most comp plan problems aren't in the rate. They're in the parts nobody explains until a big deal closes.</p>
    <p><strong>Credit.</strong> Who gets credit when a partner brought the deal, when it went through a cloud marketplace, or when another rep or a specialist worked it too. If the rules aren't written down, you'll find out what they are after the fact.</p>
    <p><strong>Payout.</strong> When a deal you close this month actually shows up in your paycheck. Some plans pay the next month, some pay quarterly, and some hold part of it until the customer pays.</p>
    <p><strong>Upside.</strong> What happens above 100%. An accelerator is only worth something if the plan lets you keep it. A cap or a decelerator can take most of it back.</p>
    <p><strong>Clawbacks.</strong> What can be taken back, why, and for how long. A customer who cancels in the first 90 days is a common trigger. An open-ended clawback is a red flag.</p>
    <p><strong>Changes.</strong> What happens when the plan, the quota or the territory changes mid-year. You want changes to apply going forward, and a territory change to come with a quota change.</p>'''),
        ('verdicts', 'What the answers mean', '''    <p>A clear plan still might not be a generous one. <a href="/pay/">Pay Check</a> shows what it pays at 50% to 200% of quota. This check is about whether you can trust how it pays.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('Is this legal or financial advice?', 'No. It points you to the questions worth asking about your plan. For anything about your rights under a contract or employment law, talk to HR or an employment attorney.'),
        ('What about stock, RSUs and ESPPs?', 'They can matter a lot, and they get complicated fast: vesting schedules, refresh grants, purchase windows, taxes. QuotaBird doesn\'t value them or give financial advice. Read the grant documents, and talk to a financial professional if the equity is a big part of your decision.'),
    ],
    config='''CheckTool({
  slug: 'comp-plan', answers: {"Clear": "Yes. It's clear.", "Mostly clear": "Mostly. Get a few answers in writing.", "Unclear": "Not yet. Too much is unwritten.", "Red flags": "No. Get answers before you count on it."}, name: 'Comp Plan Check', url: 'https://quotabird.com/comp-plan/',
  questions: [
    { k: 'credit',   n: 'CREDIT',   q: 'Is it written down who gets credit for a deal, including partner, marketplace and split deals?' },
    { k: 'payout',   n: 'PAYOUT',   q: 'Do you know when each commission gets paid, and does it show up within a quarter of the deal?' },
    { k: 'upside',   n: 'UPSIDE',   q: 'Can you earn above your target without a cap or decelerator taking most of it?' },
    { k: 'clawback', n: 'CLAWBACK', q: 'Are clawbacks spelled out, with a time limit on them?' },
    { k: 'changes',  n: 'CHANGES',  q: "Does the plan say mid-year changes aren't retroactive, and that quota moves when territory does?" },
  ],
  weights: { credit: 24, upside: 22, changes: 20, payout: 18, clawback: 16 },
  verdict(a, total) {
    if (total >= 75) return { label: 'Clear', cls: 'ready', attack: 'You know how it pays, when it pays, and what can change.', sub: 'Keep the plan and your quota letter somewhere you can find them.' };
    if (total >= 55) return { label: 'Mostly clear', cls: 'proof', attack: "Most of it is written down. A couple of things aren't.", sub: 'Get the missing answers in writing before a big deal closes.' };
    if (total >= 35) return { label: 'Unclear', cls: 'prove', attack: "Too much of how you get paid is in somebody's head.", sub: 'Ask for the written rules now, while nothing is riding on the answer.' };
    return { label: 'Red flags', cls: 'dont', attack: "You can't tell how, when or whether you'll get paid.", sub: 'Get answers in writing before you count on this plan, or before you sign it.' };
  },
  askedBy: 'Ask your manager',
  grill: {
    credit: 'Who gets credit when a partner, the marketplace or another rep is on the deal, and where is that written?',
    payout: 'When does commission on a deal I close this month actually hit my paycheck?',
    upside: 'What happens to my rate above 100%, and is there a cap anywhere in the plan?',
    clawback: 'What can be clawed back, for how long, and why?',
    changes: 'If my territory or quota changes mid-year, what happens to deals I already worked?',
  },
  moves: {
    credit: 'Ask for the crediting rules in writing, with one example deal worked through.',
    payout: 'Get the payout schedule and put the next three paydays on your calendar.',
    upside: 'Run your plan through Pay Check and look at the 125% and 150% rows.',
    clawback: 'Ask what triggers a clawback and how long the window lasts. Write down the answer.',
    changes: 'Ask how mid-year changes are handled before one happens.',
  },
  noMove: 'Keep a copy of the plan, your quota letter and every change notice in one folder.',
  handoff: (s) => s.total >= 55
    ? { overline: 'Now the payout math', text: 'Pay Check shows what the plan pays at 50% to 200% of quota, and where the upside goes.', href: '/pay/', label: 'Check your pay' }
    : { overline: 'Before you count on it', text: 'How to read a comp plan, and what to ask when something is missing.', href: '/notes/read-your-comp-plan/', label: 'Read: How your plan pays' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I've read a lot of comp plans, and the problems are usually in the parts nobody explains. Tell me what's unclear in yours, and leave out the company name and the dollars." },
  dm: (s) => `Mark, ran my comp plan through Comp Plan Check. ${s.label}, weakest is ${s.weak.n.toLowerCase()}. Worth 20 minutes?`,
});''',
)

FEDREADY = dict(
    slug='federal-readiness', name='Federal Readiness Check',
    title='Federal Readiness Check: Is There a Federal Business Here?',
    desc='Five skeptical questions on whether a company has a real federal business: customer, money, buying path, partners and team.',
    ogdesc='You think you have a federal business. Five questions to find out.',
    h1='Is there a federal business here?',
    dek='Five skeptical questions for founders, sales leaders and anyone betting on federal.',
    cta='Check your federal plan',
    questions=[
        dict(k='customer', n='CUSTOMER', q='Is there an actual federal customer asking for this?'),
        dict(k='money', n='MONEY', q='Do you know where the funding would come from?'),
        dict(k='path', n='PATH', q='Do you know how they can legally buy it?'),
        dict(k='partners', n='PARTNERS', q='Do you know whether you need a prime, reseller, marketplace or other partner?'),
        dict(k='team', n='TEAM', q='Do you have somebody who understands how to navigate all of the above?'),
    ],
    bands=[
        ('how', 'What this checks', '''    <p class="lede">A federal customer liking your product isn't the same as a federal business.</p>
    <p>A business needs a customer who has actually asked for the thing, money that can pay for it, a legal way to buy it, the right partner if the customer can't buy from you directly, and somebody on your side who knows how all of that works. Miss one and the deal waits, usually until next fiscal year.</p>
    <p>These five questions are skeptical on purpose. Answer them the way a federal buyer would, not the way the pitch deck does. More on how federal technology actually gets bought, and what a believable first year looks like, is on the <a href="/federal/">Federal GTM</a> page.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. Your answers get scored right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your answers, and nothing leaves the page unless you share a result.'),
        ('Is this legal or contracting advice?', 'No. It points to the questions a federal buyer will ask. For contracts, compliance and authorization questions, talk to people who do that work for a living.'),
    ],
    config='''CheckTool({
  slug: 'federal-readiness', answers: {"Real": "Yes. There's a business here.", "Maybe": "Maybe. Prove the weak part.", "Mostly hope": "Not yet. It's mostly hope.", "Not yet": "No. Not yet."}, name: 'Federal Readiness Check', url: 'https://quotabird.com/federal-readiness/',
  questions: [
    { k: 'customer', n: 'CUSTOMER', q: 'Is there an actual federal customer asking for this?' },
    { k: 'money',    n: 'MONEY',    q: 'Do you know where the funding would come from?' },
    { k: 'path',     n: 'PATH',     q: 'Do you know how they can legally buy it?' },
    { k: 'partners', n: 'PARTNERS', q: 'Do you know whether you need a prime, reseller, marketplace or other partner?' },
    { k: 'team',     n: 'TEAM',     q: 'Do you have somebody who understands how to navigate all of the above?' },
  ],
  weights: { customer: 24, money: 24, path: 20, team: 18, partners: 14 },
  verdict(a, total) {
    if (total >= 75) return { label: 'Real', cls: 'ready', attack: 'A customer, money, a way to buy and people who know the way. That is the start of a federal business.', sub: "Now pressure-test the timing. Federal deals take longer than anyone's plan says." };
    if (total >= 55) return { label: 'Maybe', cls: 'proof', attack: 'Most of it is there. One piece is still a guess.', sub: 'Fix the weakest answer before you hire anybody or tell the board it is a business.' };
    if (total >= 35) return { label: 'Mostly hope', cls: 'prove', attack: "You have interest. You don't have a business yet.", sub: 'Hope is not evidence. Start with the customer and the money.' };
    return { label: 'Not yet', cls: 'dont', attack: 'Nothing here would survive a hard question from a federal buyer.', sub: "That's fine for a first look. It isn't fine for a plan." };
  },
  askedBy: 'Your board will ask',
  grill: {
    customer: 'Who in the government has asked for this, by name and office?',
    money: 'What budget pays for it, and when is that money available?',
    path: 'How can they legally buy it from you today?',
    partners: 'Do you need a prime, a reseller or a marketplace, and which one?',
    team: 'Who on your team has sold this way before?',
  },
  moves: {
    customer: 'Name one federal customer who has asked for this, and write down what they asked for in their words.',
    money: 'Find out which budget the money would come from, and when that money is available.',
    path: "Write down how they would buy it: a contract vehicle they can use, a marketplace, a partner's contract, or something else.",
    partners: 'Decide whether you need a prime, a reseller or a marketplace, and talk to one this month.',
    team: 'Get somebody involved who has sold to the federal government before, even part time.',
  },
  noMove: 'Put dates on the next three steps with the customer. Then run Deal Check on the first real opportunity.',
  handoff: (s) => s.total >= 55
    ? { overline: 'Next: the first real deal', text: 'Deal Check pressure-tests one federal opportunity: customer, money, power, path and now.', href: '/deal/', label: 'Check the deal' }
    : { overline: 'Before you build the plan', text: 'How federal technology actually gets bought, and what a believable first year looks like.', href: '/federal/', label: 'Federal GTM' },
  mark: { title: () => 'Not sure it adds up?', body: "I'm Mark. I spent 20 years on the government side and the last stretch of my career selling into it. Tell me what you're seeing. No company name needed." },
  dm: (s) => `Mark, ran Federal Readiness Check. ${s.label}, weakest is ${s.weak.n.toLowerCase()}. Worth 20 minutes?`,
});''',
)

for t in (REP, PARTNER, TERRITORY, OLR, BRIEF, ACCOUNT, RISK, COMPETITION, COMPPLAN, FEDREADY):
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
      until Q3.<br>The quota is $12M.<br><b>Show me where the rest comes from.</b></div>
    <p>Then stop talking. Either somebody fills the gap with something real (new territory, a renewal you didn't know
      about, a partner with names attached), or the number moves, or at least everybody knows where it came from. Any of
      those beats signing up quietly and explaining the miss in October.</p>
    <h3>What doesn't work</h3>
    <p>Complaining about it in the team meeting. Telling your boss the reps are upset. Saying "we'll find a way," which I
      used to say, and then spent the year explaining. And don't let anybody close the gap on paper by assuming AI will
      make the reps more productive. It can write the follow-up email. It can't make the customer care.</p>
    <p>If only 20% of a reasonably tenured team hits quota year after year, stop assuming every miss is its own rep problem.</p>''',
         tool=('/quota/', 'Quota Check', 'does the multiple and the implied rate in about ten seconds. Pipeline Check and Territory Check cover the rest of the math.')),
    dict(slug='review-an-offer', title='How to review an offer, and push back on it',
         dek="The offer letter tells you what they'll pay if everything goes right. Find out what you'll make in a normal year.",
         body='''    <p class="lede">An offer letter shows you the OTE. That's what you make if you hit 100%, and about half of AEs don't. Before you sign, figure out what the job pays in a normal year.</p>
    <h3>Get the whole plan, not the summary</h3>
    <ul>
      <li>Base, variable and OTE, and how the variable pays: monthly, quarterly, or when the customer pays</li>
      <li>The quota, and what it's measured on: bookings, run rate, or the whole book</li>
      <li>The comp plan document itself, including accelerators, caps and crediting rules</li>
      <li>The ramp: how long, what the ramped quota is, and whether there's a guarantee or a draw while you ramp</li>
      <li>The territory: what's in it, and who had it before you</li>
    </ul>
    <p>If they won't show you the plan until after you sign, that tells you something.</p>
    <h3>Do the math for a normal year</h3>
    <p>Run the quota and OTE through <a href="/quota/">Quota Check</a> to see whether the multiple is in the normal range for how it's measured. Then put the plan through <a href="/pay/">Pay Check</a> and look at the 75% and 100% rows. That's closer to what you'll make than the number in the offer.</p>
    <p>For year one, count the ramp. If you start in April with a six-month ramp, you'll sell for about three months at full quota before the year ends. A guarantee or a draw changes that math a lot, so ask exactly how yours works.</p>
    <h3>Ask the questions nobody likes</h3>
    <ul>
      <li>What share of the team hit quota last year?</li>
      <li>Why is this role open, and what happened to the last person in the territory?</li>
      <li>How often has the plan changed mid-year?</li>
      <li>Has anyone on the team hit the cap, if there is one?</li>
    </ul>
    <p>A good hiring manager will answer these without flinching. If they dodge all of them, you learned something.</p>
    <h3>Stock, RSUs and ESPPs</h3>
    <p>Plenty of cloud and SaaS offers include stock: RSU grants, options, or an employee stock purchase plan. They can be worth a lot, and they get complicated fast: vesting schedules, cliffs, refresh grants, purchase windows, taxes. I don't value them here, and I'm not giving financial advice. Get the grant details in writing, and if the equity is a big part of the decision, talk to a financial professional.</p>
    <h3>How to push back</h3>
    <p>Pick the one or two things that matter most to you and ask for those. Base often moves more easily than quota. A ramp guarantee, a lower first-year number, or a start date that lines up with the plan year are all reasonable asks. So is asking them to put a verbal promise into the offer letter.</p>
    <p>Ask plainly, give your reason, and be ready to hear no. Don't bluff about a competing offer you don't have, and don't negotiate against yourself by offering a lower number before they answer.</p>''',
         tool=('/pay/', 'Pay Check', 'shows what an offer pays at 50% to 200% of quota, before you sign.')),
 dict(slug='think-youre-being-shorted', title="You think the company is shorting you",
         dek='Start with the math, then the paperwork, then the right person. In that order.',
         body='''    <p class="lede">Sooner or later a commission check comes in lighter than you expected. Most of the time it's a mistake, or a rule in the plan you didn't know about. Sometimes it isn't. Either way, start with the math, not the accusation.</p>
    <h3>Check your own math first</h3>
    <ul>
      <li>The deal amount that was actually credited, which isn't always the contract value</li>
      <li>Your share of the credit, if another rep, a partner or a specialist was on it</li>
      <li>Your rate at the attainment level you were at when it closed</li>
      <li>When it should pay under the payout schedule, and whether part of it is held until the customer pays</li>
      <li>Any clawback, hold or adjustment from an earlier deal</li>
    </ul>
    <p><a href="/commission/">Commission Check</a> does the arithmetic. If your number and theirs still don't match, you've got a real question.</p>
    <h3>Write it down</h3>
    <p>Keep the plan document, your quota letter, any change notices, and the emails about how the deal was credited. Write down the deal, what you expected, what you got, and why you think they're different, with dates.</p>
    <h3>Ask the right person, in writing</h3>
    <p>Start with your manager or sales ops, not the team channel. Ask a plain question: "I expected $X on this deal under section Y of the plan. I got $Z. Can you walk me through the difference?" Most errors get fixed right there, and a calm question gets a faster answer than an angry one.</p>
    <h3>If it doesn't get fixed</h3>
    <p>Most plans have a dispute process, and it often has a deadline, so find it and use it. If it's still not resolved and the amount matters, HR is the next stop. For questions about your rights under the plan or under employment law, talk to an employment attorney. I'm not a lawyer, and this isn't legal advice.</p>
    <h3>What not to do</h3>
    <p>Don't hold deals to push them into the next period, don't take it to customers or social media, and don't assume bad intent before you've asked. Comp teams make mistakes. So do reps.</p>''',
         tool=('/commission/', 'Commission Check', 'works out what a deal should pay you, including split credit.')),
 dict(slug='explain-a-bad-comp-plan', title='How to explain a bad comp plan without losing the room',
         dek="You'll roll out a plan you wouldn't have written. Your team will find the ugly parts fast, so get there first.",
         body='''    <p class="lede">Sooner or later you'll roll out a comp plan you wouldn't have written. The team will read it faster than you did, and they'll find the ugly parts first. Get there before they do.</p>
    <h3>Read it like a rep</h3>
    <p>Before the rollout, run the plan through <a href="/pay/">Pay Check</a> at 75%, 100% and 150% of quota for a typical rep on your team. Know what changed from last year in dollars: the rate, the accelerator, the cap, crediting and clawbacks.</p>
    <h3>Say what's good and what isn't</h3>
    <p>Start with whatever is actually better, if anything is. Then say plainly what got worse. Reps can handle a worse plan. What they can't handle is finding out on their own that you knew and didn't say.</p>
    <h3>Say what you pushed on</h3>
    <p>Tell them what you pushed back on, what you got, and what you didn't. Keep it short. You can be honest about it without criticizing your boss.</p>
    <h3>Help them plan around it</h3>
    <p>Show each rep what the plan pays for, and point their effort there. If the plan pays more for new logos than for expansion, their territory plan should say so. If there's a cap, tell them where it is before anybody gets near it.</p>
    <h3>Then stop</h3>
    <p>Take questions, answer what you can, find out what you can't, and follow up in writing. After that, stop reopening it in team meetings. Complaining about the plan every week doesn't change it, and it tells the team you've given up on it.</p>''',
         tool=('/pay/', 'Pay Check', 'shows what the plan pays a typical rep at 75%, 100% and 150% of quota.')),
 dict(slug='fight-a-comp-plan-before-it-ships', title='How to fight a comp plan before it ships',
         dek="Once the plan ships, you're mostly explaining it. The time to change it is while it's still a draft.",
         body='''    <p class="lede">The time to change a comp plan is before it's final. Once it ships, you're mostly explaining it. Plans get built months before the year starts, so find out when yours gets drafted and who's drafting it.</p>
    <h3>Bring what the plan designers don't have</h3>
    <ul>
      <li>Last year's attainment for your team: how many reps finished near 50%, 75%, 100% and 150%</li>
      <li>What reps actually earned against their OTE</li>
      <li>Territory changes, open territories and ramp for the coming year</li>
      <li>Deals that got credited in odd ways, and what that did to someone's pay</li>
    </ul>
    <h3>Test the plan against what leadership says it wants</h3>
    <p>Every plan pays for some behavior. If leadership wants new logos and the plan pays the same for expansion, reps will do expansion. If they want multi-year deals and nothing in the plan rewards them, they won't get many. Run the draft through <a href="/pay/">Pay Check</a> with your team's real attainment, and show where the money actually goes.</p>
    <h3>Ask for specific changes</h3>
    <p>One or two, with the numbers behind them. An accelerator that starts where reps actually get to. A cap high enough that it never touches a normal good year. Crediting rules written down before the first split deal. "The plan feels unfair" won't move anything.</p>
    <h3>Know when to stop</h3>
    <p>If you've made the case and the plan ships anyway, your job changes to explaining it well. <a href="/notes/explain-a-bad-comp-plan/">How to explain a bad comp plan</a> picks up from there.</p>''',
         tool=('/pay/', 'Pay Check', 'shows where a draft plan pays and where the upside goes, using your team\'s real attainment.')),
 dict(slug='ote-if-everything-goes-right', title='OTE is what you make if everything goes right',
         dek="It's a real number. It's the number for a year that goes to plan, and most years don't.",
         body='''    <p class="lede">On-target earnings is what you make if you hit exactly 100% of quota. It's a real number, but it's the number for a year that goes to plan.</p>
    <p>Bridge Group's 2026 study found 48% of AEs hit quota. So for about half of sellers, OTE is more than they'll make that year.</p>
    <h3>Budget on the lower rows</h3>
    <p>When you plan your spending, use what the plan pays at 75% to 100% of quota. <a href="/pay/">Pay Check</a> shows those rows. Anything above that is a good year, and you'll know when you're having one.</p>
    <h3>When you compare jobs</h3>
    <p>Compare what each offer pays at the same realistic attainment, not the two OTEs. A higher OTE on a quota nobody hits can pay less than a lower one you'll actually make. <a href="/offer/">Offer Check</a> puts them side by side.</p>''',
         tool=('/offer/', 'Offer Check', 'compares two offers at a realistic attainment, not at OTE.')),
 dict(slug='accelerators-need-someone-to-reach-them', title='Your accelerator only matters if somebody reaches it',
         dek='A 2× accelerator sounds great in the offer. It pays nothing in a year you finish at 90%.',
         body='''    <p class="lede">A 2× accelerator sounds great in the offer. It pays nothing in a year you finish at 90%.</p>
    <p>An accelerator raises your rate once you pass a point, usually 100% of quota. What it's worth depends on how often people actually get past that point. Bridge Group found 48% of AEs hit quota in 2026, so in a given year a little under half of reps see any accelerator at all.</p>
    <h3>What to ask</h3>
    <ul>
      <li>How many people on the team got into the accelerator last year?</li>
      <li>Where does it start, and does it apply to everything past that point?</li>
      <li>Is there a cap, or anything else that limits it?</li>
    </ul>
    <h3>How to use it</h3>
    <p>Plan your year on the base rate. The accelerator is the reason to push hard on one more deal in Q4, and it's a nice surprise when it pays. Don't spend it before it shows up.</p>''',
         tool=('/pay/', 'Pay Check', 'shows what the accelerator adds at 125%, 150% and 200% of quota.')),
 dict(slug='what-a-cap-tells-you', title="A cap tells you how much upside they're willing to share",
         dek='Past the cap, your check stops growing. Where they put it tells you a lot.',
         body='''    <p class="lede">If variable is capped at 200% of target, then past 200% your check stops growing. Your base still pays and the company still books the revenue. You just don't get paid more for it.</p>
    <h3>Why companies cap</h3>
    <p>Mostly to protect against windfalls: a giant deal that landed in one rep's territory by luck, or a pricing mistake. That's a fair worry. A cap at 150% is a different thing. It limits an ordinary good year, not a windfall.</p>
    <h3>What to ask</h3>
    <ul>
      <li>Where exactly is the cap, and is it on total variable or per deal?</li>
      <li>Has it ever been lifted for a big year?</li>
      <li>Is there a separate review for windfall deals instead?</li>
    </ul>
    <p>A plan with a windfall review and no cap is usually better for the rep than a plan with a low cap. <a href="/pay/">Pay Check</a> shows exactly what a cap does to your 150% and 200% rows.</p>''',
         tool=('/pay/', 'Pay Check', 'shows what a cap does to your pay at 150% and 200% of quota.')),
 dict(slug='split-credit', title='How a $1M deal turns into a small paycheck',
         dek='You close a $1M deal. Then the credit rules run.',
         body='''    <p class="lede">You close a $1M deal. Then the credit rules run.</p>
    <p>Here's one way it goes. A specialist worked the deal with you, so your share of the credit is 50%: $500K. It went through a channel your plan credits at half, so you're at $250K. At an 8% rate, that's $20K of commission, and after setting aside 30% for taxes, about $14K. The customer paid $1M.</p>
    <p>Every plan's rules are different, and this is just an example. The point is that the contract value and your credit are often two very different numbers.</p>
    <h3>Why it happens</h3>
    <p>Splits exist for real reasons. Specialists, partners and account managers help close deals, and plans pay them for it. The trouble is finding out how your split works after the deal closes.</p>
    <h3>What to do</h3>
    <p>Get the crediting rules in writing before a big deal closes, with one example worked through. When several people are on a deal, agree on the split early, in writing, before anybody knows how big it'll get. <a href="/commission/">Commission Check</a> shows what your share pays.</p>''',
         tool=('/commission/', 'Commission Check', 'works out what your share of the credit actually pays.')),
 dict(slug='uncapped-read-the-footnotes', title='The plan says uncapped. Read the footnotes.',
         dek="A plan can be uncapped on page one and still limit a big year. Find out before you're counting on one.",
         body='''    <p class="lede">Plenty of plans say uncapped on page one. Read the rest of the document before you count on it.</p>
    <p>A plan can be uncapped and still limit your upside. Look for:</p>
    <ul>
      <li>A decelerator, where your rate drops past a certain point</li>
      <li>A windfall clause, where deals over a certain size get reviewed or paid differently</li>
      <li>A cap on any single deal, even with no cap on the year</li>
      <li>Management discretion to adjust payouts</li>
      <li>Crediting rules that shrink a big deal before the rate applies</li>
    </ul>
    <p>None of these are unusual, and some are reasonable. The point is to know they're there before you plan on a big year.</p>
    <h3>What to ask</h3>
    <p>"Is there anything in the plan, or in a separate policy, that can reduce the payout on a large deal? Has it been used in the last two years?" Get the answer in writing. <a href="/comp-plan/">Comp Plan Check</a> covers the rest of what to look for.</p>''',
         tool=('/comp-plan/', 'Comp Plan Check', 'finds the red flags in a comp plan: crediting, payout timing, upside, clawbacks and mid-year changes.')),
 dict(slug='weighted-pipeline', title='Weighted pipeline is only as good as the weights',
         dek="Your CRM's stage probabilities are numbers somebody typed in once. Check them against what you actually win.",
         body='''    <p class="lede">Weighted pipeline takes every open deal, multiplies it by its stage probability, and adds them up. It's supposed to tell you what you'll actually close. It's only as good as the probabilities.</p>
    <h3>Where the weights come from</h3>
    <p>In most CRMs, somebody set the stage probabilities once, usually when the system was set up: maybe 50% at Proposal and 80% at Negotiation. Then nobody checked them against what actually closed. They're defaults, not data.</p>
    <h3>What that looks like</h3>
    <p>Take a pipeline with four qualified deals worth $3.08M. The CRM's weights add up to $2.19M, which works out to a 71% average. The same team's closed deals won 39% by value. At that rate, the realistic expectation is about $1.2M.</p>
    <p>The weighted number is almost double what the team's own history supports, and it makes a short pipeline look nearly fine.</p>
    <h3>How to use each one</h3>
    <ul>
      <li><strong>Unweighted pipeline goes with your real win rate.</strong> Coverage needed is one divided by the win rate: a 25% win rate needs 4X.</li>
      <li><strong>Weighted pipeline is already discounted.</strong> Compare it straight to what's left of the target, and 1.0X is enough.</li>
      <li><strong>Never hold weighted pipeline to 3X, and never multiply it by your win rate.</strong> Both count the discount twice.</li>
    </ul>
    <h3>Check your weights</h3>
    <p>Divide your weighted pipeline by your unweighted pipeline. That's the win rate your CRM assumes. Put it next to the one you actually get. If the CRM's number is ten points higher, your forecast is leaning on optimism somebody typed in years ago.</p>''',
         tool=('/pipeline/', 'Pipeline Check', 'compares your CRM\'s weighted pipeline with what your real win rate says.')),
 dict(slug='push-back-as-a-rep', title="You're the rep and the number is crazy",
         dek="You don't set the number. You can still make a case, if you bring the right one.",
         body='''    <p class="lede">A rep has less leverage on quota than a manager does. That's just true. But the reps who bring a
      clean case to their manager get more than the ones who complain in the team channel.</p>
    <h3>What can actually change</h3>
    <ul>
      <li>The territory: accounts that moved in or out after the number was set</li>
      <li>Ramp: if you're new, a ramp schedule is normal, so ask what yours is</li>
      <li>One-time deals: a giant deal from last year baked into this year's number</li>
      <li>Crediting: deals you work that don't count toward your number</li>
      <li>The start date, if you inherited the territory mid-year</li>
    </ul>
    <p>The total usually won't move much. These often do.</p>
    <h3>How to raise it</h3>
    <p>Ask your manager for fifteen minutes, not a meeting about fairness. Bring your number next to last year's actuals
      for the territory, your pipeline at your real win rate, and the one change you're asking for.</p>
    <p>Then ask: "What has to be true for me to hit this?" If your manager can answer it, you have a plan. If they
      can't, they now have something to take upstairs, in their words instead of yours.</p>
    <h3>What not to do</h3>
    <p>Don't threaten to leave unless you mean it. Don't compare your number to a teammate's in public. And don't
      sandbag the first quarter to prove a point. It proves the other point.</p>''',
         tool=('/quota-case/', 'Quota Case', 'shows the gap between last year and this year\'s number for your territory.')),
    dict(slug='handing-down-a-tough-quota', title="You have to hand down a number you don't love",
         dek="You made your case upstairs. It didn't move. Now your team needs to hear it from you.",
         body='''    <p class="lede">Sooner or later every manager carries a number down the hall that they argued against. How you
      hand it over decides whether the team spends the first quarter selling or complaining.</p>
    <h3>Own it</h3>
    <p>Don't say "corporate gave us this." Your team hears "my manager doesn't believe in it either," and they'll act
      like it. You can say you pushed back. Then say what you got, even if it's small, and that the number is the
      number.</p>
    <h3>Show the math</h3>
    <p>Most reps have never seen how their quota was built. Show them: last year, the team's run rate, and what the plan
      assumes about new logos, renewals and headcount. People take a hard number better when they can see where it came
      from.</p>
    <h3>Give each rep a path</h3>
    <p>In the first one-on-one, walk the number down for their territory: what's already coming in, what existing
      accounts can grow into, and how much new pipeline they need, by when. A rep who can see a path will work it. A rep
      who can't will update their LinkedIn.</p>
    <h3>Then stop relitigating it</h3>
    <p>Once it's handed down, stop complaining about it in team meetings. If something real changes, a territory or a
      big renewal, take it upstairs again with the math.</p>''',
         tool=('/pipeline/', 'Pipeline Check', "works backward from each rep's number to the pipeline and deals it takes.")),
    dict(slug='the-number-isnt-changing', title="The number isn't changing. Now what?",
         dek="You made the case. It didn't move. Fine. Now figure out what it takes.",
         body='''    <p class="lede">You showed them the gap, you asked what assumption you were missing, and the answer was some
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
      are to the number, even if the line is steep. If you can, it's a plan. If you can't, take the gap back upstairs.</p>''',
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
    dict(slug='3x-is-a-win-rate', title='3X is really a win rate',
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
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0B1215">
<link rel="stylesheet" href="/site.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BG9NR9GXQZ"></script>
<script src="/analytics.js" defer></script>
'''
NOTE_TAIL = '''<footer class="sitefoot">
  <a href="/">QuotaBird</a> is a pile of free sales tools. I built them because they helped me, and maybe they'll help you.
  <p>Questions or security issues: <a href="mailto:mark@quotabird.com">mark@quotabird.com</a></p>
  <p>Not affiliated with the U.S. government or Amazon.</p>
</footer>
<script>
document.addEventListener('click', (e) => { document.querySelectorAll('details.menu[open]').forEach(d => { if (!d.contains(e.target)) d.open = false; }); });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') document.querySelectorAll('details.menu[open]').forEach(d => { d.open = false; d.querySelector('summary').focus(); }); });
</script>
</body>
</html>
'''
HOME_NOTES = ['prove-the-quota-is-crazy', 'push-back-as-a-rep', 'handing-down-a-tough-quota', '3x-is-a-win-rate', 'read-your-comp-plan', 'review-an-offer']   # the six on the home page
def home_notes():
    picks = [n for s in HOME_NOTES for n in NOTES if n['slug'] == s]
    return '<div class="doors">' + ''.join(
        f'<a class="door" href="/notes/{n["slug"]}/"><span><b>{n["title"]}</b><span class="q">{n["dek"]}</span></span><span class="to">Read</span></a>'
        for n in picks) + '</div>'
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
    dict(tag='Attainment', num='48%', fact='of AEs hit quota in 2026.', line='It was 66% in 2022.', src='Bridge Group, 2026', href='/quota/', go='Check your quota', k='#E77A3C', ink='#282C2F'),
    dict(tag='The median', num='$960K', fact='is the median AE quota.', line='On a $200K OTE, across 158 B2B companies.', src='Bridge Group, 2026', href='/quota/', go='Check your quota', k='#D9B265', ink='#282C2F'),
    dict(tag='The multiple', num='4.6×', fact='is the median quota to OTE.', line='It was 4.2 two years ago.', src='Bridge Group, 2026', href='/quota/', go='Check your quota', k='#0A504B', ink='#FFFFFF'),
    dict(tag='Planning', num='20-30%', fact='is a common over-assignment rule of thumb.', line='Plans hand out more quota than the company needs.', src='Mostly Metrics', href='/how-quotas-get-built/', go='How quotas get built', k='#BEAAA3', ink='#282C2F'),
    dict(tag='Your boss', fact='Your boss may be paid on something else.', line='Growth rate, new logos, a strategic product.', src='', href='/how-quotas-get-built/', go='How quotas get built', k='#282C2F', ink='#FFFFFF'),
    dict(tag='Ramp', num='6.2 mo', fact='for a new AE to ramp.', line='A rep hired in March is a fall rep.', src='Bridge Group, 2026', href='/quota-case/', go='Find the gap', k='#1B9ED8', ink='#282C2F'),
    dict(tag='Vacancies', fact='A vacant territory still has quota.', line="Somebody's carrying it.", src='', href='/quota-case/', go='Find the gap', k='#FFFFFF', ink='#282C2F'),
    dict(tag='Coverage', num='3X', fact='is a 33% win rate wearing a nicer shirt.', line='Win 20% and you need 5X.', src='The math', href='/pipeline/', go='Check your pipeline', k='#E77A3C', ink='#282C2F'),
    dict(tag='Cloud', fact="On a consumption plan, a commit nobody uses doesn't retire much quota.", line='The customer has to run the stuff.', src='Microsoft Partner Center', href='/quota/', go='Check your quota', k='#D9B265', ink='#282C2F'),
    dict(tag='Comp', num='1.5-2×', fact='is a common accelerator range above quota.', line='Where they start matters more than the rate.', src='Comp plan surveys, 2026', href='/notes/read-your-comp-plan/', go='Read your comp plan', k='#0A504B', ink='#FFFFFF'),
    dict(tag='Federal', num='46%', fact='of federal AEs say they hit quota.', line='SLED is 45%. Self-reported.', src='RepVue, Sept. 2026', href='/territory/', go='Check your territory', k='#BEAAA3', ink='#282C2F'),
]
def _short(s, i):
    src = f'<span class="short-src">{esc_html(s["src"])}</span>' if s['src'] else ''
    num = f'<span class="short-num">{esc_html(s["num"])}</span>' if s.get('num') else ''
    return (f'<a class="short{" has-num" if s.get("num") else ""}" href="{s["href"]}" data-short="{i+1}">'
            f'<span class="short-tag">{esc_html(s["tag"])}</span>{num}<span class="short-fact">{esc_html(s["fact"])}</span>'
            f'<span class="short-line">{esc_html(s["line"])}</span><span class="short-foot">{src}<span class="short-go">{esc_html(s["go"])} →</span></span></a>')
def shorts_strip():
    return ('<section class="shorts-band" aria-labelledby="shorts-h"><div class="shorts-head"><h2 id="shorts-h">Quota Shorts</h2>'
            '<a class="shorts-all" href="/shorts/">All of them</a></div>'
            '<div class="shorts-row" role="list">' + ''.join(f'<div role="listitem">{_short(s, i)}</div>' for i, s in enumerate(SHORTS)) + '</div></section>')

# ────────────────────────────── HOME ──────────────────────────────
# The home page source lives in home.src.html; this fills in the note list and build stamp.
home = open('home.src.html').read().replace('__NOTES__', home_notes()).replace('__NOTECOUNT__', str(len(NOTES))).replace('__BUILD__', BUILD).replace('<!--shorts-->', shorts_strip())
open('index.html', 'w').write(home)
# Pipeline Check lives at /pipeline/ again (it was the home page until the shelf took over)
os.makedirs('pipeline', exist_ok=True)
open('pipeline/index.html', 'w').write(open('pipeline.src.html').read().replace('__BUILD__', BUILD))

# ────────────────────────────── CALCULATORS (Quota, Discount, Commission) ──────────────────────────────
# Rebuilt from the old Fedmo tools: Is My Quota Crazy?, They Want a Discount, Commissions Take-Home.
CALCS = [
 dict(slug='quota-case', name='Quota Case',
  title='Quota Case: Is Your Quota Actually Possible?',
  desc='Find the gap between last year and this year\'s quota: run rate or ARR, pipeline at your real win rate, headcount, one-time deals. Then push back with it, or close it with growth in existing accounts and net-new ones.',
  ogdesc='Build the case before you push back. Last year, run rate, pipeline and win rate in; the gap, and the pipeline it takes to close it, out.',
  h1='Is your quota actually possible?', dek='Use last year, your run rate, your pipeline and your win rate to find the gap. Build the case before you push back.',
  fields=[dict(id='basis',kind='choice',label='What the quota is measured on',example='cloud',options=[('saas','Bookings'),('cloud','Run rate'),('book','Whole book')]),
          dict(id='lastyear',kind='money',label='Last year, on the same measure',example='$8,200,000'),
          dict(id='oneoff',more=True,kind='money',label='One-time deals in that number',example='',placeholder='$0 (optional)'),
          dict(id='runrate',kind='money',label='Current run rate (MRR × 12)',example='$8,700,000'),
          dict(id='pipeline',kind='money',label='New qualified pipeline this year',example='$6,000,000'),
          dict(id='win',kind='pct',label='Your historical win rate',example='25%'),
          dict(id='repsthen',more=True,kind='count',label='Reps last year',example='',placeholder='optional'),
          dict(id='repsnow',more=True,kind='count',label='Fully ramped reps now',example='',placeholder='optional'),
          dict(id='quota',kind='money',label='The new number',example='$12,000,000')],
  card=dict(headline=['Build the case', 'against a crazy quota.'],dek='Last year. Run rate. Pipeline. Win rate.',pillars=['LAST YEAR','RUN RATE','PIPELINE','THE GAP']),
  bands=[('how','How the gap works','''    <p class="lede">Start with what the quota is measured on, because the math changes. On a run-rate or whole-book number, the evidence is your current run rate, which already reflects today's team, plus the new pipeline you expect to win this year. On a bookings number, run rate doesn't tell you much, so it compares last year's bookings, adjusted for today's ramped headcount, with this year's pipeline at your real win rate, and takes the stronger of the two. Whatever's left between the evidence and the new number is the gap somebody needs to explain.</p>
    <p>Take one-time deals out of last year. If a single giant deal made last year's number, building this year's quota on it is how a team ends up at 60% attainment and a lot of meetings about effort.</p>
    <p>If you lost reps or have open territories, put in the headcount. On a bookings number it changes the capacity math. On a run-rate number, your run rate already reflects today's team, so headcount shows up as context and is never counted twice. A vacant territory still has quota. That's the problem. And a rep hired in March doesn't sell much until summer, so count reps when they're ramped, not when they start.</p>'''),
         ('conversation','Taking it to your boss','''    <p class="lede">Don't walk in upset. Walk in with the gap and one question: what assumption am I missing?</p>
    <p>Sometimes there's a real answer: new territory, a big renewal you didn't know about, a product launch, partner help with names attached. Then the number's hard but fair, and your job changes to helping the team hit it (<a href="/notes/handing-down-a-tough-quota/">here's how to hand it down</a>), which means you stop relitigating it every Monday. Sometimes nobody has an answer. Then at least everybody knows where the number came from, and it's in writing before the year starts.</p>
    <p><a href="/notes/prove-the-quota-is-crazy/">Your quota is crazy. Now prove it.</a> has the longer version, including why the best time to have this fight is the year before.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The math runs right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your numbers, and nothing leaves the page unless you share a result.'),
       ('Is this the company\'s formula?','No. Nobody outside finance has that, and some years nobody inside does either. This is the evidence you have: history, capacity and pipeline. It\'s the part of the conversation you control.'),
       ('What if I don\'t know my win rate?','Count it: of last year\'s qualified deals, how much closed, by value. Or leave pipeline and win rate blank and it\'ll use your run rate alone.'),
       ('Rep or manager?','Either. A manager uses it to take the team\'s number upstairs. A rep can run it on their own territory before the one-on-one where the number gets explained.')],
  config="""CalcTool({
  slug: 'quota-case', answers: {"Supported": "Yes. It already adds up.", "Tight": "You're a little short.", "You've got a gap": "You've got a gap.", "Can't see it": "You've got a big gap."}, name: 'Quota Case', url: 'https://quotabird.com/quota-case/',
  fields: [{ id: 'basis', kind: 'choice' }, { id: 'lastyear', kind: 'money' }, { id: 'oneoff', kind: 'money' }, { id: 'runrate', kind: 'money' }, { id: 'pipeline', kind: 'money' }, { id: 'win', kind: 'pct' }, { id: 'repsthen', kind: 'count' }, { id: 'repsnow', kind: 'count' }, { id: 'quota', kind: 'money' }],
  compute(v) {
    if (!(v.quota > 0 && v.lastyear > 0)) return { msg: v.lastyear > 0 ? 'Add the new quota.' : v.quota > 0 ? "Add last year's number, on the same measure as the quota." : "Add last year's number and the new quota, on the same measure." };
    const money = (n) => { const a = Math.abs(n); return (n < 0 ? '-' : '') + (a >= 1e6 ? '$' + (a / 1e6).toFixed(1).replace(/\\.0$/, '') + 'M' : a >= 1e3 ? '$' + Math.round(a / 1e3) + 'K' : '$' + Math.round(a)); };
    const pct = (r) => Math.round(r * 100) + '%';
    const bookings = v.basis === 'saas';
    const last = v.lastyear - (v.oneoff || 0);
    const cap = (v.repsthen > 0 && v.repsnow > 0) ? v.repsnow / v.repsthen : 1;
    const pipe = (v.pipeline > 0 && v.win > 0) ? v.pipeline * v.win : 0;
    // Bookings: the stronger of last year's bookings at today's headcount and this year's pipeline at your win rate.
    // Run rate or whole book: today's run rate (it already reflects today's team) plus the new pipeline you expect to win.
    // Headcount never adjusts a run rate the user entered; that would count it twice.
    const hist = last * cap;
    const run = !bookings && v.runrate > 0 ? v.runrate : 0;
    const base = bookings ? 0 : (run || hist);
    const best = bookings ? Math.max(hist, pipe) : base + pipe, gap = v.quota - best, share = gap / v.quota, growth = (v.quota - last) / last;
    let t;
    if (gap <= 0) t = ['Supported', 'ready', `The evidence supports ${money(v.quota)}. Hard, maybe, but defensible.`, 'Stop arguing about it with the team and build the plan.'];
    else if (share <= .10) t = ['Tight', 'proof', `${money(gap)} short of what the evidence supports. That's a stretch, not a scandal.`, `Find the ${money(gap)} with names attached, then build the plan.`];
    else if (share <= .25) t = ["You've got a gap", 'prove', `${money(gap)} of your number that nobody has explained yet.`, 'Push back with the gap below, or close it with growth in existing accounts and net-new ones.'];
    else t = ["Can't see it", 'dont', `${money(gap)}, ${pct(share)} of the number, with nothing in the evidence to fill it.`, 'Take the gap to your boss before you sign anything.'];
    const rows = [['Last year', money(v.lastyear)]];
    if (v.oneoff > 0) rows.push(['Without one-time deals', money(last)]);
    if (bookings) { if (cap !== 1) rows.push(["Last year at today's headcount", money(hist)]); }
    else rows.push([run ? 'Run rate (MRR × 12)' : (cap !== 1 ? "Last year at today's headcount" : 'Last year, as your baseline'), money(base)]);
    if (pipe) rows.push([bookings ? `Pipeline at your ${pct(v.win)} win rate` : `Plus new pipeline at your ${pct(v.win)} win rate`, money(pipe)]);
    if (!bookings && run && cap !== 1) rows.push(['Ramped reps, now vs last year', `${v.repsnow} vs ${v.repsthen}`]);
    rows.push(['What the evidence supports', money(best)]);
    rows.push(['The new number', money(v.quota)]);
    rows.push([v.oneoff > 0 ? 'Growth over last year, without one-offs' : 'Growth over last year', (growth >= 0 ? '+' : '') + pct(growth), growth > .25 ? 'v-no' : '']);
    rows.push(['Gap nobody has explained', gap > 0 ? money(gap) : 'None', gap > 0 ? 'v-no' : '']);
    const need = (gap > 0 && v.win > 0) ? gap / v.win : 0;
    if (need) rows.push([`New pipeline to close it, at ${pct(v.win)}`, money(need)]);
    const said = bookings ? "here's what the pipeline supports at our win rate" : "here's what we're running at";
    const note = gap > 0 ? `To push back: \"Here's last year, ${said}, and here's a ${money(gap)} gap I can't explain. What assumption am I missing?\"` + (need ? ` To close it: about ${money(need)} of new pipeline at your win rate, from growth in existing accounts and net-new ones.` : '') : "The number holds up against the evidence. Now it's about the plan.";
    return { label: t[0], cls: t[1], attack: t[2], sub: t[3], bar: t[1] === 'prove' ? 'gap' : undefined, big: gap > 0 ? money(gap) : 'Covered', rows, note, gap, quota: v.quota, best, growth, gapm: money(gap), quotam: money(v.quota), bestm: money(best) };
  },
  handoff: (s) => s.gap > 0
    ? { overline: 'Before you take it upstairs', text: 'How to walk in with this, and what to do when they push back.', href: '/notes/prove-the-quota-is-crazy/', label: 'Read the playbook' }
    : { overline: 'Okay. How do we hit it?', text: `Pipeline Check works backward from ${s.quotam} to the pipeline and deals it takes.`, href: `/pipeline/#t=${Math.round(s.quota)}&y=cy`, label: 'Check your pipeline' },
  mark: { title: () => 'Want a second look at the gap?', body: "I'm Mark. I've taken a gap like this to my boss and had the number move, and I've had it not move. Either way it was a better conversation than 'this feels high.' Send me the numbers, no company name." },
  dm: (s) => `Mark, ran our quota through Quota Case. The new number is ${s.quotam}, the evidence supports about ${s.bestm}, so a ${s.gap > 0 ? s.gapm : '$0'} gap. Not sure how to take it upstairs. Worth 20 minutes?`,
  bookNote: (s) => `Quota Case: quota ${s.quotam}, evidence supports ${s.bestm}, gap ${s.gap > 0 ? s.gapm : 'none'}.`,
});"""),
 dict(slug='commit', name='Commit Check',
  title='Commit Check: Will They Burn the Commit?',
  desc='For cloud and consumption sellers: will the customer use their committed spend? See the pace, the monthly spend it takes from here, and the shortfall or overage.',
  ogdesc='Commit, term and spend so far. See whether they\'ll burn it, fall short, or run over.',
  h1='Will they burn the commit?', dek='The commit, the term, what they\'ve spent so far and what they spend now. See whether they\'ll use it, fall short, or run over.',
  fields=[dict(id='commit',kind='money',label='Total commit',example='$3,000,000'),
          dict(id='term',kind='count',label='Term, in months',example='36'),
          dict(id='elapsed',kind='count',label='Months in so far',example='14'),
          dict(id='used',kind='money',label='Spent so far',example='$900,000'),
          dict(id='monthly',kind='money',label='Current monthly spend',example='$70,000')],
  card=dict(headline=['Will they burn', 'the commit?'],dek='Commit. Term. Spent so far. Monthly spend.',pillars=['COMMIT','TERM','SPENT','PACE']),
  bands=[('how','How the burn-down works','''    <p class="lede">Take what they've spent, add today's monthly spend for every month that's left, and compare it with the commit. That's where the account lands if nothing changes.</p>
    <p>On a consumption plan, a commit nobody uses doesn't retire much quota. It also makes the renewal harder, because the customer remembers paying for capacity they never ran.</p>
    <p>The number that matters is the monthly spend it takes from here. If it's well above today's pace, you need new workloads with dates attached. A more hopeful forecast won't get you there.</p>
    <p>If they're running ahead of the commit, that's good news, but don't sit on it. Overage is spend nobody forecast, so start talking about the next commit before the renewal forces the conversation.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The math runs right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your numbers, and nothing leaves the page unless you share a result.'),
       ('What if the commit ramps, with a smaller first year?','This assumes the commit is spread evenly across the term. If yours ramps, run it one year at a time, with that year\'s commitment and months.'),
       ('Does marketplace or partner spend count?','If it counts toward the commit under the customer\'s agreement, include it in spent so far. Crediting rules differ by provider and contract, so check yours before you rely on the number.'),
       ('What if I leave current monthly spend blank?','Then it uses their average so far: spent divided by months in. Today\'s monthly spend is usually the better guide, because most accounts ramp.')],
  config="""CalcTool({
  slug: 'commit', answers: {"Overage": "Yes, and then some.", "On pace": "Yes. They're on pace.", "Behind": "Not at this pace.", "Short": "No. They'll fall short.", "Way short": "No. Not even close."}, name: 'Commit Check', url: 'https://quotabird.com/commit/',
  fields: [{ id: 'commit', kind: 'money' }, { id: 'term', kind: 'count' }, { id: 'elapsed', kind: 'count' }, { id: 'used', kind: 'money' }, { id: 'monthly', kind: 'money' }],
  compute(v) {
    if (!(v.commit > 0)) return { msg: 'Add the total commit.' };
    if (!(v.term > 0)) return { msg: 'Add the length of the commit, in months.' };
    if (!(v.elapsed > 0)) return { msg: 'Add how many months into the commit they are.' };
    if (v.elapsed >= v.term) return { msg: 'Months in has to be less than the term. If the term is over, compare what they spent with the commit.' };
    const pct = (r) => Math.round(r * 100) + '%';
    const money = (n) => { const neg = n < 0; n = Math.abs(n); const t = n >= 1e6 ? '$' + (n / 1e6).toFixed(2).replace(/\\.?0+$/, '') + 'M' : n >= 1e3 ? '$' + Math.round(n / 1e3) + 'K' : '$' + Math.round(n); return (neg ? '-' : '') + t; };
    const left = v.term - v.elapsed;
    const pace = v.monthly > 0 ? v.monthly : v.used / v.elapsed;
    const projected = v.used + pace * left, ratio = projected / v.commit;
    const need = Math.max(0, (v.commit - v.used) / left);
    let t;
    if (ratio >= 1.1) t = ['Overage', 'ready', 'Overage is spend nobody forecast. Start the next-commit conversation before the renewal does.'];
    else if (ratio >= .95) t = ['On pace', 'ready', 'Keep the workloads coming, and check it again next quarter.'];
    else if (ratio >= .8) t = ['Behind', 'proof', `They need ${money(need)} a month from here, up from ${money(pace)}. Find the workloads that close it, with dates.`];
    else if (ratio >= .6) t = ['Short', 'prove', `They need ${money(need)} a month from here, up from ${money(pace)}. Build a migration plan with the customer now, not in the last quarter.`];
    else t = ['Way short', 'dont', 'Have the true-up conversation now, while there\\'s still time to change the plan.'];
    const attack = `At ${money(pace)} a month, they'll use ${money(projected)} of a ${money(v.commit)} commit by month ${v.term}.`;
    const rows = [['Commit', money(v.commit)], [`Spent so far, month ${v.elapsed} of ${v.term}`, money(v.used)], ['Monthly spend now', money(pace)],
      ['Needed from here, per month', money(need), need > pace * 1.05 ? 'v-no' : ''], ['Projected by the end', money(projected)],
      [ratio >= 1 ? 'Overage' : 'Shortfall', money(Math.abs(projected - v.commit)), ratio < .95 ? 'v-no' : '']];
    return { label: t[0], cls: t[1], attack, sub: t[2], big: pct(ratio), rows, ratio, commitm: money(v.commit), projm: money(projected), stripText: '' };
  },
  handoff: (s) => s.ratio < .95
    ? { overline: 'Who else could use it?', text: 'Burning a commit takes more than one team. See how well you know the rest of the account.', href: '/account/', label: 'Check the account' }
    : { overline: 'Now put it in your number', text: 'An account running at or ahead of its commit is your easiest expansion. Make sure your quota case counts it.', href: '/quota-case/', label: 'Build your quota case' },
  mark: { title: () => 'Commit not burning?', body: "I'm Mark. I've sat in plenty of true-up conversations, the calm ones and the other kind. Send me the shape of it, no customer names." },
  dm: (s) => `Mark, ran a commit through Commit Check: ${s.projm} projected against a ${s.commitm} commit. Not sure what to do with the gap. Worth 20 minutes?`,
  bookNote: (s) => `Commit Check: ${s.projm} projected against ${s.commitm}.`,
});"""),

 dict(slug='quota', name='Quota Check',
  title='Quota Check: Is My Quota Crazy?',
  desc='Your quota against your on-target earnings, judged by what the number is measured in: new bookings, cloud consumption growth, or a whole book.',
  ogdesc='Is my quota crazy? Base, variable, quota and what it\'s measured in. A straight answer out.',
  h1='Is your quota crazy?', dek='Plug in your base, your variable and the number they handed you to find out.',
  fields=[dict(id='basis',kind='choice',label='What the number is measured in',example='cloud',options=[('saas','Bookings'),('cloud','Run rate'),('book','Whole book')]),
          dict(id='base',kind='money',label='Base salary',example='$150,000'),dict(id='variable',kind='money',label='Target variable at 100%',example='$130,000'),
          dict(id='quota',kind='money',label='Your quota for the year',example='$6,000,000'),dict(id='closed',more=True,kind='money',label='What you closed last year',example='',placeholder='$0 (optional)')],
  card=dict(headline=['Is your quota crazy?',''],dek='Your number against your on-target earnings, judged by what it\'s measured in.',pillars=['OTE','MULTIPLE','RATE','GROWTH']),
  bands=[('pushback','If the number is crazy','''    <p class="lede">Saying it feels too high won't move it. Bring the math: last year's sales, your run rate, qualified pipeline at your real win rate, headcount and ramp time. Then ask what has to be true for the number to be reasonable.</p>
    <p>Better yet, get into planning the year before, while somebody still has the spreadsheet open. <a href="/notes/prove-the-quota-is-crazy/">Your quota is crazy. Now prove it.</a> walks through it, with an example you can steal. If you're the rep, start with <a href="/notes/push-back-as-a-rep/">this one</a>. If you're the manager handing it down, <a href="/notes/handing-down-a-tough-quota/">this one</a>.</p>'''),('how','Why the multiple depends on what you sell','''    <p class="lede">Divide your quota by your on-target earnings. That one number tells you a lot about the plan, once you know what the quota is measured in.</p>
    <p>For a new-bookings AE, 4 to 6 times OTE is a useful working range. Bridge Group's 2026 median was 4.6, and enterprise roles run a little higher. That range is really just a commission rate, stated another way. At a 50/50 pay mix and roughly 10% on new ARR, quota works out to about five times OTE. Below 3 is unusual and usually means a ramp, an overlay, or a plan with a condition in it. Above 8 the plan is asking for something the territory may not have.</p>
    <p>Cloud consumption is a different animal, and it's the one most people on this site carry. The number is incremental revenue growth on a book, typically paid at a low single-digit percentage, roughly 1.5 to 3%, so the same arithmetic gives 15 to 30 times OTE at a big cloud provider and higher in strategic accounts. A rep carrying a $6M growth target on a $280K OTE is at 21×, and that's ordinary, not crazy. Whole-book targets (retention plus growth on the full run rate) are paid at around half a percent to one percent and run higher still, 40 to 80 times OTE, because most of that revenue would have happened anyway. <a href="/methodology/">How these ranges are derived</a>.</p>
    <p>The number to watch across all three is the implied rate: your variable divided by your quota. If it's well under what your peers are paid on the same kind of number, the plan is heavier than the multiple alone suggests. And if you closed last year, the growth the new number implies is the real measure of how much harder this year is. Whether the territory can produce it is <a href="/territory/">Territory Check</a>; how much pipeline it takes is <a href="/pipeline/">Pipeline Check</a>.</p>'''),
         ('ranges',"QuotaBird's working ranges",'''    <p>These ranges come from plans at cloud providers, SaaS companies and their partners. They're guides, not rules, and roles differ. Quota ÷ OTE:</p>
    <p><strong>New bookings.</strong> Under 3: low. 3 to 4: favorable. 4 to 6: standard. 6 to 8: a stretch. 8 to 12: aggressive. Over 12: crazy.</p>
    <p><strong>Cloud consumption growth.</strong> Under 8: low. 8 to 15: favorable. 15 to 30: standard. 30 to 45: a stretch. 45 to 60: aggressive. Over 60: crazy.</p>
    <p><strong>Whole book.</strong> Under 20: low. 20 to 40: favorable. 40 to 80: standard. 80 to 120: a stretch. 120 to 160: aggressive. Over 160: crazy.</p>
    <p>If your plan sits somewhere else and the range looks wrong, tell Mark and he'll take a look.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The math runs right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your numbers, and nothing leaves the page unless you share a result.'),
       ('Why does it ask what the number is measured in?','Because the same multiple means different things. A $1.4M new-bookings quota on a $280K OTE is 5× and normal. A $1.4M cloud consumption growth target on the same OTE is 5× and unusually light, because consumption is paid at a fraction of the rate bookings are. Pick the basis your plan actually uses.'),
       ('Where do the ranges come from?','The bookings range is a working range built around published data: Bridge Group\'s 2026 median was 4.6× OTE across 158 B2B companies. The cloud and whole-book ranges come from plans at cloud providers and their partners, worked back from the commission rates those plans pay. They\'ll change if enough people report plans that sit somewhere else.'),
       ('What if my variable is a bonus, not commission?','Use the target amount at 100% attainment either way. The tool cares about how much of your pay depends on the number, not what the plan calls it.')],
  config="""CalcTool({
  slug: 'quota', answers: {"Low": "It's unusually low.", "Favorable": "No. It's favorable.", "Standard": "No. It's standard.", "A stretch": "Not crazy. A stretch.", "Aggressive": "Close. It's aggressive.", "Crazy": "Yes. It's crazy."}, name: 'Quota Check', url: 'https://quotabird.com/quota/',
  fields: [{ id: 'basis', kind: 'choice', example: 'cloud' }, { id: 'base', kind: 'money' }, { id: 'variable', kind: 'money' }, { id: 'quota', kind: 'money' }, { id: 'closed', kind: 'money' }],
  compute(v) {
    if (!(v.base > 0 && v.variable > 0 && v.quota > 0)) { const m = [v.quota > 0 ? '' : 'your quota', v.base > 0 ? '' : 'your base', v.variable > 0 ? '' : 'your variable'].filter(Boolean); return { msg: 'Add ' + (m.length > 1 ? m.slice(0, -1).join(', ') + ' and ' + m[m.length - 1] : m[0]) + '.' }; }
    const ote = v.base + v.variable, mult = v.quota / ote, share = v.variable / ote, rate = v.variable / v.quota;
    const X = (mult >= 10 ? Math.round(mult) : mult.toFixed(1)) + '×';
    const pct = (r) => Math.round(r * 100) + '%';
    const ratePct = rate >= .1 ? Math.round(rate * 100) + '%' : (rate * 100).toFixed(rate >= .01 ? 1 : 2) + '%';
    const money = (n) => n >= 1e6 ? '$' + (n / 1e6).toFixed(2).replace(/\\.?0+$/, '') + 'M' : n >= 1e3 ? '$' + Math.round(n / 1e3) + 'K' : '$' + Math.round(n);
    // ranges I've seen, by what the quota is measured in (see the page copy)
    const B = { saas: { name: 'new bookings', cuts: [3, 4, 6, 8, 12] }, cloud: { name: 'cloud consumption growth', cuts: [8, 15, 30, 45, 60] }, book: { name: 'a whole book', cuts: [20, 40, 80, 120, 160] } }[v.basis] || { name: 'cloud consumption growth', cuts: [8, 15, 30, 45, 60] };
    const c = B.cuts, std = c[1] + ' to ' + c[2];
    let t;
    if (mult < c[0]) t = ['Low', 'proof', `Your quota is ${X} your OTE. For ${B.name} that's unusually low: a ramp, an overlay, or a plan with a condition in it.`, 'Read the plan twice. Low multiples usually come with a catch.'];
    else if (mult < c[1]) t = ['Favorable', 'ready', `Your quota is ${X} your OTE, below QuotaBird's working range of ${std} for ${B.name}.`, 'Common in new territories, SMB and commercial. Enjoy it while it lasts.'];
    else if (mult <= c[2]) t = ['Standard', 'ready', `Your quota is ${X} your OTE, inside QuotaBird's working range of ${std} for ${B.name}.`, "The number is ordinary. Whether the territory can produce it is a different question."];
    else if (mult <= c[3]) t = ['A stretch', 'proof', `Your quota is ${X} your OTE, above QuotaBird's working range of ${std} for ${B.name}.`, 'Normal for enterprise and strategic roles, and it needs a strong pipeline behind it.'];
    else if (mult <= c[4]) t = ['Aggressive', 'prove', `Your quota is ${X} your OTE, well above QuotaBird's working range of ${std} for ${B.name}.`, 'Strategic-account territory. You need coverage and a territory that can produce it.'];
    else t = ['Crazy', 'dont', `Your quota is ${X} your OTE. For ${B.name}, the plan is asking your territory for something it may not have.`, 'Check the territory before you sign, and get the sizing in writing.'];
    const growth = v.closed > 0 ? (v.quota - v.closed) / v.closed : null;
    const rows = [['On-target earnings', money(ote)], ['Quota ÷ OTE', X], ['Implied rate on quota', ratePct], ['Variable share of OTE', pct(share)]];
    if (growth != null) rows.push(['Growth over what you closed', (growth >= 0 ? '+' : '') + pct(growth), growth > .3 ? 'v-no' : '']);
    const note = share < .4 ? 'Variable is under 40% of OTE. You\\'re paid mostly to show up, and the quota matters less than it looks.' : share > .6 ? 'Variable is over 60% of OTE. The quota is most of your pay. Treat it like one.' : '';
    return { label: t[0], cls: t[1], attack: t[2], sub: t[3], big: X, rows, note, mult, share, growth, ote, quota: v.quota, basis: B.name, ratePct };
  },
  handoff: (s) => (s.cls === 'prove' || s.cls === 'dont')
    ? { overline: 'Before you push back', text: 'How to prove it with last year, your run rate and your pipeline, not feelings.', href: '/notes/prove-the-quota-is-crazy/', label: 'Read: Now prove it' }
    : { overline: 'Now the coverage math', text: `At 3X you'd need about $${(s.quota * 3 / 1e6).toFixed(1)}M of qualified pipeline to cover it. Your win rate will say more.`, href: `/pipeline/#t=${Math.round(s.quota)}&y=cy`, label: 'Check your pipeline' },
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
    <p>These are rough ranges from real deals; yours may differ. Up to about 5% is normal negotiation. Nobody remembers it. Between 5 and 15% is meaningful, and it should buy something specific: a signature date, a larger scope, a reference, a multi-year term. Above 15% you're paying for a decision, so the decision had better come with it, this quarter, in writing. Above 25%, you're usually paying to be liked, and the customer will remember the number.</p>
    <p>Two things sellers forget. The discount comes out of your commission at exactly the same rate it comes out of revenue, so a 15% discount is a 15% pay cut on that deal. And it comes out of the company's margin much faster than 15%: cost of goods doesn't move, so every dollar off the price is a dollar off the margin.</p>
    Before you discount at all, figure out whether the objection is really the price or the deal. A discount only helps with the price. <a href="/notes/fifteen-percent-off/">They asked for 15% off</a> walks through what to ask for in return.''')],
  faq=[('Does anything I enter leave my device?','No. The math runs right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your numbers, and nothing leaves the page unless you share a result.'),
       ('How is the new margin calculated?','Cost of goods stays the same when the price drops, so the margin after discount is one minus cost divided by the discounted price. That\'s why a 15% discount on a 40% margin leaves about 29%, not 25%.'),
       ('What if I don\'t know the company margin?','Leave it at the example and read the commission rows only. The margin rows are for the conversation with your manager; the commission row is the one that\'s about you.')],
  config='''CalcTool({
  slug: 'discount', answers: {"Normal": "This much is normal.", "Meaningful": "This much needs a trade.", "Expensive": "This much is expensive.", "Giveaway": "This much is too much."}, name: 'Discount Check', url: 'https://quotabird.com/discount/',
  fields: [{ id: 'list', kind: 'money' }, { id: 'disc', kind: 'pct' }, { id: 'margin', kind: 'pct' }, { id: 'rate', kind: 'pct' }],
  compute(v) {
    if (!(v.list > 0 && v.disc > 0)) return { msg: v.list > 0 ? 'Add the discount, as a percent of list. It has to be under 100%.' : 'Add the list price.' };
    const pct = (r) => Math.round(r * 100) + '%';
    const money = (n) => { const neg = n < 0; n = Math.abs(n); const t = n >= 1e6 ? '$' + (n / 1e6).toFixed(2).replace(/\\.?0+$/, '') + 'M' : n >= 1e3 ? '$' + Math.round(n / 1e3) + 'K' : '$' + Math.round(n); return (neg ? '-' : '') + t; };
    const discounted = v.list * (1 - v.disc), given = v.list - discounted;
    const commFull = v.list * v.rate, commLost = given * v.rate, commAfter = commFull - commLost;
    const cogs = v.list * (1 - v.margin), newMargin = v.margin > 0 ? Math.max(0, 1 - cogs / discounted) : null;
    let t;
    if (v.disc <= .05) t = ['Normal', 'ready', 'Inside the normal range for a negotiation.'];
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
  handoff: (s) => ({ overline: s.cls === 'ready' ? 'Even a small discount should buy something' : 'Before you say yes', text: s.cls === 'ready' ? 'What to ask for in return, so the next discount is never automatic.' : `What to ask for in return for ${Math.round(s.disc * 100)}% off, and how to hold the line on the rest.`, href: '/notes/fifteen-percent-off/', label: 'Read: They asked for 15% off' }),
  mark: { title: () => 'Stuck on the price?', body: "I'm Mark. I've watched a lot of discounts buy absolutely nothing. If somebody's asking you to sharpen the pencil, send me a line about why, no customer names or dollars." },
  dm: (s) => `Mark, ran a discount through Discount Check. ${Math.round(s.disc * 100)}% off costs me ${Math.round(s.disc * 100)}% of my commission${s.newMargin != null ? ' and takes margin from ' + Math.round(s.margin * 100) + '% to ' + Math.round(s.newMargin * 100) + '%' : ''}. Not sure it's worth it. Worth 20 minutes?`,
  bookNote: (s) => `Discount Check: ${Math.round(s.disc * 100)}% off${s.newMargin != null ? ', margin ' + Math.round(s.margin * 100) + '% to ' + Math.round(s.newMargin * 100) + '%' : ''}, ${s.label.toLowerCase()}.`,
});'''),
 dict(slug='pay', name='Pay Check',
  title='Pay Check: What Does This Comp Plan Actually Pay?',
  desc='Base, variable, accelerator, cap and threshold in. What the plan pays at 50% to 200% of quota out, and where the upside goes.',
  ogdesc='What does this plan actually pay at 75%, 100% and 150% of quota? Base, variable, accelerator and cap in.',
  h1='What does this plan actually pay?', dek='Put in your base, your variable and how the plan pays above 100%. See what you make at 50% to 200% of quota.',
  fields=[dict(id='base',kind='money',label='Base salary',example='$150,000'),
          dict(id='variable',kind='money',label='Target variable at 100%',example='$130,000'),
          dict(id='accel',kind='pctx',label='Rate above the accelerator, as % of your normal rate',example='150%'),
          dict(id='start',kind='pctx',label='Accelerator starts at',example='100%'),
          dict(id='cap',more=True,kind='pctx',label='Variable capped at, % of target',example='',placeholder='uncapped'),
          dict(id='threshold',more=True,kind='pct',label='Nothing pays below',example='',placeholder='0% (optional)')],
  card=dict(headline=['What does this plan', 'actually pay?'],dek='Base. Variable. Accelerator. Cap.',pillars=['BASE','VARIABLE','ACCELERATOR','CAP']),
  bands=[('how','How to read the curve','''    <p class="lede">OTE is what you make if you hit 100%. The rows above and below it are what you make in a real year.</p>
    <p>Below 100%, most plans pay your variable in a straight line: 75% of quota pays 75% of your variable. Some plans pay nothing below a threshold, often 50%, so a bad year can take the whole variable.</p>
    <p>Above 100%, an accelerator raises your rate. A 1.5× accelerator pays 150% of your normal rate on everything past the point where it starts. That's where good years make real money.</p>
    <p>A cap stops it. If variable is capped at 150% of target, nothing past that pays, however big the year. A plan that sounds exciting can pay very little above quota once the cap and the starting point are in.</p>
    <p>Plan your budget on the 75% and 100% rows. Bridge Group's 2026 study found 48% of AEs hit quota, so the accelerator rows are the good years, not the average one.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The math runs right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your numbers, and nothing leaves the page unless you share a result.'),
       ('My plan has more than one accelerator tier. What do I enter?','Enter the first tier. The rows past it will be conservative, since later tiers usually pay more. If the tiers matter to your decision, work the higher ones by hand from the plan document.'),
       ('What about stock, RSUs and bonuses outside the plan?','This covers cash comp from the plan only. Stock, RSUs and ESPPs can matter a lot, and they get complicated fast. QuotaBird doesn\'t value them or give financial advice.')],
  config="""CalcTool({
  slug: 'pay', answers: {"Real upside": "Yes, it pays for beating the number.", "Some upside": "A little extra above 100%.", "Straight line": "It pays in a straight line.", "Thin upside": "Not much above 100%.", "Capped": "The cap takes the upside."}, name: 'Pay Check', url: 'https://quotabird.com/pay/',
  fields: [{ id: 'base', kind: 'money' }, { id: 'variable', kind: 'money' }, { id: 'accel', kind: 'pctx' }, { id: 'start', kind: 'pctx' }, { id: 'cap', kind: 'pctx' }, { id: 'threshold', kind: 'pct' }],
  compute(v) {
    if (!(v.variable > 0)) return { msg: 'Add your target variable at 100% of quota.' };
    const base = v.base > 0 ? v.base : 0;
    const money = (n) => n >= 1e6 ? '$' + parseFloat((n / 1e6).toFixed(2)) + 'M' : '$' + Math.round(n / 1e3) + 'K';
    const pct = (r) => Math.round(r * 100) + '%';
    const acc = v.accel > 0 ? v.accel : 1, start = v.start > 0 ? v.start : 1, cap = v.cap > 0 ? v.cap : Infinity, th = v.threshold > 0 ? v.threshold : 0;
    const pay = (a) => a < th ? 0 : Math.min(v.variable * Math.min(a, start) + (a > start ? v.variable * (a - start) * acc : 0), v.variable * cap);
    const extra = pay(1.5) - pay(1), straight = v.variable * .5, ratio = extra / straight;
    let t;
    if (cap < 1.5 && ratio < .3) t = ['Capped', 'dont', `The cap stops your variable at ${pct(cap)} of target. Ask whether it's ever been lifted for a big year.`];
    else if (ratio < .95) t = ['Thin upside', 'prove', 'A cap or a late start takes most of the upside. Know that before you count on a big year.'];
    else if (ratio >= 1.2) t = ['Real upside', 'ready', 'Plan your budget on the 75% and 100% rows. The rows above them are the good years.'];
    else if (ratio >= 1.02) t = ['Some upside', 'proof', 'The accelerator starts late or pays a small premium. Plan on the 75% and 100% rows.'];
    else t = ['Straight line', 'proof', 'Fair, with no extra reward for beating the number. Plan on the 75% and 100% rows.'];
    const rows = [.5, .75, 1, 1.25, 1.5, 2].map(a => [`At ${pct(a)} of quota`, money(base + pay(a)), a < th ? 'v-no' : '']);
    if (th > 0) rows.push(['Nothing pays below', pct(th), 'v-no']);
    const attack = `At 150% of quota you'd make ${money(base + pay(1.5))}, ${money(extra)} more than at 100%.`;
    return { label: t[0], cls: t[1], attack, sub: t[2], big: '+' + money(extra), rows, ote: money(base + v.variable), extram: money(extra), stripText: '' };
  },
  handoff: (s) => ({ overline: 'Can you trust the rest of it?', text: 'The rate is only half of it. Comp Plan Check covers crediting, payout timing, clawbacks and mid-year changes.', href: '/comp-plan/', label: 'Check your comp plan' }),
  mark: { title: () => 'Plan look thin?', body: "I'm Mark. I've seen plans that sound great in the offer and pay very little above quota. Send me the shape of yours, no company name." },
  dm: (s) => `Mark, ran my comp plan through Pay Check: ${s.extram} more at 150% than at 100%, on a ${s.ote} OTE. Is that normal? Worth 20 minutes?`,
  bookNote: (s) => `Pay Check: ${s.extram} extra at 150%, OTE ${s.ote}.`,
});"""),
 dict(slug='offer', name='Offer Check',
  title='Offer Check: Which Offer Actually Pays More?',
  desc='Two sales job offers side by side: base, variable, ramp and guarantee in, year-one cash and a normal year at a realistic attainment out.',
  ogdesc='Two offers, side by side. Year-one cash with the ramp, and a normal year at a realistic attainment.',
  h1='Which offer actually pays more?', dek='Put in both offers and a realistic attainment. See year one with the ramp, and a normal year after it.',
  fields=[dict(id='baseA',head='Offer A',kind='money',label='Base',example='$150,000'),
          dict(id='varA',kind='money',label='Target variable',example='$130,000'),
          dict(id='rampA',kind='count',label='Ramp, in months',example='6'),
          dict(id='guarA',more=True,kind='pctx',label='Offer A: variable guaranteed during ramp',example='',placeholder='none'),
          dict(id='baseB',head='Offer B',kind='money',label='Base',example='$170,000'),
          dict(id='varB',kind='money',label='Target variable',example='$150,000'),
          dict(id='rampB',kind='count',label='Ramp, in months',example='6'),
          dict(id='guarB',more=True,kind='pctx',label='Offer B: variable guaranteed during ramp',example='',placeholder='none'),
          dict(id='attain',head='Both offers',kind='pctx',label='Realistic attainment',example='85%')],
  card=dict(headline=['Which offer', 'actually pays more?'],dek='Base. Variable. Ramp. Guarantee.',pillars=['BASE','VARIABLE','RAMP','ATTAINMENT']),
  bands=[('how','How the comparison works','''    <p class="lede">An offer letter shows OTE, which is what you make at exactly 100% of quota. This compares the two offers at the attainment you think is realistic, which is usually closer to what you'll make.</p>
    <p>A normal year is base plus variable at that attainment. Year one also counts the ramp: during the ramp months you earn your guarantee if there is one, and otherwise about half your normal attainment, since new reps rarely sell at full speed. That half is an assumption, and it's shown so you can argue with it.</p>
    <p>If one offer has a much bigger quota for the same pay, put in a lower attainment for that job and run it again. <a href="/quota/">Quota Check</a> tells you whether each quota is in the normal range for how it's measured.</p>
    <p>This covers cash only, at a straight-line rate. It doesn't include accelerators (<a href="/pay/">Pay Check</a> does), or stock, RSUs and ESPPs, which QuotaBird doesn't value. It isn't financial advice.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The math runs right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your numbers, and nothing leaves the page unless you share a result.'),
       ('What attainment should I use?','Whatever you honestly expect. Bridge Group\'s 2026 study found 48% of AEs hit quota, so 100% is optimistic for most people. Ask each company what share of its team hit quota last year and adjust.'),
       ('What if the guarantee is a draw I have to pay back?','Then leave the guarantee blank. A recoverable draw is an advance against future commission, not extra money.')],
  config="""CalcTool({
  slug: 'offer', share: { baseA: 'base', varA: 'variable' }, answers: {"Close": "About the same money.", "A pays more": "Offer A pays more in a normal year.", "B pays more": "Offer B pays more in a normal year."}, name: 'Offer Check', url: 'https://quotabird.com/offer/',
  fields: [{ id: 'baseA', kind: 'money' }, { id: 'varA', kind: 'money' }, { id: 'rampA', kind: 'count' }, { id: 'guarA', kind: 'pctx' }, { id: 'baseB', kind: 'money' }, { id: 'varB', kind: 'money' }, { id: 'rampB', kind: 'count' }, { id: 'guarB', kind: 'pctx' }, { id: 'attain', kind: 'pctx' }],
  compute(v) {
    if (!(v.baseA > 0 && v.baseB > 0)) return { msg: v.baseA > 0 ? "Add Offer B's base." : v.baseB > 0 ? "Add Offer A's base." : "Add both offers' base and variable." };
    if (v.guarA > 1 || v.guarB > 1) return { msg: `Offer ${v.guarA > 1 ? 'A' : 'B'}'s ramp guarantee is a share of its target variable, from 0 to 100%. Check that number.` };
    const money = (n) => n >= 1e6 ? '$' + parseFloat((n / 1e6).toFixed(2)) + 'M' : '$' + Math.round(n / 1e3) + 'K';
    const at = v.attain > 0 ? v.attain : .85;
    const year1 = (base, vari, ramp, guar) => { const r = Math.min(12, ramp || 0); return base + vari / 12 * (r * (guar > 0 ? guar : at * .5) + (12 - r) * at); };
    const normA = v.baseA + v.varA * at, normB = v.baseB + v.varB * at;
    const y1A = year1(v.baseA, v.varA, v.rampA, v.guarA), y1B = year1(v.baseB, v.varB, v.rampB, v.guarB);
    const diff = normB - normA, d1 = y1B - y1A, rel = Math.abs(diff) / Math.max(normA, normB);
    const lead = diff > 0 ? 'B' : 'A', other = diff > 0 ? 'A' : 'B';
    let t;
    if (rel < .03) t = ['Close', 'proof', 'Close enough that the rest of the job should decide it: the territory, the manager, and how many people actually hit quota.'];
    else t = [lead + ' pays more', 'proof', 'That assumes the same attainment at both jobs. If one quota is much harder, lower its attainment and run it again.'];
    let attack = rel < .03 ? `At ${Math.round(at * 100)}% attainment, the two offers are within ${money(Math.abs(diff))} of each other in a normal year.` : `At ${Math.round(at * 100)}% attainment, Offer ${lead} pays ${money(Math.abs(diff))} more in a normal year.`;
    // year one always gets its own sentence, so changing a ramp or a guarantee visibly changes the answer
    const y1lead = d1 > 0 ? 'B' : 'A';
    if (Math.abs(d1) < 1000) attack += ' Year one comes out about even.';
    else if (rel >= .03 && y1lead !== lead) attack += ` In year one, Offer ${y1lead} pays ${money(Math.abs(d1))} more, because of its ramp or guarantee.`;
    else attack += ` In year one, Offer ${y1lead} pays ${money(Math.abs(d1))} more.`;
    const long = ['A', 'B'].filter(k => v['ramp' + k] > 12);
    if (long.length) attack += long.length === 2 ? " Both ramps run past the first year, so all of year one is ramp pay." : ` Offer ${long[0]}'s ramp runs past the first year, so all of year one is ramp pay.`;
    const rows = [['Offer A at 100% (OTE)', money(v.baseA + v.varA)], ['Offer B at 100% (OTE)', money(v.baseB + v.varB)],
      ['Offer A, year one', money(y1A)], ['Offer B, year one', money(y1B)],
      [`Offer A, normal year at ${Math.round(at * 100)}%`, money(normA)], [`Offer B, normal year at ${Math.round(at * 100)}%`, money(normB)]];
    return { label: t[0], cls: t[1], attack, sub: t[2], big: rel < .03 ? money(Math.abs(diff)) : '+' + money(Math.abs(diff)), rows, diffm: money(Math.abs(diff)), lead, stripText: '' };
  },
  handoff: { overline: 'Before you sign', text: 'How to review an offer, what to ask, and how to push back on the parts that matter.', href: '/notes/review-an-offer/', label: 'Read: Review an offer' },
  mark: { title: () => 'Weighing two offers?', body: "I'm Mark. I've looked at a lot of offers, and the one with the bigger OTE isn't always the one that pays more. Send me the shape of both, no company names." },
  dm: (s) => `Mark, ran two offers through Offer Check. At a realistic attainment one pays ${s.diffm} more in a normal year. Worth 20 minutes before I decide?`,
  bookNote: (s) => `Offer Check: ${s.diffm} difference in a normal year.`,
});"""),
 dict(slug='commission', name='Commission Check',
  title='Commission Check: Your Take-Home on a Deal',
  desc='Deal size, commission rate and your share of the credit in, what you actually take home out, after the share you set aside for taxes.',
  ogdesc='It closed. Here is roughly what you actually take home.',
  h1="It closed. What do you actually keep?", dek='Plug in the deal and your rate to find out, roughly, before the check lands.',
  fields=[dict(id='deal',kind='money',label='Deal size',example='$500,000'),dict(id='rate',kind='pct',label='Your commission rate',example='8%'),
          dict(id='credit',more=True,kind='pct',label='Your share of the credit',example='',placeholder='100%'),
          dict(id='mult',more=True,kind='pct',label='Product multiplier',example='',placeholder='100% (optional)'),
          dict(id='buffer',kind='pct',label='Set aside for taxes',example='30%',presets=[('W-2 ~30%','30%'),('High bracket ~40%','40%'),('1099 ~20%','20%')])],
  card=dict(headline=['It closed.','What do I take home?'],dek='A planning estimate of the check after withholding, in about ten seconds.',pillars=['DEAL','RATE','WITHHELD','TAKE-HOME']),
  bands=[('how','Why the check is smaller than the math','''    <p class="lede">The commission in your plan and the money that hits your account are further apart than most sellers expect, especially the first time.</p>
    <p>The percentage you set aside is a planning buffer, not a withholding rate. For commissions paid separately from salary, the IRS lets employers withhold federal income tax at a flat 22% (up to a million dollars a year), and payroll taxes and state withholding come on top of that, so a W-2 check often lands with roughly 30% gone. High earners tend to owe closer to 40% once the year is reconciled. A 1099 contractor has nothing withheld and should set aside 20% or more. Your real number depends on your state, your filing status and everything else you earned this year, which is why the field is editable.</p>
    <p>Use it to plan, not to argue with payroll. Then ask the better question: is the comp plan itself sane? That's <a href="/quota/">Quota Check</a>.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The math runs right here in your browser. There\'s no account, and nothing goes to a server or your CRM. QuotaBird counts page views with Google Analytics, but it never sees your numbers, and nothing leaves the page unless you share a result.'),
       ('Is this tax advice?','No. It\'s just a planning buffer. Payroll and taxes are messier than this calculator. If the number actually matters, ask an accountant.'),
       ('What about accelerators and clawbacks?','Enter the rate that applies to this deal. If your plan has accelerators above quota, use the accelerated rate; if it has clawbacks, remember the take-home is provisional until the clawback window closes.')],
  config='''CalcTool({
  slug: 'commission', answers: {"Take-home": "That's your take-home."}, name: 'Commission Check', url: 'https://quotabird.com/commission/',
  fields: [{ id: 'deal', kind: 'money' }, { id: 'rate', kind: 'pct' }, { id: 'credit', kind: 'pct' }, { id: 'mult', kind: 'pct' }, { id: 'buffer', kind: 'pct' }],
  compute(v) {
    if (!(v.deal > 0 && v.rate > 0)) return { msg: v.deal > 0 ? 'Add your commission rate, as a percent.' : v.rate > 0 ? 'Add the deal size.' : 'Add the deal size and your commission rate.' };
    const money = (n) => n >= 1e6 ? '$' + (n / 1e6).toFixed(2).replace(/\\.?0+$/, '') + 'M' : n >= 1e3 ? '$' + Math.round(n / 1e3).toLocaleString() + 'K' : '$' + Math.round(n).toLocaleString();
    const tax = v.buffer > 0 ? v.buffer : .30;
    const credit = v.credit > 0 ? v.credit : 1, mult = v.mult > 0 ? v.mult : 1, credited = v.deal * credit * mult, split = credit !== 1 || mult !== 1;
    const gross = credited * v.rate, aside = gross * tax, net = gross - aside;
    return { label: 'Take-home', cls: 'ready', big: money(net), attack: (split ? `Your credit on this deal is ${money(credited)}. ` : '') + `Set aside ${Math.round(tax * 100)}% and you keep about ${Math.round((1 - tax) * 100)} cents of every commission dollar on this deal.`,
      sub: 'A planning buffer, not tax advice. Change the percentage to yours.', rows: [...(split ? [['Deal size', money(v.deal)], ['Your credit on it', money(credited)]] : []), ['Gross commission', money(gross)], ['Set aside, about', money(aside), 'v-no'], ['Take-home, about', money(net)]], keep: 1 - tax };
  },
  handoff: { overline: 'Before you count on it', text: 'Accelerators, caps, clawbacks and crediting can all change what this deal pays. Know how your plan works.', href: '/notes/read-your-comp-plan/', label: 'Read: How your plan pays' },
  mark: { title: () => 'Questions about the plan?', body: "I'm Mark. Comp plans tell you what the company actually thinks your job is worth. If yours doesn't add up, send me a line about it, and leave out the company name and the dollars." },
  dm: (s) => `Mark, ran a deal through Commission Check. I keep about ${Math.round(s.keep * 100)}% of gross. The question is whether the plan behind it is sane. Worth 20 minutes?`,
  bookNote: (s) => `Commission Check: keeps about ${Math.round(s.keep * 100)}% of gross.`,
});'''),
]

def calc_page(t):
    def field(f):
        if f['kind'] == 'choice':
            chips = ''.join(f'<button class="chip{" on" if v == f["example"] else ""}" data-choice="{f["id"]}" data-v="{v}" type="button" aria-pressed="{"true" if v == f["example"] else "false"}">{lab}</button>' for v, lab in f['options'])
            return f'        <div class="tf"><span class="tf-label" id="lbl-{f["id"]}">{f["label"]}</span><div class="chips" role="group" aria-labelledby="lbl-{f["id"]}">{chips}</div></div>\n'
        mode = 'numeric' if f['kind'] == 'count' else 'decimal'
        val = f' value="{f["example"]}"' if f.get('example') else ''
        ph = f' placeholder="{f["placeholder"]}"' if f.get('placeholder') else ''
        out = f'        <label class="tf"><span class="tf-label">{f["label"]}</span><input id="{f["id"]}" type="text" inputmode="{mode}" autocomplete="off"{val}{ph}></label>\n'
        if f.get('presets'):
            out += '        <div class="chips" style="margin:-6px 0 14px;">' + ''.join(f'<button class="chip" data-preset-for="{f["id"]}" data-v="{v}" type="button">{lab}</button>' for lab, v in f['presets']) + '</div>\n'
        return out
    def head(f): return f'        <div class="tf-head">{f["head"]}</div>\n' if f.get('head') else ''
    main = ''.join(head(f) + field(f) for f in t['fields'] if not f.get('more'))
    extra = ''.join(head(f) + field(f) for f in t['fields'] if f.get('more'))
    fields = main + (f'        <details class="more-fields"><summary>More details <span>optional</span></summary>\n{extra}        </details>\n' if extra else '')
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
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0B1215">
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
  <p>Questions or security issues: <a href="mailto:mark@quotabird.com">mark@quotabird.com</a></p>
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
  dek='Quota ÷ OTE is your variable share divided by your commission rate. It\'s really a pay rate.',
  answer='Quota ÷ OTE equals your variable share of OTE divided by your commission rate at 100% attainment. SaaS new-bookings plans cluster around 4×; cloud consumption plans, paid at a low single-digit percentage, run far higher by design.',
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
    <p>Sellers carrying consumption growth at a cloud provider are typically paid about 1.5 to 3% on their number, not ten, and whole-book plans pay around half a percent to one percent. Run that through the formula and consumption multiples land around 15 to 30 times OTE and whole-book multiples around 40 to 80, which is why a cloud AM compared against the SaaS benchmark looks wildly over-quota when the plan may be ordinary. This
      section is my experience across cloud providers and their partners, not published data; I haven't found a public
      dataset for consumption plans, and I'd rather say so than invent one. <a href="/methodology/">How QuotaBird's numbers work</a> shows the derivation.</p>''',
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
KIT_PAGES = '11'   # set from the rendered PDF
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
        <li><a href="#k-number">Where the number came from</a><span>Chapter 1</span></li>
        <li><a href="#k-fight">Quota or comp plan problem</a><span>Chapter 2</span></li>
        <li><a href="#k-handdown">Handing down a tough number</a><span>Chapter 3</span></li>
        <li><a href="#k-first">Rep problem</a><span>Chapter 4 or 9</span></li>
        <li><a href="#k-forecast">Forecast problem</a><span>Chapter 6</span></li>
        <li><a href="#k-pipeline">Pipeline problem</a><span>Chapter 7</span></li>
        <li><a href="#k-boss">Boss problem</a><span>Chapter 8</span></li>
        <li><a href="#k-review">Review season</a><span>Chapter 10</span></li>
        <li><a href="#k-alone">High performers</a><span>Chapter 13</span></li>
      </ul>
    </div>
  </section>

  <section class="kit-ch" id="k-number">
    <h2>1. How your team's number got built</h2>
    <p>Nobody built your team's number by looking at your team. At a cloud provider it starts with prior year revenue plus a growth rate, usually set above the geo VP, then gets spread down by region, segment and territory. In SaaS it's last year's ARR or bookings plus whatever the company promised its board. Either way, nobody in your chain actually picked the number. They divided it up.</p>
    <p>Every layer adds cushion. Most sales plans are over-assigned, and a common planning rule of thumb is 20 to 30%. That's why your reps' quotas can add up to more than your own number, and why a team can miss while the region makes it.</p>
    <p>Then find out what your boss is actually paid on, because it often isn't your number. Your VP might be goaled on growth rate, new business, new logos, consumption, margin, or a strategic program you've never heard of. Ask directly: "What are you measured on this year?"</p>
    <p>It changes what you fight for. If your boss is paid on growth rate and your baseline includes a one-time spike, fixing that baseline helps both of you, and now you have an ally. If your boss is paid on new logos, a plan built entirely on expansion won't get much help from above.</p>
    <p>Before you argue with anything, know your own baseline: prior year revenue by territory, what in it won't repeat, accounts that moved in or out, vacant territories, and who's still ramping. A vacant territory still has quota. Somebody's carrying it.</p>
    <div class="sheet">
      <h3>Worksheet: What your number is made of</h3>
      <p class="sheet-meta">What my boss is paid on __________________________ &nbsp; Date __________</p>
      <div class="mtable"><table class="ws"><thead><tr><th>Territory</th><th>Prior year revenue</th><th>One-time in it</th><th>Run rate now</th><th>Quota</th><th>Ramped?</th></tr></thead><tbody>
        <tr><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      </tbody></table></div>
    </div>
  </section>

  <section class="kit-ch" id="k-fight">
    <h2>2. Fighting the plan without losing</h2>
    <p>Most managers who fight the plan do it too late, get emotional, and argue about everything at once. The ones I've seen actually move a number went about it differently.</p>
    <p>Start early. The best time to shape your team's quota was last year, during planning, while the spreadsheet was still open and somebody upstairs was asking for input. The next best time is now. Once the numbers lock, the growth rate won't move, but some of the inputs still can.</p>
    <p>Put it on one page: prior year revenue minus one-time revenue, your current run rate, committed contracts landing this year, qualified pipeline at your real win rate, and capacity (ramped reps, open territories, how long ramp really takes). Then the gap. Keep the adjectives out of it.</p>
    <p>Ask for things that can actually move: the baseline, territory assignments, when new headcount lands, ramp relief for new reps, and crediting for partner and marketplace deals. Asking to change a growth rate your VP was handed just tells your VP you don't know how it works.</p>
    <p>Make one ask, in writing, once. If the answer doesn't make sense, escalate once. After that, commit to the number in front of your team and mean it. If you keep fighting a number after you've handed it down, you'll lose the team.</p>
    <p>Know when to stop. If there's a real answer to the gap, if the growth rate came from above your VP, or if your one page can't find the missing assumption, you're done arguing. Now it's a plan, and it's chapter 3.</p>
    <div class="sheet">
      <h3>Worksheet: The one-page case</h3>
      <p class="sheet-meta">Date __________ &nbsp; <span class="sheet-tool">Online: quotabird.com/quota-case</span></p>
      <div class="mtable"><table class="ws"><thead><tr><th>The evidence</th><th>$ or count</th></tr></thead><tbody>
        <tr><td>Prior year revenue, minus one-time revenue</td><td></td></tr>
        <tr><td>Current run rate (MRR × 12)</td><td></td></tr>
        <tr><td>Committed contracts landing this year</td><td></td></tr>
        <tr><td>Qualified pipeline × win rate</td><td></td></tr>
        <tr><td>Capacity: ramped reps, vacancies, months of ramp</td><td></td></tr>
        <tr><td>The number</td><td></td></tr>
        <tr><td><strong>The gap</strong></td><td></td></tr>
      </tbody></table></div>
      <p class="sheet-label">The one ask, who it went to, and when</p><div class="lines l2"></div>
    </div>
  </section>

  <section class="kit-ch" id="k-handdown">
    <h2>3. Handing down a tough number, and still crushing it</h2>
    <p>At some point you'll hand your team a number you don't love. How you hand it down decides whether they spend the year arguing about it or working on it.</p>
    <p>Own it. "Corporate made me do it" turns you into a messenger, and people don't follow messengers. You don't have to say the number is fair. Say it's the number and that you checked it.</p>
    <p>Show them the math: prior year revenue, the growth rate, where the team's number came from, and what you pushed back on and whether you got it. Reps take a hard number a lot better when they can see it didn't come out of nowhere.</p>
    <p>Give every rep a path: their gap, the new pipeline it takes at their win rate, and how much of that should come from existing accounts versus net-new ones. If a rep can't see how to get there, don't be surprised when they start updating their LinkedIn.</p>
    <p>Start early. On a run-rate number, a workload that lands in Q1 is worth about three times the same workload in Q4, so spend January building pipeline instead of reviewing the forecast.</p>
    <p>After that, stop reopening it. Talk about the gap every week, and stop debating whether the number is fair. Give people credit for pipeline they build early, as well as for deals they close.</p>
    <p>If you're the rep in this chapter, the Seller's Field Kit has the same conversation from the other side.</p>
    <div class="sheet">
      <h3>Worksheet: Every rep's path</h3>
      <p class="sheet-meta">Quarter __________</p>
      <div class="mtable"><table class="ws"><thead><tr><th>Rep</th><th>Quota</th><th>Gap</th><th>New pipeline needed</th><th>From existing</th><th>From net-new</th></tr></thead><tbody>
        <tr><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>
      </tbody></table></div>
    </div>
  </section>

  <section class="kit-ch" id="k-first">
    <h2>4. You inherited a team. Don't grade everybody yet.</h2>
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
      <p class="sheet-foot">Territory is no: fix the situation. Craft is no: coach. Will is no: manage. If both are no in a fair territory, read chapter 9.</p>
    </div>
  </section>

  <section class="kit-ch" id="k-rhythm">
    <h2>5. Keep the 1:1 and the forecast call separate</h2>
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
    <h2>6. What commit means</h2>
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
    <h2>7. Pipeline has two jobs</h2>
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
    <h2>8. Your boss mostly wants fewer surprises</h2>
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
    <h2>9. Before you write up a rep</h2>
    <p>Four very different problems can produce the same ugly dashboard.</p>
    <div class="mtable"><table><thead><tr><th>Problem</th><th>What it looks like</th><th>What I do</th></tr></thead><tbody>
      <tr><td>Bad situation</td><td>Good rep. Bad territory, quota, accounts or plan.</td><td>Fix the situation.</td></tr>
      <tr><td>Skill</td><td>They're working, customers engage, deals just aren't converting.</td><td>Coach. Sit in the room.</td></tr>
      <tr><td>Effort</td><td>They know how to sell. They're just not doing enough of it.</td><td>Set expectations clearly, in writing, with dates.</td></tr>
      <tr><td>Wrong fit</td><td>Fair territory, enough support, and neither the skill nor the effort is there.</td><td>Now it's a performance conversation.</td></tr>
    </tbody></table></div>
    <p>Before I call it a performance problem, I make sure the rep knows what good looks like next Tuesday, not someday. I spent months once coaching somebody whose territory couldn't have produced the number. I'd like those months back. So would the rep.</p>
    <p class="sheet-tool">The rep diagnostic is in chapter 4. Online: quotabird.com/rep</p>
  </section>

  <section class="kit-ch" id="k-review">
    <h2>10. Review season: bring receipts</h2>
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
    <h2>11. Things I learned the expensive way</h2>
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
    <h2>12. A few lines worth stealing</h2>
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
    <h2>13. Managing high performers</h2>
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
    <p>I'm Mark. I spent six years leading federal partner sales teams at Amazon, after plenty of years carrying a number myself. If you're staring at a deal, a forecast, a rep problem or a number that doesn't make sense, tell me about it.</p>
    <p class="kit-cta-terms">A free twenty-minute call, no pitch.</p>
    <div class="btn-row kit-cta-row">
      <a class="btn btn-primary btn-lg" id="kitBook" href="https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&amp;utm_medium=kit&amp;utm_content=kit_cta" target="_blank" rel="noopener">Chat with Mark</a>
      <a class="btn btn-lg" href="https://www.linkedin.com/in/markflournoy/" target="_blank" rel="noopener">DM on LinkedIn</a>
    </div>
    <p class="kit-bridge">Used this with your team and found something ugly? That's <a href="/work-with-mark/">most of the stuff I help managers with</a>.</p>
    <p class="fine">Or email me: <a href="mailto:mark@quotabird.com">mark@quotabird.com</a>. And if I don't think I can help, I'll tell you.</p>
  </section>
'''
_kit_url = 'https://quotabird.com/kit/'
_kit_desc = "Useful things for the weeks when the number, the team, or both are giving you trouble. A free, printable field kit for sales managers: how your team's number got built, fighting the plan, handing down a tough quota, inheriting a team, one-on-ones, the forecast call, pipeline, your boss, a struggling rep, review season, and the worksheets that go with them."
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
      <p class="kit-hero-meta">__KPAGES__ pages, prints on letter or A4. Thirteen short chapters and nine worksheets.</p>
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
_kit = _kit.replace('__KPAGES__', KIT_PAGES)
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

  <section class="kit-ch" id="l-plan">
    <h2>1. Shape the number before it shapes your team</h2>
    <p>The leaders people trust with a number are usually the ones who helped set it.</p>
    <p>If you're in the planning room, build quotas that hold. Start from prior year revenue with the one-time revenue taken out. Plan from capacity: ramped reps, vacancies, and how long ramp really takes. Decide on purpose how much over-assignment you're adding, instead of letting every layer pad it.</p>
    <p>If you're not in the room yet, get there. The best time to shape your team's quota was last year. The next best time is now: bring your baseline, your capacity and your pipeline to whoever builds the plan, before they ask.</p>
    <p>Know what your boss is paid on, and what their boss is paid on. Growth rate, new business, consumption, margin. When you can connect your team's plan to the metric the person above you is measured on, you stop being the manager who complains about the number and become the one they call while it's being built.</p>
    <div class="sheet">
      <h3>Worksheet: A plan that holds</h3>
      <p class="sheet-label">Before the year starts: &#9744; Baseline cleaned of one-time revenue &nbsp; &#9744; Capacity counts ramp and vacancies &nbsp; &#9744; Over-assignment chosen on purpose &nbsp; &#9744; Every quota explainable in one sentence</p>
    </div>
  </section>

  <section class="kit-ch" id="l-known">
    <h2>2. What do you want to be known for?</h2>
    <p>"Leadership" isn't a thing to be known for. Neither is "strategic." Pick something real: fixing bad territories, building a partner motion, getting new managers productive, selling into federal health.</p>
    <p>Pick one. You can add more later. It should be specific enough that somebody could say, "If you've got a problem with ______, call her."</p>
    <p>If your boss had one sentence to describe you to another leader today, what would it be? If you don't like the sentence, that's the work.</p>
  </section>

  <section class="kit-ch" id="l-receipts">
    <h2>3. Where are your receipts?</h2>
    <p>Nobody remembers your whole year. Keep receipts: date, what you changed, what happened.</p>
    <p>At the next level, "my team hit 112%" is good. Better is something you built that other people started using, or a rep you developed who now runs a team.</p>
  </section>

  <section class="kit-ch" id="l-believe">
    <h2>4. What do you believe that's actually yours?</h2>
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
    <h2>5. Build something other managers can borrow</h2>
    <p>If you do something well, write down how you do it and give it away. Your forecast call. Your first thirty days with a new rep. A hiring scorecard. Whatever people keep asking you about.</p>
    <p>It doesn't need to be pretty. It needs to be useful enough that another manager uses it next week.</p>
    <p>Then teach it. Thirty minutes at a leadership meeting, lunch with two newer managers, a session at kickoff. Teaching also tells you pretty quickly whether you actually know it.</p>
  </section>

  <section class="kit-ch" id="l-rooms">
    <h2>6. Get into the right rooms</h2>
    <p>Start close to the work: your boss, your boss's peers, and the leaders you depend on in partners, marketing, finance and customer success. Then go wider.</p>
    <p>The rooms you want are the ones where somebody is making decisions about your world without you: territories, headcount, your team's story, customers, industry stuff. Quota planning is the big one. How to walk in with the math: <a href="/notes/prove-the-quota-is-crazy/">quotabird.com/notes/prove-the-quota-is-crazy</a></p>
    <p>Usually the way in is simple: help somebody who's already in the room. Bring the template, the analysis, or the answer they keep getting asked for.</p>
  </section>

  <section class="kit-ch" id="l-behind">
    <h2>7. Bring people up behind you</h2>
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
    <p>I'm Mark. I spent six years leading federal partner sales teams at Amazon, after plenty of years carrying a number myself. If you've got something you need to defend to your VP, send it over and we can talk it through.</p>
    <p class="kit-cta-job">If this gets you into one better room, good enough.</p>
    <p class="kit-cta-terms">A free twenty-minute call, no pitch.</p>
    <div class="btn-row kit-cta-row">
      <a class="btn btn-primary btn-lg" id="leaderBook" href="https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&amp;utm_medium=leader&amp;utm_content=leader_cta" target="_blank" rel="noopener">Chat with Mark</a>
      <a class="btn btn-lg" href="https://www.linkedin.com/in/markflournoy/" target="_blank" rel="noopener">DM on LinkedIn</a>
    </div>
    <p class="kit-bridge">Used this with your team and found something ugly? That's <a href="/work-with-mark/">most of the stuff I help managers with</a>.</p>
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
      <p class="kit-hero-meta">__PAGES__ pages, prints on letter or A4. Seven short chapters and three worksheets.</p>
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


SELLER_PAGES = '8'   # set from the rendered PDF
# ────────────────────────────── THE SELLER'S FIELD KIT (/seller/) ──────────────────────────────
# Bottom rung of the ladder: carry the number. Not sales training; what a working seller reaches for in a bad week.
SELLER_BODY = '''
  <section class="kit-ch" id="s-start">
    <p>Some weeks the customer goes quiet, the number looks worse than it did Monday, and your boss wants an update you don't have. This is for those weeks.</p>
    <p>No sales methodology here. Just the handful of things I reached for when a quarter was going sideways, and a
      few I wish I'd reached for sooner. It starts with your number, because most bad weeks start there. <strong>Find the problem you have this week and start there.</strong></p>
    <div class="kit-start">
      <p class="kit-start-h">Having a bad week? Start here.</p>
      <ul>
        <li><a href="#s-where">Where your quota came from</a><span>Chapter 1</span></li>
        <li><a href="#s-crazy">Your quota feels crazy</a><span>Chapter 2</span></li>
        <li><a href="#s-crush">Tough number, now what?</a><span>Chapter 3</span></li>
        <li><a href="#s-deal">Is it a real deal?</a><span>Chapter 4</span></li>
        <li><a href="#s-sep30">Federal deal, year end</a><span>Chapter 12</span></li>
        <li><a href="#s-pipe">Not enough pipeline</a><span>Chapter 5</span></li>
        <li><a href="#s-big">One deal carries it</a><span>Chapter 6</span></li>
        <li><a href="#s-thread">Only one contact</a><span>Chapter 7</span></li>
        <li><a href="#s-disc">Discount request</a><span>Chapter 8</span></li>
        <li><a href="#s-quiet">Deal went quiet</a><span>Chapter 9</span></li>
        <li><a href="#s-behind">Behind the number</a><span>Chapter 10</span></li>
        <li><a href="#s-mgr">Your manager</a><span>Chapter 11</span></li>
      </ul>
    </div>
  </section>

  <section class="kit-ch" id="s-where">
    <h2>1. Where your quota came from</h2>
    <p>Most reps get a number and a kickoff slide and never find out how the number got made. You should, because you can't push back on a number you don't understand, and you can't plan against it either.</p>
    <p>At a cloud provider the number almost always starts with prior year revenue, with a growth rate on top. At Amazon that growth rate was usually set above the geo VP. By the time it got to your territory, nobody in your chain had actually picked the number. They just divided it up. SaaS works the same way with different words: last year's ARR or bookings, plus the growth the company promised its board.</p>
    <p>Every layer on the way down adds a little cushion. Most sales plans are over-assigned so a few misses don't sink the year, and a common planning rule of thumb is 20 to 30%. It's a big part of why only about half of AEs hit quota while the company still makes its number.</p>
    <p>Then find out what your number is measured in, because it changes everything:</p>
    <ul>
      <li><strong>New bookings or ACV.</strong> Contracts signed. Common in SaaS new business.</li>
      <li><strong>ARR or MRR growth.</strong> Your run rate at the end of the year against your run rate at the start.</li>
      <li><strong>Consumption revenue.</strong> What customers actually use, over prior year revenue. A committed contract only counts when the spend shows up.</li>
      <li><strong>The whole book.</strong> Renewals, expansion and new logos, all together.</li>
    </ul>
    <p>Read the comp plan like the contract it is: your on-target earnings, the split between base and variable, your rate (variable divided by quota, which is what every dollar you sell is really worth to you), accelerators above 100%, anything that caps or claws back, and the crediting rules. Who gets credit for a partner deal, a marketplace deal, or an account that moved in June?</p>
    <p>If you don't have the plan document, your territory list and prior year revenue for every account you own, ask for all three this week. That's a normal request, and a good manager won't read it as pushing back.</p>
    <div class="sheet">
      <h3>Worksheet: Your plan on one page</h3>
      <p class="sheet-meta">Year __________ &nbsp; <span class="sheet-tool">Online: quotabird.com/quota</span></p>
      <div class="mtable"><table class="ws"><thead><tr><th>Your plan</th><th>What it says</th></tr></thead><tbody>
        <tr><td>What the number is measured in</td><td></td></tr>
        <tr><td>Prior year revenue: your baseline</td><td></td></tr>
        <tr><td>The new number, and the growth it implies</td><td></td></tr>
        <tr><td>On-target earnings, and the base : variable split</td><td></td></tr>
        <tr><td>Your rate: variable ÷ quota</td><td></td></tr>
        <tr><td>Accelerators above 100%</td><td></td></tr>
        <tr><td>Caps, clawbacks, thresholds</td><td></td></tr>
        <tr><td>Crediting: partners, marketplace, moved accounts</td><td></td></tr>
      </tbody></table></div>
      <p class="sheet-foot">Anything blank goes on the list for your next one-on-one.</p>
    </div>
  </section>

  <section class="kit-ch" id="s-crazy">
    <h2>2. Is your quota crazy? Check it, then decide.</h2>
    <p>Telling your manager "this number is crazy" won't get you anywhere. Bring the math.</p>
    <p>Start with the ratio: quota divided by on-target earnings. For SaaS new bookings, 4 to 6 times is a useful working range, and Bridge Group's 2026 median was 4.6. For cloud consumption growth, the plans I've seen mostly land between 15 and 30 times, higher in strategic accounts. That's experience, not a published survey. <a href="/quota/">Quota Check</a> does it in ten seconds.</p>
    <p>Then build the case from what you actually know:</p>
    <ul>
      <li>Prior year revenue, minus anything that won't repeat: a one-time migration, a true-up, one giant deal that landed once.</li>
      <li>Your current run rate: this month's MRR times twelve.</li>
      <li>Committed contracts that ramp this year, and how much of them customers will really consume.</li>
      <li>Qualified pipeline at your real win rate.</li>
    </ul>
    <p>On a run-rate or whole-book number, add your run rate to the new pipeline you expect to win. On a bookings number, compare last year's bookings, adjusted for headcount, with pipeline at your win rate. Subtract the evidence from the new number. What's left is the gap. <a href="/quota-case/">Quota Case</a> does the arithmetic.</p>
    <p>Now be honest about what can move. The growth rate almost never does. It was set above your manager's boss, and arguing with it just makes you the rep who argued. What can move: the baseline, if it includes revenue that won't repeat; the territory, if accounts moved after the number was set; ramp time, if you're new; and crediting. Pick the one that matters most and ask for that. If you ask for five things, it sounds like complaining.</p>
    <p>Then say it plainly: "Here's last year, here's what we're running at, here's what's committed. That leaves a $1.8M gap I can't explain. What assumption am I missing?"</p>
    <p>Sometimes there's a real answer: a new program, a big renewal, a partner with names attached. Then the number is hard but fair. Accept it, get anything that moved in writing, and go to chapter 3.</p>
    <p>The best time to shape your quota was last year, while somebody still had the planning spreadsheet open. The next best time is now. Every week you wait, the number gets harder to move and the year gets shorter.</p>
    <div class="sheet">
      <h3>Worksheet: The gap</h3>
      <p class="sheet-meta">Date __________ &nbsp; <span class="sheet-tool">Online: quotabird.com/quota-case</span></p>
      <div class="mtable"><table class="ws"><thead><tr><th>The evidence</th><th>$</th></tr></thead><tbody>
        <tr><td>Prior year revenue</td><td></td></tr>
        <tr><td>Minus one-time revenue in it</td><td></td></tr>
        <tr><td>Current run rate (MRR × 12)</td><td></td></tr>
        <tr><td>Committed contracts landing this year</td><td></td></tr>
        <tr><td>Qualified pipeline × win rate</td><td></td></tr>
        <tr><td>The new number</td><td></td></tr>
        <tr><td><strong>The gap</strong></td><td></td></tr>
      </tbody></table></div>
      <p class="sheet-label">My one ask, and who I'm asking</p><div class="lines l2"></div>
    </div>
  </section>

  <section class="kit-ch" id="s-crush">
    <h2>3. It's a tough number. Crush it anyway.</h2>
    <p>Once the number is set, every week you spend arguing about it is a week you're not building pipeline. The reps I've seen hit tough numbers stopped arguing early and went to work on the gap.</p>
    <p>Turn the gap into pipeline: divide it by your win rate. A $1.8M gap at a 25% win rate is $7.2M of new qualified pipeline. That's the number to plan around.</p>
    <p>It comes from two places, and most years you need both:</p>
    <ul>
      <li><strong>Growth in accounts you already have.</strong> New workloads, migrations, expansion, renewals with uplift, the second team at a customer who loves the first. Usually faster, because they already trust you.</li>
      <li><strong>Net-new accounts.</strong> Slower, and the only place the big surprises come from.</li>
    </ul>
    <p>Put names next to both. Five existing accounts with a dollar figure and a reason. Five net-new accounts with a reason they'd buy this year. If you can't name them, you don't have a plan yet.</p>
    <p>Then start early. On a run-rate number, when a workload lands matters as much as how big it is. A workload that lands in March runs for ten months this year. The same workload in October runs for three. Pipeline you create in Q1 is worth about three times the same pipeline in Q4.</p>
    <p>Once a week, look at three numbers: the gap, the new pipeline you created, and your run rate. If the gap isn't shrinking, change what you're working on. Changing the forecast won't close it.</p>
    <div class="sheet">
      <h3>Worksheet: Filling the gap</h3>
      <p class="sheet-meta">Gap __________ ÷ win rate ______ = new pipeline needed __________</p>
      <div class="mtable"><table class="ws"><thead><tr><th>Existing account</th><th>What they'd add</th><th>$</th><th>By when</th></tr></thead><tbody>
        <tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr>
      </tbody></table></div>
      <div class="mtable"><table class="ws"><thead><tr><th>Net-new account</th><th>Why this year</th><th>$</th><th>First meeting</th></tr></thead><tbody>
        <tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr>
      </tbody></table></div>
    </div>
  </section>

  <section class="kit-ch" id="s-deal">
    <h2>4. Is this actually a deal?</h2>
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
    <h2>5. You don't have enough pipeline</h2>
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
    <h2>6. Your biggest deal is carrying the quarter</h2>
    <p>Write your forecast without it. That's closer to your real plan, and if it doesn't work, you need a second way to the number now, before the big one slips.</p>
    <p>Then look hard at the big one. Who set the close date, you or the customer? What still has to happen? Two smaller deals you can move are often better than one giant deal you're praying over.</p>
  </section>

  <section class="kit-ch" id="s-thread">
    <h2>7. You're single-threaded</h2>
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
    <h2>8. The customer wants a discount</h2>
    <p>A discount should buy you something. What comes back? A signature date, more scope, a longer term, a reference you can
      use. And remember it comes out of your commission at the same rate it comes off the price.</p>
    <p>Before you ask your manager to approve it, ask whether the problem is the price or the deal. A discount fixes price. If the real problem is power, path or timing, it just makes the deal cheaper.</p>
  </section>

  <section class="kit-ch" id="s-quiet">
    <h2>9. The deal has gone quiet</h2>
    <p>Busy and stalled look alike for about a week. Busy looks like short replies and moved meetings. Stalled looks like
      no replies and nobody else at the customer you can call.</p>
    <p>Send one short note that's easy to answer: "Is this still a priority for this quarter, or should I check back in
      January?" A no is useful. Silence for two weeks after that is an answer too.</p>
  </section>

  <section class="kit-ch" id="s-behind">
    <h2>10. You're behind the number</h2>
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
    <h2>11. Don't make your manager guess</h2>
    <p>Good managers don't need every detail. They need to know what changed, what might go wrong, and where you need help.
      "Still feeling good" isn't an update. "Procurement moved the date two weeks, Sarah told me Thursday, and I need you to
      call her VP" is an update.</p>
    <p>Before the forecast call, try to break your own deals the way your manager will. Which of the five from chapter 4
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
  <section class="kit-ch" id="s-sep30">
    <h2>12. Working back from September 30</h2>
    <p>The federal fiscal year ends September 30. Most one-year money that isn't obligated by then can't be used for new work, which is why so many federal deals close in September, and why so many slip into October.</p>
    <p>The date that matters usually isn't September 30. It's the contracting office's cutoff for getting a package in the door, and many offices set it in the summer so they have time to award. Ask your customer for their office's year-end dates in the spring, not in August.</p>
    <p>Then work backward from that cutoff. Before the package goes in, the customer needs the requirement written down, the money identified on a specific line, a way to buy it (a contract vehicle they can use, a task order on an existing contract, or a marketplace purchase), and the approvals lined up. Each of those takes weeks, and none of them is your job, which is exactly why they need dates and names on them.</p>
    <p>If the year starts under a continuing resolution, new starts are often on hold until a budget passes. Plan for a slow first quarter and build pipeline anyway.</p>
    <p>Put the dates on one page with the customer. If they won't put dates on it, it isn't a September deal yet. Run it through Deal Check.</p>
    <div class="sheet">
      <h3>Worksheet: Working back from September 30</h3>
      <p class="sheet-meta">Deal __________________ &nbsp; Contracting office cutoff __________ &nbsp; <span class="sheet-tool">Online: quotabird.com/deal</span></p>
      <div class="mtable"><table class="ws"><thead><tr><th>Step, latest first</th><th>Date</th><th>Customer owner</th><th>Done</th></tr></thead><tbody>
        <tr><td>Award signed</td><td></td><td></td><td></td></tr>
        <tr><td>Package in to the contracting office</td><td></td><td></td><td></td></tr>
        <tr><td>Requirement written down</td><td></td><td></td><td></td></tr>
        <tr><td>Money identified on a specific line</td><td></td><td></td><td></td></tr>
        <tr><td>Buying route agreed</td><td></td><td></td><td></td></tr>
        <tr><td>Approvals lined up</td><td></td><td></td><td></td></tr>
        <tr><td>Technical evaluation finished</td><td></td><td></td><td></td></tr>
      </tbody></table></div>
      <p class="sheet-foot">Any blank date is the next conversation with the customer.</p>
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
    <p class="kit-bridge">Used this with your team and found something ugly? That's <a href="/work-with-mark/">most of the stuff I help managers with</a>.</p>
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
      <p class="kit-hero-meta">__PAGES__ pages, prints on letter or A4. Twelve short chapters and nine worksheets.</p>
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


# ────────────────────────────── /ask/ now redirects to Work with Mark (Nov 6) ───────────────────────
os.makedirs('ask', exist_ok=True)
open('ask/index.html', 'w').write('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><title>Work with Mark | QuotaBird</title>\n<meta name="robots" content="noindex"><link rel="canonical" href="https://quotabird.com/work-with-mark/">\n<meta http-equiv="refresh" content="0; url=/work-with-mark/#ask"></head>\n<body><p><a href="/work-with-mark/#ask">Working with Mark, and the free twenty minutes, are here.</a></p></body></html>\n')

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
  <p>At a company the size of Amazon, Microsoft or Google, your quota is the last step of a long chain. It usually runs in
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
  <p>Planners over-assign. Sales plans are usually over-assigned. A common planning rule of thumb is 20 to 30% more quota than the company needs, sometimes more in enterprise, to cover the reps who miss, leave or ramp slowly. If your number feels like it's
    carrying somebody else's, it probably is.</p>

  <h2>Consumption plans count what customers run</h2>
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
    how your multiple compares, <a href="/quota-case/">Quota Case</a> shows the gap between last year and this year, and
    <a href="/notes/prove-the-quota-is-crazy/">Your quota is crazy. Now prove it.</a> covers the conversation for managers, and <a href="/notes/push-back-as-a-rep/">this one</a> is for reps. If the
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
# Plain stat cards: value, label. One card system with the rest of the site; the headline stat gets the emphasis container.
def stat(value, label, emph=False):
    return f'<div class="stat{" emph" if emph else ""}"><div class="stat-value">{value}</div><div class="stat-label">{label}</div></div>'
def stat_grid(cards):
    return '<div class="stat-grid">' + ''.join(stat(*c) for c in cards) + '</div>'
_num = note_head('Quota by the Numbers', 'Sales quota and comp benchmarks with sources: how many reps hit quota, median quota and OTE, quota-to-OTE, pay mix, ramp, over-assignment, accelerators, and what reps at Amazon Web Services and Microsoft report.', 'https://quotabird.com/quota-by-the-numbers/') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note numbers">
  <span class="overline">Understand it</span>
  <h1>Quota by the numbers</h1>
  <p class="dek">Who hits quota, what it pays, and how the number gets built.</p>
  <p class="fine">Every figure here is published data, a common rule of thumb, or a QuotaBird working range. <a href="/methodology/">How QuotaBird's numbers work</a> says which, and why.</p>

  <h2>Who hits quota</h2>
  ''' + stat_grid([('48%', 'of AEs hit 100% of quota in 2026', True), ('51%', 'did in 2024'), ('66%', 'did in 2022'),
                   ('42%', 'of all AEs say they hit quota (RepVue, Sept. 2026)'), ('41%', 'of enterprise AEs say they did (RepVue, Sept. 2026)'), ('46%', 'of federal AEs say they did (RepVue, Sept. 2026)'),
                   ('45%', 'of SLED AEs say they did (RepVue, Sept. 2026)'), ('43.8%', 'of sellers hit quota across 272 software companies (RepVue Cloud Sales Index, Q4 2025)')]) + '''
  <p class="fine">Bridge Group 2026 (158 B2B companies) for the first three; RepVue, September 2026, self-reported, for the next four; RepVue Cloud Sales Index, Q4 2025, for the last one. That index covers software sellers, not cloud-provider consumption sellers.</p>
  <p>Two different numbers both get called attainment: the share of reps who hit 100%, and the average share of quota reps
    reach. They aren't the same number, and people swap them in meetings.</p>

  <h2>What the number is and what it pays</h2>
  ''' + stat_grid([('$960K', 'median AE quota, 158 B2B companies'), ('$200K', 'median AE OTE, same sample'), ('4.6×', 'quota to OTE, up from 4.2× in 2024', True),
                   ('2.4%', 'quota growth per year'), ('4.9%', 'OTE growth per year'), ('53:47', 'base to variable')]) + '''
  <p class="fine">Bridge Group 2026 and 2024 SaaS AE reports.</p>
  <p>Pay has grown about twice as fast as quota for a decade, and the share of reps hitting quota fell by a quarter in four
    years. <a href="/quota/">Quota Check</a> puts your multiple next to these.</p>

  <h2>At the big cloud providers</h2>
  ''' + stat_grid([('$280K', 'Amazon Web Services Account Manager OTE'), ('$150K', 'Amazon Web Services Account Manager base'), ('54:46', 'Amazon Web Services Account Manager pay mix'),
                   ('64%', 'of Amazon Web Services Account Managers say they hit quota'), ('56%', 'of Microsoft Enterprise AEs say they did'), ('67%', 'of Microsoft SLED AEs say they did')]) + '''
  <p class="fine">RepVue, self-reported by current and former employees, 2026.</p>
  <p>These are reps rating their own employers, so treat them as a rough read. Many cloud-provider quotas are measured in consumption growth, which is why their multiples run far higher than SaaS; <a href="/how-quotas-get-built/">here's why</a>.</p>

  <h2>How plans get built</h2>
  ''' + stat_grid([('20-30%', 'over-assignment, a common planning rule of thumb'), ('6.2 mo', 'for a new AE to ramp'),
                   ('1.5-2×', 'typical first accelerator above quota'), ('80%', 'of plans use accelerators')]) + '''
  <p class="fine">Mostly Metrics on over-assignment; Bridge Group 2026 on ramp; accelerator ranges from 2026 comp plan surveys (Everstage, Prowi, QuotaPath, CaptivateIQ).</p>

  <h2>Sources</h2>
  <ul class="sources">
    <li><a href="https://blog.bridgegroupinc.com/2026-ae-compensation-quota-ai-metrics" rel="noopener">Bridge Group, AE Models, Motions and Metrics, 2026</a></li>
    <li><a href="https://blog.bridgegroupinc.com/2024-ae-metrics-compensation-benchmark" rel="noopener">Bridge Group, SaaS AE Metrics and Compensation, 2024</a></li>
    <li><a href="https://www.repvue.com/salaries/account-executive" rel="noopener">RepVue, Account Executive salaries and attainment, 2026</a></li>
    <li><a href="https://www.repvue.com/blog/sales-salary-guide" rel="noopener">RepVue, Sales Salary Guide, 2026</a></li>
    <li><a href="https://www.repvue.com/companies/Amazonwebservices/salaries" rel="noopener">RepVue, Amazon Web Services salaries</a></li>
    <li><a href="https://www.repvue.com/companies/Microsoft/salaries" rel="noopener">RepVue, Microsoft salaries</a></li>
    <li><a href="https://www.repvue.com/cloud-index/2025/Q4" rel="noopener">RepVue Cloud Sales Index, Q4 2025</a></li>
    <li><a href="https://www.mostlymetrics.com/p/your-complete-guide-to-annual-planning" rel="noopener">Mostly Metrics, Annual Planning: Building Sales Capacity</a></li>
    <li><a href="https://learn.microsoft.com/en-us/partner-center/referrals/partner-reported-azure-consumed-revenue" rel="noopener">Microsoft Learn, Partner Reported Azure Consumed Revenue</a></li>
    <li><a href="https://www.prowi.io/en/post/commission-accelerators-guide" rel="noopener">Prowi, Commission accelerators</a></li>
  </ul>
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL
assert '—' not in _num and '–' not in _num
os.makedirs('quota-by-the-numbers', exist_ok=True)
open('quota-by-the-numbers/index.html', 'w').write(_num)


# ────────────────────────────── METHODOLOGY (/methodology/) ───────────────────────────
# How every number on the site is sourced, what kind of evidence it is, and when it was checked. Written to be quotable.
METHOD_REVIEWED, METHOD_DATE = 'November 2026', '2026-11-01'
_method_sources = [
    ('Bridge Group, AE Models, Motions and Metrics, 2026', 'https://blog.bridgegroupinc.com/2026-ae-compensation-quota-ai-metrics'),
    ('Bridge Group, SaaS AE Metrics and Compensation, 2024', 'https://blog.bridgegroupinc.com/2024-ae-metrics-compensation-benchmark'),
    ('RepVue Cloud Sales Index, Q4 2025', 'https://www.repvue.com/cloud-index/2025/Q4'),
    ('RepVue, Sales Salary Guide, 2026', 'https://www.repvue.com/blog/sales-salary-guide'),
    ('RepVue, Amazon Web Services salaries', 'https://www.repvue.com/companies/Amazonwebservices/salaries'),
    ('QuotaPath, Quota:OTE ratio', 'https://www.quotapath.com/blog/calculating-otes/'),
    ('Mostly Metrics, Annual Planning: Building Sales Capacity', 'https://www.mostlymetrics.com/p/your-complete-guide-to-annual-planning'),
    ('Microsoft Learn, Partner Reported Azure Consumed Revenue', 'https://learn.microsoft.com/en-us/partner-center/referrals/partner-reported-azure-consumed-revenue'),
]
_method_ld = json.dumps({"@context": "https://schema.org", "@type": "Dataset",
    "name": "QuotaBird quota-to-OTE working ranges",
    "description": "Quota-to-OTE ranges for sales quotas measured on bookings, run rate (consumption growth) and whole book, with the evidence type, derivation and sources for each.",
    "url": "https://quotabird.com/methodology/", "creator": {"@type": "Person", "name": "Mark Flournoy", "url": "https://quotabird.com/about/"},
    "dateModified": METHOD_DATE, "isAccessibleForFree": True,
    "variableMeasured": ["Quota to OTE ratio", "Implied commission rate on quota"],
    "citation": [u for _, u in _method_sources]})
def _mt(head, rows):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tb = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="mtable"><table class="ws"><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'
_method = note_head("How QuotaBird's Numbers Work", "Where every range and benchmark on QuotaBird comes from: published data, common rules of thumb and QuotaBird working ranges, how each is derived, and when it was last checked.", 'https://quotabird.com/methodology/') + f'''<script type="application/ld+json">{_method_ld}</script>
</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note numbers">
  <span class="overline">Methodology</span>
  <h1>How QuotaBird's numbers work</h1>
  <p class="dek">Where every range and benchmark on QuotaBird comes from, how strong the evidence is, and when it was last checked.</p>
  <p class="fine">Last reviewed {METHOD_REVIEWED}. Maintained by Mark Flournoy.</p>

  <h2>Three kinds of numbers</h2>
  <p>Every number on QuotaBird is one of three kinds, and the site says which.</p>
  <ul>
    <li><strong>Published data.</strong> A figure from a named study with a sample and a date, such as Bridge Group's 2026 report on 158 B2B companies or RepVue's Cloud Sales Index. QuotaBird quotes these as reported and links the source.</li>
    <li><strong>Common rule of thumb.</strong> A planning convention practitioners widely use, such as 20 to 30% over-assignment or accelerators of 1.5 to 2×. These are useful defaults, not measured averages.</li>
    <li><strong>QuotaBird working range.</strong> A range derived from how comp plans are built and from plans Mark Flournoy has seen across cloud providers, SaaS companies and their partners. No public survey covers these, and QuotaBird says so rather than inventing one.</li>
  </ul>

  <h2>Quota-to-OTE working ranges</h2>
  <p>Quota Check divides quota by on-target earnings (OTE) and compares the multiple with the range for what the quota is measured on.</p>
  ''' + _mt(['Verdict', 'Bookings (new ARR or ACV)', 'Run rate (consumption growth)', 'Whole book'], [
      ['Low', 'under 3×', 'under 8×', 'under 20×'],
      ['Favorable', '3 to 4×', '8 to 15×', '20 to 40×'],
      ['Standard', '4 to 6×', '15 to 30×', '40 to 80×'],
      ['A stretch', '6 to 8×', '30 to 45×', '80 to 120×'],
      ['Aggressive', '8 to 12×', '45 to 60×', '120 to 160×'],
      ['Crazy', 'over 12×', 'over 60×', 'over 160×'],
      ['<strong>Evidence</strong>', 'Working range built on published data', 'QuotaBird working range', 'QuotaBird working range']]) + '''

  <h3>Where the bookings range comes from</h3>
  <p>Bridge Group's 2026 study of 158 B2B companies reports a median quota-to-OTE of 4.6×. Its 2024 study of more than 170 B2B SaaS companies reported a median of 4.2×, with the middle half of companies between 3.2× and 4.8×. QuotaPath describes about 5× as the standard it observes across SaaS plans. QuotaBird's standard band of 4 to 6× covers that published middle and leaves room for enterprise roles, which run higher.</p>

  <h3>Where the run-rate and whole-book ranges come from</h3>
  <p>One identity ties quota, pay and commission rate together: quota ÷ OTE equals the variable share of OTE divided by the commission rate at 100% attainment. It follows from the definition of a commission rate, so it holds for any plan.</p>
  <p>With a 46% variable share, the 54:46 pay mix RepVue reports for Amazon Web Services account managers:</p>
  ''' + _mt(['Measured on', 'Typical rate on the number', 'Implied quota ÷ OTE'], [
      ['Bookings', 'about 8 to 12%', 'about 4 to 6×'],
      ['Run rate (consumption growth)', 'about 1.5 to 3%', 'about 15 to 30×'],
      ['Whole book', 'about 0.6 to 1.2%', 'about 40 to 80×']]) + '''
  <p>The bookings rates are published: summaries of Bridge Group's 2024 report put the median commission rate at 11.5%. The consumption and whole-book rates come from plans Mark has seen at cloud providers and their partners, not from a survey. Quota Check shows your own implied rate (variable ÷ quota), so you can compare your plan with these ranges directly.</p>

  <h2>Where the other numbers come from</h2>
  ''' + _mt(['Number', 'Kind', 'Source'], [
      ['48% of AEs hit quota in 2026 (51% in 2024, 66% in 2022)', 'Published data', 'Bridge Group, 2026 and 2024'],
      ['$960K median AE quota, $200K median OTE, 4.6× quota to OTE', 'Published data', 'Bridge Group, 2026, 158 B2B companies'],
      ['6.2 months for a new AE to ramp', 'Published data', 'Bridge Group, 2026'],
      ['Attainment and pay for all, enterprise, federal and SLED AEs, and Amazon Web Services and Microsoft roles', 'Published data, self-reported', 'RepVue, September 2026 snapshot'],
      ['43.8% of sellers hit quota across 272 software companies', 'Published data', 'RepVue Cloud Sales Index, Q4 2025. It covers software sellers, not cloud-provider consumption sellers.'],
      ['20 to 30% over-assignment', 'Common rule of thumb', 'Mostly Metrics and planning practice'],
      ['1.5 to 2× accelerators above quota', 'Common rule of thumb', 'QuotaPath and comp plan guides'],
      ['Coverage needed = 1 ÷ win rate', 'Arithmetic', 'No source needed'],
      ['Discount bands (5, 15 and 25%)', 'QuotaBird working range', 'Practitioner experience across real deals']]) + '''
  <p>Two different numbers both get called attainment: the share of reps who reach 100% of quota, and the average share of quota reps reach. Bridge Group and RepVue report the first. QuotaBird labels which one it means.</p>

  <h2>How the tools calculate</h2>
  <ul>
    <li><strong>Quota Check:</strong> quota ÷ (base + variable), judged against the range for what the quota is measured on. Implied rate = variable ÷ quota.</li>
    <li><strong>Quota Case:</strong> on a run-rate or whole-book number, the evidence is the current run rate plus new pipeline × win rate. On a bookings number, it is the stronger of last year's bookings (minus one-time deals, scaled by ramped headcount) and pipeline × win rate. The gap is the quota minus the evidence, and the new pipeline to close it is the gap ÷ win rate.</li>
    <li><strong>Pipeline Check:</strong> coverage needed = 1 ÷ win rate, on unweighted pipeline (full deal values). A 20% win rate needs 5× coverage; 3× assumes a win rate of about 33%. Weighted pipeline (each deal times its CRM stage probability) is compared straight to the remaining target, so 1.0× is enough; weighted ÷ unweighted is the win rate the CRM's weights assume, shown next to the real one. If the biggest deal slips, the same math runs without it.</li>
    <li><strong>Discount Check:</strong> commission lost = list price × discount × your rate. Margin after the discount = 1 minus cost ÷ discounted price, because cost doesn't fall with the price.</li>
    <li><strong>Pay Check:</strong> variable paid = variable × attainment up to where the accelerator starts, plus variable × each point past it × the accelerator rate, limited by any cap, and zero below any threshold. Total pay = base + variable paid.</li>
    <li><strong>Offer Check:</strong> a normal year = base + variable × the attainment you enter. Year one also counts the ramp: during ramp months you earn the guarantee if there is one, and otherwise half your normal attainment, an assumption the page states.</li>
    <li><strong>Commission Check:</strong> your credit = deal × your share of the credit × any product multiplier. Commission = credit × your rate, minus the withholding percentage you enter. A planning estimate, not tax advice.</li>
    <li><strong>Commit Check:</strong> projected spend = spent so far + current monthly spend × months left. The monthly spend needed = (commit minus spent so far) ÷ months left.</li>
    <li><strong>The question checks</strong> (Deal, Rep, Territory, Account, Competition, Risk, Partner, Talent Review, Brief, Comp Plan and Federal Readiness) weight five yes, sort of or no answers into a score. They are structured judgment, not statistics.</li>
  </ul>

  <h2>What QuotaBird doesn't model</h2>
  <p>Crediting rules, marketplace fees, co-sell quota retirement and multi-year crediting differ by company and change often, so QuotaBird doesn't guess at them. Check your own plan document.</p>

  <h2>Updates and corrections</h2>
  <p>Published figures are rechecked when Bridge Group releases a new report and each quarter for RepVue. If a number looks wrong, or your plan sits well outside a working range, <a href="mailto:mark@quotabird.com">tell Mark</a>. The ranges change when the evidence does.</p>

  <h2>Sources</h2>
  <ul class="sources">
''' + ''.join(f'    <li><a href="{u}" rel="noopener">{n}</a></li>\n' for n, u in _method_sources) + '''  </ul>
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL
assert '—' not in _method and '–' not in _method
os.makedirs('methodology', exist_ok=True)
open('methodology/index.html', 'w').write(_method)


# ────────────────────────────── PRIVACY (/privacy/) ───────────────────────────
PRIVACY_UPDATED = 'October 2026'
_privacy = note_head('Privacy', 'What QuotaBird counts, what stays in your browser, and how to clear it. No accounts, no ads, and the numbers you type are never sent anywhere.', 'https://quotabird.com/privacy/') + f'''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note">
  <span class="overline">QuotaBird</span>
  <h1>Privacy</h1>
  <p class="dek">What QuotaBird counts, what stays in your browser, and how to clear it.</p>
  <p class="fine">Last updated {PRIVACY_UPDATED}. Questions: <a href="mailto:mark@quotabird.com">mark@quotabird.com</a>.</p>

  <h2>The short version</h2>
  <p>QuotaBird has no accounts, no ads and no sign-up. The numbers and answers you type into the tools are worked out in your browser and never sent to QuotaBird or anyone else. QuotaBird counts page views and which tools get used, so it knows what's worth improving.</p>

  <h2>What QuotaBird counts</h2>
  <p>QuotaBird uses Google Analytics 4 to count visits. Google Analytics records the pages you visit and the usual technical details that come with any visit, such as your browser, device type, approximate location and the site that sent you. It sets cookies in your browser to tell visits apart.</p>
  <p>QuotaBird also counts a few named events, with no details attached: that someone used a tool, finished a check, shared a result, copied a note to Mark, or downloaded a Field Kit. Those events never include the numbers or answers you entered.</p>
  <p>To stop Google Analytics, block its cookies in your browser settings or use Google's <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">opt-out add-on</a>. Google's handling of that data is covered by <a href="https://policies.google.com/privacy" rel="noopener">Google's privacy policy</a>.</p>

  <h2>What stays in your browser</h2>
  <ul>
    <li><strong>Your numbers and answers.</strong> Every calculation happens on your device. Nothing you type goes to a server or a CRM.</li>
    <li><strong>A pipeline export.</strong> If you load a CSV into Pipeline Check, it's read in your browser to count the deals. The file is never uploaded, and nothing in it is kept after you leave the page.</li>
    <li><strong>Base, variable and quota.</strong> If you type them into one tool, your browser remembers them so the next tool can fill them in. They're stored only in your browser's local storage, on your device. Use "Clear them" on any tool that shows them, or clear your browser's site data for quotabird.com.</li>
  </ul>

  <h2>Shared links</h2>
  <p>When you share a result, the numbers or answers ride along in the link itself, after the # sign. That part of a link isn't sent to QuotaBird's server or to Google Analytics, but anyone you send the link to can see what's in it. Share accordingly.</p>

  <h2>Other services you might click through to</h2>
  <ul>
    <li><strong>Booking a call</strong> opens Calendly, which collects what you enter there under its own privacy policy.</li>
    <li><strong>Sending a note on LinkedIn</strong> happens on LinkedIn, under its own privacy policy. The DM button only copies a note to your clipboard.</li>
    <li><strong>Email</strong> to mark@quotabird.com is read by Mark and treated as confidential. Please don't send classified, export-controlled or restricted information. The details are on the <a href="/work-with-mark/">Work with Mark</a> page.</li>
  </ul>

  <h2>What QuotaBird doesn't do</h2>
  <p>No accounts, no advertising, no selling or renting data, and no AI processing of anything you type. The Field Kits are plain PDF files.</p>

  <h2>Changes and questions</h2>
  <p>If this page changes, the date at the top changes with it. Questions about privacy or security go to <a href="mailto:mark@quotabird.com">mark@quotabird.com</a>.</p>
</article>

<section class="band" id="about"></section>

''' + NOTE_TAIL
assert '—' not in _privacy and '–' not in _privacy
os.makedirs('privacy', exist_ok=True)
open('privacy/index.html', 'w').write(_privacy)


# ────────────────────────────── WORK WITH MARK and FEDERAL ───────────────────────────
# One Mark, one front door. The tools stay free and ungated; this is the paid version of the same idea.
CAL = 'https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&utm_medium='
def _mail(subject): return 'mailto:mark@quotabird.com?subject=' + subject.replace(' ', '%20')
def offer_card(oid, name, price, body, gets, cta, subject, note=''):
    li = ''.join(f'<li>{g}</li>' for g in gets)
    return f'''  <section class="offer" id="{oid}">
    <h2>{name}</h2>
    <p class="price">{price}</p>
    <p>{body}</p>
    <ul>{li}</ul>
    {f'<p class="fine">{note}</p>' if note else ''}
    <p class="offer-cta"><a class="btn btn-tonal" href="{_mail(subject)}">{cta}</a></p>
  </section>
'''
def ask_block(src):
    return f'''  <section class="offer offer-ask" id="ask">
    <h2>Not sure you need any of this?</h2>
    <p>Grab 20 minutes. Tell me what you're wrestling with and I'll tell you what I think. If I don't think you need my help, I'll tell you that too.</p>
    <p>Pick a time and add one line about what's going on. I read it before we talk. No deck needed.</p>
    <p class="offer-cta"><a class="btn btn-primary" href="{CAL}{src}&utm_content=page" target="_blank" rel="noopener">Grab 20 minutes</a> <a class="offer-alt" href="https://www.linkedin.com/in/markflournoy/" rel="noopener">or message me on LinkedIn</a></p>
  </section>
'''
PROOF = '''  <h2>The specifics</h2>
  <p>In the Marine Corps I did government technology and acquisition work, including as a COTR, so I've sat on the buying side. Then about fifteen years in enterprise technology sales at Red Hat, F5 and Amazon. At Amazon I was a Manager of Managers leading federal partner sales teams covering Defense, Federal Civilian, Federal Financial and National Security: about 25 partner sales managers working toward a shared goal above $1B. Along the way I closed a $54M four-year committed cloud agreement with a major DoD systems integrator, and made President's Circle at F5.</p>
  <p>Seller, manager, government guy, partner guy. And I built these tools, which is probably the best evidence of how I think about these problems.</p>
'''
def offer_plain(oid, name, price, paras, cta_label, subject):
    body = ''.join(f'<p>{p}</p>' for p in paras)
    return f'''  <section class="offer" id="{oid}">
    <h3>{name}</h3>
    <p class="price">{price}</p>
    {body}
    <p class="offer-cta"><a class="btn btn-tonal" href="{_mail(subject)}">{cta_label}</a></p>
  </section>
'''
def ask_plain(src):
    return f'''  <section class="offer offer-ask" id="ask">
    <h2>Not sure yet?</h2>
    <p>Grab 20 minutes and tell me what's going on. If I don't think you need help, I'll say so. When you pick a time, add a line about the problem so I can read it before we talk.</p>
    <p class="offer-cta"><a class="btn btn-primary" href="{CAL}{src}&utm_content=page" target="_blank" rel="noopener">Grab 20 minutes</a> <a class="offer-alt" href="https://www.linkedin.com/in/markflournoy/" rel="noopener">or message me on LinkedIn</a></p>
  </section>
'''
CONF_BLOCK = '''  <h2>Confidentiality</h2>
  <p>I treat what you share with me as confidential and don't share company, deal, personnel or customer-specific information without your permission. For company engagements, I'm happy to sign a reasonable NDA. Please don't send me classified information, export-controlled material, government-sensitive information you aren't authorized to share, or anything your employer's policies prohibit you from sharing.</p>
'''
def talk_cta(src, extra=''):
    return f'''  <p class="offer-cta"><a class="btn btn-primary" href="{CAL}{src}&utm_content=page" target="_blank" rel="noopener">Grab 20 minutes</a> <a class="offer-alt" href="https://www.linkedin.com/in/markflournoy/" rel="noopener">or message me on LinkedIn</a></p>
  <p class="how-note">It's free. Pick a time and add a line about what's going on so I can read it before we talk. If you want more help after that, we can talk about what that looks like on the call.{extra}</p>
'''
_work = note_head('Work with Mark', "Need a second opinion on a deal, quota, territory, pipeline or comp plan? Grab 20 minutes with Mark and he'll tell you what he thinks. The tools stay free.", 'https://quotabird.com/work-with-mark/') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note work">
  <span class="overline">Work with Mark</span>
  <h1>Need a second opinion?</h1>
  <div class="who">
    <img src="/mark.jpg" alt="Mark Flournoy" width="120" height="120" loading="lazy" decoding="async">
    <p>I built QuotaBird because most sales problems don't need another methodology. They usually need somebody to look at the facts and ask a few uncomfortable questions.</p>
    <p>I've spent a long time around this stuff. I carried a number, managed sellers, led federal partner sales teams at Amazon, and before that spent 20 years in the Marine Corps. I've been the seller, the manager, the partner and the government customer.</p>
  </div>
  <p>I'm retired now, so I get to be selective about what I work on. I still like sales problems, especially the ones where something doesn't quite add up.</p>
  <p>If you want me to take a look at a deal, quota, territory, pipeline, comp plan or whatever else is bothering you, grab 20 minutes and tell me about it. I'll tell you what I think.</p>
''' + talk_cta('work') + '''
  <h2>If you want more help</h2>
  <p>Sometimes 20 minutes is enough. When it isn't, there are a few ways I usually help.</p>
  <ul>
    <li><strong>A working session on one problem.</strong> A deal, a quota, a territory, a pipeline, a comp plan, a QBR or a job offer. We work through it together and I write up what I think, what I'd push back on and what I'd do next.</li>
    <li><strong>Manager Wingman.</strong> For sales managers who want somebody outside the company to look at what they're seeing, a couple of times a month, for as long as it's useful.</li>
    <li><strong>A session with your team.</strong> The same kind of look across a whole team's pipeline, quotas, territories or forecast, virtually or as part of an offsite.</li>
  </ul>
  <p>If you're trying to figure out whether there's a real federal business in front of you, that has <a href="/federal/">its own page</a>.</p>

''' + CONF_BLOCK + '''
  <h2>A few specifics</h2>
  <p>At Amazon I was a Manager of Managers leading federal partner sales teams covering Defense, Federal Civilian, Federal Financial and National Security, about 25 partner sales managers working toward a shared goal of more than $1B. I closed a $54M four-year cloud agreement with a major DoD systems integrator. Before Amazon I was at F5, where I made President's Circle, and Red Hat. In the Marine Corps I worked on the government side of technology buying, including as a COTR. People I've helped have worked at Amazon, Microsoft, Google, Oracle and a lot of smaller companies you've probably never heard of.</p>
  <section class="offer offer-ask" id="ask">
    <h2>Grab 20 minutes</h2>
    <p>Tell me what you're wrestling with and I'll tell you what I think. If I don't think you need help, I'll say so.</p>
    <p class="offer-cta"><a class="btn btn-primary" href="''' + CAL + '''work&utm_content=bottom" target="_blank" rel="noopener">Pick a time</a></p>
  </section>
</article>

''' + NOTE_TAIL
_fed = note_head('Federal GTM', "Trying to figure out whether there's a real federal business? Grab 20 minutes with Mark, who led federal partner sales teams at Amazon, and he'll tell you what he thinks.", 'https://quotabird.com/federal/') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note work">
  <span class="overline">Federal GTM</span>
  <h1>You think you have a federal business? Let's find out.</h1>
  <p>A federal customer who likes your product is a good start. It turns into a business when there's money for it, a legal way to buy it and a reason to do it this year. Most of the federal plans I've seen were built on the first part and assumed the rest.</p>
  <p>I spent 20 years in the Marine Corps, some of it on the government side of technology buying, and later, as a Manager of Managers at Amazon, led federal partner sales teams covering Defense, Federal Civilian, Federal Financial and National Security. I've seen how this gets bought from both sides. If you want me to look at your federal plan, your pipeline or a federal business you're thinking about buying, grab 20 minutes and tell me about it. I'll tell you what I think.</p>
''' + talk_cta('federal') + '''
  <h2>Who this is usually for</h2>
  <ul>
    <li>Startups thinking about federal, and commercial technology companies moving into the public sector</li>
    <li>SaaS companies getting pulled into federal by a customer</li>
    <li>Companies trying to figure out partners, primes and integrators</li>
    <li>Sales leaders inheriting a federal business or making their first federal sales hire</li>
    <li>Investors and acquirers who want to know whether a federal pipeline is real</li>
  </ul>

  <h2>If it makes sense to keep going</h2>
  <ul>
    <li><strong>A federal pressure test.</strong> A working session on who's actually asking for it, where the money would come from, how they'd buy it, which partners you'd need, your pipeline and timing, and what should happen in the next 6 to 12 months, with my observations written up afterward.</li>
    <li><strong>A short federal sprint.</strong> For a company that needs more than a conversation: a working plan for which customers to start with, how they can buy, likely contract vehicles, partners and primes, the fiscal year's effect on your timing, and your first federal hire, with the risks and assumptions written down.</li>
    <li><strong>A read on federal revenue.</strong> For investors, acquirers or executives who want an outside view of whether a federal pipeline is real: how old it is, who the incumbent is, how much rides on one partner or vehicle, what's actually been won, and how much of it is funded work.</li>
  </ul>

  <h2>Some free places to start</h2>
  <ul>
    <li><a href="/federal-readiness/">Federal Readiness Check</a>: five questions on whether there's a federal business here.</li>
    <li><a href="/deal/">Deal Check</a>: pressure-test one federal opportunity on customer, money, power, path and timing.</li>
    <li><a href="/seller/#s-sep30">Working back from September 30</a>: the federal year-end chapter of the Seller's Field Kit.</li>
    <li><a href="https://fedhoo.com" rel="noopener">FedHoo</a>: federal market data tools I built.</li>
  </ul>

''' + CONF_BLOCK + '''
  <section class="offer offer-ask" id="ask">
    <h2>Grab 20 minutes</h2>
    <p>Tell me what you're looking at and I'll tell you what I think. If I don't think you need help, I'll say so.</p>
    <p class="offer-cta"><a class="btn btn-primary" href="''' + CAL + '''federal&utm_content=bottom" target="_blank" rel="noopener">Pick a time</a></p>
  </section>
</article>

''' + NOTE_TAIL
for _name, _html in (('work-with-mark', _work), ('federal', _fed)):
    assert '—' not in _html and '–' not in _html, _name
    os.makedirs(_name, exist_ok=True)
    open(f'{_name}/index.html', 'w').write(_html)



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
  <p class="dek">Let me know if you have better recommendations.</p>

  <h2>Books I actually read</h2>
  <div class="likes">
    <div class="like"><p class="like-t">The Qualified Sales Leader</p><p class="like-by">John McMahon</p><p class="like-why">A good one if you're managing serious enterprise sales teams.</p></div>
    <div class="like"><p class="like-t">Fanatical Prospecting</p><p class="like-by">Jeb Blount</p><p class="like-why">If prospecting is the part of the job you keep finding reasons not to do.</p></div>
    <div class="like"><p class="like-t">Getting to Yes</p><p class="like-by">Roger Fisher, William Ury and Bruce Patton</p><p class="like-why">Negotiating without turning it into a hostage situation.</p></div>
    <div class="like"><p class="like-t">The Little Red Book of Selling</p><p class="like-by">Jeffrey Gitomer</p><p class="like-why">If you joined my sales team, this was your onboarding gift.</p></div>
    <div class="like"><p class="like-t">How to Say It</p><p class="like-by">Rosalie Maggio</p><p class="like-why">Good when you know what you mean but can't find the words.</p></div>
    <div class="like"><p class="like-t">Atomic Habits</p><p class="like-by">James Clear</p><p class="like-why">Because a sales career is mostly boring things done over and over and over.</p></div>
    <div class="like"><p class="like-t">Meditations</p><p class="like-by">Marcus Aurelius</p><p class="like-why">Two thousand years old and still useful when the forecast call starts going south.</p></div>
    <div class="like"><p class="like-t">Tao Te Ching</p><p class="like-by">Lao Tzu</p><p class="like-why">Forcing things usually makes them worse. That goes for sales, management, meetings, pretty much everything.</p></div>
    <div class="like"><p class="like-t">The Bezos Blueprint</p><p class="like-by">Carmine Gallo</p><p class="like-why">Why Amazon writes and makes decisions the weird way it does.</p></div>
    <div class="like"><p class="like-t">Amazon Unbound</p><p class="like-by">Brad Stone</p><p class="like-why">Understanding how the company thinks. Good if you're trying to partner with Amazon.</p></div>
  </div>

  <h2>Podcasts I fall asleep to</h2>
  <div class="likes">
    <div class="like"><p class="like-t">The Brutal Truth About Sales</p><p class="like-by">Brian Burns</p><p class="like-why">Great interviews with real enterprise sellers. No corporate marketing stuff.</p></div>
    <div class="like"><p class="like-t">Hidden Brain</p><p class="like-by">Shankar Vedantam</p><p class="like-why">People are weird. Helpful to remember when selling to them or managing them.</p></div>
    <div class="like"><p class="like-t">Freakonomics Radio</p><p class="like-by">Stephen J. Dubner</p><p class="like-why">Incentives explain a lot of behavior, including sales behavior.</p></div>
    <div class="like"><p class="like-t">Marketplace</p><p class="like-by">American Public Media</p><p class="like-why">Twenty-some minutes and you know enough about the economy to sound less surprised.</p></div>
    <div class="like"><p class="like-t">Pivot</p><p class="like-by">Kara Swisher and Scott Galloway</p><p class="like-why">Tech, business, politics, and two people disagreeing with each other.</p></div>
    <div class="like"><p class="like-t">How to Be a Better Human</p><p class="like-by">TED</p><p class="like-why">Pretty much what it says.</p></div>
    <div class="like"><p class="like-t">The Daily Stoic</p><p class="like-by">Ryan Holiday</p><p class="like-why">Good before those forecast calls.</p></div>
    <div class="like"><p class="like-t">The Side Hustle Show</p><p class="like-by">Nick Loper</p><p class="like-why">For people who dream of escaping their cubicle.</p></div>
    <div class="like"><p class="like-t">Radiolab</p><p class="like-by">WNYC</p><p class="like-why">Good stories about things I didn't know I was interested in.</p></div>
    <div class="like"><p class="like-t">Stuff You Should Know</p><p class="like-by">Josh Clark and Chuck Bryant</p><p class="like-why">A great escape from thinking about your quota.</p></div>
  </div>

  <p class="fine stuff-foot">Stay tuned for my favorite Talking Heads and Hall &amp; Oates songs!</p>
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
_shelf = _shelf.replace('<h3 class="cg-h">Your number</h3><div class="cg-grid">\n', '<h3 class="cg-h">Your number</h3><div class="cg-grid">\n          <a class="ck" href="/quota/"><span class="cq">Is my quota crazy?</span><span class="cb"><span>Quota Check</span><svg viewBox=\"0 0 24 24\" width=\"18\" height=\"18\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M5 12h14M13 6l6 6-6 6\"/></svg></span></a>\n', 1)
_nf = open('404.html', encoding='utf-8').read()
_nf = re.sub(r'<!--shelf-->.*?<!--/shelf-->', lambda m_: '<!--shelf-->\n' + _shelf + '<!--/shelf-->', _nf, count=1, flags=re.S)
_nf = re.sub(r'<details class="menu">.*?</details>', lambda _m: menu(None), _nf, count=1, flags=re.S)   # the same Tools menu as every page
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
    ask = '/work-with-mark/'
    return f'''<header class="appbar">
    <a class="logo" href="/" aria-label="QuotaBird, home"><picture><source srcset="{b}logo-dark.svg" media="(prefers-color-scheme: dark)"><img class="brandmark" src="{b}logo.svg" alt="" width="39" height="34"></picture> QuotaBird</a>
    <nav class="topnav" aria-label="Site">
      {menu(current_of(path) if not path.startswith(('notes/', 'math/', 'kit/', 'leader/', 'seller/', 'kits/', 'stuff/', 'how-quotas-get-built/', 'shorts/', 'quota-by-the-numbers/', 'methodology/', 'privacy/', 'work-with-mark/', 'federal/')) else '/' + path.split('/')[0] + '/')}
      <a class="toplink" href="/kits/">Field Kits</a>
      <a class="toplink" href="/notes/">Field Notes</a>
      <a class="toplink" href="/about/">About</a>
      <a class="chip chip-ask" href="{ask}"><span class="ask-long">Work with Mark</span><span class="ask-short">Ask Mark</span></a>
    </nav>
  </header>'''
def chrome(path):
    s = open(path).read()
    # preload the one font every page uses, so headlines don't flash in a fallback face
    if 'rel="preload" href="/inter.woff2"' not in s:
        s = s.replace('<meta name="viewport"', '<link rel="preload" href="/inter.woff2" as="font" type="font/woff2" crossorigin>\n<meta name="viewport"', 1)
    s = re.sub(r'<header class="appbar">.*?</header>', lambda m: header(path), s, count=1, flags=re.S)
    ask = '/ask/'
    nav = f'<p class="foot-nav"><a href="/">Tools</a><a href="/kits/">Field Kits</a><a href="/math/">Sales Math</a><a href="/notes/">Field Notes</a><a href="/stuff/">Stuff I Like</a><a href="/about/">About</a><a href="/work-with-mark/">Work with Mark</a><a href="/privacy/">Privacy</a></p>'
    s = re.sub(r'\s*<p class="foot-nav">.*?</p>', '', s, count=1, flags=re.S)          # the footer nav is regenerated every build, so every page matches
    s = s.replace('<footer class="sitefoot">', '<footer class="sitefoot">\n  ' + nav, 1)
    # one contact line in every footer, for questions and security issues
    s = re.sub(r'\s*<p>Questions or security issues: <a href="mailto:mark@quotabird.com">mark@quotabird.com</a></p>', '', s)
    s = s.replace('<p>Not affiliated with the U.S. government or Amazon.</p>', '<p>Questions or security issues: <a href="mailto:mark@quotabird.com">mark@quotabird.com</a></p>\n  <p>Not affiliated with the U.S. government or Amazon.</p>', 1)
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
PAGES = ['index.html', 'pipeline/index.html', 'deal/index.html', 'about/index.html'] + [f'{t["slug"]}/index.html' for t in (REP, PARTNER, TERRITORY, OLR, BRIEF, ACCOUNT, RISK, COMPETITION, COMPPLAN, FEDREADY)] \
        + [f'{c["slug"]}/index.html' for c in CALCS] + ['notes/index.html'] + [f'notes/{n["slug"]}/index.html' for n in NOTES] + ['math/index.html'] + [f'math/{p["slug"]}/index.html' for p in MATH] + ['kits/index.html', 'seller/index.html', 'kit/index.html', 'leader/index.html', 'stuff/index.html', 'how-quotas-get-built/index.html', 'shorts/index.html', 'quota-by-the-numbers/index.html', 'methodology/index.html', 'privacy/index.html', 'work-with-mark/index.html', 'federal/index.html'] + ['404.html']
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
for t in (REP, PARTNER, TERRITORY, OLR, BRIEF, ACCOUNT, RISK, COMPETITION, COMPPLAN, FEDREADY): DESC['/' + t['slug'] + '/'] = t['name'] + ': ' + t['desc']
for c in CALCS: DESC['/' + c['slug'] + '/'] = c['name'] + ': ' + c['desc']
QUERIES = {'/federal-readiness/': ['is my company ready to sell to the federal government', 'federal go-to-market readiness', 'do I need a prime contractor', 'how do federal agencies buy software', 'federal sales readiness checklist'],
           '/offer/': ['compare two sales job offers', 'which sales offer pays more', 'OTE vs realistic earnings calculator', 'sales job offer ramp guarantee', 'year one sales compensation with ramp'],
           '/pay/': ['how much will my sales comp plan pay at 150% of quota', 'sales accelerator calculator', 'does my commission cap limit my upside', 'what does OTE really pay', 'comp plan payout curve'],
           '/comp-plan/': ['comp plan red flags', 'is my sales commission plan fair', 'questions to ask about a sales comp plan', 'commission clawback rules', 'who gets credit on a split deal'],
           '/commit/': ['will my customer burn their cloud commit', 'committed spend vs actual consumption', 'EDP commit burn down calculator', 'customer is behind on their committed spend', 'how much monthly spend to use a cloud commitment'],
           '/quota-case/': ['how to push back on a quota that is too high', 'is my sales quota realistic compared to last year', 'find the gap between last year and this year\'s quota', 'my quota went up and my territory did not'],
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
lines = ['# QuotaBird', '', '> QuotaBird is a free set of quota, pipeline and comp-plan calculators for B2B sellers and sales managers at cloud providers and SaaS companies, built by Mark Flournoy, who spent six years leading federal partner sales teams at Amazon. ' + f'{len([1 for g, h, n, d in TOOLS])} one-minute tools for the number they gave you and what they will pay you for it, plus short Field Notes, printable Field Kits and a methodology page that labels every benchmark as published data, a rule of thumb, or a QuotaBird working range.', '',
         'The tools are plain web pages. Each asks five questions (yes / sort of / no) or takes a few numbers, then gives a verdict, the question a manager will ask, and one thing to do first. The math runs in the browser and nothing typed is sent anywhere; base, variable and quota can be remembered in the visitor\'s own browser so other tools can prefill them. Shared results are encoded in the URL fragment; no accounts, no uploads, no AI. Privacy: https://quotabird.com/privacy/', '']
for g, items in groups:
    lines.append(f'## {g}'); lines.append('')
    for h, n, d in items:
        desc = DESC[h].split(': ', 1)[1]; lines.append(f'- [{n}]({site}{h}): {desc[0].upper() + desc[1:]} ({d[0].lower() + d[1:]}.)')
    lines.append('')
lines += ['## Methodology and benchmarks', '', f"- [How QuotaBird's numbers work]({site}/methodology/): where every range and benchmark on QuotaBird comes from, labelled as published data, a common rule of thumb, or a QuotaBird working range. Quota-to-OTE working ranges: bookings 4 to 6x (built on Bridge Group 2026 median 4.6x, 158 B2B companies), run rate or consumption growth 15 to 30x, whole book 40 to 80x (QuotaBird working ranges, derived from quota / OTE = variable share / commission rate). Includes each tool's formula and a last-reviewed date.", f"- [Quota by the numbers]({site}/quota-by-the-numbers/): sourced quota and compensation benchmarks: attainment, median quota and OTE, pay mix, ramp, over-assignment, accelerators.", '']
lines += ['## Working with Mark', '', '- [Work with Mark](https://quotabird.com/work-with-mark/): start with a free 20-minute call about a deal, quota, territory, pipeline, comp plan or anything else that doesn\'t add up. If more help makes sense (a working session, Manager Wingman for sales managers, or a session with a team), that gets discussed on the call.', '- [Federal GTM](https://quotabird.com/federal/): for companies deciding whether federal is real for them, and investors checking a federal pipeline; also starts with a free 20-minute call.', '']
lines += ['## Talking to Mark', '', f'- [The free twenty minutes]({site}/work-with-mark/#ask): a free first conversation about one sales problem; if Mark doesn\'t think you need help, he says so.', '']
lines += ['## Free printable', '', f"- [The Manager's Field Kit]({site}/kit/): a free, printable field kit for sales managers: how your team's number got built, fighting the plan without losing, handing down a tough quota and still crushing it, inheriting a team, one-on-ones, the forecast call, pipeline, managing up, a struggling rep, review season, managing high performers, and nine worksheets.", f"- [The Seller's Field Kit]({site}/seller/): a free, printable field kit for sellers: where your quota came from, checking it and pushing back, crushing a tough number anyway, is it a real deal, pipeline math, one deal carrying the quarter, single-threaded accounts, discounts, quiet deals, falling behind, and keeping your manager informed.", f"- [The Leadership Field Kit]({site}/leader/): a free, printable field kit for managers who want their influence to travel beyond their team: shaping the number before it shapes your team, what to be known for, a point of view, receipts, templates others can borrow, the right rooms, and developing the people behind you.", '', '## Sales Math Library', ''] + [f'- [{p["title"]}]({site}/math/{p["slug"]}/): {p["answer"]}' for p in MATH] + ['', '## Field Notes', ''] + [f'- [{n["title"]}]({site}/notes/{n["slug"]}/): {n["dek"]}' for n in NOTES] + ['', '## About', '', f'- [About Mark]({site}/about/): who is behind the tools, the situations he sees most, and how to book a free twenty-minute call.', '', '## Optional', '', f'- [Sitemap]({site}/sitemap.xml)', f'- [ai-catalog.json]({site}/.well-known/ai-catalog.json): ARD capability manifest listing the same tools.', '']
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
