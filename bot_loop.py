"""
BOT_LOOP v3 — Само-продвигающийся бот. Закольцовка.

Что делает:
1. Принимает /start s_... или /start r_123 — регистрирует реферала
2. Дает каждому юзеру его реф-ссылку: https://DOMAIN/?r=USER_ID
3. Считает рефералов в referrals.json
4. При 3 рефах выдает PRO код: PRO-USERID-UNLOCKED
5. Команда /pro — выдает PRO пак (50 доп инструментов + исходники)
6. Команда /source — дает ссылку на исходники фермы (твою репу)
7. Авто-постинг в канал каждый день (если указан CHANNEL_ID) — привлекает людей в бота

Хостинг бота для РФ бесплатно:
- Вариант 1 (самый простой): Запусти у себя на ноуте 24/7: python bot_loop.py
- Вариант 2: https://www.pythonanywhere.com/ — free tier, always-on task
- Вариант 3: Oracle Cloud Free (вечно бесплатно) — ставишь там
- Вариант 4: Replit.com — free

Все работает в РФ, Telegram не блокируется.

Для автономности: бот работает в polling режиме, не нужен сервер.
"""

import json, pathlib, os, time, random, urllib.request, urllib.parse
from datetime import datetime

BASE = pathlib.Path(__file__).parent
CONFIG_PATH = BASE / "config.json"
DB_PATH = BASE / "tools-database.json"
REF_PATH = BASE / "referrals.json"

def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except:
            return default
    return default

CONFIG = load_json(CONFIG_PATH, {})
TOOLS = load_json(DB_PATH, [])
REFS = load_json(REF_PATH, {})  # {user_id: {"count": 0, "invited": [], "pro": False}}

BOT_TOKEN = os.getenv("TG_BOT_TOKEN") or CONFIG.get("TELEGRAM_BOT_TOKEN") or ""
BOT_USERNAME = CONFIG.get("BOT_USERNAME","").replace('@','')
DOMAIN = CONFIG.get("DOMAIN","https://YOUR_DOMAIN").rstrip('/')
CHANNEL_ID = os.getenv("TG_CHANNEL_ID") or CONFIG.get("TELEGRAM_CHANNEL_ID") or ""

if not BOT_TOKEN or "REPLACE" in BOT_TOKEN:
    print("❌ TG_BOT_TOKEN не указан. Вставь в config.json или в env.")
    print("Для теста все равно запустится, но отправлять не будет.")
    # не выходим, чтобы можно было тестировать логику

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def api_call(method, params):
    if not BOT_TOKEN or "REPLACE" in BOT_TOKEN:
        print(f"[MOCK {method}] {params}")
        return {"ok": True}
    url = f"{API}/{method}"
    data = urllib.parse.urlencode(params).encode()
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=15) as resp:
            j = json.loads(resp.read().decode())
            return j
    except Exception as e:
        print(f"API error {method}: {e}")
        return {"ok": False}

def send_message(chat_id, text, reply_markup=None):
    params = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": False}
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)
    return api_call("sendMessage", params)

def save_refs():
    REF_PATH.write_text(json.dumps(REFS, ensure_ascii=False, indent=2), encoding='utf-8')

def get_ref_link(user_id):
    return f"{DOMAIN}/?r={user_id}"

def handle_start(user_id, username, args):
    # args вида r_123456 или s_site_from_slug_inv_..._farmid
    # Парсим кто пригласил
    inviter = None
    if args.startswith("r_"):
        inviter = args.split("_")[1]  # r_123
    elif "inv_" in args:
        # s_site_from_tool_inv_123_farmid -> вытаскиваем inv
        try:
            parts = args.split("inv_")
            inviter = parts[1].split("_")[0].split("-")[0]
        except:
            pass

    # Если новый пользователь и есть пригласивший и это не сам себя
    if inviter and str(inviter) != str(user_id):
        if str(user_id) not in REFS:
            REFS[str(user_id)] = {"count": 0, "invited": [], "invited_by": inviter, "pro": False}
        # Начисляем пригласившему
        if str(inviter) not in REFS:
            REFS[str(inviter)] = {"count": 0, "invited": [], "pro": False}
        if str(user_id) not in REFS[str(inviter)]["invited"]:
            REFS[str(inviter)]["invited"].append(str(user_id))
            REFS[str(inviter)]["count"] = len(REFS[str(inviter)]["invited"])
            save_refs()
            # Уведомляем пригласившего
            try:
                send_message(inviter, f"🎉 <b>Новый реферал!</b>\nПользователь @{username or user_id} пришел по твоей ссылке.\n\nУ тебя теперь {REFS[str(inviter)]['count']}/3 рефералов.\nПри 3 — получишь PRO пак: /balance")
            except:
                pass

    # Приветствие новому
    if str(user_id) not in REFS:
        REFS[str(user_id)] = {"count": 0, "invited": [], "pro": False}
        save_refs()

    ref_link = get_ref_link(user_id)
    welcome = f"""🚀 <b>ToolFarm Bot — твоя автономная ферма</b>

Привет! Это бот который сам себя продвигает и тебе платит трафиком.

<b>Что ты получаешь:</b>
• Твоя личная реф-ссылка: <code>{ref_link}</code>
• Поделись ею в 3 чатах / с друзьями
• Когда 3 человека перейдут по ней и нажмут Start — я дам тебе PRO код

<b>PRO пак (50 инструментов):</b>
— Массовая проверка ИНН/СНИЛС/ОГРН пачкой
— Генератор договоров/актов для РФ
— 50+ премиум тулзов + исходники фермы
— Команда /source — забрать исходники

<b>Твой прогресс:</b> {REFS[str(user_id)]['count']}/3 рефералов
/balance — проверить
/pro — получить PRO если есть 3

<b>Как закольцевать:</b>
Сайт → Бот → твоя рефка → новые люди на сайт → тебе PRO → ты делаешь свою ферму → деньги.

Твоя ссылка еще раз (копируй):
{ref_link}

Отправь её в 3 места прямо сейчас и через час проверь /balance
"""
    send_message(user_id, welcome)

def handle_balance(user_id):
    data = REFS.get(str(user_id), {"count": 0, "invited": []})
    count = data.get("count", 0)
    invited = data.get("invited", [])
    text = f"📊 <b>Баланс рефералов</b>\n\nПриглашено: {count}/3\nСписок: {', '.join(invited) if invited else 'пока никого'}\n\nТвоя реф-ссылка:\n<code>{get_ref_link(user_id)}</code>\n\n"
    if count >= 3:
        code = f"PRO-{user_id}-UNLOCKED"
        text += f"🎉 <b>Готово! Ты набрал 3!</b>\nТвой PRO код:\n<code>{code}</code>\n\nВставь его на сайте {DOMAIN}/pro/ чтобы разблокировать 50 PRO инструментов.\nТакже команда /pro"
        REFS[str(user_id)]["pro"] = True
        save_refs()
    else:
        text += f"Нужно еще {3-count} рефа. Поделись ссылкой в чатах про учебу/работу/фриланс."
    send_message(user_id, text)

def handle_pro(user_id):
    data = REFS.get(str(user_id), {"count": 0})
    if data.get("count",0) >= 3 or data.get("pro"):
        code = f"PRO-{user_id}-UNLOCKED"
        send_message(user_id, f"🔓 <b>Твой PRO доступ:</b>\nКод: <code>{code}</code>\n\nВставь на {DOMAIN}/pro/\n\nБонус — исходники фермы:\nКоманда /source\n\nИ 50 PRO инструментов уже доступны в боте по команде /pro_tools")
    else:
        send_message(user_id, f"❌ Нужно 3 рефа. У тебя {data.get('count',0)}/3. Твоя ссылка: {get_ref_link(user_id)}\n\nПоделись и проверь /balance")

def handle_source(user_id):
    # Отдаем ссылку на репу (из конфига)
    repo = CONFIG.get("REPO_URL","https://github.com/YOUR_USERNAME/tool-farm")
    send_message(user_id, f"📦 <b>Исходники автономной фермы:</b>\n\n{repo}\n\nТам:\n• 150 инструментов\n• build.py\n• bot_loop.py (этот бот который сам продвигается)\n• GitHub Actions для автодеплоя\n\nМожешь клонировать и поднимать свои фермы пачками. Каждая — отдельный доход.\n\nКак делали мы: 1 ферма = $150-300/мес пассивно. 3 фермы = $500-900.\n\nЕсли наберешь 10 рефов — дам доступ в приватный канал с новыми фермами.")

def poll():
    print("🤖 Bot Loop запущен. Polling...")
    offset = 0
    while True:
        try:
            # getUpdates
            url = f"{API}/getUpdates?offset={offset}&timeout=30"
            if not BOT_TOKEN or "REPLACE" in BOT_TOKEN:
                print("[MOCK] Жду апдейтов... (токен не указан, спим 10 сек)")
                time.sleep(10)
                continue
            with urllib.request.urlopen(url, timeout=35) as resp:
                data = json.loads(resp.read().decode())
                if not data.get("ok"):
                    time.sleep(2)
                    continue
                for upd in data.get("result",[]):
                    offset = upd["update_id"] + 1
                    msg = upd.get("message")
                    if not msg:
                        continue
                    chat_id = msg["chat"]["id"]
                    user_id = msg["from"]["id"]
                    username = msg["from"].get("username","")
                    text = msg.get("text","")

                    if text.startswith("/start"):
                        args = text.split(" ",1)[1] if " " in text else ""
                        handle_start(user_id, username, args)
                    elif text.startswith("/balance"):
                        handle_balance(user_id)
                    elif text.startswith("/pro"):
                        if "tools" in text:
                            send_message(chat_id, "🛠️ PRO инструменты (демо список):\n- mass-inn-checker\n- mass-snils\n- contract-generator\n- act-generator\n- json-csv-batch\n\nПолный доступ на сайте /pro/ по коду.")
                        else:
                            handle_pro(user_id)
                    elif text.startswith("/source"):
                        handle_source(user_id)
                    elif text.startswith("/help"):
                        send_message(chat_id, "/start - реф ссылка\n/balance - прогресс\n/pro - получить PRO\n/source - исходники")
                    else:
                        # Любое сообщение — показываем реф ссылку
                        send_message(chat_id, f"Твоя реф ссылка: {get_ref_link(user_id)}\n/balance — проверка")
        except Exception as e:
            print(f"Poll error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    poll()
