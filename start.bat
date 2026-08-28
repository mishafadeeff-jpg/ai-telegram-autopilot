@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
title AI Telegram Channel Autopilot
echo ========================================================
echo Installing / verifying dependencies...
echo ========================================================
python -m pip install -r requirements.txt
echo.
echo ========================================================
echo Starting Autopilot in Continuous Mode...
echo ========================================================
python main.py
pause
