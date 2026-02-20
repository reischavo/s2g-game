@echo off
chcp 65001 >nul
title S2G Game - Adım Adım Başlatma
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║        🚀 S2G GAME - ADIM ADIM BAŞLATMA 🚀                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo Bu script size adım adım rehberlik edecek.
echo.
pause

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ADIM 1: SİSTEM KONTROLÜ                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Python kontrolü
echo 🔍 Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı!
    echo.
    echo Python yüklü olmalı. python.org'dan indirin.
    pause
    exit /b 1
)
echo ✅ Python tamam!
echo.

REM Bağımlılıklar kontrolü
echo 🔍 Bağımlılıklar kontrol ediliyor...
python -c "import flask, flask_sqlalchemy, flask_socketio" 2>nul
if errorlevel 1 (
    echo ❌ Bağımlılıklar eksik!
    echo.
    echo INSTALL.bat çalıştırılıyor...
    call INSTALL.bat
    if errorlevel 1 (
        echo ❌ Kurulum başarısız!
        pause
        exit /b 1
    )
)
echo ✅ Bağımlılıklar tamam!
echo.

REM cloudflared.exe kontrolü
echo 🔍 cloudflared.exe kontrol ediliyor...
if not exist "cloudflared.exe" (
    echo ❌ cloudflared.exe bulunamadı!
    echo.
    echo cloudflared.exe bu klasöre kopyalanmalı:
    echo %CD%
    echo.
    pause
    exit /b 1
)
echo ✅ cloudflared.exe bulundu!
echo.

REM Config kontrolü
echo 🔍 Cloudflare config kontrol ediliyor...
if not exist "%USERPROFILE%\.cloudflared\config.yml" (
    echo ❌ Cloudflare config bulunamadı!
    echo.
    echo CLOUDFLARE_SETUP_s2ggame.bat çalıştırılmalı.
    echo.
    set /p setup_now="Şimdi çalıştırmak ister misiniz? (E/H): "
    if /i "%setup_now%"=="E" (
        call CLOUDFLARE_SETUP_s2ggame.bat
        if errorlevel 1 (
            echo ❌ Kurulum başarısız!
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo Önce CLOUDFLARE_SETUP_s2ggame.bat çalıştırın.
        pause
        exit /b 1
    )
)
echo ✅ Cloudflare config tamam!
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ SİSTEM HAZIR! ✅                           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
pause

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ADIM 2: FLASK SUNUCU BAŞLAT                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Yeni bir pencere açılacak: "S2G Game Server"
echo.
echo ⚠️  ÖNEMLİ: Bu pencereyi KAPATAMAYIN!
echo.
pause

start "S2G Game Server" cmd /k "cd /d "%CD%" && START.bat"

echo ✅ Flask sunucu penceresi açıldı!
echo.
echo 🕐 Sunucunun başlaması için 5 saniye bekleniyor...
timeout /t 5 >nul

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           ADIM 3: CLOUDFLARE TUNNEL BAŞLAT                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Yeni bir pencere açılacak: "Cloudflare Tunnel"
echo.
echo ⚠️  ÖNEMLİ: Bu pencereyi de KAPATAMAYIN!
echo.
pause

start "Cloudflare Tunnel" cmd /k "cd /d "%CD%" && START_TUNNEL.bat"

echo ✅ Cloudflare Tunnel penceresi açıldı!
echo.
echo 🕐 Tunnel'ın bağlanması için 5 saniye bekleniyor...
timeout /t 5 >nul

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ HER ŞEY BAŞLATILDI! ✅                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Siteniz: https://s2ggame.com
echo 👨‍💼 Admin: https://s2ggame.com/admin
echo.
echo 📝 Açık olan pencereler:
echo    1. S2G Game Server (Flask) - Port 5000
echo    2. Cloudflare Tunnel - s2ggame.com
echo.
echo ⚠️  HER İKİ PENCEREYİ DE AÇIK TUTUN!
echo.
echo 🌐 Tarayıcınızda test edin: https://s2ggame.com
echo.
echo 🛑 Durdurmak için: Her iki pencerede CTRL+C basın
echo.
pause
