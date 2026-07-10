import json, shutil, pathlib

BASE = pathlib.Path(__file__).parent
DB_PATH = BASE / "tools-database.json"
TEMPLATE_PATH = BASE / "site-template" / "template.html"
DIST = BASE / "dist"
CONFIG_PATH = BASE / "config.json"
FAQ_PATH = BASE / "faq_db.json"
FAQ_JSONLD_PATH = BASE / "faq_jsonld_db.json"

def load_config():
    return json.loads(CONFIG_PATH.read_text(encoding='utf-8')) if CONFIG_PATH.exists() else {"DOMAIN":"https://YOUR_USERNAME.github.io/tool-farm","BOT_USERNAME":"YourBot","MONETAG_ZONE":"REPLACE_ME"}

def build():
    config = load_config()
    domain = config.get("DOMAIN","https://YOUR_DOMAIN").rstrip('/')
    bot_username = config.get("BOT_USERNAME","").replace('@','')
    faq_db = json.loads(FAQ_PATH.read_text(encoding='utf-8')) if FAQ_PATH.exists() else {}
    faq_jld = json.loads(FAQ_JSONLD_PATH.read_text(encoding='utf-8')) if FAQ_JSONLD_PATH.exists() else {}

    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "tools").mkdir(parents=True)
    (DIST / "pro").mkdir(parents=True)

    tools = json.loads(DB_PATH.read_text(encoding='utf-8'))
    template = TEMPLATE_PATH.read_text(encoding='utf-8')

    pages=[]
    for tool in tools:
        faq_html = faq_db.get(tool["slug"], "")
        faq_j = json.dumps(faq_jld.get(tool["slug"], {}), ensure_ascii=False)
        html = (template.replace("{{TITLE}}", tool["title"])
                .replace("{{H1}}", tool["h1"])
                .replace("{{DESC}}", tool["desc"])
                .replace("{{KEYWORDS}}", tool["keywords"])
                .replace("{{JS_FUNC}}", tool["js_func"])
                .replace("{{PLACEHOLDER}}", tool["placeholder"])
                .replace("{{AFFILIATE_NICHE}}", tool["affiliate_niche"])
                .replace("{{SLUG}}", tool["slug"])
                .replace("{{DOMAIN}}", domain)
                .replace("{{BOT_USERNAME}}", bot_username)
                .replace("{{FAQ_HTML}}", faq_html)
                .replace("{{FAQ_JSONLD}}", faq_j))
        if config.get("MONETAG_ZONE") and config["MONETAG_ZONE"]!="REPLACE_ME":
            monetag = f'<script src="https://alwingulla.com/88/tag.min.js" data-zone="{config["MONETAG_ZONE"]}" async></script>'
            # + push zone if exists
            push_zone = config.get("MONETAG_PUSH_ZONE")
            if push_zone:
                monetag += f'\n<script src="https://alwingulla.com/88/tag.min.js" data-zone="{push_zone}" data-push="1" async></script>'
            html = html.replace('<!-- СЮДА КОД MONETAG', monetag+'\n<!--')
        (DIST / "tools" / tool["slug"]).mkdir(parents=True, exist_ok=True)
        (DIST / "tools" / tool["slug"] / "index.html").write_text(html, encoding='utf-8')
        pages.append(f"/tools/{tool['slug']}/")

    # index
    index_html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>ToolFarm.ONE — 150 инструментов BOOSTED + PRO + бот</title>
    <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/water.css@2/out/water.css'><link rel='manifest' href='/manifest.json'></head>
    <body><h1>ToolFarm.ONE — 150 BOOSTED инструментов</h1>
    <p>SEO + FAQ Schema + PWA + Push + Дзен + Видео-ферма + Закольцовка. Все работает в РФ.</p>
    <p>Монетизация x2-3: Monetag Tag + Push + Vignette + партнёрки. Каждая страница ловит трафик из Яндекса вечно.</p>
    <p><a href="/pro/"><b>🔓 PRO пак — 50 доп инструментов</b></a></p>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;">"""
    for t in tools:
        index_html+=f"<div style='border:1px solid #eee;padding:10px;border-radius:8px;'><a href='/tools/{t['slug']}/'><b>{t['h1']}</b></a><br><small>{t['desc']}</small></div>"
    index_html+=f"</div><hr><p>Тотал {len(tools)} страниц. Sitemap: /sitemap.xml | <a href='/pro/'>PRO</a></p></body></html>"
    (DIST / "index.html").write_text(index_html, encoding='utf-8')

    # pro page V6 — максимальная автономность + подписки + платный контент 250+ лого
    pro_html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>PRO пак 250+ лого + BOOST + подписка</title>
    <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/water.css@2/out/water.css'></head>
    <body>
    <h1>🔓 PRO v6 — Автономная касса: пак 250+ лого + 50 PRO инструментов + подписка</h1>
    <p>Зашел, собрал капусту и все. 3 варианта доступа — все автономно через бота:</p>

    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;">
      <div style="border:2px solid #111;padding:14px;border-radius:12px;">
        <h3>1️⃣ Бесплатно за 3 рефа — вирус</h3>
        <p>Поделись реф ссылкой в 3 чатах → получи PRO код</p>
        <p><a href='https://t.me/{bot_username}'><b>Получить рефку в боте</b></a></p>
        <small>Закольцовка: трафик растет сам</small>
      </div>
      <div style="border:2px solid #f59e0b;padding:14px;border-radius:12px;background:#fffbe6;">
        <h3>2️⃣ Купить PRO за 150 Stars (~$2.5)</h3>
        <p>250+ лого PNG, 1000 промтов, 100 договоров РФ, 750 инструментов offline, 50 PRO тулзов, исходники</p>
        <p><b>Авто-доставка ботом за 5 сек</b></p>
        <a href='https://t.me/{bot_username}?start=buy_pro' style="background:linear-gradient(135deg,#f59e0b,#ef4444);color:#fff;padding:10px 14px;border-radius:8px;text-decoration:none;font-weight:800;display:inline-block;">💳 Купить за Stars</a>
        <br><small>Работает в РФ, без внешних сайтов, через Telegram Stars</small>
      </div>
      <div style="border:2px solid #111;padding:14px;border-radius:12px;background:#111;color:#fff;">
        <h3>3️⃣ Подписка PRO Club 199 Stars/мес</h3>
        <p>Каждый день 1 новый пак (лого/промты/шаблоны) в приватный канал. Авто-доступ.</p>
        <a href='https://t.me/{bot_username}?start=buy_sub' style="background:#fff;color:#111;padding:10px 14px;border-radius:8px;text-decoration:none;font-weight:800;display:inline-block;">🔁 Подписаться 199 Stars</a>
        <br><small>Отмена /sub_cancel</small>
      </div>
    </div>

    <div style="background:#111;color:#fff;padding:18px;border-radius:12px;margin-top:18px;">
    <h3 style="color:#facc15;">Уже есть код? Разблокируй PRO</h3>
    <input id="code" placeholder="PRO-xxx-UNLOCKED" style="width:100%;padding:12px;border-radius:8px;"><button onclick="unlock()" style="background:#f59e0b;padding:10px 20px;border:none;border-radius:8px;font-weight:800;margin-top:10px;color:#000;">Разблокировать PRO</button><div id="msg" style="margin-top:12px;"></div>
    <hr style="border-color:#333;">
    <h4>📦 Что внутри после оплаты (авто-доставка в боте):</h4>
    <ul>
      <li><a href="/downloads/logo-pack-250.zip" style="color:#facc15;">logo-pack-250.zip</a> — 250 лого PNG (сгенерированы кодом)</li>
      <li><a href="/downloads/prompts-1000.zip" style="color:#facc15;">prompts-1000.zip</a> — 1000 промтов ChatGPT/Midjourney/Sora</li>
      <li><a href="/downloads/contracts-rf-100.zip" style="color:#facc15;">contracts-rf-100.zip</a> — 100 шаблонов договоров РФ</li>
      <li><a href="/downloads/tools-offline-750.zip" style="color:#facc15;">tools-offline-750.zip</a> — 750 инструментов offline</li>
      <li>50 PRO инструментов (массовая проверка ИНН пачкой и т.д.)</li>
      <li>Исходники фермы 750 страниц + бот + Дзен 150 + Видео 150</li>
    </ul>
    </div>

    <script>
    function unlock(){{
        const c=document.getElementById('code').value.trim();
        if(c.startsWith('PRO-')&&c.includes('UNLOCKED')){{
            localStorage.setItem('pro_unlocked','1');
            document.getElementById('msg').innerHTML='✅ PRO открыт! <br><br>Скачай паки:<br><a href="/downloads/logo-pack-250.zip">logo-pack-250.zip</a><br><a href="/downloads/prompts-1000.zip">prompts-1000.zip</a><br><a href="/downloads/contracts-rf-100.zip">contracts-rf-100.zip</a><br><a href="/downloads/tools-offline-750.zip">offline 750</a><br><br>Исходники: попроси у бота /source';
        }}else{{
            document.getElementById('msg').innerHTML='❌ Неверный код. Получи в боте: https://t.me/{bot_username} — /buy или /balance';
        }}
    }}
    if(localStorage.getItem('pro_unlocked')) document.getElementById('msg').innerHTML='✅ PRO уже разблокирован: '+localStorage.getItem('pro_code');
    </script>

    <hr><p><a href="/">← 750 инструментов</a> • <a href="/earnings/">💰 Капуста дашборд</a></p>
    </body></html>"""
    (DIST / "pro" / "index.html").write_text(pro_html, encoding='utf-8')

    # manifest + sw + robots + sitemap
    manifest = {"name":"ToolFarm.ONE 150","short_name":"ToolFarm","start_url":"/","display":"standalone","background_color":"#fff","theme_color":"#f59e0b","icons":[{"src":"https://cdn-icons-png.flaticon.com/512/1087/1087815.png","sizes":"512x512","type":"image/png"}]}
    (DIST / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (DIST / "sw.js").write_text("self.addEventListener('install',e=>self.skipWaiting());self.addEventListener('fetch',e=>{e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));});", encoding='utf-8')
    sitemap = '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    sitemap += f'<url><loc>{domain}/</loc><priority>1.0</priority></url><url><loc>{domain}/pro/</loc><priority>0.9</priority></url>'
    for p in pages: sitemap+=f'<url><loc>{domain}{p}</loc><priority>0.8</priority></url>'
    sitemap+='</urlset>'
    (DIST / "sitemap.xml").write_text(sitemap, encoding='utf-8')
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {domain}/sitemap.xml\n", encoding='utf-8')

    print(f"✅ BOOSTED BUILD: {len(tools)} + PRO + FAQ + PWA + manifest")

if __name__=="__main__":
    build()
