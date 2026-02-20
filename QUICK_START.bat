@echo off
chcp 65001 >nul
title S2G Game - Hızlı Başlangıç
color 0E

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         🎮 S2G GAME - HIZLI BAŞLANGIÇ 🎮                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo Bu script tüm kurulum adımlarını otomatik yapacak.
echo.
pause

echo.
echo ═══════════════════════════════════════════════════════════
echo  ADIM 1: KURULUM
echo ═══════════════════════════════════════════════════════════
call INSTALL.bat

if errorlevel 1 (
    echo.
    echo ❌ Kurulum başarısız!
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo  ADIM 2: ÖRNEK ÜRÜNLER EKLENİYOR
echo ═══════════════════════════════════════════════════════════
echo.
echo Örnek ürünler eklemek ister misiniz? (E/H)
set /p add_products="Seçiminiz: "

if /i "%add_products%"=="E" (
    echo.
    echo 📦 Örnek ürünler ekleniyor...
    python add_sample_products.py
    echo ✅ Örnek ürünler eklendi!
)

echo.
echo ═══════════════════════════════════════════════════════════
echo  ADIM 3: SUNUCU BAŞLATILIYOR
echo ═══════════════════════════════════════════════════════════
echo.
echo Sunucu başlatılıyor...
timeout /t 2 >nul

call START.bat
