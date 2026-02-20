@echo off
chcp 65001 >nul
title Cloudflare Tunnel - Manuel Başlatma
color 0D

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║      🌐 CLOUDFLARE TUNNEL - MANUEL BAŞLATMA 🌐            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Bu pencereyi AÇIK TUTUN!
echo.

cd /d "%~dp0"

echo 🔍 cloudflared.exe kontrol ediliyor...
if not exist "cloudflared.exe" (
    echo ❌ cloudflared.exe bulunamadı!
    echo.
    echo cloudflared.exe bu klasörde olmalı:
    echo %CD%
    echo.
    pause
    exit /b 1
)

echo ✅ cloudflared.exe bulundu!
echo.

echo 🔍 Config dosyası kontrol ediliyor...
if not exist "%USERPROFILE%\.cloudflared\config.yml" (
    echo ❌ Config dosyası bulunamadı!
    echo.
    echo Önce CLOUDFLARE_SETUP_s2ggame.bat çalıştırın.
    echo.
    pause
    exit /b 1
)

echo ✅ Config dosyası bulundu!
echo.

echo 🚇 Tunnel başlatılıyor...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Domain: https://s2ggame.com                               ║
echo ║  Domain: https://www.s2ggame.com                           ║
echo ║                                                             ║
echo ║  Durdurmak için: CTRL + C                                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

cloudflared.exe tunnel run s2g-game

pause
