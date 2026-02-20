#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerçekçi Ürün Oluşturucu - S2G Game
PlayerAuctions, G2A, Eneba tarzı profesyonel ürünler
"""

from app import app, db, Product
from datetime import datetime

def create_realistic_products():
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
                'description': '✅ Conqueror Rank\n✅ 8500+ UC Bakiye\n✅ 150+ Rare Skin\n✅ Glacier M416 (Legendary)\n✅ Fool M416, AKM Skins\n✅ 50+ Emote\n✅ Mythic Outfits\n✅ Level 85\n✅ 2.5+ KD Ratio\n✅ Anında Teslimat\n✅ Full Access - Email Değiştirilebilir',
                'price': 2499.99,
                'rank': 'Conqueror',
                'region': 'TR',
                'image_url': 'https://i.imgur.com/8YqZQYJ.png',
                'stock': 1
            },
            {
                'title': 'PUBG Mobile Ace Hesabı | 5000 UC | 80+ Skin | Pharaoh X-Suit',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': '✅ Ace Rank (Season 30)\n✅ 5000 UC Bakiye\n✅ 80+ Premium Skin\n✅ Pharaoh X-Suit\n✅ Groza, M416 Skins\n✅ 30+ Emote\n✅ Level 70\n✅ 2.0+ KD\n✅ Full Access',
                'price': 1299.99,
                'rank': 'Ace',
                'region': 'TR',
                'image_url': 'https://i.imgur.com/8YqZQYJ.png',
                'stock': 3
            },
            {
                'title': 'PUBG Mobile Crown Hesabı | 2000 UC | 40+ Skin | Starter Pack',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': '✅ Crown V Rank\n✅ 2000 UC\n✅ 40+ Skin\n✅ M416, AKM Skins\n✅ Level 50\n✅ 1.5+ KD\n✅ Temiz Hesap',
                'price': 599.99,
                'rank': 'Crown',
                'region': 'TR',
                'image_url': 'https://i.imgur.com/8YqZQYJ.png',
                'stock': 5
            },
            
            # Valorant
            {
                'title': 'Valorant Radiant Hesabı | 200+ Skin | Reaver, Prime, Elderflame',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': '✅ Radiant Rank (Peak)\n✅ 200+ Premium Skin\n✅ Reaver Vandal\n✅ Prime Vandal\n✅ Elderflame Operator\n✅ Champions Vandal\n✅ Tüm Agentler Açık\n✅ 15000+ VP Harcama\n✅ Full Access\n✅ Email Değiştirilebilir',
                'price': 3499.99,
                'rank': 'Radiant',
                'region': 'TR',
                'image_url': 'https://i.imgur.com/9TztxGb.png',
                'stock': 1
            },
            {
                'title': 'Valorant Immortal 3 Hesabı | 120+ Skin | Prime, Reaver Collection',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': '✅ Immortal 3\n✅ 120+ Skin\n✅ Prime Collection\n✅ Reaver Collection\n✅ Tüm Agentler\n✅ 8000+ VP Harcama\n✅ Full Access',
                'price': 1999.99,
                'rank': 'Immortal',
                'region': 'TR',
                'image_url': 'https://i.imgur.com/9TztxGb.png',
                'stock': 2
            },
            {
                'title': 'Valorant Ascendant Hesabı | 60+ Skin | Prime Vandal, Phantom',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': '✅ Ascendant 2\n✅ 60+ Skin\n✅ Prime Vandal\n✅ Prime Phantom\n✅ Tüm Agentler\n✅ Full Access',
                'price': 899.99,
                'rank': 'Ascendant',
                'region': 'TR',
                'image_url': 'https://i.imgur.com/9TztxGb.png',
                'stock': 4
            },
            
            # League of Legends
            {
                'title': 'LOL Challenger Hesabı | 300+ Skin | Prestige, Mythic | Tüm Şampiyonlar',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': '✅ Challenger Rank\n✅ 300+ Premium Skin\n✅ 15+ Prestige Skin\n✅ 20+ Mythic Skin\n✅ Tüm Şampiyonlar (165+)\n✅ 50000+ RP Harcama\n✅ Honor Level 5\n✅ Full Access\n✅ Email Değiştirilebilir',
                'price': 4999.99,
                'rank': 'Challenger',
                'region': 'TR',
                'image_url': 'https://i.imgur.com/xqJ8bMH.png',
                'stock': 1
            },
            {
                'title': 'LOL Master Hesabı | 180+ Skin | Prestige Collection | 150+ Şampiyon',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': '✅ Master Rank\n✅ 180+ Skin\n✅ 8+ Prestige\n✅ 150+ Şampiyon\n✅ 25000+ RP\n✅ Honor 4\n✅ Full Access',
                'price': 2499.99,
                'rank': 'Master',
                'region': 'TR',
                'image_url': 'https://i.imgur.com/xqJ8bMH.png',
                'stock': 2
            },
            
            # CS2
            {
                'title': 'CS2 Global Elite Hesabı | 15000+ Saat | Prime | Rare Skins',
                'game': 'CS2',
                'category': 'Hesap',
                'description': '✅ Global Elite\n✅ 15000+ Saat\n✅ Prime Status\n✅ Rare Skins\n✅ Knife Skin\n✅ 5 Yıllık Coin\n✅ Full Access',
                'price': 1899.99,
                'rank': 'Global Elite',
                'region': 'EU',
                'image_url': 'https://i.imgur.com/kMDLPzF.png',
                'stock': 2
            },
            
            # Clash of Clans
            {
                'title': 'Clash of Clans TH15 Max Hesabı | 8000+ Gem | Full Troops',
                'game': 'Clash of Clans',
                'category': 'Hesap',
                'description': '✅ Town Hall 15 Max\n✅ 8000+ Gem\n✅ Tüm Askerler Max\n✅ Tüm Kahramanlar Max\n✅ Champion League\n✅ Full Access',
                'price': 1599.99,
                'rank': 'TH15',
                'region': 'Global',
                'image_url': 'https://i.imgur.com/7KjU8xL.png',
                'stock': 3
            },
            
            # Discord
            {
                'title': 'Discord Nitro Hesabı | 2 Yıllık | Full Boost | Rare Username',
                'game': 'Discord',
                'category': 'Hesap',
                'description': '✅ 2 Yıllık Nitro\n✅ Full Boost\n✅ Rare Username\n✅ 2018 Hesap\n✅ Full Access',
                'price': 299.99,
                'rank': 'Nitro',
                'region': 'Global',
                'image_url': 'https://i.imgur.com/vXXiXKj.png',
                'stock': 5
            },
            
            # Fortnite
            {
                'title': 'Fortnite OG Hesabı | 500+ Skin | Renegade Raider | Black Knight',
                'game': 'Fortnite',
                'category': 'Hesap',
                'description': '✅ 500+ Skin\n✅ Renegade Raider\n✅ Black Knight\n✅ OG Skins\n✅ 200+ Emote\n✅ Full Access',
                'price': 3999.99,
                'rank': 'OG Account',
                'region': 'Global',
                'image_url': 'https://i.imgur.com/mK3S8rP.png',
                'stock': 1
            },
            
            # Minecraft
            {
                'title': 'Minecraft Premium Hesabı | Full Access | Cape | Hypixel Rank',
                'game': 'Minecraft',
                'category': 'Hesap',
                'description': '✅ Premium Account\n✅ Full Access\n✅ Cape\n✅ Hypixel VIP+\n✅ Email Değiştirilebilir',
                'price': 199.99,
                'rank': 'Premium',
                'region': 'Global',
                'image_url': 'https://i.imgur.com/Ekj0Eu4.png',
                'stock': 10
            }
        ]
        
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f'✅ {len(products)} gerçekçi ürün oluşturuldu!')
        print('✅ PlayerAuctions, G2A, Eneba tarzı profesyonel ürünler')

if __name__ == '__main__':
    create_realistic_products()
