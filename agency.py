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
  prices_h="Two simple prices", prices_note="Prices are one time. The price includes the first year of hosting. The domain name (about $10 to $15 a year) is registered in your name, so the site always belongs to you.",
  plans=[
   ("Starter", "$150", "or 400 GEL, one time", ["One-page website", "English + Russian. Georgian too, after you check the Georgian text", "Rooms, prices and photos", "WhatsApp button and Google Maps link", "Works on every phone", "First year of hosting and domain setup", "Private preview within 3 working days after we get your info and photos"]),
   ("Care", "$150", "per year, from the second year", ["Hosting", "Price, photo and text updates (up to 30 minutes a month)", "Domain renewal reminders", "We check every month that the site works", "Answer within one working day"]),
  ],
  steps_h="How it works",
  steps=[("Write to us", "Send your business name and a link to your Google Maps, Instagram or Booking.com page."),
         ("Free preview", "Within 3 working days after we get your info and photos, we send a private preview that search engines do not show."),
         ("Your changes", "Tell us what to change in a message. We fix it, usually the same day."),
         ("Go live", "You pay only when you are happy. We connect your domain and the site goes live.")],
  faq_h="Questions",
  faq=[("Why do I need a website if I am on Booking.com?", "Booking.com takes a commission on every booking and shows guests your competitors next to you. Your own site lets guests contact you directly and see everything you offer."),
       ("How do we talk?", "We work in writing, by email and WhatsApp messages. Every price and change is written down, nothing gets lost in translation, and you can answer when it suits you. We work remotely from Seoul. You may also write to us in Georgian."),
       ("How do I pay?", "By bank transfer or card payment link, after you approve the preview."),
       ("What happens after the first year?", "You choose: the Care plan at $150 a year, or we hand over all site files for free."),
       ("Can you use photos from my Booking.com or Google page?", "Only photos you own or have permission to use. Please send the original files and tell us who took them."),
       ("Who owns the website?", "You do. The domain is registered in your name."),
       ("Can you add Georgian, Armenian or another language?", "Every site is in English and Russian. Georgian is added at no cost, after you check the Georgian text.")],
  contact_h="Let's make your preview", contact_p="Send us your business name and one link where guests can find you today. We answer within one working day.",
  email_l="Email", sample_l="Open sample", mail_subject="Website preview", langs="Language", hero_tag="Serai Studio"),
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
  prices_h="Две простые цены", prices_note="Цены разовые. Цена включает хостинг на первый год. Домен (примерно $10–15 в год) регистрируется на ваше имя, поэтому сайт всегда принадлежит вам.",
  plans=[
   ("Старт", "$150", "или 400 лари, один раз", ["Одностраничный сайт", "Английский и русский. Грузинский тоже, после того как вы проверите текст", "Номера, цены и фото", "Кнопка WhatsApp и ссылка на Google Maps", "Удобно на любом телефоне", "Хостинг на первый год и подключение домена", "Закрытый пример через 3 рабочих дня после получения данных и фото"]),
   ("Поддержка", "$150", "в год, со второго года", ["Хостинг", "Обновление цен, фото и текстов (до 30 минут в месяц)", "Напоминания о продлении домена", "Ежемесячная проверка работы сайта", "Ответ в течение рабочего дня"]),
  ],
  steps_h="Как это работает",
  steps=[("Напишите нам", "Пришлите название и ссылку на вашу страницу в Google Maps, Instagram или Booking.com."),
         ("Бесплатный пример", "Через 3 рабочих дня после получения данных и фото мы пришлём закрытый пример, который не видят поисковики."),
         ("Ваши правки", "Напишите, что изменить. Обычно исправляем в тот же день."),
         ("Запуск", "Оплата только когда вам всё нравится. Подключаем домен, и сайт работает.")],
  faq_h="Вопросы",
  faq=[("Зачем сайт, если я есть на Booking.com?", "Booking.com берёт комиссию с каждой брони и показывает гостям конкурентов рядом с вами. Свой сайт позволяет гостям писать вам напрямую и видеть всё, что вы предлагаете."),
       ("Как мы общаемся?", "Мы работаем письменно: почта и сообщения в WhatsApp. Все цены и правки записаны, ничего не теряется при переводе, и вы отвечаете, когда удобно. Мы работаем удалённо из Сеула. Можно писать и по-грузински."),
       ("Как оплатить?", "Банковским переводом или по ссылке на оплату картой, после того как вы одобрите пример."),
       ("Что после первого года?", "Выбираете вы: «Поддержка» за $150 в год или бесплатная передача всех файлов сайта."),
       ("Можно взять фото с моей страницы Booking.com или Google?", "Только фото, которые принадлежат вам или на которые у вас есть разрешение. Пришлите оригиналы и напишите, кто снимал."),
       ("Кому принадлежит сайт?", "Вам. Домен регистрируется на ваше имя."),
       ("Можно добавить грузинский, армянский или другой язык?", "Каждый сайт на английском и русском. Грузинский добавляем бесплатно, после того как вы проверите текст.")],
  contact_h="Сделаем ваш пример", contact_p="Пришлите название и одну ссылку, где гости находят вас сейчас. Отвечаем в течение рабочего дня.",
  email_l="Почта", sample_l="Открыть пример", mail_subject="Пример сайта", langs="Язык", hero_tag="Serai Studio"),
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
    cards, heroes, creds = [], [], []
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
        cards.append(f'<a class="w bezel rv" href="{href}"><div class="core"><img src="{src}" alt="" loading="lazy" decoding="async">'
                     f'<div class="w-cap"><p class="w-sub">{e(label)}</p><h3>{e(name)}</h3><span class="w-go">{e(c["sample_l"])} {ARROW}</span></div></div></a>')
    stack = "".join(f'<div class="st st{i} bezel"><div class="core"><img src="{h}" alt="" decoding="async"{"" if i == 0 else " loading=\"lazy\""}></div></div>' for i, h in enumerate(heroes[:3]))

    plans = "".join(f'''<article class="plan{" dark" if i == 0 else ""} rv"><div class="p-in"><p class="p-name">{e(n)}</p><p class="amt"><b>{e(p)}</b><span>{e(unit)}</span></p>
<ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul>{f'<a class="btn" href="{mail}"><span>{e(c["cta"])}</span>{ARROW}</a>' if i == 0 else ""}</div></article>''' for i, (n, p, unit, items) in enumerate(c["plans"]))
    su = SUI.get(lang, SUI["en"])
    link = lambda c: f'<a href="{e(c["page"])}" target="_blank" rel="noopener">{e(c["artist"])}</a> (' + (
        f'<a href="{e(lic_url(c["license"]))}" target="_blank" rel="noopener license">{e(c["license"])}</a>' if lic_url(c["license"]) else e(c["license"])) + ")"
    credits = "" if not creds else f'<p class="credits">{e(su["photos_by"])}: ' + ", ".join(link(c) for c in creds) + f'. {e(su["modified"])}</p>'
    steps = "".join(f'<li class="rv"><span class="n">0{i}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(c["steps"], 1))
    faq = "".join(f'<details class="rv"><summary>{e(q)}{PLUS}</summary><p>{e(a)}</p></details>' for q, a in c["faq"])
    proof = "".join(f'<div class="rv"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in c["proof"])
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
<script>{js}</script>
<style>
:root{{--gold-t:#86601f;--paper:#f6f3ed;--ink:#191714;--muted:#6b665d;--hair:rgba(25,23,20,.12);--accent:#14524b;--gold:#b5873a;--deep:#14201d;
--serif:"Instrument Serif","Noto Serif Georgian",Georgia,serif;--sans:"Hanken Grotesk","Noto Sans Georgian",system-ui,-apple-system,"Segoe UI",sans-serif;--ease:cubic-bezier(.32,.72,0,1)}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:90px}}
body{{margin:0;background:var(--paper);color:var(--ink);font:400 16.5px/1.7 var(--sans);-webkit-font-smoothing:antialiased}}
body::after{{content:"";position:fixed;inset:0;pointer-events:none;z-index:90;opacity:.05;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}}
img{{display:block;max-width:100%}}a{{color:inherit}}:focus-visible{{outline:2px solid var(--accent);outline-offset:4px;border-radius:6px}}p{{margin:0}}
.wrap{{width:min(1240px,100% - 2*clamp(20px,5vw,64px));margin-inline:auto}}
h1,h2,h3{{font-family:var(--serif);font-weight:400;letter-spacing:-.015em;margin:0;text-wrap:balance}}
h2{{font-size:clamp(2.6rem,6vw,5.2rem);line-height:.98}}h3{{font-size:1.6rem;line-height:1.1}}
html[lang=ko]{{--serif:"Noto Serif KR","Instrument Serif",serif;--sans:"Noto Sans KR","Hanken Grotesk",system-ui,sans-serif}}html[lang=ko] body{{word-break:keep-all}}html[lang=ko] h1,html[lang=ko] h2,html[lang=ko] h3{{font-weight:500;letter-spacing:-.02em}}html[lang=ko] h2{{font-size:clamp(2rem,4.4vw,3.6rem);line-height:1.18}}html[lang=ko] .hero h1{{font-size:clamp(2.2rem,4.8vw,4.4rem);line-height:1.18}}html[lang=ko] .contact h2{{font-size:clamp(2.2rem,5vw,4.4rem);line-height:1.18}}html[lang=ko] summary{{font-size:clamp(1.1rem,1.6vw,1.35rem)}}html[lang=ko] .mail{{font-size:clamp(1.15rem,1.9vw,1.6rem)}}html[lang=ko] .amt b{{font-size:clamp(2.8rem,5vw,4.2rem)}}:lang(ko) .tag,:lang(ko) .p-name,:lang(ko) .w-sub{{text-transform:none;letter-spacing:.04em}}
html[lang=ka] h1,html[lang=ka] h2,html[lang=ka] h3{{font-weight:300;letter-spacing:0}}html[lang=ka] h2{{font-size:clamp(2rem,4.4vw,3.6rem);line-height:1.15}}
.tag{{display:inline-flex;font:500 .7rem/1 var(--sans);letter-spacing:.22em;text-transform:uppercase;padding:.55rem .9rem;border-radius:99px;color:var(--gold-t);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--gold) 40%,transparent)}}.how .tag{{color:var(--gold)}}
:lang(ka) .tag{{text-transform:none;letter-spacing:.04em}}
.nav{{position:fixed;top:18px;left:0;right:0;z-index:50;display:flex;justify-content:center;pointer-events:none}}
.pill{{pointer-events:auto;display:flex;align-items:center;gap:clamp(.8rem,2vw,1.8rem);padding:.45rem .45rem .45rem 1.3rem;border-radius:99px;background:rgba(246,243,237,.72);
box-shadow:inset 0 0 0 1px var(--hair);backdrop-filter:blur(18px) saturate(1.4);transition:box-shadow .6s var(--ease),background .6s var(--ease)}}
.nav[data-solid="1"] .pill{{background:rgba(246,243,237,.9);box-shadow:inset 0 0 0 1px var(--hair),0 24px 48px -28px rgba(40,30,20,.35)}}
.logo{{display:flex;align-items:center;gap:.5rem;font-family:var(--serif);font-size:1.35rem;text-decoration:none;white-space:nowrap}}.logo svg{{color:var(--gold)}}
.pill nav{{display:flex;gap:1.3rem;font-size:.88rem}}.pill nav a{{text-decoration:none;opacity:.72;transition:opacity .3s}}.pill nav a:hover{{opacity:1}}
.langs{{display:flex;gap:.1rem}}.langs a{{font-size:.7rem;font-weight:600;letter-spacing:.08em;text-decoration:none;padding:.35rem .5rem;border-radius:99px;opacity:.6}}.langs a[aria-current]{{opacity:1;box-shadow:inset 0 0 0 1px currentColor}}
.mini{{font-size:.82rem;font-weight:600;text-decoration:none;padding:.65rem 1.1rem;border-radius:99px;background:var(--ink);color:#fff;white-space:nowrap}}
.btn{{display:inline-flex;align-items:center;gap:.9rem;padding:.45rem .45rem .45rem 1.5rem;border-radius:99px;background:var(--ink);color:#fff;text-decoration:none;font-weight:600;font-size:.95rem;transition:transform .5s var(--ease)}}
.btn:active{{transform:scale(.98)}}.ic{{display:grid;place-items:center;flex:none;width:2.4rem;height:2.4rem;border-radius:50%;background:rgba(255,255,255,.14);transition:transform .5s var(--ease)}}
.btn:hover .ic,.w:hover .ic{{transform:translate(2px,-2px) scale(1.06)}}
.ghost{{display:inline-flex;align-items:center;padding:.95rem 1.4rem;border-radius:99px;text-decoration:none;font-weight:600;font-size:.95rem;box-shadow:inset 0 0 0 1px var(--hair)}}
.bezel{{padding:.45rem;border-radius:1.7rem;background:rgba(25,23,20,.04);box-shadow:inset 0 0 0 1px rgba(25,23,20,.06)}}
.core{{position:relative;border-radius:calc(1.7rem - .45rem);overflow:hidden;height:100%}}.core img{{width:100%;height:100%;object-fit:cover;transition:transform 1.4s var(--ease)}}
.hero{{min-height:100svh;display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(2rem,5vw,5rem);align-items:center;padding-block:8rem 4rem}}
.hero h1{{font-size:clamp(3.2rem,7.4vw,7.4rem);line-height:.92;margin:1.6rem 0 2rem}}
html[lang=ka] .hero h1{{font-size:clamp(2.2rem,4.6vw,4.4rem);line-height:1.12}}html[lang=ru] .hero h1{{font-size:clamp(2.8rem,6vw,6rem)}}
.lead{{max-width:48ch;font-size:clamp(1.02rem,1.4vw,1.15rem);color:var(--muted)}}.ctas{{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:2.2rem}}
.stack{{position:relative;height:min(78svh,680px)}}.st{{position:absolute;width:62%;aspect-ratio:3/4;transition:transform 1.2s var(--ease)}}
.st0{{right:0;top:4%;z-index:3;transform:rotate(2deg)}}.st1{{left:4%;top:18%;z-index:2;transform:rotate(-4deg);width:52%}}.st2{{right:22%;bottom:0;z-index:1;transform:rotate(-1deg);width:46%}}
.st{{background:rgba(246,243,237,.9);box-shadow:inset 0 0 0 1px rgba(25,23,20,.08),0 40px 80px -40px rgba(30,20,10,.45)}}
.stack:hover .st0{{transform:rotate(0) translateY(-6px)}}.stack:hover .st1{{transform:rotate(-6deg) translateX(-10px)}}
.proof{{display:grid;grid-template-columns:repeat(4,1fr);gap:2rem;padding-block:3rem 4rem;border-top:1px solid var(--hair)}}
.proof b{{display:block;font-family:var(--serif);font-weight:400;font-size:clamp(2.4rem,4vw,3.4rem);line-height:1;margin-bottom:.5rem}}.proof span{{color:var(--muted);font-size:.9rem}}
section{{padding-block:clamp(5rem,10vw,9rem)}}.head{{display:flex;flex-direction:column;align-items:flex-start;gap:1.3rem;margin-bottom:clamp(2.5rem,5vw,4rem)}}.note{{color:var(--muted);max-width:60ch}}
.works{{display:grid;grid-template-columns:repeat(12,1fr);gap:clamp(1rem,2vw,1.6rem)}}
.w{{text-decoration:none;color:#fff;display:block}}.w:nth-child(1){{grid-column:span 7;height:clamp(360px,40vw,560px)}}.w:nth-child(2){{grid-column:span 5;height:clamp(360px,40vw,560px)}}
.w:nth-child(3){{grid-column:span 5;height:clamp(300px,32vw,460px)}}.w:nth-child(4){{grid-column:span 7;height:clamp(300px,32vw,460px)}}
.w .core::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(10,8,6,.72))}}.w:hover .core img{{transform:scale(1.05)}}
.w-cap{{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:clamp(1.2rem,2.4vw,2rem);display:grid;gap:.3rem}}
.w h3{{font-size:clamp(1.8rem,3vw,2.6rem)}}.w-sub{{font-size:.75rem;letter-spacing:.16em;text-transform:uppercase;opacity:.8}}:lang(ka) .w-sub{{text-transform:none;letter-spacing:.02em}}
.w-go{{display:inline-flex;align-items:center;gap:.6rem;font-weight:600;font-size:.9rem;margin-top:.6rem}}.w-go .ic{{width:2rem;height:2rem;background:rgba(255,255,255,.18)}}
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
@media (max-width:960px){{.hero,.faq-grid,.c-grid{{grid-template-columns:1fr}}.hero{{padding-top:7rem;min-height:auto}}.stack{{height:min(110vw,560px)}}.faq-grid .head{{position:static}}
.steps{{grid-template-columns:1fr 1fr}}.plans{{grid-template-columns:1fr}}.pill nav{{display:none}}.works .w{{grid-column:span 12!important;height:clamp(300px,90vw,480px)!important}}.proof{{grid-template-columns:1fr 1fr}}}}
@media (max-width:640px){{.mini{{display:none}}.steps{{grid-template-columns:1fr}}.st{{transform:none!important}}.pill{{padding-right:.6rem}}}}
.menu-btn{{display:none}}@media (max-width:900px){{.pill{{position:relative}}.menu-btn{{display:grid;place-content:center;gap:5px;flex:none;width:2.5rem;height:2.5rem;margin-left:auto;border:0;border-radius:50%;background:rgba(255,255,255,.16);color:inherit;cursor:pointer}}.nav[data-solid="1"] .menu-btn{{background:rgba(29,26,23,.07)}}.menu-btn span{{display:block;width:16px;height:1.5px;background:currentColor;transition:transform .35s var(--ease)}}.pill.open .menu-btn span:first-child{{transform:translateY(3.25px) rotate(45deg)}}.pill.open .menu-btn span:last-child{{transform:translateY(-3.25px) rotate(-45deg)}}.pill.open nav{{display:flex;position:absolute;top:calc(100% + 8px);left:0;right:0;flex-direction:column;gap:0;padding:.5rem;border-radius:1.4rem;background:rgba(250,247,242,.98);color:var(--ink);box-shadow:inset 0 0 0 1px rgba(29,26,23,.08),0 24px 48px -20px rgba(20,14,10,.35)}}.pill.open nav a{{padding:.9rem 1rem;font-size:1rem;opacity:1;border-radius:1rem}}.pill.open nav a:active{{background:rgba(29,26,23,.06)}}}}
</style></head><body>
<header class="nav" data-solid="0"><div class="pill"><a class="logo" href="{pre}{sub_dir(lang)}">{LOGO}Serai Studio</a>
<nav id="mnav" aria-label="Main">{"".join(f'<a href="#{i}">{e(n)}</a>' for i, n in zip(ids, c["nav"]))}</nav>{switch}<a class="mini" href="#contact">{e(c["nav"][4])}</a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu"><span></span><span></span></button></div></header>
<main>
<section class="hero wrap"><div><p class="tag rv">{e(c["eyebrow"])}</p><h1 class="rv">{e(c["h1"])}</h1><p class="lead rv">{e(c["lead"])}</p>
<div class="ctas rv"><a class="btn" href="#contact"><span>{e(c["cta"])}</span>{ARROW}</a><a class="ghost" href="#work">{e(c["cta2"])}</a></div></div>
<div class="stack rv" aria-hidden="true">{stack}</div></section>
<div class="wrap proof">{proof}</div>
<section id="work" class="wrap"><div class="head rv"><p class="tag">{e(c["sample_l"])}</p><h2>{e(c["work_h"])}</h2><p class="note">{e(c["work_note"])}</p></div><div class="works">{"".join(cards)}</div></section>
<section id="prices" class="wrap prices"><div class="head rv"><p class="tag">{"KRW" if lang == "ko" else "GEL · USD"}</p><h2>{e(c["prices_h"])}</h2></div><div class="plans">{plans}</div><p class="note rv">{e(c["prices_note"])}</p></section>
<section id="how" class="how"><div class="wrap"><div class="head rv"><p class="tag">{e(c["hero_tag"])}</p><h2>{e(c["steps_h"])}</h2></div><ol class="steps">{steps}</ol></div></section>
<section id="faq" class="wrap faq-grid"><div class="head rv"><h2>{e(c["faq_h"])}</h2></div><div>{faq}</div></section>
<section id="contact" class="contact"><div class="wrap c-grid"><h2 class="rv">{e(c["contact_h"])}</h2><div class="rv"><p>{e(c["contact_p"])}</p>
<span class="mail">{EMAIL}</span><a class="btn" href="{mail}"><span>{e(c["cta"])}</span>{ARROW}</a></div></div>
<footer class="wrap">© Serai Studio{credits}</footer></section>
</main></body></html>'''


def write(out: Path):
    for l in LANGS + ["ko"]:
        d = out if l == "en" else out / l
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(render(l), encoding="utf-8")
    (out / ".nojekyll").write_text("")
