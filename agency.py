"""Serai Studio's own website: site/index.html (English), site/ru/ and site/ka/ (Georgian)."""
import html
import json
from pathlib import Path

EMAIL = "seraistudio.web@gmail.com"
BASE = "https://preparedmale.github.io/client-sites"

T = {
 "en": dict(
  title="Serai Studio · Websites for guesthouses, wineries and tours",
  desc="Serai Studio builds fast, bilingual websites for small hospitality businesses in Georgia, Armenia and Central Asia. Fixed prices, free preview, you only pay if you like it.",
  nav=["Work", "Prices", "How it works", "Questions", "Contact"],
  eyebrow="Georgia · Armenia · Central Asia",
  h1="Websites for the places travellers remember",
  lead="We build websites for family guesthouses, wineries, tour guides and small restaurants. Your rooms, prices and story in English and Russian, with one button that brings guests straight to your WhatsApp.",
  cta="See a free preview for your business", cta2="See our work",
  proof=[("Free", "preview before you pay"), ("3 days", "from photos to live site"), ("2+", "languages on every site"), ("0", "booking commission")],
  work_h="Recent work", work_note="These are sample sites for fictional businesses, made to show what we build.",
  prices_h="Simple, fixed prices", prices_note="Prices are one time and include the first year of hosting. The domain name (about $10 to $15 a year) is registered in your name, so the site always belongs to you.",
  plans=[
   ("Starter", "$150", "or 400 GEL, one time", ["One-page website", "Two languages of your choice", "Rooms, prices and photos", "WhatsApp button and Google Maps link", "Works on every phone", "First year of hosting and domain setup", "Ready 3 days after we get your photos"]),
   ("Plus", "$290", "or 780 GEL, one time", ["Everything in Starter", "Up to 4 languages", "Photo gallery and menu or price list", "Help setting up your Google Business Profile", "Two rounds of changes"]),
   ("Care", "$15", "per month, or $150 per year", ["Hosting from the second year", "Price, photo and text updates (up to 30 minutes a month)", "We check every month that the site works", "Answer within one working day"]),
  ],
  steps_h="How it works",
  steps=[("Write to us", "Send your business name and a link to your Google Maps, Instagram or Booking.com page."),
         ("Free preview", "Within 3 days we send you a working preview of your website, built with your photos and details."),
         ("Your changes", "Tell us what to change in a message. We fix it, usually the same day."),
         ("Go live", "You pay only when you are happy. We connect your domain and the site goes live.")],
  faq_h="Questions",
  faq=[("Why do I need a website if I am on Booking.com?", "Booking.com takes a commission on every booking and shows guests your competitors next to you. Your own site lets guests contact you directly and see everything you offer."),
       ("How do we talk?", "We work in writing, by email and WhatsApp messages. Every price and change is written down, nothing gets lost in translation, and you can answer when it suits you. We reply in English or Russian."),
       ("How do I pay?", "By bank transfer or card payment link, after you approve the preview. For the Care plan you can pay monthly or once a year."),
       ("What happens after the first year?", "You choose: keep the Care plan, or we hand over all site files for free."),
       ("Who owns the website?", "You do. The domain is registered in your name. If you ever leave the Care plan, we hand over all files."),
       ("Can you add Georgian, Armenian or another language?", "Yes. Starter includes two languages, Plus up to four. Texts in local languages are checked with you before going live.")],
  contact_h="Let's make your preview", contact_p="Send us your business name and one link where guests can find you today. We answer within one working day.",
  email_l="Email", sample_l="Open sample", mail_subject="Website preview",
  langs="Language"),
 "ru": dict(
  title="Serai Studio · Сайты для гостевых домов, виноделен и туров",
  desc="Serai Studio делает быстрые двуязычные сайты для небольшого гостеприимного бизнеса в Грузии, Армении и Центральной Азии. Фиксированные цены, бесплатный пример, оплата только если понравится.",
  nav=["Работы", "Цены", "Как это работает", "Вопросы", "Контакты"],
  eyebrow="Грузия · Армения · Центральная Азия",
  h1="Сайты для мест, которые путешественники запоминают",
  lead="Мы делаем сайты для семейных гостевых домов, виноделен, гидов и небольших ресторанов. Ваши номера, цены и история на английском и русском, и одна кнопка, которая ведёт гостей прямо в ваш WhatsApp.",
  cta="Получить бесплатный пример сайта", cta2="Посмотреть работы",
  proof=[("Бесплатно", "пример до оплаты"), ("3 дня", "от фото до готового сайта"), ("2+", "языка на каждом сайте"), ("0", "комиссии с бронирований")],
  work_h="Наши работы", work_note="Это примеры сайтов для вымышленных заведений, чтобы показать, что мы делаем.",
  prices_h="Простые фиксированные цены", prices_note="Цены разовые и включают хостинг на первый год. Домен (примерно $10–15 в год) регистрируется на ваше имя, поэтому сайт всегда принадлежит вам.",
  plans=[
   ("Старт", "$150", "или 400 лари, один раз", ["Одностраничный сайт", "Два языка на ваш выбор", "Номера, цены и фото", "Кнопка WhatsApp и ссылка на Google Maps", "Удобно на любом телефоне", "Хостинг на первый год и подключение домена", "Готово через 3 дня после получения фото"]),
   ("Плюс", "$290", "или 780 лари, один раз", ["Всё из «Старт»", "До 4 языков", "Фотогалерея и меню или прайс", "Помощь с профилем Google Business", "Два круга правок"]),
   ("Поддержка", "$15", "в месяц или $150 в год", ["Хостинг со второго года", "Обновление цен, фото и текстов (до 30 минут в месяц)", "Ежемесячная проверка работы сайта", "Ответ в течение рабочего дня"]),
  ],
  steps_h="Как это работает",
  steps=[("Напишите нам", "Пришлите название и ссылку на вашу страницу в Google Maps, Instagram или Booking.com."),
         ("Бесплатный пример", "За 3 дня мы пришлём рабочий пример сайта с вашими фото и данными."),
         ("Ваши правки", "Напишите, что изменить. Обычно исправляем в тот же день."),
         ("Запуск", "Оплата только когда вам всё нравится. Подключаем домен, и сайт работает.")],
  faq_h="Вопросы",
  faq=[("Зачем сайт, если я есть на Booking.com?", "Booking.com берёт комиссию с каждой брони и показывает гостям конкурентов рядом с вами. Свой сайт позволяет гостям писать вам напрямую и видеть всё, что вы предлагаете."),
       ("Как мы общаемся?", "Мы работаем письменно: почта и сообщения в WhatsApp. Все цены и правки записаны, ничего не теряется при переводе, и вы отвечаете, когда удобно. Отвечаем на английском или русском."),
       ("Как оплатить?", "Банковским переводом или по ссылке на оплату картой, после того как вы одобрите пример. Поддержку можно оплачивать помесячно или раз в год."),
       ("Что после первого года?", "Выбираете вы: продолжить «Поддержку» или бесплатно получить все файлы сайта."),
       ("Кому принадлежит сайт?", "Вам. Домен регистрируется на ваше имя. Если откажетесь от поддержки, передадим все файлы."),
       ("Можно добавить грузинский, армянский или другой язык?", "Да. В «Старт» два языка, в «Плюс» до четырёх. Тексты на местных языках согласуем с вами до запуска.")],
  contact_h="Сделаем ваш пример", contact_p="Пришлите название и одну ссылку, где гости находят вас сейчас. Отвечаем в течение рабочего дня.",
  email_l="Почта", sample_l="Открыть пример", mail_subject="Пример сайта",
  langs="Язык"),
}
T["ka"] = json.loads((Path(__file__).parent / "i18n" / "agency_ka.json").read_text(encoding="utf-8"))
LANGS = ["en", "ru", "ka"]

WORK = [("cloudline-kazbegi", "Cloudline Guesthouse", {"en": "Guesthouse · Kazbegi, Georgia", "ru": "Гостевой дом · Казбеги, Грузия"}, "#1d5873"),
        ("babua-marani", "Babua's Marani", {"en": "Family winery · Kakheti, Georgia", "ru": "Семейная винодельня · Кахетия, Грузия"}, "#7a2440"),
        ("steppe-roads", "Steppe Roads", {"en": "Trekking tours · Karakol, Kyrgyzstan", "ru": "Треккинг-туры · Каракол, Кыргызстан"}, "#2f6b3a"),
        ("dukani-nine", "Dukani Nine", {"en": "Restaurant · Old Tbilisi, Georgia", "ru": "Ресторан · Старый Тбилиси, Грузия"}, "#8a4b14")]


def e(s):
    return html.escape(str(s), quote=True)


def render(lang):
    c = T[lang]
    pre = "./" if lang == "en" else "../"
    sub_dir = lambda l: "" if l == "en" else l + "/"
    ids = ["work", "prices", "how", "faq", "contact"]
    switch = '<div class="langs">' + "".join(f'<a class="lang" href="{pre}{sub_dir(l)}" hreflang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{l.upper()}</a>' for l in LANGS) + "</div>"

    def card(slug, name, sub, col):
        cl = json.loads((Path(__file__).parent / "clients" / f"{slug}.json").read_text(encoding="utf-8"))
        langs = cl.get("languages") or ["en"]
        href = f"{pre}{slug}/" + ("" if lang == langs[0] or lang not in langs else lang + "/")
        photo = (cl.get("photos") or [{}])[0].get("file")
        thumb = (f'<img src="{pre}{slug}/{photo}" alt="" loading="lazy">' if photo else "") + f"<span>{e(name)}</span>"
        label = c.get("work_sub", {}).get(slug) or sub.get(lang) or sub["en"]
        return (f'<a class="work" href="{href}" style="--c:{col}"><div class="thumb" aria-hidden="true">{thumb}</div>'
                f'<div class="wmeta"><b>{e(name)}</b><span>{e(label)}</span><em>{e(c["sample_l"])} →</em></div></a>')
    work = "".join(card(*w) for w in WORK)
    plans = "".join(f'''<article class="plan{' hl' if i == 0 else ''}"><h3>{e(n)}</h3><p class="amt"><b>{e(p)}</b> <span>{e(unit)}</span></p>
<ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul></article>''' for i, (n, p, unit, items) in enumerate(c["plans"]))
    steps = "".join(f'<li><b>{e(a)}</b><p>{e(b)}</p></li>' for a, b in c["steps"])
    faq = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in c["faq"])
    proof = "".join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in c["proof"])
    mail = f"mailto:{EMAIL}?subject=" + __import__("urllib.parse").parse.quote(c["mail_subject"])
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(c["title"])}</title><meta name="description" content="{e(c["desc"])}">
<link rel="canonical" href="{BASE}/{sub_dir(lang)}">{"".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}/{sub_dir(l)}">' for l in LANGS)}
<meta property="og:title" content="Serai Studio"><meta property="og:description" content="{e(c["desc"])}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Inter:wght@400;500;600&family=Noto+Sans+Georgian:wght@400;600&family=Noto+Serif+Georgian:wght@400&display=swap">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ProfessionalService","name":"Serai Studio","email":"{EMAIL}","areaServed":["Georgia","Armenia","Kyrgyzstan","Uzbekistan","Kazakhstan"],"url":"{BASE}/"}}</script>
<style>
:root{{--bg:#f7f5f0;--paper:#fffdf9;--ink:#1b1a17;--muted:#66625a;--line:#e4dfd5;--accent:#0f5c55;--on:#fff;--gold:#b5873a;
--serif:"Instrument Serif","Noto Serif Georgian",Georgia,serif;--sans:"Inter","Noto Sans Georgian",system-ui,-apple-system,"Segoe UI",sans-serif}}
@media (prefers-color-scheme:dark){{:root{{--bg:#12130f;--paper:#1a1b17;--ink:#eeebe4;--muted:#a9a498;--line:#2d2e28;--accent:#5fc4b8;--on:#0d1210;--gold:#e2b56a;color-scheme:dark}}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:70px}}@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.65 var(--sans);-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1120px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left));padding-right:max(20px,env(safe-area-inset-right))}}
a{{color:var(--accent)}}a:focus-visible,summary:focus-visible{{outline:3px solid var(--accent);outline-offset:3px;border-radius:4px}}
h1,h2,h3{{font-family:var(--serif);font-weight:400;line-height:1.05;letter-spacing:-.01em;margin:0 0 .8rem;text-wrap:balance}}
h1{{font-size:clamp(2.8rem,8vw,5.6rem);max-width:14ch}}h2{{font-size:clamp(2rem,5vw,3.2rem)}}h3{{font-size:1.7rem}}
p{{margin:0 0 .8rem}}
header{{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}}
.bar{{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding-block:.8rem;flex-wrap:wrap}}
.logo{{font-family:var(--serif);font-size:1.6rem;color:var(--ink);text-decoration:none;display:flex;align-items:center;gap:.5rem}}
.logo svg{{color:var(--gold)}}nav{{display:flex;gap:1.2rem;flex-wrap:wrap;font-size:.95rem}}nav a{{color:var(--ink);text-decoration:none;opacity:.8}}nav a:hover{{opacity:1}}
.langs{{display:flex;gap:.25rem}}.lang[aria-current]{{background:var(--ink);color:var(--bg);border-color:var(--ink)}}.lang{{font-size:.8rem;font-weight:600;border:1px solid var(--line);border-radius:999px;padding:.2rem .7rem;text-decoration:none;color:var(--ink)}}
.hero{{padding-block:clamp(3rem,9vw,7rem) clamp(2.5rem,6vw,4.5rem);position:relative;overflow:hidden}}
.hero::after{{content:"";position:absolute;right:-8vw;top:8%;width:min(46vw,560px);aspect-ratio:1;border-radius:50% 50% 0 0;border:1px solid var(--line);
background:repeating-linear-gradient(90deg,transparent 0 22px,color-mix(in srgb,var(--gold) 14%,transparent) 22px 23px);z-index:-1}}
:lang(ka) .eyebrow{{text-transform:none;letter-spacing:.03em}}html[lang=ka] h1{{font-size:clamp(2.2rem,5.6vw,4rem);max-width:18ch}}html[lang=ka] h2{{font-size:clamp(1.7rem,4vw,2.6rem)}}
.eyebrow{{text-transform:uppercase;letter-spacing:.16em;font-size:.78rem;font-weight:600;color:var(--gold)}}
.lead{{font-size:clamp(1.08rem,2vw,1.25rem);color:var(--muted);max-width:56ch}}
.ctas{{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:1.6rem}}
.btn{{display:inline-block;padding:.9rem 1.5rem;border-radius:999px;font-weight:600;text-decoration:none;background:var(--accent);color:var(--on)}}
.btn.ghost{{background:transparent;color:var(--ink);border:1px solid var(--line)}}
.proof{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:1rem;margin-top:clamp(2.5rem,6vw,4rem);border-top:1px solid var(--line);padding-top:1.5rem}}
.proof b{{display:block;font-family:var(--serif);font-size:2.2rem;font-weight:400;line-height:1}}.proof span{{color:var(--muted);font-size:.9rem}}
section{{padding-block:clamp(3rem,7vw,5.5rem);border-top:1px solid var(--line)}}
.note{{color:var(--muted);font-size:.92rem}}
.works{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:1.2rem;margin-top:1.5rem}}
.work{{display:block;text-decoration:none;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:16px;overflow:hidden;transition:transform .2s}}
.work:hover{{transform:translateY(-3px)}}
.thumb{{aspect-ratio:4/3;background:linear-gradient(160deg,color-mix(in srgb,var(--c) 25%,var(--bg)),var(--c));display:flex;align-items:flex-end;padding:1rem;position:relative;overflow:hidden}}
.thumb img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .4s}}.work:hover .thumb img{{transform:scale(1.04)}}
.thumb:has(img)::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(0,0,0,.6))}}
.thumb span{{font-family:var(--serif);font-size:1.9rem;color:#fff;line-height:1;position:relative;z-index:1}}
.wmeta{{padding:1rem 1.1rem 1.2rem;display:grid;gap:.15rem}}.wmeta span{{color:var(--muted);font-size:.9rem}}.wmeta em{{font-style:normal;color:var(--accent);font-weight:600;font-size:.9rem;margin-top:.4rem}}
.plans{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:1.2rem;margin:1.5rem 0 1rem}}
.plan{{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:1.6rem}}.plan.hl{{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}}
.amt b{{font-family:var(--serif);font-size:3rem;font-weight:400}}.amt span{{color:var(--muted);font-size:.9rem}}
.plan ul{{padding-left:1.1rem;margin:.6rem 0 0}}.plan li{{margin-bottom:.35rem}}
.steps{{list-style:none;padding:0;margin:1.5rem 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:1.5rem;counter-reset:s}}
.steps li{{counter-increment:s;border-top:2px solid var(--ink);padding-top:1rem}}.steps li::before{{content:counter(s);font-family:var(--serif);font-size:2.4rem;color:var(--gold);display:block;line-height:1;margin-bottom:.4rem}}
.steps p{{color:var(--muted)}}
details{{border-bottom:1px solid var(--line);padding:1rem 0;max-width:760px}}summary{{cursor:pointer;font-weight:600;font-size:1.05rem}}details p{{margin:.6rem 0 0;color:var(--muted)}}
.contact{{background:var(--ink);color:var(--bg)}}.contact h2{{color:var(--bg)}}.contact p{{color:color-mix(in srgb,var(--bg) 75%,var(--ink));max-width:56ch}}
.contact .btn{{background:var(--bg);color:var(--ink)}}.mail{{font-weight:600;user-select:all;color:var(--bg)}}
footer{{padding-block:1.5rem;color:var(--muted);font-size:.85rem}}
</style></head><body>
<header><div class="wrap bar"><a class="logo" href="{pre}"><svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true"><path d="M3 24V12a10 10 0 0 1 20 0v12" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 24v-9a5 5 0 0 1 10 0v9" fill="none" stroke="currentColor" stroke-width="2"/></svg>Serai Studio</a>
<nav aria-label="Main">{"".join(f'<a href="#{i}">{e(n)}</a>' for i, n in zip(ids, c["nav"]))}</nav>{switch}</div></header>
<main>
<div class="hero"><div class="wrap"><p class="eyebrow">{e(c["eyebrow"])}</p><h1>{e(c["h1"])}</h1><p class="lead">{e(c["lead"])}</p>
<div class="ctas"><a class="btn" href="#contact">{e(c["cta"])}</a><a class="btn ghost" href="#work">{e(c["cta2"])}</a></div>
<div class="proof">{proof}</div></div></div>
<section id="work"><div class="wrap"><h2>{e(c["work_h"])}</h2><p class="note">{e(c["work_note"])}</p><div class="works">{work}</div></div></section>
<section id="prices"><div class="wrap"><h2>{e(c["prices_h"])}</h2><div class="plans">{plans}</div><p class="note">{e(c["prices_note"])}</p></div></section>
<section id="how"><div class="wrap"><h2>{e(c["steps_h"])}</h2><ol class="steps">{steps}</ol></div></section>
<section id="faq"><div class="wrap"><h2>{e(c["faq_h"])}</h2>{faq}</div></section>
<section id="contact" class="contact"><div class="wrap"><h2>{e(c["contact_h"])}</h2><p>{e(c["contact_p"])}</p>
<p>{e(c["email_l"])}: <span class="mail">{EMAIL}</span></p><a class="btn" href="{mail}">{e(c["cta"])}</a></div></section>
</main><footer><div class="wrap">© Serai Studio</div></footer></body></html>'''


def write(out: Path):
    for l in LANGS:
        d = out if l == "en" else out / l
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(render(l), encoding="utf-8")
    (out / ".nojekyll").write_text("")
