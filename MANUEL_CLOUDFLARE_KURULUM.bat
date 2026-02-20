@echo off
chcp 65001 >nul
title Cloudflare Tunnel - Manuel Kurulum
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║    🌐 CLOUDFLARE TUNNEL - MANUEL KURULUM (s2ggame.com)    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 📁 Çalışma dizini: %CD%
echo.

echo 🔍 cloudflared.exe kontrol ediliyor...
if not exist "cloudflared.exe" (
    echo ❌ HATA: cloudflared.exe bulunamadı!
    echo.
    echo Bu dosya şu konumda olmalı:
    echo %CD%\cloudflared.exe
    echo.
    pause
    exit /b 1
)

echo ✅ cloudflared.exe bulundu!
echo.

echo ═══════════════════════════════════════════════════════════
echo ADIM 1: CLOUDFLARE'E GİRİŞ
echo ═══════════════════════════════════════════════════════════
echo.
echo Tarayıcı açılacak, Cloudflare hesabınıza giriş yapın.
echo s2ggame.com domain'ini seçin ve "Authorize" tıklayın.
echo.
pause

cloudflared.exe tunnel login

if errorlevel 1 (
    echo.
    echo ❌ Giriş başarısız!
    pause
    exit /b 1
)

echo.
echo ✅ Cloudflare girişi başarılı!
echo.

echo ═══════════════════════════════════════════════════════════
echo ADIM 2: TUNNEL OLUŞTUR
echo ═══════════════════════════════════════════════════════════
echo.
echo "s2g-game" adında tunnel oluşturuluyor...
echo.
pause

cloudflared.exe tunnel create s2g-game

if errorlevel 1 (
    echo.
    echo ⚠️  Tunnel zaten var olabilir, devam ediyoruz...
    echo.
)

echo.
echo ═══════════════════════════════════════════════════════════
echo ADIM 3: TUNNEL ID'Yİ BULMA
echo ═══════════════════════════════════════════════════════════
echo.

cloudflared.exe tunnel list

echo.
echo ⚠️  YUKARDA "s2g-game" tunnel'ının ID'sini görüyorsunuz.
echo    Örnek: abc123-def456-ghi789
echo.
set /p tunnel_id="Tunnel ID'yi kopyalayıp buraya yapıştırın: "

if "%tunnel_id%"=="" (
    echo.
    echo ❌ Tunnel ID girilmedi!
    pause
    exit /b 1
)

echo.
echo ✅ Tunnel ID: %tunnel_id%
echo.

echo ═══════════════════════════════════════════════════════════
echo ADIM 4: CONFIG DOSYASI OLUŞTUR
echo ═══════════════════════════════════════════════════════════
echo.

REM Config klasörünü oluştur
if not exist "%USERPROFILE%\.cloudflared" mkdir "%USERPROFILE%\.cloudflared"

REM Config dosyasını oluştur
(
echo tunnel: %tunnel_id%
echo credentials-file: %USERPROFILE%\.cloudflared\%tunnel_id%.json
echo.
echo ingress:
echo   - hostname: s2ggame.com
echo     service: http://localhost:8000
echo   - hostname: www.s2ggame.com
echo     service: http://localhost:8000
echo   - service: http_status:404
) > "%USERPROFILE%\.cloudflared\config.yml"

echo ✅ Config dosyası oluşturuldu!
echo    Konum: %USERPROFILE%\.cloudflared\config.yml
echo.

echo ═══════════════════════════════════════════════════════════
echo ADIM 5: DNS ROUTE EKLE
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
echo 📝 ŞİMDİ YAPMANIZ GEREKENLER:
echo.
echo 1. İKİ PENCERE AÇIN:
echo.
echo    Pencere 1: START.bat
echo    (Flask sunucusu - Port 8000)
echo.
echo    Pencere 2: START_TUNNEL.bat
echo    (Cloudflare Tunnel)
echo.
echo 2. VEYA TEK KOMUTLA:
echo    HIZLI_BASLATMA.bat
echo.
echo 3. SİTENİZİ TEST EDİN:
echo    🌐 https://s2ggame.com
echo    🌐 https://www.s2ggame.com
echo    👨‍💼 https://s2ggame.com/admin
echo.
echo 💡 Lokal test: http://localhost:8000
echo.
pause
