# 🚀 S2G GAME - DEPLOYMENT HIZLI REFERANS

## 📋 Hızlı Başlangıç

### Linux/Ubuntu VPS (Önerilen)
```bash
chmod +x deploy_to_vps.sh
./deploy_to_vps.sh
```

### Manuel Kurulum
```bash
# 1. Sunucuya bağlan
ssh root@SUNUCU_IP

# 2. Sistem güncelle
apt update && apt upgrade -y

# 3. Gerekli paketleri yükle
apt install -y python3 python3-pip python3-venv nginx git certbot python3-certbot-nginx

# 4. Proje yükle
mkdir -p /home/s2guser/s2g-game
# Dosyaları yükle (SCP, FTP, Git)

# 5. Python ortamı
cd /home/s2guser/s2g-game
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn eventlet

# 6. Nginx config
nano /etc/nginx/sites-available/s2g-game
# Config'i yapıştır (PRODUCTION_DEPLOYMENT.md'den)
ln -s /etc/nginx/sites-available/s2g-game /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx

# 7. Systemd service
nano /etc/systemd/system/s2g-game.service
# Service config'i yapıştır
systemctl daemon-reload
systemctl enable s2g-game
systemctl start s2g-game

# 8. SSL
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 🌐 DNS Ayarları

### Domain Sağlayıcınızda:
```
A Record:
Name: @
Value: SUNUCU_IP
TTL: 3600

A Record:
Name: www
Value: SUNUCU_IP
TTL: 3600
```

### Kontrol:
```bash
nslookup yourdomain.com
ping yourdomain.com
```

---

## 🔧 Yönetim Komutları

### Service Yönetimi
```bash
# Başlat
sudo systemctl start s2g-game

# Durdur
sudo systemctl stop s2g-game

# Yeniden başlat
sudo systemctl restart s2g-game

# Durum
sudo systemctl status s2g-game

# Loglar
sudo journalctl -u s2g-game -f
```

### Nginx Yönetimi
```bash
# Test
sudo nginx -t

# Yeniden yükle
sudo systemctl reload nginx

# Yeniden başlat
sudo systemctl restart nginx

# Loglar
sudo tail -f /var/log/nginx/s2g-game-error.log
```

### SSL Yönetimi
```bash
# Yenile
sudo certbot renew

# Test
sudo certbot renew --dry-run

# Durum
sudo certbot certificates
```

---

## 📊 Monitoring

### Sistem Durumu
```bash
# CPU, RAM, Disk
htop
df -h
free -h

# Network
netstat -tulpn | grep :8000
ss -tulpn | grep :8000
```

### Uygulama Logları
```bash
# Gunicorn
tail -f /home/s2guser/s2g-game/logs/gunicorn-error.log
tail -f /home/s2guser/s2g-game/logs/gunicorn-access.log

# Nginx
tail -f /var/log/nginx/s2g-game-error.log
tail -f /var/log/nginx/s2g-game-access.log

# System
sudo journalctl -u s2g-game -f
```

---

## 🔄 Güncelleme

### Kod Güncellemesi
```bash
cd /home/s2guser/s2g-game
git pull  # veya yeni dosyaları yükle
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart s2g-game
```

### Veritabanı Yedekleme
```bash
# Yedek al
cp s2g_game.db s2g_game_backup_$(date +%Y%m%d).db

# Geri yükle
cp s2g_game_backup_20240101.db s2g_game.db
sudo systemctl restart s2g-game
```

---

## 🔒 Güvenlik

### Firewall
```bash
# Durumu kontrol
sudo ufw status

# Port aç
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp

# Aktif et
sudo ufw enable
```

### Fail2Ban
```bash
# Durum
sudo fail2ban-client status

# SSH koruması
sudo fail2ban-client status sshd

# Ban listesi
sudo fail2ban-client get sshd banned
```

---

## 🐛 Sorun Giderme

### Site Açılmıyor
```bash
# 1. Service çalışıyor mu?
sudo systemctl status s2g-game

# 2. Port dinleniyor mu?
sudo netstat -tulpn | grep :8000

# 3. Nginx çalışıyor mu?
sudo systemctl status nginx

# 4. Logları kontrol et
sudo journalctl -u s2g-game -n 50
tail -f /home/s2guser/s2g-game/logs/gunicorn-error.log
```

### 502 Bad Gateway
```bash
# Gunicorn çalışmıyor olabilir
sudo systemctl restart s2g-game
sudo systemctl status s2g-game
```

### SSL Hatası
```bash
# Sertifikayı yenile
sudo certbot renew --force-renewal
sudo systemctl reload nginx
```

### Yüksek CPU/RAM Kullanımı
```bash
# Worker sayısını azalt
nano /home/s2guser/s2g-game/gunicorn_config.py
# workers = 2  # Azalt
sudo systemctl restart s2g-game
```

---

## 📞 Hızlı Komutlar

### Tek Satırda Deployment
```bash
curl -sSL https://raw.githubusercontent.com/yourusername/s2g-game/main/deploy_to_vps.sh | bash
```

### Hızlı Yeniden Başlatma
```bash
sudo systemctl restart s2g-game && sudo systemctl reload nginx
```

### Tüm Logları Temizle
```bash
sudo truncate -s 0 /var/log/nginx/*.log
sudo truncate -s 0 /home/s2guser/s2g-game/logs/*.log
```

### Disk Alanı Temizleme
```bash
# Eski logları sil
sudo find /var/log -type f -name "*.log" -mtime +30 -delete

# Eski yedekleri sil
find /home/s2guser/backups -name "*.db" -mtime +7 -delete

# APT cache temizle
sudo apt clean
sudo apt autoremove -y
```

---

## 🎯 Performans Optimizasyonu

### Gunicorn Workers
```python
# gunicorn_config.py
import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1  # Optimal
```

### Nginx Cache
```nginx
# /etc/nginx/sites-available/s2g-game
location /static {
    alias /home/s2guser/s2g-game/static;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### Database Optimization
```bash
# SQLite optimize
sqlite3 s2g_game.db "VACUUM;"
sqlite3 s2g_game.db "ANALYZE;"
```

---

## 📱 Mobil Erişim Test

```bash
# Ngrok ile test (geliştirme)
ngrok http 8000

# Gerçek domain ile
curl -I https://yourdomain.com
```

---

## ✅ Deployment Checklist

- [ ] VPS satın alındı
- [ ] Domain satın alındı ve DNS ayarlandı
- [ ] SSH erişimi sağlandı
- [ ] Sistem güncellemeleri yapıldı
- [ ] Gerekli paketler yüklendi
- [ ] Proje dosyaları yüklendi
- [ ] Python ortamı hazırlandı
- [ ] Nginx yapılandırıldı
- [ ] SSL sertifikası alındı
- [ ] Systemd service oluşturuldu
- [ ] Firewall ayarlandı
- [ ] Yedekleme scripti kuruldu
- [ ] Site test edildi
- [ ] Admin şifresi değiştirildi
- [ ] Monitoring kuruldu

---

## 🎉 Başarılı!

Site canlı: https://yourdomain.com

**Önemli Linkler:**
- Ana Sayfa: https://yourdomain.com
- Admin Panel: https://yourdomain.com/admin
- Ürünler: https://yourdomain.com/products

**Varsayılan Admin:**
- Kullanıcı: admin
- Şifre: admin123 (Değiştirin!)

Mohawk Development 🦅
