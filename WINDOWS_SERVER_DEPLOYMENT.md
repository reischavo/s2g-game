# 🪟 S2G GAME - WINDOWS SERVER DEPLOYMENT

## 📋 Windows Server'da Çalıştırma Rehberi

### 🖥️ Gereksinimler
- Windows Server 2016/2019/2022
- IIS (Internet Information Services)
- Python 3.8+
- Domain (opsiyonel)

---

## 🚀 Kurulum Adımları

### 1. Python Kurulumu
1. Python 3.8+ indirin: https://www.python.org/downloads/
2. Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin
3. Kurulumu tamamlayın

### 2. IIS Kurulumu
```powershell
# PowerShell'i Administrator olarak açın
Install-WindowsFeature -name Web-Server -IncludeManagementTools
```

### 3. Proje Kurulumu
```powershell
# Proje klasörüne gidin
cd C:\inetpub\wwwroot\s2g-game

# Virtual environment oluştur
python -m venv venv

# Aktif et
.\venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt
pip install waitress  # Windows için production server
```

### 4. Waitress ile Çalıştırma
```python
# run_production.py oluşturun
from waitress import serve
from app import app, socketio

if __name__ == '__main__':
    print("🚀 S2G Game başlatılıyor...")
    print("📍 http://localhost:8000")
    serve(socketio, host='0.0.0.0', port=8000, threads=4)
```

### 5. Windows Service Olarak Çalıştırma

#### NSSM (Non-Sucking Service Manager) Kullanarak:
1. NSSM indirin: https://nssm.cc/download
2. PowerShell'de:
```powershell
# NSSM ile service oluştur
nssm install S2GGame "C:\inetpub\wwwroot\s2g-game\venv\Scripts\python.exe" "C:\inetpub\wwwroot\s2g-game\run_production.py"

# Service'i başlat
nssm start S2GGame

# Durum kontrol
nssm status S2GGame
```

### 6. IIS Reverse Proxy Yapılandırması

#### URL Rewrite ve ARR Modüllerini Yükleyin:
- URL Rewrite: https://www.iis.net/downloads/microsoft/url-rewrite
- Application Request Routing: https://www.iis.net/downloads/microsoft/application-request-routing

#### web.config Oluşturun:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <rewrite>
            <rules>
                <rule name="ReverseProxyInboundRule1" stopProcessing="true">
                    <match url="(.*)" />
                    <action type="Rewrite" url="http://localhost:8000/{R:1}" />
                </rule>
            </rules>
        </rewrite>
        <httpProtocol>
            <customHeaders>
                <add name="X-Frame-Options" value="SAMEORIGIN" />
                <add name="X-Content-Type-Options" value="nosniff" />
            </customHeaders>
        </httpProtocol>
    </system.webServer>
</configuration>
```

### 7. Domain Bağlama

#### IIS Manager'da:
1. Sites > Add Website
2. Site name: S2G Game
3. Physical path: C:\inetpub\wwwroot\s2g-game
4. Binding:
   - Type: http
   - IP: All Unassigned
   - Port: 80
   - Host name: yourdomain.com

### 8. SSL Sertifikası (Let's Encrypt)

#### Win-ACME Kullanarak:
1. Win-ACME indirin: https://www.win-acme.com/
2. Çalıştırın:
```powershell
wacs.exe
```
3. Menüden "Create certificate" seçin
4. Domain'inizi seçin
5. Otomatik yenileme ayarlanır

---

## 🔧 Yönetim Komutları

### Service Yönetimi
```powershell
# Başlat
Start-Service S2GGame

# Durdur
Stop-Service S2GGame

# Yeniden başlat
Restart-Service S2GGame

# Durum
Get-Service S2GGame
```

### Loglar
```powershell
# Event Viewer'da logları görüntüle
eventvwr.msc

# Veya PowerShell ile
Get-EventLog -LogName Application -Source S2GGame -Newest 50
```

---

## 🔒 Güvenlik

### Windows Firewall
```powershell
# HTTP
New-NetFirewallRule -DisplayName "S2G Game HTTP" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Allow

# HTTPS
New-NetFirewallRule -DisplayName "S2G Game HTTPS" -Direction Inbound -LocalPort 443 -Protocol TCP -Action Allow
```

### Otomatik Yedekleme
```powershell
# backup.ps1 oluşturun
$BackupPath = "C:\Backups\S2GGame"
$Date = Get-Date -Format "yyyyMMdd_HHmmss"
$DbFile = "C:\inetpub\wwwroot\s2g-game\s2g_game.db"

New-Item -ItemType Directory -Force -Path $BackupPath
Copy-Item $DbFile "$BackupPath\s2g_game_$Date.db"

# 7 günden eski yedekleri sil
Get-ChildItem $BackupPath -Filter "*.db" | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | Remove-Item
```

```powershell
# Task Scheduler ile otomatik çalıştır
$Action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\inetpub\wwwroot\s2g-game\backup.ps1"
$Trigger = New-ScheduledTaskTrigger -Daily -At 3am
Register-ScheduledTask -TaskName "S2G Game Backup" -Action $Action -Trigger $Trigger
```

---

## 📊 Performans İzleme

### Performance Monitor
```powershell
# Performans sayaçlarını görüntüle
perfmon.msc
```

### Resource Monitor
```powershell
resmon.exe
```

---

## 🎯 Hızlı Başlangıç Scripti

```powershell
# deploy_windows.ps1
Write-Host "🚀 S2G Game Deployment Başlıyor..." -ForegroundColor Blue

# Python kontrolü
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python bulunamadı!" -ForegroundColor Red
    exit 1
}

# Proje klasörü
$ProjectPath = "C:\inetpub\wwwroot\s2g-game"
Set-Location $ProjectPath

# Virtual environment
Write-Host "🐍 Virtual environment oluşturuluyor..." -ForegroundColor Yellow
python -m venv venv
.\venv\Scripts\activate

# Bağımlılıklar
Write-Host "📦 Bağımlılıklar yükleniyor..." -ForegroundColor Yellow
pip install -r requirements.txt
pip install waitress

# Service oluştur
Write-Host "🔧 Windows Service oluşturuluyor..." -ForegroundColor Yellow
nssm install S2GGame "$ProjectPath\venv\Scripts\python.exe" "$ProjectPath\run_production.py"
nssm start S2GGame

Write-Host "✅ Deployment tamamlandı!" -ForegroundColor Green
Write-Host "🌐 Site: http://localhost" -ForegroundColor Cyan
```

---

## ✅ Başarılı Deployment!

Site artık Windows Server'da çalışıyor!

Mohawk Development 🦅
