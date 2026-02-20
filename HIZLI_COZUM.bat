@echo off
chcp 65001 >nul
title S2G Game - Hızlı Çözüm
color 0C

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           🔧 S2G GAME - HIZLI ÇÖZÜM 🔧                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Bu script yaygın sorunları otomatik çözer.
echo.
pause

echo.
echo 🔍 SORUN TESPİTİ YAPILIYOR...
echo.

REM 1. cloudflared.exe kontrolü
if not exist "cloudflared.exe" (
    echo ❌ SORUN BULUNDU: cloudflared.exe yok!
    echo.
    echo 📥 cloudflared.exe'yi indirip bu klasöre kopyalamanız gerekiyor.
    echo.
    echo İndirme linki:
    echo https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe
    echo.
    echo İndirdikten sonra:
    echo 1. Dosya adını "cloudflared.exe" yapın
    echo 2. Bu klasöre kopyalayın: %CD%
    echo.
    set /p open_link="Tarayıcıda açmak ister misiniz? (E/H): "
    if /i "%open_link%"=="E" (
        start https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe
    )
    echo.
    echo cloudflared.exe'yi kopyaladıktan sonra bu scripti tekrar çalıştırın.
    pause
    exit /b 1
)
echo ✅ cloudflared.exe bulundu!

REM 2. Config kontrolü
if not exist "%USERPROFILE%\.cloudflared\config.yml" (
    echo ❌ SORUN BULUNDU: Cloudflare config yok!
    echo.
    echo 🔧 CLOUDFLARE_SETUP_s2ggame.bat çalıştırılıyor...
    echo.
    pause
    call CLOUDFLARE_SETUP_s2ggame.bat
    if errorlevel 1 (
        echo ❌ Kurulum başarısız!
        pause
        exit /b 1
    )
)
echo ✅ Cloudflare config tamam!

REM 3. Bağımlılıklar kontrolü
python -c "import flask, flask_sqlalchemy, flask_socketio" 2>nul
if errorlevel 1 (
    echo ❌ SORUN BULUNDU: Bağımlılıklar eksik!
    echo.
    echo 🔧 INSTALL.bat çalıştırılıyor...
    echo.
    call INSTALL.bat
    if errorlevel 1 (
        echo ❌ Kurulum başarısız!
        pause
        exit /b 1
    )
)
echo ✅ Bağımlılıklar tamam!

REM 4. Port kontrolü
netstat -ano | findstr :5000 >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  UYARI: Port 5000 kullanımda!
    echo.
    echo Başka bir program 5000 portunu kullanıyor.
    echo Flask sunucu başlatılamayabilir.
    echo.
    set /p kill_port="Port 5000'i kullanan programı sonlandırmak ister misiniz? (E/H): "
    if /i "%kill_port%"=="E" (
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
            taskkill /F /PID %%a >nul 2>&1
        )
        echo ✅ Port 5000 temizlendi!
    )
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ TÜM SORUNLAR ÇÖZÜLDÜ! ✅                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Şimdi sistemi başlatabilirsiniz:
echo.
echo 1. BASLATMA_ADIM_ADIM.bat (Önerilen - Adım adım)
echo 2. HIZLI_BASLATMA.bat (Hızlı başlatma)
echo.
set /p start_now="Şimdi başlatmak ister misiniz? (1/2/H): "

if "%start_now%"=="1" (
    call BASLATMA_ADIM_ADIM.bat
) else if "%start_now%"=="2" (
    call HIZLI_BASLATMA.bat
) else (
    echo.
    echo İstediğiniz zaman başlatabilirsiniz.
    pause
)
