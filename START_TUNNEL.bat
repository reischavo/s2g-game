@echo off
chcp 65001 >nul
title Cloudflare Tunnel - s2ggame.com
color 0D

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         🌐 CLOUDFLARE TUNNEL BAŞLATILIYOR 🌐              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Domain: s2ggame.com
echo 🌐 Domain: www.s2ggame.com
echo.
echo 🚇 Tunnel başlatılıyor...
echo.

REM Doğru dizine geç
cd /d "%~dp0"

echo 📁 Çalışma dizini: %CD%
echo.

REM cloudflared.exe'nin varlığını kontrol et
if not exist "cloudflared.exe" (
    echo ❌ HATA: cloudflared.exe bulunamadı!
    echo.
    echo cloudflared.exe bu klasörde olmalı: %CD%
    echo.
    pause
    exit /b 1
)

echo ✅ cloudflared.exe bulundu!
echo.

cloudflared.exe tunnel run s2g-game

if errorlevel 1 (
    echo.
    echo ❌ Tunnel başlatılamadı!
    echo.
    echo Olası nedenler:
    echo 1. Config dosyası bulunamadı
    echo 2. Tunnel oluşturulmamış
    echo 3. Cloudflare girişi yapılmamış
    echo.
    echo Çözüm: CLOUDFLARE_SETUP_s2ggame.bat çalıştırın
    echo.
    pause
)
