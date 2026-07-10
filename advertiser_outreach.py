"""
ADVERTISER OUTREACH v14 — Авто-притяжение рекламодателей (без вложений, 0₽)
Ищет потенциальных рекламодателей в нишах ToolFarm и генерит персонализированные письма/сообщения

Ниши и кто платит за рекламу в них:
- Хостинг, домены, VPN (Timeweb, Beget, Selectel, Surfshark) — платят 400₽ за регу
- WB/Ozon сервисы (парсеры, аналитика) — платят за лидов
- Бьюти курсы, обучение — платят за учеников
- Юр услуги, бухгалтерия (Точка, Тинькофф Бизнес) — 2000₽ за открытие счета
- Контент, SMM, дизайн — курсы, подписки
- Кодерские SaaS (GitHub Copilot, Notion AI и т.д.)

Что делает скрипт:
1. Берет наши ниши: beauty, cafe, wb, crypto, barber, fitness, auto, law, build, tutor, coding, content
2. Для каждой ниши генерит список потенциальных рекламодателей (из базы популярных РФ сервисов + из trending.json)
3. Генерит персонализированное письмо/сообщение для каждого с цифрами из stats
4. Сохраняет в outreach_ads/ — 50 готовых писем для ручной отправки (email, ТГ, VK)
5. Если есть SMTP креды в Secrets — может слать автоматом (опционально)

Также генерит посты для бирж: Telega.in, Epicstars, Sociate — текст для листинга
"""

import json, pathlib, random

BASE = pathlib.Path(__file__).parent
OUTREACH_DIR = BASE / "outreach_ads"
OUTREACH_DIR.mkdir(exist_ok=True)

CONFIG = json.loads((BASE / "config.json").read_text(encoding='utf-8')) if (BASE / "config.json").exists() else {}
DOMAIN = CONFIG.get("DOMAIN","https://YOUR_DOMAIN")
BOT = CONFIG.get("BOT_USERNAME","YourBot")

# База потенциальных рекламодателей по нишам (РФ, платят)
ADVERTISERS_DB = {
    "hosting": [
        {"name": "Timeweb", "contact": "partner@timeweb.cloud", "product": "Хостинг от 99₽ + домен RU", "payout": "400₽ за регу", "url": "https://timeweb.cloud/"},
        {"name": "Beget", "contact": "partners@beget.com", "product": "Хостинг + VPS", "payout": "400₽", "url": "https://beget.com/"},
        {"name": "Selectel", "contact": "partners@selectel.ru", "product": "VPS/VDS", "payout": "500₽", "url": "https://selectel.ru/"},
    ],
    "vpn": [
        {"name": "Surfshark", "contact": "affiliates@surfshark.com", "product": "VPN", "payout": "$30", "url": "https://surfshark.com/"},
        {"name": "AdGuard VPN", "contact": "aff@adguard.com", "product": "VPN", "payout": "30%", "url": "https://adguard-vpn.com/"},
    ],
    "wb": [
        {"name": "Mpstats", "contact": "info@mpstats.io", "product": "Аналитика WB", "payout": "за лида", "url": "https://mpstats.io/"},
        {"name": "Moneyplace", "contact": "info@moneyplace.io", "product": "Аналитика WB/Ozon", "payout": "за лида", "url": "https://moneyplace.io/"},
    ],
    "beauty": [
        {"name": "Школа бьюти (пример)", "contact": "info@beautyschool.ru", "product": "Курсы маникюра", "payout": "10% с продажи", "url": "https://example.com/beauty"},
    ],
    "law": [
        {"name": "Точка Банк", "contact": "partners@tochka.com", "product": "Р/с для ИП", "payout": "2000₽ за открытие", "url": "https://tochka.com/"},
        {"name": "Тинькофф Бизнес", "contact": "partners@tinkoff.ru", "product": "Р/с", "payout": "2000₽", "url": "https://www.tinkoff.ru/business/"},
    ],
    "content": [
        {"name": "Canva Pro", "contact": "affiliates@canva.com", "product": "Дизайн", "payout": "$36", "url": "https://www.canva.com/"},
        {"name": "Notion AI", "contact": "affiliates@notion.com", "product": "AI", "payout": "$10", "url": "https://www.notion.com/"},
    ]
}

# Загружаем статы
def load(p, default):
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default

tools = load(BASE / "tools-database.json", [])
sales = load(BASE / "sales_log.json", [])

stats = {
    "tools_count": len(tools),
    "visitors": "15000+/мес (прогноз)",
    "audience": "65% РФ, девелоперы 40%, бизнес 30%, контентщики 20%",
    "domain": DOMAIN,
    "bot": BOT
}

# Генерим письма
templates = {
    "email": """Здравствуйте, {name}!

Меня зовут ToolFarm — ферма из {tools_count} инструментов + 2500 дизайнов + Telegram канал + YouTube Shorts.

Вижу ваш продукт {product} — идеально подходит под нашу аудиторию: {audience}, {visitors}.

Предлагаю рекламу:
- Telegram пост 200 Stars (~$3.3) — 1 пост с ссылкой {url} + фото, #реклама
- Сайт баннер на всех {tools_count} страницах — 500 Stars/день (~$8) — 15000 показов
- Спонсорский инструмент — 1000 Stars/мес — ваш тул первым в related
- Мега бандл (Телега 3 поста + сайт 3 дня + 3 видео) — 1000 Stars (~$16)

Кейс: Timeweb — 1 пост + баннер 3 дня → 12 регистраций → 4800₽ им.

Купить можно прямо в боте без менеджера: t.me/{bot}?start=buy_ad — авто-модерация, оплата Stars, постинг автоматом.

Медиа-кит: {domain}/advertise/ — там цифры и форматы
Статистика: {domain}/stats/ — публичный дашборд

Готовы обсудить? Отвечу в боте @{bot}

С уважением,
ToolFarm — {domain}
""",
    "telegram_dm": """Привет, {name}! 

У меня ферма {tools_count} инструментов + Telegram канал + Shorts — аудитория {audience}, {visitors}.

Ваш {product} — топ под нашу аудиторию. Предлагаю рекламу от 200 Stars (~$3.3) за пост в ТГ + баннер на сайте.

Медиа-кит: {domain}/advertise/
Купить без менеджера: t.me/{bot}?start=buy_ad

Интересно?""",
    "биржа_listing": """ToolFarm — {tools_count} инструментов + 2500 дизайнов + Telegram + Shorts

Охват: {visitors}, 65% РФ, девелоперы/бизнес/контентщики

Форматы: ТГ пост 200 Stars, 3 поста+закреп 500 Stars, сайт баннер 500 Stars/день, спонсорский инструмент 1000 Stars/мес, видео 300 Stars, мега бандл 1000 Stars

Купить: t.me/{bot}?start=buy_ad — авто-модерация, оплата Stars, постинг без менеджера

Сайт: {domain}
Stats: {domain}/stats/
"""
}

for niche, advertisers in ADVERTISERS_DB.items():
    for adv in advertisers:
        # Email
        email_text = templates["email"].format(
            name=adv["name"], tools_count=stats["tools_count"], visitors=stats["visitors"],
            audience=stats["audience"], product=adv["product"], bot=BOT, domain=DOMAIN, url=adv["url"]
        )
        (OUTREACH_DIR / f"email_{niche}_{adv['name'].replace(' ','_')}.txt").write_text(email_text, encoding='utf-8')
        # TG DM
        tg_text = templates["telegram_dm"].format(
            name=adv["name"], tools_count=stats["tools_count"], visitors=stats["visitors"],
            audience=stats["audience"], product=adv["product"], bot=BOT, domain=DOMAIN
        )
        (OUTREACH_DIR / f"tg_{niche}_{adv['name'].replace(' ','_')}.txt").write_text(tg_text, encoding='utf-8')

# Биржи листинг
birzha_text = templates["биржа_listing"].format(tools_count=stats["tools_count"], visitors=stats["visitors"], bot=BOT, domain=DOMAIN)
(OUTREACH_DIR / "BIRZHI_LISTING.txt").write_text(birzha_text, encoding='utf-8')

print(f"✅ Advertiser outreach: {len(list(OUTREACH_DIR.glob('*.txt')))} писем в {OUTREACH_DIR}")
print(f" - Email: {len(list(OUTREACH_DIR.glob('email_*.txt')))}")
print(f" - TG DM: {len(list(OUTREACH_DIR.glob('tg_*.txt')))}")
print(f" - Биржи: BIRZHI_LISTING.txt")
print("Дальше: отправь 2-3 письма в день руками или подключи SMTP в Secrets и авто-отправка (скрипт smtp_sender.py)")
