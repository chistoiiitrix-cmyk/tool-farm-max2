import json, pathlib
BASE = pathlib.Path(__file__).parent
DIST = BASE / "dist"
CONFIG = json.loads((BASE / "config.json").read_text(encoding='utf-8')) if (BASE / "config.json").exists() else {}
DOMAIN = CONFIG.get("DOMAIN","https://YOUR_DOMAIN")
BOT = CONFIG.get("BOT_USERNAME","YourBot")

drops_path = DIST / "downloads" / "drops.json"
if not drops_path.exists():
    print("No drops.json")
    exit(0)

drops = json.loads(drops_path.read_text(encoding='utf-8'))

html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>Еженедельные дропы — свежие паки каждую неделю</title>
<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/water.css@2/out/water.css'></head>
<body>
<h1>🔥 Еженедельные дропы — авто-контент каждую неделю</h1>
<p>Каждую неделю новая ниша: 50 лого + 100 промтов + 20 шаблонов. Подписка PRO Club 199 Stars/мес = все дропы бесплатно. Отдельный дроп 79 Stars.</p>
<p><a href="https://t.me/{BOT}?start=drops">👉 Получить дроп в боте</a> • <a href="/">← 750 инструментов</a> • <a href="/pro/">PRO</a></p>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;">
"""

for d in drops:
    html += f"""
    <div style="border:1px solid #e5e7eb;padding:14px;border-radius:12px;background:#fff;">
      <b>{d['week_id']} — {d['niche']['name']}</b><br>
      <small>{d['date']} — {d['description']}</small><br><br>
      <ul>
        <li><a href="/downloads/{d['files']['logos']}">50 лого</a></li>
        <li><a href="/downloads/{d['files']['prompts']}">100 промтов</a></li>
        <li><a href="/downloads/{d['files']['templates']}">20 шаблонов</a></li>
      </ul>
      <a href="/downloads/{d['files']['bundle']}" style="background:#111;color:#fff;padding:6px 12px;border-radius:8px;text-decoration:none;">⬇️ Бандл {d['price_stars_bundle']} Stars</a>
      <a href="https://t.me/{BOT}?start=buy_drop_{d['week_id']}" style="background:#f59e0b;color:#000;padding:6px 12px;border-radius:8px;text-decoration:none;margin-left:6px;">💳 Купить 79 Stars</a>
    </div>
    """

html += "</div><hr><p>Подписка PRO Club: /buy_sub в боте — все дропы бесплатно + 1 новый пак в день в приватный канал.</p></body></html>"

(DIST / "drops").mkdir(parents=True, exist_ok=True)
(DIST / "drops" / "index.html").write_text(html, encoding='utf-8')
print(f"✅ Drops page: {len(drops)} дропов -> /drops/")
