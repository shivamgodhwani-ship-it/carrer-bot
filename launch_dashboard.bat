@echo off
echo Starting Career Bot Dashboard...
echo.
echo Dashboard will open at http://localhost:5000
echo Keep this window open while using the dashboard.
echo.
pip install flask flask-cors -q
python dashboard.py
pause
