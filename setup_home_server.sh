#!/bin/bash

# S2G Game - Ev Sunucusu Kurulum Scripti

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║      🏠 S2G GAME - EV SUNUCUSU KURULUMU 🏠                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo "Bu script sitenizi kendi bilgisayarınızda çalıştırmanıza yardımcı olur."
echo ""
read -p "Devam etmek için Enter'a basın..."

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 1: KURULUM YÖNTEMİ SEÇİN${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "1. Cloudflare Tunnel (Önerilen - En Kolay)"
echo "2. Port Forwarding + Dynamic DNS (Hızlı)"
echo "3. Ngrok (Hızlı Test)"
echo "4. Sadece Lokal Kurulum"
echo ""
read -p "Seçiminiz (1-4): " method

case $method in
    1)
        echo ""
        echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${YELLOW} CLOUDFLARE TUNNEL KURULUMU${NC}"
        echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        echo "📝 Gereksinimler:"
        echo "   1. Cloudflare hesabı (ücretsiz)"
        echo "   2. Domain (Cloudflare'e eklenmiş)"
        echo ""
        read -p "Devam etmek için Enter'a basın..."
        
        # Cloudflared yükle
        echo ""
        echo "📥 Cloudflared yükleniyor..."
        
        if ! command -v cloudflared &> /dev/null; then
            if [[ "$OSTYPE" == "linux-gnu"* ]]; then
                wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
                sudo dpkg -i cloudflared-linux-amd64.deb
                rm cloudflared-linux-amd64.deb
            elif [[ "$OSTYPE" == "darwin"* ]]; then
                brew install cloudflared
            fi
        fi
        
        echo -e "${GREEN}✅ Cloudflared yüklendi!${NC}"
        
        # Login
        echo ""
        echo "🔐 Cloudflare'e giriş yapılıyor..."
        cloudflared tunnel login
        
        # Tunnel oluştur
        echo ""
        read -p "Domain adınız (örn: example.com): " domain
        read -p "Tunnel adı (örn: s2g-game): " tunnelname
        
        echo ""
        echo "🚇 Tunnel oluşturuluyor..."
        cloudflared tunnel create $tunnelname
        
        # Config oluştur
        echo ""
        echo "📝 Config dosyası oluşturuluyor..."
        mkdir -p ~/.cloudflared
        
        TUNNEL_ID=$(cloudflared tunnel list | grep $tunnelname | awk '{print $1}')
        
        cat > ~/.cloudflared/config.yml << EOF
tunnel: $TUNNEL_ID
credentials-file: $HOME/.cloudflared/$TUNNEL_ID.json

ingress:
  - hostname: $domain
    service: http://localhost:5000
  - hostname: www.$domain
    service: http://localhost:5000
  - service: http_status:404
EOF
        
        # DNS route
        echo ""
        echo "🌐 DNS route ekleniyor..."
        cloudflared tunnel route dns $tunnelname $domain
        cloudflared tunnel route dns $tunnelname www.$domain
        
        # Service olarak kur
        echo ""
        echo "🔧 Service olarak kuruluyor..."
        sudo cloudflared service install
        
        echo ""
        echo -e "${GREEN}✅ Cloudflare Tunnel kurulumu tamamlandı!${NC}"
        echo ""
        echo "🌐 Siteniz: https://$domain"
        echo ""
        
        CLOUDFLARE_SETUP=true
        ;;
        
    2)
        echo ""
        echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${YELLOW} PORT FORWARDING KURULUMU${NC}"
        echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        echo "📝 Yapmanız gerekenler:"
        echo ""
        echo "1. BİLGİSAYARINIZIN IP ADRESİ:"
        ip addr show | grep "inet " | grep -v 127.0.0.1
        echo ""
        echo "2. MODEM/ROUTER ADMİN PANELİ:"
        echo "   - Genellikle: 192.168.1.1 veya 192.168.0.1"
        echo "   - Kullanıcı: admin"
        echo "   - Şifre: Modem üzerinde yazıyor"
        echo ""
        echo "3. PORT FORWARDING AYARLARI:"
        echo "   Dış Port: 80  → İç IP: [BİLGİSAYARINIZ] → İç Port: 5000"
        echo "   Dış Port: 443 → İç IP: [BİLGİSAYARINIZ] → İç Port: 5000"
        echo ""
        echo "4. DYNAMIC DNS (No-IP veya DuckDNS):"
        echo "   - https://www.noip.com/ veya"
        echo "   - https://www.duckdns.org/"
        echo ""
        read -p "Devam etmek için Enter'a basın..."
        ;;
        
    3)
        echo ""
        echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${YELLOW} NGROK KURULUMU${NC}"
        echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        
        # Ngrok yükle
        if ! command -v ngrok &> /dev/null; then
            echo "📥 Ngrok yükleniyor..."
            
            if [[ "$OSTYPE" == "linux-gnu"* ]]; then
                curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
                echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
                sudo apt update && sudo apt install ngrok
            elif [[ "$OSTYPE" == "darwin"* ]]; then
                brew install ngrok/ngrok/ngrok
            fi
        fi
        
        echo ""
        read -p "Ngrok auth token'ınız: " ngrok_token
        
        echo ""
        echo "🔐 Ngrok yapılandırılıyor..."
        ngrok config add-authtoken $ngrok_token
        
        echo ""
        echo -e "${GREEN}✅ Ngrok hazır!${NC}"
        echo ""
        
        NGROK_SETUP=true
        ;;
esac

# Lokal kurulum
echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 2: LOKAL KURULUM${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

if [ ! -d "venv" ]; then
    echo "📦 Kurulum yapılıyor..."
    ./install.sh
fi

# Firewall
echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 3: FIREWALL AYARLARI${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""
read -p "Firewall'da port 5000'i açmak ister misiniz? (E/H): " firewall

if [[ $firewall == "E" || $firewall == "e" ]]; then
    echo ""
    echo "🔒 Firewall kuralı ekleniyor..."
    
    if command -v ufw &> /dev/null; then
        sudo ufw allow 5000/tcp
        echo -e "${GREEN}✅ UFW kuralı eklendi!${NC}"
    elif command -v firewall-cmd &> /dev/null; then
        sudo firewall-cmd --permanent --add-port=5000/tcp
        sudo firewall-cmd --reload
        echo -e "${GREEN}✅ Firewalld kuralı eklendi!${NC}"
    else
        echo -e "${YELLOW}⚠️  Firewall bulunamadı${NC}"
    fi
fi

# Sunucu başlat
echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW} ADIM 4: SUNUCU BAŞLATILIYOR${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo "🚀 Sunucu başlatılıyor..."
echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Lokal Erişim:  http://localhost:5000                      ║"
echo "║  Ağ Erişimi:    http://[BİLGİSAYAR_IP]:5000               ║"
echo "║  Admin Panel:   http://localhost:5000/admin                ║"
echo "║                                                             ║"
echo "║  Durdurmak için: CTRL + C                                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

if [ "$CLOUDFLARE_SETUP" = true ]; then
    echo ""
    echo "🌐 Cloudflare Tunnel başlatılıyor..."
    sudo systemctl start cloudflared
    echo ""
    echo -e "${GREEN}✅ Tunnel başlatıldı!${NC}"
    echo "🌐 Siteniz: https://$domain"
    echo ""
fi

if [ "$NGROK_SETUP" = true ]; then
    echo ""
    echo "🌐 Ngrok başlatılıyor..."
    gnome-terminal -- bash -c "ngrok http 5000; exec bash" 2>/dev/null || \
    xterm -e "ngrok http 5000" 2>/dev/null || \
    ngrok http 5000 &
    echo ""
    echo -e "${GREEN}✅ Ngrok başlatıldı!${NC}"
    echo "📝 Ngrok penceresindeki URL'i kullanın"
    echo ""
    sleep 2
fi

# Ana sunucuyu başlat
./start.sh
