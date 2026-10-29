"""Сборка прототипа сайта Свято-Никольского собора в Мосальске.

Контент — в content/, каркас — в templates/base.html.
Запуск: python build.py
"""

from __future__ import annotations

import html
import json
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
TEMPLATE = ROOT / "templates" / "base.html"

SITE = "https://dankkoom187.github.io/mosalsk-nikolsky"
NAME = "Свято-Никольский собор"
CITY = "Мосальск"
PHONE = "+7 (920) 881-54-59"
PHONE_HREF = "tel:+79208815459"
EMAIL = "beregovoy@mail.ru"
VK = "https://vk.com/s_nik_s"
ADDRESS = "249930, Калужская область, г. Мосальск, ул. Советская, 15А"
ADDRESS_SHORT = "Мосальск, ул. Советская, 15А"
COORDS = (54.489344, 34.981352)
MAPS = "https://yandex.ru/maps/org/sobor_nikolaya_chudotvortsa_v_mosalske/1281664434/"
ROUTE = "https://yandex.ru/maps/?rtext=~54.489344%2C34.981352&rtt=auto"
YEAR = 2026

MONTHS_GENITIVE = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}


def d(iso: str) -> date:
    return date.fromisoformat(iso)


def date_label(iso: str) -> str:
    dt = d(iso)
    return f"{dt.day} {MONTHS_GENITIVE[dt.month]}"


# Демонстрационное расписание: сентябрь 2026.
# Источник: https://vk.com/wall-117411861_4104
# На боевом сайте данные должны обновляться из CMS/API, а не жить в build.py.
SCHEDULE = [
    {"date": "2026-09-01", "weekday": "вторник", "feast": "Донской иконы Божией Матери", "service": "Молебен с акафистом", "time": "10:00", "place": "Собор"},
    {"date": "2026-09-03", "weekday": "четверг", "feast": "", "service": "Молебен с акафистом свт. Николаю", "time": "10:00", "place": "Собор"},
    {"date": "2026-09-04", "weekday": "пятница", "feast": "Грузинской иконы Божией Матери. Престольный праздник", "service": "Божественная литургия", "time": "09:00", "place": "Собор"},
    {"date": "2026-09-05", "weekday": "суббота", "feast": "", "service": "Панихида", "time": "10:00", "place": "Собор"},
    {"date": "2026-09-05", "weekday": "суббота", "feast": "", "service": "Всенощное бдение", "time": "17:00", "place": "Собор"},
    {"date": "2026-09-06", "weekday": "воскресенье", "feast": "Неделя 14-я по Пятидесятнице. Собор Московских святых", "service": "Божественная литургия, молебен", "time": "09:00", "place": "Собор"},
    {"date": "2026-09-08", "weekday": "вторник", "feast": "Владимирской иконы Пресвятой Богородицы, мчч. Адриана и Наталии", "service": "Божественная литургия", "time": "09:00", "place": "Собор"},
    {"date": "2026-09-10", "weekday": "четверг", "feast": "", "service": "Молебен с акафистом свт. Николаю", "time": "10:00", "place": "Собор"},
    {"date": "2026-09-10", "weekday": "четверг", "feast": "", "service": "Всенощное бдение", "time": "17:00", "place": "Собор"},
    {"date": "2026-09-11", "weekday": "пятница", "feast": "Усекновение главы Пророка, Предтечи и Крестителя Господня Иоанна", "service": "Божественная литургия", "time": "09:00", "place": "Собор"},
    {"date": "2026-09-12", "weekday": "суббота", "feast": "Блгв. кн. Даниила Московского, блгв. кн. Александра Невского", "service": "Панихида", "time": "10:00", "place": "Собор"},
    {"date": "2026-09-12", "weekday": "суббота", "feast": "", "service": "Молебен", "time": "10:30", "place": "Собор"},
    {"date": "2026-09-12", "weekday": "суббота", "feast": "", "service": "Всенощное бдение", "time": "17:00", "place": "Собор"},
    {"date": "2026-09-13", "weekday": "воскресенье", "feast": "Неделя 15-я по Пятидесятнице. Перенесение мощей блгв. кн. Петра и кн. Февронии, Муромских чудотворцев", "service": "Божественная литургия, молебен", "time": "09:00", "place": "Собор"},
    {"date": "2026-09-15", "weekday": "вторник", "feast": "Калужской иконы Божией Матери. Прпп. Антония и Феодосия Киево-Печерских", "service": "Божественная литургия", "time": "09:00", "place": "Собор"},
    {"date": "2026-09-17", "weekday": "четверг", "feast": "Иконы Божией Матери «Неопалимая Купина»", "service": "Молебен с акафистом", "time": "10:00", "place": "Собор"},
    {"date": "2026-09-19", "weekday": "суббота", "feast": "Воспоминание чуда Архистратига Михаила, бывшего в Хонех", "service": "Панихида", "time": "10:00", "place": "Собор"},
    {"date": "2026-09-19", "weekday": "суббота", "feast": "", "service": "Молебен", "time": "10:00", "place": "Собор"},
    {"date": "2026-09-19", "weekday": "суббота", "feast": "", "service": "Всенощное бдение", "time": "17:00", "place": "Собор"},
    {"date": "2026-09-20", "weekday": "воскресенье", "feast": "Неделя 16-я по Пятидесятнице. Прп. Макария Оптинского", "service": "Божественная литургия, молебен", "time": "09:00", "place": "Собор"},
    {"date": "2026-09-20", "weekday": "воскресенье", "feast": "", "service": "Всенощное бдение", "time": "17:00", "place": "Собор"},
    {"date": "2026-09-21", "weekday": "понедельник", "feast": "Рождество Пресвятой Владычицы нашей Богородицы и Приснодевы Марии", "service": "Божественная литургия", "time": "09:00", "place": "Собор"},
    {"date": "2026-09-24", "weekday": "четверг", "feast": "", "service": "Молебен с акафистом свт. Николаю", "time": "10:00", "place": "Собор"},
    {"date": "2026-09-26", "weekday": "суббота", "feast": "Память обновления храма Воскресения Христова в Иерусалиме (Воскресение словущее)", "service": "Божественная литургия пасхальным чином, крестный ход", "time": "09:00", "place": "Собор"},
    {"date": "2026-09-26", "weekday": "суббота", "feast": "", "service": "Всенощное бдение с выносом Креста Господня", "time": "17:00", "place": "Собор"},
    {"date": "2026-09-27", "weekday": "воскресенье", "feast": "Неделя 17-я по Пятидесятнице. Воздвижение Честного и Животворящего Креста Господня. Свт. Иоанна Златоуста", "service": "Божественная литургия, молебен", "time": "09:00", "place": "Собор"},
    {"date": "2026-09-27", "weekday": "воскресенье", "feast": "", "service": "Всенощное бдение", "time": "17:00", "place": "Собор"},
    {"date": "2026-09-30", "weekday": "среда", "feast": "Мцц. Веры, Надежды, Любови и матери их Софии", "service": "Молебен с акафистом", "time": "10:00", "place": "Собор"},
]

for item in SCHEDULE:
    item["date_label"] = date_label(item["date"])
    item["feast"] = item["feast"] or "—"
    item.setdefault("note", "")


def schedule_table() -> str:
    rows = []
    for item in SCHEDULE:
        rows.append(
            "<tr data-date=\"{date}\">"
            "<td data-label=\"Дата\"><span class=\"schedule-date-block\">"
            "<span class=\"schedule-date\">{date_label}</span>"
            "<span class=\"schedule-weekday\">{weekday}</span></span></td>"
            "<td data-label=\"Праздник\">{feast}</td>"
            "<td data-label=\"Богослужение\">{service}</td>"
            "<td data-label=\"Время\"><strong>{time}</strong></td>"
            "<td data-label=\"Место\">{place}</td>"
            "</tr>".format(**item)
        )
    return "\n".join(rows)


def nav_html(active: str) -> str:
    items = [
        ("raspisanie.html", "Расписание", "schedule"),
        ("hram.html", "О соборе", "about"),
        ("hram.html#svyatyni", "Святыни", "shrines"),
        ("kontakty.html", "Контакты", "contacts"),
    ]
    out = []
    for href, label, key in items:
        cls = "nav__link is-active" if key == active else "nav__link"
        aria = ' aria-current="page"' if key == active else ""
        out.append(f'<a class="{cls}" href="{href}"{aria}>{label}</a>')
    return "\n".join(out)


def mobile_nav_html(active: str) -> str:
    items = [
        ("index.html", "Главная", "home"),
        ("raspisanie.html", "Расписание", "schedule"),
        ("hram.html", "О соборе", "about"),
        ("hram.html#svyatyni", "Святыни", "shrines"),
        ("kontakty.html", "Контакты", "contacts"),
    ]
    out = []
    for href, label, key in items:
        cls = "mobile-menu__link is-active" if key == active else "mobile-menu__link"
        aria = ' aria-current="page"' if key == active else ""
        out.append(f'<a class="{cls}" href="{href}"{aria}>{label}</a>')
    return "\n".join(out)


def church_schema() -> dict:
    return {
        "@type": ["Church", "Organization"],
        "name": "Свято-Никольский собор г. Мосальска",
        "alternateName": "Храм святителя Николая Чудотворца",
        "description": "Действующий православный собор в центре Мосальска. Памятник архитектуры классицизма, воссозданный в 1999–2001 годах.",
        "url": SITE + "/",
        "image": SITE + "/assets/img/og.jpg",
        "telephone": PHONE,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "ул. Советская, 15А",
            "addressLocality": CITY,
            "addressRegion": "Калужская область",
            "postalCode": "249930",
            "addressCountry": "RU",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": COORDS[0], "longitude": COORDS[1]},
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "opens": "09:00",
                "closes": "13:00",
            }
        ],
        "sameAs": [VK],
    }


def page_schema(page: dict, breadcrumbs: list[tuple[str, str]]) -> str:
    graph = [
        church_schema(),
        {
            "@type": "WebPage",
            "name": page["title"],
            "description": page["description"],
            "url": SITE + page["canonical"],
            "inLanguage": "ru-RU",
            "isPartOf": {"@type": "WebSite", "name": NAME, "url": SITE + "/"},
        },
    ]
    if breadcrumbs:
        graph.append(
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + url}
                    for i, (name, url) in enumerate(breadcrumbs)
                ],
            }
        )
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


PAGES = [
    {
        "slug": "index",
        "file": "index.html",
        "title": "Свято-Никольский собор в Мосальске — расписание богослужений",
        "description": "Сайт Свято-Никольского собора г. Мосальска: расписание богослужений, история, святыни, воскресная школа и контакты. Адрес — Советская, 15А.",
        "canonical": "/",
        "nav": "home",
        "og_title": "Свято-Никольский собор в Мосальске",
        "og_alt": "Свято-Никольский собор в Мосальске: жёлтое здание с колоннами и высокой колокольней",
        "breadcrumbs": [],
    },
    {
        "slug": "raspisanie",
        "file": "raspisanie.html",
        "title": "Расписание богослужений — Свято-Никольский собор, Мосальск",
        "description": "Расписание богослужений в Свято-Никольском соборе Мосальска: Литургия, всенощное бдение, молебны, панихиды. Демонстрационный месяц — сентябрь 2026.",
        "canonical": "/raspisanie.html",
        "nav": "schedule",
        "og_title": "Расписание богослужений — Свято-Никольский собор",
        "og_alt": "Расписание богослужений Свято-Никольского собора в Мосальске",
        "breadcrumbs": [("Главная", "/"), ("Расписание", "/raspisanie.html")],
    },
    {
        "slug": "hram",
        "file": "hram.html",
        "title": "О Свято-Никольском соборе в Мосальске — история и святыни",
        "description": "Свято-Никольский собор в Мосальске: три придела, история 1806–1818 годов, восстановление 1999–2001 годов, святыни, духовенство и жизнь прихода.",
        "canonical": "/hram.html",
        "nav": "about",
        "og_title": "О Свято-Никольском соборе в Мосальске",
        "og_alt": "Свято-Никольский собор в Мосальске, вид с площади",
        "breadcrumbs": [("Главная", "/"), ("О соборе", "/hram.html")],
    },
    {
        "slug": "kontakty",
        "file": "kontakty.html",
        "title": "Контакты и как добраться — Свято-Никольский собор, Мосальск",
        "description": "Контакты Свято-Никольского собора в Мосальске: адрес — Советская, 15А, телефон, часы работы, маршрут на карте, парковка и как добраться до храма.",
        "canonical": "/kontakty.html",
        "nav": "contacts",
        "og_title": "Контакты и как добраться — Свято-Никольский собор",
        "og_alt": "Свято-Никольский собор в Мосальске, адрес и маршрут",
        "breadcrumbs": [("Главная", "/"), ("Контакты", "/kontakty.html")],
    },
    {
        "slug": "404",
        "file": "404.html",
        "title": "Страница не найдена — Свято-Никольский собор, Мосальск",
        "description": "Страница не найдена. Вернитесь на главную или откройте расписание богослужений.",
        "canonical": "/404.html",
        "nav": "",
        "og_title": "Страница не найдена",
        "og_alt": "Свято-Никольский собор в Мосальске",
        "breadcrumbs": [],
        "robots": "noindex, nofollow",
    },
]


def render() -> None:
    template = TEMPLATE.read_text(encoding="utf-8")
    schedule_json = json.dumps(SCHEDULE, ensure_ascii=False, indent=2)
    table = schedule_table()

    for page in PAGES:
        content = (CONTENT / f"{page['slug']}.html").read_text(encoding="utf-8")
        content = content.replace("{{SCHEDULE_TABLE}}", table)
        content = content.replace("{{SCHEDULE_MONTH}}", "сентябрь 2026")
        content = content.replace("{{YEAR}}", str(YEAR))

        values = {
            "{{TITLE}}": html.escape(page["title"]),
            "{{DESCRIPTION}}": html.escape(page["description"]),
            "{{ROBOTS}}": page.get("robots", "index, follow"),
            "{{CANONICAL}}": SITE + page["canonical"],
            "{{OG_TITLE}}": html.escape(page.get("og_title", page["title"])),
            "{{OG_DESCRIPTION}}": html.escape(page["description"]),
            "{{OG_IMAGE}}": SITE + "/assets/img/og.jpg",
            "{{OG_IMAGE_ALT}}": html.escape(page.get("og_alt", "")),
            "{{SCHEMA}}": page_schema(page, page["breadcrumbs"]),
            "{{NAV}}": nav_html(page["nav"]),
            "{{MOBILE_NAV}}": mobile_nav_html(page["nav"]),
            "{{BODY}}": content,
            "{{PHONE}}": PHONE,
            "{{PHONE_HREF}}": PHONE_HREF,
            "{{EMAIL}}": EMAIL,
            "{{ADDRESS}}": ADDRESS,
            "{{ADDRESS_SHORT}}": ADDRESS_SHORT,
            "{{VK}}": VK,
            "{{MAPS}}": MAPS,
            "{{ROUTE}}": ROUTE,
            "{{YEAR}}": str(YEAR),
            "{{SCHEDULE_JSON}}": schedule_json,
        }
        result = template
        for key, value in values.items():
            result = result.replace(key, value)
        (ROOT / page["file"]).write_text(result, encoding="utf-8")
        print("written", page["file"])

    # sitemap
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in PAGES:
        if page["slug"] == "404":
            continue
        sitemap.append(
            f"  <url><loc>{SITE}{page['canonical']}</loc><changefreq>monthly</changefreq><priority>{'1.0' if page['slug'] == 'index' else '0.8'}</priority></url>"
        )
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: " + SITE + "/sitemap.xml\n",
        encoding="utf-8",
    )

    build_ics()


def ics_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def build_ics() -> None:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Mosalsk Nikolsky Sobor//Prototype//RU",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{ics_escape('Свято-Никольский собор — сентябрь 2026')}",
        "X-WR-TIMEZONE:Europe/Moscow",
    ]
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for i, item in enumerate(SCHEDULE, 1):
        dt = datetime.combine(d(item["date"]), time.fromisoformat(item["time"]), tzinfo=timezone(timedelta(hours=3)))
        start = dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        end = (dt + timedelta(hours=2)).astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        summary = item["service"] + (" — " + item["feast"] if item["feast"] != "—" else "")
        description = item["feast"] + ("\n" + item["note"] if item["note"] else "")
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{item['date']}-{item['time'].replace(':', '')}-{i}@mosalsk-nikolsky",
                f"DTSTAMP:{now}",
                f"DTSTART:{start}",
                f"DTEND:{end}",
                f"SUMMARY:{ics_escape(summary)}",
                f"DESCRIPTION:{ics_escape(description)}",
                f"LOCATION:{ics_escape('Свято-Никольский собор, Мосальск, ул. Советская, 15А')}",
                "END:VEVENT",
            ]
        )
    lines.append("END:VCALENDAR")
    (ROOT / "schedule.ics").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    render()
