#!/usr/bin/env python3
"""Builds rep/index.html, partner/index.html and territory/index.html from one template.
Run from the web root after editing copy below. Deal Check and Pipeline Check are hand-written."""
import json, os, re

BUILD = '2026-10-13.1500'
TOOLS = [
    ('Your deal', '/deal/', 'Deal Check', 'Before you put it in commit'),
    ('Your deal', '/account/', 'Account Check', 'When you only know one person there'),
    ('Your deal', '/competition/', 'Competition Check', 'When you are not sure you are ahead'),
    ('Your number', '/quota/', 'Quota Check', 'The day the number lands'),
    ('Your number', '/territory/', 'Territory Check', 'Month one in a new patch'),
    ('Your number', '/discount/', 'Discount Check', 'When they ask you to sharpen the pencil'),
    ('Your number', '/commission/', 'Commission Check', 'When it closes'),
    ('Your team', '/', 'Pipeline Check', 'Quarterly, before the review'),
    ('Your team', '/risk/', 'Risk Check', 'When coverage looks fine and you do not trust it'),
    ('Your team', '/rep/', 'Rep Check', 'When a rep is worrying you'),
    ('Your team', '/partner/', 'Partner Check', 'Before you renew the partnership'),
    ('Your team', '/olr/', 'OLR Check', 'Review season'),
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
    kit = '<a class="menu-kit" href="/kit/"><span class="pill">Free</span>The Sales Manager\'s Field Kit (PDF)</a>'
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
    dek='Answer five questions about the rep and find out whether it\'s the rep, the patch, a skill gap or an effort gap.',
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
    dek='Answer five questions and find out whether this partner sells with you or just sits on your slide.',
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
    : { overline: 'How much of your number is leaning on them?', text: 'If this partner is in your coverage math, the math is wrong. Pipeline Check shows you by how much.', href: '/', label: 'Check my pipeline' },
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
    dek='Answer five questions and find out whether this patch can make the number.',
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
        ('What about the coverage math?', 'That is the other tool. Once you know the territory can produce, <a href="/">Pipeline Check</a> tells you how much pipeline it has to produce.'),
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
    ? { overline: 'Now the coverage math', text: 'The territory can produce. Pipeline Check tells you how much it has to.', href: '/', label: 'Check my pipeline' }
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
    dek='Answer five questions about your case and find out whether it survives the room.',
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
        ('What does Pressure test do?', 'It plays the room. Three hard questions about your weakest answer, one at a time, and you say honestly whether you can answer each. If you cannot answer two of three about ownership, that case is not ready, and better to learn that here than across the table.'),
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
  grillBy: 'The room', grillLabel: 'Pressure test', fixLabel: 'Before the room',
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
    dek='Answer five questions about the doc, deck or QBR and find out before the meeting does.',
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
        ('What does Pressure test do?', 'It plays the room. Pick who is across the table, and it asks three of their questions about your weakest answer, one at a time. You say honestly whether you could answer. Better to find the hole here than in the meeting.'),
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
  grillBy: 'The room', grillLabel: 'Pressure test', fixLabel: 'Before the meeting',
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
    : { overline: 'If the brief is about the number', text: 'Vague impact usually means the coverage math is missing. Pipeline Check puts a number on it.', href: '/', label: 'Check my pipeline' },
  mark: { title: (s) => 'Stuck on the ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I have written the doc that got shredded and the one that got funded, and the difference was always one question I hadn't asked myself. Send me one line about the brief. No document, no company name." },
  dm: (s) => `Mark, ran a brief through Brief Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is the ${s.weak.n.toLowerCase()}. Meeting is coming and I'm not sure it holds. Worth 20 minutes?`,
  dmGrill: (s, missed) => `Mark, ran a brief through Brief Check and could not answer ${missed} of the room's 3 questions about the ${s.weak.n.toLowerCase()}. Verdict was ${s.label.toLowerCase()}. Want to tell me what you'd go fix first?`,
});''',
)

# ────────────────────────────── ACCOUNT CHECK ──────────────────────────────
ACCOUNT = dict(
    slug='account', name='Account Check',
    title='Account Check: Do You Know the Account, or Just Your Contact?',
    desc='Five questions that tell you whether you know the account or only the opportunity in front of you: mission, money, power, incumbents, how they buy. One minute, nothing stored.',
    ogdesc='Do you know the account, or just your contact? Five questions, one minute, no names.',
    h1='Do you know the account, or just your contact?',
    dek="Answer five questions and find out where you're single-threaded.",
    cta='Check my account',
    questions=[
        dict(k='mission', n='MISSION', q='Can you say what this account is trying to get done this year, in their words?'),
        dict(k='money', n='MONEY', q='Do you know where their money comes from and when it moves, beyond your deal?'),
        dict(k='power', n='POWER', q='Have you met someone who matters beyond the deal in front of you?'),
        dict(k='incumbent', n='INCUMBENT', q='Do you know who already owns the relationships, the contracts and the workloads?'),
        dict(k='path', n='PATH', q='Do you know how this account actually buys, and who runs that process?'),
    ],
    bands=[
        ('how', 'The five questions, and what each one disproves', '''    <p class="lede">Deal Check asks whether one opportunity is real. This asks whether you know the account it lives in.
      The difference shows up the day your contact leaves, gets reorganized, or stops answering.</p>
    <p><strong>MISSION: What are they trying to get done?</strong> Not what you sell them. What the agency, the program or the
      business unit has to accomplish this year, in words they'd recognize. If you can only describe the account in terms
      of your product, you know the opportunity, not the account.</p>
    <p><strong>MONEY: Where does it come from, beyond your deal?</strong> Appropriations, program lines, colors of money,
      fiscal calendars, the budget office. A seller who knows the account's money knows about deals before they exist. A
      seller who only knows the money for their own deal finds out about the others from the competitor's press release.</p>
    <p><strong>POWER: Who matters beyond this deal?</strong> Single-threaded is the most common way a good account goes
      quiet. If every conversation runs through one person, you don't have a relationship with the account; you have a
      relationship with them, and they have a career.</p>
    <p><strong>INCUMBENT: Who already owns it?</strong> Relationships, contracts and workloads all have owners, and most of
      them aren't you. Knowing who they are, and what they'd lose, is the difference between competing and hoping.</p>
    <p><strong>PATH: How do they actually buy?</strong> The contracting office, the vehicles they use, the approvals, the
      people who run the process. Every account has a way it buys, and it's the same for your deal as for the next one.
      Learn it once.</p>'''),
        ('verdicts', 'Four kinds of coverage', '''    <p><strong>Mapped.</strong> You know the mission, the money, the people and the process. Now find the next deal
      before anyone else does.</p>
    <p><strong>Half mapped.</strong> You know the parts your deal touches. Fill in the rest before the deal makes you.</p>
    <p><strong>One thread.</strong> Everything runs through one person. That's a risk, not a relationship. Get introduced
      upward and sideways this month.</p>
    <p><strong>A contact.</strong> You know someone there. That's the beginning of an account, not an account.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. The five answers are scored in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your answers. Nothing else leaves the page unless you choose to share a result.'),
        ('How is this different from Deal Check?', 'Deal Check is about one opportunity: is it real, will it close. Account Check is about the customer it lives in: do you know enough about them to find the next deal, survive a reorg, or beat the incumbent. A real deal in an unmapped account is how good sellers get surprised.'),
        ('Is this only for federal?', 'The questions were written with agencies in mind, where mission, colors of money and contract vehicles are everything. But every enterprise account has a mission, a budget process, an incumbent and a way it buys. Read the words that way and it works the same.'),
    ],
    config='''CheckTool({
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
    if (total >= 55) return { label: 'Half mapped', cls: 'proof', attack: 'You know the parts your deal touches.', sub: 'Fill in the rest before the deal makes you, or the reorg does.' };
    if (total >= 35) return { label: 'One thread', cls: 'prove', attack: 'Everything runs through one person.', sub: "That's a risk, not a relationship. Get introduced upward and sideways this month." };
    return { label: 'A contact', cls: 'dont', attack: 'You know someone there. That is the beginning of an account, not an account.', sub: 'Start with the mission and the money. The people follow from those.' };
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
    path: 'Find the contracting office and the vehicle they used last time. Ask how the last buy actually happened.',
  },
  noMove: 'Write the account down on one page while you still know it. Accounts change; the page is what survives the reorg.',
  handoff: (s) => s.total >= 55
    ? { overline: 'Now the deal inside it', text: 'You know the account. Is the opportunity in it real? Deal Check asks the five questions your manager will.', href: '/deal/', label: 'Check my deal' }
    : { overline: 'Before you build the account', text: "Can the patch it sits in make the number at all? Territory Check answers that before you spend a year here.", href: '/territory/', label: 'Check my territory' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I've built accounts from one contact and lost accounts that were mapped to the bone. Send me one line about the account, no name, and I'll tell you where I'd start." },
  dm: (s) => `Mark, ran an account through Account Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. Not sure where to start. Worth 20 minutes?`,
});''',
)

# ────────────────────────────── RISK CHECK ──────────────────────────────
RISK = dict(
    slug='risk', name='Risk Check',
    title='Risk Check: How Fragile Is the Pipeline You Have?',
    desc='Coverage says whether you have enough pipeline. This says how fragile it is: concentration, aging, next steps, timing and creation. Five questions, one minute, nothing stored.',
    ogdesc='4X coverage can still be a house of cards. Five questions, one minute, no deal names.',
    h1='4X coverage can still be a house of cards.',
    dek='Answer five questions and find out how fragile the pipeline you have really is.',
    cta='Check my risk',
    questions=[
        dict(k='spread', n='SPREAD', q='Would you still make the number if your biggest deal slipped a quarter?'),
        dict(k='motion', n='MOTION', q='Has every deal in commit moved stage in the last sixty days?'),
        dict(k='next', n='NEXT', q='Does every commit deal have a customer action on the calendar, not just yours?'),
        dict(k='timing', n='TIMING', q='Is at least half of it due before the last month of the period?'),
        dict(k='fresh', n='FRESH', q='Did you create at least a quarter of it this quarter?'),
    ],
    bands=[
        ('how', 'Five ways a covered pipeline falls over', '''    <p class="lede">Pipeline Check asks whether you have enough. This asks whether what you have would survive a bad
      week. A seller can be at 4X and one slipped deal from missing the year.</p>
    <p><strong>SPREAD: What if the big one slips?</strong> If a third of the number sits in one or two deals, your
      forecast is a bet on one customer's procurement calendar. Managers can't see this in the coverage ratio, which is
      why they ask about it in the review.</p>
    <p><strong>MOTION: Is it moving?</strong> A deal that hasn't changed stage in sixty days isn't in the stage it's in.
      It's parked, and parked deals leave the forecast all at once, usually in the last week of the quarter.</p>
    <p><strong>NEXT: Whose calendar is the next step on?</strong> A next step that only you scheduled is a task. A next
      step the customer put on their calendar is a commitment. Commit pipeline with no customer action in it is
      pipeline with no customer in it.</p>
    <p><strong>TIMING: When is it due?</strong> If most of the number lands in the last month of the period, you've built
      a year that can only be saved in December. Federal money makes this worse, not better: a September close is a
      September problem.</p>
    <p><strong>FRESH: Are you still creating?</strong> Pipeline you inherited or carried over runs out. If a quarter of
      what you're carrying wasn't created this quarter, next year's crater is already dug.</p>'''),
        ('verdicts', 'Four states of a pipeline', '''    <p><strong>Sturdy.</strong> Spread out, moving, with customers on the calendar. Go get the coverage number too.</p>
    <p><strong>Lopsided.</strong> One weakness. Fix it before the review notices.</p>
    <p><strong>Fragile.</strong> A slip or a quiet customer takes you off the number. Re-underwrite the commit deals now.</p>
    <p><strong>House of cards.</strong> It looks like coverage. It is a schedule of hopes. Rebuild it from the customers
      up.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. The five answers are scored in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your answers. Nothing else leaves the page unless you choose to share a result.'),
        ('I am at 4X coverage. Why does this say fragile?', 'Because coverage measures size, not shape. Four times the number in two deals that have not moved since spring is a smaller pipeline than it looks. Run Pipeline Check for the size and this for the shape; you need both to sleep.'),
        ('Should a manager run this on the team?', 'Yes, deal by deal is even better. The questions are the ones a good forecast call asks anyway. Running them before the call turns an argument into a plan.'),
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
    if (total >= 75) return { label: 'Sturdy', cls: 'ready', attack: 'Spread out, moving, customers on the calendar.', sub: 'Now go get the coverage number too. Shape without size is still a miss.' };
    if (total >= 55) return { label: 'Lopsided', cls: 'proof', attack: 'One weakness, and it is the one the review will find.', sub: 'Fix the weakest answer before someone asks about it.' };
    if (total >= 35) return { label: 'Fragile', cls: 'prove', attack: 'A slip or a quiet customer takes you off the number.', sub: 'Re-underwrite every commit deal this week. Whose calendar is the next step on?' };
    return { label: 'House of cards', cls: 'dont', attack: 'It looks like coverage. It is a schedule of hopes.', sub: 'Rebuild it from the customers up, starting with the deals that have not moved.' };
  },
  askedBy: 'Your boss will ask',
  grill: {
    spread: 'What happens to the number if the big one slips a quarter?',
    motion: 'Which commit deals have not changed stage since last quarter?',
    next: "Which commit deals have a customer action on the customer's calendar?",
    timing: 'How much of the number lands in the last month?',
    fresh: 'How much of this did you create this quarter?',
  },
  moves: {
    spread: 'Write the number without your biggest deal. That is the plan you are actually running.',
    motion: 'Move every deal that has not changed stage in sixty days back a stage, today. Then work the ones that argue.',
    next: 'For each commit deal, get one customer action onto their calendar this week or move it out of commit.',
    timing: 'Pull one deal into an earlier month, or accept that the year is a December bet and tell your manager so.',
    fresh: 'Block two mornings this week for creation. Nothing else fixes a crater.',
  },
  noMove: 'Keep the shape. Now check the size: run the coverage math with your real win rate.',
  handoff: (s) => ({ overline: 'Shape checked. Now the size.', text: 'Risk is the shape of the pipeline. Pipeline Check is the size. You need both.', href: '/', label: 'Check my pipeline' }),
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I have forecast the year on two deals and watched both slip in the same week. Send me one line about the shape of the pipeline, no customer names, no dollars." },
  dm: (s) => `Mark, ran my pipeline through Risk Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. Coverage looks fine and I don't trust it. Worth 20 minutes?`,
});''',
)

# ────────────────────────────── COMPETITION CHECK ──────────────────────────────
COMPETITION = dict(
    slug='competition', name='Competition Check',
    title='Competition Check: Why You, Instead of Nothing?',
    desc='Five questions that tell you whether the incumbent, the competitor, or doing nothing is beating you right now. One minute, nothing stored.',
    ogdesc='Why you, instead of nothing? Five questions, one minute, no names.',
    h1='Why you, instead of nothing?',
    dek='Answer five questions and find out whether the incumbent or doing nothing is beating you.',
    cta='Check my position',
    questions=[
        dict(k='nothing', n='NOTHING', q='Do you know what it costs them to do nothing, in their numbers?'),
        dict(k='switch', n='SWITCH', q='Do you know what it costs them to leave the incumbent, and who feels it?'),
        dict(k='preference', n='PREFERENCE', q='Has the customer told you, unprompted, why they would prefer you?'),
        dict(k='proof', n='PROOF', q='Do you have proof only you can show them: a reference, a pilot, a result?'),
        dict(k='access', n='ACCESS', q='Do you know who at the customer the competitor already owns?'),
    ],
    bands=[
        ('how', 'The five questions, and what each one disproves', '''    <p class="lede">Most deals aren't lost to a competitor. They're lost to nothing: the customer keeps what they have,
      the money goes elsewhere, the project waits a year. This checks whether you're beating nothing before it checks
      whether you're beating anyone.</p>
    <p><strong>NOTHING: What does inaction cost them?</strong> If you can't put a number, in their terms, on what happens if
      they don't act, then doing nothing is free, and free wins. This is the question sellers skip because the answer
      lives in the customer's world, not the product's.</p>
    <p><strong>SWITCH: What does leaving cost them?</strong> Incumbents don't win on merit. They win on the cost of
      change: retraining, migration, the person whose job is the current system. Know that cost and who carries it, or
      you'll lose to someone who never showed up to a meeting.</p>
    <p><strong>PREFERENCE: Have they said it?</strong> Not "we like your solution." An unprompted reason, in their words,
      why you instead of the alternative. Until you've heard it, you're a column in their comparison, and columns don't
      win.</p>
    <p><strong>PROOF: What can only you show?</strong> A reference they can call, a pilot in their environment, a result
      at a customer they respect. Claims are free. Proof they can check is the only thing the incumbent can't copy.</p>
    <p><strong>ACCESS: Who does the competitor own?</strong> Somewhere in the account there's a person the other side has
      been having lunch with for three years. Knowing who tells you where the fight is; not knowing means you'll find
      out in the debrief.</p>'''),
        ('verdicts', 'Four positions', '''    <p><strong>Preferred.</strong> They've told you why, you can prove it, and you know the cost of nothing. Close.</p>
    <p><strong>In the mix.</strong> You're a real option. So is something else. Find the reason and get it in their
      words.</p>
    <p><strong>Behind.</strong> The incumbent or the competitor has something you don't: access, proof, or a friend.
      Name it before you spend another quarter here.</p>
    <p><strong>Nothing wins.</strong> Doing nothing is beating you, and it isn't even trying. Until inaction has a cost,
      you don't have a competitor. You have a hobby.</p>'''),
    ],
    faq=[
        ('Does anything I enter leave my device?', 'No. The five answers are scored in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your answers. Nothing else leaves the page unless you choose to share a result.'),
        ('What if there is no competitor?', 'There is always one: doing nothing. Most deals that are "uncontested" are lost to the status quo, which is why the first question is about the cost of inaction rather than a named rival. Answer it honestly and the tool will tell you whether nothing is winning.'),
        ('Is this a battlecard?', 'No. Battlecards are about them. This is about the customer: what inaction costs, what switching costs, what they have said, what you can prove, and who the other side already has. Win those and the battlecard is optional.'),
    ],
    config='''CheckTool({
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
    return { label: 'Nothing wins', cls: 'dont', attack: "Doing nothing is beating you, and it isn't even trying.", sub: "Until inaction has a cost in their numbers, you don't have a competitor. You have a hobby." };
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
  noMove: 'You are preferred. Write down why, in their words, so the reason survives the next reorg.',
  handoff: (s) => s.total >= 55
    ? { overline: 'Now the deal itself', text: 'Position is about them. Deal Check is about the deal: customer, money, power, path, now.', href: '/deal/', label: 'Check my deal' }
    : { overline: 'Do you know the account?', text: 'Being behind usually means the other side knows the account better. Account Check finds where.', href: '/account/', label: 'Check my account' },
  mark: { title: (s) => 'Stuck on ' + s.weak.n.toLowerCase() + '?', body: "I'm Mark. I've lost to incumbents I never saw and to nothing more times than I'd like. Send me one line about where you stand, no company names." },
  dm: (s) => `Mark, ran a deal through Competition Check. ${s.label[0] + s.label.slice(1).toLowerCase()}, ${s.provenText}, weakest is ${s.weak.n.toLowerCase()}. Not sure I'm actually ahead. Worth 20 minutes?`,
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
         tool=('/', 'Pipeline Check', 'does both in about a minute, and shows the 3X line and yours on the same bar.')),
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
    dict(slug='quota-went-up-did-your-territory', title='Your quota went up 30%. Did your territory?',
         dek='The number moved. Ask what else did.',
         body='''    <p class="lede">The number moved. Before you decide whether you can make it, ask what else did.</p>
    <p>A quota is a claim about a patch. When it goes up 30%, one of three things is true: the patch got bigger, the
      patch got better, or somebody needed the spreadsheet to add up. The first two are fine. The third is the one
      you want to know about in January, not in October.</p>
    <p>So do the boring arithmetic first. Divide the new number by your on-target earnings. Somewhere between 4 and
      6 is the range I've usually seen for mid-market cloud and SaaS reps; 6 to 8 is enterprise at a big provider;
      above 10 the plan is asking the territory for something it may not have. Then divide the number by what you
      actually closed last year. That's the growth the plan is assuming, and it is the honest measure of how much
      harder this year is.</p>
    <p>Then look at the patch the same way a stranger would. Has anyone ever made this number in it? What's the
      addressable spend, and how much of it is already committed to somebody else? If the number went up and the
      patch didn't, say so early, with the sizing, in writing. Nobody argues with a number that came with its
      work shown.</p>''',
         tool=('/quota/', 'Quota Check', 'does the arithmetic in ten seconds, and hands the number to the territory and pipeline checks.')),
    dict(slug='fifteen-percent-off', title='They asked for 15% off. What are you buying with it?',
         dek='A discount is a purchase. Make sure you get something for it.',
         body='''    <p class="lede">Every point off the price buys something. The question is whether you got it.</p>
    <p>Sellers think of a discount as a concession. I'd think of it as a purchase, because that's how the customer
      thinks of it. Up to about 5% off is normal negotiation and nobody remembers it. Between 5 and 15% is real
      money, and it should buy something specific: a signature date, a bigger scope, a multi-year term, a reference
      you can use. Above 15% you're paying for a decision, so make sure a decision is what you're getting, this
      quarter, in writing. Above 25%, in my experience, you're paying to be liked, and the customer will remember
      the number rather than the gesture.</p>
    <p>Two things worth knowing before the conversation. The discount comes out of your commission at exactly the
      rate it comes out of revenue, so 15% off is a 15% pay cut on that deal. And it comes out of the company's
      margin faster than that, because the cost of delivering the thing doesn't drop when the price does.</p>
    <p>The last question is the one I'd ask first: is the objection the price, or the deal? A discount fixes exactly
      one of those, and it isn't usually the one you have.</p>''',
         tool=('/discount/', 'Discount Check', 'shows what the discount costs you and the company before you agree to it.')),
    dict(slug='best-rep-hates-meetings', title='Your best rep hates internal meetings. Is that a problem?',
         dek="Probably not the one you think.",
         body='''    <p class="lede">Every team has one. Skips the pipeline call, answers Slack in bursts, CRM hygiene is a
      disgrace, and customers call her back.</p>
    <p>The manager's instinct is to fix the behavior. Before you do, ask which differences matter to selling and
      which don't. Do customers choose to spend time with her? Is there pipeline that exists only because she's
      here? When she's in front of a customer, can she sell? Is she still trying to win? If the answers are yes,
      you don't have a performance problem. You have a visibility problem, and it's yours to solve, not hers.</p>
    <p>Decide what visibility you actually need. Usually it's less than the process asks for: the five deals that
      matter, a straight answer on where each one stands, and a heads-up before something moves in the forecast.
      Get that, and let her sell. The polished rep with immaculate CRM hygiene and no customer pull is the one who
      should worry you, and he's the one the dashboard likes.</p>
    <p>None of this means standards don't apply. It means the standard is customers and pipeline, and the meeting
      is a means to it. When the means starts costing you the end, it's the means that's wrong.</p>''',
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
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#F9FCFF">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#101418">
<link rel="stylesheet" href="/site.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BG9NR9GXQZ"></script>
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
  desc='Your quota against your on-target earnings, judged by what the number is measured in: new bookings, cloud consumption growth, or a whole book. Free, in your browser, nothing stored.',
  ogdesc='Is my quota crazy? Base, variable, quota and what it is measured in. A straight answer out.',
  h1='Is my quota crazy?', dek='Plug in your base, your variable and the number they handed you to find out.',
  fields=[dict(id='basis',kind='choice',label='What the number is measured in',example='cloud',options=[('saas','New bookings'),('cloud','Cloud consumption growth'),('book','Whole book')]),
          dict(id='base',kind='money',label='Base salary',example='$150,000'),dict(id='variable',kind='money',label='Target variable at 100%',example='$130,000'),
          dict(id='quota',kind='money',label='Your quota for the year',example='$6,000,000'),dict(id='closed',kind='money',label='What you closed last year',example='',placeholder='$0 (optional)')],
  card=dict(headline=['Is my quota crazy?',''],dek='Your number against your on-target earnings, judged by what it is measured in.',pillars=['OTE','MULTIPLE','RATE','GROWTH']),
  bands=[('how','Why the multiple depends on what you sell','''    <p class="lede">Divide your quota by your on-target earnings. That number tells you more about the plan than the plan will, but only once you know what the quota is measured in.</p>
    <p>For SaaS reps carrying new bookings, the published benchmarks agree: 4 to 6 times OTE, with 5 as the steady state and enterprise roles a little higher. That range is really a commission rate in disguise. At a 50/50 pay mix and roughly 10% on new ARR, quota works out to about five times OTE. Below 3 is unusual and usually means a ramp, an overlay, or a plan with a condition in it. Above 8 the plan is asking for something the patch may not have.</p>
    <p>Cloud consumption is a different animal, and it's the one most people on this site carry. The number is incremental revenue growth on a book, paid at a fraction of a percent, so the same arithmetic gives 15 to 30 times OTE at a big cloud provider and higher in strategic accounts. A rep carrying a $6M growth target on a $280K OTE is at 21×, and in my experience that's ordinary, not crazy. Whole-book targets (retention plus growth on the full run rate) run higher still, 40 to 80 times OTE, because most of that revenue would have happened anyway.</p>
    <p>The number to watch across all three is the implied rate: your variable divided by your quota. If it's well under what your peers are paid on the same kind of number, the plan is heavier than the multiple alone suggests. And if you closed last year, the growth the new number implies is the honest measure of how much harder this year is. Whether the patch can produce it is <a href="/territory/">Territory Check</a>; how much pipeline it takes is <a href="/">Pipeline Check</a>.</p>'''),
         ('ranges','The ranges I use','''    <p>These are ranges I've seen across cloud providers, SaaS companies and their partners, not rules, and roles differ. Quota ÷ OTE:</p>
    <p><strong>New bookings.</strong> Under 3: low. 3 to 4: favorable. 4 to 6: standard. 6 to 8: a stretch. 8 to 12: aggressive. Over 12: crazy.</p>
    <p><strong>Cloud consumption growth.</strong> Under 8: low. 8 to 15: favorable. 15 to 30: standard. 30 to 45: a stretch. 45 to 60: aggressive. Over 60: crazy.</p>
    <p><strong>Whole book.</strong> Under 20: low. 20 to 40: favorable. 40 to 80: standard. 80 to 120: a stretch. 120 to 160: aggressive. Over 160: crazy.</p>
    <p>If your plan sits in a different place and you think the range is wrong, tell me. I'd rather fix the range than argue with your paycheck.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The arithmetic runs in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your numbers. Nothing else leaves the page unless you choose to share a result.'),
       ('Why does it ask what the number is measured in?','Because the same multiple means different things. A $1.4M new-bookings quota on a $280K OTE is 5× and normal. A $1.4M cloud consumption growth target on the same OTE is 5× and unusually light, because consumption is paid at a fraction of the rate bookings are. Pick the basis your plan actually uses.'),
       ('Where do the ranges come from?','The SaaS range is the published consensus (Bridge Group, RepVue, Pavilion and others put it at 4 to 6× OTE). The cloud and whole-book ranges are what I have seen at cloud providers and their partners, derived from the commission rates those plans pay. They are ranges, not rules, and I will change them if enough people tell me their plan sits somewhere else.'),
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
    else if (mult < c[1]) t = ['Favorable', 'ready', `Quota is ${X} OTE, below the ${std} I usually see for ${B.name}.`, 'Common in new patches, SMB and commercial. Enjoy it while it lasts.'];
    else if (mult <= c[2]) t = ['Standard', 'ready', `Quota is ${X} OTE, inside the ${std} I usually see for ${B.name}.`, "The number is ordinary. Whether the patch can produce it is a different question."];
    else if (mult <= c[3]) t = ['A stretch', 'proof', `Quota is ${X} OTE, above the ${std} I usually see for ${B.name}.`, 'Normal for enterprise and strategic roles, and it needs a strong pipeline behind it.'];
    else if (mult <= c[4]) t = ['Aggressive', 'prove', `Quota is ${X} OTE, well above the ${std} I usually see for ${B.name}.`, 'Strategic-account territory. You need coverage and a patch that can produce it.'];
    else t = ['Crazy', 'dont', `Quota is ${X} OTE. For ${B.name}, the plan is asking the patch for something it may not have.`, 'Check the territory before you sign, and get the sizing in writing.'];
    const growth = v.closed > 0 ? (v.quota - v.closed) / v.closed : null;
    const rows = [['On-target earnings', money(ote)], ['Quota ÷ OTE', X], ['Implied rate on quota', ratePct], ['Variable share of OTE', pct(share)]];
    if (growth != null) rows.push(['Growth over what you closed', (growth >= 0 ? '+' : '') + pct(growth), growth > .3 ? 'v-no' : '']);
    const note = share < .4 ? 'Variable is under 40% of OTE. You are paid mostly to show up, and the quota matters less than it looks.' : share > .6 ? 'Variable is over 60% of OTE. The quota is most of your pay. Treat it like one.' : '';
    return { label: t[0], cls: t[1], attack: t[2], sub: t[3], big: X, rows, note, mult, share, growth, ote, quota: v.quota, basis: B.name, ratePct };
  },
  handoff: (s) => ({ overline: 'Now the coverage math', text: `At 3X you'd need about $${(s.quota * 3 / 1e6).toFixed(1)}M of qualified pipeline to cover it. Your win rate will say more.`, href: `/#t=${Math.round(s.quota)}&y=cy`, label: 'Check my pipeline' }),
  mark: { title: () => 'Is the plan sane?', body: "I'm Mark. I've been handed the crazy number and handed one out by mistake. If the multiple is off, I can help you make the case. If it's fair, I can help you make the plan. One line, no company name, no dollar figures." },
  dm: (s) => `Mark, ran my comp plan through Quota Check. Quota is ${s.big} OTE on ${s.basis}, implied rate ${s.ratePct}, variable ${Math.round(s.share * 100)}% of OTE${s.growth != null ? ', ' + Math.round(s.growth * 100) + '% over what I closed last year' : ''}. Not sure it's sane. Worth 20 minutes?`,
  bookNote: (s) => `Quota Check: ${s.big} OTE on ${s.basis}, implied rate ${s.ratePct}, ${s.label.toLowerCase()}.`,
});"""),
 dict(slug='discount', name='Discount Check',
  title='Discount Check: What a Discount Costs You',
  desc='They want a discount. See what it costs in your commission and the company\'s margin before you say yes. Free, in your browser, nothing stored.',
  ogdesc='They want a discount. Here is exactly what it costs you before you sharpen the pencil.',
  h1='They want a discount.', dek='Plug in the price and the discount to see what it costs you before you say yes.',
  fields=[dict(id='list',kind='money',label='Full list price',example='$500,000'),dict(id='disc',kind='pct',label='Discount they want',example='15%'),
          dict(id='margin',kind='pct',label="Company gross margin",example='40%'),dict(id='rate',kind='pct',label='Your commission rate',example='8%')],
  card=dict(headline=['They want a discount.',''],dek='What it costs you in commission, and the company in margin, before you say yes.',pillars=['PRICE','DISCOUNT','MARGIN','YOUR CUT']),
  bands=[('how','A discount is a purchase','''    <p class="lede">Every point off the price buys something. The question is whether you got it.</p>
    <p>These are rough ranges from my own deals and the ones I've reviewed; yours may differ. Up to about 5% is normal negotiation. Nobody remembers it. Between 5 and 15% is meaningful, and it should buy something specific: a signature date, a larger scope, a reference, a multi-year term. Above 15% you are paying for a decision, so make sure a decision is what you're getting, this quarter, in writing. Above 25%, you're usually paying to be liked, and the customer will remember the number, not the gesture.</p>
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
  handoff: { overline: 'Before you discount', text: 'Is it the price, or the deal? A discount fixes exactly one of those.', href: '/deal/', label: 'Check my deal' },
  mark: { title: () => 'Stuck on the price?', body: "I'm Mark. Most of the discounts I've watched given away bought nothing but a warmer feeling. If you're being asked to sharpen the pencil, send me one line about why. No customer names, no dollar figures." },
  dm: (s) => `Mark, ran a discount through Discount Check. ${Math.round(s.disc * 100)}% off costs me ${Math.round(s.disc * 100)}% of my commission${s.newMargin != null ? ' and takes margin from ' + Math.round(s.margin * 100) + '% to ' + Math.round(s.newMargin * 100) + '%' : ''}. Not sure it's worth it. Worth 20 minutes?`,
  bookNote: (s) => `Discount Check: ${Math.round(s.disc * 100)}% off${s.newMargin != null ? ', margin ' + Math.round(s.margin * 100) + '% to ' + Math.round(s.newMargin * 100) + '%' : ''}, ${s.label.toLowerCase()}.`,
});'''),
 dict(slug='commission', name='Commission Check',
  title='Commission Check: Your Take-Home on a Deal',
  desc='Deal size and commission rate in, what you actually take home out, after the share you set aside for taxes. Free, in your browser, nothing stored.',
  ogdesc='It closed. Here is roughly what you actually take home.',
  h1='It closed. What do I actually take home?', dek='Plug in the deal and your rate to find out, roughly, before the check lands.',
  fields=[dict(id='deal',kind='money',label='Deal size',example='$500,000'),dict(id='rate',kind='pct',label='Your commission rate',example='8%'),
          dict(id='buffer',kind='pct',label='Set aside for taxes',example='30%',presets=[('W-2 ~30%','30%'),('High bracket ~40%','40%'),('1099 ~20%','20%')])],
  card=dict(headline=['It closed.','What do I take home?'],dek='A planning estimate of the check after withholding, in about ten seconds.',pillars=['DEAL','RATE','WITHHELD','TAKE-HOME']),
  bands=[('how','Why the check is smaller than the math','''    <p class="lede">Gross commission is the number in the plan. Take-home is the number in your account. They are further apart than most sellers expect the first time.</p>
    <p>The percentage you set aside is a planning buffer, not a withholding rate. For commissions paid separately from salary, the IRS lets employers withhold federal income tax at a flat 22% (up to a million dollars a year), and payroll taxes and state withholding come on top of that, so a W-2 check often lands with roughly 30% gone. High earners tend to owe closer to 40% once the year is reconciled. A 1099 contractor has nothing withheld and should set aside 20% or more. Your real number depends on your state, your filing status and everything else you earned this year, which is why the field is editable.</p>
    <p>Use it to plan, not to argue with payroll. And once you know what a deal pays, the more useful question is whether the plan behind it is sane: <a href="/quota/">Quota Check</a>.</p>''')],
  faq=[('Does anything I enter leave my device?','No. The arithmetic runs in your browser. No account, no CRM connection, no API call. The site counts page views with Google Analytics and never sends your numbers. Nothing else leaves the page unless you choose to share a result.'),
       ('Is this tax advice?','No. The percentage is a planning buffer you can change; it is not a withholding rate. Federal withholding on separately paid commissions is typically a flat 22%, with payroll and state taxes on top, and what you actually owe is settled at tax time. For anything that matters, ask an accountant.'),
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
      <div class="useful" id="useful"><span>Useful?</span><button class="btn btn-text" data-u="yes" type="button">Yes</button><button class="btn btn-text" data-u="no" type="button">Not really</button></div>
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
  body=f'''    <p>Coverage ratios get quoted as if they were laws. They're arithmetic. If you close a fraction <em>w</em> of the
      qualified pipeline that's due in a period, the pipeline you need to make a number is the number divided by
      <em>w</em>. Coverage is that divided by the number, which leaves <strong>1 ÷ w</strong>.</p>
    <p>So 3X is a 33% win rate written down without saying so. It's right for a team that wins a third of what it
      qualifies, and wrong for everyone else, in one direction or the other.</p>
    <h2>Coverage by win rate</h2>
    {_table(['Qualified win rate', 'Coverage needed', 'Pipeline for a $1M number', 'Pipeline for a $10M number'], cov_rows)}
    <h2>Three things the ratio quietly assumes</h2>
    <p><strong>Qualified, not total.</strong> The win rate and the pipeline have to measure the same thing. If your win
      rate is calculated on qualified opportunities, count only qualified pipeline against it. Mixing a qualified win
      rate with a CRM total overstates coverage every time.</p>
    <p><strong>Due in the period.</strong> Pipeline that closes next year doesn't cover this year, however real it is.</p>
    <p><strong>By value, not by count.</strong> If you win 30% of your deals but mostly the small ones, your win rate by
      value is lower than 30%, and that's the one that matters here.</p>
    <h2>Worked example</h2>
    <p>A $6M number, a 20% qualified win rate. Coverage needed is 1 ÷ 0.20 = 5X, so the pipeline needed is $30M. A
      seller carrying $18M is at 3X, which looks covered, and is $12M short.</p>''',
  tool=('/', 'Pipeline Check', 'runs this with your own number and win rate, and shows the 3X line and yours on one bar.'),
  sources=['The arithmetic on this page needs no source. The 3X convention is widespread in sales planning; this page explains what it assumes rather than endorsing it.']),
 dict(slug='quota-to-ote', title='What your quota-to-OTE ratio really says',
  dek='Quota ÷ OTE is your variable share divided by your commission rate. It is a pay rate in disguise.',
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
    <p>Those numbers check each other: 47% variable divided by an 11.5% rate is 4.1×, within rounding of the reported
      4.2×. The multiple isn't a convention someone chose. It falls out of the rate.</p>
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
  dek='Commission falls at the rate of the discount. Margin falls faster, because cost does not move.',
  answer='A discount cuts your commission by exactly the discount percentage, and cuts gross margin to 1 − (1 − margin) ÷ (1 − discount). A 15% discount on a 40% margin leaves about 29%, not 25%.',
  body=f'''    <p>Two formulas, and the second is the one sellers get wrong.</p>
    <p><strong>Your commission.</strong> If you're paid a rate on the price, commission lost = rate × discount × list price.
      A 15% discount is a 15% pay cut on that deal, no more and no less.</p>
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
  answer='US employers may withhold federal income tax on separately paid commissions at a flat 22% (37% on supplemental wages above $1 million in a year), plus 7.65% Social Security and Medicare, before any state tax. That is withholding, not the tax you finally owe.',
  body=f'''    <p>The IRS treats commissions and bonuses as supplemental wages. When they're paid separately from salary, employers
      can withhold federal income tax at a flat rate instead of running them through the normal tables. Social Security
      and Medicare come out on top, then your state, if it has an income tax.</p>
    <h2>Federal withholding and payroll tax, before state</h2>
    {_table(['Gross commission', 'Federal (22%)', 'Social Security + Medicare (7.65%)', 'Left before state tax'], c_rows,
            'Assumes supplemental wages under $1 million for the year and earnings under the Social Security wage base. Above the wage base, the 6.2% Social Security portion stops; above $200,000 in wages, an extra 0.9% Medicare applies.')}
    <p>That's where the rough 30% figure comes from: 22% plus 7.65% is 29.65% before any state tax. It's why Commission
      Check starts its set-aside at 30% for a W-2 seller.</p>
    <h2>What this is not</h2>
    <p>Withholding is an estimate collected in advance. What you actually owe is settled when you file, and depends on
      your bracket, your state, your filing status and everything else you earned. A 1099 contractor has nothing
      withheld at all. None of this is tax advice; for anything that matters, ask an accountant.</p>''',
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
  <nav class="kit-toc" aria-label="Contents">
    <a href="#k-first">Inherited a team</a><a href="#k-rhythm">1:1 vs forecast</a><a href="#k-forecast">The forecast call</a>
    <a href="#k-pipeline">Pipeline</a><a href="#k-boss">Your boss</a><a href="#k-rep">A struggling rep</a>
    <a href="#k-review">Review season</a><a href="#k-mistakes">Learned the hard way</a><a href="#k-lines">Lines worth stealing</a><a href="#k-alone">Leave them alone</a>
  </nav>

  <section class="kit-ch" id="k-start">
    <p>I've taken over teams that were doing great, teams that were struggling, and a few that were already on fire
      when I got there. Some I fixed. A couple I made worse before I made them better.</p>
    <p>This isn't a management methodology, and there's no certification at the end. It's the stuff that kept being
      useful: figuring out whether the problem is the rep or the patch, getting an honest forecast, knowing whether
      there's really enough pipeline, helping a rep who's struggling, defending your people in review season, and
      keeping your own boss out of surprise mode.</p>
    <p>Don't read it front to back. <strong>Find the problem you have this week and start there.</strong> Each chapter
      ends with the worksheet that goes with it.</p>
  </section>

  <section class="kit-ch" id="k-first">
    <h2>1. You inherited a team. Don't grade everybody yet.</h2>
    <p>My first mistake as a new manager was deciding pretty quickly who was good and who wasn't. I was wrong. Now I
      look at the patch before the person.</p>
    <p>Before I decide a rep has a performance problem, I want to know whether the territory is any good, what's
      installed already, whether the quota is remotely reasonable, what the last rep did there, what the comp plan
      rewards, and whether there are enough customers who can actually buy what we sell.</p>
    <p>If three good people have failed in the same patch, I probably don't have three bad salespeople. I have a bad
      patch.</p>
    <p>Then I look at the rep. Not the CRM first. The rep. Do customers want to spend time with them? Have they
      created anything that wouldn't exist without them? Can they sell when they're actually in the room? Are they
      still trying?</p>
    <p>One of the most useful things I ever did with a new team was sit with each rep and go through five real deals.
      You learn a lot from how somebody talks about a customer. And every once in a while, the rep who drives you nuts
      internally turns out to be the one customers keep calling back. That matters.</p>
    <p class="kit-note"><strong>My first month.</strong> Week 1: meet everybody, ask what they'd change. Week 2: size the
      patches. Week 3: sit in deals and customer calls. Week 4: tell your boss what you found. Patches first, people
      second.</p>
    <div class="sheet">
      <h3>Worksheet: Rep diagnostic</h3>
      <p class="sheet-meta">Rep ____________________ &nbsp; Date __________ &nbsp; <span class="sheet-tool">Online: quotabird.com/rep</span></p>
      <div class="mtable"><table class="ws"><thead><tr><th>In this order</th><th>Yes / Sort of / No</th><th>Notes</th></tr></thead><tbody>
        <tr><td>Patch: could a good rep make this number here?</td><td></td><td></td></tr>
        <tr><td>Customers: do they want time with this rep?</td><td></td><td></td></tr>
        <tr><td>Pipeline: is there pipeline only this rep created?</td><td></td><td></td></tr>
        <tr><td>Craft: can they sell in the room?</td><td></td><td></td></tr>
        <tr><td>Will: are they still trying to win?</td><td></td><td></td></tr>
      </tbody></table></div>
      <p class="sheet-foot">Patch is no: fix the situation. Craft is no: coach. Will is no: manage. Both no in a fair patch: see chapter 6.</p>
    </div>
  </section>

  <section class="kit-ch" id="k-rhythm">
    <h2>2. Keep the 1:1 and the forecast call separate</h2>
    <p>These are not the same meeting. A 1:1 is about the person. A forecast call is about the number. Whenever I mixed
      them together, both got worse.</p>
    <p>My 1:1 was usually thirty minutes, and the rep went first. What are they working on? What's getting in their
      way? What am <em>I</em> doing that's getting in their way? Then we look at one real deal properly.</p>
    <p>I finish with one thing I saw them do well, one thing I'd try differently, and anything I said I'd do. Then I
      write my commitment down, and I do it. That last part built more trust than any management technique I ever
      learned.</p>
    <p>Once a month I'd ask, "If you were running this team, what would you change?" You'll hear things nobody says in
      the staff meeting.</p>
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
    <h2>3. The forecast call is not story time</h2>
    <p>To me, commit means the customer could explain how the money gets from them to us, and roughly when. Anything
      short of that is some flavor of hope. Most shaky deals eventually break in one of five places:</p>
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
    <p>When a rep and I disagree, I don't need to win the argument. I ask which of the five they'd defend to my boss,
      and we forecast that. Nobody has to lose face. The forecast just gets better.</p>
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
    <p>Managers usually ask whether there's enough pipeline. I'd ask one more question: is it sturdy enough to survive a
      bad week? Those are different questions.</p>
    <p><strong>Enough.</strong> The 3X rule everybody repeats assumes roughly a 33% win rate. The math is simple:
      coverage needed is one divided by your win rate. Use your own team's qualified win rate, not somebody else's
      benchmark.</p>
    <div class="mtable kit-small"><table><thead><tr><th>Win rate</th><th>Coverage needed</th></tr></thead><tbody>
      <tr><td>15%</td><td>6.7X</td></tr><tr><td>20%</td><td>5.0X</td></tr><tr><td>25%</td><td>4.0X</td></tr>
      <tr><td>33%</td><td>3.0X</td></tr><tr><td>40%</td><td>2.5X</td></tr>
    </tbody></table></div>
    <p><strong>Sturdy.</strong> A team can have 4X coverage and still be in trouble. So I also ask what happens if our
      biggest deal slips, whether the commit deals are actually moving, whether each one has a next step the customer
      owns, how much is back-loaded into the last month, and whether we're creating new pipeline or just aging the old
      stuff.</p>
    <p>One habit I like: run the forecast once without your biggest deal. That's the plan I'd want to manage.</p>
    <div class="sheet">
      <h3>Worksheet: Team pipeline</h3>
      <p class="sheet-meta">Quarter __________ &nbsp; Date __________ &nbsp; <span class="sheet-tool">Online: quotabird.com</span></p>
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
    <p>I spent too much time early in management trying to give my boss more information. Usually they didn't need
      more information. They needed fewer surprises.</p>
    <p>My update fits on one page: the number (commit, best case, gap), what changed and why, what worries me, what I'm
      doing about it, and one ask with a date. Or "nothing this week." And I lead with the bad news. "Heads up before
      this shows up in the CRM" beats letting your boss discover it.</p>
    <p>I learned another one the expensive way. When somebody above me handed me a number I couldn't see, I used to
      say, "We'll find a way." Sometimes we did. Sometimes I spent the rest of the year explaining that sentence. Now
      I'd say, "Here's what I can commit to with what we have. Here's what would have to be true to get to your
      number." Then I show the math.</p>
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
    <h2>6. A struggling rep is a diagnosis before it's a verdict</h2>
    <p>Four very different problems can produce the same ugly dashboard.</p>
    <div class="mtable"><table><thead><tr><th>Problem</th><th>What it looks like</th><th>What I do</th></tr></thead><tbody>
      <tr><td>Bad situation</td><td>Good rep. Bad territory, quota, accounts or plan.</td><td>Fix the situation.</td></tr>
      <tr><td>Skill</td><td>They're working, customers engage, deals just aren't converting.</td><td>Coach. Sit in the room.</td></tr>
      <tr><td>Effort</td><td>They know how to sell. They're just not doing enough of it.</td><td>Set expectations clearly, in writing, with dates.</td></tr>
      <tr><td>Wrong fit</td><td>Fair patch, enough support, and neither the skill nor the effort is there.</td><td>Now it's a performance conversation, not a coaching conversation.</td></tr>
    </tbody></table></div>
    <p>I want to rule out the first three before I convince myself it's the fourth. I once spent months coaching
      somebody whose territory couldn't have produced the number for almost anyone. I'd like those months back. So
      would the rep.</p>
    <p class="sheet-tool">The rep diagnostic is in chapter 1. Online: quotabird.com/rep</p>
  </section>

  <section class="kit-ch" id="k-review">
    <h2>7. Review season: bring receipts</h2>
    <p>The calibration room didn't see your rep's whole year. It saw whatever case you brought into the room. That
      took me too long to appreciate.</p>
    <p>I keep a running note during the year: date, what happened, result. Nothing elaborate. Then review season isn't
      an archaeological dig through email and Slack.</p>
    <p>For each rep I want three meaningful results (with numbers where numbers make sense), what happened because this
      person was there, why the work was at their level, specific examples behind any behavior I'm going to claim, and
      the harder thing I'd trust them with next.</p>
    <p>Then I do one uncomfortable thing: I say the weakest part of my case first. It saves the room the trouble of
      finding it, and it makes everything else I say more credible.</p>
    <p>I also check myself. Am I overweighting the last sixty days? Would I see this person differently if I didn't
      personally like working with them? Take away their biggest win: does my view hold? Take away their worst month:
      same question.</p>
    <div class="sheet">
      <h3>Worksheet: Talent review prep</h3>
      <p class="sheet-meta">Rep ____________________ &nbsp; Level ______ &nbsp; <span class="sheet-tool">Online: quotabird.com/olr</span></p>
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
      <li><strong>Managing the dashboard.</strong> The CRM got cleaner. The pipeline didn't get bigger.</li>
      <li><strong>Saving the deal myself.</strong> Worked great once. Then the rep learned to wait for me.</li>
      <li><strong>Managing the average.</strong> Two reps at 6X and two at 1X is not a healthy team at 3.5X.</li>
      <li><strong>Forecasting confidence.</strong> Some people sound certain about everything. That's a personality trait, not deal evidence.</li>
      <li><strong>Waiting to deliver bad news.</strong> I wanted the fix before I told my boss. They'd have preferred the news Monday and the fix Friday.</li>
      <li><strong>Giving everyone the same 1:1.</strong> My best seller and my newest seller needed completely different things from those thirty minutes.</li>
      <li><strong>Discounting the wrong problem.</strong> I approved a discount when the real issue was access to power. We solved a price problem the customer didn't have.</li>
      <li><strong>Talking too much on customer calls.</strong> I thought I was helping the rep. Mostly I was teaching the customer to look at me instead of them.</li>
      <li><strong>Being the answer machine.</strong> Eventually everybody brought me problems and nobody brought me decisions.</li>
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
    <h2>10. When to leave the rep alone</h2>
    <p>Managers can hurt good sellers by managing them too much. I've done it.</p>
    <p>I leave them alone when customers call them back, when they create their own pipeline, when they know their
      deals better than I do, when they tell me bad news before I find it, when they ask for help when they actually
      need it, and when they make the number often enough that the system clearly works.</p>
    <p>My job isn't to turn my best rep into me. It's to make sure they have a fair patch, get the stuff that slows
      them down out of the way, help when they ask, and keep the rest of the company from improving them to death.</p>
  </section>
'''
KIT_CTA = '''
  <section class="kit-cta" aria-labelledby="kit-cta-h">
    <h2 id="kit-cta-h">Sometimes another set of eyes helps</h2>
    <p>I'm Mark. I carried a number, managed people who did, and led partner sales teams at AWS. I still like this stuff.
      If you're staring at a deal, a forecast, a rep problem or a number that doesn't make sense, I'm happy to talk.</p>
    <p class="kit-cta-terms">Twenty minutes. Free. No deck. No pitch.</p>
    <div class="btn-row kit-cta-row">
      <a class="btn btn-primary btn-lg" id="kitBook" href="https://calendly.com/markflournoy/chat-with-mark?utm_source=quotabird&amp;utm_medium=kit&amp;utm_content=kit_cta" target="_blank" rel="noopener">Chat with Mark</a>
      <a class="btn btn-lg" href="https://www.linkedin.com/in/markflournoy/" target="_blank" rel="noopener">DM on LinkedIn</a>
    </div>
    <p class="fine">And if I don't think I can help, I'll tell you.</p>
  </section>
'''
_kit_url = 'https://quotabird.com/kit/'
_kit_desc = "A free, printable field kit for sales managers: inheriting a team, one-on-ones, the forecast call, pipeline, your boss, a struggling rep, review season, and the worksheets that go with them."
_kit_ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": "The Sales Manager's Field Kit", "description": _kit_desc, "url": _kit_url, "isAccessibleForFree": True,
                      "dateModified": BUILD[:10], "image": "https://quotabird.com/card.jpg", "author": {"@type": "Person", "@id": "https://quotabird.com/#about", "name": "Mark Flournoy"},
                      "publisher": {"@type": "Organization", "name": "QuotaBird", "url": "https://quotabird.com/"}}, indent=2)
_kit = note_head("The Sales Manager's Field Kit", _kit_desc, _kit_url).replace("| QuotaBird</title>", "| Free Printable | QuotaBird</title>") + f'''<script type="application/ld+json">
{_kit_ld}
</script>
</head>
<body class="kit-page">

<div class="wrap">
  <header class="appbar"></header>
</div>
<article class="note kit">
  <span class="overline">Free printable</span>
  <h1>The Sales Manager's Field Kit</h1>
  <p class="dek">Stuff I wish somebody had handed me the first time I ran a team.</p>
  <div class="kit-promo kit-hero">
    <div class="kit-thumb" aria-hidden="true">
      <img class="kt-back" src="/kit/preview-2.jpg" alt="" width="480" height="622" decoding="async">
      <img class="kt-front" src="/kit/preview-1.jpg" alt="" width="480" height="622" decoding="async">
    </div>
    <div class="kit-promo-body">
      <span class="pill">Free printable</span>
      <p class="kit-hero-meta">8 pages, letter or A4. Ten short chapters and six worksheets. No email required.</p>
      <div class="kit-promo-actions">
        <a class="btn btn-primary btn-lg btn-icon" id="kitBookDl" href="/kit/managers-field-kit.pdf" download>Download the PDF<svg aria-hidden="true" viewBox="0 -960 960 960" width="20" height="20"><path fill="currentColor" d="M480-320 280-520l56-58 104 104v-326h80v326l104-104 56 58-200 200ZM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160H240Z"/></svg></a>
        <button class="btn btn-text" id="kitPrint" type="button">Print this page</button>
      </div>
    </div>
  </div>
{KIT_BODY}
{KIT_CTA}
</article>

''' + NOTE_TAIL.replace('Field Notes are part of', "The Sales Manager's Field Kit is part of").replace('</script>\n</body>', """document.getElementById('kitPrint').addEventListener('click', function () { if (window.qbTrack) window.qbTrack('kit_print'); window.print(); });
document.getElementById('kitBook').addEventListener('click', function () { if (window.qbTrack) window.qbTrack('kit_book'); });
</script>
</body>""")
assert '—' not in _kit and '–' not in _kit
os.makedirs('kit', exist_ok=True)
open('kit/index.html', 'w').write(_kit)
print('kit', len(_kit))


# ────────────────────────────── ABOUT ──────────────────────────────
os.makedirs('about', exist_ok=True)
open('about/index.html', 'w').write(note_head('About Mark', "Who's behind QuotaBird, the situations he sees most, and how to reach him. Twenty minutes, free, no deck required.", 'https://quotabird.com/about/').replace('<meta property="og:type" content="article">', '<meta property="og:type" content="profile">') + '''</head>
<body>

<div class="wrap">
  <header class="appbar"></header>
  <div id="screen">
    <span class="overline tool-name">QuotaBird</span>
    <h1>About Mark</h1>
    <p class="dek">Who's behind the tools, the situations I see most, and how to reach me.</p>
  </div>
</div>

<section class="band" id="about"></section>

''' + NOTE_TAIL.replace('Field Notes are part of', 'QuotaBird is'))

# ────────────────────────────── SHARED CHROME ──────────────────────────────
# Every page gets the same header and the same About section, from one source.
MARK_SRC = open('partials/mark.html').read()
MADEBY_SRC = open('partials/made-by.html').read()
KITCARD_SRC = open('partials/kit-card.html').read()
KITCARD_PAGES = {'index.html', 'rep/index.html', 'partner/index.html', 'olr/index.html', 'risk/index.html', 'notes/index.html', 'math/index.html', 'about/index.html'}
def root_of(path):
    if path == '404.html': return '/'
    return '../' * path.count('/')
def utm_of(path):
    return 'home' if path == 'index.html' else path.split('/')[0]
def current_of(path):
    return '/' if path == 'index.html' else '/' + path.rsplit('/', 1)[0] + '/'
def header(path):
    b = root_of(path)
    ask = '#ask' if path == 'about/index.html' else '/about/#ask'
    return f'''<header class="appbar">
    <a class="logo" href="/" aria-label="QuotaBird, home"><picture><source srcset="{b}logo-dark.svg" media="(prefers-color-scheme: dark)"><img class="brandmark" src="{b}logo.svg" alt="" width="39" height="34"></picture> QuotaBird</a>
    <nav class="topnav" aria-label="Site">
      {menu(current_of(path) if not path.startswith(('notes/', 'math/', 'kit/')) else '/' + path.split('/')[0] + '/')}
      <a class="toplink" href="/kit/">Free kit</a>
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
    ask = '#ask' if path == 'about/index.html' else '/about/#ask'
    if 'class="foot-nav"' not in s:
        s = s.replace('<footer class="sitefoot">', f'<footer class="sitefoot">\n  <p class="foot-nav"><a href="/">Tools</a><a href="/kit/">Free kit</a><a href="/math/">Sales Math</a><a href="/notes/">Field Notes</a><a href="/about/">About</a><a href="{ask}">Ask Mark</a></p>', 1)
    if path != '404.html':
        # the full story lives on the About page; every other page gets the short "Made by Mark" card
        src = MARK_SRC if path == 'about/index.html' else MADEBY_SRC
        mark = src.replace('{ROOT}', root_of(path)).replace('{UTM}', utm_of(path))
        if path in KITCARD_PAGES and 'kit-band' not in mark: mark = KITCARD_SRC + mark
        s = re.sub(r'<section class="band" id="(?:about|mark)"[^>]*>.*?</section>\n*', lambda m: mark, s, count=1, flags=re.S)
    open(path, 'w').write(s)
PAGES = ['index.html', 'deal/index.html', 'about/index.html'] + [f'{t["slug"]}/index.html' for t in (REP, PARTNER, TERRITORY, OLR, BRIEF, ACCOUNT, RISK, COMPETITION)] \
        + [f'{c["slug"]}/index.html' for c in CALCS] + ['notes/index.html'] + [f'notes/{n["slug"]}/index.html' for n in NOTES] + ['math/index.html'] + [f'math/{p["slug"]}/index.html' for p in MATH] + ['kit/index.html'] + ['404.html']
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
DESC = {'/': 'Pipeline Check: target, pipeline and win rate in, the gap out. 3X is a rule of thumb; your win rate says what you actually need.',
        '/deal/': 'Deal Check: five questions (customer, money, power, path, now) that separate proof from hopium in a federal deal.'}
for t in (REP, PARTNER, TERRITORY, OLR, BRIEF, ACCOUNT, RISK, COMPETITION): DESC['/' + t['slug'] + '/'] = t['name'] + ': ' + t['desc']
for c in CALCS: DESC['/' + c['slug'] + '/'] = c['name'] + ': ' + c['desc']
QUERIES = {'/': ['do I have enough pipeline to make my number', 'pipeline coverage calculator with my win rate', 'is 3X pipeline coverage enough'],
           '/deal/': ['is my deal real or hopium', 'qualify a federal sales deal before commit', 'what will my manager ask about this deal'],
           '/quota/': ['is my quota crazy', 'quota to OTE ratio for cloud sales', 'is my sales quota fair'],
           '/territory/': ['can my territory make the number', 'is my sales territory viable', 'new patch sizing check'],
           '/discount/': ['what does a discount cost me in commission', 'should I give a 15 percent discount', 'discount impact on margin and commission'],
           '/commission/': ['how much of my commission do I take home', 'commission take home after taxes', 'commission check calculator'],
           '/rep/': ['is it the rep or the territory', 'why is my sales rep underperforming', 'rep problem or patch problem'],
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
lines = ['# QuotaBird', '', '> Quick reality checks for people who carry a number: thirteen free, one-minute tools for sellers and sales managers (deals, pipeline, quota, territories, partners, reps, reviews), plus short field notes. Everything runs in the browser; nothing is stored. Built by Mark Flournoy, who led partner sales teams at AWS.', '',
         'The tools are plain web pages. Each asks five questions (yes / sort of / no) or takes a few numbers, then gives a verdict, the question a manager will ask, and one thing to do first. Shared results are encoded in the URL fragment; no accounts, no uploads, no AI.', '']
for g, items in groups:
    lines.append(f'## {g}'); lines.append('')
    for h, n, d in items:
        desc = DESC[h].split(': ', 1)[1]; lines.append(f'- [{n}]({site}{h}): {desc[0].upper() + desc[1:]} ({d[0].lower() + d[1:]}.)')
    lines.append('')
lines += ['## Free printable', '', f"- [The Sales Manager's Field Kit]({site}/kit/): a free, printable field kit for sales managers: inheriting a team, one-on-ones, the forecast call, pipeline, managing up, a struggling rep, review season, when to leave a rep alone, and six worksheets.", '', '## Sales Math Library', ''] + [f'- [{p["title"]}]({site}/math/{p["slug"]}/): {p["answer"]}' for p in MATH] + ['', '## Field Notes', ''] + [f'- [{n["title"]}]({site}/notes/{n["slug"]}/): {n["dek"]}' for n in NOTES] + ['', '## About', '', f'- [About Mark]({site}/about/): who is behind the tools, the situations he sees most, and how to book a free twenty-minute call.', '', '## Optional', '', f'- [Sitemap]({site}/sitemap.xml)', f'- [ai-catalog.json]({site}/.well-known/ai-catalog.json): ARD capability manifest listing the same tools.', '']
open('llms.txt', 'w').write('\n'.join(lines))
entries = []
for g, h, n, d in TOOLS:
    slug = 'pipeline' if h == '/' else h.strip('/')
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
