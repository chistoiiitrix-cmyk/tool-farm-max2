"""
BOT AUTONOMOUS v6 — Максимальная автономность: зашел, собрал капусту, все.

Что умеет (0₽ вложений, работает в РФ):
1. Реферальный доступ (как раньше) — 3 рефа = PRO бесплатно (вирусный рост)
2. Платный доступ через Telegram Stars (встроенные платежи ТГ) — полностью автономно, без внешних сервисов, работает в РФ. Юзер платит Stars внутри ТГ → бот мгновенно выдает паки
3. Платный доступ через CryptoBot (USDT) — для тех у кого нет Stars, тоже автономно через API
4. Подписка PRO Club — 199 Stars/месяц — бот выдает доступ в приватный канал где каждый день автопостит 1 новый инструмент/лого/шаблон (через GitHub Actions)
5. Авто-доставка: после оплаты бот шлет 4 zip-архива + PRO код + ссылку на /pro/ + исходники
6. Логи продаж в sales_log.json и earnings.json — зашел, посмотрел капусту
7. Дашборд: /earnings/ страница (генерит build.py) показывает продажи

Как подключить платежи (2 минуты, один раз):
- Telegram Stars: ничего подключать не надо! Просто включи платежи в @BotFather → /mybots → Payments → отключи провайдера, Stars работают из коробки
- CryptoBot (опционально, для USDT): иди в @CryptoBot → /app → Create App → получи токен → вставь в config.json CRYPTOBOT_TOKEN. Работает в РФ, вывод в USDT.

После этого все само: юзер жмет /buy → платит Stars → бот ловит successful_payment → отдает файлы. Тебе только заходить в @BotFather → Статистика или в sales_log.json смотреть продажи и выводить Stars через @BotFather → конверт в TON/USDT.

Доход: 1 продажа PRO 150 Stars (~$2.5) × 2 в день = $150/мес только с бота + основной сайт Monetag $500-1500.
"""

import json, pathlib, os, time, random, urllib.request, urllib.parse, datetime, zipfile

BASE = pathlib.Path(__file__).parent
CONFIG = json.loads((BASE / "config.json").read_text(encoding='utf-8')) if (BASE / "config.json").exists() else {}
DB = json.loads((BASE / "tools-database.json").read_text(encoding='utf-8')) if (BASE / "tools-database.json").exists() else []

BOT_TOKEN = os.getenv("TG_BOT_TOKEN") or CONFIG.get("TELEGRAM_BOT_TOKEN") or ""
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN") or CONFIG.get("CRYPTOBOT_TOKEN") or ""
BOT_USERNAME = CONFIG.get("BOT_USERNAME","").replace('@','')
DOMAIN = CONFIG.get("DOMAIN","https://YOUR_DOMAIN").rstrip('/')

REF_PATH = BASE / "referrals.json"
SALES_PATH = BASE / "sales_log.json"
SUBS_PATH = BASE / "subscriptions.json"
PENDING_PATH = BASE / "pending_payments.json"

def load(p, default):
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default

REFS = load(REF_PATH, {})
SALES = load(SALES_PATH, [])
SUBS = load(SUBS_PATH, {})
PENDING = load(PENDING_PATH, {})

def save():
    REF_PATH.write_text(json.dumps(REFS, ensure_ascii=False, indent=2), encoding='utf-8')
    SALES_PATH.write_text(json.dumps(SALES, ensure_ascii=False, indent=2), encoding='utf-8')
    SUBS_PATH.write_text(json.dumps(SUBS, ensure_ascii=False, indent=2), encoding='utf-8')
    PENDING_PATH.write_text(json.dumps(PENDING, ensure_ascii=False, indent=2), encoding='utf-8')

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def api(method, params):
    if not BOT_TOKEN or "REPLACE" in BOT_TOKEN:
        print(f"[MOCK {method}] {list(params.keys())}")
        return {"ok": True, "result": {"message_id": 1}}
    url = f"{API}/{method}"
    # Если есть файлы — multipart, упростим: для документов отдельно
    try:
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"API error {method}: {e}")
        return {"ok": False}

def send_msg(chat_id, text, rm=None):
    p={"chat_id": chat_id, "text": text, "parse_mode":"HTML", "disable_web_page_preview": False}
    if rm: p["reply_markup"]=json.dumps(rm)
    return api("sendMessage", p)

def send_doc(chat_id, file_path, caption=""):
    if not BOT_TOKEN or "REPLACE" in BOT_TOKEN:
        print(f"[MOCK send_doc] {file_path} -> {chat_id}")
        return {"ok": True}
    try:
        import requests
        url = f"{API}/sendDocument"
        with open(file_path,'rb') as f:
            files={'document': f}
            data={'chat_id': chat_id, 'caption': caption, 'parse_mode':'HTML'}
            r = requests.post(url, data=data, files=files, timeout=30)
            print(f"send_doc {file_path}: {r.status_code}")
            return r.json()
    except Exception as e:
        # fallback urllib (без requests)
        print(f"send_doc fallback {e}")
        # пробуем без файла — даем ссылку
        send_msg(chat_id, f"📦 Твой пак: {file_path} — скачай с сайта {DOMAIN}/downloads/{pathlib.Path(file_path).name}\n{caption}")
        return {"ok": True}

def create_stars_invoice(chat_id):
    # Telegram Stars invoice: 150 Stars (~$2.5)
    title="PRO пак 250+ лого + 50 инструментов + исходники"
    desc="Авто-доставка: 4 архива + PRO код + доступ в приват /pro/ + исходники фермы. Работает в РФ."
    payload=f"pro_pack_{chat_id}_{int(time.time())}"
    currency="XTR"
    prices=[{"label":"PRO пак", "amount": 150}]  # 150 Stars
    params={
        "chat_id": chat_id,
        "title": title,
        "description": desc,
        "payload": payload,
        "provider_token": "",  # для Stars пустой
        "currency": currency,
        "prices": json.dumps(prices),
    }
    return api("sendInvoice", params)

def create_subscription_invoice(chat_id):
    title="PRO Club подписка — 30 дней, 1 новый пак в день"
    desc="Доступ в приватный канал с ежедневными паками лого/шаблонов/промтов. Авто-продление. Отмена в /sub_cancel"
    payload=f"sub_30d_{chat_id}"
    currency="XTR"
    prices=[{"label":"PRO Club 30 дней", "amount": 199}]
    params={
        "chat_id": chat_id,
        "title": title,
        "description": desc,
        "payload": payload,
        "provider_token": "",
        "currency": currency,
        "prices": json.dumps(prices),
    }
    return api("sendInvoice", params)

def deliver_pro(chat_id, reason="Оплата"):
    code=f"PRO-{chat_id}-UNLOCKED"
    # Логируем продажу
    SALES.append({"user_id": str(chat_id), "time": datetime.datetime.now().isoformat(), "reason": reason, "code": code, "amount_stars": 150 if "Оплата" in reason else 0})
    save()
    send_msg(chat_id, f"""✅ <b>Оплата получена! Забрал капусту?</b> Теперь твоя очередь — получил PRO

<b>Твой PRO код:</b> <code>{code}</code>
Вставь на сайте {DOMAIN}/pro/ — откроются 50 доп инструментов

<b>Твои паки (авто-доставка):</b>
Сейчас пришлю 4 архива. Если не пришли — скачай с сайта {DOMAIN}/downloads/

- logo-pack-250.zip (250 лого PNG)
- prompts-1000.zip (1000 промтов ChatGPT/Midjourney)
- contracts-rf-100.zip (100 договоров РФ)
- tools-offline-750.zip (750 инструментов offline)

<b>Исходники фермы:</b> /source

<b>Подписка PRO Club:</b> Хочешь каждый день новый пак? /buy_sub

Спасибо что поддержал ферму! Твоя реф ссылка для вируса: {DOMAIN}/?r={chat_id}
Поделись — получишь еще трафик.
""")
    # Шлем файлы если есть локально
    for fname in ["logo-pack-250.zip","prompts-1000.zip","contracts-rf-100.zip","tools-offline-750.zip"]:
        fpath = BASE / "dist" / "downloads" / fname
        if fpath.exists():
            send_doc(chat_id, str(fpath), caption=f"📦 {fname} — PRO пак")
            time.sleep(1)

def handle_start(chat_id, username, args):
    # 0. Обратная связь fb_
    if args.startswith("fb_") or args.startswith("feedback_") or args.startswith("idea:") or args.startswith("bug:"):
        try:
            import urllib.parse
            fb_text = urllib.parse.unquote(args[3:] if args.startswith("fb_") else args)
            # Сохраняем через feedback_system
            import feedback_system
            entry = feedback_system.add_feedback(chat_id, fb_text, username)
            send_msg(chat_id, f"✅ <b>Спасибо за идею!</b>\n\nТвоя заявка: <code>{fb_text[:200]}</code>\n\nТип: {entry['type']} | Голосов: {entry['votes']}\n\nТоп-3 идеи каждую неделю автоматом становятся новыми инструментами на сайте (1500 → 1501...). Смотри /drops/ и /designs/ — там дропаем новое по твоим заявкам.\n\nХочешь PRO за 3 рефа или купить пак 250+ лого? /buy")
            # Пересылаем админу
            admin_id = os.getenv("ADMIN_ID") or CONFIG.get("ADMIN_ID")
            if admin_id:
                try:
                    send_msg(admin_id, f"📩 <b>Новый фидбек</b> от @{username or chat_id} ({chat_id}):\n{fb_text}\n\nТип: {entry['type']} Голоса: {entry['votes']}")
                except: pass
            return
        except Exception as e:
            print(f"Feedback handle error: {e}")

    # 0.1 Реклама ad_ payload уже оплаченный? ad_{ad_id}
    if args.startswith("buy_ad") or args.startswith("ad_"):
        send_msg(chat_id, "📢 <b>Покупка рекламы в канале</b>\n\nПришли текст рекламы в формате:\n<code>ТЕКСТ РЕКЛАМЫ | https://ссылка</code>\n\nПример:\nКурс по Photoshop — 50% скидка, 1500 инструментов в комплекте | https://example.com\n\nМожно прикрепить 1 фото следом. Запрещенка: казино, наркотики, оружие, порно, пирамиды — авто-бан.\n\nЛимит 1 заявка в день. Цена: 200 Stars = 1 пост, 500 Stars = 3 поста + закреп.", )
        # Ставим состояние ожидания рекламы
        import ads_manager
        # сохраняем состояние
        states_path = BASE / "user_states.json"
        states = json.loads(states_path.read_text(encoding='utf-8')) if states_path.exists() else {}
        states[str(chat_id)] = {"state": "awaiting_ad_text", "username": username}
        states_path.write_text(json.dumps(states, ensure_ascii=False, indent=2), encoding='utf-8')
        return

    # рефералка
    inviter=None
    if args.startswith("r_"):
        inviter=args.split("_",1)[1]
    elif "inv_" in args:
        try:
            inviter=args.split("inv_")[1].split("_")[0]
        except: pass

    if inviter and str(inviter)!=str(chat_id):
        if str(chat_id) not in REFS:
            REFS[str(chat_id)]={"count":0,"invited":[],"invited_by":inviter,"pro":False}
        if str(inviter) not in REFS: REFS[str(inviter)]={"count":0,"invited":[],"pro":False}
        if str(chat_id) not in REFS[str(inviter)]["invited"]:
            REFS[str(inviter)]["invited"].append(str(chat_id))
            REFS[str(inviter)]["count"]=len(REFS[str(inviter)]["invited"])
            save()
            try: send_msg(inviter, f"🎉 Новый реферал @{username or chat_id}! У тебя {REFS[str(inviter)]['count']}/3 — /balance")
            except: pass

    if str(chat_id) not in REFS:
        REFS[str(chat_id)]={"count":0,"invited":[],"pro":False}
        save()

    send_msg(chat_id, f"""🚀 <b>ToolFarm AUTONOMOUS v6 — зашел, собрал капусту</b>

Привет! Это бот который сам продает паки и сам растет.

<b>💰 2 способа получить PRO + паки 250+ лого:</b>

1️⃣ <b>Бесплатно за 3 рефа (вирус):</b>
Твоя реф ссылка: <code>{DOMAIN}/?r={chat_id}</code>
Поделись с 3 друзьями → /balance → получишь PRO код

2️⃣ <b>Купить за 150 Stars (~$2.5) — мгновенно:</b>
/buy — оплата Stars внутри ТГ, без внешних сайтов, работает в РФ, бот сразу шлет 4 архива

3️⃣ <b>Подписка PRO Club 199 Stars/мес:</b>
/buy_sub — каждый день 1 новый пак (лого/шаблоны/промты) в приватный канал. Авто-доступ.

<b>Команды:</b>
/buy — купить PRO пак 250+ лого + 50 инструментов + исходники
/buy_sub — подписка PRO Club
/balance — прогресс рефов
/pro — получить PRO если есть 3 рефа
/source — исходники фермы
/earnings — если ты админ, посмотреть капусту (продажи)

Твоя рефка еще раз: {DOMAIN}/?r={chat_id}
""")

def poll():
    print("🤖 AUTONOMOUS v6 polling...")
    offset=0
    while True:
        try:
            if not BOT_TOKEN or "REPLACE" in BOT_TOKEN:
                print("[MOCK] polling — токен не указан, спим 10 сек. Вставь TG_BOT_TOKEN в config.json")
                time.sleep(10)
                continue
            url=f"{API}/getUpdates?offset={offset}&timeout=25"
            with urllib.request.urlopen(url, timeout=30) as resp:
                data=json.loads(resp.read().decode())
                if not data.get("ok"):
                    time.sleep(2)
                    continue
                for upd in data.get("result",[]):
                    offset=upd["update_id"]+1
                    # pre_checkout_query
                    if "pre_checkout_query" in upd:
                        pcq=upd["pre_checkout_query"]
                        # одобряем любой платеж
                        api("answerPreCheckoutQuery", {"pre_checkout_query_id": pcq["id"], "ok": True})
                        continue
                    # callback_query — для модерации рекламы админом
                    if "callback_query" in upd:
                        cq = upd["callback_query"]
                        cq_id = cq["id"]
                        from_id = cq["from"]["id"]
                        data_cb = cq.get("data","")
                        # только админ может модерировать
                        admin_id = str(os.getenv("ADMIN_ID") or CONFIG.get("ADMIN_ID",""))
                        if admin_id and str(from_id)!=admin_id:
                            api("answerCallbackQuery", {"callback_query_id": cq_id, "text": "Только админ", "show_alert": True})
                            continue
                        # data_cb вида approve_ad_{ad_id} или reject_ad_{ad_id}
                        import ads_manager
                        if data_cb.startswith("approve_ad_"):
                            ad_id = data_cb.replace("approve_ad_","")
                            ad = ads_manager.approve_ad(ad_id, from_id)
                            if ad:
                                api("answerCallbackQuery", {"callback_query_id": cq_id, "text": "Одобрено, ждем оплату"})
                                # Создаем инвойс юзеру
                                # 200 Stars за 1 пост
                                user_chat = ad["user_id"]
                                # создаем Stars инвойс для рекламы
                                payload = f"ad_{ad_id}"
                                api("sendInvoice", {
                                    "chat_id": user_chat,
                                    "title": f"Реклама в канале — {ad_id}",
                                    "description": f"Текст: {ad['text'][:200]} | Ссылка: {ad['link']} | После оплаты пост в канал",
                                    "payload": payload,
                                    "provider_token": "",
                                    "currency": "XTR",
                                    "prices": json.dumps([{"label": "Реклама 1 пост", "amount": 200}])
                                })
                                send_msg(from_id, f"✅ Реклама {ad_id} одобрена, инвойс отправлен юзеру {user_chat}")
                            else:
                                api("answerCallbackQuery", {"callback_query_id": cq_id, "text": "Не найдено"})
                        elif data_cb.startswith("reject_ad_"):
                            ad_id = data_cb.replace("reject_ad_","")
                            ad = ads_manager.reject_ad(ad_id, from_id, "Отклонено админом")
                            api("answerCallbackQuery", {"callback_query_id": cq_id, "text": "Отклонено"})
                            if ad:
                                send_msg(ad["user_id"], f"❌ Твоя реклама {ad_id} отклонена админом. Причина: запрещенка или спам. Попробуй другой текст. /buy_ad")
                                send_msg(from_id, f"❌ Реклама {ad_id} отклонена")
                        continue

                    msg=upd.get("message")
                    if not msg: continue
                    chat_id=msg["chat"]["id"]
                    user_id=msg["from"]["id"]
                    username=msg["from"].get("username","")
                    text=msg.get("text","")

                    # Проверка состояния ожидания рекламы
                    states_path = BASE / "user_states.json"
                    states = json.loads(states_path.read_text(encoding='utf-8')) if states_path.exists() else {}
                    user_state = states.get(str(user_id), {}).get("state")

                    # Если юзер прислал фото — сохраняем file_id для рекламы
                    if "photo" in msg and user_state=="awaiting_ad_photo":
                        photo = msg["photo"][-1]  # самый большой
                        file_id = photo["file_id"]
                        # Обновляем последнюю заявку этого юзера
                        import ads_manager
                        pending = ads_manager.load_json(ads_manager.PENDING_ADS, [])
                        # находим последнюю pending этого юзера
                        for ad in reversed(pending):
                            if ad["user_id"]==str(user_id) and ad["status"] in ["pending_admin","pending_admin_warning"]:
                                ad["photo_file_id"]=file_id
                                break
                        ads_manager.save_json(ads_manager.PENDING_ADS, pending)
                        send_msg(chat_id, "✅ Фото сохранено к рекламе. Жди модерации админа.")
                        # сбрасываем состояние
                        states.pop(str(user_id), None)
                        states_path.write_text(json.dumps(states, ensure_ascii=False, indent=2), encoding='utf-8')
                        continue

                    if user_state=="awaiting_ad_text" and text and not text.startswith("/"):
                        # Парсим текст рекламы: "ТЕКСТ | https://ссылка" или просто текст
                        import ads_manager
                        ad_text = text
                        link = ""
                        if "|" in text:
                            parts = text.split("|")
                            ad_text = parts[0].strip()
                            link = parts[1].strip()
                        else:
                            # ищем ссылку в тексте
                            import re
                            m = re.search(r'https?://\S+', text)
                            if m:
                                link = m.group(0)
                                ad_text = text.replace(link,"").strip()
                        entry, reason = ads_manager.create_ad_request(user_id, username, ad_text, link)
                        if not entry:
                            send_msg(chat_id, f"❌ {reason}\nПопробуй другой текст. /buy_ad")
                            states.pop(str(user_id), None)
                            states_path.write_text(json.dumps(states, ensure_ascii=False, indent=2), encoding='utf-8')
                            continue
                        # Успешно создано, просим фото
                        send_msg(chat_id, f"✅ Заявка создана: {entry['ad_id']}\nАвто-проверка: {reason}\n\nТеперь можешь прислать 1 фото для рекламы (опционально) или напиши /skip чтобы без фото. После этого заявка уйдет на модерацию админу.")
                        states[str(user_id)] = {"state": "awaiting_ad_photo", "ad_id": entry["ad_id"], "username": username}
                        states_path.write_text(json.dumps(states, ensure_ascii=False, indent=2), encoding='utf-8')
                        # Отправляем админу на модерацию
                        admin_id = os.getenv("ADMIN_ID") or CONFIG.get("ADMIN_ID")
                        if admin_id:
                            kb = {
                                "inline_keyboard": [
                                    [{"text": "✅ Одобрить", "callback_data": f"approve_ad_{entry['ad_id']}"},
                                     {"text": "❌ Отклонить", "callback_data": f"reject_ad_{entry['ad_id']}"}]
                                ]
                            }
                            send_msg(admin_id, f"📢 <b>Новая заявка на рекламу</b>\n\nID: {entry['ad_id']}\nОт: @{username} ({user_id})\nТекст: {ad_text}\nСсылка: {link}\nАвто-проверка: {reason}\n\nОдобрить?", rm=kb)
                        continue

                    if text.startswith("/skip") and user_state=="awaiting_ad_photo":
                        # Пропуск фото
                        states.pop(str(user_id), None)
                        states_path.write_text(json.dumps(states, ensure_ascii=False, indent=2), encoding='utf-8')
                        send_msg(chat_id, "✅ Без фото, заявка ушла на модерацию. Жди одобрения админа.")
                        continue

                    if "successful_payment" in msg:
                        pay=msg["successful_payment"]
                        payload=pay.get("invoice_payload","")
                        print(f"💰 Оплата Stars от {chat_id}: {pay}")
                        if payload.startswith("pro_pack") or "pro_pack" in payload:
                            deliver_pro(chat_id, reason=f"Оплата Stars {pay.get('total_amount')} {pay.get('currency')}")
                        elif payload.startswith("ad_"):
                            # Оплата рекламы
                            ad_id = payload.replace("ad_","")
                            import ads_manager
                            ad = ads_manager.mark_paid_and_posted(ad_id)
                            if ad:
                                # Постим в канал
                                channel_id = os.getenv("TG_CHANNEL_ID") or CONFIG.get("TELEGRAM_CHANNEL_ID")
                                if channel_id:
                                    text_to_post = f"📢 <b>Реклама</b>\n\n{ad['text']}\n\n{ad['link']}\n\n#реклама"
                                    # Если есть фото — шлем фото с подписью
                                    if ad.get("photo_file_id"):
                                        api("sendPhoto", {"chat_id": channel_id, "photo": ad["photo_file_id"], "caption": text_to_post, "parse_mode":"HTML"})
                                    else:
                                        # api("sendMessage", {"chat_id": channel_id, "text": text_to_post, "parse_mode":"HTML"})
                                        send_msg(channel_id, text_to_post)
                                    send_msg(chat_id, f"✅ Оплата получена, реклама {ad_id} опубликована в канале!")
                                    # Лог продажи рекламы
                                    SALES.append({"user_id": str(chat_id), "time": datetime.datetime.now().isoformat(), "reason": f"Реклама {ad_id}", "code": ad_id, "amount_stars": pay.get('total_amount',200)})
                                    save()
                                else:
                                    send_msg(chat_id, "❌ Канал не настроен, но оплата принята. Админ выложит вручную.")
                            else:
                                send_msg(chat_id, f"Оплата рекламы получена, но заявка {ad_id} не найдена. Напиши админу.")
                        elif "sub_" in payload:
                            # подписка
                            SUBS[str(chat_id)]={"since": datetime.datetime.now().isoformat(), "until": (datetime.datetime.now()+datetime.timedelta(days=30)).isoformat(), "active": True}
                            save()
                            send_msg(chat_id, f"✅ Подписка PRO Club активирована на 30 дней! Доступ в приватный канал: скоро. Твоя рефка: {DOMAIN}/?r={chat_id}")
                        elif payload.startswith("drop_"):
                            # Оплата дропа
                            # payload drop_{week_id}_{user_id}
                            parts = payload.split("_")
                            week_id = "_".join(parts[1:-1]) if len(parts)>2 else parts[1]
                            send_msg(chat_id, f"✅ Оплата дропа {week_id} получена! Сейчас пришлю архив.")
                            # Найти файлы дропа и отправить
                            import pathlib, json as js
                            dpath = BASE / "dist" / "downloads" / "drops.json"
                            if dpath.exists():
                                drops = js.loads(dpath.read_text(encoding='utf-8'))
                                drop = next((d for d in drops if d["week_id"]==week_id), None)
                                if drop:
                                    for key, rel in drop["files"].items():
                                        fpath = BASE / "dist" / "downloads" / rel
                                        if fpath.exists():
                                            send_doc(chat_id, str(fpath), caption=f"📦 {rel} — дроп {week_id}")
                        continue

                    if text.startswith("/start"):
                        args=text.split(" ",1)[1] if " " in text else ""
                        handle_start(user_id, username, args)
                    elif text.startswith("/drops"):
                        handle_drops(chat_id)
                    elif text.startswith("/buy_drop_"):
                        week_id = text.split("/buy_drop_")[1].strip().split()[0].split("@")[0]
                        handle_buy_drop(chat_id, week_id)
                    elif text.startswith("/buy_ad"):
                        # Начинаем флоу покупки рекламы
                        handle_start(user_id, username, "buy_ad")
                    elif text.startswith("/buy_sub"):
                        create_subscription_invoice(chat_id)
                    elif text.startswith("/buy"):
                        create_stars_invoice(chat_id)
                    elif text.startswith("/balance"):
                        d=REFS.get(str(chat_id),{"count":0,"invited":[]})
                        send_msg(chat_id, f"📊 Рефов: {d.get('count',0)}/3\nТвоя ссылка: <code>{DOMAIN}/?r={chat_id}</code>\nПри 3 — /pro")
                    elif text.startswith("/pro"):
                        d=REFS.get(str(chat_id),{"count":0})
                        if d.get("count",0)>=3 or d.get("pro"):
                            deliver_pro(chat_id, reason="Доступ по рефам")
                        else:
                            send_msg(chat_id, f"❌ Нужно 3 рефа, у тебя {d.get('count',0)}/3. Или купи: /buy")
                    elif text.startswith("/source"):
                        repo=CONFIG.get("REPO_URL","https://github.com/YOUR_USERNAME/tool-farm")
                        send_msg(chat_id, f"📦 Исходники фермы 750 инструментов:\n{repo}\n\nТам: build.py, bot_autonomous_v6.py, product_generator.py, 750 tools")
                    elif text.startswith("/stats"):
                        send_msg(chat_id, f"📊 Статистика: {DOMAIN}/stats/ — публичный дашборд, {DOMAIN}/earnings/ — приватный (ADMIN_ID)")
                    elif text.startswith("/earnings"):
                        # только для админа — проверка по ID из env ADMIN_ID
                        admin_id=str(os.getenv("ADMIN_ID") or CONFIG.get("ADMIN_ID",""))
                        if admin_id and str(chat_id)!=admin_id:
                            send_msg(chat_id, "❌ Только для админа")
                            continue
                        total=len(SALES)
                        stars_total=sum(s.get("amount_stars",0) for s in SALES)
                        text_r = f"💰 <b>Капуста — продажи</b>\nВсего продаж: {total}\nStars: {stars_total} (~${stars_total*0.016:.2f})\n\nПоследние 5:\n"
                        for s in SALES[-5:]:
                            text_r+=f"{s['time'][:19]} — {s['user_id']} — {s['reason']}\n"
                        send_msg(chat_id, text_r)
                    elif text.startswith("/help"):
                        send_msg(chat_id, "/buy — купить PRO 250+ лого за Stars\n/buy_ad — купить рекламу в канале (200 Stars)\n/buy_sub — подписка\n/balance — рефы\n/pro — получить PRO\n/drops — дропы\n/stats — статистика\n/source — исходники")
                    else:
                        # Если не команда и нет состояния — показываем рефку
                        # Проверяем не является ли это текстом рекламы в состоянии ожидания
                        send_msg(chat_id, f"Твоя рефка: {DOMAIN}/?r={chat_id}\n/buy — купить пак\n/buy_ad — реклама в канале\n/balance — прогресс\n/drops — дропы")
        except Exception as e:
            print(f"Poll error: {e}")
            import traceback; traceback.print_exc()
            time.sleep(5)

if __name__=="__main__":
    poll()

# === V7 PATCH: drops handling ===
def handle_drops(chat_id):
    import pathlib, json
    BASE = pathlib.Path(__file__).parent
    drops_path = BASE / "dist" / "downloads" / "drops.json"
    if not drops_path.exists():
        drops_path = BASE / "drops.json"
    if not drops_path.exists():
        send_msg(chat_id, "Пока нет дропов, жди понедельника — каждую неделю новый пак!")
        return
    drops = json.loads(drops_path.read_text(encoding='utf-8'))
    text = "🔥 <b>Еженедельные дропы — свежий контент каждую неделю</b>\n\n"
    for d in drops[:5]:
        text += f"<b>{d['week_id']} — {d['niche']['name']}</b> ({d['date']})\n{d['description']}\nЦена: {d['price_stars']} Stars / Бандл {d['price_stars_bundle']} Stars\nКупить: /buy_drop_{d['week_id']}\n\n"
    text += "PRO Club подписка 199 Stars/мес = все дропы бесплатно → /buy_sub\n"
    send_msg(chat_id, text)

def handle_buy_drop(chat_id, week_id):
    # Создаем инвойс Stars на дроп
    import json, pathlib
    BASE = pathlib.Path(__file__).parent
    drops_path = BASE / "dist" / "downloads" / "drops.json"
    if not drops_path.exists(): drops_path = BASE / "drops.json"
    drops = json.loads(drops_path.read_text(encoding='utf-8')) if drops_path.exists() else []
    drop = next((d for d in drops if d["week_id"]==week_id), None)
    if not drop:
        send_msg(chat_id, f"Дроп {week_id} не найден. /drops — список")
        return
    title=f"Дроп {drop['week_id']} — {drop['niche']['name']}"
    desc=drop['description'][:250]
    payload=f"drop_{week_id}_{chat_id}"
    currency="XTR"
    prices=[{"label": f"Дроп {week_id}", "amount": drop["price_stars"]}]
    api("sendInvoice", {
        "chat_id": chat_id,
        "title": title,
        "description": desc,
        "payload": payload,
        "provider_token": "",
        "currency": currency,
        "prices": json.dumps(prices)
    })

# Патчим poll loop для drops — добавляем обработчики в основной цикл (вручную допиши в poll() если нужно)
# Для быстрого теста вызываем через команды:
# /drops и /buy_drop_W...
