"""Generates the three DR Experiences landing pages from one template.
Run: python3 build_sites.py  -> writes crew.html, getaway.html, celebrate.html next to this file."""
import html, os, json
OUT = os.path.dirname(os.path.abspath(__file__))
E = html.escape

TYPE_LABEL = {"REAL": "Real photo needed", "CREATED": "Created image", "PREF": "Created now · swap for real"}

def ph(pid, kind, desc, ratio="4/3", cls=""):
    return (f'<figure class="ph ph-{kind.lower()} {cls}" style="aspect-ratio:{ratio}">'
            f'<div class="ph-art" aria-hidden="true"></div>'
            f'<figcaption><span class="ph-id">{pid}</span><span class="ph-type">{TYPE_LABEL[kind]}</span>'
            f'<span class="ph-desc">{E(desc)}</span></figcaption></figure>')

CSS = r"""
:root{
  --bg:#F4F8F7; --surface:#FFFFFF; --ink:#0F1F1D; --muted:#4A5F5B; --line:#D3DFDB;
  --sea:#0E5C57; --sea-soft:#DCEDEA; --sun:#E9A13B; --on-photo:#FFFFFF; --scrim:rgba(6,22,20,.62);
  --ph-a:#9FD3CB; --ph-b:#F3C98B; --ph-c:#5FA9A0;
  --font-display:"Bricolage Grotesque", "Avenir Next", system-ui, sans-serif;
  --font-body:"Instrument Sans", "Helvetica Neue", Arial, sans-serif;
  --radius:14px;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0B1514; --surface:#12201E; --ink:#E6F0EE; --muted:#9BB1AC; --line:#22403B;
  --sea:#56C2B6; --sea-soft:#163330; --sun:#F0B55E; --scrim:rgba(4,12,11,.66);
  --ph-a:#1F5B54; --ph-b:#7A5B2E; --ph-c:#2D7A70; color-scheme:dark;}}
:root[data-theme="dark"]{
  --bg:#0B1514; --surface:#12201E; --ink:#E6F0EE; --muted:#9BB1AC; --line:#22403B;
  --sea:#56C2B6; --sea-soft:#163330; --sun:#F0B55E; --scrim:rgba(4,12,11,.66);
  --ph-a:#1F5B54; --ph-b:#7A5B2E; --ph-c:#2D7A70; color-scheme:dark;}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--font-body);font-size:17px;line-height:1.6}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--surface)}
.wrap{max-width:1120px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3{font-family:var(--font-display);line-height:1.08;text-wrap:balance;margin:0;letter-spacing:-.015em}
h1{font-size:clamp(2.3rem,6vw,4.2rem);font-weight:800}
h2{font-size:clamp(1.8rem,4vw,2.7rem);font-weight:750}
h3{font-size:1.2rem;font-weight:700}
p{margin:0}
a{color:var(--sea)}
.eyebrow{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--accent)}
section{padding-block:72px}
.sec-head{display:grid;gap:12px;max-width:62ch;margin-bottom:36px}
.sec-head p{color:var(--muted)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--accent);color:var(--accent-ink);font-weight:700;
  border:0;border-radius:999px;padding:14px 26px;font-size:1rem;text-decoration:none;cursor:pointer;font-family:var(--font-body)}
.btn:hover{filter:brightness(1.08)}
.btn:focus-visible,a:focus-visible,summary:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,.tile:focus-visible{outline:3px solid var(--sun);outline-offset:2px}
.preview-bar{background:var(--sun);color:#1B1203;font-size:.85rem;text-align:center}
.preview-bar .wrap{padding-block:7px}
/* top bar */
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--surface);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-block:12px}
.logo{font-family:var(--font-display);font-weight:800;font-size:1.25rem;color:var(--ink);text-decoration:none;letter-spacing:-.02em}
.logo span{color:var(--sea)}
.top nav{display:flex;align-items:center;gap:20px}
.top nav a.plain{color:var(--ink);text-decoration:none;font-weight:600;font-size:.95rem}
.top .btn{padding:10px 18px;font-size:.92rem}
@media (max-width:620px){.top nav a.plain{display:none}}
/* placeholders */
.ph{position:relative;margin:0;border-radius:var(--radius);overflow:hidden;max-width:100%;
  background:linear-gradient(170deg,var(--ph-b) 0%,var(--ph-a) 55%,var(--ph-c) 100%)}
.ph-art{position:absolute;inset:0;background:
  radial-gradient(circle at 78% 30%,rgba(255,255,255,.55) 0 7%,transparent 7.5%),
  repeating-linear-gradient(0deg,rgba(255,255,255,.12) 0 2px,transparent 2px 14px);
  -webkit-mask:linear-gradient(to bottom,#000 0 62%,transparent 62%);mask:linear-gradient(to bottom,#000 0 62%,transparent 62%)}
.ph::after{content:"";position:absolute;left:0;right:0;bottom:0;height:38%;
  background:repeating-linear-gradient(170deg,rgba(255,255,255,.18) 0 3px,transparent 3px 18px)}
.ph-real{outline:2px dashed var(--ink);outline-offset:-8px}
.ph figcaption{position:absolute;left:10px;right:10px;bottom:10px;z-index:1;display:flex;flex-wrap:wrap;gap:6px;align-items:center;
  background:var(--surface);color:var(--ink);border-radius:10px;padding:8px 10px;font-size:.76rem;line-height:1.35}
.ph-id{font-weight:800;font-family:ui-monospace,Menlo,monospace}
.ph-type{background:var(--sea-soft);color:var(--sea);border-radius:999px;padding:1px 8px;font-weight:700}
.ph-real .ph-type{background:var(--accent);color:var(--accent-ink)}
.ph-desc{flex-basis:100%;color:var(--muted)}
/* hero */
.hero{padding-block:24px 0}
.hero-frame{position:relative;border-radius:22px;overflow:hidden;min-height:560px;display:grid;align-items:end}
.hero-frame .ph{position:absolute;inset:0;border-radius:0;aspect-ratio:auto !important}
.hero-frame .ph figcaption{top:14px;bottom:auto;left:14px;right:auto;max-width:330px}
.hero-copy{position:relative;z-index:2;padding:40px clamp(20px,4vw,48px);display:grid;gap:18px;color:var(--on-photo);
  background:linear-gradient(to top,var(--scrim),transparent);width:100%}
.hero-copy>*{max-width:760px}
.hero-copy .eyebrow{color:var(--on-photo);opacity:.9}
.hero-copy p.sub{font-size:1.18rem;max-width:52ch}
.hero-price{display:flex;flex-wrap:wrap;align-items:center;gap:16px}
.hero-price .from{font-weight:700;font-size:1.05rem}
.hero-price .from b{font-family:var(--font-display);font-size:1.5rem}
/* story */
.story{display:grid;grid-template-columns:1.25fr .75fr;gap:48px;align-items:center}
.story-text{display:grid;gap:18px;font-size:1.13rem;max-width:62ch}
.story-text p:first-child::first-letter{font-family:var(--font-display);font-size:3.4em;float:left;line-height:.9;padding-right:8px;color:var(--accent)}
.story-text .close{font-family:var(--font-display);font-size:1.45rem;font-weight:700;line-height:1.25}
.chat{background:var(--surface);border:1px solid var(--line);border-radius:28px;padding:18px;display:grid;gap:10px;max-width:360px;justify-self:center;width:100%}
.chat .meta{font-size:.75rem;color:var(--muted);text-align:center}
.bubble{padding:10px 14px;border-radius:18px;max-width:85%;font-size:.95rem;line-height:1.4}
.bubble.me{background:var(--sea);color:var(--bg);justify-self:end;border-bottom-right-radius:4px}
.bubble.them{background:var(--sea-soft);color:var(--ink);border-bottom-left-radius:4px}
.chat .tag{font-size:.7rem;color:var(--muted)}
@media (max-width:820px){.story{grid-template-columns:1fr}}
/* included */
.band{background:var(--surface);border-block:1px solid var(--line)}
.incl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px 36px}
.incl div{display:grid;gap:6px;padding-top:16px;border-top:2px solid var(--accent)}
.incl p{color:var(--muted)}
.excl{margin-top:30px;font-size:.95rem;color:var(--muted)}
.excl b{color:var(--ink)}
@media (max-width:820px){.incl{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.incl{grid-template-columns:1fr}}
/* steps */
.steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;counter-reset:s}
.steps li{list-style:none;display:grid;gap:8px;counter-increment:s}
.steps li::before{content:counter(s);font-family:var(--font-display);font-weight:800;font-size:2.6rem;color:var(--accent);line-height:1}
.steps p{color:var(--muted)}
.steps{padding:0;margin:0}
@media (max-width:720px){.steps{grid-template-columns:1fr}}
/* team */
.team{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:18px}
.team article{display:grid;gap:10px;align-content:start}
.team .role{font-weight:700}
.team p{color:var(--muted);font-size:.93rem}
@media (max-width:980px){.team{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:620px){.team{grid-template-columns:repeat(2,minmax(0,1fr))}}
/* day */
.day{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
.day article{display:grid;gap:10px;align-content:start}
.day .when{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--accent)}
.day p{color:var(--muted);font-size:.95rem}
@media (max-width:900px){.day{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:480px){.day{grid-template-columns:1fr}}
/* excursions */
.exc{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.exc article{display:grid;gap:8px}
.exc h3{font-size:1.02rem}
@media (max-width:820px){.exc{grid-template-columns:repeat(2,minmax(0,1fr))}}
.note{margin-top:22px;color:var(--muted);font-size:.95rem}
/* compare */
.cmp-wrap{overflow-x:auto}
.cmp{width:100%;border-collapse:collapse;min-width:520px;font-size:.98rem}
.cmp th,.cmp td{padding:14px 16px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
.cmp thead th{font-family:var(--font-display);font-size:1.1rem}
.cmp td:first-child{font-weight:700;width:24%}
.cmp td:last-child{background:var(--sea-soft)}
.cmp thead th:last-child{background:var(--sea-soft);color:var(--sea)}
/* price */
.price{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.price-card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:28px;display:grid;gap:10px;align-content:start}
.price-card.main{border:2px solid var(--accent)}
.price-card .lbl{font-weight:700;color:var(--muted)}
.price-card .amt{font-family:var(--font-display);font-size:clamp(2.4rem,6vw,3.4rem);font-weight:800;line-height:1;font-variant-numeric:tabular-nums}
.price-card .amt small{font-size:.4em;font-weight:600;color:var(--muted)}
.fine{font-size:.85rem;color:var(--muted)}
.price-cta{margin-top:26px;display:flex;flex-wrap:wrap;gap:16px;align-items:center}
@media (max-width:720px){.price{grid-template-columns:1fr}}
/* bars */
.bars{display:grid;gap:12px;max-width:720px}
.bar{display:grid;grid-template-columns:110px 1fr;gap:12px;align-items:center}
.bar .track{background:var(--sea-soft);border-radius:999px;overflow:hidden}
.bar .fill{background:var(--accent);color:var(--accent-ink);font-weight:700;padding:8px 14px;border-radius:999px;font-variant-numeric:tabular-nums;white-space:nowrap}
/* tiles */
.tiles{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px}
.tile{all:unset;cursor:pointer;display:grid;gap:8px;border-radius:var(--radius)}
.tile b{font-family:var(--font-display);font-size:1.02rem}
.tile .ph figcaption{font-size:.68rem}
@media (max-width:900px){.tiles{grid-template-columns:repeat(2,minmax(0,1fr))}}
/* split band */
.split{display:grid;grid-template-columns:1fr 1fr;gap:36px;align-items:center}
.split .copy{display:grid;gap:14px}
.split .copy p{color:var(--muted);font-size:1.08rem}
@media (max-width:760px){.split{grid-template-columns:1fr}}
/* reviews */
.reviews{border:2px dashed var(--line);border-radius:var(--radius);padding:32px;display:grid;gap:10px;text-align:center;justify-items:center}
.reviews p{color:var(--muted);max-width:56ch}
/* faq */
.faq{display:grid;gap:10px;max-width:820px}
.faq details{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:4px 18px}
.faq summary{cursor:pointer;font-weight:700;padding:14px 0;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::after{content:"+";font-size:1.3rem;color:var(--accent);line-height:1}
.faq details[open] summary::after{content:"–"}
.faq details p{padding-bottom:16px;color:var(--muted)}
/* form */
.form-sec{background:var(--surface);border-top:1px solid var(--line)}
.form-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:48px}
.form-side{display:grid;gap:16px;align-content:start}
.form-side p{color:var(--muted)}
.form-side ul{margin:0;padding-left:20px;color:var(--muted);display:grid;gap:6px}
form{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.f{display:grid;gap:6px;min-width:0}
.f.full{grid-column:1/-1}
label,.legend{font-weight:600;font-size:.92rem}
.req{color:var(--accent)}
input,select,textarea{font:inherit;font-size:1rem;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:12px;width:100%}
textarea{min-height:96px;resize:vertical}
.check{display:grid;grid-template-columns:22px 1fr;gap:10px;align-items:start;font-weight:400;font-size:.88rem;color:var(--muted)}
.check input{width:20px;height:20px;margin-top:2px;padding:0}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips label{font-weight:500;border:1px solid var(--line);border-radius:999px;padding:8px 14px;cursor:pointer;background:var(--bg)}
.chips input{position:absolute;opacity:0;width:1px;height:1px}
.chips input:checked+span{color:var(--accent);font-weight:700}
.chips label:has(input:checked){border-color:var(--accent)}
.chips label:has(input:focus-visible){outline:3px solid var(--sun);outline-offset:2px}
form .btn{justify-self:start}
.hp{position:absolute;left:-9999px}
.thanks{background:var(--sea-soft);border-radius:var(--radius);padding:28px;display:grid;gap:12px}
.thanks h3{font-size:1.5rem}
.thanks .pv{font-size:.88rem;color:var(--muted);border-top:1px solid var(--line);padding-top:12px}
.err{color:#B3261E;font-size:.9rem}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .err{color:#FF8A80}}
:root[data-theme="dark"] .err{color:#FF8A80}
@media (max-width:820px){.form-grid{grid-template-columns:1fr}}
@media (max-width:560px){form{grid-template-columns:1fr}}
/* footer */
footer{padding-block:40px;font-size:.9rem;color:var(--muted)}
footer .wrap{display:grid;gap:14px}
footer .tagline{font-family:var(--font-display);font-size:1.3rem;font-weight:700;color:var(--ink)}
footer .links{display:flex;flex-wrap:wrap;gap:18px}
@media (prefers-reduced-motion: reduce){*{scroll-behavior:auto !important;transition:none !important}}
html{scroll-behavior:smooth}
"""

def page(p):
    a = p["accent"]
    tokens = (f':root{{--accent:{a[0]};--accent-ink:{a[1]}}}'
              f'@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--accent:{a[2]};--accent-ink:{a[3]}}}}}'
              f':root[data-theme="dark"]{{--accent:{a[2]};--accent-ink:{a[3]}}}')
    incl = [
        ("Private villa, private pool", "Your group has the whole villa, minutes from the beach. No shared pool, no wristbands."),
        ("Most meals made in your villa", "Breakfast and lunch fresh every full day. Your private chef cooks dinner every night but one, which we leave open for a night out."),
        ("Private car service", "Airport pickup and drop-off, and a driver for your scheduled outings, with security along for those outings."),
        ("A concierge team, day or night", "Your personal concierge, plus a 24/7 AI concierge assistant for instant answers."),
        ("Excursions for less", "Fishing, catamarans, golf, spa days and more, at least 15% below resort prices. Booked separately."),
        ("Welcome kit", "Waiting for you when you arrive, with local tips and emergency contacts."),
    ]
    team = [
        ("SH-10", "PREF", "Chef plating dinner for a group in the villa kitchen", "Private chef", p["team"][0]),
        ("SH-14", "REAL", "Headshot of your personal concierge (the VA), with first name", "Personal concierge", p["team"][1]),
        ("SH-11", "PREF", "Driver holding the SUV door as guests step out at night", "Driver", p["team"][2]),
        ("SH-13", "PREF", "Security walking a group from a venue to the SUV at night", "Security", p["team"][3]),
        ("SH-15", "PREF", "Housekeeper setting out breakfast by the pool", "Housekeeper & cook", p["team"][4]),
    ]
    faq = p["faq_extra"] + [
        ("Is this legit? How do I pay?", "You'll talk with a real person on our team before you pay anything. To reserve, you pay a 50% deposit by card through our secure checkout and sign our terms. The balance is due 30 days before you arrive."),
        ("What's not included?", "Flights, excursions, drinks and meals out (including your free night), gratuities and travel insurance. We recommend every guest buys their own travel insurance."),
        ("Who is my concierge?", "Your personal concierge handles your trip from booking to departure. Our AI concierge assistant is available 24/7 for quick answers, and anything it can't handle goes straight to your personal concierge and our team in the DR."),
        ("What if someone in the group cancels?", "Cancellations follow our published tiers, based on how many days before arrival you cancel. We'll walk you through them before you book. Date changes are possible for a rebooking fee, subject to availability."),
        ("How far is the beach?", "Our villas are minutes from the beach, and your driver can take you there on scheduled outings."),
        ("What about getting around safely?", "Your driver takes you to and from scheduled outings, security comes along, and your concierge always knows your plans. Your welcome kit includes local tips and emergency contacts."),
    ]
    occ_opts = "".join(f'<option>{E(o)}</option>' for o in p["occasions"])
    hero_ph = ph(p["hero_ph"][0], p["hero_ph"][1], p["hero_ph"][2], "16/9")
    story_ps = "".join(f"<p>{s}</p>" for s in p["story"])
    chat = "".join(f'<div class="bubble {w}">{E(t)}</div>' for w, t in p["chat"])
    incl_h = "".join(f'<div><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in incl)
    steps_h = "".join(f'<li><h3>{E(t)}</h3><p>{E(d)}</p></li>' for t, d in p["steps"])
    team_h = "".join(f'<article>{ph(i,k,d,"4/5")}<span class="role">{E(r)}</span><p>{E(l)}</p></article>' for i,k,d,r,l in team)
    day_h = "".join(f'<article>{ph(i,k,d,"4/3")}<span class="when">{E(w)}</span><h3>{E(t)}</h3><p>{E(x)}</p></article>' for w,t,x,i,k,d in p["day"])
    exc_h = "".join(f'<article>{ph(i,"PREF",d,"1/1")}<h3>{E(t)}</h3></article>' for t,i,d in p["exc"])
    cmp_h = "".join(f'<tr><td>{E(r)}</td><td>{E(x)}</td><td>{E(y)}</td></tr>' for r,x,y in p["cmp"])
    faq_h = "".join(f'<details><summary>{E(q)}</summary><p>{E(ans)}</p></details>' for q, ans in faq)
    pm, ps = p["price_main"], p["price_sec"]
    fine = "Flights, excursions, drinks and meals out, and gratuities not included. Your exact price depends on dates, group size and villa."
    return f"""<title>{E(p['title'])}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{E(p['meta'])}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600;700&display=swap">
<style>
/* Layout: one long scroll; photo-led hero, alternating plain and banded sections, form at the end. Accent changes per audience. */
{CSS}
{tokens}
</style>
<div class="preview-bar"><div class="wrap">Preview draft. Boxes marked with an ID are image placeholders; prices are from the current pricing model.</div></div>
<header class="top"><div class="wrap">
  <a class="logo" href="#top">DR <span>Experiences</span></a>
  <nav><a class="plain" href="#how">How it works</a><a class="plain" href="#pricing">Pricing</a><a class="btn" href="#contact">{E(p['cta'])}</a></nav>
</div></header>
<main id="top">
<section class="hero"><div class="wrap"><div class="hero-frame">
  {hero_ph}
  <div class="hero-copy">
    <span class="eyebrow">{E(p['eyebrow'])}</span>
    <h1>{E(p['h1'])}</h1>
    <p class="sub">{E(p['sub'])}</p>
    <div class="hero-price"><a class="btn" href="#contact">{E(p['cta'])}</a><span class="from">From <b>{pm[0]}</b>/person</span></div>
  </div>
</div></div></section>

<section><div class="wrap story">
  <div class="story-text">{story_ps}<p class="close">That's DR Experiences. Travel like the top 0.1%.</p></div>
  <div><div class="chat" role="img" aria-label="Example text conversation with the concierge">
    <span class="meta">Concierge · placeholder SH-07 (phone mockup)</span>{chat}
    <span class="tag">Example conversation</span></div></div>
</div></section>

<section class="band"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">What's included</span><h2>{E(p['incl_h'])}</h2></div>
  <div class="incl">{incl_h}</div>
  <p class="excl"><b>Not included:</b> flights, excursions, drinks and meals out, gratuities, travel insurance.</p>
</div></section>

<section id="how"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">How it works</span><h2>Three steps, and only one of them is packing.</h2></div>
  <ol class="steps">{steps_h}</ol>
</div></section>

<section class="band"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Your team</span><h2>{E(p['team_h'])}</h2><p>Every trip comes with the same team, matched to your dates.</p></div>
  <div class="team">{team_h}</div>
</div></section>

{p['extra_before_day']}

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{E(p['day_eyebrow'])}</span><h2>{E(p['day_h'])}</h2></div>
  <div class="day">{day_h}</div>
</div></section>

<section class="band"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Excursions</span><h2>{E(p['exc_h'])}</h2><p>Your concierge books them for you, at least 15% below resort prices, at times that suit your group instead of the tour bus.</p></div>
  <div class="exc">{exc_h}</div>
  <p class="note">Excursions are optional and priced separately, so you only pay for what your group wants to do.</p>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Villa vs. resort</span><h2>Same island. Very different trip.</h2></div>
  <div class="cmp-wrap"><table class="cmp"><thead><tr><th></th><th>Typical resort</th><th>DR Experiences</th></tr></thead><tbody>{cmp_h}</tbody></table></div>
</div></section>

{p['extra_before_price']}

<section id="pricing" class="band"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Pricing</span><h2>One price for the whole trip, split across your group.</h2><p>No resort fees and no surprise charges. Here's where groups start. Our team will send you an exact quote for your dates.</p></div>
  <div class="price">
    <div class="price-card main"><span class="lbl">{E(pm[1])}</span><span class="amt">{pm[0]}<small> /person</small></span><span class="fine">{E(pm[2])} {fine}</span></div>
    <div class="price-card"><span class="lbl">{E(ps[1])}</span><span class="amt">{ps[0]}<small> /person</small></span><span class="fine">{E(ps[2])} {fine}</span></div>
  </div>
  <div class="price-cta"><a class="btn" href="#contact">{E(p['cta'])}</a><span class="fine">50% deposit to reserve. Balance due 30 days before arrival.</span></div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Reviews</span><h2>From our guests</h2></div>
  <div class="reviews">{ph('SH-17','REAL','Guest photos and reviews, with written permission','16/5')}<p>Our first groups travel in early 2027. Real reviews from real guests will appear here, with their permission.</p></div>
</div></section>

<section class="band"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">FAQ</span><h2>Good questions</h2></div>
  <div class="faq">{faq_h}</div>
</div></section>

<section id="contact" class="form-sec"><div class="wrap form-grid">
  <div class="form-side">
    <span class="eyebrow">Talk to our team</span>
    <h2>{E(p['form_h'])}</h2>
    <p>Tell us a little about your group. A member of our sales team will reach out the way you prefer, usually within [X] business hours.</p>
    <ul><li>No payment needed to get a quote</li><li>Your price, split per person</li><li>Real answers from a real person</li></ul>
  </div>
  <div>
    <form id="lead" novalidate>
      <input type="hidden" id="f-page" name="page" value="{p['slug']}">
      <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
      <div class="f"><label for="f-first">First name <span class="req">*</span></label><input id="f-first" name="first" autocomplete="given-name" required></div>
      <div class="f"><label for="f-last">Last name <span class="req">*</span></label><input id="f-last" name="last" autocomplete="family-name" required></div>
      <div class="f"><label for="f-email">Email <span class="req">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
      <div class="f"><label for="f-phone">Mobile phone <span class="req">*</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
      <fieldset class="f full" style="border:0;padding:0;margin:0"><legend class="legend">Best way to reach you <span class="req">*</span></legend>
        <div class="chips" id="f-method">
          <label><input type="radio" name="method" value="Call" required><span>Call</span></label>
          <label><input type="radio" name="method" value="Text"><span>Text</span></label>
          <label><input type="radio" name="method" value="Email"><span>Email</span></label>
          <label><input type="radio" name="method" value="WhatsApp"><span>WhatsApp</span></label>
        </div></fieldset>
      <div class="f"><label for="f-time">Best time to reach you</label><select id="f-time" name="time"><option value="">Any time</option><option>Morning (ET)</option><option>Afternoon (ET)</option><option>Evening (ET)</option></select></div>
      <div class="f"><label for="f-size">Group size <span class="req">*</span></label><select id="f-size" name="size" required><option value="">Choose…</option><option>2</option><option>3–4</option><option>5–6</option><option>7–8</option><option>Not sure yet</option></select></div>
      <div class="f"><label for="f-occ">What's the occasion? <span class="req">*</span></label><select id="f-occ" name="occasion" required><option value="">Choose…</option>{occ_opts}</select></div>
      <div class="f"><label for="f-month">When are you thinking? <span class="req">*</span></label><input id="f-month" name="month" type="month" required></div>
      <div class="f"><label for="f-nights">How many nights?</label><select id="f-nights" name="nights"><option value="">Not sure</option><option>3</option><option>4</option><option>5</option><option>6</option></select></div>
      <div class="f"><label for="f-from">Flying from</label><select id="f-from" name="from"><option value="">Choose…</option><option>Philadelphia (PHL)</option><option>DC area (DCA / IAD / BWI)</option><option>Atlanta (ATL)</option><option>New Jersey (EWR)</option><option>New York (JFK / LGA)</option><option>Other</option></select></div>
      <div class="f full"><label class="check"><input type="checkbox" id="f-flex" name="flexible"><span>Our dates are flexible</span></label></div>
      <div class="f full"><label for="f-notes">Anything we should know?</label><textarea id="f-notes" name="notes" placeholder="Birthdays, dietary needs, excursions you're curious about…"></textarea></div>
      <div class="f full"><label for="f-heard">How did you hear about us?</label><select id="f-heard" name="heard"><option value="">Choose…</option><option>Instagram</option><option>Facebook</option><option>A friend</option><option>Google</option><option>Other</option></select></div>
      <div class="f full"><label class="check"><input type="checkbox" id="f-sms" name="sms"><span>I agree to receive text messages from DR Experiences about my trip inquiry. Message and data rates may apply. Reply STOP to opt out. Consent isn't required to get a quote.</span></label></div>
      <div class="f full"><label class="check"><input type="checkbox" id="f-news" name="news"><span>Send me occasional emails with open dates and offers. Unsubscribe any time.</span></label></div>
      <p class="err f full" id="f-err" hidden>Please fill in the fields marked with *.</p>
      <button class="btn" type="submit">{E(p['cta'])}</button>
    </form>
    <div class="thanks" id="thanks" hidden tabindex="-1">
      <h3>Got it, <span id="t-name"></span>!</h3>
      <p>A member of our team will reach out by <b id="t-method"></b> within [X] business hours to start planning your trip.</p>
      <p class="pv">Preview: this form isn't connected to the sales team yet, so nothing was sent. On the live site it will create a lead in the CRM and alert the team.</p>
    </div>
  </div>
</div></section>
</main>
<footer><div class="wrap">
  <span class="tagline">DR Experiences. Travel like the top 0.1%.</span>
  <div class="links"><span>Terms</span><span>Privacy</span><span>Guest conduct policy</span><span>[EMAIL]</span><span>[PHONE]</span><span>[BUSINESS ADDRESS]</span><span>@[HANDLE]</span></div>
  <span>Private villa group trips to the Dominican Republic. Prices shown are per person and depend on group size, dates and villa.</span>
</div></footer>
<script>
(function(){{
  var form=document.getElementById('lead'),err=document.getElementById('f-err'),thanks=document.getElementById('thanks');
  form.addEventListener('submit',function(e){{
    e.preventDefault();
    if(document.getElementById('f-web').value){{return;}}
    if(!form.checkValidity()){{err.hidden=false;form.reportValidity();return;}}
    err.hidden=true;
    document.getElementById('t-name').textContent=document.getElementById('f-first').value.trim();
    var m=form.querySelector('input[name=method]:checked');
    document.getElementById('t-method').textContent=m?m.value.toLowerCase():'your preferred method';
    form.hidden=true;thanks.hidden=false;thanks.focus();
  }});
  document.querySelectorAll('[data-occ]').forEach(function(t){{
    t.addEventListener('click',function(){{
      var s=document.getElementById('f-occ');s.value=t.getAttribute('data-occ');
      document.getElementById('contact').scrollIntoView();
    }});
  }});
}})();
</script>
"""

CREW = dict(
    slug="crew", title="DR Experiences Crew Trips",
    meta="Your crew, a private villa with a pool, a chef, a driver and a concierge on call. One price, split by the group. From $1,320/person.",
    accent=("#1F2E4D", "#FFFFFF", "#9DB4E0", "#0B1424"),
    eyebrow="Private villa guys trips · Dominican Republic",
    h1="The trip your group chat keeps talking about. Done.",
    sub="Private villa. Private chef. A driver and a concierge on call. You just show up.",
    cta="Get my group's price",
    hero_ph=("CR-01", "REAL", "Video loop: 4–6 guys arriving at the villa, first look at the pool"),
    story=[
        "Imagine your feet in the pool. It's 86 degrees, there's a breeze, and Dominican music is playing while you and your boys laugh about the ride back from today's excursion, when you told your driver to pull over at a random roadside chimi stand.",
        "Someone says it's time to go out. You text your concierge that you want a lounge where you can relax and have a good night. Thirty seconds later: <i>\"Done. Your driver has the details and will be outside when you're ready.\"</i>",
        "You finish your drink, get dressed, and your driver takes you straight to your VIP table. Security comes along, and the driver is waiting when the night is over.",
    ],
    chat=[("me", "Lounge tonight for the 4 of us? Somewhere chill, good music."), ("them", "Done. Your driver has the details and will be outside at 10:30. Table's reserved under your name.")],
    incl_h="Everything handled, so the only plan is to show up.",
    steps=[("Tell us about your crew", "Group size, rough dates, and what you're celebrating, if anything."), ("Get your all-in price", "We send one price for the trip, split per person, so everyone knows their share."), ("Pack a bag", "Your driver meets you at the airport. We handle everything else.")],
    team_h="The team that makes it run.",
    team=["Dinner in the villa every night but one. Grilled fish, steak, whatever the group wants.", "Your point of contact from booking to wheels-up.", "Airport pickup, nights out, the random roadside stop. He knows the island.", "Along for your scheduled outings, so you can focus on the night.", "Breakfast by the pool every morning, lunch ready when you're back."],
    day_eyebrow="A day in the life", day_h="Pool, ocean, dinner, night out. Repeat.",
    day=[("Morning", "Breakfast by the pool", "Coffee, eggs, fresh fruit. Nobody has to cook.", "CR-03", "PREF", "Breakfast spread by the pool, guys trip"),
         ("Afternoon", "Fishing or golf", "Deep-sea charter or a tee time, booked by your concierge.", "CR-04", "PREF", "Deep-sea fishing catch or golf course"),
         ("Evening", "Chef's dinner", "Dinner on the terrace, cooked in your villa.", "SH-05", "REAL", "Villa dining table set for dinner"),
         ("Night", "VIP table", "Lounges and rooftops. Your driver gets you there and back.", "CR-05", "CREATED", "Friends at a VIP lounge table (illustrative)")],
    exc_h="Fishing, golf, catamarans and more.",
    exc=[("Deep-sea fishing", "CR-06", "Fishing charter excursion"), ("Golf", "CR-07", "Golf course excursion"), ("ATVs & dune buggies", "CR-08", "ATV excursion"), ("Cigar factory tour", "CR-09", "Cigar tour excursion")],
    cmp=[("Space", "Shared pool, lobby and beach", "The whole villa is yours"), ("Getting around", "Shuttle buses and taxi lines", "Your own driver, on your schedule"), ("Food", "Buffet lines and reservations", "A private chef in your kitchen"), ("Price", "Room rate plus resort fees and add-ons", "One all-in price, split by the group")],
    extra_before_day="""<section><div class="wrap split">
  <div class="copy"><span class="eyebrow">Nights out</span><h2>Lounges, rooftops, VIP tables.</h2><p>Your concierge books it, your driver gets you there and back, and security comes along on scheduled outings. Your only job is to decide what time you're leaving.</p></div>
  """ + ph("CR-02", "PREF", "Guys with feet in the pool, laughing, drinks in hand", "4/3") + """
</div></section>""",
    extra_before_price="",
    price_main=("$1,320", "Crew of 8 · 3 nights", "Based on 8 guests sharing a 4-bedroom villa."),
    price_sec=("$1,880", "Crew of 4 · 4 nights", "Based on 4 guests sharing a 2-bedroom villa."),
    faq_extra=[("Can we add people later?", "Usually, yes. Bigger groups move into a bigger villa and the per-person price drops. Tell our team and we'll requote."),
               ("What about nightlife?", "Your concierge can book lounges, rooftops and VIP tables, and your driver takes you there and brings you back. Drinks and table minimums are paid separately.")],
    occasions=["Guys trip", "Birthday", "Bachelor party", "Reunion", "Golf or fishing trip", "Just because"],
    form_h="Get your crew's price.",
)

GETAWAY = dict(
    slug="getaway", title="DR Experiences Getaways",
    meta="A private villa, a private pool, most meals made in your villa and a concierge a text away. Nobody asks you for anything. From $1,510/person.",
    accent=("#C4503F", "#FFFFFF", "#F2958A", "#2A0D08"),
    eyebrow="Girls' trips & moms' getaways · Dominican Republic",
    h1="Four days where nobody needs anything from you.",
    sub="A private villa, a private chef, and a concierge team that handles every detail.",
    cta="Get my group's price",
    hero_ph=("GW-01", "REAL", "Video loop: 4 women arriving, first look at the pool"),
    story=[
        "Imagine your feet in the pool. It's 86 degrees, there's a breeze, Dominican music is playing, and you're laughing with your girls about this afternoon, when you asked the driver to stop at a roadside fruit stand and he knew the best one.",
        "Breakfast this morning? Someone else made it. Lunch? Ready when you got back from the catamaran. Tonight you text your concierge for a rooftop lounge where you can relax and have fun. A minute later: <i>\"Done. Your driver will be outside when you're ready.\"</i>",
        "You finish your drink, get dressed, and your driver takes you straight to your table. Security comes along, and the driver is waiting when you're ready to head back.",
    ],
    chat=[("me", "Can we do a spa morning tomorrow for 4? Then a rooftop at night 🙏"), ("them", "Done. Spa at 10am, driver picks you up at 9:30. Rooftop table is booked for 9pm.")],
    incl_h="Everything taken care of. Truly everything.",
    steps=[("Tell us about your group", "Who's coming, rough dates, and what you're celebrating or escaping."), ("Get your all-in price", "One price for the trip, split per person. Easy to send to the group chat."), ("Pack a bag", "Your driver meets you at the airport. We handle everything else.")],
    team_h="The people taking care of you.",
    team=["Dinner in the villa every night but one, made around your dietary needs.", "Your point of contact from booking to departure.", "Airport pickup, beach days, nights out. Always on time.", "Along for your scheduled outings, so you can just enjoy the night.", "Breakfast you didn't make, every single morning."],
    day_eyebrow="A day in the life", day_h="Slow morning, beautiful afternoon, good night.",
    day=[("Morning", "A long breakfast", "Fresh fruit, coffee, and nowhere to be.", "GW-03", "PREF", "Long breakfast table with fruit and coffee"),
         ("Afternoon", "Catamaran or spa", "Out on the water, or a massage. Or both.", "GW-04", "PREF", "Catamaran or Saona Island excursion"),
         ("Evening", "Chef's dinner", "Dinner on the terrace, cooked in your villa.", "SH-05", "REAL", "Villa dining table set for dinner"),
         ("Night", "Rooftop lounge", "Dressed up, driven there, driven home.", "GW-06", "CREATED", "Friends at a rooftop lounge (illustrative)")],
    exc_h="Catamarans, spa days, Saona Island and more.",
    exc=[("Saona Island", "GW-07", "Saona Island excursion"), ("Horseback on the beach", "GW-08", "Horseback riding excursion"), ("Cooking class", "GW-09", "Dominican cooking class"), ("Spa day", "GW-10", "Spa day excursion")],
    cmp=[("Space", "Fighting for pool chairs", "Your own private pool"), ("Food", "Buffet lines and reservations", "A private chef in your kitchen"), ("Planning", "You figure it all out", "Your concierge handles it"), ("Price", "Room rate plus resort fees and add-ons", "One all-in price, split by the group")],
    extra_before_day="",
    extra_before_price="""<section class="band"><div class="wrap split">
  """ + ph("GW-11", "CREATED", "A woman alone on a pool lounger with a book (illustrative)", "16/10") + """
  <div class="copy"><span class="eyebrow">For moms</span><h2>The moms' reset.</h2><p>Thursday to Sunday in your own villa. Meals made for you, a pool to yourself, and back home before anyone notices you were gone.</p><a class="btn" href="#contact" data-occ="Moms' getaway" style="justify-self:start">Plan a moms' getaway</a></div>
</div></section>""",
    price_main=("$1,510", "4 friends · 3 nights", "Based on 4 guests sharing a 2-bedroom villa."),
    price_sec=("$1,880", "4 friends · 4 nights", "Based on 4 guests sharing a 2-bedroom villa."),
    faq_extra=[("Can the chef handle dietary needs?", "Yes. Tell us about allergies and preferences when you book, and your chef will plan around them."),
               ("Do we have to go out, or can we stay in?", "Completely up to you. Some groups never leave the pool. Excursions and nights out are optional."),
               ("Can we bring kids?", "These trips are designed for adults. Ask our team about your group and we'll let you know what works.")],
    occasions=["Girls' trip", "Moms' getaway", "Birthday", "Bachelorette", "Reunion", "Just because"],
    form_h="Get your group's price.",
)

CELEB = dict(
    slug="celebrate", title="DR Experiences Celebrations",
    meta="Turn 40, 50 or a new chapter into a private villa trip with your people. Chef, driver, concierge, VIP nights. From $1,320/person.",
    accent=("#9A6B12", "#FFFFFF", "#E6BC62", "#241703"),
    eyebrow="Birthday & celebration trips · Dominican Republic",
    h1="Some birthdays deserve a villa.",
    sub="Bring your people. We'll bring the chef, the driver, the concierge and the plan.",
    cta="Plan my celebration",
    hero_ph=("CE-01", "REAL", "Video loop: group of 6–8 toasting at the villa pool at sunset"),
    story=[
        "Imagine your feet in the pool. It's 86 degrees, there's a breeze, Dominican music is playing, and everyone you love is laughing about the ride back from today's catamaran, when you made the driver stop for empanadas.",
        "Tonight is the night. Your chef brings out dinner on the terrace, then the cake. Someone gives a toast that makes everyone cry a little. Then you text your concierge: <i>\"We're ready to go out.\"</i> Thirty seconds later: <i>\"Done. Your driver is outside.\"</i>",
        "Your driver takes the whole group to your VIP table. Security comes along, and the driver is waiting when the night is over.",
    ],
    chat=[("me", "Birthday dinner tonight, then VIP table for 8 after? 🎉"), ("them", "Done. Cake is with the chef for 8pm. Table's booked for 10:30 and your driver will be outside.")],
    incl_h="The whole celebration, handled.",
    steps=[("Tell us the occasion", "What you're celebrating, who's coming and roughly when."), ("Get your all-in price", "One price for the trip, split per person. Easy to share with everyone."), ("Pack a bag", "Your driver meets you at the airport. We handle the rest.")],
    team_h="The team behind the celebration.",
    team=["Your birthday dinner, cooked in your villa.", "Your point of contact from booking to departure.", "Airport pickup, nights out, and every stop in between.", "Along for your scheduled outings, so everyone can just celebrate.", "Breakfast by the pool every morning after."],
    day_eyebrow="The celebration night", day_h="From the pool toast to the VIP table.",
    day=[("Sunset", "Pool toast", "Everyone together, golden hour, the first toast of the night.", "CE-01", "REAL", "Group toasting at the pool at sunset"),
         ("Dinner", "Chef's celebration dinner", "A decorated table on the terrace, cooked in your villa.", "CE-08", "PREF", "Decorated celebration dinner table"),
         ("Dessert", "The cake moment", "Your chef brings it out. Phones come out.", "CE-07", "PREF", "Chef bringing out a birthday cake"),
         ("Night", "VIP table", "Your driver takes the whole group out and brings everyone home.", "CR-05", "CREATED", "Group at a VIP lounge table (illustrative)")],
    exc_h="Catamarans, fishing, spa days and more.",
    exc=[("Catamaran", "GW-04", "Catamaran excursion"), ("Deep-sea fishing", "CR-06", "Fishing charter excursion"), ("Saona Island", "GW-07", "Saona Island excursion"), ("Spa day", "GW-10", "Spa day excursion")],
    cmp=[("Space", "Shared pool, lobby and beach", "The whole villa is yours"), ("The big night", "A table at the resort restaurant", "Your chef, your terrace, your cake"), ("Getting around", "Shuttle buses and taxi lines", "Your own driver for the whole group"), ("Price", "Room rate plus resort fees and add-ons", "One all-in price, split by the group")],
    extra_before_day="""<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">What are you celebrating?</span><h2>Pick your occasion.</h2><p>Tap one and we'll fill it in on your inquiry.</p></div>
  <div class="tiles">
    <button class="tile" type="button" data-occ="Milestone birthday">""" + ph("CE-02", "CREATED", "“40” balloons at the pool (illustrative)", "1/1") + """<b>40th · 50th</b></button>
    <button class="tile" type="button" data-occ="New chapter / divorce party">""" + ph("CE-03", "CREATED", "Champagne toast (illustrative)", "1/1") + """<b>New chapter</b></button>
    <button class="tile" type="button" data-occ="Reunion">""" + ph("CE-04", "CREATED", "Reunion group photo (illustrative)", "1/1") + """<b>Reunion</b></button>
    <button class="tile" type="button" data-occ="Anniversary">""" + ph("CE-05", "CREATED", "Anniversary dinner (illustrative)", "1/1") + """<b>Anniversary</b></button>
    <button class="tile" type="button" data-occ="Retirement / promotion">""" + ph("CE-06", "CREATED", "Retirement toast (illustrative)", "1/1") + """<b>Retirement · promotion</b></button>
  </div>
</div></section>""",
    extra_before_price="""<section class="band"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Bigger group, better price</span><h2>More of you, less each.</h2><p>Price per person for a 4-night trip.</p></div>
  <div class="bars">
    <div class="bar"><b>4 guests</b><div class="track"><div class="fill" style="width:100%">$1,880</div></div></div>
    <div class="bar"><b>6 guests</b><div class="track"><div class="fill" style="width:91.5%">$1,720</div></div></div>
    <div class="bar"><b>8 guests</b><div class="track"><div class="fill" style="width:87.5%">$1,645</div></div></div>
  </div>
</div></section>""",
    price_main=("$1,320", "8 guests · 3 nights", "Based on 8 guests sharing a 4-bedroom villa."),
    price_sec=("$1,720", "6 guests · 4 nights", "Based on 6 guests sharing a 3-bedroom villa."),
    faq_extra=[("Can you help with a cake or decorations?", "Yes. Tell us what you have in mind and our team will arrange it. Extras like decor or a photographer are priced separately."),
               ("Can people arrive on different days?", "Usually, yes. Your driver will handle each airport pickup. Let our team know when you ask for your quote."),
               ("Can everyone pay their own share?", "Ask our team. We'll walk you through how to handle payment across your group when we send your quote.")],
    occasions=["Milestone birthday", "New chapter / divorce party", "Reunion", "Anniversary", "Retirement / promotion", "Other"],
    form_h="Let's plan your celebration.",
)

for p in (CREW, GETAWAY, CELEB):
    with open(os.path.join(OUT, p["slug"] + ".html"), "w") as f:
        f.write(page(p))
print("built")
