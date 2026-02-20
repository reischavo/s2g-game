@echo off
chcp 65001 >nul
echo ========================================
echo GERÇEK ÜRÜN ÇEKME - S2G GAME
echo ========================================
echo.
echo GameSatış, ItemSatış, GameMarkt sitelerinden
echo gerçek ürün ilanları çekiliyor...
echo.

python scrape_real_products.py

echo.
echo ========================================
pause
