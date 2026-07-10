"""
WEEKLY DROP FACTORY — авто-дроп каждую неделю для продажи и подписки
Запускается по cron каждый понедельник 6 UTC через GitHub Actions.
Генерит новый пак недели: 50 лого + 100 промтов трендовой ниши + 20 шаблонов
Записывает в drops.json манифест, который читает бот.

Логика:
- Неделя 1: ниша кафе
- Неделя 2: WB sellers
- Неделя 3: крипто боты
и т.д. — 52 недели в году, бесконечный контент.

Подписка PRO Club 199 Stars/мес = все дропы бесплатно
Отдельный дроп = 49-99 Stars

Бот: /drops — список, /buy_drop_Wxx — купить
"""

import json, pathlib, random, zipfile, io, datetime
from PIL import Image, ImageDraw, ImageFont

BASE = pathlib.Path(__file__).parent
DIST = BASE / "dist" / "downloads" / "weekly"
DIST.mkdir(parents=True, exist_ok=True)
DROPS_MANIFEST = BASE / "dist" / "downloads" / "drops.json"
if not DROPS_MANIFEST.exists():
    DROPS_MANIFEST.write_text("[]", encoding='utf-8')

NICHES = [
    {"id": "cafe", "name": "Кафе и рестораны", "keywords": ["меню","бронь","кофе"]},
    {"id": "wb", "name": "WB/Ozon продавцы", "keywords": ["карточка товара","описание","SEO"]},
    {"id": "crypto", "name": "Крипто боты и каналы", "keywords": ["сигналы","бот","трейдинг"]},
    {"id": "barber", "name": "Барбершопы и салоны", "keywords": ["стрижка","запись","прайс"]},
    {"id": "fitness", "name": "Фитнес и спорт", "keywords": ["тренировка","абонемент","челлендж"]},
    {"id": "auto", "name": "Автосервисы", "keywords": ["диагностика","ТО","запчасти"]},
    {"id": "law", "name": "Юристы", "keywords": ["договор","иск","консультация"]},
    {"id": "build", "name": "Стройка и ремонт", "keywords": ["смета","отделка","объект"]},
    {"id": "beauty", "name": "Бьюти сфера", "keywords": ["маникюр","ресницы","уход"]},
    {"id": "tutor", "name": "Репетиторы", "keywords": ["урок","курс","домашка"]},
]

def gen_week_niche():
    # Выбираем нишу по номеру недели
    year, week, _ = datetime.date.today().isocalendar()
    niche = NICHES[week % len(NICHES)]
    return year, week, niche

def gen_logos(niche, out_path, count=50):
    with zipfile.ZipFile(out_path,'w') as z:
        for i in range(count):
            img = Image.new('RGB', (512,512), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            draw = ImageDraw.Draw(img)
            # форма
            draw.ellipse([60,60,452,452], fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            draw.text((140,230), f"{niche['id'].upper()} {i+1}", fill="white", font=ImageFont.load_default())
            b=io.BytesIO(); img.save(b, format='PNG')
            z.writestr(f"logos/{niche['id']}_logo_{i+1:03d}.png", b.getvalue())
        z.writestr("README.txt", f"Weekly drop {niche['name']} — 50 logos — ToolFarm PRO Club")

def gen_prompts(niche, out_path, count=100):
    prompts=[]
    for _ in range(count):
        kw = random.choice(niche["keywords"])
        prompts.append(f"Лого для {niche['name']} с акцентом на {kw}, минимализм, вектор")
        prompts.append(f"Промт Midjourney: {niche['name']} {kw} brand, 4k")
        prompts.append(f"Контент план на неделю для {niche['name']} в ТГ про {kw}")
        prompts.append(f"Договор оказания услуг: {niche['name']} — {kw}")
    prompts = prompts[:count]
    with zipfile.ZipFile(out_path,'w') as z:
        z.writestr("prompts.json", json.dumps(prompts, ensure_ascii=False, indent=2))

def gen_templates(niche, out_path, count=20):
    with zipfile.ZipFile(out_path,'w') as z:
        for i in range(count):
            content = f"""Шаблон {i+1} для ниши {niche['name']}
Услуга: {random.choice(niche['keywords'])}
Договор № {random.randint(100,999)}-{i}
Сумма: {random.randint(5000,150000)} руб.
Дата: {datetime.date.today()}
Подписи: ______ / ______
"""
            z.writestr(f"templates/{niche['id']}_template_{i+1:03d}.txt", content)

def main():
    year, week, niche = gen_week_niche()
    week_id = f"W{year}W{week:02d}_{niche['id']}"
    week_dir = DIST / week_id
    week_dir.mkdir(parents=True, exist_ok=True)

    print(f"Генерю дроп недели {week_id} — ниша {niche['name']}")

    logo_path = week_dir / f"logo-drop-50-{niche['id']}.zip"
    prompts_path = week_dir / f"prompts-drop-100-{niche['id']}.zip"
    templates_path = week_dir / f"templates-drop-20-{niche['id']}.zip"
    bundle_path = week_dir / f"BUNDLE-{week_id}.zip"

    gen_logos(niche, logo_path, 50)
    gen_prompts(niche, prompts_path, 100)
    gen_templates(niche, templates_path, 20)

    # Банлд
    with zipfile.ZipFile(bundle_path,'w') as zb:
        for fp in [logo_path, prompts_path, templates_path]:
            zb.write(fp, arcname=fp.name)

    # Обновляем drops.json
    drops = json.loads((BASE / "dist" / "downloads" / "drops.json").read_text(encoding='utf-8'))
    # Удаляем если такой уже есть (перегенерация)
    drops = [d for d in drops if d["week_id"] != week_id]
    entry = {
        "week_id": week_id,
        "year": year,
        "week": week,
        "date": str(datetime.date.today()),
        "niche": niche,
        "files": {
            "logos": f"weekly/{week_id}/{logo_path.name}",
            "prompts": f"weekly/{week_id}/{prompts_path.name}",
            "templates": f"weekly/{week_id}/{templates_path.name}",
            "bundle": f"weekly/{week_id}/{bundle_path.name}"
        },
        "price_stars": 79,
        "price_stars_bundle": 149,
        "free_for_subscribers": True,
        "description": f"Недельный дроп {niche['name']}: 50 лого, 100 промтов, 20 шаблонов. Свежая ниша недели."
    }
    drops.append(entry)
    # Сорт по дате
    drops.sort(key=lambda x: x["date"], reverse=True)
    (BASE / "dist" / "downloads" / "drops.json").write_text(json.dumps(drops, ensure_ascii=False, indent=2), encoding='utf-8')
    # Копия в корень dist/downloads для бота
    (BASE / "drops.json").write_text(json.dumps(drops, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"✅ DROP {week_id} готов:")
    for f in week_dir.glob("*.zip"):
        print(f" - {f.name}: {f.stat().st_size//1024}KB")
    print(f"Манифест: drops.json — {len(drops)} дропов")

if __name__ == "__main__":
    main()
