import pathlib, json
BASE = pathlib.Path(__file__).parent
DIST = BASE / "dist"
CONFIG = json.loads((BASE / "config.json").read_text(encoding='utf-8')) if (BASE / "config.json").exists() else {}
BOT = CONFIG.get("BOT_USERNAME","YourBot")
DOMAIN = CONFIG.get("DOMAIN","https://YOUR_DOMAIN")

design_dir = DIST / "downloads" / "designs"
packs = list(design_dir.glob("*.zip")) if design_dir.exists() else []
downloads = list((DIST / "downloads").glob("*.zip"))

# Считаем все паки
all_packs = []
for p in DIST.glob("**/*.zip"):
    if "weekly" in str(p): continue
    rel = p.relative_to(DIST)
    all_packs.append({"file": str(rel), "name": p.name, "size_kb": p.stat().st_size//1024})

html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>Дизайны и оформления — 2500+ шаблонов — ПУШКА</title>
<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/water.css@2/out/water.css'></head>
<body>
<h1>🎨 ПУШКА — Дизайны и оформления — 2500+ файлов</h1>
<p>Авто-сгенерировано кодом, 10 ниш: beauty, cafe, crypto, WB, barber, fitness, auto, law, build, tutor. Продается паками по 79-299 Stars, все входит в PRO Club 199 Stars/мес.</p>
<p><a href="https://t.me/{BOT}?start=designs">👉 Забрать дизайны в боте</a> • <a href="/pro/">PRO</a> • <a href="/drops/">Дропы</a> • <a href="/">1500 инструментов</a></p>

<h2>💥 Мега-бандл ПУШКА — все в одном (42MB)</h2>
<p><a href="/downloads/PUCHKA-MEGA-BUNDLE.zip" style="background:#111;color:#fff;padding:12px 20px;border-radius:10px;text-decoration:none;font-weight:800;">⬇️ Скачать PUCHKA MEGA BUNDLE (42MB)</a> — 2500+ дизайнов + 1000 лого + 5000 промтов + 200 шаблонов. Цена: 399 Stars в боте /buy</p>

<h2>📦 Паки оформлений</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px;">
"""

for pack in sorted(all_packs, key=lambda x: x["size_kb"], reverse=True)[:20]:
    html += f"""
    <div style="border:1px solid #eee;padding:12px;border-radius:12px;">
      <b>{pack['name']}</b><br><small>{pack['size_kb']}KB — /{pack['file']}</small><br>
      <a href="/{pack['file']}" style="background:#f59e0b;color:#000;padding:6px 10px;border-radius:8px;text-decoration:none;">⬇️ Скачать</a>
      <a href="https://t.me/{BOT}?start=buy_design_{pack['name']}" style="background:#111;color:#fff;padding:6px 10px;border-radius:8px;text-decoration:none;margin-left:6px;">💳 Купить 99 Stars</a>
    </div>
    """

html += """</div>
<hr>
<h2>Как это продается автономно?</h2>
<ul>
<li>PRO Club 199 Stars/мес = все дизайны + все недельные дропы бесплатно + 1 новый дизайн-пак каждый день в приватный канал</li>
<li>Отдельный пак = 79-149 Stars (бот /buy_design_...)</li>
<li>Мега-бандл ПУШКА 42MB = 399 Stars (все что есть)</li>
<li>Бот сам доставляет zip за 5 сек после оплаты Stars</li>
</ul>
<p>Генерация: design_factory.py + content_factory.py + weekly_drop_factory.py — все автоматом каждый понедельник через GitHub Actions. Ниши меняются, контент бесконечный.</p>
</body></html>
"""

(DIST / "designs").mkdir(exist_ok=True)
(DIST / "designs" / "index.html").write_text(html, encoding='utf-8')
print(f"✅ Designs page: {len(all_packs)} паков -> /designs/")
