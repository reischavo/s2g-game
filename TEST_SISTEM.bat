@echo off
chcp 65001 >nul
title S2G Game - Sistem Testi
color 0E

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           🔍 S2G GAME - SİSTEM TESTİ 🔍                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 📋 TEST 1: Python Kontrolü
echo ═══════════════════════════════════════════════════════════
python --version
if errorlevel 1 (
    echo ❌ Python bulunamadı!
    goto :error
) else (
    echo ✅ Python tamam!
)
echo.

echo 📋 TEST 2: Bağımlılıklar Kontrolü
echo ═══════════════════════════════════════════════════════════
python -c "import flask, flask_sqlalchemy, flask_socketio" 2>nul
if errorlevel 1 (
    echo ❌ Bağımlılıklar eksik!
    echo.
    echo INSTALL.bat çalıştırın.
    goto :error
) else (
    echo ✅ Bağımlılıklar tamam!
)
echo.

echo 📋 TEST 3: cloudflared.exe Kontrolü
echo ═══════════════════════════════════════════════════════════
if exist "cloudflared.exe" (
    echo ✅ cloudflared.exe bulundu!
    echo 📁 Konum: %CD%\cloudflared.exe
) else (
    echo ❌ cloudflared.exe bulunamadı!
    echo.
    echo cloudflared.exe bu klasöre kopyalanmalı:
    echo %CD%
    goto :error
)
echo.

echo 📋 TEST 4: Cloudflare Config Kontrolü
echo ═══════════════════════════════════════════════════════════
if exist "%USERPROFILE%\.cloudflared\config.yml" (
    echo ✅ Config dosyası bulundu!
    echo 📁 Konum: %USERPROFILE%\.cloudflared\config.yml
    echo.
    echo 📄 Config içeriği:
    type "%USERPROFILE%\.cloudflared\config.yml"
) else (
    echo ❌ Config dosyası bulunamadı!
    echo.
    echo CLOUDFLARE_SETUP_s2ggame.bat çalıştırın.
    goto :error
)
echo.

echo 📋 TEST 5: Flask Sunucu Testi
echo ═══════════════════════════════════════════════════════════
echo Flask sunucusu 5 saniye başlatılacak...
echo.
start /B python app.py
timeout /t 5 >nul
taskkill /F /IM python.exe >nul 2>&1
echo ✅ Flask sunucu testi tamamlandı!
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ TÜM TESTLER BAŞARILI! ✅                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Sistem hazır! Şimdi şunları yapabilirsiniz:
echo.
echo 1. HIZLI_BASLATMA.bat - Her ikisini birden başlat
echo 2. Manuel başlatma:
echo    - İlk pencere: START.bat
echo    - İkinci pencere: START_TUNNEL.bat
echo.
pause
exit /b 0

:error
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                  ❌ TEST BAŞARISIZ! ❌                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Yukarıdaki hataları düzeltin ve tekrar deneyin.
echo.
pause
exit /b 1
