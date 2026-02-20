# 🎮 S2G GAME - KURULUM REHBERİ

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- Windows/Linux/MacOS

## 🚀 Hızlı Kurulum (Windows)

### 1. Bağımlılıkları Yükle
```cmd
INSTALL.bat
```

### 2. Sunucuyu Başlat
```cmd
START.bat
```

### 3. Tarayıcıda Aç
```
http://localhost:5000
```

## 🐧 Linux/MacOS Kurulum

### 1. Bağımlılıkları Yükle
```bash
chmod +x install.sh
./install.sh
```

### 2. Sunucuyu Başlat
```bash
chmod +x start.sh
./start.sh
```

## 📦 Manuel Kurulum

### 1. Virtual Environment Oluştur (Opsiyonel ama Önerilen)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/MacOS
source venv/bin/activate
```

### 2. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 3. Veritabanını Oluştur
```bash
python app.py
```
İlk çalıştırmada veritabanı otomatik oluşturulur.

### 4. Sunucuyu Başlat
```bash
python app.py
```

## 👤 Varsayılan Admin Hesabı

İlk kurulumda otomatik oluşturulur:

- **Kullanıcı Adı:** admin
- **Şifre:** admin123
- **Email:** admin@s2ggame.com

⚠️ **ÖNEMLİ:** Üretim ortamında mutlaka şifreyi değiştirin!

## 🎯 Örnek Ürünler Ekleme

Sistemi test etmek için örnek ürünler ekleyin:

```bash
python add_sample_products.py
```

veya daha gelişmiş ürünler için:

```bash
python add_advanced_products.py
```

## 🌐 Sunucu Ayarları

### Port Değiştirme
`app.py` dosyasının sonundaki satırı düzenleyin:
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5000)
```

### Dış Erişim İçin
```python
socketio.run(app, debug=False, host='0.0.0.0', port=5000)
```

### Sadece Localhost
```python
socketio.run(app, debug=True, host='127.0.0.1', port=5000)
```

## 📁 Klasör Yapısı

```
s2g-game/
├── app.py                      # Ana uygulama
├── requirements.txt            # Python bağımlılıkları
├── INSTALL.bat                 # Windows kurulum scripti
├── START.bat                   # Windows başlatma scripti
├── install.sh                  # Linux/Mac kurulum scripti
├── start.sh                    # Linux/Mac başlatma scripti
├── static/                     # Statik dosyalar
│   ├── css/                    # CSS dosyaları
│   ├── js/                     # JavaScript dosyaları
│   │   └── livechat.js        # Canlı destek widget
│   └── uploads/                # Yüklenen dosyalar
│       └── products/           # Ürün görselleri
├── templates/                  # HTML şablonları
│   ├── index_modern.html      # Ana sayfa
│   ├── products_pro.html      # Ürünler sayfası
│   ├── product_detail_pro.html # Ürün detay
│   ├── login_modern.html      # Giriş
│   ├── register_modern.html   # Kayıt
│   ├── profile_modern.html    # Profil
│   ├── order_success.html     # Sipariş başarılı
│   ├── seller_delivery.html   # Satıcı teslimat
│   ├── admin_advanced.html    # Admin panel
│   └── ...                    # Diğer sayfalar
└── s2g_game.db                # SQLite veritabanı (otomatik oluşur)
```

## 🔧 Veritabanı Yönetimi

### Veritabanını Sıfırla
```bash
# Veritabanı dosyasını sil
rm s2g_game.db  # Linux/Mac
del s2g_game.db  # Windows

# Uygulamayı tekrar başlat
python app.py
```

### Veritabanını Yedekle
```bash
# SQLite veritabanını kopyala
cp s2g_game.db s2g_game_backup.db  # Linux/Mac
copy s2g_game.db s2g_game_backup.db  # Windows
```

## 🎨 Özellikler

### ✅ Kullanıcı Özellikleri
- Modern kayıt/giriş sistemi
- Profil yönetimi
- Bakiye yükleme/çekme
- Ürün satın alma
- Ürün satışa koyma
- Sipariş takibi
- Canlı destek (Socket.IO)

### ✅ Satıcı Özellikleri
- Ürün ekleme/düzenleme
- Bekleyen teslimatlar
- Teslimat yapma
- Kazanç takibi (%90 komisyon)
- İlan yönetimi

### ✅ Admin Özellikleri
- Kullanıcı yönetimi
- Ürün yönetimi
- Sipariş yönetimi
- İşlem onaylama/reddetme
- Canlı destek mesajları
- Aktivite logları

### ✅ Teknik Özellikler
- Flask + SQLAlchemy
- Socket.IO (gerçek zamanlı chat)
- SQLite veritabanı
- Responsive tasarım
- Modern UI/UX
- Güvenli şifreleme (Werkzeug)

## 🔒 Güvenlik

### Üretim Ortamı İçin:
1. `SECRET_KEY`'i değiştirin (app.py)
2. `debug=False` yapın
3. HTTPS kullanın
4. Güçlü şifreler kullanın
5. Düzenli yedekleme yapın

## 🐛 Sorun Giderme

### Port Zaten Kullanılıyor
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Modül Bulunamadı Hatası
```bash
pip install -r requirements.txt --upgrade
```

### Veritabanı Hatası
```bash
# Veritabanını sil ve yeniden oluştur
rm s2g_game.db
python app.py
```

### Socket.IO Bağlantı Hatası
- Tarayıcı konsolunu kontrol edin
- Firewall ayarlarını kontrol edin
- Port 5000'in açık olduğundan emin olun

## 📞 Destek

Sorun yaşarsanız:
1. Hata mesajını kontrol edin
2. Konsol çıktısını inceleyin
3. Veritabanını sıfırlamayı deneyin
4. Bağımlılıkları güncelleyin

## 🎉 Başarılı Kurulum!

Sunucu başarıyla çalışıyorsa:
- Ana sayfa: http://localhost:5000
- Admin panel: http://localhost:5000/admin (admin/admin123)
- Ürünler: http://localhost:5000/products

Mohawk Development 🦅
