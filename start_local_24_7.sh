#!/bin/bash
# START LOCAL 24/7 — Linux/Mac, без карты, без Fly.io, бот онлайн пока комп включен
# chmod +x start_local_24_7.sh && ./start_local_24_7.sh

while true; do
  echo "[$(date)] Запускаю бота-кассу 24/7..."
  python3 bot_autonomous_v6.py
  echo "[$(date)] Бот упал, рестарт через 5 сек..."
  sleep 5
done
