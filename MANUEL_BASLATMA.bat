@echo off
chcp 65001 >nul
title S2G Game - Manuel Başlatma
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         🎮 S2G GAME - MANUEL BAŞLATMA 🎮                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Bu pencereyi AÇIK TUTUN!
echo.

cd /d "%~dp0"

echo 🚀 Flask sunucusu başlatılıyor...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Sunucu Adresi: http://localhost:5000                      ║
echo ║  Admin Panel:   http://localhost:5000/admin                ║
echo ║                                                             ║
echo ║  Durdurmak için: CTRL + C                                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

python app.py

pause
