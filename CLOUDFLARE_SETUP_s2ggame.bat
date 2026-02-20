@echo off
chcp 65001 >nul
title Cloudflare Tunnel - s2ggame.com Kurulumu
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║    🌐 CLOUDFLARE TUNNEL - s2ggame.com KURULUMU 🌐         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 📋 ADIM 1: CLOUDFLARE'E GİRİŞ
echo ═══════════════════════════════════════════════════════════
echo.
echo Tarayıcı açılacak, Cloudflare'e giriş yapın ve
echo s2ggame.com domain'ini seçin.
echo.
pause

cloudflared.exe tunnel login

if errorlevel 1 (
    echo.
    echo ❌ Giriş başarısız! Lütfen tekrar deneyin.
    pause
    exit /b 1
)

echo.
echo ✅ Cloudflare girişi başarılı!
echo.

echo 📋 ADIM 2: TUNNEL OLUŞTUR
echo ═══════════════════════════════════════════════════════════
echo.
pause

cloudflared.exe tunnel create s2g-game

if errorlevel 1 (
    echo.
    echo ❌ Tunnel oluşturulamadı!
    pause
    exit /b 1
)

echo.
echo ✅ Tunnel oluşturuldu!
echo.
echo ⚠️  ÖNEMLİ: Yukarıdaki TUNNEL ID'yi kopyalayın!
echo Örnek: abc123-def456-ghi789
echo.
set /p tunnel_id="Tunnel ID'yi buraya yapıştırın: "

echo.
echo 📋 ADIM 3: CONFIG DOSYASI OLUŞTUR
echo ═══════════════════════════════════════════════════════════
echo.

REM Config klasörünü oluştur
if not exist "%USERPROFILE%\.cloudflared" mkdir "%USERPROFILE%\.cloudflared"

REM Config dosyasını oluştur
echo tunnel: %tunnel_id% > "%USERPROFILE%\.cloudflared\config.yml"
echo credentials-file: %USERPROFILE%\.cloudflared\%tunnel_id%.json >> "%USERPROFILE%\.cloudflared\config.yml"
echo. >> "%USERPROFILE%\.cloudflared\config.yml"
echo ingress: >> "%USERPROFILE%\.cloudflared\config.yml"
echo   - hostname: s2ggame.com >> "%USERPROFILE%\.cloudflared\config.yml"
echo     service: http://localhost:8000 >> "%USERPROFILE%\.cloudflared\config.yml"
echo   - hostname: www.s2ggame.com >> "%USERPROFILE%\.cloudflared\config.yml"
echo     service: http://localhost:8000 >> "%USERPROFILE%\.cloudflared\config.yml"
echo   - service: http_status:404 >> "%USERPROFILE%\.cloudflared\config.yml"

echo ✅ Config dosyası oluşturuldu!
echo.

echo 📋 ADIM 4: DNS ROUTE EKLE
echo ═══════════════════════════════════════════════════════════
echo.
pause

cloudflared.exe tunnel route dns s2g-game s2ggame.com
cloudflared.exe tunnel route dns s2g-game www.s2ggame.com

echo.
echo ✅ DNS route'lar eklendi!
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ KURULUM TAMAMLANDI! ✅                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📝 Şimdi yapmanız gerekenler:
echo.
echo 1. İKİ PENCERE AÇIN:
echo.
echo    Pencere 1: START.bat
echo    (S2G Game sunucusunu başlatır)
echo.
echo    Pencere 2: START_TUNNEL.bat
echo    (Cloudflare Tunnel'ı başlatır)
echo.
echo 2. SİTENİZİ AÇIN:
echo    https://s2ggame.com
echo    https://www.s2ggame.com
echo.
echo 3. ADMİN PANELİ:
echo    https://s2ggame.com/admin
echo    Kullanıcı: admin
echo    Şifre: admin123
echo.
pause
