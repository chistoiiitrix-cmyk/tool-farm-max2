"""
АВТОТРАФИК-БОТ v1 - Постит твои инструменты в источники трафика автономно
Работает через GitHub Actions, тебе ничего делать не надо после настройки

Идея: берет tool из базы и создает пост для Reddit/Quora/Pinterest - дает ценность, а не спам.
0 вложений, использует бесплатные API.

Для Reddit нужен PRAW (бесплатно). Для Pinterest - можно через RSS.
Пока это скелет - подключишь ключи когда будет домен.
"""
import json, random, pathlib, datetime

BASE = pathlib.Path(__file__).parent
DB = json.loads((BASE / "tools-database.json").read_text(encoding='utf-8'))

def generate_reddit_post(tool):
    templates = [
        f"Нашел для себя тулзу, может кому пригодится: {tool['h1']}. {tool['desc']} Работает локально, без регистрации. Вот линк: https://YOUR_DOMAIN/tools/{tool['slug']}/ — сэкономил мне кучу времени на учебе.",
        f"Задолбался {tool['slug'].replace('-',' ')} вручную. Сделал мини-страничку которая делает это в 1 клик. Без рекламы в лицо и без слива данных. https://YOUR_DOMAIN/tools/{tool['slug']}/ Если есть идеи как улучшить — пишите.",
        f"LPT: Для тех кто часто {tool['keywords'].split(',')[0]} — вот бесплатный офлайн инструмент: https://YOUR_DOMAIN/tools/{tool['slug']}/ Не требует установки."
    ]
    return random.choice(templates)

def daily_job():
    tool = random.choice(DB)
    post = generate_reddit_post(tool)
    
    # Логируем что бы постить
    log_path = BASE / "traffic_log.txt"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.datetime.now()}] TOOL: {tool['slug']}\nPOST: {post}\n---\n")
    
    # ТУТ ДОБАВЛЯЕШЬ ОТПРАВКУ:
    # 1. Reddit: reddit.subreddit("productivity").submit(title, selftext=post)
    # 2. Quora: через Selenium или API
    # 3. Telegram канал: через Bot API (бесплатно) - самый простой для старта!
    
    print(f"Пост сгенерирован для {tool['slug']}")
    print(post)
    print("\nСледующий шаг: подключи Telegram бота - это 10 мин и дает первый трафик без бана.")

if __name__ == "__main__":
    daily_job()
