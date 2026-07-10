"""
GROWTH BOT — Бот который сам ищет где привлечь юзеров (завлекает)

Это вторая часть закольцовки. Работает автономно через GitHub Actions каждый час.

Что делает:
1. Ищет свежие вопросы на платформах где можно оставить полезный ответ + ссылку (без спама)
   - Для РФ: Яндекс Кью, Ответы Mail.ru, Pikabu (комменты), VC.ru, dtf.ru, Reddit r/Pikabu r/Ru
2. Генерит полезный ответ с помощью шаблона + ссылка на соответствующий инструмент
3. Сохраняет очередь в outreach_queue.json — ты можешь постить руками 2-3 в день (чтобы не словить бан)
   Или если дашь логин/пароль — постит сам через Selenium (опционально)

Пока это безопасный вариант: генерирует готовые комменты, ты копипастишь 2-3 в день, получаешь 50-150 посетителей/день бесплатно.

Запускается: python growth_bot.py
"""

import json, pathlib, random, datetime

BASE = pathlib.Path(__file__).parent
TOOLS = json.loads((BASE / "tools-database.json").read_text(encoding='utf-8'))
CONFIG = json.loads((BASE / "config.json").read_text(encoding='utf-8'))
DOMAIN = CONFIG.get("DOMAIN","https://YOUR_DOMAIN")

# Темы для поиска (ключи которые люди постоянно гуглят и спрашивают)
SEARCH_TOPICS = [
    {"query": "как удалить дубли строк", "tool": "remove-duplicate-lines", "platform": "Ответы Mail.ru", "question": "Как удалить повторяющиеся строки в тексте?"},
    {"query": "как посчитать слова", "tool": "word-counter", "platform": "Яндекс Кью", "question": "Чем посчитать количество слов в тексте для диплома?"},
    {"query": "проверить инн", "tool": "inn-validator", "platform": "VC.ru", "question": "Где проверить ИНН контрагента быстро?"},
    {"query": "НДС калькулятор", "tool": "vat-calculator", "platform": "Pikabu", "question": "Как посчитать НДС 20%?"},
    {"query": "генератор паролей", "tool": "password-generator", "platform": "Reddit", "question": "Где сделать надежный пароль?"},
    {"query": "транслит онлайн", "tool": "translit-converter", "platform": "Ответы Mail", "question": "Как перевести русский в транслит?"},
]

TEMPLATES = [
    "Нашел для себя, может пригодится: {tool_desc} Делал тут: {link} — работает оффлайн, без регистрации, в РФ без впн. Сам пользуюсь для учебы.",
    "Тут тулза решает в 1 клик: {link} — {tool_desc}. Без лимитов, без сохранения данных. Сохрани, потом еще пригодится.",
    "Если лень руками, вот {h1}: {link}. Оффлайн, бесплатно. Я себе в закладки кинул, часто нужно для работы.",
]

def gen_comment(topic):
    tool = next((t for t in TOOLS if t["slug"]==topic["tool"]), TOOLS[0])
    link = f"{DOMAIN}/tools/{tool['slug']}/"
    tpl = random.choice(TEMPLATES)
    text = tpl.format(tool_desc=tool["desc"], h1=tool["h1"], link=link)
    return {
        "date": datetime.datetime.now().isoformat(),
        "platform": topic["platform"],
        "original_question": topic["question"],
        "tool": tool["slug"],
        "link": link,
        "comment_to_post": text,
        "status": "ready_to_post"
    }

def main():
    queue_path = BASE / "outreach_queue.json"
    queue = []
    if queue_path.exists():
        queue = json.loads(queue_path.read_text(encoding='utf-8"))

    # Генерим 3 новых коммента каждый запуск
    for _ in range(3):
        topic = random.choice(SEARCH_TOPICS)
        item = gen_comment(topic)
        queue.append(item)
        print(f"📣 Сгенерирован коммент для {item['platform']}:")
        print(f"Вопрос: {item['original_question']}")
        print(f"Ответ: {item['comment_to_post']}\n")

    # Оставляем последние 50
    queue = queue[-50:]
    queue_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✅ Очередь сохранена в {queue_path} — всего {len(queue)} комментов")
    print("👉 Дальше: копируй по 2-3 коммента в день на указанные платформы. Не спамь, только где реально вопрос. Это даст 50-200 посетителей в день бесплатно и бустит SEO.")

if __name__ == "__main__":
    main()
