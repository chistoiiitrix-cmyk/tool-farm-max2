# Fly.io / Render / Railway — бот 24/7 удаленно, без твоего ПК, 0₽, работает в РФ
# Образ теперь легкий (~150MB вместо 500MB) — игнорим dist/ через .dockerignore

FROM python:3.11-slim

WORKDIR /app

# Системные зависимости для Pillow (лого) и т.д.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev zlib1g-dev libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-bot.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем только нужное для бота (dist не копируется из-за .dockerignore — боту не нужен сайт, только json логи)
COPY bot_autonomous_v6.py ads_manager.py feedback_system.py config.json ./
COPY *.json ./

# Создаем пустые json если нет
RUN touch referrals.json sales_log.json feedback.json pending_ads.json ads_log.json subscriptions.json looting_log.json tiktok_log.json promo_queue.json promo_log.json

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Healthcheck для Fly.io/Render — бот пишет в логи polling
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 CMD pgrep -f bot_autonomous_v6.py || exit 1

CMD ["python", "bot_autonomous_v6.py"]
