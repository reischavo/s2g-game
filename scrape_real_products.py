#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerçek Oyun Hesabı Sitelerinden Ürün ve Görsel Çekme
GameSatış, ItemSatış, GameMarkt API/Scraping
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from app import app, db, Product

# User Agent - Bot olarak algılanmamak için
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0'
}

def scrape_gamesatis():
    """GameSatış sitesinden ürün çekme"""
    print("🔍 GameSatış sitesinden ürünler çekiliyor...")
    
    try:
        # GameSatış ana sayfa
        url = "https://www.gamesatis.com"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Ürün kartlarını bul
            products = []
            product_cards = soup.find_all('div', class_=['product-card', 'product-item', 'item'])
            
            for card in product_cards[:20]:  # İlk 20 ürün
                try:
                    # Başlık
                    title_elem = card.find(['h3', 'h4', 'a'], class_=['title', 'product-title'])
                    title = title_elem.text.strip() if title_elem else None
                    
                    # Fiyat
                    price_elem = card.find(['span', 'div'], class_=['price', 'product-price'])
                    price_text = price_elem.text.strip() if price_elem else "0"
                    price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
                    
                    # Görsel
                    img_elem = card.find('img')
                    image_url = img_elem.get('src') or img_elem.get('data-src') if img_elem else None
                    
                    # Link
                    link_elem = card.find('a')
                    product_link = link_elem.get('href') if link_elem else None
                    
                    if title and price > 0:
                        products.append({
                            'title': title,
                            'price': price,
                            'image_url': image_url,
                            'link': product_link,
                            'source': 'GameSatış'
                        })
                        print(f"✅ {title} - {price}₺")
                
                except Exception as e:
                    print(f"⚠️ Ürün parse hatası: {e}")
                    continue
            
            return products
        else:
            print(f"❌ GameSatış erişim hatası: {response.status_code}")
            return []
    
    except Exception as e:
        print(f"❌ GameSatış scraping hatası: {e}")
        return []

def scrape_itemsatis():
    """ItemSatış sitesinden ürün çekme"""
    print("\n🔍 ItemSatış sitesinden ürünler çekiliyor...")
    
    try:
        url = "https://www.itemsatis.com"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            product_cards = soup.find_all('div', class_=['product', 'item', 'listing'])
            
            for card in product_cards[:20]:
                try:
                    title_elem = card.find(['h3', 'h4', 'a'])
                    title = title_elem.text.strip() if title_elem else None
                    
                    price_elem = card.find(['span', 'div'], class_=['price'])
                    price_text = price_elem.text.strip() if price_elem else "0"
                    price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
                    
                    img_elem = card.find('img')
                    image_url = img_elem.get('src') or img_elem.get('data-src') if img_elem else None
                    
                    if title and price > 0:
                        products.append({
                            'title': title,
                            'price': price,
                            'image_url': image_url,
                            'source': 'ItemSatış'
                        })
                        print(f"✅ {title} - {price}₺")
                
                except Exception as e:
                    continue
            
            return products
        else:
            print(f"❌ ItemSatış erişim hatası: {response.status_code}")
            return []
    
    except Exception as e:
        print(f"❌ ItemSatış scraping hatası: {e}")
        return []

def scrape_gamemarkt():
    """GameMarkt sitesinden ürün çekme"""
    print("\n🔍 GameMarkt sitesinden ürünler çekiliyor...")
    
    try:
        url = "https://www.gamemarkt.com"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            product_cards = soup.find_all('div', class_=['product', 'item'])
            
            for card in product_cards[:20]:
                try:
                    title_elem = card.find(['h3', 'h4', 'a'])
                    title = title_elem.text.strip() if title_elem else None
                    
                    price_elem = card.find(['span', 'div'], class_=['price'])
                    price_text = price_elem.text.strip() if price_elem else "0"
                    price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
                    
                    img_elem = card.find('img')
                    image_url = img_elem.get('src') or img_elem.get('data-src') if img_elem else None
                    
                    if title and price > 0:
                        products.append({
                            'title': title,
                            'price': price,
                            'image_url': image_url,
                            'source': 'GameMarkt'
                        })
                        print(f"✅ {title} - {price}₺")
                
                except Exception as e:
                    continue
            
            return products
        else:
            print(f"❌ GameMarkt erişim hatası: {response.status_code}")
            return []
    
    except Exception as e:
        print(f"❌ GameMarkt scraping hatası: {e}")
        return []

def detect_game_from_title(title):
    """Başlıktan oyun adını tespit et"""
    title_lower = title.lower()
    
    if 'pubg' in title_lower or 'mobile' in title_lower:
        return 'PUBG Mobile'
    elif 'valorant' in title_lower:
        return 'Valorant'
    elif 'lol' in title_lower or 'league' in title_lower:
        return 'League of Legends'
    elif 'cs2' in title_lower or 'cs:go' in title_lower or 'counter' in title_lower:
        return 'CS2'
    elif 'clash' in title_lower or 'coc' in title_lower:
        return 'Clash of Clans'
    elif 'discord' in title_lower:
        return 'Discord'
    elif 'fortnite' in title_lower:
        return 'Fortnite'
    elif 'minecraft' in title_lower:
        return 'Minecraft'
    else:
        return 'Diğer'

def detect_rank_from_title(title):
    """Başlıktan rank tespit et"""
    title_lower = title.lower()
    
    # PUBG Mobile
    if 'conqueror' in title_lower:
        return 'Conqueror'
    elif 'ace' in title_lower:
        return 'Ace'
    elif 'crown' in title_lower:
        return 'Crown'
    
    # Valorant
    elif 'radiant' in title_lower:
        return 'Radiant'
    elif 'immortal' in title_lower:
        return 'Immortal'
    elif 'ascendant' in title_lower:
        return 'Ascendant'
    
    # LOL
    elif 'challenger' in title_lower:
        return 'Challenger'
    elif 'master' in title_lower:
        return 'Master'
    elif 'diamond' in title_lower:
        return 'Diamond'
    
    # CS2
    elif 'global' in title_lower:
        return 'Global Elite'
    elif 'supreme' in title_lower:
        return 'Supreme'
    
    # COC
    elif 'th15' in title_lower:
        return 'TH15'
    elif 'th14' in title_lower:
        return 'TH14'
    
    else:
        return 'Premium'

def create_products_from_scraped_data(scraped_products):
    """Çekilen ürünleri veritabanına ekle"""
    with app.app_context():
        # Mevcut ürünleri temizle
        Product.query.delete()
        db.session.commit()
        
        added_count = 0
        
        for product_data in scraped_products:
            try:
                # Oyun ve rank tespit et
                game = detect_game_from_title(product_data['title'])
                rank = detect_rank_from_title(product_data['title'])
                
                # Açıklama oluştur
                description = f"""✅ {game} Hesabı
✅ {rank} Rank/Seviye
✅ Güvenli Teslimat
✅ Full Access
✅ Email Değiştirilebilir
✅ Anında Teslimat
✅ 7/24 Destek

📌 Kaynak: {product_data['source']}
📌 Orijinal İlan Kopyası"""
                
                # Ürün oluştur
                product = Product(
                    title=product_data['title'],
                    game=game,
                    category='Hesap',
                    description=description,
                    price=product_data['price'],
                    rank=rank,
                    region='TR',
                    image_url=product_data.get('image_url'),
                    stock=1,
                    seller_id=1  # Admin
                )
                
                db.session.add(product)
                added_count += 1
                
            except Exception as e:
                print(f"⚠️ Ürün ekleme hatası: {e}")
                continue
        
        db.session.commit()
        print(f"\n✅ {added_count} ürün veritabanına eklendi!")

def main():
    print("=" * 60)
    print("🎮 GERÇEK OYUN HESABI SİTELERİNDEN ÜRÜN ÇEKME")
    print("=" * 60)
    
    all_products = []
    
    # GameSatış'tan çek
    gamesatis_products = scrape_gamesatis()
    all_products.extend(gamesatis_products)
    time.sleep(2)  # Rate limiting
    
    # ItemSatış'tan çek
    itemsatis_products = scrape_itemsatis()
    all_products.extend(itemsatis_products)
    time.sleep(2)
    
    # GameMarkt'tan çek
    gamemarkt_products = scrape_gamemarkt()
    all_products.extend(gamemarkt_products)
    
    print(f"\n📊 Toplam {len(all_products)} ürün çekildi")
    
    if all_products:
        # Veritabanına ekle
        create_products_from_scraped_data(all_products)
        
        # JSON olarak kaydet
        with open('scraped_products.json', 'w', encoding='utf-8') as f:
            json.dump(all_products, f, ensure_ascii=False, indent=2)
        print("✅ Ürünler scraped_products.json dosyasına kaydedildi")
    else:
        print("❌ Hiç ürün çekilemedi!")
        print("\n💡 Alternatif Çözümler:")
        print("1. Manuel ürün ekleme scripti çalıştır")
        print("2. Gerçek hesap screenshot'ları yükle")
        print("3. API key al ve resmi API kullan")

if __name__ == '__main__':
    main()
