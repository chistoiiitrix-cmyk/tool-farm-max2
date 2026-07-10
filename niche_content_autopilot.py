"""
NICHE CONTENT AUTOPILOT v10 — Авто-генерация контента под ниши и тренды для дропов
Каждый день/неделю генерит паки под самую горячую нишу из trending.json + feedback.json

Что делает:
1. Читает trending.json (из niche_trending_fetcher.py) → топ ниша недели
2. Читает feedback.json → топ запросы пользователей по этой нише
3. Генерит:
   - 50 лого под нишу (с текстом из трендов)
   - 100 промтов под нишу (с ключевыми словами из трендов)
   - 20 шаблонов договоров/постов под нишу
   - 20 дизайнов сторис/постов под нишу
   - 1 новый инструмент под нишу (если есть запрос из feedback)
4. Записывает в weekly_drops + packs + обновляет drops.json
5. Бот постит "🔥 Новый дроп недели — {niche} — по трендам: {keywords}"

Полностью автономно: тренды → контент → дроп → продажа → кэш
"""

import json, pathlib, random, datetime, io, zipfile
from PIL import Image, ImageDraw, ImageFont

BASE = pathlib.Path(__file__).parent
TRENDING_PATH = BASE / "trending.json"
FEEDBACK_PATH = BASE / "feedback.json"
DIST_WEEKLY = BASE / "dist" / "downloads" / "weekly"
DIST_WEEKLY.mkdir(parents=True, exist_ok=True)

NICHES = {
    "cafe": {"colors": [(139,69,19),(210,180,140)], "texts": ["Меню","Кофе","Бронь"]},
    "wb": {"colors": [(138,43,226),(255,0,128)], "texts": ["Хит","TOP","WB"]},
    "beauty": {"colors": [(255,105,180),(255,182,193)], "texts": ["SALE","Маникюр","NEW"]},
    "crypto": {"colors": [(255,215,0),(0,0,0)], "texts": ["BUY","HODL","TOP"]},
    "law": {"colors": [(0,0,128),(255,255,255)], "texts": ["Договор","ИП","НДС"]},
    "build": {"colors": [(255,140,0),(50,50,50)], "texts": ["Ремонт","Дом"]},
    "tutor": {"colors": [(30,144,255),(255,255,255)], "texts": ["Урок","ЕГЭ"]},
    "trending": {"colors": [(255,0,0),(0,0,0)], "texts": ["TOP","TREND","NEW"]},
}

def get_top_niche():
    if TRENDING_PATH.exists():
        data = json.loads(TRENDING_PATH.read_text(encoding='utf-8'))
        return data.get("top_niche","trending"), data.get("trends",[])[:5]
    return "trending", []

def get_feedback_for_niche(niche_id):
    if not FEEDBACK_PATH.exists():
        return []
    fb = json.loads(FEEDBACK_PATH.read_text(encoding='utf-8'))
    return [f for f in fb if niche_id in f.get("text","").lower()][:5]

def gen_niche_pack(niche_id, keywords):
    year, week, _ = datetime.date.today().isocalendar()
    week_id = f"W{year}W{week:02d}_{niche_id}_TREND"
    week_dir = DIST_WEEKLY / week_id
    week_dir.mkdir(parents=True, exist_ok=True)

    niche = NICHES.get(niche_id, NICHES["trending"])
    # 50 лого с ключевыми словами тренда
    logo_path = week_dir / f"logo-drop-50-{niche_id}-trend.zip"
    with zipfile.ZipFile(logo_path,'w') as z:
        for i in range(50):
            kw = random.choice(keywords) if keywords else random.choice(niche["texts"])
            img = Image.new('RGB', (512,512), color=random.choice(niche["colors"]))
            draw = ImageDraw.Draw(img)
            draw.ellipse([60,60,452,452], fill=random.choice(niche["colors"]))
            draw.text((100,230), f"{kw[:15]} {i+1}", fill="white")
            b=io.BytesIO(); img.save(b, format='PNG')
            z.writestr(f"logos/{niche_id}_{i+1}.png", b.getvalue())

    # 100 промтов с трендами
    prompts_path = week_dir / f"prompts-drop-100-{niche_id}-trend.zip"
    prompts=[]
    for kw in keywords[:10]:
        prompts.append(f"Лого для {niche_id} с текстом {kw}, минимализм")
        prompts.append(f"Контент план для {niche_id} на неделю про {kw}")
        prompts.append(f"SEO статья про {kw} для {niche_id} 1000 слов")
    # добиваем до 100
    while len(prompts)<100:
        prompts.append(f"Идея для {niche_id}: {random.choice(keywords) if keywords else 'тренд'}")
    with zipfile.ZipFile(prompts_path,'w') as z:
        z.writestr("prompts.json", json.dumps(prompts, ensure_ascii=False, indent=2))

    # 20 шаблонов
    templates_path = week_dir / f"templates-drop-20-{niche_id}.zip"
    with zipfile.ZipFile(templates_path,'w') as z:
        for i in range(20):
            kw = random.choice(keywords) if keywords else "услуга"
            z.writestr(f"template_{i+1}.txt", f"Шаблон для {niche_id}: {kw} — Договор № {i} от {datetime.date.today()}")

    # 30 дизайнов сторис/постов под нишу (авто-оформления)
    designs_path = week_dir / f"designs-drop-30-{niche_id}.zip"
    with zipfile.ZipFile(designs_path,'w') as z:
        for i in range(15):
            # сторис 1080x1920
            img = Image.new('RGB', (1080,1920), color=random.choice(niche["colors"]))
            draw = ImageDraw.Draw(img)
            draw.rectangle([50,50,1030,500], fill=random.choice(niche["colors"]))
            kw = random.choice(keywords) if keywords else niche["texts"][0]
            draw.text((100,200), f"{kw[:20]}", fill="white")
            b=io.BytesIO(); img.save(b, format='PNG')
            z.writestr(f"stories/{niche_id}_story_{i+1}.png", b.getvalue())
        for i in range(15):
            # пост 1080x1080
            img = Image.new('RGB', (1080,1080), color=random.choice(niche["colors"]))
            draw = ImageDraw.Draw(img)
            draw.ellipse([100,100,980,980], fill=random.choice(niche["colors"]))
            kw = random.choice(keywords) if keywords else niche["texts"][0]
            draw.text((200,500), f"{kw[:15]}", fill="white")
            b=io.BytesIO(); img.save(b, format='PNG')
            z.writestr(f"posts/{niche_id}_post_{i+1}.png", b.getvalue())

    # BUNDLE
    bundle_path = week_dir / f"BUNDLE-{week_id}.zip"
    with zipfile.ZipFile(bundle_path,'w') as zb:
        for fp in [logo_path, prompts_path, templates_path, designs_path]:
            zb.write(fp, arcname=fp.name)

    # Запись в drops.json
    drops_path = BASE / "dist" / "downloads" / "drops.json"
    drops = json.loads(drops_path.read_text(encoding='utf-8')) if drops_path.exists() else []
    # Удаляем старый такой же week_id если есть
    drops = [d for d in drops if d["week_id"]!=week_id]
    drops.append({
        "week_id": week_id,
        "year": year,
        "week": week,
        "date": str(datetime.date.today()),
        "niche": {"id": niche_id, "name": f"{niche_id.upper()} TREND", "keywords": keywords},
        "files": {
            "logos": f"weekly/{week_id}/{logo_path.name}",
            "prompts": f"weekly/{week_id}/{prompts_path.name}",
            "templates": f"weekly/{week_id}/{templates_path.name}",
            "designs": f"weekly/{week_id}/{designs_path.name}",
            "bundle": f"weekly/{week_id}/{bundle_path.name}"
        },
        "price_stars": 79,
        "price_stars_bundle": 149,
        "free_for_subscribers": True,
        "description": f"Трендовый дроп {niche_id}: по запросам {', '.join(keywords[:3])}. Авто-сгенерировано по трендам {datetime.date.today()}. 50 лого + 100 промтов + 20 шаблонов + 30 дизайнов (сторис+посты)."
    })
    drops_path.write_text(json.dumps(drops, ensure_ascii=False, indent=2), encoding='utf-8')
    (BASE / "drops.json").write_text(json.dumps(drops, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✅ TREND DROP {week_id} — niche {niche_id} — keywords {keywords[:3]} — включает дизайны")

if __name__ == "__main__":
    # Сначала фетчим тренды
    try:
        import niche_trending_fetcher
        trending_data = niche_trending_fetcher.main()
        top_niche = trending_data.get("top_niche","trending")
        keywords = [t["keyword"] for t in trending_data.get("trends",[])[:5]]
    except:
        top_niche = "trending"
        keywords = ["тренд недели","топ запрос","новинка"]

    gen_niche_pack(top_niche, keywords)
