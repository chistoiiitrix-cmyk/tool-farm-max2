"""
FEEDBACK SYSTEM v10 — Авто-сбор обратной связи + авто-создание инструментов
0₽, РФ, автономно

Как работает:
1. На каждом инструменте в template.html добавлен виджет обратной связи:
   "Какой инструмент нужен? Что не работает?" → поле + кнопка
   При клике открывается t.me/бот?start=fb_{текст} — без палева токена
2. Бот ловит /start fb_... → сохраняет в feedback.json + пересылает админу
3. Если в тексте есть "сделайте", "нужен инструмент", "добавьте", "не хватает" — помечаем как idea
4. auto_tool_adder.py раз в день читает feedback.json, берет топ-3 идеи по лайкам/повторам
   и через Groq API (бесплатно) генерит новый инструмент (slug, title, desc, js_func)
   Добавляет в tools-database.json и коммитит → сайт пересобирается автоматом

Пример:
Юзер на /tools/word-counter/ пишет "Сделайте подсчет символов без пробелов для диплома, очень надо"
→ уходит в бота → сохраняется → ночью скрипт генерит инструмент "char-counter-no-spaces" → утром уже на сайте 1501 страница

Полностью замкнутый цикл: посетитель просит → система сама делает → посетитель возвращается → трафик растет.
"""

import json, pathlib, datetime, re
from collections import Counter

BASE = pathlib.Path(__file__).parent
FEEDBACK_PATH = BASE / "feedback.json"
TOOLS_DB = BASE / "tools-database.json"

def load_feedback():
    return json.loads(FEEDBACK_PATH.read_text(encoding='utf-8')) if FEEDBACK_PATH.exists() else []

def save_feedback(data):
    FEEDBACK_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def add_feedback(user_id, text, username=""):
    data = load_feedback()
    entry = {
        "user_id": str(user_id),
        "username": username,
        "text": text,
        "date": datetime.datetime.now().isoformat(),
        "type": "idea" if any(w in text.lower() for w in ["сделайте","нужен","добавьте","хочу","не хватает","инструмент"]) else "feedback",
        "votes": 1
    }
    # Если такой же текст уже есть — +1 голос
    for e in data:
        if e["text"].lower().strip() == text.lower().strip():
            e["votes"] += 1
            e["date"] = entry["date"]
            save_feedback(data)
            return e
    data.append(entry)
    save_feedback(data)
    return entry

def suggest_new_tools_from_feedback(limit=3):
    """Берет топ идей и предлагает новые инструменты"""
    feedback = load_feedback()
    ideas = [f for f in feedback if f["type"]=="idea"]
    # Топ по голосам
    ideas_sorted = sorted(ideas, key=lambda x: x["votes"], reverse=True)[:limit]
    suggestions=[]
    for idea in ideas_sorted:
        txt = idea["text"].lower()
        # Простая эвристика генерации slug
        slug = re.sub(r'[^a-z0-9]+','-', txt[:40].strip())
        slug = re.sub(r'[^a-z0-9\-]','', slug).strip('-')
        if len(slug)<3:
            slug = f"tool-{abs(hash(txt))%10000}"
        # Ограничиваем
        slug = slug[:40]
        suggestions.append({
            "slug": slug,
            "title": idea["text"][:50],
            "h1": idea["text"][:80],
            "desc": f"Инструмент по запросу пользователей: {idea['text']}",
            "keywords": idea["text"].lower(),
            "js_func": "textTool",
            "placeholder": "Вставь текст...",
            "affiliate_niche": "none",
            "source": "feedback",
            "votes": idea["votes"],
            "original_request": idea["text"]
        })
    return suggestions

if __name__ == "__main__":
    # Тест
    print("Feedback count:", len(load_feedback()))
    print("Top ideas:", suggest_new_tools_from_feedback(3))
