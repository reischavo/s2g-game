#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2G Game - Veritabanı Sıfırlama Scripti
Tüm verileri siler ve yeni bir veritabanı oluşturur
"""

import os
import sys

def reset_database():
    print("\n" + "="*60)
    print("🗑️  VERİTABANI SIFIRLAMA")
    print("="*60 + "\n")
    
    # Onay al
    print("⚠️  UYARI: Bu işlem tüm verileri silecek!")
    print("   - Tüm kullanıcılar")
    print("   - Tüm ürünler")
    print("   - Tüm siparişler")
    print("   - Tüm işlemler")
    print("   - Tüm chat mesajları")
    print()
    
    confirm = input("Devam etmek istediğinize emin misiniz? (EVET yazın): ")
    
    if confirm != "EVET":
        print("\n❌ İşlem iptal edildi.")
        return
    
    # Veritabanı dosyasını sil
    db_file = "s2g_game.db"
    
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print(f"\n✅ {db_file} silindi.")
        except Exception as e:
            print(f"\n❌ Hata: {e}")
            return
    else:
        print(f"\n⚠️  {db_file} bulunamadı.")
    
    # Yeni veritabanı oluştur
    print("\n📦 Yeni veritabanı oluşturuluyor...")
    
    try:
        from app import app, db, User
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            db.create_all()
            print("✅ Veritabanı tabloları oluşturuldu.")
            
            # Admin kullanıcısı oluştur
            admin = User(
                username='admin',
                email='admin@s2ggame.com',
                password=generate_password_hash('admin123'),
                is_admin=True,
                balance=0.0
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin kullanıcısı oluşturuldu.")
            
            print("\n" + "="*60)
            print("✅ VERİTABANI BAŞARIYLA SIFIRLANDI!")
            print("="*60)
            print("\n📝 Admin Hesabı:")
            print("   Kullanıcı Adı: admin")
            print("   Şifre: admin123")
            print("   Email: admin@s2ggame.com")
            print()
            
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    reset_database()
