@echo off
chcp 65001 >nul
title S2G Game - Port Düzeltme ve Başlatma
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         🔧 PORT SORUNU ÇÖZÜLÜYOR VE BAŞLATILIYOR 🔧       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 📋 ADIM 1: Eski Python process'lerini sonlandır
echo ═══════════════════════════════════════════════════════════
echo.
taskkill /F /IM python.exe 2>nul
if errorlevel 1 (
    echo ℹ️  Çalışan python.exe bulunamadı
) else (
    echo ✅ Python process'leri sonlandırıldı
)
echo.
timeout /t 2 >nul

echo 📋 ADIM 2: Cloudflare config dosyasını güncelle
echo ═══════════════════════════════════════════════════════════
echo.

REM Config dosyasının varlığını kontrol et
if exist "%USERPROFILE%\.cloudflared\config.yml" (
    echo ✅ Config dosyası bulundu, güncelleniyor...
    
    REM Yedek al
    copy "%USERPROFILE%\.cloudflared\config.yml" "%USERPROFILE%\.cloudflared\config.yml.backup" >nul
    
    REM Port 5000'i 8000'e değiştir
    powershell -Command "(Get-Content '%USERPROFILE%\.cloudflared\config.yml') -replace 'localhost:5000', 'localhost:8000' | Set-Content '%USERPROFILE%\.cloudflared\config.yml'"
    
    echo ✅ Config dosyası güncellendi! (Port: 5000 → 8000)
) else (
    echo ⚠️  Config dosyası bulunamadı!
    echo    Önce CLOUDFLARE_SETUP_s2ggame.bat çalıştırın
    echo.
    pause
    exit /b 1
)
echo.

echo 📋 ADIM 3: S2G Game sunucusunu başlat (Port 8000)
echo ═══════════════════════════════════════════════════════════
echo.
start "S2G Game Server - Port 8000" cmd /k "python app.py"
timeout /t 3 >nul

echo 📋 ADIM 4: Cloudflare Tunnel'ı başlat
echo ═══════════════════════════════════════════════════════════
echo.
start "Cloudflare Tunnel" cmd /k "cloudflared.exe tunnel run s2g-game"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ HER ŞEY BAŞLATILDI! ✅                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Siteniz: https://s2ggame.com
echo 🌐 Siteniz: https://www.s2ggame.com
echo 👨‍💼 Admin: https://s2ggame.com/admin
echo.
echo 🔧 Port değişikliği: 5000 → 8000
echo.
echo 📝 İki pencere açıldı:
echo    1. S2G Game Server (Port 8000)
echo    2. Cloudflare Tunnel
echo.
echo ⚠️  Her iki pencereyi de açık tutun!
echo.
echo 💡 Lokal test için: http://localhost:8000
echo.
pause
