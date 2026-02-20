@echo off
chcp 65001 >nul
echo ========================================
echo GERÇEK GÖRSEL EKLEME - S2G GAME
echo ========================================
echo.
echo Gerçek oyun hesabı görselleri ile
echo ürünler oluşturuluyor...
echo.

python create_products_with_real_images.py

echo.
echo ========================================
echo.
echo ✅ Ürünler oluşturuldu!
echo.
echo 💡 Görselleri değiştirmek için:
echo    1. static/images/products/ klasörüne
echo       gerçek hesap screenshot'larını ekle
echo    2. Admin panelden ürün görsellerini güncelle
echo.
pause
