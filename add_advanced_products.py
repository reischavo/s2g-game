#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2G Game - Gelişmiş Örnek Ürün Ekleme Scripti
PUBG, Clash of Clans, Discord, ve daha fazlası!
"""

from app import app, db, Product, User
from werkzeug.security import generate_password_hash
import random

def add_advanced_products():
    with app.app_context():
        # Veritabanını oluştur
        db.create_all()
        
        # Admin kullanıcısı oluştur
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@s2ggame.com',
                password=generate_password_hash('admin123'),
                is_admin=True,
                balance=0.0,
                last_ip='127.0.0.1'
            )
            db.session.add(admin)
            db.session.commit()
            print('✅ Admin kullanıcısı oluşturuldu! (admin / admin123)')
        
        admin_user = User.query.filter_by(username='admin').first()
        
        # Gelişmiş ürün listesi - Çok daha fazla kategori!
        advanced_products = [
            # VALORANT
            {
                'title': 'Valorant Radiant Hesabı - Tüm Agentler',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': 'Radiant rank, tüm agentler açık, 150+ skin koleksiyonu. Reaver, Prime, Elderflame setleri mevcut. Hesap 2 yıllık, temiz geçmiş.',
                'price': 4500.00,
                'rank': 'Radiant',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400&h=200&fit=crop'
            },
            {
                'title': 'Valorant Immortal 3 Hesabı',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': 'Immortal 3 rank, 80+ skin, tüm agentler. Prime Vandal, Reaver Phantom dahil. Güvenli hesap.',
                'price': 1850.00,
                'rank': 'Immortal 3',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400&h=200&fit=crop'
            },
            {
                'title': 'Valorant Ascendant 2 - Skin Paketi',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': 'Ascendant 2 rank, 45+ skin, Elderflame Vandal, Ion Phantom. Tüm agentler açık.',
                'price': 1200.00,
                'rank': 'Ascendant 2',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400&h=200&fit=crop'
            },
            {
                'title': 'Valorant Diamond 3 Hesabı',
                'game': 'Valorant',
                'category': 'Hesap',
                'description': 'Diamond 3 rank, 30+ skin, temiz hesap. Başlangıç için ideal.',
                'price': 750.00,
                'rank': 'Diamond 3',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=400&h=200&fit=crop'
            },
            
            # LEAGUE OF LEGENDS
            {
                'title': 'League of Legends Challenger Hesabı',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': 'Challenger rank, 200+ champion, 100+ skin. Prestij skinler dahil. 7 yıllık hesap.',
                'price': 5500.00,
                'rank': 'Challenger',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=400&h=200&fit=crop'
            },
            {
                'title': 'League of Legends Master Hesabı',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': 'Master rank, 180+ champion, 80+ skin. Tüm runlar açık. Temiz hesap.',
                'price': 3200.00,
                'rank': 'Master',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1556438064-2d7646166914?w=400&h=200&fit=crop'
            },
            {
                'title': 'League of Legends Elmas 1 Hesabı',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': 'Elmas 1 rank, 120+ champion, 40+ skin. 5 yıllık hesap.',
                'price': 1100.00,
                'rank': 'Elmas 1',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=400&h=200&fit=crop'
            },
            {
                'title': 'League of Legends Platin 2 Hesabı',
                'game': 'League of Legends',
                'category': 'Hesap',
                'description': 'Platin 2 rank, 90+ champion, temiz hesap. Başlangıç için ideal.',
                'price': 550.00,
                'rank': 'Platin 2',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=200&fit=crop'
            },
            
            # CS2 (Counter-Strike 2)
            {
                'title': 'CS2 Global Elite Hesabı - Prime',
                'game': 'CS2',
                'category': 'Hesap',
                'description': 'Global Elite rank, 3000+ saat, Prime hesap. Temiz VAC kaydı. Nadir skinler mevcut.',
                'price': 2800.00,
                'rank': 'Global Elite',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400&h=200&fit=crop'
            },
            {
                'title': 'CS2 Supreme Master Hesabı',
                'game': 'CS2',
                'category': 'Hesap',
                'description': 'Supreme rank, 2000+ saat, Prime hesap. Güvenli ve temiz.',
                'price': 1600.00,
                'rank': 'Supreme',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400&h=200&fit=crop'
            },
            {
                'title': 'CS2 Legendary Eagle Hesabı',
                'game': 'CS2',
                'category': 'Hesap',
                'description': 'Legendary Eagle rank, 1200+ saat, Prime. İyi başlangıç hesabı.',
                'price': 950.00,
                'rank': 'Legendary Eagle',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400&h=200&fit=crop'
            },
            
            # PUBG MOBILE
            {
                'title': 'PUBG Mobile Conqueror Hesabı',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': 'Conqueror rank, 50+ UC skin, tüm sezon geçişleri. Nadir kıyafetler ve silah skinleri.',
                'price': 2200.00,
                'rank': 'Conqueror',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=400&h=200&fit=crop'
            },
            {
                'title': 'PUBG Mobile Ace Hesabı',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': 'Ace rank, 30+ UC skin, M416 Glacier skin dahil. Temiz hesap.',
                'price': 1400.00,
                'rank': 'Ace',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=400&h=200&fit=crop'
            },
            {
                'title': 'PUBG Mobile Crown Hesabı',
                'game': 'PUBG Mobile',
                'category': 'Hesap',
                'description': 'Crown rank, 20+ skin, güvenli hesap. İyi başlangıç.',
                'price': 800.00,
                'rank': 'Crown',
                'region': 'TR',
                'image_url': 'https://images.unsplash.com/photo-1556438064-2d7646166914?w=400&h=200&fit=crop'
            },
            
            # CLASH OF CLANS
            {
                'title': 'Clash of Clans TH15 Max Hesabı',
                'game': 'Clash of Clans',
                'category': 'Hesap',
                'description': 'Town Hall 15 max level, tüm binalar max, 5000+ kupa. Nadir skinler ve dekorasyonlar.',
                'price': 3800.00,
                'rank': 'TH15 Max',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=400&h=200&fit=crop'
            },
            {
                'title': 'Clash of Clans TH14 Hesabı',
                'game': 'Clash of Clans',
                'category': 'Hesap',
                'description': 'Town Hall 14, çoğu bina max, 4000+ kupa. Güçlü hesap.',
                'price': 2100.00,
                'rank': 'TH14',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=200&fit=crop'
            },
            {
                'title': 'Clash of Clans TH13 Hesabı',
                'game': 'Clash of Clans',
                'category': 'Hesap',
                'description': 'Town Hall 13, iyi gelişmiş, 3500+ kupa. Temiz hesap.',
                'price': 1300.00,
                'rank': 'TH13',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400&h=200&fit=crop'
            },
            
            # DISCORD
            {
                'title': 'Discord Nitro 1 Yıllık',
                'game': 'Discord',
                'category': 'Abonelik',
                'description': 'Discord Nitro 1 yıllık abonelik. Tüm özellikler açık, emoji boost, HD video.',
                'price': 450.00,
                'rank': 'Nitro',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400&h=200&fit=crop'
            },
            {
                'title': 'Discord Nitro 6 Aylık',
                'game': 'Discord',
                'category': 'Abonelik',
                'description': 'Discord Nitro 6 aylık abonelik. Tüm premium özellikler.',
                'price': 250.00,
                'rank': 'Nitro',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400&h=200&fit=crop'
            },
            {
                'title': 'Discord Nitro Basic 1 Yıl',
                'game': 'Discord',
                'category': 'Abonelik',
                'description': 'Discord Nitro Basic 1 yıllık. Emoji ve dosya yükleme özellikleri.',
                'price': 180.00,
                'rank': 'Nitro Basic',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=400&h=200&fit=crop'
            },
            
            # FORTNITE
            {
                'title': 'Fortnite Hesabı - 300+ Skin',
                'game': 'Fortnite',
                'category': 'Hesap',
                'description': '300+ skin, Renegade Raider, Ghoul Trooper, Black Knight. Nadir emote ve pickaxe\'ler.',
                'price': 6500.00,
                'rank': 'Level 1000+',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=400&h=200&fit=crop'
            },
            {
                'title': 'Fortnite Hesabı - 150+ Skin',
                'game': 'Fortnite',
                'category': 'Hesap',
                'description': '150+ skin, tüm battle pass skinleri, nadir emote\'lar. Güvenli hesap.',
                'price': 2800.00,
                'rank': 'Level 600+',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1556438064-2d7646166914?w=400&h=200&fit=crop'
            },
            {
                'title': 'Fortnite Hesabı - 80+ Skin',
                'game': 'Fortnite',
                'category': 'Hesap',
                'description': '80+ skin, güzel koleksiyon. İyi başlangıç hesabı.',
                'price': 1200.00,
                'rank': 'Level 400+',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=400&h=200&fit=crop'
            },
            
            # MINECRAFT
            {
                'title': 'Minecraft Premium Hesabı - Full Access',
                'game': 'Minecraft',
                'category': 'Hesap',
                'description': 'Minecraft Java Edition premium hesap. Full access, isim değiştirme hakkı. Temiz hesap.',
                'price': 85.00,
                'rank': 'Premium',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=200&fit=crop'
            },
            {
                'title': 'Minecraft Premium + Hypixel VIP',
                'game': 'Minecraft',
                'category': 'Hesap',
                'description': 'Minecraft premium + Hypixel VIP rank. Özel avantajlar.',
                'price': 150.00,
                'rank': 'Premium + VIP',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400&h=200&fit=crop'
            },
            
            # APEX LEGENDS
            {
                'title': 'Apex Legends Predator Hesabı',
                'game': 'Apex Legends',
                'category': 'Hesap',
                'description': 'Predator rank, tüm legendler açık, 100+ skin. Heirloom setleri mevcut.',
                'price': 3200.00,
                'rank': 'Predator',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400&h=200&fit=crop'
            },
            {
                'title': 'Apex Legends Master Hesabı',
                'game': 'Apex Legends',
                'category': 'Hesap',
                'description': 'Master rank, 60+ skin, tüm legendler. Güvenli hesap.',
                'price': 1800.00,
                'rank': 'Master',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400&h=200&fit=crop'
            },
            
            # ROCKET LEAGUE
            {
                'title': 'Rocket League Grand Champion Hesabı',
                'game': 'Rocket League',
                'category': 'Hesap',
                'description': 'Grand Champion rank, 50+ araba, nadir decal\'ler. Titanium White Octane dahil.',
                'price': 2400.00,
                'rank': 'Grand Champion',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=400&h=200&fit=crop'
            },
            {
                'title': 'Rocket League Champion Hesabı',
                'game': 'Rocket League',
                'category': 'Hesap',
                'description': 'Champion rank, 30+ araba, güzel koleksiyon.',
                'price': 1100.00,
                'rank': 'Champion',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=400&h=200&fit=crop'
            },
            
            # OVERWATCH 2
            {
                'title': 'Overwatch 2 Grandmaster Hesabı',
                'game': 'Overwatch 2',
                'category': 'Hesap',
                'description': 'Grandmaster rank, tüm kahramanlar açık, 80+ skin. Altın silahlar mevcut.',
                'price': 2600.00,
                'rank': 'Grandmaster',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1556438064-2d7646166914?w=400&h=200&fit=crop'
            },
            {
                'title': 'Overwatch 2 Master Hesabı',
                'game': 'Overwatch 2',
                'category': 'Hesap',
                'description': 'Master rank, 50+ skin, tüm kahramanlar. Temiz hesap.',
                'price': 1400.00,
                'rank': 'Master',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=400&h=200&fit=crop'
            },
            
            # GENSHIN IMPACT
            {
                'title': 'Genshin Impact AR60 Hesabı',
                'game': 'Genshin Impact',
                'category': 'Hesap',
                'description': 'AR60, 30+ 5 yıldız karakter, tüm bölgeler açık. Nadir silahlar ve artifactlar.',
                'price': 4200.00,
                'rank': 'AR60',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=200&fit=crop'
            },
            {
                'title': 'Genshin Impact AR55 Hesabı',
                'game': 'Genshin Impact',
                'category': 'Hesap',
                'description': 'AR55, 20+ 5 yıldız karakter, güçlü hesap.',
                'price': 2400.00,
                'rank': 'AR55',
                'region': 'EU',
                'image_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400&h=200&fit=crop'
            },
            
            # BRAWL STARS
            {
                'title': 'Brawl Stars 50+ Brawler Hesabı',
                'game': 'Brawl Stars',
                'category': 'Hesap',
                'description': '50+ brawler, tüm efsanevi brawler\'lar açık. 30000+ kupa.',
                'price': 1600.00,
                'rank': '30000+ Kupa',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400&h=200&fit=crop'
            },
            {
                'title': 'Brawl Stars 40+ Brawler Hesabı',
                'game': 'Brawl Stars',
                'category': 'Hesap',
                'description': '40+ brawler, 25000+ kupa. İyi gelişmiş hesap.',
                'price': 950.00,
                'rank': '25000+ Kupa',
                'region': 'Global',
                'image_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400&h=200&fit=crop'
            }
        ]
        
        # Ürünleri ekle
        added_count = 0
        for product_data in advanced_products:
            # Aynı başlıkta ürün varsa ekleme
            if not Product.query.filter_by(title=product_data['title']).first():
                product = Product(
                    title=product_data['title'],
                    game=product_data['game'],
                    category=product_data['category'],
                    description=product_data['description'],
                    price=product_data['price'],
                    rank=product_data['rank'],
                    region=product_data['region'],
                    image_url=product_data['image_url'],
                    views=random.randint(10, 500),
                    seller_id=admin_user.id
                )
                db.session.add(product)
                added_count += 1
        
        db.session.commit()
        
        print(f'\n✅ {added_count} yeni ürün eklendi!')
        print(f'\n📊 Veritabanı İstatistikleri:')
        print(f'   - Kullanıcılar: {User.query.count()}')
        print(f'   - Toplam Ürünler: {Product.query.count()}')
        print(f'   - Kategoriler: Valorant, LOL, CS2, PUBG Mobile, Clash of Clans, Discord, Fortnite, Minecraft, Apex Legends, Rocket League, Overwatch 2, Genshin Impact, Brawl Stars')
        print('\n🔐 Admin Giriş Bilgileri:')
        print('   Kullanıcı Adı: admin')
        print('   Şifre: admin123')
        print('\n🚀 Siteyi başlatmak için: python app.py')

if __name__ == '__main__':
    add_advanced_products()
