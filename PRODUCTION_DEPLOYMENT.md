# 🚀 S2G GAME - PRODUCTION DEPLOYMENT REHBERİ

## 📋 İçindekiler
1. [Sunucu Gereksinimleri](#sunucu-gereksinimleri)
2. [VPS Kurulumu](#vps-kurulumu)
3. [Domain Bağlama](#domain-bağlama)
4. [SSL Sertifikası](#ssl-sertifikası)
5. [Nginx Yapılandırması](#nginx-yapılandırması)
6. [Gunicorn ile Çalıştırma](#gunicorn-ile-çalıştırma)
7. [Systemd Service](#systemd-service)
8. [Güvenlik Ayarları](#güvenlik-ayarları)

---

## 🖥️ Sunucu Gereksinimleri

### Minimum Gereksinimler
- **CPU:** 1 Core
- **RAM:** 1GB
- **Disk:** 10GB SSD
- **OS:** Ubuntu 20.04/22.04 LTS (önerilen)
- **Network:** 100Mbps

### Önerilen Gereksinimler
- **CPU:** 2 Core
- **RAM:** 2GB
- **Disk:** 20GB SSD
- **OS:** Ubuntu 22.04 LTS
- **Network:** 1Gbps

### Popüler VPS Sağlayıcıları
- **DigitalOcean** - $6/ay (1GB RAM)
- **Vultr** - $6/ay (1GB RAM)
- **Linode** - $5/ay (1GB RAM)
- **Hetzner** - €4.5/ay (2GB RAM)
- **AWS Lightsail** - $5/ay (1GB RAM)

---

## 🔧 VPS Kurulumu

### 1. Sunucuya Bağlan
```bash
ssh root@SUNUCU_IP_ADRESI
```

### 2. Sistem Güncellemesi
```bash
apt update && apt upgrade -y
```

### 3. Gerekli Paketleri Yükle
```bash
apt install -y python3 python3-pip python3-venv nginx git supervisor ufw
```

### 4. Yeni Kullanıcı Oluştur (Güvenlik)
```bash
adduser s2guser
usermod -aG sudo s2guser
su - s2guser
```

### 5. Projeyi Klonla/Yükle
```bash
cd /home/s2guser
mkdir s2g-game
cd s2g-game

# Dosyaları yükle (FTP, SCP veya Git ile)
# Örnek: scp -r /local/s2g-game/* s2guser@SUNUCU_IP:/home/s2guser/s2g-game/
```

### 6. Virtual Environment Oluştur
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn eventlet  # Production için
```

---

## 🌐 Domain Bağlama

### 1. Domain Satın Al
- **Namecheap** - namecheap.com
- **GoDaddy** - godaddy.com
- **Cloudflare** - cloudflare.com (ücretsiz DNS)

### 2. DNS Ayarları
Domain sağlayıcınızın DNS panelinden:

```
A Record:
Name: @
Value: SUNUCU_IP_ADRESI
TTL: 3600

A Record:
Name: www
Value: SUNUCU_IP_ADRESI
TTL: 3600
```

**Örnek:**
```
@ -> 123.45.67.89
www -> 123.45.67.89
```

### 3. DNS Propagation Kontrolü
```bash
# 5-30 dakika bekleyin, sonra kontrol edin:
nslookup yourdomain.com
ping yourdomain.com
```

---

## 🔒 SSL Sertifikası (Let's Encrypt - Ücretsiz)

### 1. Certbot Yükle
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 2. SSL Sertifikası Al
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 3. Otomatik Yenileme
```bash
# Test et
sudo certbot renew --dry-run

# Cron job otomatik eklenir
sudo systemctl status certbot.timer
```

---

## ⚙️ Nginx Yapılandırması

### 1. Nginx Config Oluştur
```bash
sudo nano /etc/nginx/sites-available/s2g-game
```

### 2. Config İçeriği
```nginx
# HTTP -> HTTPS Yönlendirme
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS Ana Config
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Sertifikaları (Certbot otomatik ekler)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Ayarları
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Güvenlik Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Loglar
    access_log /var/log/nginx/s2g-game-access.log;
    error_log /var/log/nginx/s2g-game-error.log;
    
    # Max Upload Size
    client_max_body_size 16M;
    
    # Static Files
    location /static {
        alias /home/s2guser/s2g-game/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Uploads
    location /uploads {
        alias /home/s2guser/s2g-game/static/uploads;
        expires 30d;
    }
    
    # Socket.IO (WebSocket)
    location /socket.io {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_redirect off;
    }
    
    # Ana Uygulama
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeout ayarları
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### 3. Config'i Aktif Et
```bash
sudo ln -s /etc/nginx/sites-available/s2g-game /etc/nginx/sites-enabled/
sudo nginx -t  # Test et
sudo systemctl restart nginx
```

---

## 🦄 Gunicorn ile Çalıştırma

### 1. Gunicorn Config Oluştur
```bash
nano /home/s2guser/s2g-game/gunicorn_config.py
```

```python
# Gunicorn Configuration
import multiprocessing

# Bind
bind = "127.0.0.1:8000"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "eventlet"  # Socket.IO için gerekli
worker_connections = 1000

# Timeout
timeout = 120
keepalive = 5

# Logging
accesslog = "/home/s2guser/s2g-game/logs/gunicorn-access.log"
errorlog = "/home/s2guser/s2g-game/logs/gunicorn-error.log"
loglevel = "info"

# Process naming
proc_name = "s2g-game"

# Daemon
daemon = False

# Reload
reload = False  # Production'da False
```

### 2. Log Klasörü Oluştur
```bash
mkdir -p /home/s2guser/s2g-game/logs
```

### 3. Test Çalıştırma
```bash
cd /home/s2guser/s2g-game
source venv/bin/activate
gunicorn -c gunicorn_config.py app:app
```

---

## 🔄 Systemd Service (Otomatik Başlatma)

### 1. Service Dosyası Oluştur
```bash
sudo nano /etc/systemd/system/s2g-game.service
```

```ini
[Unit]
Description=S2G Game - Oyun Hesabı Platformu
After=network.target

[Service]
Type=notify
User=s2guser
Group=www-data
WorkingDirectory=/home/s2guser/s2g-game
Environment="PATH=/home/s2guser/s2g-game/venv/bin"
ExecStart=/home/s2guser/s2g-game/venv/bin/gunicorn -c gunicorn_config.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Service'i Aktif Et
```bash
sudo systemctl daemon-reload
sudo systemctl enable s2g-game
sudo systemctl start s2g-game
sudo systemctl status s2g-game
```

### 3. Service Komutları
```bash
# Başlat
sudo systemctl start s2g-game

# Durdur
sudo systemctl stop s2g-game

# Yeniden başlat
sudo systemctl restart s2g-game

# Durum kontrol
sudo systemctl status s2g-game

# Logları görüntüle
sudo journalctl -u s2g-game -f
```

---

## 🔐 Güvenlik Ayarları

### 1. Firewall (UFW)
```bash
# UFW'yi aktif et
sudo ufw enable

# Gerekli portları aç
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Durumu kontrol et
sudo ufw status
```

### 2. Fail2Ban (Brute Force Koruması)
```bash
# Yükle
sudo apt install fail2ban -y

# Config
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = 22
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
```

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. app.py Güvenlik Ayarları
```python
# Production ayarları
app.config['SECRET_KEY'] = 'GÜÇLÜ_RANDOM_KEY_BURAYA'  # Değiştir!
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS için
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Debug kapalı
if __name__ == '__main__':
    socketio.run(app, debug=False, host='127.0.0.1', port=8000)
```

### 4. Veritabanı Yedekleme
```bash
# Yedekleme scripti
nano /home/s2guser/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/s2guser/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_FILE="/home/s2guser/s2g-game/s2g_game.db"

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/s2g_game_$DATE.db

# 7 günden eski yedekleri sil
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
```

```bash
chmod +x /home/s2guser/backup.sh

# Cron job ekle (her gün 03:00)
crontab -e
0 3 * * * /home/s2guser/backup.sh
```

---

## 📊 Monitoring ve Loglar

### 1. Nginx Logları
```bash
# Access log
sudo tail -f /var/log/nginx/s2g-game-access.log

# Error log
sudo tail -f /var/log/nginx/s2g-game-error.log
```

### 2. Gunicorn Logları
```bash
tail -f /home/s2guser/s2g-game/logs/gunicorn-access.log
tail -f /home/s2guser/s2g-game/logs/gunicorn-error.log
```

### 3. System Logları
```bash
sudo journalctl -u s2g-game -f
sudo journalctl -u nginx -f
```

---

## 🔄 Güncelleme ve Bakım

### 1. Kod Güncellemesi
```bash
cd /home/s2guser/s2g-game
git pull  # veya yeni dosyaları yükle
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart s2g-game
```

### 2. Veritabanı Migrasyonu
```bash
cd /home/s2guser/s2g-game
source venv/bin/activate
python reset_database.py  # Dikkatli kullan!
```

### 3. SSL Yenileme
```bash
# Otomatik yenilenir, manuel test:
sudo certbot renew
```

---

## 🎯 Hızlı Deployment Scripti

```bash
nano /home/s2guser/deploy.sh
```

```bash
#!/bin/bash
echo "🚀 S2G Game Deployment Başlıyor..."

cd /home/s2guser/s2g-game

# Yedek al
echo "📦 Veritabanı yedekleniyor..."
./backup.sh

# Kodu güncelle
echo "📥 Kod güncelleniyor..."
# git pull  # Git kullanıyorsanız

# Virtual environment
echo "🐍 Bağımlılıklar güncelleniyor..."
source venv/bin/activate
pip install -r requirements.txt

# Service'i yeniden başlat
echo "🔄 Servis yeniden başlatılıyor..."
sudo systemctl restart s2g-game

# Nginx'i yeniden yükle
echo "🌐 Nginx yeniden yükleniyor..."
sudo nginx -t && sudo systemctl reload nginx

echo "✅ Deployment tamamlandı!"
echo "📊 Durum kontrol ediliyor..."
sudo systemctl status s2g-game --no-pager
```

```bash
chmod +x /home/s2guser/deploy.sh
```

---

## ✅ Deployment Checklist

- [ ] VPS satın alındı
- [ ] Domain satın alındı
- [ ] DNS ayarları yapıldı (A record)
- [ ] Sunucuya SSH bağlantısı yapıldı
- [ ] Sistem güncellemeleri yapıldı
- [ ] Python ve gerekli paketler yüklendi
- [ ] Proje dosyaları yüklendi
- [ ] Virtual environment oluşturuldu
- [ ] Bağımlılıklar yüklendi
- [ ] Nginx kuruldu ve yapılandırıldı
- [ ] SSL sertifikası alındı
- [ ] Gunicorn yapılandırıldı
- [ ] Systemd service oluşturuldu
- [ ] Firewall ayarlandı
- [ ] Fail2Ban kuruldu
- [ ] app.py production ayarları yapıldı
- [ ] Yedekleme scripti oluşturuldu
- [ ] Site test edildi
- [ ] Admin şifresi değiştirildi

---

## 🎉 Başarılı Deployment!

Siteniz artık canlı: https://yourdomain.com

**Kontrol Listesi:**
- ✅ Ana sayfa açılıyor
- ✅ HTTPS çalışıyor (yeşil kilit)
- ✅ Giriş/Kayıt çalışıyor
- ✅ Canlı destek çalışıyor
- ✅ Ürün ekleme/satın alma çalışıyor
- ✅ Admin panel erişilebilir

Mohawk Development 🦅
