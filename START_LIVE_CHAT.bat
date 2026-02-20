@echo off
title S2G Game - Live Chat Sistemi
color 0D
echo.
echo ============================================
echo    S2G GAME - LIVE CHAT SISTEMI
echo    Mohawk Development - Ultra Modern
echo ============================================
echo.
echo [*] Veritabani guncelleniyor...
python update_db.py
echo.
echo [*] Sunucu baslatiliyor...
echo [*] Ana Sayfa: http://localhost:5000
echo [*] Admin Panel: http://localhost:5000/admin
echo [*] Network: http://[IP_ADRESINIZ]:5000
echo.
echo [!] Kapatmak icin CTRL+C basin
echo.
python app.py
pause
