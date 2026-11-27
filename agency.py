"""Serai Studio's own website: site/index.html (English), site/ru/ and site/ka/ (Georgian)."""
import html
import json
import os
import urllib.parse
from pathlib import Path

HERE = Path(__file__).parent
EMAIL = "seraistudio.web@gmail.com"
# Public address of the site. Set SITE_BASE to override (no trailing slash).
BASE = os.environ.get("SITE_BASE", "https://serai-studio.pages.dev").rstrip("/")

T = {
 "en": dict(
  title="Serai Studio · Websites for guesthouses, wineries and tours",
  desc="Serai Studio builds fast, multilingual websites for small hospitality businesses in Georgia, Armenia and Central Asia. Fixed prices, a free private preview, and you only pay if you like it.",
  nav=["Work", "Prices", "How it works", "Questions", "Contact"],
  eyebrow="Georgia · Armenia · Central Asia",
  h1="Websites for the places travellers remember",
  lead="We build websites for family guesthouses, wineries, tour guides and small restaurants. Your rooms, prices and story in English and Russian, with one button that brings guests straight to your WhatsApp.",
  cta="Ask for a free preview", cta2="See our work",
  proof=[("Free", "preview before you pay"), ("3 days", "to a private preview"), ("2+", "languages on every site"), ("0", "booking commission")],
  work_h="Recent work", work_note="These are sample sites for fictional businesses, made to show what we build.",
  prices_h="Two simple prices", prices_note="Prices are one time. We set up free hosting on a Cloudflare account in your name, and we look after it for the first year. The domain name (about $10 to $15 a year) is registered in your name, so the site always belongs to you.",
  plans=[
   ("Starter", "$150", "or 400 GEL, one time", ["One-page website", "English + Russian. Georgian too, after you check the Georgian text", "Rooms, prices and photos", "WhatsApp button and Google Maps link", "Works on every phone", "Free hosting set up on a Cloudflare account in your name, looked after by us for the first year, and domain setup", "Private preview within 3 working days after we get your info and photos"]),
   ("Care", "$150", "per year, from the second year", ["Keeping the site running and updated", "Price, photo and text updates (up to 30 minutes a month)", "Domain renewal reminders", "We check every month that the site works", "Answer within one working day"]),
  ],
  steps_h="How it works",
  steps=[("Write to us", "Send your business name and a link to your Google Maps, Instagram or Booking.com page."),
         ("Free preview", "Within 3 working days after we get your info and photos, we send a private preview that search engines do not show."),
         ("Your changes", "Tell us what to change in a message. One round of changes is included before launch."),
         ("Go live", "You pay only when you are happy. We connect your domain and the site goes live.")],
  faq_h="Questions",
  faq=[("Why do I need a website if I am on Booking.com?", "Booking.com takes a commission on every booking and shows guests your competitors next to you. Your own site lets guests contact you directly and see everything you offer."),
       ("How do we talk?", "We work in writing, by email. Every price and change is written down, nothing gets lost in translation, and you can answer when it suits you. We work remotely from Seoul. You may also write to us in Georgian."),
       ("How do I pay?", "By PayPal payment link, after you approve the preview."),
       ("What happens after the first year?", "You choose: the Care plan at $150 a year, or we hand over all site files for free."),
       ("Can you use photos from my Booking.com or Google page?", "Only photos you own or have permission to use. Please send the original files and tell us who took them."),
       ("Who owns the website?", "You do. The domain and the hosting account are registered in your name."),
       ("Can you add Georgian, Armenian or another language?", "Every site is in English and Russian. Georgian is added at no cost, after you check the Georgian text.")],
  contact_h="Let's make your preview", contact_p="Send us your business name and one link where guests can find you today. We answer within one working day.",
  email_l="Email", sample_l="Open sample", mail_subject="Website preview", privacy="We use what you send us only to answer you and build your site.", langs="Language", hero_tag="Serai Studio"),
 "ru": dict(
  title="Serai Studio · Сайты для гостевых домов, виноделен и туров",
  desc="Serai Studio делает быстрые многоязычные сайты для небольшого гостеприимного бизнеса в Грузии, Армении и Центральной Азии. Фиксированные цены, бесплатный закрытый пример, оплата только если понравится.",
  nav=["Работы", "Цены", "Как это работает", "Вопросы", "Контакты"],
  eyebrow="Грузия · Армения · Центральная Азия",
  h1="Сайты для мест, которые путешественники запоминают",
  lead="Мы делаем сайты для семейных гостевых домов, виноделен, гидов и небольших ресторанов. Ваши номера, цены и история на английском и русском, и одна кнопка, которая ведёт гостей прямо в ваш WhatsApp.",
  cta="Получить бесплатный пример", cta2="Посмотреть работы",
  proof=[("Бесплатно", "пример до оплаты"), ("3 дня", "до закрытого примера"), ("2+", "языка на каждом сайте"), ("0", "комиссии с бронирований")],
  work_h="Наши работы", work_note="Это примеры сайтов для вымышленных заведений, чтобы показать, что мы делаем.",
  prices_h="Две простые цены", prices_note="Цены разовые. Мы бесплатно настраиваем хостинг (Cloudflare) на аккаунте на ваше имя и первый год следим за ним. Домен (примерно $10–15 в год) регистрируется на ваше имя, поэтому сайт всегда принадлежит вам.",
  plans=[
   ("Старт", "$150", "или 400 лари, один раз", ["Одностраничный сайт", "Английский и русский. Грузинский тоже, после того как вы проверите текст", "Номера, цены и фото", "Кнопка WhatsApp и ссылка на Google Maps", "Удобно на любом телефоне", "Бесплатный хостинг на аккаунте Cloudflare на ваше имя, первый год под нашим присмотром, и подключение домена", "Закрытый пример через 3 рабочих дня после получения данных и фото"]),
   ("Поддержка", "$150", "в год, со второго года", ["Работа сайта и его обновление", "Обновление цен, фото и текстов (до 30 минут в месяц)", "Напоминания о продлении домена", "Ежемесячная проверка работы сайта", "Ответ в течение рабочего дня"]),
  ],
  steps_h="Как это работает",
  steps=[("Напишите нам", "Пришлите название и ссылку на вашу страницу в Google Maps, Instagram или Booking.com."),
         ("Бесплатный пример", "Через 3 рабочих дня после получения данных и фото мы пришлём закрытый пример, который не видят поисковики."),
         ("Ваши правки", "Напишите, что изменить. До запуска включён один круг правок."),
         ("Запуск", "Оплата только когда вам всё нравится. Подключаем домен, и сайт работает.")],
  faq_h="Вопросы",
  faq=[("Зачем сайт, если я есть на Booking.com?", "Booking.com берёт комиссию с каждой брони и показывает гостям конкурентов рядом с вами. Свой сайт позволяет гостям писать вам напрямую и видеть всё, что вы предлагаете."),
       ("Как мы общаемся?", "Мы работаем письменно, по электронной почте. Все цены и правки записаны, ничего не теряется при переводе, и вы отвечаете, когда удобно. Мы работаем удалённо из Сеула. Можно писать и по-грузински."),
       ("Как оплатить?", "Через ссылку на оплату PayPal, после того как вы одобрите пример."),
       ("Что после первого года?", "Выбираете вы: «Поддержка» за $150 в год или бесплатная передача всех файлов сайта."),
       ("Можно взять фото с моей страницы Booking.com или Google?", "Только фото, которые принадлежат вам или на которые у вас есть разрешение. Пришлите оригиналы и напишите, кто снимал."),
       ("Кому принадлежит сайт?", "Вам. Домен и аккаунт хостинга регистрируются на ваше имя."),
       ("Можно добавить грузинский, армянский или другой язык?", "Каждый сайт на английском и русском. Грузинский добавляем бесплатно, после того как вы проверите текст.")],
  contact_h="Сделаем ваш пример", contact_p="Пришлите название и одну ссылку, где гости находят вас сейчас. Отвечаем в течение рабочего дня.",
  email_l="Почта", sample_l="Открыть пример", mail_subject="Пример сайта", privacy="Всё, что вы нам присылаете, мы используем только чтобы ответить вам и сделать ваш сайт.", langs="Язык", hero_tag="Serai Studio"),
}
T["ka"] = json.loads((HERE / "i18n" / "agency_ka.json").read_text(encoding="utf-8"))
LANGS = ["en", "ru", "ka"]
# Korean page: a separate offer for shops in Korea (KRW price), so it is not in the language switcher or hreflang set.
T["ko"] = json.loads((HERE / "i18n" / "agency_ko.json").read_text(encoding="utf-8"))

WORK = [("babua-marani", "Babua's Marani", {"en": "Family winery · Kakheti, Georgia", "ru": "Семейная винодельня · Кахетия, Грузия"}),
        ("cloudline-kazbegi", "Cloudline Guesthouse", {"en": "Guesthouse · Kazbegi, Georgia", "ru": "Гостевой дом · Казбеги, Грузия"}),
        ("steppe-roads", "Steppe Roads", {"en": "Trekking tours · Karakol, Kyrgyzstan", "ru": "Треккинг-туры · Каракол, Кыргызстан"}),
        ("dukani-nine", "Dukani Nine", {"en": "Restaurant · Old Tbilisi, Georgia", "ru": "Ресторан · Старый Тбилиси, Грузия"})]

ARROW = '<span class="ic" aria-hidden="true"><svg viewBox="0 0 16 16" width="14" height="14"><path d="M4 12 12 4M6 4h6v6" fill="none" stroke="currentColor" stroke-width="1.3"/></svg></span>'
PLUS = '<svg class="pl" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M8 2v12M2 8h12" stroke="currentColor" stroke-width="1.2"/></svg>'
LOGO = '<svg width="22" height="22" viewBox="0 0 26 26" aria-hidden="true"><path d="M3 24V12a10 10 0 0 1 20 0v12" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 24v-9a5 5 0 0 1 10 0v9" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'


def e(s):
    return html.escape(str(s), quote=True)


def sub_dir(l):
    return "" if l == "en" else l + "/"


def render(lang):
    c = T[lang]
    pre = "./" if lang == "en" else "../"
    ids = ["work", "prices", "how", "faq", "contact"]
    switch = "" if lang == "ko" else '<div class="langs">' + "".join(f'<a href="{pre}{sub_dir(l)}" hreflang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{l.upper()}</a>' for l in LANGS) + "</div>"
    mail = f"mailto:{EMAIL}?subject=" + urllib.parse.quote(c["mail_subject"])

    from build import UI as SUI, lic_url
    cards, heroes, creds, labels = [], [], [], []
    for slug, name, sub in WORK:
        cl = json.loads((HERE / "clients" / f"{slug}.json").read_text(encoding="utf-8"))
        langs = cl.get("languages") or ["en"]
        href = f"{pre}{slug}/" + ("" if lang == langs[0] or lang not in langs else lang + "/")
        photo = (cl.get("photos") or [{}])[0].get("file")
        cr = (cl.get("photos") or [{}])[0].get("credit")
        if cr and cr not in creds: creds.append(cr)
        src = f"{pre}{slug}/{photo}" if photo else ""
        heroes.append(src)
        label = c.get("work_sub", {}).get(slug) or sub.get(lang) or sub["en"]
        cards.append(f'<a class="slide" href="{href}" aria-label="{e(name)}, {e(c["sample_l"])}"><img src="{src}" alt="" loading="lazy" decoding="async">'
                     f'<div class="cap"><div><p class="w-sub">{e(label)}</p><h3>{e(name)}</h3></div><span class="go">{e(c["sample_l"])} {ARROW}</span></div></a>')
        labels.append(label)

    plans = "".join(f'''<article class="plan{" dark" if i == 0 else ""} rv"><div class="p-in"><p class="p-name">{e(n)}</p><p class="amt"><b>{e(p)}</b><span>{e(unit)}</span></p>
<ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul>{f'<a class="btn" href="{mail}"><span>{e(c["cta"])}</span>{ARROW}</a>' if i == 0 else ""}</div></article>''' for i, (n, p, unit, items) in enumerate(c["plans"]))
    su = SUI.get(lang, SUI["en"])
    link = lambda c: f'<a href="{e(c["page"])}" target="_blank" rel="noopener">{e(c["artist"])}</a> (' + (
        f'<a href="{e(lic_url(c["license"]))}" target="_blank" rel="noopener license">{e(c["license"])}</a>' if lic_url(c["license"]) else e(c["license"])) + ")"
    credits = "" if not creds else f'<p class="credits">{e(su["photos_by"])}: ' + ", ".join(link(c) for c in creds) + f'. {e(su["modified"])}</p>'
    steps = "".join(f'<li class="rv"><span class="n">0{i}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(c["steps"], 1))
    faq = "".join(f'<details class="rv"><summary>{e(q)}{PLUS}</summary><p>{e(a)}</p></details>' for q, a in c["faq"])
    proof = "".join(f'<div class="rv"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in c["proof"])
    kinds = [l.split(" · ")[0] for l in labels]
    band = "".join(f"<span>{e(k)}</span>" for k in kinds * 2)
    js = """document.documentElement.classList.add('js');addEventListener('DOMContentLoaded',()=>{
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}}),{rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.rv').forEach((el,i)=>{el.style.transitionDelay=(el.closest('.hero')?i*110:((i%4)*80))+'ms';io.observe(el)});
const pl=document.querySelector('.pill'),mb=document.querySelector('.menu-btn');if(pl&&mb){const set=o=>{pl.classList.toggle('open',o);mb.setAttribute('aria-expanded',o)};mb.addEventListener('click',()=>set(!pl.classList.contains('open')));pl.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>set(false)));addEventListener('keydown',ev=>{if(ev.key==='Escape')set(false)});document.addEventListener('click',ev=>{if(!pl.contains(ev.target))set(false)})}
const nav=document.querySelector('.nav'),hero=document.querySelector('.hero');
new IntersectionObserver(([x])=>nav.dataset.solid=x.isIntersecting?'0':'1',{rootMargin:'-120px 0px 0px 0px'}).observe(hero)});"""
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(c["title"])}</title><meta name="description" content="{e(c["desc"])}"><meta name="theme-color" content="#14201d">
<link rel="canonical" href="{BASE}/{sub_dir(lang)}">{"" if lang == "ko" else "".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}/{sub_dir(l)}">' for l in LANGS)}
<meta property="og:title" content="Serai Studio"><meta property="og:description" content="{e(c["desc"])}"><meta property="og:image" content="{BASE}/babua-marani/hero.jpg">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 26 26'%3E%3Cpath d='M3 24V12a10 10 0 0 1 20 0v12M8 24v-9a5 5 0 0 1 10 0v9' fill='none' stroke='%23b5873a' stroke-width='2.4'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Hanken+Grotesk:wght@400;500;600&family=Noto+Sans+Georgian:wght@400;500;600&family=Noto+Serif+Georgian:wght@300;400{'&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@400;500' if lang == 'ko' else ''}&display=swap">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ProfessionalService","name":"Serai Studio","email":"{EMAIL}","areaServed":{'["South Korea"]' if lang == "ko" else '["Georgia","Armenia","Kyrgyzstan","Uzbekistan","Kazakhstan"]'},"url":"{BASE}/"}}</script>
<script>if(!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('fx')</script>
<link rel="stylesheet" href="{pre}motion.css">
<script>if(document.documentElement.classList.contains('fx'))['gsap.min.js','ScrollTrigger.min.js','SplitText.min.js','lenis.min.js','motion.js'].forEach(f=>{{const s=document.createElement('script');s.src='{pre}'+f;s.async=false;document.head.appendChild(s)}})</script>
<script>{js}</script>
<style>
:root{{--gold-t:#86601f;--paper:#f6f3ed;--ink:#191714;--muted:#6b665d;--hair:rgba(25,23,20,.12);--accent:#14524b;--gold:#b5873a;--deep:#14201d;
--serif:"Instrument Serif","Noto Serif Georgian",Georgia,serif;--sans:"Hanken Grotesk","Noto Sans Georgian",system-ui,-apple-system,"Segoe UI",sans-serif;--ease:cubic-bezier(.32,.72,0,1)}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:90px}}
body{{margin:0;background:var(--paper);color:var(--ink);font:400 16.5px/1.7 var(--sans);-webkit-font-smoothing:antialiased}}
img{{display:block;max-width:100%}}a{{color:inherit}}:focus-visible{{outline:2px solid var(--accent);outline-offset:4px;border-radius:6px}}p{{margin:0}}
.wrap{{width:min(1240px,100% - 2*clamp(20px,5vw,64px));margin-inline:auto}}
h1,h2,h3{{font-family:var(--serif);font-weight:400;letter-spacing:-.015em;margin:0;text-wrap:balance}}
h2{{font-size:clamp(2.6rem,6vw,5.2rem);line-height:.98}}h3{{font-size:1.6rem;line-height:1.1}}
html[lang=ko]{{--serif:"Noto Serif KR","Instrument Serif",serif;--sans:"Noto Sans KR","Hanken Grotesk",system-ui,sans-serif}}html[lang=ko] body{{word-break:keep-all}}html[lang=ko] h1,html[lang=ko] h2,html[lang=ko] h3{{font-weight:500;letter-spacing:-.02em}}html[lang=ko] h2{{font-size:clamp(2rem,4.4vw,3.6rem);line-height:1.18}}html[lang=ko] .hero h1{{font-size:clamp(2.2rem,4.8vw,4.4rem);line-height:1.18}}html[lang=ko] .contact h2{{font-size:clamp(2.2rem,5vw,4.4rem);line-height:1.18}}html[lang=ko] summary{{font-size:clamp(1.1rem,1.6vw,1.35rem)}}html[lang=ko] .mail{{font-size:clamp(1.15rem,1.9vw,1.6rem)}}html[lang=ko] .amt b{{font-size:clamp(2.8rem,5vw,4.2rem)}}:lang(ko) .tag,:lang(ko) .p-name,:lang(ko) .w-sub{{text-transform:none;letter-spacing:.04em}}
html[lang=ka] h1,html[lang=ka] h2,html[lang=ka] h3{{font-weight:300;letter-spacing:0}}html[lang=ka] h2{{font-size:clamp(2rem,4.4vw,3.6rem);line-height:1.15}}
.tag{{display:inline-flex;font:500 .7rem/1 var(--sans);letter-spacing:.22em;text-transform:uppercase;padding:.55rem .9rem;border-radius:99px;color:var(--gold-t);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--gold) 40%,transparent)}}.how .tag{{color:var(--gold)}}
:lang(ka) .tag{{text-transform:none;letter-spacing:.04em}}
.nav{{position:fixed;top:18px;left:0;right:0;z-index:50;display:flex;justify-content:center;pointer-events:none}}
.pill{{pointer-events:auto;display:flex;align-items:center;gap:clamp(.8rem,2vw,1.8rem);padding:.45rem .45rem .45rem 1.3rem;border-radius:99px;background:rgba(246,243,237,.94);
box-shadow:inset 0 0 0 1px var(--hair);backdrop-filter:blur(18px) saturate(1.4);transition:box-shadow .6s var(--ease),background .6s var(--ease)}}
.nav[data-solid="1"] .pill{{background:rgba(246,243,237,.9);box-shadow:inset 0 0 0 1px var(--hair),0 24px 48px -28px rgba(40,30,20,.35)}}
.logo{{display:flex;align-items:center;gap:.5rem;font-family:var(--serif);font-size:1.35rem;text-decoration:none;white-space:nowrap}}.logo svg{{color:var(--gold)}}
.pill nav{{display:flex;gap:1.3rem;font-size:.88rem}}.pill nav a{{text-decoration:none;color:var(--ink);transition:color .3s}}.pill nav a:hover{{color:var(--accent)}}
.langs{{display:flex;gap:.1rem}}.langs a{{font-size:.7rem;font-weight:600;letter-spacing:.08em;text-decoration:none;padding:.35rem .5rem;border-radius:99px;color:#5c574f}}.langs a[aria-current]{{color:var(--ink);box-shadow:inset 0 0 0 1px currentColor}}
.mini{{font-size:.82rem;font-weight:600;text-decoration:none;padding:.65rem 1.1rem;border-radius:99px;background:var(--ink);color:#fff;white-space:nowrap}}
.btn{{display:inline-flex;align-items:center;gap:.9rem;padding:.45rem .45rem .45rem 1.5rem;border-radius:99px;background:var(--ink);color:#fff;text-decoration:none;font-weight:600;font-size:.95rem;transition:transform .5s var(--ease)}}
.btn:active{{transform:scale(.98)}}.ic{{display:grid;place-items:center;flex:none;width:2.4rem;height:2.4rem;border-radius:50%;background:rgba(255,255,255,.14);transition:transform .5s var(--ease)}}
.btn:hover .ic,.w:hover .ic{{transform:translate(2px,-2px) scale(1.06)}}
.ghost{{display:inline-flex;align-items:center;padding:.95rem 1.4rem;border-radius:99px;text-decoration:none;font-weight:600;font-size:.95rem;box-shadow:inset 0 0 0 1px var(--hair)}}
.bezel{{padding:.45rem;border-radius:1.7rem;background:rgba(25,23,20,.04);box-shadow:inset 0 0 0 1px rgba(25,23,20,.06)}}
.core{{position:relative;border-radius:calc(1.7rem - .45rem);overflow:hidden;height:100%}}.core img{{width:100%;height:100%;object-fit:cover;transition:transform 1.4s var(--ease)}}
section{{padding-block:clamp(5rem,10vw,9rem)}}.head{{display:flex;flex-direction:column;align-items:flex-start;gap:1.3rem;margin-bottom:clamp(2.5rem,5vw,4rem)}}.note{{color:var(--muted);max-width:60ch}}
.plans{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(1rem,2vw,1.6rem);align-items:stretch}}
.plan{{padding:.45rem;border-radius:1.9rem;background:rgba(25,23,20,.04);box-shadow:inset 0 0 0 1px rgba(25,23,20,.06)}}
.p-in{{height:100%;border-radius:calc(1.9rem - .45rem);background:#fffdf9;padding:clamp(1.8rem,3.4vw,3rem);display:flex;flex-direction:column;box-shadow:inset 0 1px 1px rgba(255,255,255,.6)}}
.plan.dark .p-in{{background:var(--deep);color:#efe9e0}}.dark .p-name{{color:var(--gold)}}.plan.dark .amt span,.plan.dark li{{color:rgba(239,233,224,.72)}}.plan.dark .btn{{background:#efe9e0;color:var(--ink);margin-top:2rem;align-self:flex-start}}.plan.dark .ic{{background:var(--ink);color:#fff}}
.p-name{{font:500 .72rem/1 var(--sans);letter-spacing:.22em;text-transform:uppercase;color:var(--gold-t)}}:lang(ka) .p-name{{text-transform:none;letter-spacing:.04em}}
.amt{{display:flex;align-items:baseline;gap:.8rem;flex-wrap:wrap;margin:1.2rem 0 1.6rem}}.amt b{{font-family:var(--serif);font-weight:400;font-size:clamp(3.6rem,6vw,5.2rem);line-height:.9}}.amt span{{color:var(--muted);font-size:.92rem}}
.plan ul{{list-style:none;padding:0;margin:0;display:grid;gap:.7rem}}.plan li{{padding-left:1.6rem;position:relative;color:var(--muted)}}
.plan li::before{{content:"";position:absolute;left:0;top:.8em;width:.8rem;height:1px;background:var(--gold)}}
.prices .note{{margin-top:1.6rem;font-size:.92rem}}
.how{{background:var(--deep);color:#efe9e0}}.how .tag{{color:#d7b57a}}
.steps{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(1.5rem,3vw,2.5rem)}}
.steps li{{border-top:1px solid rgba(239,233,224,.18);padding-top:1.6rem}}.n{{display:block;font-family:var(--serif);font-size:3.4rem;line-height:1;color:var(--gold);margin-bottom:1.6rem}}
.steps h3{{margin-bottom:.7rem}}.steps p{{color:rgba(239,233,224,.68)}}
.faq-grid{{display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(2rem,6vw,6rem);align-items:start}}.faq-grid .head{{position:sticky;top:120px}}
details{{border-bottom:1px solid var(--hair)}}details:first-of-type{{border-top:1px solid var(--hair)}}
summary{{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:1rem;align-items:center;padding:1.5rem 0;font-family:var(--serif);font-size:clamp(1.25rem,1.9vw,1.6rem)}}
summary::-webkit-details-marker{{display:none}}.pl{{flex:none;color:var(--gold);transition:transform .5s var(--ease)}}details[open] .pl{{transform:rotate(45deg)}}details p{{padding:0 0 1.6rem;color:var(--muted);max-width:62ch}}
.contact{{background:var(--deep);color:#efe9e0;padding-bottom:0}}.contact h2{{font-size:clamp(3rem,8vw,7.6rem);line-height:.92;max-width:12ch}}html[lang=ka] .contact h2{{font-size:clamp(2.2rem,5vw,4.4rem);line-height:1.15}}
.c-grid{{display:grid;grid-template-columns:1.2fr .8fr;gap:3rem;align-items:end;padding-bottom:clamp(5rem,9vw,8rem)}}
.c-grid p{{color:rgba(239,233,224,.7);max-width:44ch}}.mail{{display:block;font-family:var(--serif);font-size:clamp(1.5rem,2.6vw,2.2rem);color:#efe9e0;margin:1.6rem 0 2rem;user-select:all;overflow-wrap:anywhere}}
.contact .btn{{background:#efe9e0;color:var(--ink)}}.contact .ic{{background:var(--accent);color:#fff}}
footer{{border-top:1px solid rgba(239,233,224,.14);padding-block:2rem;color:rgba(239,233,224,.66);font-size:.82rem}}.credits{{margin-top:1rem;font-size:.72rem;color:rgba(239,233,224,.72)}}
.js .rv{{opacity:0;transform:translateY(40px);filter:blur(6px);transition:opacity 1.1s var(--ease),transform 1.1s var(--ease),filter 1.1s var(--ease)}}.js .rv.in{{opacity:1;transform:none;filter:none}}
@media (prefers-reduced-motion:reduce){{.js .rv{{opacity:1;transform:none;filter:none;transition:none}}html{{scroll-behavior:auto}}}}
/* ---------- v2 homepage ---------- */
.hero{{position:relative;min-height:100svh;display:flex;align-items:flex-end;background:var(--deep);color:#efe9e0;padding:9rem 0 clamp(3rem,6vw,5rem);overflow:hidden}}
.hero::before{{content:"";position:absolute;inset:-20% -10% auto auto;width:70vw;aspect-ratio:1;border-radius:50%;background:radial-gradient(closest-side,rgba(181,135,58,.22),transparent);pointer-events:none}}
.hero .tag{{color:#d7b57a;box-shadow:inset 0 0 0 1px rgba(215,181,122,.35)}}
.hero h1{{font-size:clamp(3.4rem,9.4vw,10.5rem);line-height:.9;letter-spacing:-.03em;margin:1.6rem 0 clamp(2rem,4vw,3.4rem);max-width:12ch}}
html[lang=ru] .hero h1{{font-size:clamp(2.2rem,7vw,7.6rem);max-width:14ch;hyphens:auto}}html[lang=ko] .hero h1{{font-size:clamp(2.4rem,6.2vw,6.8rem);line-height:1.12;max-width:16ch;letter-spacing:-.01em;word-break:keep-all}}html[lang=ka] .hero h1{{font-size:clamp(1.85rem,5.6vw,5.6rem);line-height:1.1;max-width:20ch;letter-spacing:0;overflow-wrap:break-word}}
.hero-row{{display:flex;justify-content:space-between;align-items:flex-end;gap:2rem 4rem;flex-wrap:wrap;padding-top:2rem;border-top:1px solid rgba(239,233,224,.16)}}
.hero .lead{{max-width:46ch;color:rgba(239,233,224,.74)}}.ctas{{display:flex;gap:.8rem;flex-wrap:wrap}}
.hero .btn{{background:#efe9e0;color:var(--ink)}}.hero .btn .ic{{background:var(--gold);color:#fff}}.hero .ghost{{color:#efe9e0;box-shadow:inset 0 0 0 1px rgba(239,233,224,.3)}}
.lead{{font-size:clamp(1.02rem,1.4vw,1.15rem)}}
/* showreel of the samples */
.reel{{padding-block:clamp(5rem,9vw,8rem) 0}}
.reel-head{{margin-bottom:clamp(2rem,4vw,3rem)}}
.reel-stage{{display:grid;gap:clamp(1rem,2vw,1.6rem);width:min(1240px,100% - 2*clamp(20px,5vw,64px));margin-inline:auto}}
.slide{{position:relative;display:block;height:clamp(380px,62vw,720px);border-radius:1.6rem;overflow:hidden;color:#fff;text-decoration:none;background:var(--deep)}}
.slide img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.slide::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,8,.1) 40%,rgba(10,10,8,.72))}}
.cap{{position:absolute;left:0;right:0;bottom:0;z-index:2;display:flex;justify-content:space-between;align-items:flex-end;gap:1rem 2rem;flex-wrap:wrap;padding:clamp(1.4rem,3.4vw,3rem)}}
.cap h3{{font-size:clamp(2.4rem,6vw,5.6rem);line-height:.95;letter-spacing:-.02em}}.w-sub{{font-size:.75rem;letter-spacing:.16em;text-transform:uppercase;opacity:.85;margin-bottom:.8rem}}:lang(ka) .w-sub{{text-transform:none;letter-spacing:.02em}}
.go{{display:inline-flex;align-items:center;gap:.7rem;font-weight:600;padding:.4rem .4rem .4rem 1.2rem;border-radius:99px;background:rgba(255,255,255,.14);backdrop-filter:blur(10px);box-shadow:inset 0 0 0 1px rgba(255,255,255,.24)}}
.slide:hover .ic{{transform:translate(2px,-2px) scale(1.06)}}
.count{{display:none}}
/* moving band of what we build for */
.band{{overflow:hidden;padding-block:clamp(2.5rem,5vw,4rem);border-bottom:1px solid var(--hair)}}
.band-track{{display:flex;width:max-content;gap:3rem;font-family:var(--serif);font-size:clamp(2.2rem,5.4vw,4.8rem);line-height:1;white-space:nowrap}}
.band-track span{{display:inline-flex;align-items:center;gap:3rem}}.band-track span::after{{content:"";width:.5em;height:.5em;border-radius:50%;background:var(--gold);opacity:.8}}
/* proof numbers */
.proof{{display:grid;grid-template-columns:repeat(4,1fr);gap:2rem;padding-block:clamp(3rem,6vw,5rem)}}
.proof b{{display:block;font-family:var(--serif);font-weight:400;font-size:clamp(2.8rem,5vw,4.6rem);line-height:1;margin-bottom:.6rem}}.proof span{{font-size:.85rem;color:var(--muted)}}
/* steps with a progress line */
.steps-wrap{{position:relative}}.bar{{display:none}}
@media (min-width:961px){{
 html.fx .reel-stage{{position:relative;display:block;height:100svh;width:100%;}}
 html.fx .slide{{position:absolute;inset:0;height:auto;border-radius:0}}
 html.fx .count{{display:block;position:absolute;right:clamp(20px,5vw,64px);top:7.5rem;z-index:5;color:#fff;font:500 .8rem/1 var(--sans);letter-spacing:.2em}}
 html.fx .how .steps{{grid-template-columns:1fr;gap:0;max-width:760px;margin-left:auto}}
 html.fx .how .steps li{{display:grid;grid-template-columns:6rem 1fr;column-gap:2rem;padding-block:2rem}}html.fx .how .n{{grid-row:span 2;margin:0}}
 html.fx .how .bar{{display:block;position:absolute;left:-2rem;top:0;bottom:0;width:1px;background:rgba(239,233,224,.16)}}html.fx .how .bar i{{display:block;height:100%;background:var(--gold);transform-origin:top;transform:scaleY(0)}}
 html.fx .how .wrap{{display:grid;grid-template-columns:.8fr 1.2fr;gap:4rem;align-items:start}}html.fx .how .head{{position:sticky;top:8rem}}
}}
@media (max-width:400px){{.pill{{gap:.45rem;padding-left:.9rem}}.logo{{font-size:1.1rem;gap:.35rem}}.logo svg{{width:18px;height:18px}}.langs a{{padding:.3rem .32rem}}
.proof b{{font-size:clamp(1.9rem,9vw,2.6rem)}}.proof>*{{min-width:0;overflow-wrap:anywhere}}}}
@media (max-width:960px){{.faq-grid,.c-grid{{grid-template-columns:1fr}}.faq-grid .head{{position:static}}
.steps{{grid-template-columns:1fr 1fr}}.plans{{grid-template-columns:1fr}}.pill nav{{display:none}}.proof{{grid-template-columns:1fr 1fr}}.hero-row{{align-items:flex-start}}}}
@media (max-width:640px){{.mini{{display:none}}.steps{{grid-template-columns:1fr}}.st{{transform:none!important}}.pill{{padding-right:.6rem}}}}
.menu-btn{{display:none}}@media (max-width:900px){{.pill{{position:relative}}.menu-btn{{display:grid;place-content:center;gap:5px;flex:none;width:2.5rem;height:2.5rem;margin-left:auto;border:0;border-radius:50%;background:rgba(255,255,255,.16);color:inherit;cursor:pointer}}.nav[data-solid="1"] .menu-btn{{background:rgba(29,26,23,.07)}}.menu-btn span{{display:block;width:16px;height:1.5px;background:currentColor;transition:transform .35s var(--ease)}}.pill.open .menu-btn span:first-child{{transform:translateY(3.25px) rotate(45deg)}}.pill.open .menu-btn span:last-child{{transform:translateY(-3.25px) rotate(-45deg)}}.pill.open nav{{display:flex;position:absolute;top:calc(100% + 8px);left:0;right:0;flex-direction:column;gap:0;padding:.5rem;border-radius:1.4rem;background:rgba(250,247,242,.98);color:var(--ink);box-shadow:inset 0 0 0 1px rgba(29,26,23,.08),0 24px 48px -20px rgba(20,14,10,.35)}}.pill.open nav a{{padding:.9rem 1rem;font-size:1rem;opacity:1;border-radius:1rem}}.pill.open nav a:active{{background:rgba(29,26,23,.06)}}}}
</style></head><body>
<header class="nav" data-solid="0"><div class="pill"><a class="logo" href="{pre}{sub_dir(lang)}">{LOGO}Serai Studio</a>
<nav id="mnav" aria-label="Main">{"".join(f'<a href="#{i}">{e(n)}</a>' for i, n in zip(ids, c["nav"]))}</nav>{switch}<a class="mini" href="#contact">{e(c["nav"][4])}</a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu"><span></span><span></span></button></div></header>
<main>
<section class="hero"><div class="wrap"><p class="tag rv">{e(c["eyebrow"])}</p><h1 class="rv">{e(c["h1"])}</h1>
<div class="hero-row"><p class="lead rv">{e(c["lead"])}</p><div class="ctas rv"><a class="btn" href="#contact"><span>{e(c["cta"])}</span>{ARROW}</a><a class="ghost" href="#work">{e(c["cta2"])}</a></div></div></div></section>
<section id="work" class="reel"><div class="wrap head reel-head rv"><p class="tag">{e(c["sample_l"])}</p><h2>{e(c["work_h"])}</h2><p class="note">{e(c["work_note"])}</p></div>
<div class="reel-stage">{"".join(cards)}<p class="count" aria-hidden="true"><span class="cur">01</span> / {len(cards):02d}</p></div></section>
<div class="band" aria-hidden="true"><div class="band-track">{band}</div></div>
<div class="wrap proof">{proof}</div>
<section id="prices" class="wrap prices"><div class="head rv"><p class="tag">{"KRW" if lang == "ko" else "GEL · USD"}</p><h2>{e(c["prices_h"])}</h2></div><div class="plans">{plans}</div><p class="note rv">{e(c["prices_note"])}</p></section>
<section id="how" class="how"><div class="wrap"><div class="head rv"><p class="tag">{e(c["hero_tag"])}</p><h2>{e(c["steps_h"])}</h2></div><div class="steps-wrap"><span class="bar" aria-hidden="true"><i></i></span><ol class="steps">{steps}</ol></div></div></section>
<section id="faq" class="wrap faq-grid"><div class="head rv"><h2>{e(c["faq_h"])}</h2></div><div>{faq}</div></section>
<section id="contact" class="contact"><div class="wrap c-grid"><h2 class="rv">{e(c["contact_h"])}</h2><div class="rv"><p>{e(c["contact_p"])}</p>
<span class="mail">{EMAIL}</span><a class="btn" href="{mail}"><span>{e(c["cta"])}</span>{ARROW}</a></div></div>
<footer class="wrap">© Serai Studio<p class="credits">{e(c.get("privacy", T["en"]["privacy"]))}</p>{credits}</footer></section>
</main></body></html>'''


def write(out: Path):
    for l in LANGS:  # Korean page (/ko/) dropped 2026-11-27: overseas only
        d = out if l == "en" else out / l
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(render(l), encoding="utf-8")
    (out / ".nojekyll").write_text("")
    from build import VENDOR
    for f, head in VENDOR.items():  # same motion kit as the samples, with licence notices
        (out / f).write_text(head + (HERE / "vendor" / f).read_text(encoding="utf-8"), encoding="utf-8")
    for f in ("motion.js", "motion.css"):
        (out / f).write_text((HERE / "assets" / f).read_text(encoding="utf-8"), encoding="utf-8")
