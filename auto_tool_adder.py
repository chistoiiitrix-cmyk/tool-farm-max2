"""
AUTO TOOL ADDER v10 — Авто-добавление инструментов из обратной связи
Запускается каждый день через GitHub Actions (cron 0 8 * * *)
Читает feedback.json → берет топ-3 идеи → генерит новые инструменты → добавляет в DB → коммитит

Генерация через:
1. Groq API (бесплатно, ключ в Secrets GROQ_API_KEY) — если есть, генерит идеальный slug/title/desc/js
2. Фолбек — эвристика из feedback_system.py (без API)

Полностью автономно: юзер просит → ночью появляется инструмент → утром в sitemap → индекс → трафик
"""

import json, pathlib, os, re, datetime
try:
    import requests
except ImportError:
    requests = None

BASE = pathlib.Path(__file__).parent
FEEDBACK_PATH = BASE / "feedback.json"
TOOLS_DB_PATH = BASE / "tools-database.json"
CONFIG_PATH = BASE / "config.json"

def load_json(p, default):
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default

def gen_tool_via_groq(idea_text, groq_key):
    """Через Groq API (llama3-8b, бесплатно) генерит JSON инструмента"""
    if not groq_key or not requests:
        return None
    try:
        prompt = f"""Ты генератор инструментов для сайта ToolFarm. Пользователь просит: "{idea_text}"
Сгенерируй JSON одного инструмента для сайта. Формат:
{{
  "slug": "короткий-url-латиницей-через-дефис",
  "title": "Короткое название",
  "h1": "H1 заголовок для SEO",
  "desc": "Описание 1 предложение",
  "keywords": "ключевые слова через запятую",
  "js_func": "выбери: textTool, wordCount, jsonFormat, base64Tool, generatorTool, calcTool",
  "placeholder": "Вставь текст...",
  "affiliate_niche": "none"
}}
Только JSON, без текста.
"""
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=20
        )
        if resp.status_code==200:
            content = resp.json()["choices"][0]["message"]["content"]
            # вытаскиваем JSON
            m = re.search(r'\{.*\}', content, re.DOTALL)
            if m:
                return json.loads(m.group(0))
    except Exception as e:
        print(f"Groq fail: {e}")
    return None

def gen_tool_fallback(idea_text):
    slug = re.sub(r'[^a-z0-9]+','-', idea_text.lower()[:40])
    slug = re.sub(r'[^a-z0-9\-]','', slug).strip('-')
    if len(slug)<3:
        slug = f"tool-{abs(hash(idea_text))%10000}"
    slug = slug[:40]
    return {
        "slug": slug,
        "title": idea_text[:50],
        "h1": idea_text[:80],
        "desc": f"Инструмент по запросу: {idea_text}",
        "keywords": idea_text.lower(),
        "js_func": "textTool",
        "placeholder": "Вставь текст...",
        "affiliate_niche": "none"
    }

def main():
    feedback = load_json(FEEDBACK_PATH, [])
    tools = load_json(TOOLS_DB_PATH, [])
    existing_slugs = set(t["slug"] for t in tools)

    # Топ идеи по голосам — исключаем уже реализованные
    ideas = [f for f in feedback if f.get("type")=="idea" and not f.get("implemented")]
    ideas_sorted = sorted(ideas, key=lambda x: x.get("votes",0), reverse=True)

    # Берем только те что >=2 голоса или хотя бы 1 и свежие (7 дней)
    to_add=[]
    for idea in ideas_sorted[:5]:
        if idea.get("votes",0)>=2 or (datetime.datetime.now() - datetime.datetime.fromisoformat(idea["date"])).days < 7:
            to_add.append(idea)

    if not to_add:
        print("Нет новых идей для добавления")
        return

    groq_key = os.getenv("GROQ_API_KEY") or load_json(CONFIG_PATH, {}).get("GROQ_API_KEY")

    added=[]
    for idea in to_add[:3]:  # максимум 3 в день чтобы не спамить
        txt = idea["text"]
        # генерим
        tool = gen_tool_via_groq(txt, groq_key) if groq_key else None
        if not tool:
            tool = gen_tool_fallback(txt)
        # Проверяем slug уникальный
        base_slug = tool["slug"]
        i=1
        while tool["slug"] in existing_slugs:
            tool["slug"] = f"{base_slug}-{i}"
            i+=1
        tools.append(tool)
        existing_slugs.add(tool["slug"])
        added.append(tool)
        print(f"✅ Добавлен инструмент из фидбека: {tool['slug']} — {tool['h1']} (votes={idea.get('votes')})")

    if added:
        TOOLS_DB_PATH.write_text(json.dumps(tools, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"✅ Всего добавлено {len(added)}, теперь {len(tools)} инструментов")
        # Помечаем идеи как реализованные
        for idea in to_add[:len(added)]:
            idea["implemented"]=True
            idea["implemented_slug"]=added[0]["slug"] if added else ""
        FEEDBACK_PATH.write_text(json.dumps(feedback, ensure_ascii=False, indent=2), encoding='utf-8')
    else:
        print("Ничего не добавлено")

if __name__ == "__main__":
    main()
