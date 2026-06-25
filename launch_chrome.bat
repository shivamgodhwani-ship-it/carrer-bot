@echo off
echo Launching Chrome with remote debugging...
echo.
echo After Chrome opens:
echo 1. Log into Internshala
echo 2. Then run: python apply_bot.py
echo.
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome_debug"
echo Chrome launched! Log into Internshala then run apply_bot.py
pause
