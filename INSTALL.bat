@echo off
chcp 65001 >nul
title S2G Game - Kurulum
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║          🎮 S2G GAME - KURULUM BAŞLATILIYOR 🎮            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [1/4] Python versiyonu kontrol ediliyor...
python --version
if errorlevel 1 (
    echo.
    echo ❌ HATA: Python bulunamadı!
    echo.
    echo Python 3.8 veya üzeri yüklü olmalıdır.
    echo İndirmek için: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo [2/4] pip güncelleniyor...
python -m pip install --upgrade pip

echo.
echo [3/4] Bağımlılıklar yükleniyor...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ HATA: Bağımlılıklar yüklenemedi!
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] Klasörler oluşturuluyor...
if not exist "static\uploads\products" mkdir static\uploads\products

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ KURULUM BAŞARIYLA TAMAMLANDI! ✅           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📝 Sonraki Adımlar:
echo.
echo 1. START.bat dosyasını çalıştırın
echo 2. Tarayıcınızda http://localhost:5000 adresini açın
echo 3. Admin hesabı: admin / admin123
echo.
echo 💡 İpucu: Örnek ürünler eklemek için:
echo    python add_sample_products.py
echo.
pause
