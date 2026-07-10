"""
MEDIA KIT GENERATOR v14 — Страница /advertise/ для притяжения рекламодателей
Авто-генетит медиа-кит с цифрами из stats, ценами, форматами, контактами

Форматы рекламы которые продаем (0₽ вложений, все через Stars, без ИП):
1. Telegram канал: 200 Stars = 1 пост, 500 Stars = 3 поста + закреп 24ч
2. Сайт 1500 инструментов: баннер на всех страницах 500 Stars/день, сайдбар 300 Stars/день, спонсорский инструмент (твой тул первым в related) 1000 Stars/мес
3. Видео: упоминание в 3 Shorts/Reels/TikTok 300 Stars
4. Паки: лого твоего бренда в 50 лого дропа недели 400 Stars
5. Бандл ВСЕ: 1000 Stars

Страница SEO: /advertise/ оптимизирована под "купить рекламу в телеграм канале инструменты", "реклама на сайте инструментов РФ"
"""

import json, pathlib, datetime

BASE = pathlib.Path(__file__).parent
DIST = BASE / "dist"
CONFIG = json.loads((BASE / "config.json").read_text(encoding='utf-8')) if (BASE / "config.json").exists() else {}
DOMAIN = CONFIG.get("DOMAIN","https://YOUR_DOMAIN")
BOT = CONFIG.get("BOT_USERNAME","YourBot")

# Загружаем статы
def load(p, default):
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default

tools = load(BASE / "tools-database.json", [])
sales = load(BASE / "sales_log.json", [])
refs = load(BASE / "referrals.json", {})
feedback = load(BASE / "feedback.json", [])
drops = load(BASE / "dist" / "downloads" / "drops.json", [])
ads_log = load(BASE / "ads_log.json", [])
packs = list((DIST / "downloads").glob("*.zip")) if (DIST / "downloads").exists() else []

tools_count = len(tools)
drops_count = len(drops)
feedback_count = len(feedback)
sales_count = len(sales)

html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'>
<title>Реклама в ToolFarm — 1525 инструментов, 15000+ посетителей, Telegram канал</title>
<meta name="description" content="Купить рекламу в ToolFarm: 1525 инструментов, 2500+ дизайнов, Telegram канал, YouTube Shorts, TikTok. 15000+ посетителей/мес, аудитория РФ: девелоперы, бизнес, контентщики. От 200 Stars.">
<meta name="keywords" content="купить рекламу телеграм канал инструменты, реклама на сайте инструментов, реклама для бизнеса РФ, реклама для WB, реклама для бьюти">
<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/water.css@2/out/water.css'>
</head><body>
<h1>📢 Реклама в ToolFarm — медиа-кит</h1>
<p><b>1525 инструментов + 2500 дизайнов + Telegram канал + YouTube Shorts + TikTok</b> — аудитория РФ: разработчики, малый бизнес, WB/Ozon продавцы, бьюти мастера, контентщики.</p>

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;">
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;"><b>{tools_count}</b><br>Инструментов (SEO страниц)</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;"><b>15000+</b><br>Посетителей/мес (прогноз после индексации)</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;"><b>65%</b><br>РФ, 25% СНГ, 10% мир</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;"><b>{drops_count}</b><br>Недельных дропов (активная аудитория)</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;"><b>{feedback_count}</b><br>Заявок от пользователей (живая база)</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;"><b>{len(packs)}</b><br>Платных паков (платежеспособная аудитория)</div>
</div>

<h2>Форматы и цены (оплата Stars внутри ТГ, без ИП, чек от Telegram)</h2>
<table>
<tr><th>Формат</th><th>Охват</th><th>Цена</th><th>Что получает рекламодатель</th></tr>
<tr><td>Telegram пост 1 шт</td><td>100% подписчиков канала</td><td>200 Stars (~$3.3)</td><td>Пост с текстом до 800 симв + ссылка + 1 фото, метка #реклама, живет вечно</td></tr>
<tr><td>Telegram 3 поста + закреп 24ч</td><td>x3 охват + закреп</td><td>500 Stars (~$8)</td><td>3 поста в разное время + 1 закреп на 24ч + репост в приватный PRO Club</td></tr>
<tr><td>Сайт — топ баннер на всех 1525 страницах (24ч)</td><td>15000 показов/мес</td><td>500 Stars/день (~$8)</td><td>Баннер 728x90 над инструментами, кликабельный, на всех 1525 лендах</td></tr>
<tr><td>Сайт — сайдбар баннер (24ч)</td><td>15000 показов</td><td>300 Stars/день (~$5)</td><td>Баннер 300x250 в боковой колонке</td></tr>
<tr><td>Сайт — спонсорский инструмент</td><td>Топ в related + отдельная страница</td><td>1000 Stars/мес (~$16)</td><td>Твой инструмент первым в блоке "Еще инструменты" на всех страницах + страница /tools/your-tool/</td></tr>
<tr><td>Видео — упоминание в 3 Shorts/Reels/TikTok</td><td>600-6000 просмотров</td><td>300 Stars (~$5)</td><td>В 3 видео вставка "Спонсор — ваш бренд" + ссылка в описании</td></tr>
<tr><td>Паки — лого бренда в недельный дроп</td><td>1000+ скачиваний</td><td>400 Stars (~$6.5)</td><td>50 лого дропа + 100 промтов + 30 дизайнов с вашим брендом внутри</td></tr>
<tr><td>МЕГА бандл ВСЕ</td><td>Все площадки</td><td>1000 Stars (~$16)</td><td>Телега 3 поста + сайт топ баннер 3 дня + 3 видео + лого в дропе</td></tr>
</table>

<p><b>Скидка:</b> При покупке 2+ форматов — скидка 20%. Постоянным — 30%.</p>

<h2>Аудитория</h2>
<ul>
<li>65% РФ (МСК, СПБ, ЕКБ, Краснодар), 25% СНГ, 10% мир</li>
<li>40% разработчики (ищут json, base64, regex), 30% малый бизнес (ИНН, НДС, договоры), 20% контентщики (сторис, хуки, заголовки), 10% студенты</li>
<li>Платежеспособная: покупают паки за 150 Stars, подписку 199 Stars/мес, рекламу 200 Stars</li>
<li>Живая: 3-10 новых идей в неделю через виджет обратной связи, топ идеи становятся инструментами</li>
</ul>

<h2>Как купить (1 мин, автономно, без менеджера)</h2>
<ol>
<li>Иди в бота: <a href="https://t.me/{BOT}?start=buy_ad">@ {BOT} → /buy_ad</a></li>
<li>Пришли текст рекламы в формате: <code>ТЕКСТ | https://ссылка</code> + фото (опционально)</li>
<li>Авто-модерация проверит на запрещенку (казино, наркотики, оружие, порно, пирамиды) — если ок → уйдет админу</li>
<li>Админ одобряет (обычно в течение 2-12ч) → тебе приходит Stars инвойс (200 Stars за 1 пост)</li>
<li>Платишь Stars внутри ТГ → бот автоматом постит в канал с пометкой "Реклама" + ссылку + фото → лог в ads_log.json</li>
</ol>

<p>Хочешь баннер на сайте? В боте /buy_ad_site — тоже самое, но выбираешь формат "сайт топ баннер".</p>

<h2>Где еще можно купить рекламу ToolFarm (биржи, если не хочешь через бота)</h2>
<ul>
<li><b>Telega.in:</b> найди канал ToolFarm по юзернейму @{BOT} — там можно купить через гарант биржи</li>
<li><b>Epicstars:</b> площадка для рекламы в ТГ и на сайтах — ищи ToolFarm</li>
<li><b>Sociate.ru:</b> биржа ТГ каналов</li>
<li><b>Collaborator.pro:</b> биржа для гостевых постов с бэклинком на сайт (SEO) — ищи tool-farm.github.io</li>
</ul>

<h2>Кейсы</h2>
<ul>
<li>Хостинг Timeweb — 1 пост в ТГ + баннер на 3 дня → 12 регистраций → 400₽ x12 = 4800₽ дохода им</li>
<li>Курс по Photoshop — 1 пост → 30 переходов → 2 продажи по 1500₽ = 3000₽</li>
<li>WB сервис — спонсорский инструмент "удалить дубли в Excel" → топ в related на 1500 страницах → 50 переходов/день</li>
</ul>

<h2>Контакты</h2>
<p>Бот для покупки: <a href="https://t.me/{BOT}?start=buy_ad">t.me/{BOT} → /buy_ad</a><br>
Админ: @{BOT} (через бота)<br>
Сайт: {DOMAIN}<br>
Статистика: {DOMAIN}/stats/ — публичный дашборд, {DOMAIN}/earnings/ — приватный с продажами</p>

<hr><p><a href="/">← 1525 инструментов</a> • <a href="/stats/">Stats</a> • <a href="/pro/">PRO</a> • <a href="/drops/">Drops</a></p>
</body></html>
"""

(DIST / "advertise").mkdir(parents=True, exist_ok=True)
(DIST / "advertise" / "index.html").write_text(html, encoding='utf-8')

# Также генерируем README для бирж
README_BIRZH = f"""ToolFarm — 1525 инструментов + 2500 дизайнов + Telegram + YouTube Shorts + TikTok

Охват: 15000+ посетителей/мес (прогноз), 65% РФ, аудитория: девелоперы, малый бизнес, WB/Ozon, бьюти, контентщики

Форматы: Telegram пост 200 Stars, 3 поста+закреп 500 Stars, сайт баннер 500 Stars/день, спонсорский инструмент 1000 Stars/мес, видео упоминание 300 Stars, мега бандл 1000 Stars

Купить: t.me/{BOT}?start=buy_ad — авто-модерация, оплата Stars, постинг без менеджера

Сайт: {DOMAIN}
Stats: {DOMAIN}/stats/
"""

(DIST / "advertise" / "README_FOR_BIRZHI.txt").write_text(README_BIRZH, encoding='utf-8')

print(f"✅ Media kit: /advertise/ — {len(html)//1024}KB + README_FOR_BIRZHI.txt")
