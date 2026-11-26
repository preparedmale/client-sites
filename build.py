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
               your_wa="your WhatsApp number", your_email="your email", photos_by="Photos"),
    "ru": dict(rooms="Номера", stay="Проживание", experiences="Впечатления", gallery="Фото", reviews="Отзывы",
               faq="Полезно знать", getting_here="Как добраться", contact="Контакты", per_night="за ночь",
               guests="гостей", up_to="до", write="Написать в WhatsApp", book="Узнать о датах",
               map="Открыть в Google Maps", from_="от", reply="Обычно отвечаем в течение нескольких часов.",
               greeting="Здравствуйте! Нашёл(ла) {name} в интернете.", email="Почта", menu="Меню", lang_name="Русский", sample="Пример сайта. Это вымышленное заведение.",
               your_wa="ваш номер WhatsApp", your_email="ваша почта", photos_by="Фото"),
    "ka": dict(rooms="ოთახები", stay="განთავსება", experiences="აქტივობები", gallery="ფოტოები", reviews="სტუმრების შეფასებები", faq="სასარგებლო ინფორმაცია", getting_here="როგორ მოგვაგნოთ", contact="კონტაქტი", per_night="ღამეში", guests="სტუმარი", up_to="მაქსიმუმ", write="მოგვწერეთ WhatsApp-ზე", book="თარიღების შემოწმება", map="Google Maps-ზე ნახვა", from_="საწყისი ფასი", reply="ჩვეულებრივ რამდენიმე საათში გპასუხობთ.", email="ელფოსტა", menu="მენიუ", lang_name="ქართული", sample="საცდელი საიტი. ეს ობიექტი გამოგონილია.", your_wa="თქვენი WhatsApp ნომერი", your_email="თქვენი ელფოსტა", photos_by="ფოტო", greeting="გამარჯობა! {name} ინტერნეტში ვიპოვე."),
}

THEMES = {
    # display font, body font, colours (light / dark), hero scene
    "valley": dict(display="Literata", body="Inter", accent="#7a2440", accent_d="#ec9bb5", ink="#221d1c",
                   bg="#faf8f5", bg_d="#181514", soft="#f1ece6", soft_d="#231f1d", scene="vines"),
    "mountain": dict(display="Sora", body="Inter", accent="#1d5873", accent_d="#8fd0ef", ink="#1a2026",
                     bg="#f6f8f9", bg_d="#13181b", soft="#e9eef1", soft_d="#1c2328", scene="peaks"),
    "oldtown": dict(display="Fraunces", body="Inter", accent="#8a4b14", accent_d="#f0b672", ink="#231c16",
                    bg="#fbf8f3", bg_d="#191512", soft="#f2ebe1", soft_d="#241e19", scene="arches"),
    "steppe": dict(display="Space Grotesk", body="Inter", accent="#2f6b3a", accent_d="#9ad6a5", ink="#1c211d",
                   bg="#f7f8f4", bg_d="#151814", soft="#ecefe6", soft_d="#1e221d", scene="steppe"),
}

SCENES = {
    "vines": """<path d="M0 230 Q200 170 420 205 T820 190 T1200 200 V400 H0Z" fill="var(--s1)"/>
<path d="M0 290 Q300 240 600 275 T1200 260 V400 H0Z" fill="var(--s2)"/>
<g stroke="var(--s3)" stroke-width="3" opacity=".7">""" + "".join(
        f'<line x1="{x}" y1="{300 + (x % 7)}" x2="{x + 60}" y2="{400}"/>' for x in range(-40, 1240, 46)) + """</g>
<path d="M0 340 Q400 310 800 335 T1200 325 V400 H0Z" fill="var(--s3)"/>""",
    "peaks": """<path d="M0 260 L140 150 L230 210 L380 80 L520 200 L640 120 L780 220 L930 95 L1060 190 L1200 140 V400 H0Z" fill="var(--s1)"/>
<path d="M380 80 L420 110 L345 112Z M930 95 L968 123 L893 124Z M640 120 L668 140 L612 141Z" fill="var(--bg)"/>
<path d="M0 300 Q300 250 600 290 T1200 280 V400 H0Z" fill="var(--s2)"/>
<path d="M0 345 Q400 320 800 342 T1200 335 V400 H0Z" fill="var(--s3)"/>""",
    "arches": """<rect y="200" width="1200" height="200" fill="var(--s1)"/>""" + "".join(
        f'<path d="M{x} 400 V265 a45 45 0 0 1 90 0 V400Z" fill="var(--s2)"/>' for x in range(30, 1200, 140)) + """
<rect y="370" width="1200" height="30" fill="var(--s3)"/>""",
    "steppe": """<path d="M0 250 Q300 225 600 245 T1200 238 V400 H0Z" fill="var(--s1)"/>
<path d="M0 300 Q300 285 600 298 T1200 292 V400 H0Z" fill="var(--s2)"/>
<g fill="var(--bg)" stroke="var(--s3)" stroke-width="3"><path d="M820 300 h90 v-25 l-45 -28 l-45 28Z"/><path d="M940 305 h70 v-20 l-35 -22 l-35 22Z"/></g>
<path d="M0 350 Q400 335 800 348 T1200 342 V400 H0Z" fill="var(--s3)"/>""",
}


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
    wa = digits(d.get("whatsapp"))
    wa_text = t(d.get("whatsapp_greeting"), lang) or u.get("greeting", "Hello! I found {name} online.").format(name=name)
    wa_link = f"https://wa.me/{wa}?text={html.escape(__import__('urllib.parse').parse.quote(wa_text))}" if wa else ""
    wa_tgt = ' target="_blank" rel="noopener"'
    if d.get("sample"): wa_link, wa_tgt = "#contact", ""   # fictional samples: no live WhatsApp link to a number that may belong to someone
    cur = d.get("currency", "")
    desc = t(d.get("intro"), lang)
    hero_img = (d.get("photos") or [{}])[0].get("file") if d.get("photos") else None
    fonts = "family=" + th["display"].replace(" ", "+") + ":wght@400;600&family=" + th["body"].replace(" ", "+") + ":wght@400;500;600" + ("&family=Noto+Sans+Georgian:wght@400;600&family=Noto+Serif+Georgian:wght@400;600" if "ka" in langs else "")

    nav = []
    sec_title = t(d.get("section_title"), lang) or (u["stay"] if d.get("kind") == "lodging" else u["rooms"])
    if d.get("rooms"): nav.append(("stay", sec_title))
    if d.get("experiences"): nav.append(("experiences", u["experiences"]))
    if d.get("photos") and len(d["photos"]) > 1: nav.append(("gallery", u["gallery"]))
    nav.append(("contact", u["contact"]))

    alt_links = "".join(f'<link rel="alternate" hreflang="{l}" href="{page_url(d["slug"], l, langs)}">' for l in langs)
    switch = "" if len(langs) < 2 else '<div class="langs">' + "".join(
        f'<a href="{prefix}{"" if l == langs[0] else l + "/"}" lang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{l.upper()}</a>' for l in langs) + "</div>"

    jsonld = {"@context": "https://schema.org", "@type": d.get("schema_type", "LodgingBusiness"), "name": name,
              "description": desc, "url": page_url(d["slug"], lang, langs),
              "address": {"@type": "PostalAddress", "addressLocality": town, "addressCountry": d.get("country_code", "")}}
    if d.get("whatsapp") and not d.get("sample"): jsonld["telephone"] = d["whatsapp"]
    if d.get("email"): jsonld["email"] = d["email"]
    if d.get("price_range"): jsonld["priceRange"] = d["price_range"]
    if d.get("geo"): jsonld["geo"] = {"@type": "GeoCoordinates", "latitude": d["geo"][0], "longitude": d["geo"][1]}

    s = []
    if d.get("sample"):
        s.append(f'<div class="sample">{e(u["sample"])}</div>')
    s.append(f'<header class="top"><div class="wrap bar"><a class="brand" href="{prefix}{"" if lang == langs[0] else lang + "/"}">{e(name)}</a>'
             f'<nav aria-label="{e(u["menu"])}">' + "".join(f'<a href="#{k}">{e(v)}</a>' for k, v in nav) + f"</nav>{switch}</div></header>")
    hero_art = (f'<img class="hero-img" src="{prefix}{e(hero_img)}" alt="{e(t(d["photos"][0].get("alt"), lang))}" fetchpriority="high">' if hero_img else
                f'<svg class="hero-art" viewBox="0 0 1200 400" preserveAspectRatio="xMidYMax slice" aria-hidden="true">{SCENES[th["scene"]]}</svg>')
    s.append(f'<section class="hero{" has-img" if hero_img else ""}">{hero_art}<div class="wrap hero-text"><p class="eyebrow">{e(t(d.get("location_line"), lang))}</p>'
             f'<h1>{e(t(d.get("headline"), lang))}</h1><p class="lead">{e(desc)}</p><div class="cta">'
             + (f'<a class="btn" href="{wa_link}"{wa_tgt}>{e(u["book"])}</a>' if wa else "")
             + (f'<span class="from">{e(u["from_"])} <b>{e(d["price_from"])} {e(cur)}</b> {e(u["per_night"]) if d.get("kind") == "lodging" else ""}</span>' if d.get("price_from") else "")
             + "</div></div></section>")
    if d.get("facts"):
        s.append('<section class="facts"><div class="wrap grid4">' + "".join(
            f'<div><b>{e(f.get("value"))}</b><span>{e(t(f.get("label"), lang))}</span></div>' for f in d["facts"]) + "</div></section>")
    if d.get("story"):
        s.append(f'<section class="story"><div class="wrap narrow"><p>{e(t(d["story"], lang))}</p></div></section>')
    if d.get("rooms"):
        title = sec_title
        cards = []
        for r in d["rooms"]:
            img = f'<img src="{prefix}{e(r["photo"])}" alt="" loading="lazy">' if r.get("photo") else ""
            meta = []
            if r.get("guests"): meta.append(f'{e(u["up_to"])} {e(r["guests"])} {e(u["guests"])}')
            feats = "".join(f"<li>{e(t(x, lang))}</li>" for x in (r.get("features") or []))
            price = (f'<p class="price"><b>{e(r["price"])} {e(cur)}</b> <span>{e(r.get("unit") and t(r["unit"], lang) or u["per_night"])}</span></p>' if r.get("price") else "")
            cards.append(f'<article class="card">{img}<div class="card-body"><h3>{e(t(r.get("name"), lang))}</h3>'
                         f'<p class="meta">{" · ".join(meta)}</p><p>{e(t(r.get("text"), lang))}</p>'
                         + (f"<ul>{feats}</ul>" if feats else "") + price + "</div></article>")
        s.append(f'<section id="stay"><div class="wrap"><h2>{e(title)}</h2><div class="cards">{"".join(cards)}</div></div></section>')
    if d.get("experiences"):
        items = "".join(f'<article class="exp"><h3>{e(t(x.get("name"), lang))}</h3><p>{e(t(x.get("text"), lang))}</p>'
                        + (f'<p class="price"><b>{e(x["price"])} {e(cur)}</b> <span>{e(t(x.get("unit"), lang))}</span></p>' if x.get("price") else "")
                        + "</article>" for x in d["experiences"])
        sched = d.get("schedule")
        table = ("" if not sched else '<table class="sched">' + "".join(
            f'<tr><th scope="row">{e(row[0])}</th><td>{e(t(row[1], lang))}</td></tr>' for row in sched) + "</table>")
        s.append(f'<section id="experiences" class="alt"><div class="wrap"><h2>{e(u["experiences"])}</h2><div class="split"><div class="exps">{items}</div>{table}</div></div></section>')
    if d.get("photos") and len(d["photos"]) > 1:
        s.append('<section id="gallery"><div class="wrap"><h2>' + e(u["gallery"]) + '</h2><div class="gallery">' + "".join(
            f'<img src="{prefix}{e(p["file"])}" alt="{e(t(p.get("alt"), lang))}" loading="lazy">' for p in d["photos"][1:]) + "</div></div></section>")
    if d.get("reviews"):
        s.append(f'<section class="alt"><div class="wrap"><h2>{e(u["reviews"])}</h2><div class="quotes">' + "".join(
            f'<figure><blockquote>{e(r.get("text"))}</blockquote><figcaption>{e(r.get("author"))}'
            + (f' · {e(r["source"])}' if r.get("source") else "") + "</figcaption></figure>" for r in d["reviews"]) + "</div></div></section>")
    if d.get("faq") or d.get("getting_here"):
        faq = "".join(f'<details><summary>{e(t(q.get("q"), lang))}</summary><p>{e(t(q.get("a"), lang))}</p></details>' for q in (d.get("faq") or []))
        route = f'<div><h3>{e(u["getting_here"])}</h3><p>{e(t(d["getting_here"], lang))}</p></div>' if d.get("getting_here") else ""
        s.append(f'<section><div class="wrap split"><div><h2>{e(u["faq"])}</h2>{faq}</div>{route}</div></section>')
    contact = []
    smp = d.get("sample")  # fictional samples show where the owner's real details will go
    if d.get("whatsapp"): contact.append(f'<p><span class="k">WhatsApp</span> <span class="v{" ph" if smp else ""}">{e(u["your_wa"] if smp else d["whatsapp"])}</span></p>')
    if d.get("email"): contact.append(f'<p><span class="k">{e(u["email"])}</span> <span class="v{" ph" if smp else ""}">{e(u["your_email"] if smp else d["email"])}</span></p>')
    if d.get("address"): contact.append(f'<p><span class="k">⌖</span> <span class="v">{e(t(d["address"], lang))}</span></p>')
    if str(d.get("maps_url", "")).startswith("https://"): contact.append(f'<p><a href="{e(d["maps_url"])}" target="_blank" rel="noopener">{e(u["map"])}</a></p>')
    s.append(f'<section id="contact" class="contact"><div class="wrap split"><div><h2>{e(u["contact"])}</h2>{"".join(contact)}<p class="muted">{e(u["reply"])}</p></div>'
             + (f'<div class="cta-box"><a class="btn big" href="{wa_link}"{wa_tgt}>{e(u["write"])}</a></div>' if wa else "") + "</div></section>")
    creds = [p["credit"] for p in (d.get("photos") or []) if p.get("credit")] + (d.get("extra_credits") or [])
    cred_line = ("" if not creds else f'<p class="credits wrap">{e(u["photos_by"])}: ' + ", ".join(
        f'<a href="{e(c["page"])}" target="_blank" rel="noopener">{e(c["artist"])}</a> ({e(c["license"])})' for c in creds) + "</p>")
    s.append(f'<footer><div class="wrap bar"><span>© {e(name)} · {e(town)}</span><span>{e(d.get("credit", ""))}</span></div>{cred_line}</footer>')
    if wa:
        s.append(f'<a class="fab" href="{wa_link}"{wa_tgt} aria-label="{e(u["write"])}"><svg viewBox="0 0 24 24" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg></a>')

    og_img = f'<meta property="og:image" content="{BASE_URL}/{d["slug"]}/{e(hero_img)}">' if hero_img else ""
    css = f"""
:root{{--bg:{th['bg']};--soft:{th['soft']};--ink:{th['ink']};--muted:color-mix(in srgb,var(--ink) 62%,var(--bg));--line:color-mix(in srgb,var(--ink) 12%,var(--bg));
--accent:{th['accent']};--on:#fff;--card:#fff;--s1:color-mix(in srgb,var(--accent) 18%,var(--soft));--s2:color-mix(in srgb,var(--accent) 34%,var(--soft));--s3:color-mix(in srgb,var(--accent) 55%,var(--ink));
--display:"{th['display']}","Noto Serif Georgian",Georgia,serif;--body:"{th['body']}","Noto Sans Georgian",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
@media (prefers-color-scheme:dark){{:root{{--bg:{th['bg_d']};--soft:{th['soft_d']};--ink:#ece8e3;--accent:{th['accent_d']};--on:#141210;--card:color-mix(in srgb,var(--soft) 70%,#000);color-scheme:dark}}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:72px}}@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.65 var(--body);-webkit-font-smoothing:antialiased}}
img{{max-width:100%;display:block}}a{{color:var(--accent)}}a:focus-visible,summary:focus-visible{{outline:3px solid var(--accent);outline-offset:3px;border-radius:4px}}
.wrap{{max-width:1120px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left));padding-right:max(20px,env(safe-area-inset-right))}}
.narrow{{max-width:760px}}
h1,h2,h3{{font-family:var(--display);font-weight:600;line-height:1.12;letter-spacing:-.01em;text-wrap:balance;margin:0 0 .7rem}}
h1{{font-size:clamp(2.2rem,6.2vw,4rem);max-width:17ch}}h2{{font-size:clamp(1.6rem,3.6vw,2.4rem)}}h3{{font-size:1.2rem}}
p{{margin:0 0 .8rem}}.muted{{color:var(--muted);font-size:.95rem}}
.sample{{background:var(--ink);color:var(--bg);text-align:center;font-size:.85rem;padding:.4rem 1rem}}
.top{{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}}
.bar{{display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;padding-block:.8rem}}
.brand{{font-family:var(--display);font-weight:600;font-size:1.15rem;color:var(--ink);text-decoration:none}}
nav{{display:flex;gap:1.2rem;flex-wrap:wrap;font-size:.95rem}}nav a{{color:var(--ink);text-decoration:none;opacity:.85}}nav a:hover{{opacity:1;text-decoration:underline}}
.langs{{display:flex;gap:.25rem}}.langs a{{font-size:.78rem;font-weight:600;text-decoration:none;color:var(--ink);border:1px solid var(--line);border-radius:999px;padding:.2rem .6rem}}
.langs a[aria-current]{{background:var(--ink);color:var(--bg);border-color:var(--ink)}}
.hero{{position:relative;background:var(--soft);overflow:hidden}}
.hero-art{{display:block;width:100%;height:clamp(150px,26vw,300px)}}
.hero-img{{width:100%;height:clamp(240px,48vw,520px);object-fit:cover}}
.has-img{{padding:0;color:#fff;background:#111}}.has-img .hero-img{{height:min(88svh,760px);min-height:520px;filter:saturate(1.05)}}
.has-img::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 35%,rgba(0,0,0,.7) 100%),linear-gradient(90deg,rgba(0,0,0,.5) 0%,rgba(0,0,0,.15) 55%,rgba(0,0,0,0) 80%);pointer-events:none}}
@media (max-width:640px){{.has-img .hero-img{{height:76svh;min-height:480px}}.has-img::after{{background:linear-gradient(180deg,rgba(0,0,0,0) 25%,rgba(0,0,0,.78) 100%)}}
.bar{{row-gap:.4rem}}.top nav{{order:3;width:100%;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;gap:1rem;font-size:.9rem}}.langs{{margin-left:auto}}}}
.has-img .hero-text{{position:absolute;left:0;right:0;bottom:0;z-index:1;padding-block:0 clamp(2rem,6vw,4rem)}}
.has-img h1{{color:#fff;text-shadow:0 2px 24px rgba(0,0,0,.35)}}.has-img .lead,.has-img .from{{color:rgba(255,255,255,.88)}}.has-img .from b{{color:#fff}}
.has-img .eyebrow{{color:#fff;opacity:.9}}:lang(ka) .eyebrow{{text-transform:none;letter-spacing:.03em}}html[lang=ka] h1{{font-size:clamp(2rem,5.4vw,3.4rem)}}.has-img .btn{{background:#fff;color:#141210}}
.hero-text{{padding-block:2.2rem 3rem}}.eyebrow{{text-transform:uppercase;letter-spacing:.14em;font-size:.78rem;font-weight:600;color:var(--accent)}}
.lead{{font-size:clamp(1.05rem,2vw,1.2rem);color:var(--muted);max-width:58ch}}
.cta{{display:flex;align-items:center;gap:1.2rem;flex-wrap:wrap;margin-top:1.2rem}}.from{{color:var(--muted)}}.from b{{color:var(--ink);font-size:1.15rem}}
.btn{{display:inline-flex;align-items:center;gap:.5rem;background:var(--accent);color:var(--on);text-decoration:none;font-weight:600;padding:.85rem 1.4rem;border-radius:999px;transition:transform .15s}}
.btn:hover{{transform:translateY(-1px)}}.btn.big{{font-size:1.1rem;padding:1rem 1.8rem}}
section{{padding-block:clamp(2.5rem,6vw,4.5rem)}}.alt{{background:var(--soft)}}
.facts{{padding-block:1.6rem;border-bottom:1px solid var(--line)}}.grid4{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1.2rem}}
.grid4 b{{display:block;font-family:var(--display);font-size:1.6rem;font-weight:600}}.grid4 span{{color:var(--muted);font-size:.9rem}}
.story p{{font-family:var(--display);font-size:clamp(1.2rem,2.6vw,1.6rem);line-height:1.45}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:1.2rem}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}}
.card img{{aspect-ratio:4/3;object-fit:cover}}.card-body{{padding:1.2rem 1.3rem 1.4rem;display:flex;flex-direction:column;flex:1}}
.card ul{{margin:0 0 1rem;padding-left:1.1rem;color:var(--muted);font-size:.95rem}}.meta{{color:var(--muted);font-size:.88rem;margin-bottom:.4rem}}
.price{{margin-top:auto}}.price b{{font-size:1.2rem}}.price span{{color:var(--muted);font-size:.9rem}}
.split{{display:grid;grid-template-columns:1.2fr 1fr;gap:clamp(1.5rem,4vw,3.5rem);align-items:start}}.split>*{{min-width:0}}
@media (max-width:760px){{.split{{grid-template-columns:1fr}}}}
.exps{{display:grid;gap:1.4rem}}.exp{{border-left:3px solid var(--accent);padding-left:1rem}}
.sched{{width:100%;border-collapse:collapse;font-size:.95rem;background:var(--card);border-radius:12px;overflow:hidden}}
.sched th,.sched td{{padding:.7rem .9rem;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}.sched th{{color:var(--accent);white-space:nowrap;font-variant-numeric:tabular-nums}}
.gallery{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:.6rem}}.gallery img{{aspect-ratio:4/3;object-fit:cover;border-radius:10px}}
.quotes{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:1.2rem}}
figure{{margin:0;background:var(--card);border-radius:14px;padding:1.3rem;border:1px solid var(--line)}}blockquote{{margin:0 0 .8rem;font-size:1.02rem}}figcaption{{color:var(--muted);font-size:.88rem}}
details{{border-bottom:1px solid var(--line);padding:.85rem 0}}summary{{cursor:pointer;font-weight:600}}details p{{margin:.6rem 0 0;color:var(--muted)}}
.contact .k{{display:inline-block;min-width:6rem;color:var(--muted);font-size:.9rem}}.contact .v{{font-weight:600;user-select:all}}
.cta-box{{display:flex;align-items:center;justify-content:flex-start;min-height:100%}}
footer{{border-top:1px solid var(--line);color:var(--muted);font-size:.85rem}}.credits{{font-size:.72rem;padding-bottom:1rem;opacity:.8}}.credits a{{color:inherit}}
.v.ph{{font-weight:500;font-style:italic;color:var(--muted);border:1px dashed var(--line);border-radius:6px;padding:.1rem .5rem;user-select:none}}
.fab{{position:fixed;right:max(18px,env(safe-area-inset-right));bottom:max(18px,env(safe-area-inset-bottom));width:58px;height:58px;border-radius:50%;
background:#25d366;color:#fff;display:grid;place-items:center;box-shadow:0 6px 20px rgba(0,0,0,.25);z-index:30}}
"""
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(name)} · {e(town)}</title><meta name="description" content="{e(desc[:160])}">
<link rel="canonical" href="{page_url(d['slug'], lang, langs)}">{alt_links}
<meta property="og:type" content="website"><meta property="og:title" content="{e(name)}"><meta property="og:description" content="{e(desc[:200])}">{og_img}
{'<meta name="robots" content="noindex">' if d.get("sample") else ''}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False).replace("<", "\\u003c")}</script>
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
