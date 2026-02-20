@echo off
chcp 65001 >nul
title S2G GAME - HIZLI BAŞLATMA
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║          🎮 S2G GAME - HIZLI BAŞLATMA 🎮                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo [*] Domain: s2ggame.com
echo [*] Port: 8000
echo [*] DNS: ✅ CNAME kayıtları doğru!
echo.
echo ═══════════════════════════════════════════════════════════
echo.

echo [1/2] Flask sunucusu başlatılıyor (Port 8000)...
start "S2G GAME - FLASK SERVER" cmd /k "cd /d %~dp0 && color 0B && title S2G GAME - FLASK SERVER && python app.py"
timeout /t 3 /nobreak >nul

echo [2/2] Cloudflare Tunnel başlatılıyor...
start "S2G GAME - CLOUDFLARE TUNNEL" cmd /k "cd /d %~dp0 && color 0D && title S2G GAME - CLOUDFLARE TUNNEL && cloudflared.exe tunnel run s2g-game"
timeout /t 3 /nobreak >nul

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ HER İKİ SUNUCU BAŞLATILDI!                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📊 DURUM:
echo ════════════════════════════════════════════════════════════
echo.
echo ✅ Flask Server: http://localhost:8000
echo ✅ Cloudflare Tunnel: Aktif
echo ✅ DNS: CNAME kayıtları doğru
echo.
echo 🌐 SİTE ADRESLERİ:
echo ════════════════════════════════════════════════════════════
echo.
echo 💻 Lokal Test (Hemen):
echo    http://localhost:8000
echo.
echo 🌐 Canlı Site (5-10 dakika sonra):
echo    https://s2ggame.com
echo    https://www.s2ggame.com
echo.
echo ⚠️  ÖNEMLİ:
echo ════════════════════════════════════════════════════════════
echo.
echo • Her iki pencereyi de AÇIK tutun!
echo • DNS yayılması 5-10 dakika sürebilir
echo • Lokal site hemen çalışır
echo • Canlı site biraz bekleyebilir
echo.
echo 🔍 TEST:
echo ════════════════════════════════════════════════════════════
echo.
echo 1. http://localhost:8000 açılıyor mu? (Hemen test et)
echo 2. https://s2ggame.com açılıyor mu? (5-10 dk sonra)
echo.
pause
