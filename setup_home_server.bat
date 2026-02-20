@echo off
chcp 65001 >nul
title S2G Game - Ev Sunucusu Kurulumu
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║      🏠 S2G GAME - EV SUNUCUSU KURULUMU 🏠                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo Bu script sitenizi kendi bilgisayarınızda çalıştırmanıza yardımcı olur.
echo.
pause

echo.
echo ═══════════════════════════════════════════════════════════
echo  ADIM 1: KURULUM YÖNTEMİ SEÇİN
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Cloudflare Tunnel (Önerilen - En Kolay)
echo 2. Port Forwarding + Dynamic DNS (Hızlı)
echo 3. Ngrok (Hızlı Test)
echo 4. Sadece Lokal Kurulum
echo.
set /p method="Seçiminiz (1-4): "

if "%method%"=="1" goto cloudflare
if "%method%"=="2" goto portforward
if "%method%"=="3" goto ngrok
if "%method%"=="4" goto local
goto end

:cloudflare
echo.
echo ═══════════════════════════════════════════════════════════
echo  CLOUDFLARE TUNNEL KURULUMU
echo ═══════════════════════════════════════════════════════════
echo.
echo 📝 Gereksinimler:
echo    1. Cloudflare hesabı (ücretsiz)
echo    2. Domain (Cloudflare'e eklenmiş)
echo.
echo 🔗 Adımlar:
echo    1. https://dash.cloudflare.com/ hesap açın
echo    2. Domain'inizi ekleyin
echo    3. Nameserver'ları değiştirin
echo.
pause

echo.
echo 📥 Cloudflared indiriliyor...
echo.
echo Lütfen şu adresten Cloudflared'i indirin:
echo https://github.com/cloudflare/cloudflared/releases/latest
echo.
echo cloudflared-windows-amd64.exe dosyasını indirin
echo ve bu klasöre kopyalayın.
echo.
pause

if not exist "cloudflared.exe" (
    echo.
    echo ❌ cloudflared.exe bulunamadı!
    echo Lütfen dosyayı indirip bu klasöre kopyalayın.
    pause
    goto end
)

echo.
echo ✅ Cloudflared bulundu!
echo.
echo 🔐 Cloudflare'e giriş yapılıyor...
cloudflared.exe tunnel login

echo.
set /p domain="Domain adınız (örn: example.com): "
set /p tunnelname="Tunnel adı (örn: s2g-game): "

echo.
echo 🚇 Tunnel oluşturuluyor...
cloudflared.exe tunnel create %tunnelname%

echo.
echo 📝 Config dosyası oluşturuluyor...
echo tunnel: %tunnelname% > config.yml
echo credentials-file: %USERPROFILE%\.cloudflared\%tunnelname%.json >> config.yml
echo. >> config.yml
echo ingress: >> config.yml
echo   - hostname: %domain% >> config.yml
echo     service: http://localhost:5000 >> config.yml
echo   - hostname: www.%domain% >> config.yml
echo     service: http://localhost:5000 >> config.yml
echo   - service: http_status:404 >> config.yml

move config.yml %USERPROFILE%\.cloudflared\config.yml

echo.
echo 🌐 DNS route ekleniyor...
cloudflared.exe tunnel route dns %tunnelname% %domain%
cloudflared.exe tunnel route dns %tunnelname% www.%domain%

echo.
echo ✅ Cloudflare Tunnel kurulumu tamamlandı!
echo.
echo 📝 Tunnel'ı başlatmak için:
echo    cloudflared.exe tunnel run %tunnelname%
echo.
echo 🌐 Siteniz: https://%domain%
echo.
pause
goto local

:portforward
echo.
echo ═══════════════════════════════════════════════════════════
echo  PORT FORWARDING KURULUMU
echo ═══════════════════════════════════════════════════════════
echo.
echo 📝 Yapmanız gerekenler:
echo.
echo 1. BİLGİSAYARINIZIN IP ADRESİ:
ipconfig | findstr /i "IPv4"
echo.
echo 2. MODEM/ROUTER ADMİN PANELİ:
echo    - Genellikle: 192.168.1.1 veya 192.168.0.1
echo    - Kullanıcı: admin
echo    - Şifre: Modem üzerinde yazıyor
echo.
echo 3. PORT FORWARDING AYARLARI:
echo    Dış Port: 80  → İç IP: [BİLGİSAYARINIZ] → İç Port: 5000
echo    Dış Port: 443 → İç IP: [BİLGİSAYARINIZ] → İç Port: 5000
echo.
echo 4. DYNAMIC DNS (No-IP veya DuckDNS):
echo    - https://www.noip.com/ veya
echo    - https://www.duckdns.org/
echo.
pause
goto local

:ngrok
echo.
echo ═══════════════════════════════════════════════════════════
echo  NGROK KURULUMU
echo ═══════════════════════════════════════════════════════════
echo.
echo 📝 Adımlar:
echo    1. https://ngrok.com/ hesap açın
echo    2. Ngrok indirin
echo    3. Auth token alın
echo.
pause

echo.
set /p ngrok_token="Ngrok auth token'ınız: "

if exist "ngrok.exe" (
    echo.
    echo 🔐 Ngrok yapılandırılıyor...
    ngrok.exe config add-authtoken %ngrok_token%
    
    echo.
    echo ✅ Ngrok hazır!
    echo.
    echo 📝 Ngrok'u başlatmak için:
    echo    ngrok.exe http 5000
    echo.
    pause
) else (
    echo.
    echo ❌ ngrok.exe bulunamadı!
    echo Lütfen https://ngrok.com/download adresinden indirin.
    pause
)
goto local

:local
echo.
echo ═══════════════════════════════════════════════════════════
echo  ADIM 2: LOKAL KURULUM
echo ═══════════════════════════════════════════════════════════
echo.

REM Kurulum yap
if not exist "venv" (
    echo 📦 Kurulum yapılıyor...
    call INSTALL.bat
)

echo.
echo ═══════════════════════════════════════════════════════════
echo  ADIM 3: FIREWALL AYARLARI
echo ═══════════════════════════════════════════════════════════
echo.
echo Firewall'da port 5000'i açmak ister misiniz? (E/H)
set /p firewall="Seçiminiz: "

if /i "%firewall%"=="E" (
    echo.
    echo 🔒 Firewall kuralı ekleniyor...
    netsh advfirewall firewall add rule name="S2G Game" dir=in action=allow protocol=TCP localport=5000
    echo ✅ Firewall kuralı eklendi!
)

echo.
echo ═══════════════════════════════════════════════════════════
echo  ADIM 4: SUNUCU BAŞLATILIYOR
echo ═══════════════════════════════════════════════════════════
echo.

echo 🚀 Sunucu başlatılıyor...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Lokal Erişim:  http://localhost:5000                      ║
echo ║  Ağ Erişimi:    http://[BİLGİSAYAR_IP]:5000               ║
echo ║  Admin Panel:   http://localhost:5000/admin                ║
echo ║                                                             ║
echo ║  Durdurmak için: CTRL + C                                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

if "%method%"=="1" (
    echo.
    echo 🌐 Cloudflare Tunnel başlatılıyor...
    start "S2G Game Server" cmd /k "START.bat"
    timeout /t 5 >nul
    start "Cloudflare Tunnel" cmd /k "cloudflared.exe tunnel run %tunnelname%"
    echo.
    echo ✅ Sunucu ve Tunnel başlatıldı!
    echo 🌐 Siteniz: https://%domain%
) else if "%method%"=="3" (
    echo.
    echo 🌐 Ngrok başlatılıyor...
    start "S2G Game Server" cmd /k "START.bat"
    timeout /t 5 >nul
    start "Ngrok Tunnel" cmd /k "ngrok.exe http 5000"
    echo.
    echo ✅ Sunucu ve Ngrok başlatıldı!
    echo 📝 Ngrok penceresindeki URL'i kullanın
) else (
    call START.bat
)

:end
echo.
pause
