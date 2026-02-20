#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2G Game - Sistem Kontrol Scripti
Kurulum ve sistem durumunu kontrol eder
"""

import sys
import os

def check_python():
    """Python versiyonunu kontrol et"""
    print("🐍 Python Versiyonu:")
    print(f"   {sys.version}")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Python versiyonu uygun (3.8+)")
        return True
    else:
        print("   ❌ Python 3.8 veya üzeri gerekli!")
        return False

def check_dependencies():
    """Bağımlılıkları kontrol et"""
    print("\n📦 Bağımlılıklar:")
    
    dependencies = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'werkzeug': 'Werkzeug',
        'flask_socketio': 'Flask-SocketIO',
        'socketio': 'python-socketio'
    }
    
    all_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} - YÜKLENMEDİ!")
            all_ok = False
    
    return all_ok

def check_database():
    """Veritabanını kontrol et"""
    print("\n💾 Veritabanı:")
    
    # s2g-game klasöründe ara
    db_paths = ["s2g_game.db", "s2g-game/s2g_game.db"]
    db_file = None
    
    for path in db_paths:
        if os.path.exists(path):
            db_file = path
            break
    
    if db_file:
        size = os.path.getsize(db_file)
        print(f"   ✅ {db_file} mevcut ({size} bytes)")
        
        try:
            # s2g-game klasörüne geç
            original_dir = os.getcwd()
            if 's2g-game' in db_file:
                os.chdir('s2g-game')
            
            from app import app, db, User, Product, Order
            with app.app_context():
                user_count = User.query.count()
                product_count = Product.query.count()
                order_count = Order.query.count()
                
                print(f"   📊 İstatistikler:")
                print(f"      - Kullanıcılar: {user_count}")
                print(f"      - Ürünler: {product_count}")
                print(f"      - Siparişler: {order_count}")
            
            os.chdir(original_dir)
            return True
        except Exception as e:
            os.chdir(original_dir)
            print(f"   ⚠️  Veritabanı okunamadı: {e}")
            return False
    else:
        print(f"   ⚠️  Veritabanı bulunamadı (ilk çalıştırmada oluşturulacak)")
        return True

def check_folders():
    """Gerekli klasörleri kontrol et"""
    print("\n📁 Klasörler:")
    
    # s2g-game klasöründe kontrol et
    base_paths = ["", "s2g-game/"]
    
    folders = [
        'static',
        'static/css',
        'static/js',
        'static/uploads',
        'static/uploads/products',
        'templates'
    ]
    
    all_ok = True
    for folder in folders:
        found = False
        for base in base_paths:
            if os.path.exists(base + folder):
                print(f"   ✅ {folder}/")
                found = True
                break
        
        if not found:
            print(f"   ❌ {folder}/ - BULUNAMADI!")
            all_ok = False
    
    return all_ok

def check_files():
    """Önemli dosyaları kontrol et"""
    print("\n📄 Önemli Dosyalar:")
    
    # s2g-game klasöründe kontrol et
    base_paths = ["", "s2g-game/"]
    
    files = [
        'app.py',
        'requirements.txt',
        'templates/index_modern.html',
        'templates/products_pro.html',
        'templates/login_modern.html',
        'templates/register_modern.html',
        'templates/profile_modern.html',
        'static/js/livechat.js'
    ]
    
    all_ok = True
    for file in files:
        found = False
        for base in base_paths:
            if os.path.exists(base + file):
                print(f"   ✅ {file}")
                found = True
                break
        
        if not found:
            print(f"   ❌ {file} - BULUNAMADI!")
            all_ok = False
    
    return all_ok

def main():
    print("\n" + "="*60)
    print("🎮 S2G GAME - SİSTEM KONTROL")
    print("="*60 + "\n")
    
    results = []
    
    # Kontrolleri yap
    results.append(("Python", check_python()))
    results.append(("Bağımlılıklar", check_dependencies()))
    results.append(("Veritabanı", check_database()))
    results.append(("Klasörler", check_folders()))
    results.append(("Dosyalar", check_files()))
    
    # Özet
    print("\n" + "="*60)
    print("📊 ÖZET")
    print("="*60 + "\n")
    
    all_ok = True
    for name, status in results:
        icon = "✅" if status else "❌"
        print(f"{icon} {name}")
        if not status:
            all_ok = False
    
    print("\n" + "="*60)
    if all_ok:
        print("✅ TÜM KONTROLLER BAŞARILI!")
        print("="*60)
        print("\n🚀 Sunucuyu başlatmak için:")
        print("   Windows: START.bat")
        print("   Linux/Mac: ./start.sh")
    else:
        print("❌ BAZI KONTROLLER BAŞARISIZ!")
        print("="*60)
        print("\n🔧 Kurulum yapmak için:")
        print("   Windows: INSTALL.bat")
        print("   Linux/Mac: ./install.sh")
    print()

if __name__ == '__main__':
    main()
