#!/bin/bash

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║           🎮 S2G GAME - SUNUCU BAŞLATILIYOR 🎮            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Bağımlılık kontrolü
echo -e "${YELLOW}🔍 Bağımlılıklar kontrol ediliyor...${NC}"
python3 -c "import flask, flask_sqlalchemy, flask_socketio" 2>/dev/null

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ HATA: Bağımlılıklar yüklü değil!${NC}"
    echo ""
    echo "Önce ./install.sh dosyasını çalıştırın:"
    echo "  chmod +x install.sh"
    echo "  ./install.sh"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Bağımlılıklar tamam!${NC}"
echo ""
echo -e "${YELLOW}🚀 Sunucu başlatılıyor...${NC}"
echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Sunucu Adresi: http://localhost:5000                      ║"
echo "║  Admin Panel:   http://localhost:5000/admin                ║"
echo "║  Admin Hesap:   admin / admin123                           ║"
echo "║                                                             ║"
echo "║  Durdurmak için: CTRL + C                                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

python3 app.py
