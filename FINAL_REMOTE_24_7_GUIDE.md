# FINAL REMOTE 24/7 — ВСЕ УДАЛЕННО, БЕЗ ТВОЕГО ПК, РАБОТАЕТ КРУГЛОСУТОЧНО
**Цель: 0₽, 0 лица, РФ, 0 локального компа — все на бесплатных серверах GitHub + Fly.io/Render. Настроил 1 раз за 1 час → потом только лутаешь с телефона.**

Ты сказал "буду запускать все удаленно 24/7, на компе локально запускать не буду" — переделал всю систему под удаленку.

---

## ЧТО ГДЕ РАБОТАЕТ УДАЛЕННО (без твоего ПК)

| Компонент | Где работает удаленно 24/7 | Бесплатно? | Работает в РФ? |
|-----------|---------------------------|------------|----------------|
| Сайт 1525 инструментов | GitHub Pages | Да, безлимит | Да |
| Авто-генерация 1500 страниц + 2500 дизайнов + 18 паков + 2 дропа + 3 видео + статьи + бэклинки | GitHub Actions (каждый день 9:00 МСК) | Да, 2000 минут/мес бесплатно | Да |
| Бот-касса (рефы + Stars оплата 150/79/199 + подписка + реклама + фидбек + авто-доставка) | **Fly.io** (Frankfurt) или **Render.com** или **PythonAnywhere** — 24/7 | Да, 3 VM бесплатно | Да, Frankfurt близко |
| Авто-постинг статей без рук | GitHub Actions → Telegra.ph API (без ключа) + Medium/dev.to если токены есть | Да | Да |
| Авто-заливка Shorts в YouTube/TikTok | GitHub Actions → YouTube Data API + TikTok API (если токены есть) | Да | Да |
| Авто-лутинг и статистика | GitHub Actions + бот → /stats/ + /earnings/ дашборды | Да | Да |

Твой ПК нужен только 1 раз для регистрации (можно даже с телефона через GitHub App + Codespaces — тоже удаленно).

---

## ПОШАГОВАЯ ИНСТРУКЦИЯ — ТОЛЬКО УДАЛЕННО 24/7 (1 час, 1 раз)

### Шаг 0: Аккаунты (5 мин, все с телефона можно)

1. **GitHub** https://github.com → Sign up (email)
2. **Telegram** — у тебя уже есть, нужен @BotFather и @getidsbot, @userinfobot (все в ТГ)
3. **Monetag** https://monetag.com → Sign up (РФ без VPN)
4. **Fly.io** (для бота 24/7, бесплатно, без твоего ПК) — https://fly.io → Sign up → можно через GitHub аккаунт → попросит карту для верификации (не спишет, просто проверка, можно виртуальную, РФ карты не принимает — нужен VPN + зарубежная виртуальная карта типа Pyypl/ PSTNET — если нет, используй Render.com ниже, там без карты)
5. **Render.com** (альтернатива Fly.io, без карты, работает в РФ) — https://render.com → Sign up через GitHub → бесплатно, без карты, бот будет спать 15 мин если нет трафика, но проснется при сообщении (для бота норм)
6. **PythonAnywhere** (еще альтернатива, без карты) — https://www.pythonanywhere.com → Sign Up Free — но always-on только в платном, в бесплатном только scheduled tasks каждый час (тоже ок для бота)

**Рекомендую для РФ без карты: Render.com — 2 мин, без карты, 24/7 с автопросыпанием.**

### Шаг 1: GitHub репа + Pages + Actions (3 мин, удаленно)

1. GitHub → New repository → Name: `tool-farm-max` → Public → Create
2. Upload files: нажми `uploading an existing file` → перетащи ВСЕ файлы из `passive-income-system/` **кроме `dist/` и `__pycache__`** → Commit
3. Actions → Enable workflows → Run workflow `V11 PUCHKA MAX AUTOPILOT` → Run (подожди 4 мин, зеленая галочка)
4. Settings → Pages → Source: GitHub Actions → через 2 мин появится ссылка `https://ТВОЙ_НИК.github.io/tool-farm-max/` — это твой сайт 1525 инструментов, уже в сети 24/7 без твоего ПК.

### Шаг 2: Telegram бот + каналы (3 мин, с телефона)

1. @BotFather → /newbot → имя `ToolFarmMaxBot` → юзернейм `toolfarmmax_ТВОЙ_НИК_bot` → токен скопируй
2. Создай канал публичный `toolfarm_max` → добавь бота в админы (все права)
3. Создай приватный канал `toolfarm_private` (для PRO Club) → добавь бота админом
4. Узнай ID: напиши в каждый канал "тест", перешли сообщение в @getidsbot → даст `-100...`
5. Узнай свой ADMIN_ID: @userinfobot → даст цифры

### Шаг 3: Secrets в GitHub (2 мин, удаленно)

GitHub → репа → Settings → Secrets and variables → Actions → New secret (по одному):

```
TG_BOT_TOKEN = токен из BotFather
TG_CHANNEL_ID = ID публичного канала -100...
TG_PRIVATE_CHANNEL_ID = ID приватного канала -100...
ADMIN_ID = твой цифровой ID
GROQ_API_KEY = gsk_... с console.groq.com (бесплатно, для AI генерации инструментов из фидбека, опционально)
```

### Шаг 4: config.json (2 мин, удаленно)

В репе открой `config.json` → Edit → вставь:

```json
{
  "DOMAIN": "https://ТВОЙ_НИК.github.io/tool-farm-max",
  "BOT_USERNAME": "toolfarmmax_ТВОЙ_НИК_bot",
  "ADMIN_ID": "12345678",
  "MONETAG_ZONE": "REPLACE_ME"
}
```

Commit → Actions сам пересоберет сайт с твоим доменом.

### Шаг 5: Monetag (5 мин, РФ, удаленно)

1. monetag.com → My Websites → Add Website → вставь твой github.io → Add
2. Даст 2 зоны: Tag + Push → вставь в `config.json` `MONETAG_ZONE` и `MONETAG_PUSH_ZONE` → Commit → реклама на всех 1525 страницах
3. Выплата: Settings → Payments → USDT TRC20 → адрес из Trust Wallet/Bybit → минимум $5 → BestChange → Сбер (РФ работает)

### Шаг 6: БОТ 24/7 УДАЛЕННО — БЕЗ ТВОЕГО ПК (5 мин, главный шаг)

**Вариант A — Render.com (рекомендую для РФ, без карты, 2 мин):**

1. https://render.com → Sign Up через GitHub → Dashboard → New → Background Worker → Connect твою репу `tool-farm-max` → Name: `toolfarm-bot` → Build Command: `pip install -r requirements.txt` → Start Command: `python bot_autonomous_v6.py` → Advanced → Add Env Var:
   - `TG_BOT_TOKEN` = токен
   - `ADMIN_ID` = твой ID
   - `TG_CHANNEL_ID` = ID публичного
   - `PYTHONUNBUFFERED` = 1
2. Create Worker → Render сам соберет Dockerfile и запустит бота 24/7. Логи смотри в Dashboard → Logs. Если бот спит (free tier спит через 15 мин без трафика) — первое сообщение в бота его разбудит за 10 сек (для ТГ бота это норм, т.к. сообщения редкие).

**Вариант B — Fly.io (мощнее, 24/7 без сна, но нужна карта для верификации, работает через VPN):**

1. Установи flyctl локально? Но ты хочешь без ПК — используй GitHub Codespaces: GitHub → твоя репа → Code → Codespaces → Create codespace → в терминале Codespaces:
```
curl -L https://fly.io/install.sh | sh
export FLYCTL_INSTALL="/home/codespace/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"
fly auth signup (или login)
fly launch --no-deploy (выбери Frankfurt fra, не деплой)
fly secrets set TG_BOT_TOKEN=xxx ADMIN_ID=yyy TG_CHANNEL_ID=zzz
fly deploy
```
2. Бот онлайн 24/7 без сна, 3 VM бесплатно, 160GB трафика. Логи: `fly logs`

**Вариант C — PythonAnywhere (без карты, но в бесплатном нет always-on, только hourly task — костыль):**
- pythonanywhere.com → Sign Up → Files → Upload `bot_autonomous_v6.py`, `config.json` и т.д. → Tasks → Create scheduled task → каждый час → `python /home/ты/bot_autonomous_v6.py` → бот будет проверять раз в час, не 24/7, но для продаж паков ок (юзер ждет до часа).

**Выбери 1 вариант — я рекомендую Render.com для старта (без карты, 2 мин).**

### Шаг 7: YouTube + TikTok — полная автономия без ПК (10 мин, 1 раз, тоже удаленно через Codespaces)

**YouTube Shorts авто-заливка (5 мин):**
1. https://console.cloud.google.com → Новый проект ToolFarm → Enable YouTube Data API v3
2. OAuth consent screen → External → Save
3. Credentials → Create → OAuth Client ID → Desktop App → Download JSON → сохрани как `credentials.json`
4. **Без ПК:** используй GitHub Codespaces: в Codespaces терминале:
```
pip install google-api-python-client google-auth-oauthlib -q
python youtube_uploader.py --auth
```
Откроется ссылка → скопируй в браузер (телефона/ПК) → логин Google → разрешить → создастся `token.json`
5. Закодируй для Actions:
```
cat credentials.json | base64 -w0 → Secret YOUTUBE_CREDENTIALS_JSON
cat token.json | base64 -w0 → Secret YOUTUBE_TOKEN_JSON
```
Теперь Actions каждый день: `video_auto_factory.py` (3 видео) → `youtube_uploader.py` → 3 Shorts в YouTube без твоего ПК.

**TikTok (10 мин, нужен аппрув 1-3 дня):**
1. https://developers.tiktok.com → Create app → Name ToolFarm → Add Login Kit + Content Posting API → Apply
2. Client Key/Secret → `tiktok_credentials.json`
3. В Codespaces: `python tiktok_uploader.py --auth` → следуй инструкции в файле → получишь `tiktok_token.json`
4. Base64 → Secrets `TIKTOK_CREDENTIALS_JSON`, `TIKTOK_TOKEN_JSON` → Actions заливает 3 видео/день в TikTok без ПК.

Без ключей — видео остаются в `dist/videos/` и `tiktok_log.json` пишет MOCK, для ручной заливки за 2 мин.

### Шаг 8: Авто-постинг статей без рук (уже работает)

- **Telegra.ph** — без ключа, уже постит автоматом через `self_promo_autopilot.py` → https://telegra.ph/... (жирный бэклинк, индекс за 2 часа). Ничего настраивать не надо — работает из коробки каждый день.
- **Medium/dev.to** — опционально: Medium token 1 мин (medium.com/me/settings → Integration tokens), dev.to token 30 сек (dev.to/settings/extensions) → Secrets `MEDIUM_TOKEN`, `DEVTO_TOKEN` → `auto_article_poster.py` постит 1 статью в день на Medium/dev.to с бэклинком.

### Шаг 9: Яндекс + Google (2 мин, удаленно)

- webmaster.yandex.ru → Добавить сайт → твой github.io → Sitemap → `.../sitemap.xml` (1527 URL)
- search.google.com/search-console → то же

### Шаг 10: Где чекать капусту — все удаленно с телефона

- **Сайт:** `.../stats/` — публичный дашборд (1525, 18 паков, 2 дропа, 3 фидбека, топ ниша, видео, реклама)
- **Сайт:** `.../earnings/` — введи ADMIN_ID → продажи Stars, подписчики, рефералы, реклама, график Chart.js, дропы, TikTok лог
- **Бот:** `/earnings` (только админ), `/stats`, `/balance`, `/drops`, `/buy_ad`, `/buy`
- **Monetag:** monetag.com Dashboard
- **TikTok:** Creator Tools → Analytics
- **YouTube:** studio.youtube.com → Analytics
- **GitHub Actions логи:** Actions → последний ран → TOOLS, VIDEOS, DROPS, FEEDBACK

### Шаг 11: Авто-лутинг — без захода в BotFather (почти)

`auto_looting.py` + `auto_withdraw.py` каждый день 9:10 МСК:
- Stars >=1000 → шлет тебе в ТГ "пора выводить в BotFather" (авто-вывод Stars по API невозможен — только руками 2 мин в @BotFather → Withdraw → TON)
- CryptoBot USDT >=10 → если указал `CRYPTOBOT_TOKEN` + `CRYPTOBOT_WITHDRAW_WALLET` + `CRYPTOBOT_WITHDRAW_USER_ID` → сам переводит USDT на твой кошелек без тебя

Настройка: @CryptoBot → /app → API Token → Secrets + Bybit USDT TRC20 адрес + твой TG ID.

После этого — полный автопилот без твоего ПК: GitHub Pages (сайт 24/7) + GitHub Actions (генерация 1500 + паки + дизайны + дропы + 3 видео + статьи + бэклинки каждый день) + Fly.io/Render (бот 24/7) + YouTube/TikTok API (заливка видео) + Monetag (деньги) + Stars (продажи паков/рекламы).

Ты только с телефона заходишь в `/earnings/` и лутаешь.

Чек-лист удаленного запуска (без ПК):
- [ ] GitHub репа + Pages + Actions зеленый
- [ ] Telegram бот + 2 канала + ID получены (все с телефона)
- [ ] Secrets в GitHub добавлены (TG_BOT_TOKEN, CHANNEL_ID, ADMIN_ID)
- [ ] config.json с DOMAIN и BOT_USERNAME закоммичен
- [ ] Monetag Zone вставлен
- [ ] Render.com worker создан, бот онлайн (логи показывают polling)
- [ ] Yandex Webmaster sitemap добавлен
- [ ] (Опционально) YouTube/TikTok/Medium/dev.to токены для полной автономии видео и статей

После чек-листа — все удаленно 24/7, без твоего компа. Потом только лутаешь.

Хочешь, сгенерю еще Dockerfile для Fly.io уже готовый + render.yaml уже есть — деплой в 1 клик?
