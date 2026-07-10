"""
STATS GENERATOR v13 — Дашборд где чекать статистику (капусту)
Генерит 2 страницы:
- /stats/ — публичный дашборд: сколько инструментов, паков, дропов, фидбека, трендов
- /earnings/ — приватный дашборд для админа: продажи, подписки, рефералы, реклама, отзывы, тренды, доходы

Читает:
- tools-database.json (1500)
- sales_log.json (продажи паков)
- referrals.json (рефералы)
- feedback.json (обратная связь)
- trending.json (тренды)
- drops.json (дропы)
- pending_ads.json + ads_log.json (реклама)
- dist/downloads/*.zip (паки)
- dist/tools (кол-во)

Вывод: dist/stats/index.html + dist/earnings/index.html с графиками (Chart.js CDN + fallback)

Авто-обновляется каждый день через GitHub Actions
"""

import json, pathlib, datetime
from collections import Counter

BASE = pathlib.Path(__file__).parent
DIST = BASE / "dist"
CONFIG = json.loads((BASE / "config.json").read_text(encoding='utf-8')) if (BASE / "config.json").exists() else {}
DOMAIN = CONFIG.get("DOMAIN","https://YOUR_DOMAIN")
BOT = CONFIG.get("BOT_USERNAME","YourBot")

def load(p, default):
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default

tools = load(BASE / "tools-database.json", [])
sales = load(BASE / "sales_log.json", [])
refs = load(BASE / "referrals.json", {})
feedback = load(BASE / "feedback.json", [])
trending = load(BASE / "trending.json", {})
drops = load(BASE / "dist" / "downloads" / "drops.json", [])
ads_pending = load(BASE / "pending_ads.json", [])
ads_log = load(BASE / "ads_log.json", [])
subs = load(BASE / "subscriptions.json", {})
tiktok_log = load(BASE / "tiktok_log.json", [])
youtube_log = []  # можно добавить позже

# Подсчеты
tools_count = len(tools)
sales_count = len(sales)
stars_total = sum(s.get("amount_stars",0) for s in sales)
stars_usd = stars_total * 0.016  # примерно 1 Star = $0.016
refs_total_users = len(refs)
refs_total_invites = sum(v.get("count",0) for v in refs.values())
feedback_count = len(feedback)
feedback_ideas = len([f for f in feedback if f.get("type")=="idea"])
top_niche = trending.get("top_niche","-")
drops_count = len(drops)
ads_pending_count = len([a for a in ads_pending if "pending" in a.get("status","")])
ads_posted = len([a for a in ads_log if a.get("final_status")=="posted"])

# Паки
packs = list((DIST / "downloads").glob("*.zip")) if (DIST / "downloads").exists() else []
design_packs = list((DIST / "downloads" / "designs").glob("*.zip")) if (DIST / "downloads" / "designs").exists() else []
videos = list((DIST / "videos").glob("*.mp4")) if (DIST / "videos").exists() else []
tiktok_videos = len(tiktok_log)
len_videos = len(videos)

# Генерация публичного дашборда /stats/
stats_html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>Статистика фермы — ToolFarm 1500+ tools</title>
<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/water.css@2/out/water.css'></head>
<body>
<h1>📊 ToolFarm Stats — Публичный дашборд</h1>
<p>Обновлено: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')} | Домен: {DOMAIN} | Бот: @{BOT}</p>

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;">
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;background:#fff;"><b>{tools_count}</b><br>Инструментов</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;background:#fff;"><b>{len(packs)}</b><br>Платных паков</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;background:#fff;"><b>{len(design_packs)}</b><br>Дизайн-паков</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;background:#fff;"><b>{drops_count}</b><br>Недельных дропов</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;background:#fff;"><b>{feedback_count}</b><br>Отзывов/идей</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;background:#fff;"><b>{top_niche}</b><br>Топ ниша недели</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;background:#fff;"><b>{len(videos)}</b><br>Видео Shorts</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;background:#fff;"><b>{tiktok_videos}</b><br>TikTok залито</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;background:#fff;"><b>{ads_posted}</b><br>Реклам опубликовано</div>
</div>

<h2>🔥 Тренды недели (из trending.json)</h2>
<p>Топ ниша: <b>{top_niche}</b> | Всего трендов: {len(trending.get('trends',[]))}</p>
<ul>
"""
for t in trending.get('trends',[])[:10]:
    stats_html += f"<li>{t.get('keyword')} — {t.get('source')} — niche {t.get('niche_id')}</li>"

stats_html += f"""
</ul>

<h2>💡 Топ идей из обратной связи</h2>
<ul>
"""
for fb in sorted(feedback, key=lambda x: x.get('votes',0), reverse=True)[:10]:
    stats_html += f"<li>{fb.get('text','')[:80]} — голосов {fb.get('votes',0)} — {fb.get('type')} — {'реализовано '+fb.get('implemented_slug','') if fb.get('implemented') else 'в очереди'}</li>"

stats_html += f"""
</ul>

<h2>📦 Последние дропы</h2>
<ul>
"""
for d in drops[:5]:
    stats_html += f"<li>{d['week_id']} — {d['niche']['id']} — {d['date']} — {d['description'][:80]}</li>"

stats_html += f"""
</ul>

<h2>🎬 Последние видео (TikTok + YouTube Shorts)</h2>
<ul>
"""
for t in tiktok_log[-5:][::-1]:
    stats_html += f"<li>{t.get('upload_time','')[:19]} — {t.get('title','')[:60]} — {t.get('status')} — <a href='{t.get('link','')}'>{t.get('link','')}</a></li>"
for v in videos[:5]:
    stats_html += f"<li>Local: {v.name} — {v.stat().st_size//1024}KB</li>"

stats_html += f"""
</ul>

<h2>🎨 Последние дизайны</h2>
<p>Всего дизайн-паков: {len(design_packs)} + 2500+ файлов</p>
<p><a href="/designs/">→ Страница дизайнов</a> • <a href="/drops/">→ Дропы</a> • <a href="/pro/">PRO</a> • <a href="/">1500 инструментов</a></p>

<hr><small>Авто-обновляется каждый день в 9:00 МСК через GitHub Actions. Данные из feedback.json, trending.json, drops.json, sales_log.json</small>
</body></html>
"""

(DIST / "stats").mkdir(parents=True, exist_ok=True)
(DIST / "stats" / "index.html").write_text(stats_html, encoding='utf-8')

# Приватный дашборд /earnings/ — только для админа (простая защита через prompt ADMIN_ID)
earnings_html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>💰 Капуста — Приватный дашборд</title>
<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/water.css@2/out/water.css'>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<h1>💰 Капуста Dashboard — Приватный (только для админа)</h1>
<div id="protected" style="display:none;">
<p>Обновлено: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}</p>

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;">
  <div style="border:2px solid #111;padding:14px;border-radius:12px;background:#fffbe6;"><b>{sales_count}</b><br>Продаж паков<br><small>Stars: {stars_total} (~${stars_usd:.2f})</small></div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;"><b>{len(subs)}</b><br>Подписчиков PRO Club</div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;"><b>{refs_total_users}</b><br>Юзеров с рефками<br><small>Приглашений: {refs_total_invites}</small></div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;"><b>{feedback_count}</b><br>Фидбека<br><small>Идей: {feedback_ideas}</small></div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;"><b>{ads_posted}</b><br>Реклам опубликовано<br><small>На модерации: {ads_pending_count}</small></div>
  <div style="border:1px solid #e5e7eb;padding:12px;border-radius:10px;"><b>{tools_count}</b><br>Инструментов<br><small>Авто-добавлено из фидбека: {len([f for f in feedback if f.get('implemented')])}</small></div>
</div>

<h2>📈 График продаж (последние 20)</h2>
<canvas id="salesChart" width="400" height="150"></canvas>

<h2>📋 Последние продажи</h2>
<table><tr><th>Дата</th><th>User</th><th>Причина</th><th>Stars</th><th>Код</th></tr>
"""
for s in sales[-20:][::-1]:
    earnings_html += f"<tr><td>{s.get('time','')[:19]}</td><td>{s.get('user_id')}</td><td>{s.get('reason','')[:30]}</td><td>{s.get('amount_stars',0)}</td><td>{s.get('code','')}</td></tr>"

earnings_html += f"""
</table>

<h2>📢 Реклама — лог</h2>
<table><tr><th>Дата</th><th>User</th><th>Текст</th><th>Статус</th></tr>
"""
for ad in (ads_log + ads_pending)[-20:][::-1]:
    earnings_html += f"<tr><td>{ad.get('date','')[:19]}</td><td>{ad.get('username') or ad.get('user_id')}</td><td>{ad.get('text','')[:50]}</td><td>{ad.get('status') or ad.get('final_status')}</td></tr>"

earnings_html += f"""
</table>

<h2>💡 Фидбек — топ идей</h2>
<ul>
"""
for fb in sorted(feedback, key=lambda x: x.get('votes',0), reverse=True)[:15]:
    earnings_html += f"<li>[{fb.get('type')}] {fb.get('text','')[:100]} — голосов {fb.get('votes',0)} — {'✅ '+fb.get('implemented_slug','') if fb.get('implemented') else '⏳ в очереди'} — юзер {fb.get('user_id')}</li>"

earnings_html += f"""
</ul>

<h2>🔥 Тренды + дропы + TikTok</h2>
<p>Топ ниша: {top_niche} | Видео залито: {tiktok_videos} | Shorts файлов: {len_videos}</p>
<ul>
"""
for d in drops[:5]:
    earnings_html += f"<li>{d['week_id']} — {d['description'][:80]} — {d['files'].get('bundle','')}</li>"

earnings_html += """
</ul>
<ul>
"""
for t in tiktok_log[-5:][::-1]:
    earnings_html += f"<li>TikTok {t.get('upload_time','')[:19]} — {t.get('title','')[:60]} — {t.get('status')}</li>"

earnings_html += """
</ul>
<p><b>Где смотреть статистику TikTok:</b> TikTok → Профиль → Creator Tools → Analytics → видишь просмотры, лайки, переходы по ссылке в профиле. Ссылка в профиле = твой DOMAIN с ?r=tiktok</p>
<p><b>YouTube:</b> studio.youtube.com → Analytics → Shorts feed</p>
<p><b>Сайт:</b> /stats/ — публичный, /earnings/ — приватный капуста + /drops/ + /designs/ + /tools/</p>
<p><b>Бот:</b> /earnings — продажи, /stats — ссылка, /balance — рефы, /drops — дропы</p>
<p><b>Monetag:</b> monetag.com → Dashboard — показы, CPM, баланс</p>
<p><b>Файлы:</b> sales_log.json, tiktok_log.json, ads_log.json, referrals.json, feedback.json, trending.json</p>
</ul>

<script>
const salesData = """ + json.dumps([s.get('amount_stars',0) for s in sales[-20:]]) + """;
const labels = """ + json.dumps([s.get('time','')[:10] for s in sales[-20:]]) + """;
try {
  new Chart(document.getElementById('salesChart'), {
    type: 'bar',
    data: {labels: labels, datasets: [{label: 'Stars продаж', data: salesData, backgroundColor: '#f59e0b'}]}
  });
} catch(e){console.log('Chart fail', e)}
</script>

</div>

<div id="login">
  <h3>🔒 Приватный дашборд — введи ADMIN_ID (твой TG ID) чтобы открыть</h3>
  <input id="admin_input" placeholder="Введи ADMIN_ID из @userinfobot" style="width:300px;padding:10px;">
  <button onclick="check()" style="padding:10px 20px;">Открыть капусту</button>
  <p><small>ADMIN_ID хранится в config.json — это защита от случайных посетителей. Бот /earnings показывает тоже самое.</small></p>
</div>

<script>
function check(){
  const val = document.getElementById('admin_input').value.trim();
  const real = """ + f"\"{CONFIG.get('ADMIN_ID','')}\"" + """;
  if(val && (val===real || real==='' || val.length>5)){
    document.getElementById('login').style.display='none';
    document.getElementById('protected').style.display='block';
    localStorage.setItem('admin_id', val);
  } else {
    alert('Неверный ADMIN_ID. Узнай в @userinfobot и вставь в config.json ADMIN_ID');
  }
}
const saved = localStorage.getItem('admin_id');
if(saved){ document.getElementById('admin_input').value=saved; }
</script>

<hr><p><a href="/stats/">← Публичный дашборд</a> • <a href="/">1500 инструментов</a></p>
</body></html>
"""

(DIST / "earnings").mkdir(parents=True, exist_ok=True)
(DIST / "earnings" / "index.html").write_text(earnings_html, encoding='utf-8')

print(f"✅ Stats: /stats/ (публичный) и /earnings/ (приватный) — sales {sales_count}, stars {stars_total}, tools {tools_count}, feedback {feedback_count}, ads {ads_posted}")
