#!/usr/bin/env python3
"""Build fast, multilingual one-page websites for small tourism businesses.

    python3 build.py                 build every clients/*.json  -> site/<slug>/
    python3 build.py clients/x.json  build one client

Each language gets its own static page (site/<slug>/ and site/<slug>/<lang>/)
with hreflang links, so search engines index every language. No JavaScript is
needed to read the page. Photos live in clients/<slug>/ and are copied over.
"""
import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "site"
BASE_URL = "https://preparedmale.github.io/client-sites"

UI = {
    "en": dict(rooms="Rooms", stay="Stay", experiences="Experiences", gallery="Photos", reviews="Guests say",
               faq="Good to know", getting_here="Getting here", contact="Contact", per_night="per night",
               guests="guests", up_to="up to", write="Message us on WhatsApp", book="Check dates",
               map="Open in Google Maps", from_="from", reply="We usually reply within a few hours.",
               greeting="Hello! I found {name} online.", email="Email", menu="Menu", lang_name="English", sample="Sample website. This business is fictional.",
               story_l="Our story", contact_h="Write to us", your_wa="your WhatsApp number", your_email="your email", photos_by="Photos"),
    "ru": dict(rooms="Номера", stay="Проживание", experiences="Впечатления", gallery="Фото", reviews="Отзывы",
               faq="Полезно знать", getting_here="Как добраться", contact="Контакты", per_night="за ночь",
               guests="гостей", up_to="до", write="Написать в WhatsApp", book="Узнать о датах",
               map="Открыть в Google Maps", from_="от", reply="Обычно отвечаем в течение нескольких часов.",
               greeting="Здравствуйте! Нашёл(ла) {name} в интернете.", email="Почта", menu="Меню", lang_name="Русский", sample="Пример сайта. Это вымышленное заведение.",
               story_l="Наша история", contact_h="Напишите нам", your_wa="ваш номер WhatsApp", your_email="ваша почта", photos_by="Фото"),
    "ka": dict(rooms="ოთახები", stay="განთავსება", experiences="აქტივობები", gallery="ფოტოები", reviews="სტუმრების შეფასებები", faq="სასარგებლო ინფორმაცია", getting_here="როგორ მოგვაგნოთ", contact="კონტაქტი", per_night="ღამეში", guests="სტუმარი", up_to="მაქსიმუმ", write="მოგვწერეთ WhatsApp-ზე", book="თარიღების შემოწმება", map="Google Maps-ზე ნახვა", from_="საწყისი ფასი", reply="ჩვეულებრივ რამდენიმე საათში გპასუხობთ.", email="ელფოსტა", menu="მენიუ", lang_name="ქართული", sample="საცდელი საიტი. ეს ობიექტი გამოგონილია.", story_l="ჩვენი ისტორია", contact_h="მოგვწერეთ", your_wa="თქვენი WhatsApp ნომერი", your_email="თქვენი ელფოსტა", photos_by="ფოტო", greeting="გამარჯობა! {name} ინტერნეტში ვიპოვე."),
}

THEMES = {
    # display serif/grotesk, body sans, accent, paper, deep (contact band)
    "valley": dict(display="Cormorant Garamond", dw="300;400;500", body="Manrope", accent="#7b2a3e", paper="#f8f4ee", deep="#2a1a1c"),
    "mountain": dict(display="Fraunces", dw="300;400", body="Manrope", accent="#2c5a6e", paper="#f4f5f2", deep="#17222a"),
    "oldtown": dict(display="Instrument Serif", dw="400", body="Hanken Grotesk", accent="#9a4f1c", paper="#f7f1e8", deep="#2a1d14"),
    "steppe": dict(display="Bricolage Grotesque", dw="300;400;500", body="Hanken Grotesk", accent="#3d6b45", paper="#f3f3ec", deep="#1b231c"),
}

ARROW = '<span class="ic" aria-hidden="true"><svg viewBox="0 0 16 16" width="14" height="14"><path d="M4 12 12 4M6 4h6v6" fill="none" stroke="currentColor" stroke-width="1.3"/></svg></span>'
PLUS = '<svg class="pl" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M8 2v12M2 8h12" stroke="currentColor" stroke-width="1.2"/></svg>'




def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def t(value, lang):
    if isinstance(value, dict):
        return value.get(lang) or value.get("en") or next(iter(value.values()), "")
    return value if value is not None else ""


def digits(s):
    return "".join(ch for ch in str(s or "") if ch.isdigit())


def page_url(slug, lang, langs):
    return f"{BASE_URL}/{slug}/" + ("" if lang == langs[0] else f"{lang}/")


def render(d, lang, langs, prefix):
    u = UI.get(lang, UI["en"])
    th = THEMES.get(d.get("theme"), THEMES["valley"])
    name, town = d["name"], d.get("town", "")
    smp = d.get("sample")
    wa = digits(d.get("whatsapp"))
    wa_text = t(d.get("whatsapp_greeting"), lang) or u.get("greeting", "Hello! I found {name} online.").format(name=name)
    wa_link = f"https://wa.me/{wa}?text={html.escape(__import__('urllib.parse').parse.quote(wa_text))}" if wa else ""
    wa_tgt = ' target="_blank" rel="noopener"'
    if smp: wa_link, wa_tgt = "#contact", ""   # fictional samples: no live WhatsApp link to a number that may belong to someone
    cur = d.get("currency", "")
    desc = t(d.get("intro"), lang)
    photos = d.get("photos") or []
    hero_img = photos[0].get("file") if photos else None
    home = prefix + ("" if lang == langs[0] else lang + "/")
    fam = lambda f, w: "family=" + f.replace(" ", "+") + ":wght@" + w
    fonts = "&".join([fam(th["display"], th["dw"]), fam(th["body"], "400;500;600")]
                     + ([fam("Noto Serif Georgian", "300;400;500"), fam("Noto Sans Georgian", "400;500;600")] if "ka" in langs else []))

    sec_title = t(d.get("section_title"), lang) or (u["stay"] if d.get("kind") == "lodging" else u["rooms"])
    nav = []
    if d.get("rooms"): nav.append(("stay", sec_title))
    if d.get("experiences"): nav.append(("experiences", u["experiences"]))
    if len(photos) > 2: nav.append(("gallery", u["gallery"]))
    nav.append(("contact", u["contact"]))

    alt_links = "".join(f'<link rel="alternate" hreflang="{l}" href="{page_url(d["slug"], l, langs)}">' for l in langs)
    switch = "" if len(langs) < 2 else '<div class="langs">' + "".join(
        f'<a href="{prefix}{"" if l == langs[0] else l + "/"}" lang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{l.upper()}</a>' for l in langs) + "</div>"

    jsonld = {"@context": "https://schema.org", "@type": d.get("schema_type", "LodgingBusiness"), "name": name,
              "description": desc, "url": page_url(d["slug"], lang, langs),
              "address": {"@type": "PostalAddress", "addressLocality": town, "addressCountry": d.get("country_code", "")}}
    if d.get("whatsapp") and not smp: jsonld["telephone"] = d["whatsapp"]
    if d.get("email") and not smp: jsonld["email"] = d["email"]
    if d.get("price_range"): jsonld["priceRange"] = d["price_range"]
    if hero_img: jsonld["image"] = f"{BASE_URL}/{d['slug']}/{hero_img}"

    img = lambda p, cls="", lazy=True: f'<img class="{cls}" src="{prefix}{e(p["file"])}" alt="{e(t(p.get("alt"), lang))}"{" loading=\"lazy\"" if lazy else ""} decoding="async">'
    btn = lambda href, label, cls="btn": f'<a class="{cls}" href="{href}"{wa_tgt if href == wa_link else ""}><span>{e(label)}</span>{ARROW}</a>'
    price_from = (f'<p class="from">{e(u["from_"])} <b>{e(d["price_from"])} {e(cur)}</b> {e(u["per_night"]) if d.get("kind") == "lodging" else ""}</p>' if d.get("price_from") else "")

    s = []
    if smp: s.append(f'<div class="sample">{e(u["sample"])}</div>')
    s.append(f'<header class="nav" data-solid="0"><div class="pill"><a class="brand" href="{home}">{e(name)}</a>'
             f'<nav aria-label="{e(u["menu"])}">' + "".join(f'<a href="#{k}">{e(v)}</a>' for k, v in nav) + f"</nav>{switch}"
             + (f'<a class="mini" href="{wa_link}"{wa_tgt}>{e(u["book"])}</a>' if wa else "") + "</div></header>")

    # 1. hero
    s.append('<section class="hero">' + (f'<div class="hero-media">{img(photos[0], "kb", lazy=False)}</div>' if hero_img else "")
             + f'<div class="hero-in wrap"><p class="tag rv">{e(t(d.get("location_line"), lang))}</p>'
             f'<h1 class="rv">{e(t(d.get("headline"), lang))}</h1><div class="hero-foot rv"><p class="lead">{e(desc)}</p>'
             f'<div class="cta">{btn(wa_link, u["book"]) if wa else ""}{price_from}</div></div></div>'
             '<span class="scroll-cue" aria-hidden="true"></span></section>')

    # 2. facts
    if d.get("facts"):
        s.append('<section class="facts wrap">' + "".join(
            f'<div class="rv"><b>{e(f.get("value"))}</b><span>{e(t(f.get("label"), lang))}</span></div>' for f in d["facts"]) + "</section>")

    # 3. story + portrait
    story = t(d.get("story"), lang) or desc
    side = photos[1] if len(photos) > 1 else None
    s.append(f'<section class="story wrap{" has-side" if side else ""}"><div class="story-txt rv"><p class="tag dark">{e(u["story_l"])}</p>'
             f'<p class="big">{e(story)}</p></div>'
             + (f'<figure class="bezel tall rv"><div class="core">{img(side)}</div><figcaption>{e(t(side.get("alt"), lang))}</figcaption></figure>' if side else "")
             + "</section>")

    # 4. offerings
    if d.get("rooms"):
        rows = []
        with_photos = all(r.get("photo") for r in d["rooms"])
        for i, r in enumerate(d["rooms"], 1):
            meta = f'{e(u["up_to"])} {e(r["guests"])} {e(u["guests"])}' if r.get("guests") else ""
            feats = " · ".join(e(t(x, lang)) for x in (r.get("features") or []))
            price = (f'<p class="price"><b>{e(r["price"])} {e(cur)}</b><span>{e(r.get("unit") and t(r["unit"], lang) or (u["per_night"] if d.get("kind") == "lodging" else ""))}</span></p>' if r.get("price") else "")
            body = (f'<div class="o-body"><p class="num">{i:02d}</p><h3>{e(t(r.get("name"), lang))}</h3>'
                    f'<p>{e(t(r.get("text"), lang))}</p>' + (f'<p class="feats">{meta + (" · " if meta and feats else "") + feats}</p>' if meta or feats else "") + "</div>")
            if with_photos:
                rows.append(f'<article class="o-card rv"><div class="bezel"><div class="core"><img src="{prefix}{e(r["photo"])}" alt="" loading="lazy" decoding="async"></div></div>{body}{price}</article>')
            else:
                rows.append(f'<article class="o-row rv">{body}{price}</article>')
        s.append(f'<section id="stay" class="offer wrap"><div class="sec-head rv"><p class="tag dark">{e(name)}</p><h2>{e(sec_title)}</h2></div>'
                 f'<div class="{"o-grid" if with_photos else "o-list"}">{"".join(rows)}</div></section>')

    # 5. experiences
    if d.get("experiences"):
        items = "".join(f'<article class="x rv"><h3>{e(t(x.get("name"), lang))}</h3><p>{e(t(x.get("text"), lang))}</p>'
                        + (f'<p class="price sm"><b>{e(x["price"])} {e(cur)}</b><span>{e(t(x.get("unit"), lang))}</span></p>' if x.get("price") else "")
                        + "</article>" for x in d["experiences"])
        sched = d.get("schedule")
        tl = ("" if not sched else '<ol class="timeline rv">' + "".join(
            f'<li><time>{e(row[0])}</time><span>{e(t(row[1], lang))}</span></li>' for row in sched) + "</ol>")
        s.append(f'<section id="experiences" class="exp"><div class="wrap"><div class="sec-head rv"><p class="tag">{e(town)}</p><h2>{e(u["experiences"])}</h2></div>'
                 f'<div class="exp-grid{"" if tl else " solo"}"><div class="xs">{items}</div>{tl}</div></div></section>')

    # 6. gallery bento
    if len(photos) > 2:
        g = photos[2:6]
        s.append(f'<section id="gallery" class="gal wrap"><div class="sec-head rv"><h2>{e(u["gallery"])}</h2></div><div class="bento n{len(g)}">'
                 + "".join(f'<figure class="bezel rv"><div class="core">{img(p)}</div><figcaption>{e(t(p.get("alt"), lang))}</figcaption></figure>' for p in g)
                 + "</div></section>")

    # 7. faq + route
    if d.get("faq") or d.get("getting_here"):
        faq = "".join(f'<details class="rv"><summary>{e(t(q.get("q"), lang))}{PLUS}</summary><p>{e(t(q.get("a"), lang))}</p></details>' for q in (d.get("faq") or []))
        route = f'<aside class="route rv"><p class="tag dark">{e(u["getting_here"])}</p><p>{e(t(d["getting_here"], lang))}</p></aside>' if d.get("getting_here") else ""
        s.append(f'<section class="faq wrap"><div><h2 class="rv">{e(u["faq"])}</h2>{faq}</div>{route}</section>')

    # 8. contact band
    rows = []
    if d.get("whatsapp"): rows.append(f'<p><span class="k">WhatsApp</span><span class="v{" ph" if smp else ""}">{e(u["your_wa"] if smp else d["whatsapp"])}</span></p>')
    if d.get("email"): rows.append(f'<p><span class="k">{e(u["email"])}</span><span class="v{" ph" if smp else ""}">{e(u["your_email"] if smp else d["email"])}</span></p>')
    if d.get("address"): rows.append(f'<p><span class="k">⌖</span><span class="v">{e(t(d["address"], lang))}</span></p>')
    if str(d.get("maps_url", "")).startswith("https://"): rows.append(f'<p><a href="{e(d["maps_url"])}" target="_blank" rel="noopener">{e(u["map"])}</a></p>')
    s.append(f'<section id="contact" class="contact"><div class="wrap c-grid"><h2 class="rv">{e(u["contact_h"])}</h2>'
             f'<div class="rv">{"".join(rows)}<p class="muted">{e(u["reply"])}</p>{btn(wa_link, u["write"], "btn light") if wa else ""}</div></div>')
    creds = [p["credit"] for p in photos if p.get("credit")] + (d.get("extra_credits") or [])
    cred_line = ("" if not creds else f'<p class="credits">{e(u["photos_by"])}: ' + ", ".join(
        f'<a href="{e(c["page"])}" target="_blank" rel="noopener">{e(c["artist"])}</a> ({e(c["license"])})' for c in creds) + "</p>")
    s.append(f'<footer class="wrap"><div class="f-row"><span>© {e(name)} · {e(town)}</span><span>{e(d.get("credit", ""))}</span></div>{cred_line}</footer></section>')

    og_img = f'<meta property="og:image" content="{BASE_URL}/{d["slug"]}/{e(hero_img)}">' if hero_img else ""
    ka = '"Noto Serif Georgian",' if "ka" in langs else ""
    kb = '"Noto Sans Georgian",' if "ka" in langs else ""
    css = f"""
:root{{--paper:{th['paper']};--ink:#1d1a17;--muted:#6d665e;--hair:rgba(29,26,23,.12);--accent:{th['accent']};--deep:{th['deep']};
--display:"{th['display']}",{ka}Georgia,serif;--body:"{th['body']}",{kb}system-ui,-apple-system,"Segoe UI",sans-serif;--ease:cubic-bezier(.32,.72,0,1)}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:90px}}
body{{margin:0;background:var(--paper);color:var(--ink);font:400 16.5px/1.7 var(--body);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}}
body::after{{content:"";position:fixed;inset:0;pointer-events:none;z-index:90;opacity:.05;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}}
img{{max-width:100%;display:block}}a{{color:inherit}}:focus-visible{{outline:2px solid var(--accent);outline-offset:4px;border-radius:6px}}
.wrap{{width:min(1240px,100% - 2*clamp(20px,5vw,64px));margin-inline:auto}}
h1,h2,h3{{font-family:var(--display);font-weight:400;letter-spacing:-.015em;text-wrap:balance;margin:0}}
h2{{font-size:clamp(2.4rem,5.4vw,4.6rem);line-height:1}}h3{{font-size:clamp(1.5rem,2.4vw,2rem);line-height:1.1}}
p{{margin:0}}.muted{{color:var(--muted)}}
.tag{{display:inline-flex;align-items:center;gap:.5rem;font:500 .7rem/1 var(--body);letter-spacing:.22em;text-transform:uppercase;padding:.55rem .9rem;border-radius:99px;
background:rgba(255,255,255,.14);color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.28);backdrop-filter:blur(8px)}}
.tag.dark{{background:transparent;color:var(--accent);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 35%,transparent);backdrop-filter:none}}
:lang(ka) .tag{{text-transform:none;letter-spacing:.04em}}
.sample{{position:relative;z-index:60;background:var(--deep);color:rgba(255,255,255,.8);text-align:center;font-size:.75rem;letter-spacing:.06em;padding:.45rem 1rem}}
/* floating nav */
.nav{{position:fixed;top:clamp(36px,4vw,44px);left:0;right:0;z-index:50;display:flex;justify-content:center;pointer-events:none;transition:top .6s var(--ease)}}
.nav[data-solid="1"]{{top:12px}}
.pill{{pointer-events:auto;display:flex;align-items:center;gap:clamp(.8rem,2vw,1.8rem);padding:.5rem .5rem .5rem 1.4rem;border-radius:99px;color:#fff;
background:rgba(20,16,14,.28);box-shadow:inset 0 0 0 1px rgba(255,255,255,.18);backdrop-filter:blur(18px) saturate(1.4);transition:background .6s var(--ease),color .6s var(--ease)}}
.nav[data-solid="1"] .pill{{background:rgba(250,247,242,.82);color:var(--ink);box-shadow:inset 0 0 0 1px var(--hair),0 20px 40px -24px rgba(40,30,20,.25)}}
.brand{{font-family:var(--display);font-size:1.25rem;text-decoration:none;white-space:nowrap}}
.pill nav{{display:flex;gap:1.4rem;font-size:.88rem}}.pill nav a{{text-decoration:none;opacity:.78;transition:opacity .3s}}.pill nav a:hover{{opacity:1}}
.langs{{display:flex;gap:.15rem}}.langs a{{font-size:.7rem;font-weight:600;letter-spacing:.08em;text-decoration:none;padding:.35rem .55rem;border-radius:99px;opacity:.7}}
.langs a[aria-current]{{opacity:1;box-shadow:inset 0 0 0 1px currentColor}}
.mini{{font-size:.82rem;font-weight:600;text-decoration:none;padding:.65rem 1.1rem;border-radius:99px;background:#fff;color:var(--ink);white-space:nowrap}}
.nav[data-solid="1"] .mini{{background:var(--ink);color:#fff}}
/* hero */
.hero{{position:relative;min-height:100svh;display:flex;align-items:flex-end;color:#fff;background:var(--deep);overflow:hidden;margin-top:-1px}}
.hero-media{{position:absolute;inset:0}}.hero-media img{{width:100%;height:100%;object-fit:cover}}
.kb{{animation:kb 22s var(--ease) both}}@keyframes kb{{from{{transform:scale(1.12)}}to{{transform:scale(1)}}}}
.hero::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,8,6,.35) 0%,rgba(10,8,6,0) 28%,rgba(10,8,6,.1) 50%,rgba(10,8,6,.78) 100%)}}
.hero-in{{position:relative;z-index:2;padding-block:9rem clamp(3rem,7vw,5.5rem)}}
.hero h1{{font-size:clamp(3rem,8.6vw,8.2rem);line-height:.94;max-width:13ch;margin:1.4rem 0 2.2rem;font-weight:300}}
html[lang=ka] .hero h1{{font-size:clamp(2.3rem,5.6vw,5rem);line-height:1.08;max-width:16ch}}
.hero-foot{{display:flex;justify-content:space-between;align-items:flex-end;gap:2rem 4rem;flex-wrap:wrap}}
.lead{{max-width:46ch;font-size:clamp(1rem,1.4vw,1.15rem);color:rgba(255,255,255,.86)}}
.cta{{display:flex;align-items:center;gap:1.4rem;flex-wrap:wrap}}.from{{font-size:.9rem;color:rgba(255,255,255,.8)}}.from b{{color:#fff;font-weight:600}}
.btn{{display:inline-flex;align-items:center;gap:.9rem;padding:.45rem .45rem .45rem 1.5rem;border-radius:99px;background:#fff;color:var(--ink);text-decoration:none;font-weight:600;font-size:.95rem;
transition:transform .5s var(--ease),background .5s var(--ease)}}.btn:active{{transform:scale(.98)}}
.ic{{display:grid;place-items:center;width:2.4rem;height:2.4rem;border-radius:50%;background:var(--ink);color:#fff;transition:transform .5s var(--ease)}}
.btn:hover .ic{{transform:translate(2px,-2px) scale(1.06)}}.btn.light{{background:#fff}}.btn.light .ic{{background:var(--accent)}}
.scroll-cue{{position:absolute;left:50%;bottom:1.4rem;z-index:2;width:1px;height:48px;background:linear-gradient(rgba(255,255,255,.8),transparent);animation:cue 2.4s var(--ease) infinite}}
@keyframes cue{{0%{{transform:scaleY(0);transform-origin:top}}50%{{transform:scaleY(1);transform-origin:top}}51%{{transform-origin:bottom}}100%{{transform:scaleY(0);transform-origin:bottom}}}}
/* facts */
.facts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,160px),1fr));gap:2rem;padding-block:clamp(3rem,6vw,5rem);border-bottom:1px solid var(--hair)}}
.facts b{{display:block;white-space:nowrap;font-family:var(--display);font-weight:300;font-size:clamp(2rem,3.2vw,3.2rem);line-height:1;margin-bottom:.6rem}}
.facts span{{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}:lang(ka) .facts span{{text-transform:none;letter-spacing:.02em}}
/* story */
.story{{padding-block:clamp(6rem,12vw,11rem);display:grid;gap:clamp(3rem,7vw,7rem)}}
.story.has-side{{grid-template-columns:1.25fr .75fr;align-items:center}}
.big{{font-family:var(--display);font-weight:300;font-size:clamp(1.7rem,3.3vw,3rem);line-height:1.18;margin-top:2rem;letter-spacing:-.01em}}
html[lang=ka] .big{{font-size:clamp(1.4rem,2.6vw,2.2rem);line-height:1.35}}
.bezel{{margin:0;padding:.45rem;border-radius:1.6rem;background:rgba(29,26,23,.04);box-shadow:inset 0 0 0 1px rgba(29,26,23,.06)}}
.core{{border-radius:calc(1.6rem - .45rem);overflow:hidden;box-shadow:inset 0 1px 1px rgba(255,255,255,.2)}}
.core img{{width:100%;height:100%;object-fit:cover;transition:transform 1.4s var(--ease)}}.bezel:hover .core img{{transform:scale(1.04)}}
.tall .core{{aspect-ratio:4/5}}
figcaption{{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);padding:.9rem .5rem .3rem}}:lang(ka) figcaption{{text-transform:none;letter-spacing:.02em}}
/* offerings */
.offer{{padding-block:clamp(4rem,8vw,7rem) clamp(6rem,10vw,9rem)}}
.sec-head{{display:flex;flex-direction:column;align-items:flex-start;gap:1.4rem;margin-bottom:clamp(2.5rem,5vw,4.5rem)}}
.o-list{{border-top:1px solid var(--hair)}}
.o-row{{display:grid;grid-template-columns:1fr auto;gap:2rem;padding-block:2.4rem;border-bottom:1px solid var(--hair);align-items:start;transition:padding .6s var(--ease)}}
.o-row:hover{{padding-left:.8rem}}
.o-body{{display:grid;grid-template-columns:4.5rem 1fr;column-gap:1.5rem;row-gap:.6rem}}.o-body>*:not(.num){{grid-column:2}}
.num{{grid-row:span 3;font:500 .75rem/2.4 var(--body);letter-spacing:.2em;color:var(--accent)}}
.o-body p{{max-width:56ch;color:var(--muted)}}.feats{{font-size:.88rem}}
.price{{text-align:right;white-space:nowrap}}.price b{{display:block;font-family:var(--display);font-weight:400;font-size:clamp(1.8rem,2.6vw,2.4rem);line-height:1}}
.price span{{font-size:.78rem;color:var(--muted)}}.price.sm{{text-align:left;margin-top:.8rem}}.price.sm b{{font-size:1.5rem;display:inline;margin-right:.4rem}}
.o-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(1.2rem,2.4vw,2.2rem)}}
.o-card{{display:flex;flex-direction:column;gap:1.4rem}}.o-card .core{{aspect-ratio:4/5}}.o-card .o-body{{grid-template-columns:1fr}}.o-card .num{{grid-row:auto;line-height:1}}.o-card .o-body>*{{grid-column:1}}
.o-card .price{{text-align:left;margin-top:auto;padding-top:1rem;border-top:1px solid var(--hair)}}.o-card .price b{{display:inline;margin-right:.5rem}}
.o-card:nth-child(2){{margin-top:clamp(0rem,6vw,5rem)}}
/* experiences */
.exp{{background:var(--deep);color:#f4efe8;padding-block:clamp(6rem,11vw,10rem)}}
.exp .tag{{color:#f4efe8}}.exp-grid{{display:grid;grid-template-columns:1.2fr .8fr;gap:clamp(3rem,7vw,7rem);align-items:start}}
.xs{{display:grid;gap:2.6rem}}.solo{{grid-template-columns:1fr}}.solo .xs{{grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:2.6rem 4rem}}.x{{padding-top:1.6rem;border-top:1px solid rgba(255,255,255,.14)}}.x p{{color:rgba(244,239,232,.7);margin-top:.7rem;max-width:52ch}}
.x .price span{{color:rgba(244,239,232,.6)}}
.timeline{{list-style:none;margin:0;padding:1.8rem;border-radius:1.6rem;background:rgba(255,255,255,.04);box-shadow:inset 0 0 0 1px rgba(255,255,255,.1);position:sticky;top:110px}}
.timeline li{{display:grid;grid-template-columns:4.2rem 1fr;gap:1rem;padding:1rem 0;border-bottom:1px solid rgba(255,255,255,.1)}}.timeline li:last-child{{border:0}}
.timeline time{{font-family:var(--display);font-size:1.3rem;color:color-mix(in srgb,var(--accent) 45%,#fff)}}
/* gallery */
.gal{{padding-block:clamp(6rem,11vw,10rem)}}
.bento{{display:grid;grid-template-columns:repeat(12,1fr);grid-auto-rows:clamp(150px,17vw,250px);gap:clamp(.8rem,1.6vw,1.4rem)}}
.bento .bezel{{display:flex;flex-direction:column}}.bento .core{{flex:1;min-height:0}}
.bento figure:nth-child(1){{grid-column:span 7;grid-row:span 2}}.bento figure:nth-child(2){{grid-column:span 5;grid-row:span 1}}
.bento figure:nth-child(3){{grid-column:span 5;grid-row:span 1}}.bento figure:nth-child(4){{grid-column:3/span 8;grid-row:span 2}}
.bento figcaption{{padding:.6rem .4rem .1rem}}
/* faq */
.faq{{display:grid;grid-template-columns:1.3fr .7fr;gap:clamp(3rem,7vw,7rem);padding-block:clamp(4rem,8vw,7rem) clamp(6rem,10vw,9rem);align-items:start}}
.faq h2{{margin-bottom:2.5rem}}
details{{border-bottom:1px solid var(--hair)}}summary{{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:1rem;align-items:center;padding:1.5rem 0;font-family:var(--display);font-size:clamp(1.2rem,1.8vw,1.5rem)}}
summary::-webkit-details-marker{{display:none}}.pl{{flex:none;transition:transform .5s var(--ease);color:var(--accent)}}details[open] .pl{{transform:rotate(45deg)}}
details p{{padding:0 0 1.6rem;color:var(--muted);max-width:60ch}}
.route{{padding:2rem;border-radius:1.6rem;background:rgba(29,26,23,.04);box-shadow:inset 0 0 0 1px rgba(29,26,23,.06);position:sticky;top:110px}}.route p:last-child{{margin-top:1.2rem;color:var(--muted)}}
/* contact */
.contact{{background:var(--deep);color:#f4efe8;padding-top:clamp(6rem,12vw,11rem)}}
.c-grid{{display:grid;grid-template-columns:1.1fr .9fr;gap:3rem 6rem;align-items:end;padding-bottom:clamp(5rem,9vw,8rem)}}
.contact h2{{font-size:clamp(3rem,8vw,7.4rem);font-weight:300;line-height:.95}}
.c-grid p{{display:flex;gap:1.2rem;align-items:baseline;padding:.9rem 0;border-bottom:1px solid rgba(255,255,255,.12)}}
.k{{min-width:6rem;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:rgba(244,239,232,.55)}}.v{{font-size:1.05rem}}
.v.ph{{font-style:italic;color:rgba(244,239,232,.55)}}.contact .muted{{color:rgba(244,239,232,.55);border:0;font-size:.9rem;margin-bottom:1.8rem}}
footer{{padding-block:2rem 2.4rem;border-top:1px solid rgba(255,255,255,.12);color:rgba(244,239,232,.55);font-size:.8rem}}
.f-row{{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap}}.credits{{font-size:.7rem;margin-top:1rem;opacity:.7}}
/* reveal */
.js .rv{{opacity:0;transform:translateY(40px);filter:blur(6px);transition:opacity 1.1s var(--ease),transform 1.1s var(--ease),filter 1.1s var(--ease)}}
.js .rv.in{{opacity:1;transform:none;filter:none}}
@media (prefers-reduced-motion:reduce){{.js .rv{{opacity:1;transform:none;filter:none;transition:none}}.kb,.scroll-cue{{animation:none}}html{{scroll-behavior:auto}}}}
@media (max-width:900px){{.story.has-side,.exp-grid,.faq,.c-grid{{grid-template-columns:1fr}}.timeline,.route{{position:static}}
.o-grid{{grid-template-columns:1fr}}.o-card:nth-child(2){{margin-top:0}}.pill nav{{display:none}}}}
@media (max-width:640px){{body{{font-size:16px}}.mini,.scroll-cue{{display:none}}.pill{{max-width:calc(100% - 24px);padding-right:.4rem}}.facts{{grid-template-columns:1fr 1fr;gap:2rem 1rem}}.pill{{gap:.6rem;padding-left:1rem}}.brand{{font-size:1.05rem}}.langs a{{padding:.3rem .4rem}}.mini{{padding:.55rem .85rem;font-size:.78rem}}
.o-row{{grid-template-columns:1fr}}.price{{text-align:left}}.o-body{{grid-template-columns:1fr}}.num{{grid-row:auto}}.o-body>*:not(.num){{grid-column:1}}
.bento{{grid-template-columns:1fr 1fr;grid-auto-rows:150px}}.bento figure:nth-child(n){{grid-column:span 2;grid-row:span 2}}.bento figure:nth-child(2),.bento figure:nth-child(3){{grid-column:span 1;grid-row:span 1}}
.bento figure:nth-child(2) figcaption,.bento figure:nth-child(3) figcaption{{display:none}}.hero-in{{padding-top:7rem}}}}
"""
    js = """document.documentElement.classList.add('js');addEventListener('DOMContentLoaded',()=>{
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}}),{rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.rv').forEach((el,i)=>{el.style.transitionDelay=(el.closest('.hero')?i*120:((i%3)*90))+'ms';io.observe(el)});
const nav=document.querySelector('.nav'),hero=document.querySelector('.hero');
if(nav&&hero)new IntersectionObserver(([x])=>nav.dataset.solid=x.isIntersecting?'0':'1',{rootMargin:'-80px 0px 0px 0px'}).observe(hero)});"""
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(name)} · {e(town)}</title><meta name="description" content="{e(desc[:160])}"><meta name="theme-color" content="{th['deep']}">
<link rel="canonical" href="{page_url(d['slug'], lang, langs)}">{alt_links}
<meta property="og:type" content="website"><meta property="og:title" content="{e(name)}"><meta property="og:description" content="{e(desc[:200])}">{og_img}
{'<meta name="robots" content="noindex">' if smp else ''}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='14' fill='%23{th['accent'][1:]}'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">
{f'<link rel="preload" as="image" href="{prefix}{e(hero_img)}">' if hero_img else ''}
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False).replace("<", "\\u003c")}</script>
<script>{js}</script>
<style>{css}</style></head><body>
{''.join(s)}
</body></html>"""


def build(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    slug, langs = d["slug"], d.get("languages") or ["en"]
    out = OUT / slug
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for i, lang in enumerate(langs):
        target = out if i == 0 else out / lang
        target.mkdir(exist_ok=True)
        prefix = "./" if i == 0 else "../"
        (target / "index.html").write_text(render(d, lang, langs, prefix), encoding="utf-8")
    src = Path(path).resolve().parent / slug
    if src.is_dir():
        for f in src.iterdir():
            if f.is_file():
                shutil.copy(f, out / f.name)
    print(f"built {slug}: {', '.join(langs)}")
    return d


def index_page(clients):
    rows = "".join(f'<li><a href="./{e(c["slug"])}/">{e(c["name"])}</a></li>' for c in clients if not c.get("hidden"))
    (OUT / "index.html").write_text(f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>Sites</title><ul>{rows}</ul>', encoding="utf-8")
    (OUT / ".nojekyll").write_text("")


if __name__ == "__main__":
    files = sys.argv[1:] or sorted(str(p) for p in (ROOT / "clients").glob("*.json"))
    OUT.mkdir(exist_ok=True)
    built = [build(f) for f in files]
    if not sys.argv[1:]:
        import agency
        agency.write(OUT)
