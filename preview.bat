@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
title AI Telegram Autopilot - Preview Mode
python main.py --dry-run
pause
