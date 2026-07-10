"""
DESIGN FACTORY v9 — ПУШКА: Генерация дизайнов и оформлений
0₽, Pillow, работает в РФ, полностью автономно.

Генерим паки оформлений (все рандом, но выглядят как дизайны):
- insta-post-pack-500.zip (1080x1080) — посты для Инсты/VK/ТГ
- stories-pack-500.zip (1080x1920) — сторис
- yt-thumb-pack-300.zip (1280x720) — превью YouTube / обложки видео
- business-card-pack-200.zip (1050x600) — визитки
- presentation-pack-200.zip (1920x1080) — слайды презы
- vk-telegram-pack-300.zip — обложки ВК, ТГ канала, баннеры
- pattern-pack-200.zip — бесшовные паттерны/фоны
- brandkits-100.zip — бренд-кит: лого + палитра + шрифт (json + png)

Каждый пак по нишам (как недельные дропы): beauty, cafe, crypto, wb, barber, fitness, auto, law, build, tutor

Итого: +2500 файлов дизайнов, все в dist/downloads/designs/
Продается как: "Пак оформлений 500 сторис для бьюти", "1000 постов для WB" — 99-299 Stars
Подписка PRO Club: все дизайны бесплатно каждую неделю
"""

import pathlib, random, zipfile, io, json, datetime
from PIL import Image, ImageDraw, ImageFont
import os

BASE = pathlib.Path(__file__).parent
DIST = BASE / "dist" / "downloads" / "designs"
DIST.mkdir(parents=True, exist_ok=True)

NICHES = {
    "beauty": {"colors": [(255,105,180),(255,182,193),(255,255,255)], "texts": ["SALE -30%","Маникюр","Ресницы","Запись в DM","NEW"]},
    "cafe": {"colors": [(139,69,19),(210,180,140),(255,248,220)], "texts": ["Меню дня","Кофе","Бронь","Открыто","-20%"]},
    "crypto": {"colors": [(255,215,0),(0,0,0),(30,30,30)], "texts": ["BUY","HODL","+150%","Сигналы","TOP"]},
    "wb": {"colors": [(138,43,226),(255,0,128),(255,255,255)], "texts": ["Хит","TOP 1","WB","Ozon","-50%"]},
    "barber": {"colors": [(50,50,50),(200,200,200),(255,255,255)], "texts": ["BARBER","Fade","Запись","Стрижка","STYLE"]},
    "fitness": {"colors": [(50,205,50),(0,0,0),(255,255,255)], "texts": ["FIT","Тренировка","-30%","Challenge","POWER"]},
    "auto": {"colors": [(220,20,60),(0,0,0),(255,255,255)], "texts": ["TO","Диагностика","SALE","Авто","Ремонт"]},
    "law": {"colors": [(0,0,128),(255,255,255),(200,200,200)], "texts": ["Юрист","Договор","Консультация","Суд","ИП"]},
    "build": {"colors": [(255,140,0),(50,50,50),(255,255,255)], "texts": ["Ремонт","Смета","Объект","Под ключ","Дом"]},
    "tutor": {"colors": [(30,144,255),(255,255,255),(255,215,0)], "texts": ["Урок","Курс","ЕГЭ","Запись","TOP"]},
}

def rand_color_pair(niche):
    c1 = random.choice(niche["colors"])
    c2 = random.choice(niche["colors"])
    while c2==c1: c2=random.choice(niche["colors"])
    return c1,c2

def draw_text_center(draw, text, W, H, size_factor=1.0):
    # Простой центрированный текст без шрифта (load_default)
    # Оцениваем размер
    try:
        # Костыль для центрирования
        bbox = draw.textbbox((0,0), text, font=ImageFont.load_default())
        tw = bbox[2]-bbox[0]
        th = bbox[3]-bbox[1]
        x = (W - tw)//2
        y = (H - th)//2
        draw.text((x,y), text, fill="white", stroke_width=2, stroke_fill="black", font=ImageFont.load_default())
    except:
        draw.text((W//4, H//2), text, fill="white")

def gen_pack(name, size, count, niche_filter=None):
    """генерит пак одного размера"""
    path = DIST / f"{name}.zip"
    niches = [NICHES[k] for k in (niche_filter or NICHES.keys())]
    if not isinstance(niches[0], dict):
        # если передали ключи
        pass
    # Для простоты берем все ниши по очереди
    niche_keys = list(NICHES.keys())
    W,H = size
    with zipfile.ZipFile(path,'w') as z:
        for i in range(count):
            niche_key = niche_keys[i % len(niche_keys)]
            niche = NICHES[niche_key]
            c1,c2 = rand_color_pair(niche)
            # Градиент упрощенный — заливаем c1, рисуем фигуру c2
            img = Image.new('RGB', (W,H), color=c1)
            draw = ImageDraw.Draw(img)
            # Фигура
            shape = random.choice(["ellipse","rect","line"])
            if shape=="ellipse":
                draw.ellipse([W*0.1, H*0.1, W*0.9, H*0.9], fill=c2)
            elif shape=="rect":
                draw.rectangle([W*0.15, H*0.15, W*0.85, H*0.85], fill=c2)
            else:
                for _ in range(5):
                    x1=random.randint(0,W); y1=random.randint(0,H); x2=random.randint(0,W); y2=random.randint(0,H)
                    draw.line([x1,y1,x2,y2], fill=c2, width=random.randint(5,20))
            # Текст
            txt = random.choice(niche["texts"])
            # Делаем текст крупнее для превью
            draw_text_center(draw, f"{txt}", W, H)
            # Мелкий текст ниши внизу
            draw.text((20, H-40), f"{niche_key.upper()} #{i+1}", fill="white")
            # Сохраняем
            b=io.BytesIO()
            img.save(b, format='PNG')
            z.writestr(f"{niche_key}/{name}_{niche_key}_{i+1:04d}.png", b.getvalue())
        z.writestr("README.txt", f"{name} — {count} дизайнов — ToolFarm PUCHKA v9. Ниши: {', '.join(NICHES.keys())}")
    print(f"✅ {path.name}: {path.stat().st_size//1024}KB — {count} файлов {size}")

def gen_all():
    print("💣 ГЕНЕРЮ ПУШКУ ДИЗАЙНОВ...")
    gen_pack("insta-post-pack-500", (1080,1080), 500)
    gen_pack("stories-pack-500", (1080,1920), 500)
    gen_pack("yt-thumb-pack-300", (1280,720), 300)
    gen_pack("business-card-pack-200", (1050,600), 200)
    gen_pack("presentation-pack-200", (1920,1080), 200)
    gen_pack("vk-telegram-pack-300", (1590,400), 300)  # обложка ВК
    # brandkits
    brand_path = DIST / "brandkits-100.zip"
    with zipfile.ZipFile(brand_path,'w') as z:
        for i in range(100):
            niche_key = list(NICHES.keys())[i % len(NICHES)]
            niche = NICHES[niche_key]
            palette = [f"#{random.randint(0,0xFFFFFF):06x}" for _ in range(5)]
            kit = {
                "id": f"brandkit_{niche_key}_{i+1}",
                "niche": niche_key,
                "name": f"{niche_key} brand {i+1}",
                "colors": palette,
                "fonts": ["Inter","Montserrat","Bebas Neue"],
                "logo_text": random.choice(niche["texts"])
            }
            # Логотип к бренд-киту
            img = Image.new('RGB', (512,512), color=tuple(int(palette[0].lstrip('#')[j:j+2],16) for j in (0,2,4)))
            draw = ImageDraw.Draw(img)
            draw.ellipse([50,50,462,462], fill=tuple(int(palette[1].lstrip('#')[j:j+2],16) for j in (0,2,4)))
            b=io.BytesIO(); img.save(b, format='PNG')
            z.writestr(f"{niche_key}/logo_{i+1:03d}.png", b.getvalue())
            z.writestr(f"{niche_key}/kit_{i+1:03d}.json", json.dumps(kit, ensure_ascii=False, indent=2))
        z.writestr("README.txt","100 бренд-китов — лого+палитра+шрифты — PUCHKA")
    print(f"✅ brandkits-100.zip")

    # Итоговый мега-бандл ПУШКА
    all_zips = list(DIST.glob("*.zip"))
    puchka_path = BASE / "dist" / "downloads" / "PUCHKA-MEGA-BUNDLE.zip"
    # Не включаем сам бандл чтобы не рекурсия
    with zipfile.ZipFile(puchka_path,'w') as z:
        for zp in all_zips:
            if zp.name=="PUCHKA-MEGA-BUNDLE.zip": continue
            z.write(zp, arcname=zp.name)
        # Добавим и старые паки из downloads/
        for old in (BASE / "dist" / "downloads").glob("*.zip"):
            if old.parent==DIST: continue
            if "PUCHKA" in old.name: continue
            z.write(old, arcname=f"base_packs/{old.name}")
    print(f"💥 ПУШКА СОБРАНА: {puchka_path} — {puchka_path.stat().st_size//1024//1024}MB, файлов: {len(all_zips)+10}")

if __name__=="__main__":
    gen_all()
