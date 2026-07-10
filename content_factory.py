"""
CONTENT FACTORY v7 — Авто-расширение паков + еженедельные дропы для продажи/подписки
0₽, работает в РФ, полностью автономно.

Что генерим:
БАЗОВЫЕ РАСШИРЕННЫЕ ПАКИ (один раз, большие, для продажи):
- logo-pack-1000.zip (1000 PNG лого, 10 категорий)
- icon-pack-500.zip (500 иконок)
- prompts-mega-5000.zip (5000 промтов: ChatGPT, Midjourney, Sora, SEO, Insta)
- biz-templates-200.zip (200 шаблонов договоров/актов/счетов/КП РФ)
- color-palettes-500.json (500 палитр по 5 цветов)
- business-names-1000.txt (1000 названий бизнеса)
- hashtags-2000.json (2000 хештегов по нишам)

ЕЖЕНЕДЕЛЬНЫЕ ДРОПЫ (авто, каждый понедельник, для подписки/продажи):
- weekly/W{year}W{week}/logo-drop-50.zip (50 новых лого)
- weekly/W{year}W{week}/prompts-drop-100.zip (100 новых промтов по трендовой нише недели)
- weekly/W{year}W{week}/templates-drop-20.zip (20 новых шаблонов)
- drops.json — манифест всех дропов с ценой, датой, ссылкой

Продажи:
- PRO Club подписка 199 Stars/мес = все недельные дропы бесплатно
- Отдельный дроп = 49-99 Stars (бот продает автоматом)
- Базовые паки = 150 Stars за пак или 399 Stars за все (бандл)

Бот читает drops.json и предлагает /drops, /buy_drop_Wxx
GitHub Actions: каждый понедельник 6 UTC запускает weekly_drop_generator.py → генерит новый дроп → коммитит → деплоит → бот_autonomous постит в приватный канал "Новый дроп недели!"
"""

import json, pathlib, random, zipfile, io, datetime
from PIL import Image, ImageDraw, ImageFont
import os

BASE = pathlib.Path(__file__).parent
DIST = BASE / "dist" / "downloads"
WEEKLY_BASE = DIST / "weekly"
DIST.mkdir(parents=True, exist_ok=True)
WEEKLY_BASE.mkdir(parents=True, exist_ok=True)

# ---------- БАЗОВЫЕ РАСШИРЕННЫЕ ПАКИ ----------
def gen_logo_pack_1000():
    print("Генерю logo-pack-1000 (10 категорий x100)...")
    categories = {
        "tech": [(30,144,255),(0,0,0)],
        "cafe": [(139,69,19),(255,228,181)],
        "crypto": [(255,215,0),(0,0,0)],
        "beauty": [(255,105,180),(255,255,255)],
        "fitness": [(50,205,50),(0,0,0)],
        "auto": [(220,20,60),(255,255,255)],
        "law": [(0,0,128),(255,255,255)],
        "build": [(255,140,0),(0,0,0)],
        "food": [(255,69,0),(255,255,255)],
        "shop": [(138,43,226),(255,255,255)],
    }
    buf_path = DIST / "logo-pack-1000.zip"
    with zipfile.ZipFile(buf_path,'w') as z:
        idx=0
        for cat, (c1,c2) in categories.items():
            for i in range(100):
                idx+=1
                img = Image.new('RGB', (512,512), color=c1)
                draw = ImageDraw.Draw(img)
                # рандом форма
                shape = random.choice(["ellipse","rect","poly"])
                if shape=="ellipse":
                    draw.ellipse([80,80,432,432], fill=c2)
                elif shape=="rect":
                    draw.rectangle([100,100,412,412], fill=c2)
                else:
                    draw.polygon([(256,80),(100,400),(412,400)], fill=c2)
                try:
                    draw.text((150,230), f"{cat.upper()} {i+1}", fill=(0,0,0) if sum(c2)//3>128 else (255,255,255), font=ImageFont.load_default())
                except:
                    draw.text((150,230), f"{cat.upper()} {i+1}", fill="black")
                b = io.BytesIO()
                img.save(b, format='PNG')
                z.writestr(f"{cat}/logo_{cat}_{i+1:03d}.png", b.getvalue())
        z.writestr("README.txt", "1000 логотипов 10 категорий — ToolFarm PRO v7. Автогенерация.")
    print(f"✅ {buf_path} {buf_path.stat().st_size//1024}KB")

def gen_icon_pack_500():
    print("Генерю icon-pack-500...")
    path = DIST / "icon-pack-500.zip"
    with zipfile.ZipFile(path,'w') as z:
        for i in range(500):
            img = Image.new('RGBA', (256,256), (0,0,0,0))
            draw = ImageDraw.Draw(img)
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255), 255)
            # иконка — простая геометрия
            t = random.choice(["circle","square","triangle","plus","arrow"])
            if t=="circle": draw.ellipse([32,32,224,224], fill=color)
            elif t=="square": draw.rectangle([32,32,224,224], fill=color)
            elif t=="triangle": draw.polygon([(128,32),(32,224),(224,224)], fill=color)
            elif t=="plus": draw.rectangle([96,32,160,224], fill=color); draw.rectangle([32,96,224,160], fill=color)
            else: draw.polygon([(32,128),(160,32),(224,96),(96,192)], fill=color)
            b=io.BytesIO(); img.save(b, format='PNG')
            z.writestr(f"icons/icon_{i+1:03d}_{t}.png", b.getvalue())
        z.writestr("README.txt","500 иконок — PRO")
    print(f"✅ {path}")

def gen_prompts_mega():
    print("Генерю prompts-mega-5000...")
    niches = {
        "chatgpt_biz": ["Напиши бизнес-план для {biz} в РФ на 2026", "Составь КП для {biz} на сумму {sum} руб", "Скрипт продаж для {biz}", "10 заголовков для ленда {biz}", "SEO статья 1000 слов про {tool}"],
        "midjourney": ["Logo for {biz} minimalist flat vector --ar 1:1 --v 6", "{biz} brand identity, modern, 4k", "Icon for {tool}, line style, white background"],
        "sora": ["Promo video for {biz} 15 sec, cinematic, 4k", "{biz} ad, vertical 9:16, trending TikTok style", "How to {tool} tutorial, screen capture"],
        "insta": ["Reels idea for {biz}: 3 hooks про {tool}", "100 hashtags for {biz} in Russia", "Story template text for {biz} sale"],
        "seo": ["Article outline: {tool} онлайн бесплатно", "Meta title/description for {tool}", "FAQ for {tool} landing"],
    }
    biz = ["кафе","барбершоп","WB магазин","Ozon продавец","крипто бот","тул сайт","репетитор","фитнес","автосервис","салон красоты","юрист","стройка","IT агентство","кофейня","пиццерия"]
    tools = ["удаление дублей","счетчик слов","проверка ИНН","НДС калькулятор","генератор паролей","транслит"]
    prompts=[]
    for cat, tpls in niches.items():
        for _ in range(1000):
            tpl = random.choice(tpls)
            prompts.append({"category": cat, "prompt": tpl.format(biz=random.choice(biz), tool=random.choice(tools), sum=random.randint(5000,500000))})
    random.shuffle(prompts)
    path_json = DIST / "prompts-mega-5000.json"
    path_json.write_text(json.dumps(prompts, ensure_ascii=False, indent=2), encoding='utf-8')
    with zipfile.ZipFile(DIST / "prompts-mega-5000.zip",'w') as z:
        z.writestr("prompts-mega-5000.json", json.dumps(prompts, ensure_ascii=False, indent=2))
        # разобьем по категориям
        for cat in niches.keys():
            cat_prompts = [p for p in prompts if p["category"]==cat]
            z.writestr(f"{cat}.json", json.dumps(cat_prompts, ensure_ascii=False, indent=2))
    print(f"✅ prompts-mega-5000.zip {len(prompts)}")

def gen_biz_templates_200():
    print("Генерю biz-templates-200...")
    services = ["разработка сайта","дизайн логотипа","SMM","контекст","доставка","аренда","консалтинг","ремонт","обучение","маркетинг"]
    with zipfile.ZipFile(DIST / "biz-templates-200.zip",'w') as z:
        for i in range(200):
            num = f"ДГ-{random.randint(100,999)}-{i}"
            service = random.choice(services)
            content = f"""ШАБЛОН {i+1}: ДОГОВОР {service.upper()}
№ {num} от {datetime.date.today()}
Исполнитель: ИП Иванов И.И. ИНН 1234567890
Заказчик: ___________
Предмет: {service}
Сумма: {random.randint(5000,200000)} руб. НДС не облагается (УСН)
Срок: {random.randint(1,30)} дней
Подписи: _________ / _________

АКТ № {num}
Работы по {service} выполнены.
Сумма: ...

СЧЕТ № {num}
...
"""
            z.writestr(f"templates/{service}_{i+1:03d}.txt", content)
        z.writestr("README.txt","200 шаблонов РФ — PRO")
    print("✅ biz-templates-200.zip")

def gen_extra_packs():
    print("Генерю color-palettes + business-names + hashtags...")
    # palettes
    palettes=[]
    for _ in range(500):
        palettes.append([f"#{random.randint(0,0xFFFFFF):06x}" for _ in range(5)])
    (DIST / "color-palettes-500.json").write_text(json.dumps(palettes, ensure_ascii=False, indent=2), encoding='utf-8')
    with zipfile.ZipFile(DIST / "color-palettes-500.zip",'w') as z:
        z.writestr("palettes.json", json.dumps(palettes, ensure_ascii=False, indent=2))
    # business names
    prefixes=["Альфа","Бета","Супер","Мега","Про","Эко","Техно","Смарт","Быстро","Лидер"]
    suffixes=["Торг","Строй","Трейд","Сервис","Групп","Про","Маркет","Лаб","Хаб","Бюро"]
    names=[f"{random.choice(prefixes)}{random.choice(suffixes)} {random.randint(1,99)}" for _ in range(1000)]
    (DIST / "business-names-1000.txt").write_text("\n".join(names), encoding='utf-8')
    # hashtags
    niches_h = {
        "business": ["#бизнес","#рф","#ип","#ооо","#стартап"],
        "tools": ["#инструменты","#лайфхак","#полезное","#бесплатно"],
        "design": ["#лого","#дизайн","#брендинг","#айдентика"],
    }
    hashtags=[]
    for niche, tags in niches_h.items():
        for _ in range(600):
            hashtags.append({"niche": niche, "tags": tags + [f"#{random.choice(['топ','2026','рф','мск','спб'])}{random.randint(1,99)}"]})
    (DIST / "hashtags-2000.json").write_text(json.dumps(hashtags, ensure_ascii=False, indent=2), encoding='utf-8')
    with zipfile.ZipFile(DIST / "extra-pack.zip",'w') as z:
        z.writestr("color-palettes-500.json", json.dumps(palettes, ensure_ascii=False, indent=2))
        z.writestr("business-names-1000.txt", "\n".join(names))
        z.writestr("hashtags-2000.json", json.dumps(hashtags, ensure_ascii=False, indent=2))
    print("✅ extra-pack.zip")

if __name__ == "__main__":
    gen_logo_pack_1000()
    gen_icon_pack_500()
    gen_prompts_mega()
    gen_biz_templates_200()
    gen_extra_packs()
    print("✅ EXPANDED PACKS DONE")
    for f in DIST.glob("*.zip"):
        print(f" - {f.name}: {f.stat().st_size//1024}KB")
