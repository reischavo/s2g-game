@echo off
chcp 65001 >nul
title Flask Test
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              🧪 FLASK SUNUCU TESTİ 🧪                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔍 Python kontrol ediliyor...
python --version
if errorlevel 1 (
    echo ❌ Python bulunamadı!
    pause
    exit /b 1
)
echo.

echo 🔍 Flask kontrol ediliyor...
python -c "import flask; print('Flask version:', flask.__version__)"
if errorlevel 1 (
    echo ❌ Flask yüklü değil!
    pause
    exit /b 1
)
echo.

echo 🔍 SocketIO kontrol ediliyor...
python -c "import flask_socketio; print('SocketIO version:', flask_socketio.__version__)"
if errorlevel 1 (
    echo ❌ Flask-SocketIO yüklü değil!
    pause
    exit /b 1
)
echo.

echo ✅ Tüm bağımlılıklar tamam!
echo.
echo 🚀 Flask sunucusu başlatılıyor...
echo.
echo ⚠️  Bu pencereyi AÇIK TUTUN!
echo ⚠️  Durdurmak için CTRL+C basın
echo.
echo ═══════════════════════════════════════════════════════════
echo.

python app.py

echo.
echo ═══════════════════════════════════════════════════════════
echo Sunucu durduruldu.
pause
