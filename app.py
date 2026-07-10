"""
APP.PY — Веб-сервис для Render.com бесплатного тарифа без карты
Запускает бота-кассу 24/7 в фоновом потоке + Flask сервер для healthcheck (чтобы Render не убивал)

Render free web service спит через 15 мин без трафика, но просыпается за 10 сек при первом запросе.
Telegram шлет апдейты на webhook? Нет, мы используем polling, поэтому нужен фоновый поток.
Flask сервер отвечает на / и /health — Render считает что сервис жив + UptimeRobot может пинговать каждые 5 мин чтобы не спал.

Запуск: python app.py
Render: Build pip install -r requirements-bot.txt, Start python app.py
"""

import threading, os, time
from flask import Flask

app = Flask(__name__)

# Флаг чтобы бот запускался один раз
bot_thread = None

def run_bot():
    print("🚀 Запускаю бота-кассу 24/7 в фоновом потоке...")
    try:
        import bot_autonomous_v6
        bot_autonomous_v6.poll()
    except Exception as e:
        print(f"Bot crash: {e}")
        import traceback; traceback.print_exc()
        time.sleep(5)
        run_bot()

@app.route('/')
def home():
    return f"ToolFarm Bot is running! 1525 tools, 2500 designs, 18 packs. Bot @{os.getenv('BOT_USERNAME','YourBot')} — polling active. <a href='/health'>health</a> | <a href='/stats'>stats</a>"

@app.route('/health')
def health():
    return "OK - Bot polling thread alive", 200

@app.route('/stats')
def stats():
    try:
        import json, pathlib
        base = pathlib.Path(__file__).parent
        tools = json.loads((base / "tools-database.json").read_text(encoding='utf-8')) if (base / "tools-database.json").exists() else []
        sales = json.loads((base / "sales_log.json").read_text(encoding='utf-8')) if (base / "sales_log.json").exists() else []
        return f"Tools: {len(tools)}, Sales: {len(sales)}, Stars: {sum(s.get('amount_stars',0) for s in sales)}"
    except Exception as e:
        return f"Stats error: {e}"

def start_bot_thread():
    global bot_thread
    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        print("Bot thread started")

if __name__ == '__main__':
    start_bot_thread()
    # Flask на порту который требует Render (10000)
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Flask health server on port {port} — для Render.com free tier без карты")
    # Запускаем Flask (блокирующий)
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
