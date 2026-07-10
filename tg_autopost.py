"""
TG_AUTOPOST - полностью автономный трафик и деньги для РФ
1. Постит твои инструменты в ТГ-канал (бесплатно, без бана как в Reddit)
2. Парсит халяву и кидает с партнеркой Admitad

Работает на GitHub Actions 1 раз в день. Нужен только TELEGRAM_BOT_TOKEN.
Выплаты Admitad -> на карту МИР / СБП, работает в РФ.

Как получить токен (2 мин, ты должен сделать это сам):
1. В ТГ найди @BotFather -> /newbot -> имя ToolFarmBot -> получи токен вида 123456:AAH...
2. Создай канал, например toolfarm_tools
3. Добавь бота в админы канала
4. Напиши в канал что-то, перешли сообщение боту @getidsbot чтобы узнать ID канала вида -1001234567890
5. Вставь токен и ID в config.json или в GitHub Secrets
"""
import json, random, pathlib, os
import urllib.request
import urllib.parse

BASE = pathlib.Path(__file__).parent
DB = json.loads((BASE / "tools-database.json").read_text(encoding='utf-8'))
CONFIG = json.loads((BASE / "config.json").read_text(encoding='utf-8'))

BOT_TOKEN = os.getenv("TG_BOT_TOKEN") or CONFIG.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TG_CHANNEL_ID") or CONFIG.get("TELEGRAM_CHANNEL_ID")
DOMAIN = CONFIG.get("DOMAIN","https://YOUR_DOMAIN")

def send_tg(text):
    if not BOT_TOKEN or not CHANNEL_ID or "REPLACE" in BOT_TOKEN:
        print("TG не настроен, пропуск. Текст который был бы отправлен:\n", text[:500])
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": False}).encode()
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req) as resp:
            print("TG sent:", resp.read().decode()[:200])
            return True
    except Exception as e:
        print("TG error:", e)
        return False

def post_random_tool():
    tool = random.choice(DB)
    texts = [
        f"🛠️ <b>{tool['h1']}</b>\n\n{tool['desc']}\nРаботает офлайн, без регистрации, бесплатно и в РФ без VPN.\n\n👉 Попробовать: {DOMAIN}/tools/{tool['slug']}/\n\n#инструменты #лайфхак #полезное",
        f"Нашел тулзу которая экономит 10 мин в день:\n<b>{tool['h1']}</b> — {tool['desc'].lower()}\n\nСсылка: {DOMAIN}/tools/{tool['slug']}/ — не сохраняет данные, все в браузере.\n\nСохрани, пригодится для учебы/работы.",
        f"⚡ Быстрый инструмент дня:\n{tool['h1']}\n\n{DOMAIN}/tools/{tool['slug']}/ — 1 клик и готово. Без рекламы на весь экран.\n\nУ нас уже {len(DB)} таких."
    ]
    msg = random.choice(texts)
    send_tg(msg)

def post_affiliate_deal():
    # Демо-парсинг халявы. Можешь заменить на реальный парсинг Admitad API
    deals = [
        f"🔥 <b>Хостинг для такого же сайта от 99₽</b>\nTimeweb — оплачивается СБП, домен .RU в подарок, работает в РФ.\n👉 {CONFIG['ADMITAD'].get('HOSTING','https://timeweb.cloud/')} \nСайт как у нас соберешь за вечер.",
        f"💳 <b>Расчетный счет для самозанятого 0₽</b>\nТочка/Тинькофф — открытие 0₽, вывод на карту. Бонус 2000₽ по партнерке.\n",
        f"📚 <b>Бесплатный курс сегодня</b>\nНа Udemy раздают курс по Python/Excel. Ищи по промо FREE. Ссылка в закрепе канала."
    ]
    send_tg(random.choice(deals))

if __name__ == "__main__":
    # 70% инструмент, 30% партнерка
    if random.random() < 0.7:
        post_random_tool()
    else:
        post_affiliate_deal()
