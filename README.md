# 🎮 S2G GAME - Oyun Hesabı Alışveriş Platformu

Modern ve profesyonel oyun hesabı alım-satım platformu. GameSatış tarzında teslimat sistemi, canlı destek ve admin paneli ile tam özellikli e-ticaret çözümü.

## ✨ Özellikler

### 👤 Kullanıcı Özellikleri
- ✅ Modern kayıt/giriş sistemi
- ✅ Profil yönetimi ve avatar
- ✅ Bakiye yükleme/çekme (Papara, Banka, Crypto)
- ✅ Ürün arama ve filtreleme
- ✅ Ürün satın alma
- ✅ Ürün satışa koyma
- ✅ Sipariş takibi ve geçmişi
- ✅ Canlı destek (Socket.IO)
- ✅ Email bildirimleri

### 🛒 Satıcı Özellikleri
- ✅ Ürün ekleme/düzenleme/silme
- ✅ Bekleyen teslimatlar listesi
- ✅ Profesyonel teslimat formu
- ✅ Kazanç takibi (%90 komisyon)
- ✅ İlan yönetimi (aktif/satıldı)
- ✅ Satış istatistikleri

### 👨‍💼 Admin Özellikleri
- ✅ Kullanıcı yönetimi (ban, doğrulama)
- ✅ Ürün yönetimi (onay, düzenleme, silme)
- ✅ Sipariş yönetimi
- ✅ İşlem onaylama/reddetme
- ✅ Canlı destek mesajları
- ✅ Aktivite logları
- ✅ İstatistikler ve raporlar

### 🎨 Teknik Özellikler
- ✅ Flask + SQLAlchemy
- ✅ Socket.IO (gerçek zamanlı chat)
- ✅ SQLite veritabanı
- ✅ Responsive tasarım
- ✅ Modern UI/UX (glassmorphism)
- ✅ Güvenli şifreleme (Werkzeug)
- ✅ Session yönetimi
- ✅ File upload sistemi

## 🚀 Hızlı Başlangıç

### Windows

1. **Hızlı Kurulum (Önerilen)**
   ```cmd
   QUICK_START.bat
   ```

2. **Manuel Kurulum**
   ```cmd
   INSTALL.bat
   START.bat
   ```

### Linux/MacOS

1. **Kurulum**
   ```bash
   chmod +x install.sh start.sh
   ./install.sh
   ```

2. **Başlatma**
   ```bash
   ./start.sh
   ```

## 📋 Gereksinimler

- Python 3.8+
- pip
- 100MB disk alanı

## 🎯 İlk Adımlar

1. **Sunucuyu Başlat**
   - Windows: `START.bat`
   - Linux/Mac: `./start.sh`

2. **Tarayıcıda Aç**
   - Ana Sayfa: http://localhost:5000
   - Admin Panel: http://localhost:5000/admin

3. **Admin Girişi**
   - Kullanıcı Adı: `admin`
   - Şifre: `admin123`

4. **Örnek Ürünler Ekle**
   ```bash
   python add_sample_products.py
   ```

## 🎮 Desteklenen Oyunlar

- League of Legends
- Valorant
- CS:GO
- Fortnite
- PUBG
- Apex Legends
- Overwatch
- Rainbow Six Siege
- Rocket League
- ve daha fazlası...

## 📁 Proje Yapısı

```
s2g-game/
├── app.py                      # Ana uygulama
├── requirements.txt            # Bağımlılıklar
├── INSTALL.bat                 # Windows kurulum
├── START.bat                   # Windows başlatma
├── install.sh                  # Linux/Mac kurulum
├── start.sh                    # Linux/Mac başlatma
├── QUICK_START.bat             # Hızlı başlangıç
├── check_system.py             # Sistem kontrolü
├── reset_database.py           # Veritabanı sıfırlama
├── add_sample_products.py      # Örnek ürünler
├── static/
│   ├── css/                    # Stil dosyaları
│   ├── js/
│   │   └── livechat.js        # Canlı destek widget
│   └── uploads/
│       └── products/           # Ürün görselleri
├── templates/
│   ├── index_modern.html      # Ana sayfa
│   ├── products_pro.html      # Ürünler
│   ├── product_detail_pro.html # Ürün detay
│   ├── login_modern.html      # Giriş
│   ├── register_modern.html   # Kayıt
│   ├── profile_modern.html    # Profil
│   ├── order_success.html     # Sipariş başarılı
│   ├── seller_delivery.html   # Satıcı teslimat
│   ├── admin_advanced.html    # Admin panel
│   └── ...
└── s2g_game.db                # Veritabanı
```

## 🔧 Yönetim Komutları

### Sistem Kontrolü
```bash
python check_system.py
```

### Veritabanı Sıfırlama
```bash
python reset_database.py
```

### Örnek Ürünler Ekleme
```bash
python add_sample_products.py
```

## 🎨 Ekran Görüntüleri

### Ana Sayfa
- Modern hero section
- Öne çıkan ürünler
- Oyun kategorileri
- Canlı destek widget

### Ürün Sayfası
- Grid/List görünüm
- Filtreleme (oyun, fiyat, rank)
- Sıralama
- Arama

### Profil Sayfası
- Bakiye kartı
- Siparişlerim
- İlanlarım
- Bekleyen teslimatlar
- İşlem geçmişi

### Admin Panel
- Dashboard (istatistikler)
- Kullanıcı yönetimi
- Ürün yönetimi
- Sipariş yönetimi
- Canlı destek

## 💰 Komisyon Sistemi

- Müşteri ödeme yapar: 100₺
- Platform komisyonu: %10 (10₺)
- Satıcıya giden: %90 (90₺)

## 🔒 Güvenlik

- Şifre hashleme (Werkzeug)
- Session yönetimi
- CSRF koruması
- SQL injection koruması
- XSS koruması
- Güvenli file upload

## 🐛 Sorun Giderme

### Port Zaten Kullanılıyor
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Modül Bulunamadı
```bash
pip install -r requirements.txt --upgrade
```

### Veritabanı Hatası
```bash
python reset_database.py
```

## 📞 Destek

Sorun yaşarsanız:
1. `check_system.py` çalıştırın
2. Hata mesajlarını kontrol edin
3. Veritabanını sıfırlamayı deneyin
4. Bağımlılıkları güncelleyin

## 📝 Lisans

Bu proje eğitim amaçlıdır.

## 👨‍💻 Geliştirici

Mohawk Development 🦅

---

## 🎉 Başarılı Kurulum!

Sunucu çalışıyorsa:
- 🌐 Ana Sayfa: http://localhost:5000
- 👨‍💼 Admin Panel: http://localhost:5000/admin
- 🛒 Ürünler: http://localhost:5000/products
- 👤 Profil: http://localhost:5000/profile

**İyi Satışlar! 🎮**
