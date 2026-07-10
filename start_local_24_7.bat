@echo off
REM START LOCAL 24/7 — Windows, без карты, без Fly.io, бот онлайн пока комп включен
REM Кидаешь этот .bat в папку с ботом и запускаешь 1 раз — дальше сам рестартует если упадет

:loop
echo [%date% %time%] Запускаю бота-кассу 24/7...
python bot_autonomous_v6.py
echo [%date% %time%] Бот упал или закрылся, рестарт через 5 сек...
timeout /t 5 /nobreak >nul
goto loop
