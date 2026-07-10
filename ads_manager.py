"""
ADS MANAGER v13 — Покупка рекламы в канале с модерацией, без запрещенки
0₽, работает в РФ, полностью автономно

Поток:
1. Юзер /buy_ad в боте
2. Бот: "Пришли текст рекламы (до 500 символов) + ссылку + картинку (опционально, 1 фото)"
3. Юзер шлет текст, бот сохраняет в pending_ads.json со статусом pending
4. Авто-проверка на запрещенку (черный список + длина + ссылка)
   - Запрещенка: наркотики, казино, ставки, оружие, порно, спам, фин пирамиды, крипта скамы и т.д.
   - Если найдено — авто-отклон с причиной
5. Если ок — бот форвардит админу (ADMIN_ID) с кнопками: ✅ Одобрить / ❌ Отклонить + причина
6. Админ жмет Одобрить → бот создает Stars инвойс юзеру: 200 Stars = 1 пост, 500 Stars = 3 поста (закреп на 24ч)
7. Юзер платит Stars → successful_payment с payload ad_{ad_id} → бот постит рекламу в канал CHANNEL_ID с пометкой "Реклама" + ссылка + картинка
8. Лог в ads_log.json + sales_log.json, статистика в dashboard

Модерация:
- Черный список слов (RU/EN)
- Проверка ссылки на фишинг (просто проверка домена на короткий список)
- Лимит 1 реклама в день на юзера (чтобы не спамили)
- Админ может в любой момент отклонить

Оплата:
- Telegram Stars: 200 Stars = 1 пост ( ~$3.3 ), 500 Stars = 3 поста + закреп
- Авто-доставка: после оплаты бот сам постит, без тебя
"""

import json, pathlib, datetime, re, os

BASE = pathlib.Path(__file__).parent
PENDING_ADS = BASE / "pending_ads.json"
ADS_LOG = BASE / "ads_log.json"

# Черный список запрещенки — расширяемый
BLACKLIST = [
    "казино","casino","1xbet","ставки","букмекер","наркотик","мефедрон","героин","оружие","пистолет","автомат","проститут","порно","porn","onlyfans","пирамида","млм","крипта.*инвест.*100%","удвой крипту","займ под 0","микрозайм",
    "закладки","спайс","соль","экстази","кокаин","амфетамин","оружие","взрывчатка","терроризм","экстремизм",
    "детское порно","cp","лолит"
]

# Разрешенные домены? Проверяем что не фишинг короткий
SUSPICIOUS_DOMAINS = ["bit.ly","tinyurl","short.link"]  # можно разрешать но с предупреждением

def load_json(p, default):
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default

def save_json(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def check_ad_text(text, link=""):
    """Возвращает (ok: bool, reason: str)"""
    low = (text + " " + link).lower()
    # Длина
    if len(text)<10:
        return False, "Слишком короткий текст, минимум 10 символов"
    if len(text)>800:
        return False, "Слишком длинный, максимум 800"
    # Черный список
    for bad in BLACKLIST:
        # поддержка regex
        if re.search(bad, low, re.IGNORECASE):
            return False, f"Запрещенка: найдено '{bad}' — рекламировать нельзя (наркотики/казино/оружие/порно/пирамиды)"
    # Ссылка обязательна?
    if link:
        if not re.match(r'https?://', link):
            return False, "Ссылка должна начинаться с https://"
        # Проверка на подозрительные сокращалки — предупреждаем но не баним
        for sus in SUSPICIOUS_DOMAINS:
            if sus in link:
                # не баним, но помечаем для админа
                return True, f"Внимание: короткая ссылка {sus} — проверь админом"
    return True, "OK"

def create_ad_request(user_id, username, text, link="", photo_file_id=""):
    pending = load_json(PENDING_ADS, [])
    # Лимит 1 в день на юзера
    today = str(datetime.date.today())
    today_ads = [a for a in pending if a.get("user_id")==str(user_id) and a.get("date","").startswith(today)]
    if len(today_ads)>=1:
        return None, "Лимит: 1 заявка на рекламу в день. Попробуй завтра."

    ok, reason = check_ad_text(text, link)
    if not ok:
        return None, f"❌ Авто-модерация отклонила: {reason}"

    ad_id = f"ad_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{user_id}"
    entry = {
        "ad_id": ad_id,
        "user_id": str(user_id),
        "username": username,
        "text": text,
        "link": link,
        "photo_file_id": photo_file_id,
        "status": "pending_admin" if "Внимание" not in reason else "pending_admin_warning",
        "auto_check": reason,
        "date": datetime.datetime.now().isoformat(),
        "moderated_by": None
    }
    pending.append(entry)
    save_json(PENDING_ADS, pending)
    return entry, reason

def approve_ad(ad_id, admin_id):
    pending = load_json(PENDING_ADS, [])
    for ad in pending:
        if ad["ad_id"]==ad_id:
            ad["status"]="approved_pending_payment"
            ad["moderated_by"]=str(admin_id)
            ad["moderated_date"]=datetime.datetime.now().isoformat()
            save_json(PENDING_ADS, pending)
            return ad
    return None

def reject_ad(ad_id, admin_id, reason=""):
    pending = load_json(PENDING_ADS, [])
    for ad in pending:
        if ad["ad_id"]==ad_id:
            ad["status"]="rejected"
            ad["moderated_by"]=str(admin_id)
            ad["reject_reason"]=reason
            ad["moderated_date"]=datetime.datetime.now().isoformat()
            save_json(PENDING_ADS, pending)
            # лог
            log = load_json(ADS_LOG, [])
            log.append({**ad, "final_status":"rejected"})
            save_json(ADS_LOG, log)
            return ad
    return None

def mark_paid_and_posted(ad_id):
    pending = load_json(PENDING_ADS, [])
    for ad in pending:
        if ad["ad_id"]==ad_id:
            ad["status"]="posted"
            ad["posted_date"]=datetime.datetime.now().isoformat()
            save_json(PENDING_ADS, pending)
            log = load_json(ADS_LOG, [])
            log.append({**ad, "final_status":"posted"})
            save_json(ADS_LOG, log)
            return ad
    return None

if __name__=="__main__":
    # Тест
    ad, reason = create_ad_request(12345, "test", "Продаю курс по Photoshop — 50% скидка, 1500 инструментов в комплекте", "https://example.com/course")
    print(ad, reason)
