#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2G Game - Örnek Ürün Ekleme Scripti
"""

from app import app, db, Product, User
from werkzeug.security import generate_password_hash

def add_sample_products():
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
                balance=0.0
            )
            db.session.add(admin)
            db.session.commit()
            print('✅ Admin kullanıcısı oluşturuldu! (admin / admin123)')
        
        # Örnek ürünler
        sample_products = [
            {
                'title': 'Valorant Immortal 3 Hesabı',
                'game': 'Valorant',
                'description': 'Immortal 3 rank, tüm agentler açık, 50+ skin var. Hesap temiz ve güvenli.',
                'price': 1250.00,
                'rank': 'Immortal 3',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/400x200/7b2cbf/ffffff?text=Valorant'
            },
            {
                'title': 'League of Legends Elmas 2 Hesabı',
                'game': 'League of Legends',
                'description': 'Elmas 2 rank, 120+ champion, 30+ skin. Hesap 5 yıllık.',
                'price': 850.00,
                'rank': 'Elmas 2',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/400x200/9d4edd/ffffff?text=League+of+Legends'
            },
            {
                'title': 'CS2 Global Elite Hesabı',
                'game': 'CS2',
                'description': 'Global Elite rank, 2000+ saat, Prime hesap. Temiz VAC kaydı.',
                'price': 2100.00,
                'rank': 'Global Elite',
                'region': 'EU',
                'image_url': 'https://via.placeholder.com/400x200/ff006e/ffffff?text=CS2'
            },
            {
                'title': 'Valorant Radiant Hesabı',
                'game': 'Valorant',
                'description': 'Radiant rank, tüm agentler ve 100+ skin. Özel hesap!',
                'price': 3500.00,
                'rank': 'Radiant',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/400x200/7b2cbf/ffffff?text=Valorant+Radiant'
            },
            {
                'title': 'Fortnite Hesabı - 200+ Skin',
                'game': 'Fortnite',
                'description': '200+ skin, tüm battle pass skinleri, nadir emote\'lar.',
                'price': 1800.00,
                'rank': 'Level 500+',
                'region': 'EU',
                'image_url': 'https://via.placeholder.com/400x200/fb5607/ffffff?text=Fortnite'
            },
            {
                'title': 'League of Legends Platin 1 Hesabı',
                'game': 'League of Legends',
                'description': 'Platin 1 rank, 80+ champion, temiz hesap.',
                'price': 450.00,
                'rank': 'Platin 1',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/400x200/9d4edd/ffffff?text=LoL+Platin'
            },
            {
                'title': 'Valorant Ascendant 2 Hesabı',
                'game': 'Valorant',
                'description': 'Ascendant 2 rank, 30+ skin, tüm agentler.',
                'price': 950.00,
                'rank': 'Ascendant 2',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/400x200/7b2cbf/ffffff?text=Valorant+Ascendant'
            },
            {
                'title': 'CS2 Supreme Hesabı',
                'game': 'CS2',
                'description': 'Supreme rank, 1500+ saat, Prime hesap.',
                'price': 1400.00,
                'rank': 'Supreme',
                'region': 'EU',
                'image_url': 'https://via.placeholder.com/400x200/ff006e/ffffff?text=CS2+Supreme'
            },
            {
                'title': 'Valorant Diamond 3 Hesabı',
                'game': 'Valorant',
                'description': 'Diamond 3 rank, 20+ skin, güvenli hesap.',
                'price': 650.00,
                'rank': 'Diamond 3',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/400x200/7b2cbf/ffffff?text=Valorant+Diamond'
            },
            {
                'title': 'League of Legends Master Hesabı',
                'game': 'League of Legends',
                'description': 'Master rank, 150+ champion, 50+ skin, prestij hesap!',
                'price': 2800.00,
                'rank': 'Master',
                'region': 'TR',
                'image_url': 'https://via.placeholder.com/400x200/9d4edd/ffffff?text=LoL+Master'
            },
            {
                'title': 'Fortnite Hesabı - Rare Skins',
                'game': 'Fortnite',
                'description': 'Nadir skinler, Renegade Raider, Ghoul Trooper ve daha fazlası!',
                'price': 4500.00,
                'rank': 'Level 800+',
                'region': 'EU',
                'image_url': 'https://via.placeholder.com/400x200/fb5607/ffffff?text=Fortnite+Rare'
            },
            {
                'title': 'CS2 Legendary Eagle Hesabı',
                'game': 'CS2',
                'description': 'Legendary Eagle rank, 1000+ saat, Prime.',
                'price': 900.00,
                'rank': 'Legendary Eagle',
                'region': 'EU',
                'image_url': 'https://via.placeholder.com/400x200/ff006e/ffffff?text=CS2+LE'
            }
        ]
        
        # Ürünleri ekle
        admin_user = User.query.filter_by(username='admin').first()
        
        for product_data in sample_products:
            # Aynı başlıkta ürün varsa ekleme
            if not Product.query.filter_by(title=product_data['title']).first():
                product = Product(
                    title=product_data['title'],
                    game=product_data['game'],
                    description=product_data['description'],
                    price=product_data['price'],
                    rank=product_data['rank'],
                    region=product_data['region'],
                    image_url=product_data['image_url'],
                    seller_id=admin_user.id
                )
                db.session.add(product)
        
        db.session.commit()
        print(f'✅ {len(sample_products)} örnek ürün eklendi!')
        print('\n📊 Veritabanı İstatistikleri:')
        print(f'   - Kullanıcılar: {User.query.count()}')
        print(f'   - Ürünler: {Product.query.count()}')
        print('\n🔐 Admin Giriş Bilgileri:')
        print('   Kullanıcı Adı: admin')
        print('   Şifre: admin123')
        print('\n🚀 Siteyi başlatmak için: python app.py')

if __name__ == '__main__':
    add_sample_products()
