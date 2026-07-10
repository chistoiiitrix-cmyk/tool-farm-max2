"""
NICHE TRENDING FETCHER v10 — Авто-поиск трендовых ниш для дропов и новых инструментов
0₽, работает в РФ, без ключей (free APIs)

Источники трендов:
1. Google Trends daily RSS (geo=RU) — что гуглят в РФ сегодня
2. Reddit r/popular + r/Pikabu + r/RuAsk + r/Entrepreneur (JSON, без ключа)
3. Hacker News top (для dev ниши)
4. Yandex Wordstat идеи через Google Suggest (бесплатно) — подсказки

Выдает top ниш для генерации контента: [{niche_id, keyword, volume_hint, source}]
Сохраняет в trending.json
"""
import json, pathlib, urllib.request, xml.etree.ElementTree as ET, datetime, random

BASE = pathlib.Path(__file__).parent
TRENDING_PATH = BASE / "trending.json"

def fetch_google_trends_ru():
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=RU"
        with urllib.request.urlopen(url, timeout=10) as r:
            data = r.read().decode('utf-8', errors='ignore')
            root = ET.fromstring(data)
            trends=[]
            for item in root.findall('.//item')[:15]:
                title = item.find('title').text if item.find('title') is not None else ""
                if title:
                    trends.append({"keyword": title.lower(), "source": "google_trends_ru", "niche_id": "trending"})
            return trends
    except Exception as e:
        print(f"Google Trends fail: {e}")
        return []

def fetch_reddit_top(subreddit="Pikabu"):
    try:
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit=10"
        req = urllib.request.Request(url, headers={"User-Agent": "ToolFarmBot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            j = json.loads(r.read().decode())
            trends=[]
            for post in j.get("data",{}).get("children",[]):
                title = post["data"].get("title","").lower()
                # извлекаем ключевые слова
                if len(title)>5:
                    trends.append({"keyword": title[:60], "source": f"reddit_{subreddit}", "niche_id": subreddit.lower()})
            return trends
    except Exception as e:
        print(f"Reddit {subreddit} fail: {e}")
        return []

def fetch_hn_top():
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        with urllib.request.urlopen(url, timeout=10) as r:
            ids = json.loads(r.read().decode())[:10]
            trends=[]
            for iid in ids[:5]:
                try:
                    iurl = f"https://hacker-news.firebaseio.com/v0/item/{iid}.json"
                    with urllib.request.urlopen(iurl, timeout=5) as ir:
                        item = json.loads(ir.read().decode())
                        title = item.get("title","").lower()
                        if title:
                            trends.append({"keyword": title[:60], "source": "hackernews", "niche_id": "dev"})
                except: pass
            return trends
    except Exception as e:
        print(f"HN fail: {e}")
        return []

def generate_niche_suggestions():
    # Фолбек если все API упали — берем наши 10 ниш + рандом хвост
    fallback = [
        {"keyword": "удалить дубли в excel", "niche_id": "wb", "source": "fallback"},
        {"keyword": "проверка инн контрагента", "niche_id": "law", "source": "fallback"},
        {"keyword": "генератор логотипа онлайн", "niche_id": "beauty", "source": "fallback"},
        {"keyword": "счетчик слов для диплома", "niche_id": "tutor", "source": "fallback"},
        {"keyword": "калькулятор ндс 20 процентов", "niche_id": "build", "source": "fallback"},
        {"keyword": "транслит онлайн", "niche_id": "tutor", "source": "fallback"},
        {"keyword": "парсер wildberries", "niche_id": "wb", "source": "fallback"},
        {"keyword": "шаблон договора гпх", "niche_id": "law", "source": "fallback"},
        {"keyword": "сторис для бьюти мастера", "niche_id": "beauty", "source": "fallback"},
        {"keyword": "лого для кофейни", "niche_id": "cafe", "source": "fallback"},
    ]
    return fallback

def main():
    all_trends=[]
    all_trends += fetch_google_trends_ru()
    for sub in ["Pikabu","RuAsk","Entrepreneur","popular","InternetIsBeautiful"]:
        all_trends += fetch_reddit_top(sub)
    all_trends += fetch_hn_top()
    if len(all_trends)<5:
        all_trends += generate_niche_suggestions()

    # Маппим ключевые слова на наши ниши
    niche_map = {
        "cafe": ["кафе","кофе","ресторан","меню","бар","пицц"],
        "wb": ["wb","wildberries","ozon","маркетплейс","карточка товара","excel"],
        "beauty": ["маникюр","ресницы","бьюти","салон","красота","сторис"],
        "crypto": ["крипто","биткоин","трейдинг","сигнал","бот"],
        "barber": ["барбер","стрижка","борода","fade"],
        "fitness": ["фитнес","тренировка","спорт","похудение"],
        "auto": ["авто","машина","то","диагностика","запчасти"],
        "law": ["договор","инн","юрист","акт","счет","ндс","налог"],
        "build": ["стройка","ремонт","смета","дом","отделка"],
        "tutor": ["диплом","слова","транслит","учеба","егэ"],
    }

    enriched=[]
    for t in all_trends[:50]:
        kw = t["keyword"]
        matched = "trending"
        for nid, words in niche_map.items():
            if any(w in kw for w in words):
                matched = nid
                break
        enriched.append({"keyword": kw, "niche_id": matched, "source": t["source"], "date": str(datetime.date.today())})

    # Группируем по нишам — топ ниша недели
    from collections import Counter
    niche_counts = Counter([e["niche_id"] for e in enriched])
    top_niche = niche_counts.most_common(1)[0][0] if niche_counts else "trending"

    result = {
        "date": str(datetime.date.today()),
        "top_niche": top_niche,
        "niche_counts": dict(niche_counts),
        "trends": enriched[:30]
    }

    TRENDING_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✅ TRENDING: top niche {top_niche}, total {len(enriched)} keywords")
    print(json.dumps(result, ensure_ascii=False, indent=2)[:1000])
    return result

if __name__ == "__main__":
    main()
