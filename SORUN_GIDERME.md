# 🔧 S2G Game - Sorun Giderme Rehberi

## 🚨 Pencereler Hemen Kapanıyor

### Neden Olur?
- cloudflared.exe bulunamıyor
- Cloudflare config eksik veya hatalı
- Flask sunucu hata veriyor
- Bağımlılıklar eksik

### Çözüm Adımları

#### 1. Sistem Testini Çalıştırın
```batch
TEST_SISTEM.bat
```

Bu script tüm sistemi kontrol eder ve hangi adımda sorun olduğunu gösterir.

#### 2. Manuel Test - Flask Sunucu

Yeni bir CMD penceresi açın:
```batch
cd s2g-game
python app.py
```

**Beklenen Çıktı:**
```
✅ Admin kullanıcısı oluşturuldu! (admin / admin123)
 * Running on http://0.0.0.0:5000
```

**Hata Alırsanız:**
- `ModuleNotFoundError`: INSTALL.bat çalıştırın
- `Port already in use`: 5000 portu kullanımda, başka program kapatın
- Başka hata: Hata mesajını okuyun

#### 3. Manuel Test - Cloudflare Tunnel

Yeni bir CMD penceresi açın:
```batch
cd s2g-game
cloudflared.exe tunnel run s2g-game
```

**Beklenen Çıktı:**
```
Connection registered
```

**Hata Alırsanız:**

##### "cloudflared.exe bulunamadı"
```batch
# cloudflared.exe'nin s2g-game klasöründe olduğundan emin olun
dir cloudflared.exe
```

##### "config.yml bulunamadı"
```batch
# Config dosyasını kontrol edin
type %USERPROFILE%\.cloudflared\config.yml
```

Config yoksa:
```batch
CLOUDFLARE_SETUP_s2ggame.bat
```

##### "tunnel not found"
Tunnel oluşturulmamış. Yeniden kurulum:
```batch
CLOUDFLARE_SETUP_s2ggame.bat
```

## 🌐 Site Açılmıyor (https://s2ggame.com)

### Kontrol Listesi

#### 1. Her İki Pencere de Açık mı?
- ✅ "S2G Game Server" penceresi
- ✅ "Cloudflare Tunnel" penceresi

#### 2. Flask Sunucu Çalışıyor mu?
Lokal test:
```
http://localhost:5000
```

Açılıyorsa Flask tamam, sorun Cloudflare'de.

#### 3. Cloudflare Tunnel Bağlı mı?
Tunnel penceresinde şu mesajı görmelisiniz:
```
Connection registered
```

Görmüyorsanız:
- Config dosyasını kontrol edin
- Tunnel'ı yeniden oluşturun

#### 4. DNS Ayarları Doğru mu?
Cloudflare Dashboard'da:
- s2ggame.com → CNAME → [tunnel-id].cfargotunnel.com
- www.s2ggame.com → CNAME → [tunnel-id].cfargotunnel.com

#### 5. Nameserver Değişti mi?
Domain'inizin nameserver'ları Cloudflare'e işaret etmeli:
```
ns1.cloudflare.com
ns2.cloudflare.com
```

**Not:** Nameserver değişikliği 24-48 saat sürebilir!

## 🔄 Yeniden Başlatma

### Temiz Başlatma
1. Tüm pencereleri kapatın
2. Şunu çalıştırın:
```batch
BASLATMA_ADIM_ADIM.bat
```

### Hızlı Başlatma
```batch
HIZLI_BASLATMA.bat
```

## 🗑️ Sıfırlama ve Yeniden Kurulum

### Cloudflare Tunnel Sıfırlama
```batch
# Eski tunnel'ı sil
cloudflared.exe tunnel delete s2g-game

# Config dosyasını sil
del %USERPROFILE%\.cloudflared\config.yml

# Yeniden kur
CLOUDFLARE_SETUP_s2ggame.bat
```

### Veritabanı Sıfırlama
```batch
python reset_database.py
```

### Tam Sıfırlama
```batch
# Bağımlılıkları yeniden yükle
INSTALL.bat

# Veritabanını sıfırla
python reset_database.py

# Cloudflare'i yeniden kur
CLOUDFLARE_SETUP_s2ggame.bat
```

## 📋 Sık Karşılaşılan Hatalar

### "ModuleNotFoundError: No module named 'flask'"
**Çözüm:**
```batch
INSTALL.bat
```

### "Address already in use: Port 5000"
**Çözüm:**
```batch
# Port 5000'i kullanan programı bul
netstat -ano | findstr :5000

# Process ID'yi not alın ve sonlandırın
taskkill /F /PID [process_id]
```

### "cloudflared.exe is not recognized"
**Çözüm:**
- cloudflared.exe'yi s2g-game klasörüne kopyalayın
- Tam yol kullanın: `%CD%\cloudflared.exe`

### "tunnel not found"
**Çözüm:**
```batch
# Mevcut tunnel'ları listele
cloudflared.exe tunnel list

# Yoksa yeniden oluştur
CLOUDFLARE_SETUP_s2ggame.bat
```

### "ERR_NAME_NOT_RESOLVED" (Tarayıcı)
**Çözüm:**
- DNS propagation bekleyin (24-48 saat)
- Nameserver'ları kontrol edin
- Cloudflare Dashboard'da DNS kayıtlarını kontrol edin

## 🆘 Hala Çalışmıyor?

### Debug Modu

#### Flask Debug
```batch
cd s2g-game
set FLASK_DEBUG=1
python app.py
```

#### Cloudflare Debug
```batch
cloudflared.exe tunnel --loglevel debug run s2g-game
```

### Log Dosyaları
```batch
# Flask logları
type app.log

# Cloudflare logları
type %USERPROFILE%\.cloudflared\*.log
```

## 📞 Destek

### Kontrol Listesi (Destek İsterken)
- [ ] TEST_SISTEM.bat çıktısı
- [ ] Flask sunucu hata mesajı
- [ ] Cloudflare tunnel hata mesajı
- [ ] Config dosyası içeriği
- [ ] Nameserver bilgileri
- [ ] Ne kadar süre geçti (DNS propagation için)

### Yararlı Komutlar
```batch
# Sistem durumu
TEST_SISTEM.bat

# Python versiyonu
python --version

# Yüklü paketler
pip list

# Cloudflare tunnel listesi
cloudflared.exe tunnel list

# Config dosyası
type %USERPROFILE%\.cloudflared\config.yml

# Port kontrolü
netstat -ano | findstr :5000
```
