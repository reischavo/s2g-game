#!/bin/bash

# S2G Game - VPS Otomatik Deployment Scripti
# Bu script tüm kurulum adımlarını otomatik yapar

set -e  # Hata durumunda dur

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║       🚀 S2G GAME - VPS DEPLOYMENT BAŞLATILIYOR 🚀        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Bilgileri al
read -p "Domain adınız (örn: example.com): " DOMAIN
read -p "Sunucu IP adresi: " SERVER_IP
read -p "SSH kullanıcı adı (varsayılan: root): " SSH_USER
SSH_USER=${SSH_USER:-root}

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 1: SUNUCUYA BAĞLANIYOR${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"

# SSH bağlantısı test et
if ssh -o ConnectTimeout=5 $SSH_USER@$SERVER_IP "echo 'Bağlantı başarılı'" 2>/dev/null; then
    echo -e "${GREEN}✅ SSH bağlantısı başarılı${NC}"
else
    echo -e "${RED}❌ SSH bağlantısı başarısız!${NC}"
    echo "Lütfen SSH anahtarınızı kontrol edin veya şifre ile bağlanın."
    exit 1
fi

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 2: SUNUCU HAZIRLANIY OR${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"

ssh $SSH_USER@$SERVER_IP << 'ENDSSH'
# Sistem güncelleme
echo "📦 Sistem güncelleniyor..."
apt update && apt upgrade -y

# Gerekli paketleri yükle
echo "📦 Gerekli paketler yükleniyor..."
apt install -y python3 python3-pip python3-venv nginx git supervisor ufw certbot python3-certbot-nginx fail2ban

# Kullanıcı oluştur
if ! id -u s2guser > /dev/null 2>&1; then
    echo "👤 s2guser kullanıcısı oluşturuluyor..."
    adduser --disabled-password --gecos "" s2guser
    usermod -aG sudo s2guser
    echo "s2guser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
fi

# Firewall ayarla
echo "🔒 Firewall ayarlanıyor..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

echo "✅ Sunucu hazır!"
ENDSSH

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 3: PROJE DOSYALARI YÜKLENIYOR${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"

# Proje dosyalarını yükle
echo "📤 Dosyalar sunucuya yükleniyor..."
ssh $SSH_USER@$SERVER_IP "mkdir -p /home/s2guser/s2g-game"
scp -r ./* $SSH_USER@$SERVER_IP:/home/s2guser/s2g-game/
ssh $SSH_USER@$SERVER_IP "chown -R s2guser:s2guser /home/s2guser/s2g-game"

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 4: PYTHON ORTAMI HAZIRLANIYOR${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"

ssh $SSH_USER@$SERVER_IP << ENDSSH
su - s2guser << 'ENDSU'
cd /home/s2guser/s2g-game

# Virtual environment
echo "🐍 Virtual environment oluşturuluyor..."
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
echo "📦 Python paketleri yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn eventlet

# Log klasörü
mkdir -p logs

echo "✅ Python ortamı hazır!"
ENDSU
ENDSSH

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 5: GUNICORN YAPILAN DIRIYOR${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"

# Gunicorn config oluştur
ssh $SSH_USER@$SERVER_IP "cat > /home/s2guser/s2g-game/gunicorn_config.py" << 'EOF'
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "eventlet"
worker_connections = 1000
timeout = 120
keepalive = 5
accesslog = "/home/s2guser/s2g-game/logs/gunicorn-access.log"
errorlog = "/home/s2guser/s2g-game/logs/gunicorn-error.log"
loglevel = "info"
proc_name = "s2g-game"
daemon = False
reload = False
EOF

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 6: NGINX YAPILAN DIRIYOR${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"

# Nginx config oluştur
ssh $SSH_USER@$SERVER_IP "cat > /etc/nginx/sites-available/s2g-game" << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    client_max_body_size 16M;
    
    location /static {
        alias /home/s2guser/s2g-game/static;
        expires 30d;
    }
    
    location /socket.io {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ssh $SSH_USER@$SERVER_IP << 'ENDSSH'
ln -sf /etc/nginx/sites-available/s2g-game /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx
ENDSSH

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 7: SYSTEMD SERVICE OLUŞTURULUYOR${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"

ssh $SSH_USER@$SERVER_IP "cat > /etc/systemd/system/s2g-game.service" << 'EOF'
[Unit]
Description=S2G Game Platform
After=network.target

[Service]
Type=notify
User=s2guser
Group=www-data
WorkingDirectory=/home/s2guser/s2g-game
Environment="PATH=/home/s2guser/s2g-game/venv/bin"
ExecStart=/home/s2guser/s2g-game/venv/bin/gunicorn -c gunicorn_config.py app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

ssh $SSH_USER@$SERVER_IP << 'ENDSSH'
systemctl daemon-reload
systemctl enable s2g-game
systemctl start s2g-game
ENDSSH

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 8: SSL SERTİFİKASI ALINIYOR${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"

read -p "SSL sertifikası almak ister misiniz? (E/H): " SSL_CHOICE
if [[ $SSL_CHOICE == "E" || $SSL_CHOICE == "e" ]]; then
    read -p "Email adresiniz: " EMAIL
    ssh $SSH_USER@$SERVER_IP "certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos -m $EMAIL"
    echo -e "${GREEN}✅ SSL sertifikası alındı!${NC}"
else
    echo -e "${YELLOW}⚠️  SSL sertifikası atlandı${NC}"
fi

echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║            ✅ DEPLOYMENT BAŞARIYLA TAMAMLANDI! ✅          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo ""
echo -e "${BLUE}📊 SİTE BİLGİLERİ:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ $SSL_CHOICE == "E" || $SSL_CHOICE == "e" ]]; then
    echo -e "🌐 Site Adresi: ${GREEN}https://$DOMAIN${NC}"
    echo -e "👨‍💼 Admin Panel: ${GREEN}https://$DOMAIN/admin${NC}"
else
    echo -e "🌐 Site Adresi: ${GREEN}http://$DOMAIN${NC}"
    echo -e "👨‍💼 Admin Panel: ${GREEN}http://$DOMAIN/admin${NC}"
fi
echo -e "👤 Admin Kullanıcı: ${YELLOW}admin${NC}"
echo -e "🔑 Admin Şifre: ${YELLOW}admin123${NC} ${RED}(Mutlaka değiştirin!)${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo -e "${BLUE}🔧 YARDIMCI KOMUTLAR:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Servisi yeniden başlat: ssh $SSH_USER@$SERVER_IP 'sudo systemctl restart s2g-game'"
echo "Durum kontrol: ssh $SSH_USER@$SERVER_IP 'sudo systemctl status s2g-game'"
echo "Logları görüntüle: ssh $SSH_USER@$SERVER_IP 'tail -f /home/s2guser/s2g-game/logs/gunicorn-error.log'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo -e "${GREEN}🎉 Başarılı deployment! İyi satışlar! 🎮${NC}"
