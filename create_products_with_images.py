#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GameSatış Tarzı Gerçek Ürünler - Görsellerle
"""

from app import app, db, Product
from datetime import datetime

def create_products_with_real_images():
    with app.app_context():
        # Önce mevcut ürünleri temizle
        Product.query.delete()
        db.session.commit()
        
        products = [
            # PUBG Mobile - Sponsor Oyun
            {
                'title': 'PUBG Mobile Conqueror Hesabı | 8500+ UC | 150+ Skin | Glacier M416',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': '''✅ Conqueror Rank (Season 30)
✅ 8500+ UC Bakiye
✅ 150+ Rare Skin
✅ Glacier M416 (Legendary)
✅ Fool M416, AKM Skins
✅ 50+ Emote
✅ Mythic Outfits
✅ Level 85
✅ 2.5+ KD Ratio
✅ Anında Teslimat
✅ Full Access - Email Değiştirilebilir
✅ S2G Esports Garantisi''',
                'price': 2499.99,
                'rank': 'Conqueror',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1625805866449-3589fe3f71a3?w=800&h=400&fit=crop',
                'stock': 1
            },
            {
                'title': 'PUBG Mobile Ace Hesabı | 5000 UC | 80+ Skin | Pharaoh X-Suit',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': '''✅ Ace Rank (Season 30)
✅ 5000 UC Bakiye
✅ 80+ Premium Skin
✅ Pharaoh X-Suit
✅ Groza, M416 Skins
✅ 30+ Emote
✅ Level 70
✅ 2.0+ KD
✅ Full Access
✅ Anında Teslimat''',
                'price': 1299.99,
                'rank': 'Ace',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&h=400&fit=crop',
                'stock': 3
            },
            {
                'title': 'PUBG Mobile Crown Hesabı | 2000 UC | 40+ Skin | Starter Pack',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': '''✅ Crown V Rank
✅ 2000 UC
✅ 40+ Skin
✅ M416, AKM Skins
✅ Level 50
✅ 1.5+ KD
✅ Temiz Hesap
✅ Full Access''',
                'price': 599.99,
                'rank': 'Crown',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800&h=400&fit=crop',
                'stock': 5
            },
            
            # Valorant
            {
                'title': 'Valorant Radiant Hesabı | 200+ Skin | Reaver, Prime, Elderflame',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': '''✅ Radiant Rank (Peak)
✅ 200+ Premium Skin
✅ Reaver Vandal
✅ Prime Vandal
✅ Elderflame Operator
✅ Champions Vandal
✅ Tüm Agentler Açık
✅ 15000+ VP Harcama
✅ Full Access
✅ Email Değiştirilebilir''',
                'price': 3499.99,
                'rank': 'Radiant',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=800&h=400&fit=crop',
                'stock': 1
            },
            {
                'title': 'Valorant Immortal 3 Hesabı | 120+ Skin | Prime, Reaver Collection',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': '''✅ Immortal 3
✅ 120+ Skin
✅ Prime Collection
✅ Reaver Collection
✅ Tüm Agentler
✅ 8000+ VP Harcama
✅ Full Access''',
                'price': 1999.99,
                'rank': 'Immortal',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=800&h=400&fit=crop',
                'stock': 2
            },
            {
                'title': 'Valorant Ascendant Hesabı | 60+ Skin | Prime Vandal, Phantom',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': '''✅ Ascendant 2
✅ 60+ Skin
✅ Prime Vandal
✅ Prime Phantom
✅ Tüm Agentler
✅ Full Access''',
                'price': 899.99,
                'rank': 'Ascendant',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=800&h=400&fit=crop',
                'stock': 4
            },
            
            # League of Legends
            {
                'title': 'LOL Challenger Hesabı | 300+ Skin | Prestige, Mythic | Tüm Şampiyonlar',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': '''✅ Challenger Rank
✅ 300+ Premium Skin
✅ 15+ Prestige Skin
✅ 20+ Mythic Skin
✅ Tüm Şampiyonlar (165+)
✅ 50000+ RP Harcama
✅ Honor Level 5
✅ Full Access
✅ Email Değiştirilebilir''',
                'price': 4999.99,
                'rank': 'Challenger',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1625805866449-3589fe3f71a3?w=800&h=400&fit=crop',
                'stock': 1
            },
            {
                'title': 'LOL Master Hesabı | 180+ Skin | Prestige Collection | 150+ Şampiyon',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': '''✅ Master Rank
✅ 180+ Skin
✅ 8+ Prestige
✅ 150+ Şampiyon
✅ 25000+ RP
✅ Honor 4
✅ Full Access''',
                'price': 2499.99,
                'rank': 'Master',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800&h=400&fit=crop',
                'stock': 2
            },
            
            # CS2
            {
                'title': 'CS2 Global Elite Hesabı | 15000+ Saat | Prime | Rare Skins',
                'game': 'CS2',
                'category': 'Hesap',
                'description': '''✅ Global Elite
✅ 15000+ Saat
✅ Prime Status
✅ Rare Skins
✅ Knife Skin
✅ 5 Yıllık Coin
✅ Full Access''',
                'price': 1899.99,
                'rank': 'Global Elite',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&h=400&fit=crop',
                'stock': 2
            },
            
            # Clash of Clans
            {
                'title': 'Clash of Clans TH15 Max Hesabı | 8000+ Gem | Full Troops',
                'game': 'Clash of Clans',
                'category': 'Hesap',
                'description': '''✅ Town Hall 15 Max
✅ 8000+ Gem
✅ Tüm Askerler Max
✅ Tüm Kahramanlar Max
✅ Champion League
✅ Full Access''',
                'price': 1599.99,
                'rank': 'TH15',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=800&h=400&fit=crop',
                'stock': 3
            },
            
            # Discord
            {
                'title': 'Discord Nitro Hesabı | 2 Yıllık | Full Boost | Rare Username',
                'game': 'Discord',
                'category': 'Hesap',
                'description': '''✅ 2 Yıllık Nitro
✅ Full Boost
✅ Rare Username
✅ 2018 Hesap
✅ Full Access''',
                'price': 299.99,
                'rank': 'Nitro',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1614680376593-902f74cf0d41?w=800&h=400&fit=crop',
                'stock': 5
            },
            
            # Fortnite
            {
                'title': 'Fortnite OG Hesabı | 500+ Skin | Renegade Raider | Black Knight',
                'game': 'Fortnite',
                'category': 'Hesap',
                'description': '''✅ 500+ Skin
✅ Renegade Raider
✅ Black Knight
✅ OG Skins
✅ 200+ Emote
✅ Full Access''',
                'price': 3999.99,
                'rank': 'OG Account',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=800&h=400&fit=crop',
                'stock': 1
            },
            
            # Minecraft
            {
                'title': 'Minecraft Premium Hesabı | Full Access | Cape | Hypixel Rank',
                'game': 'Minecraft',
                'category': 'Hesap',
                'description': '''✅ Premium Account
✅ Full Access
✅ Cape
✅ Hypixel VIP+
✅ Email Değiştirilebilir''',
                'price': 199.99,
                'rank': 'Premium',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=800&h=400&fit=crop',
                'stock': 10
            }
        ]
        
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f'✅ {len(products)} ürün gerçek görsellerle oluşturuldu!')
        print('✅ Unsplash gaming görselleri kullanıldı')
        print('✅ GameSatış tarzı profesyonel ilanlar')

if __name__ == '__main__':
    create_products_with_real_images()
