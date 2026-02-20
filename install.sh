#!/bin/bash

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║          🎮 S2G GAME - KURULUM BAŞLATILIYOR 🎮            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Python kontrolü
echo -e "${YELLOW}[1/4] Python versiyonu kontrol ediliyor...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ HATA: Python3 bulunamadı!${NC}"
    echo ""
    echo "Python 3.8 veya üzeri yüklü olmalıdır."
    echo ""
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "MacOS: brew install python3"
    exit 1
fi

python3 --version

# pip kontrolü
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ HATA: pip3 bulunamadı!${NC}"
    echo ""
    echo "Ubuntu/Debian: sudo apt install python3-pip"
    echo "MacOS: brew install python3"
    exit 1
fi

# pip güncelleme
echo ""
echo -e "${YELLOW}[2/4] pip güncelleniyor...${NC}"
python3 -m pip install --upgrade pip

# Bağımlılıkları yükleme
echo ""
echo -e "${YELLOW}[3/4] Bağımlılıklar yükleniyor...${NC}"
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ HATA: Bağımlılıklar yüklenemedi!${NC}"
    exit 1
fi

# Klasörleri oluşturma
echo ""
echo -e "${YELLOW}[4/4] Klasörler oluşturuluyor...${NC}"
mkdir -p static/uploads/products

echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ KURULUM BAŞARIYLA TAMAMLANDI! ✅           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo "📝 Sonraki Adımlar:"
echo ""
echo "1. ./start.sh dosyasını çalıştırın"
echo "2. Tarayıcınızda http://localhost:5000 adresini açın"
echo "3. Admin hesabı: admin / admin123"
echo ""
echo "💡 İpucu: Örnek ürünler eklemek için:"
echo "   python3 add_sample_products.py"
echo ""
