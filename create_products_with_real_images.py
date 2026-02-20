#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerçek Oyun Hesabı Görselleri ile Ürün Oluşturma
Unsplash, Pexels ve Gaming API'lerinden gerçek görsel çekme
"""

import requests
import json
from app import app, db, Product

# Unsplash API (Ücretsiz - gerçek oyun görselleri)
UNSPLASH_ACCESS_KEY = "YOUR_ACCESS_KEY"  # https://unsplash.com/developers

# Pexels API (Ücretsiz - gerçek oyun görselleri)
PEXELS_API_KEY = "YOUR_API_KEY"  # https://www.pexels.com/api/

def get_game_image_from_unsplash(game_name):
    """Unsplash'tan gerçek oyun görseli çek"""
    try:
        url = f"https://api.unsplash.com/search/photos"
        params = {
            'query': f'{game_name} gaming account',
            'per_page': 1,
            'orientation': 'landscape'
        }
        headers = {
            'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['urls']['regular']
    except:
        pass
    
    return None

def get_game_image_from_pexels(game_name):
    """Pexels'tan gerçek oyun görseli çek"""
    try:
        url = f"https://api.pexels.com/v1/search"
        params = {
            'query': f'{game_name} gaming',
            'per_page': 1,
            'orientation': 'landscape'
        }
        headers = {
            'Authorization': PEXELS_API_KEY
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                return data['photos'][0]['src']['large']
    except:
        pass
    
    return None

def get_game_screenshot_urls():
    """Gerçek oyun screenshot URL'leri - Manuel olarak toplanmış"""
    return {
        'PUBG Mobile': [
            'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800',
            'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=800',
            'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800'
        ],
        'Valorant': [
            'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800',
            'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=800'
        ],
        'League of Legends': [
            'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=800',
            'https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=800'
        ],
        'CS2': [
            'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800',
            'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=800'
        ],
        'Clash of Clans': [
            'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800'
        ],
        'Discord': [
            'https://images.unsplash.com/photo-1614680376593-902f74cf0d41?w=800'
        ],
        'Fortnite': [
            'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=800'
        ],
        'Minecraft': [
            'https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=800'
        ]
    }

def create_realistic_products():
    """Gerçek görseller ve detaylı bilgilerle ürün oluştur"""
    with app.app_context():
        # Mevcut ürünleri temizle
        Product.query.delete()
        db.session.commit()
        
        screenshot_urls = get_game_screenshot_urls()
        
        products = [
            # PUBG Mobile - Gerçekçi İlanlar
            {
                'title': '🔥 PUBG Mobile Conqueror | Glacier M416 | Fool M416 | 8500 UC | 150+ Skin',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': '''✅ Conqueror Rank (Season 30)
✅ 8500+ UC Bakiye
✅ Glacier M416 (Legendary) 🔥
✅ Fool M416 (Legendary) 🔥
✅ Hellfire AKM
✅ Pharaoh X-Suit
✅ 150+ Premium Skins
✅ 50+ Emotes
✅ Mythic Outfits
✅ Level 85
✅ 2.5+ KD Ratio
✅ Full Access
✅ Email Değiştirilebilir
✅ Anında Teslimat

📱 Hesap Detayları:
• Tüm skinler hesapta
• Email + şifre teslim
• Güvenli ödeme
• 7/24 destek

⚠️ NOT: Hesap satışı sonrası iade yoktur!''',
                'price': 2499.99,
                'rank': 'Conqueror',
                'region': 'TR',
                'image_url': screenshot_urls['PUBG Mobile'][0],
                'stock': 1
            },
            {
                'title': '⭐ PUBG Mobile Ace | Pharaoh X-Suit | 5000 UC | 80+ Skin | Mythic',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': '''✅ Ace Rank
✅ 5000 UC
✅ Pharaoh X-Suit ⭐
✅ Groza Skins
✅ M416 Skins
✅ 80+ Skins
✅ 30+ Emotes
✅ Level 70
✅ 2.0+ KD
✅ Full Access
✅ Email Değiştirilebilir

📱 Hesap Özellikleri:
• Temiz hesap
• Ban geçmişi yok
• Tüm bilgiler verilir
• Anında teslimat''',
                'price': 1299.99,
                'rank': 'Ace',
                'region': 'TR',
                'image_url': screenshot_urls['PUBG Mobile'][1],
                'stock': 3
            },
            {
                'title': '💎 PUBG Mobile Crown | 2000 UC | 40+ Skin | Starter Account',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': '''✅ Crown V
✅ 2000 UC
✅ 40+ Skins
✅ M416 Skins
✅ Level 50
✅ 1.5+ KD
✅ Clean Account
✅ Full Access

📱 Başlangıç Hesabı:
• Temiz geçmiş
• UC yüklü
• Email değiştirilebilir''',
                'price': 599.99,
                'rank': 'Crown',
                'region': 'TR',
                'image_url': screenshot_urls['PUBG Mobile'][2],
                'stock': 5
            },
            
            # Valorant - Gerçekçi İlanlar
            {
                'title': '🔥 Valorant Radiant | Reaver Vandal | Prime Collection | 200+ Skin',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': '''✅ Radiant Peak 🏆
✅ 200+ Skins
✅ Reaver Vandal 🔥
✅ Prime Vandal
✅ Elderflame Operator
✅ Champions Vandal
✅ All Agents Unlocked
✅ 15000+ VP Spent
✅ Full Access
✅ Email Değiştirilebilir

🎮 Hesap Detayları:
• Tüm agentlar açık
• Rare skin collection
• Competitive ready
• Ban geçmişi yok''',
                'price': 3499.99,
                'rank': 'Radiant',
                'region': 'TR',
                'image_url': screenshot_urls['Valorant'][0],
                'stock': 1
            },
            {
                'title': '⭐ Valorant Immortal 3 | Prime Vandal | 120+ Skin | All Agents',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': '''✅ Immortal 3
✅ 120+ Skins
✅ Prime Collection
✅ Reaver Collection
✅ All Agents
✅ 8000+ VP Spent
✅ Full Access
✅ Email Değiştirilebilir

🎮 Premium Hesap:
• High rank
• Rare skins
• Competitive ready''',
                'price': 1999.99,
                'rank': 'Immortal',
                'region': 'TR',
                'image_url': screenshot_urls['Valorant'][1],
                'stock': 2
            },
            
            # League of Legends
            {
                'title': '🏆 LOL Challenger | 300+ Skin | 15 Prestige | All Champions',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': '''✅ Challenger Rank 🏆
✅ 300+ Skins
✅ 15+ Prestige Skins
✅ 20+ Mythic Skins
✅ All Champions
✅ 50000+ RP Spent
✅ Honor Level 5
✅ Full Access

🎮 Premium Collection:
• Rare prestige skins
• All champions unlocked
• High honor level
• Clean account''',
                'price': 4999.99,
                'rank': 'Challenger',
                'region': 'TR',
                'image_url': screenshot_urls['League of Legends'][0],
                'stock': 1
            },
            {
                'title': '⭐ LOL Master | 180+ Skin | Prestige Collection | 150 Champions',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': '''✅ Master Rank
✅ 180+ Skins
✅ 8+ Prestige
✅ 150+ Champions
✅ 25000+ RP Spent
✅ Honor 4
✅ Full Access

🎮 High Rank Account:
• Master tier
• Prestige collection
• Many champions''',
                'price': 2499.99,
                'rank': 'Master',
                'region': 'TR',
                'image_url': screenshot_urls['League of Legends'][1],
                'stock': 2
            },
            
            # CS2
            {
                'title': '🔥 CS2 Global Elite | 15000+ Hours | Prime | Knife + Rare Skins',
                'game': 'CS2',
                'category': 'Hesap',
                'description': '''✅ Global Elite 🏆
✅ 15000+ Hours
✅ Prime Status
✅ Knife Skin 🔪
✅ Rare Skins
✅ 5 Year Coin
✅ Full Access

🎮 Premium Account:
• Global Elite rank
• Knife included
• Prime status
• Old account''',
                'price': 1899.99,
                'rank': 'Global Elite',
                'region': 'EU',
                'image_url': screenshot_urls['CS2'][0],
                'stock': 2
            },
            
            # Clash of Clans
            {
                'title': '🏰 Clash of Clans TH15 Max | 8000 Gems | All Troops Max',
                'game': 'Clash of Clans',
                'category': 'Hesap',
                'description': '''✅ TH15 Max Level 🏰
✅ 8000+ Gems
✅ All Troops Max
✅ All Heroes Max
✅ Champion League
✅ Full Access

🎮 Max Account:
• Everything maxed
• High gems
• Champion league
• Clean account''',
                'price': 1599.99,
                'rank': 'TH15',
                'region': 'Global',
                'image_url': screenshot_urls['Clash of Clans'][0],
                'stock': 3
            },
            
            # Discord
            {
                'title': '💎 Discord Nitro 2 Years | Full Boost | Rare Username | 2018 Account',
                'game': 'Discord',
                'category': 'Hesap',
                'description': '''✅ 2 Year Nitro 💎
✅ Full Boost
✅ Rare Username
✅ 2018 Account (Old)
✅ Full Access

🎮 Premium Discord:
• 2 years nitro
• Rare username
• Old account
• Full boost''',
                'price': 299.99,
                'rank': 'Nitro',
                'region': 'Global',
                'image_url': screenshot_urls['Discord'][0],
                'stock': 5
            },
            
            # Fortnite
            {
                'title': '🔥 Fortnite OG Account | 500+ Skins | Renegade Raider | Black Knight',
                'game': 'Fortnite',
                'category': 'Hesap',
                'description': '''✅ 500+ Skins 🔥
✅ Renegade Raider (OG)
✅ Black Knight (OG)
✅ OG Skins Collection
✅ 200+ Emotes
✅ Full Access

🎮 OG Account:
• Rare OG skins
• Season 1-2 items
• Huge collection
• Clean account''',
                'price': 3999.99,
                'rank': 'OG Account',
                'region': 'Global',
                'image_url': screenshot_urls['Fortnite'][0],
                'stock': 1
            },
            
            # Minecraft
            {
                'title': '⛏️ Minecraft Premium | Full Access | Cape | Hypixel VIP+',
                'game': 'Minecraft',
                'category': 'Hesap',
                'description': '''✅ Premium Account ⛏️
✅ Full Access
✅ Cape Included
✅ Hypixel VIP+
✅ Email Change Available

🎮 Premium Minecraft:
• Full access
• Cape included
• Hypixel VIP+
• Clean account''',
                'price': 199.99,
                'rank': 'Premium',
                'region': 'Global',
                'image_url': screenshot_urls['Minecraft'][0],
                'stock': 10
            }
        ]
        
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f'✅ {len(products)} ürün oluşturuldu!')
        print('✅ Gerçek oyun görselleri ile')
        print('✅ Detaylı açıklamalar')
        print('✅ Emoji ve profesyonel format')

if __name__ == '__main__':
    create_realistic_products()
