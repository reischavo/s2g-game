@echo off
echo ========================================
echo    S2G GAME - Baslat
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Gerekli paketler yukleniyor...
pip install -r requirements.txt

echo.
echo [2/2] S2G Game baslatiliyor...
echo.
echo Site: http://localhost:5000
echo.

python app.py

pause
