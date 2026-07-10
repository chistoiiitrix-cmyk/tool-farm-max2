"""
FEEDBACK NOTIFIER v11 — Авто-уведомление когда идея из фидбека реализована
Запускается после auto_tool_adder.py
Читает feedback.json → находит где implemented=True и not notified → шлет юзеру в ТГ: "Твой инструмент готов: /tools/{slug}/"
"""

import json, pathlib, os, urllib.request, urllib.parse

BASE = pathlib.Path(__file__).parent
FEEDBACK_PATH = BASE / "feedback.json"
CONFIG = json.loads((BASE / "config.json").read_text(encoding='utf-8')) if (BASE / "config.json").exists() else {}
BOT_TOKEN = os.getenv("TG_BOT_TOKEN") or CONFIG.get("TELEGRAM_BOT_TOKEN","")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_msg(chat_id, text):
    if not BOT_TOKEN or "REPLACE" in BOT_TOKEN:
        print(f"[MOCK NOTIFY {chat_id}] {text[:100]}")
        return
    try:
        params = {"chat_id": chat_id, "text": text, "parse_mode":"HTML"}
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(f"{API}/sendMessage", data=data)
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"Notified {chat_id}: {r.read()[:100]}")
    except Exception as e:
        print(f"Notify fail {chat_id}: {e}")

def main():
    if not FEEDBACK_PATH.exists():
        print("No feedback")
        return
    feedback = json.loads(FEEDBACK_PATH.read_text(encoding='utf-8'))
    updated=False
    for fb in feedback:
        if fb.get("implemented") and not fb.get("notified"):
            user_id = fb["user_id"]
            slug = fb.get("implemented_slug","")
            original = fb.get("text","")[:100]
            DOMAIN = CONFIG.get("DOMAIN","https://YOUR_DOMAIN")
            msg = f"""🔥 <b>Твоя идея реализована!</b>

Ты просил: <code>{original}</code>

✅ Мы сделали инструмент: {DOMAIN}/tools/{slug}/

Зацени, потести и напиши еще идей — топ идеи каждую неделю становятся новыми дропами в /drops/ и /designs/.

Твоя реф ссылка для вируса (поделись — получи PRO): {DOMAIN}/?r={user_id}

Спасибо что делаешь ферму лучше!
"""
            send_msg(user_id, msg)
            fb["notified"]=True
            updated=True
    if updated:
        FEEDBACK_PATH.write_text(json.dumps(feedback, ensure_ascii=False, indent=2), encoding='utf-8')
        print("✅ Уведомления отправлены")
    else:
        print("Нет новых реализованных идей для уведомления")

if __name__=="__main__":
    main()
