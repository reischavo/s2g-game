#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerçek Oyun Pazaryeri Sitelerinden İlham Alınarak Ürün Oluşturma
PlayerAuctions, ItemSatış, GameMarkt tarzı
"""

from app import app, db, Product
from datetime import datetime

def create_marketplace_products():
    with app.app_context():
        # Önce mevcut ürünleri temizle
        Product.query.delete()
        db.session.commit()
        
        # Gerçek pazaryeri sitelerinden ilham alınmış ürünler
        products = [
            # PUBG Mobile - PlayerAuctions tarzı
            {
                'title': 'PUBG Mobile Conqueror | Glacier M416 | Fool M416 | 8500 UC | 150+ Skins',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': '''✅ Conqueror Rank (Season 30)
✅ 8500+ UC Bakiye
✅ Glacier M416 (Legendary)
✅ Fool M416 (Legendary)
✅ Hellfire AKM
✅ Pharaoh X-Suit
✅ 150+ Premium Skins
✅ 50+ Emotes
✅ Mythic Outfits
✅ Level 85
✅ 2.5+ KD Ratio
✅ Full Access
✅ Email Değiştirilebilir
✅ Anında Teslimat''',
                'price': 2499.99,
                'rank': 'Conqueror',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/800x400/1a1a2e/9d4edd?text=PUBG+Conqueror+Glacier+M416',
                'stock': 1
            },
            {
                'title': 'PUBG Mobile Ace | Pharaoh X-Suit | 5000 UC | 80+ Skins | Mythic',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': '''✅ Ace Rank
✅ 5000 UC
✅ Pharaoh X-Suit
✅ Groza Skins
✅ M416 Skins
✅ 80+ Skins
✅ 30+ Emotes
✅ Level 70
✅ 2.0+ KD
✅ Full Access''',
                'price': 1299.99,
                'rank': 'Ace',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/800x400/16213e/ff006e?text=PUBG+Ace+Pharaoh',
                'stock': 3
            },
            {
                'title': 'PUBG Mobile Crown | 2000 UC | 40+ Skins | Starter Account',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': '''✅ Crown V
✅ 2000 UC
✅ 40+ Skins
✅ M416 Skins
✅ Level 50
✅ 1.5+ KD
✅ Clean Account''',
                'price': 599.99,
                'rank': 'Crown',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/800x400/0f3460/06ffa5?text=PUBG+Crown',
                'stock': 5
            },
            
            # Valorant - PlayerAuctions tarzı
            {
                'title': 'Valorant Radiant | Reaver Vandal | Prime Collection | 200+ Skins',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': '''✅ Radiant Peak
✅ 200+ Skins
✅ Reaver Vandal
✅ Prime Vandal
✅ Elderflame Operator
✅ Champions Vandal
✅ All Agents
✅ 15000+ VP Spent
✅ Full Access''',
                'price': 3499.99,
                'rank': 'Radiant',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/800x400/ff4655/ffffff?text=Valorant+Radiant+Reaver',
                'stock': 1
            },
            {
                'title': 'Valorant Immortal 3 | Prime Vandal | 120+ Skins | All Agents',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': '''✅ Immortal 3
✅ 120+ Skins
✅ Prime Collection
✅ Reaver Collection
✅ All Agents
✅ 8000+ VP
✅ Full Access''',
                'price': 1999.99,
                'rank': 'Immortal',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/800x400/fd4556/000000?text=Valorant+Immortal',
                'stock': 2
            },
            {
                'title': 'Valorant Ascendant | Prime Vandal + Phantom | 60+ Skins',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': '''✅ Ascendant 2
✅ 60+ Skins
✅ Prime Vandal
✅ Prime Phantom
✅ All Agents
✅ Full Access''',
                'price': 899.99,
                'rank': 'Ascendant',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/800x400/ff4655/ffffff?text=Valorant+Ascendant',
                'stock': 4
            },
            
            # League of Legends
            {
                'title': 'LOL Challenger | 300+ Skins | 15 Prestige | All Champions',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': '''✅ Challenger
✅ 300+ Skins
✅ 15+ Prestige
✅ 20+ Mythic
✅ All Champions
✅ 50000+ RP
✅ Honor 5
✅ Full Access''',
                'price': 4999.99,
                'rank': 'Challenger',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/800x400/0ac8b9/c89b3c?text=LOL+Challenger',
                'stock': 1
            },
            {
                'title': 'LOL Master | 180+ Skins | Prestige Collection | 150 Champions',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': '''✅ Master
✅ 180+ Skins
✅ 8+ Prestige
✅ 150+ Champions
✅ 25000+ RP
✅ Honor 4''',
                'price': 2499.99,
                'rank': 'Master',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/800x400/0397ab/ffffff?text=LOL+Master',
                'stock': 2
            },
            
            # CS2
            {
                'title': 'CS2 Global Elite | 15000+ Hours | Prime | Knife + Rare Skins',
                'game': 'CS2',
                'category': 'Hesap',
                'description': '''✅ Global Elite
✅ 15000+ Hours
✅ Prime Status
✅ Knife Skin
✅ Rare Skins
✅ 5 Year Coin
✅ Full Access''',
                'price': 1899.99,
                'rank': 'Global Elite',
                'region': 'EU',
                'image_url': 'https://via.placeholder.com/800x400/f7b731/000000?text=CS2+Global+Elite',
                'stock': 2
            },
            
            # Clash of Clans
            {
                'title': 'Clash of Clans TH15 Max | 8000 Gems | All Troops Max',
                'game': 'Clash of Clans',
                'category': 'Hesap',
                'description': '''✅ TH15 Max
✅ 8000+ Gems
✅ All Troops Max
✅ All Heroes Max
✅ Champion League
✅ Full Access''',
                'price': 1599.99,
                'rank': 'TH15',
                'region': 'Global',
                'image_url': 'https://via.placeholder.com/800x400/ff6b6b/ffd700?text=COC+TH15',
                'stock': 3
            },
            
            # Discord
            {
                'title': 'Discord Nitro 2 Years | Full Boost | Rare Username | 2018 Account',
                'game': 'Discord',
                'category': 'Hesap',
                'description': '''✅ 2 Year Nitro
✅ Full Boost
✅ Rare Username
✅ 2018 Account
✅ Full Access''',
                'price': 299.99,
                'rank': 'Nitro',
                'region': 'Global',
                'image_url': 'https://via.placeholder.com/800x400/5865f2/ffffff?text=Discord+Nitro',
                'stock': 5
            },
            
            # Fortnite
            {
                'title': 'Fortnite OG Account | 500+ Skins | Renegade Raider | Black Knight',
                'game': 'Fortnite',
                'category': 'Hesap',
                'description': '''✅ 500+ Skins
✅ Renegade Raider
✅ Black Knight
✅ OG Skins
✅ 200+ Emotes
✅ Full Access''',
                'price': 3999.99,
                'rank': 'OG Account',
                'region': 'Global',
                'image_url': 'https://via.placeholder.com/800x400/00d9ff/000000?text=Fortnite+OG',
                'stock': 1
            },
            
            # Minecraft
            {
                'title': 'Minecraft Premium | Full Access | Cape | Hypixel VIP+',
                'game': 'Minecraft',
                'category': 'Hesap',
                'description': '''✅ Premium
✅ Full Access
✅ Cape
✅ Hypixel VIP+
✅ Email Change''',
                'price': 199.99,
                'rank': 'Premium',
                'region': 'Global',
                'image_url': 'https://via.placeholder.com/800x400/8b4513/654321?text=Minecraft+Premium',
                'stock': 10
            }
        ]
        
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f'✅ {len(products)} ürün oluşturuldu!')
        print('✅ PlayerAuctions, ItemSatış, GameMarkt tarzı')
        print('✅ Gerçek pazaryeri formatında')
        print('✅ Placeholder görseller (gerçek görseller eklenebilir)')

if __name__ == '__main__':
    create_marketplace_products()
