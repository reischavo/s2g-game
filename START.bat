@echo off
chcp 65001 >nul
title S2G Game - Sunucu
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           🎮 S2G GAME - SUNUCU BAŞLATILIYOR 🎮            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Bağımlılıklar kontrol ediliyor...
python -c "import flask, flask_sqlalchemy, flask_socketio" 2>nul
if errorlevel 1 (
    echo.
    echo ❌ HATA: Bağımlılıklar yüklü değil!
    echo.
    echo Önce INSTALL.bat dosyasını çalıştırın.
    echo.
    pause
    exit /b 1
)

echo ✅ Bağımlılıklar tamam!
echo.

REM Doğru dizine geç
cd /d "%~dp0"

echo 📁 Çalışma dizini: %CD%
echo.
echo 🚀 Sunucu başlatılıyor...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Sunucu Adresi: http://localhost:8000                      ║
echo ║  Admin Panel:   http://localhost:8000/admin                ║
echo ║  Admin Hesap:   admin / admin123                           ║
echo ║                                                             ║
echo ║  Durdurmak için: CTRL + C                                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

python app.py

if errorlevel 1 (
    echo.
    echo ❌ Sunucu hata ile kapandı!
    echo.
    pause
    exit /b 1
)

echo.
echo ⚠️  Sunucu durduruldu!
pause
