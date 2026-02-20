@echo off
chcp 65001 >nul
title S2G Game + Cloudflare Tunnel - Hızlı Başlatma
color 0E

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║      🚀 S2G GAME + CLOUDFLARE TUNNEL BAŞLATILIYOR 🚀      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 📦 S2G Game sunucusu başlatılıyor...
start "S2G Game Server" cmd /k "START.bat"

timeout /t 3 >nul

echo 🌐 Cloudflare Tunnel başlatılıyor...
start "Cloudflare Tunnel" cmd /k "START_TUNNEL.bat"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                  ✅ HER İKİSİ BAŞLATILDI! ✅              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Siteniz: https://s2ggame.com
echo 👨‍💼 Admin: https://s2ggame.com/admin
echo 💡 Lokal: http://localhost:8000
echo.
echo 📝 İki pencere açıldı:
echo    1. S2G Game Server (Port 8000)
echo    2. Cloudflare Tunnel
echo.
echo ⚠️  Her iki pencereyi de açık tutun!
echo.
pause
