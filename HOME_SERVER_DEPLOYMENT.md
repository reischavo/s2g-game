# 🏠 S2G GAME - EV/OFİS BİLGİSAYARINDA ÇALIŞTIRMA REHBERİ

## 📋 İçindekiler
1. [Genel Bakış](#genel-bakış)
2. [Yöntem 1: Port Forwarding + Dynamic DNS (Ücretsiz)](#yöntem-1-port-forwarding--dynamic-dns)
3. [Yöntem 2: Cloudflare Tunnel (Ücretsiz, Kolay)](#yöntem-2-cloudflare-tunnel)
4. [Yöntem 3: Ngrok (Hızlı Test)](#yöntem-3-ngrok)
5. [Yöntem 4: Tailscale (VPN Tabanlı)](#yöntem-4-tailscale)

---

## 🎯 Genel Bakış

Kendi bilgisayarınızda web sitesi çalıştırmak için 3 ana sorun çözülmeli:

1. **Dinamik IP Sorunu** - İnternet sağlayıcınız IP'nizi sürekli değiştirir
2. **Port Erişimi** - Modem/router'ınız dış erişimi engelliyor
3. **Domain Bağlama** - Domain'i değişen IP'nize yönlendirme

---

## 🌐 Yöntem 1: Port Forwarding + Dynamic DNS (ÖNERİLEN)

### Avantajlar
✅ Tamamen ücretsiz
✅ Kendi domain'inizi kullanabilirsiniz
✅ Hızlı ve stabil
✅ Tam kontrol

### Dezavantajlar
❌ Modem/router ayarları gerekli
❌ Statik IP yoksa Dynamic DNS gerekli
❌ Teknik bilgi gerektirir

---

### ADIM 1: Bilgisayarınızı Hazırlayın

#### Windows:
```cmd
# 1. Projeyi kurun
cd C:\s2g-game
INSTALL.bat

# 2. Sunucuyu başlatın
START.bat
```

#### Linux:
```bash
# 1. Projeyi kurun
cd ~/s2g-game
./install.sh

# 2. Sunucuyu başlatın
./start.sh
```

### ADIM 2: Statik Lokal IP Ayarlayın

#### Windows:
1. Başlat > Ayarlar > Ağ ve İnternet
2. Ethernet/Wi-Fi > Özellikler
3. IP ataması > Düzenle
4. Manuel > IPv4 Aç
5. IP adresi: `192.168.1.100` (örnek)
6. Alt ağ maskesi: `255.255.255.0`
7. Ağ geçidi: `192.168.1.1` (modem IP'si)
8. DNS: `8.8.8.8` (Google DNS)

#### Linux:
```bash
# Netplan ile (Ubuntu 18.04+)
sudo nano /etc/netplan/01-netcfg.yaml
```

```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses: [192.168.1.100/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

```bash
sudo netplan apply
```

### ADIM 3: Port Forwarding (Modem/Router Ayarları)

#### Genel Adımlar:
1. Modem/Router admin paneline girin
   - Genellikle: `192.168.1.1` veya `192.168.0.1`
   - Kullanıcı: `admin`
   - Şifre: Modem üzerinde yazıyor

2. Port Forwarding/NAT/Sanal Sunucu bölümünü bulun

3. Yeni kural ekleyin:
   ```
   Servis Adı: S2G-HTTP
   Dış Port: 80
   İç IP: 192.168.1.100 (bilgisayarınızın IP'si)
   İç Port: 80
   Protokol: TCP
   
   Servis Adı: S2G-HTTPS
   Dış Port: 443
   İç IP: 192.168.1.100
   İç Port: 443
   Protokol: TCP
   ```

#### Popüler Modem/Router Markaları:

**TP-Link:**
- Forwarding > Virtual Servers > Add New

**D-Link:**
- Advanced > Port Forwarding

**Asus:**
- WAN > Virtual Server/Port Forwarding

**ZTE (Türk Telekom):**
- Uygulama > Port Yönlendirme

**Huawei:**
- Forwarding Rules > Port Mapping

### ADIM 4: Nginx Kurulumu (Opsiyonel ama Önerilen)

#### Windows:
```powershell
# Nginx indirin: http://nginx.org/en/download.html
# C:\nginx klasörüne çıkarın

# nginx.conf düzenleyin
notepad C:\nginx\conf\nginx.conf
```

```nginx
http {
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        
        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

```powershell
# Nginx'i başlatın
cd C:\nginx
start nginx
```

#### Linux:
```bash
sudo apt install nginx -y

sudo nano /etc/nginx/sites-available/s2g-game
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/s2g-game /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### ADIM 5: Dynamic DNS Kurulumu

Statik IP'niz yoksa (çoğu ev interneti), Dynamic DNS kullanın:

#### No-IP (Ücretsiz)
1. https://www.noip.com/ hesap açın
2. Hostname oluşturun: `yoursite.ddns.net`
3. DUC (Dynamic Update Client) indirin
4. Kurulum yapın ve giriş yapın
5. Hostname'i seçin

#### DuckDNS (Ücretsiz, Kolay)
1. https://www.duckdns.org/ girin
2. GitHub/Google ile giriş yapın
3. Subdomain oluşturun: `yoursite.duckdns.org`
4. Token'ı kopyalayın

**Windows için otomatik güncelleme:**
```batch
@echo off
REM update_duckdns.bat
curl "https://www.duckdns.org/update?domains=yoursite&token=YOUR_TOKEN&ip="
```

Görev Zamanlayıcı ile 5 dakikada bir çalıştırın.

**Linux için:**
```bash
# Crontab ekle
crontab -e

# Her 5 dakikada bir güncelle
*/5 * * * * curl "https://www.duckdns.org/update?domains=yoursite&token=YOUR_TOKEN&ip="
```

### ADIM 6: Kendi Domain'inizi Bağlayın (Opsiyonel)

Domain sağlayıcınızda (Namecheap, GoDaddy vb.):

```
CNAME Record:
Name: @
Value: yoursite.duckdns.org
TTL: 3600

CNAME Record:
Name: www
Value: yoursite.duckdns.org
TTL: 3600
```

### ADIM 7: SSL Sertifikası (Let's Encrypt)

#### Certbot ile (Linux):
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

#### Win-ACME ile (Windows):
1. https://www.win-acme.com/ indirin
2. Çalıştırın ve domain'inizi seçin

---

## ☁️ Yöntem 2: Cloudflare Tunnel (ÖNERİLEN - KOLAY)

### Avantajlar
✅ Port forwarding gerekmez
✅ Otomatik SSL
✅ DDoS koruması
✅ Ücretsiz
✅ Çok kolay kurulum

### Dezavantajlar
❌ Cloudflare üzerinden geçer
❌ Cloudflare'in kurallarına tabi

---

### ADIM 1: Cloudflare Hesabı

1. https://dash.cloudflare.com/ hesap açın
2. Domain'inizi ekleyin
3. Nameserver'ları değiştirin (domain sağlayıcınızda)

### ADIM 2: Cloudflared Kurulumu

#### Windows:
```powershell
# Cloudflared indirin
# https://github.com/cloudflare/cloudflared/releases

# Kurulum
cloudflared.exe tunnel login

# Tunnel oluştur
cloudflared.exe tunnel create s2g-game

# Config oluştur
notepad C:\Users\%USERNAME%\.cloudflared\config.yml
```

```yaml
tunnel: TUNNEL_ID
credentials-file: C:\Users\USERNAME\.cloudflared\TUNNEL_ID.json

ingress:
  - hostname: yourdomain.com
    service: http://localhost:5000
  - hostname: www.yourdomain.com
    service: http://localhost:5000
  - service: http_status:404
```

```powershell
# DNS route ekle
cloudflared.exe tunnel route dns s2g-game yourdomain.com
cloudflared.exe tunnel route dns s2g-game www.yourdomain.com

# Tunnel'ı başlat
cloudflared.exe tunnel run s2g-game
```

#### Linux:
```bash
# Cloudflared yükle
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Login
cloudflared tunnel login

# Tunnel oluştur
cloudflared tunnel create s2g-game

# Config
mkdir -p ~/.cloudflared
nano ~/.cloudflared/config.yml
```

```yaml
tunnel: TUNNEL_ID
credentials-file: /home/USERNAME/.cloudflared/TUNNEL_ID.json

ingress:
  - hostname: yourdomain.com
    service: http://localhost:5000
  - hostname: www.yourdomain.com
    service: http://localhost:5000
  - service: http_status:404
```

```bash
# DNS route
cloudflared tunnel route dns s2g-game yourdomain.com
cloudflared tunnel route dns s2g-game www.yourdomain.com

# Service olarak çalıştır
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

### ADIM 3: Test

Site otomatik olarak HTTPS ile çalışır:
- https://yourdomain.com

---

## 🚀 Yöntem 3: Ngrok (HIZLI TEST)

### Avantajlar
✅ Anında çalışır
✅ Kurulum yok
✅ Test için mükemmel

### Dezavantajlar
❌ Ücretsiz sürümde random URL
❌ Kalıcı değil
❌ Yavaş olabilir

---

### Kurulum

1. https://ngrok.com/ hesap açın
2. Ngrok indirin
3. Auth token'ı ayarlayın:

```bash
ngrok config add-authtoken YOUR_TOKEN
```

4. Tunnel başlatın:

```bash
# HTTP
ngrok http 5000

# Custom domain (ücretli)
ngrok http --domain=yourdomain.com 5000
```

5. Verilen URL'i kullanın:
```
https://abc123.ngrok.io
```

---

## 🔐 Yöntem 4: Tailscale (VPN TABANLI)

### Avantajlar
✅ Güvenli VPN
✅ Kolay kurulum
✅ Ücretsiz (100 cihaza kadar)

### Dezavantajlar
❌ Sadece Tailscale ağındakiler erişebilir
❌ Genel erişim için ek ayar gerekli

---

### Kurulum

1. https://tailscale.com/ hesap açın
2. Tailscale yükleyin (Windows/Linux/Mac)
3. Giriş yapın
4. Funnel özelliğini aktif edin:

```bash
tailscale funnel 5000
```

5. Verilen URL'i kullanın

---

## 🔧 Önerilen Yapılandırma

### app.py Ayarları

```python
# Production için
if __name__ == '__main__':
    # Dış erişim için 0.0.0.0
    socketio.run(app, 
                 debug=False,  # Production'da False
                 host='0.0.0.0',  # Tüm IP'lerden erişim
                 port=5000)
```

### Güvenlik

```python
# app.py
app.config['SECRET_KEY'] = 'GÜÇLÜ_RANDOM_KEY'
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS için
app.config['SESSION_COOKIE_HTTPONLY'] = True
```

### Firewall (Windows)

```powershell
# Port 5000'i aç
New-NetFirewallRule -DisplayName "S2G Game" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

### Firewall (Linux)

```bash
sudo ufw allow 5000/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 📊 Karşılaştırma Tablosu

| Yöntem | Kolay | Ücretsiz | Hız | Güvenlik | Önerilen |
|--------|-------|----------|-----|----------|----------|
| Port Forwarding + DDNS | ⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ Evet |
| Cloudflare Tunnel | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Evet |
| Ngrok | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Test için |
| Tailscale | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Özel ağ |

---

## 🎯 Hangi Yöntemi Seçmeliyim?

### Cloudflare Tunnel (En Kolay)
- ✅ Teknik bilgi gerektirmez
- ✅ Port forwarding gerekmez
- ✅ Otomatik SSL
- ✅ DDoS koruması
- **Önerilen: Başlangıç için**

### Port Forwarding + DDNS (En Hızlı)
- ✅ Tam kontrol
- ✅ En hızlı
- ✅ Kendi domain'iniz
- **Önerilen: Teknik bilginiz varsa**

### Ngrok (Test İçin)
- ✅ Anında çalışır
- ✅ Test için mükemmel
- **Önerilen: Sadece test**

---

## ⚠️ Önemli Notlar

### Güvenlik
- Güçlü şifreler kullanın
- Firewall aktif tutun
- Düzenli yedekleme yapın
- Admin şifresini değiştirin

### Performans
- Ev internetinin upload hızı önemli
- Çok fazla kullanıcı için VPS önerilir
- Elektrik kesintisine karşı UPS kullanın

### Yasal
- İnternet sağlayıcınızın kurallarını kontrol edin
- Bazı ISP'ler sunucu çalıştırmayı yasaklar
- Ticari kullanım için VPS önerilir

---

## 🚀 Hızlı Başlangıç (Cloudflare Tunnel)

```bash
# 1. Projeyi başlat
cd s2g-game
START.bat  # Windows
./start.sh  # Linux

# 2. Cloudflared kur
# Windows: cloudflared.exe indirin
# Linux: sudo dpkg -i cloudflared.deb

# 3. Login
cloudflared tunnel login

# 4. Tunnel oluştur
cloudflared tunnel create s2g-game

# 5. Config oluştur
# config.yml dosyasını düzenle

# 6. DNS route
cloudflared tunnel route dns s2g-game yourdomain.com

# 7. Başlat
cloudflared tunnel run s2g-game

# 8. Site hazır!
# https://yourdomain.com
```

---

## ✅ Başarılı Kurulum!

Siteniz artık kendi bilgisayarınızda çalışıyor ve domain ile erişilebilir!

**Test Edin:**
- https://yourdomain.com
- Admin panel: https://yourdomain.com/admin
- Canlı destek çalışıyor mu?

Mohawk Development 🦅
