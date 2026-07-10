# ToolFarm PUCHKA v14 — 1525 инструментов + 2500 дизайнов + бот-касса 24/7 — ФИНАЛЬНАЯ ВЕРСИЯ

**Версия: v14 — 16/16 тестов OK — 10.07.2026 — актуальный и рабочий проект**

## Что внутри (максималка)
- 1525 SEO инструментов (x10 вариантов: -excel, -google-sheets, -online, -besplatno, -bez-registracii, -rf, -skachat, -2026, -dlya-raboty)
- 2500+ дизайнов: 500 insta, 500 stories, 300 yt thumbs, 200 визиток, 200 през, 300 VK/TG, 100 бренд-китов
- 18 платных паков: logo-pack-1000, icon-pack-500, prompts-mega-5000, biz-templates-200, code-snippets-1000, hooks-1000 и т.д.
- 2 недельных дропа + авто-генерация под тренды (niche_trending_fetcher + niche_content_autopilot)
- 3 видео Shorts mp4 с озвучкой gTTS + авто-заливка YouTube/TikTok
- Бот-касса 24/7: рефы ?r=ID (вирус), Stars оплата 150/79/199/200/500, подписка PRO Club 199 Stars/мес, реклама в канале с модерацией, фидбек + авто-добавление инструментов + авто-уведомления
- Дашборды: /stats/ публичный, /earnings/ приватный (ADMIN_ID), /advertise/ медиа-кит, /drops/, /designs/, /pro/
- Авто-постинг статей без рук: Telegra.ph без ключа (жирный бэклинк) + Medium/dev.to/Reddit если токены
- Авто-самореклама: Telegra.ph + Reddit + Twitter + VC.ru/Habr + видео
- Авто-лутинг: Stars >=1000 уведомление, CryptoBot USDT >=10 авто-вывод, Monetag >=$5 уведомление
- Деплой: GitHub Pages (сайт 24/7) + GitHub Actions (генерация каждый день 9:00 МСК) + Render.com (бот 24/7 без карты, без ПК) + Fly.io (опционально, с картой, без сна)

## Быстрый старт сегодня (30 мин, без карты, удаленно 24/7)

1. GitHub → New Repo `tool-farm-max` Public → Upload все файлы из этой папки кроме `dist/` → Commit
2. Actions → Enable workflows → Run workflow `V11 PUCHKA MAX AUTOPILOT` → Run → жди 4 мин зеленую галочку → Settings → Pages → Source: GitHub Actions → ссылка `https://ТВОЙ_НИК.github.io/tool-farm-max/` — 1525 инструментов
3. Telegram: @BotFather → /newbot → токен, канал публичный + приватный → @getidsbot ID каналов -100..., @userinfobot ADMIN_ID
4. GitHub → Settings → Secrets → `TG_BOT_TOKEN`, `TG_CHANNEL_ID`, `TG_PRIVATE_CHANNEL_ID`, `ADMIN_ID`, `GROQ_API_KEY` (опционально бесплатно console.groq.com)
5. `config.json` → DOMAIN, BOT_USERNAME, ADMIN_ID → Commit
6. Monetag.com → Add Website → твой github.io → Zone ID Tag + Push → в `config.json` MONETAG_ZONE + PUSH → Commit
7. Render.com → Sign Up через GitHub (без карты) → New → Web Service → Connect репу → Build `pip install -r requirements-bot.txt` → Start `python app.py` → Env Vars TG_BOT_TOKEN, ADMIN_ID, TG_CHANNEL_ID, BOT_USERNAME → Create → логи `polling...` → бот в ТГ /start отвечает 24/7 без ПК. Добавь UptimeRobot пинг на `/health` каждые 5 мин чтобы не спал.
8. Yandex Webmaster → Sitemap `.../sitemap.xml` (1527 URL)
9. Первый трафик сегодня: `zen_articles/` 3 статьи → dzen.ru, `self_promo_autopilot.py` уже запостил Telegra.ph, `promo_queue.json` 2-3 текста → Ответы Mail/VC/Habr, `dist/videos/` 3 mp4 → TikTok/YouTube Shorts
10. Капуста: `/stats/`, `/earnings/` (введи ADMIN_ID), бот `/earnings`, `sales_log.json`, Monetag Dashboard, TikTok Analytics

Полный детальный гайд до последнего клика: `FINAL_ALL_IN_ONE_TODAY.md` + `FINAL_FULL_AUTOPILOT_GUIDE_V14.md` + `RENDER_DEPLOY_NO_CARD.md` + `FINAL_REMOTE_24_7_GUIDE.md`

## Тесты
`python run_all_tests.py` → 16/16 OK

## Скачать
- `ToolFarm-PUCHKA-v14-FINAL.zip` — исходники (916KB)
- `ToolFarm-SITE-1525-ONLY.zip` — готовый сайт HTML (9.3MB)

## Деплой бота без карты
- Render.com (без карты, 2 мин) — см. `RENDER_DEPLOY_NO_CARD.md` — `render.yaml` + `app.py` + `requirements-bot.txt` + `.dockerignore`
- Fly.io (с картой, без сна) — `fly.toml` + `Dockerfile` + `.github/workflows/fly-deploy-bot.yml`

## Авто-генерация
- `content_factory.py` — 1000 лого, 500 иконок, 5000 промтов
- `product_generator.py` — 250 лого, 1000 промтов
- `design_factory.py` — 2100 дизайнов
- `creator_coding_factory.py` — 1000 сниппетов, 1000 хуков, 500 yt titles, 365 контент-план + 20 новых инструментов для кодеров/контентщиков
- `weekly_drop_factory.py` + `niche_content_autopilot.py` — недельные дропы под тренды
- `video_auto_factory.py` — 3 Shorts/день + `youtube_uploader.py` + `tiktok_uploader.py`
- `auto_article_poster.py` — Telegra.ph без ключа + Medium/dev.to
- `self_promo_autopilot.py` — 8 промо-текстов + Telegra.ph auto + Reddit
- `feedback_system.py` + `auto_tool_adder.py` + `feedback_notifier.py` — сбор фидбека → авто-добавление инструментов → уведомление
- `ads_manager.py` — покупка рекламы в канале с модерацией черного списка
- `stats_generator.py` + `media_kit_generator.py` + `advertiser_outreach.py` — дашборды + медиа-кит + 25 писем рекламодателям
- `auto_looting.py` + `auto_withdraw.py` — авто-лутинг Stars/CryptoBot/Monetag

Все в `.github/workflows/deploy.yml` — каждый день 9:00 МСК полный автопилот без твоего ПК.

