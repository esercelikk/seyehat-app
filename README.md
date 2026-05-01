#  TravelPlan – Akıllı Seyahat Planlama Uygulaması

> Seyahatlerinizi tek bir yerden planlayıp yönetebileceğiniz, AI destekli modern bir masaüstü uygulaması.

---

##  Genel Bakış

**TravelPlan**, kullanıcıların seyahatlerini planlamasını, yönetmesini ve takip etmesini sağlayan masaüstü tabanlı bir uygulamadır.

Planlama, bütçe yönetimi, harita, takvim ve yapay zeka destekli önerileri tek bir sistemde birleştirir.

---

##  Amaç

Bu uygulamanın amacı, seyahat sürecini **tek merkezden yönetilebilir, düzenli ve anlaşılır** hale getirmektir.

TravelPlan ile kullanıcılar:

- Seyahat oluşturabilir ve yönetebilir
- Bütçesini takip edebilir
- Günlük plan oluşturabilir
- Harita üzerinden konumları inceleyebilir
- Yapay zeka ile öneriler alabilir

---

##  Özellikler

###  Kullanıcı Sistemi
- Kayıt olma ve giriş yapma
- Profil düzenleme
- Profil fotoğrafı yükleme

###  Seyahat Yönetimi
- Yeni seyahat oluşturma
- Seyahat düzenleme ve silme
- Arama ve filtreleme
- Seyahat listeleme

###  Seyahat Detayları
- Konaklama ekleme ve silme
- Aktivite planlama
- Uçuş bilgisi ekleme
- Notlar
- Seyahat arkadaşları

###  Planlama Araçları
- Günlük plan oluşturma
- Takvim görünümü
- Zaman çizelgesi

###  Bütçe Sistemi
- Harcama takibi
- Bütçe yönetimi

###  Harita Özellikleri
- Seyahat noktalarını görüntüleme
- Genel harita ekranı

###  Bildirim Sistemi
- Sistem bildirimleri

###  Arayüz Özellikleri
- Açık / Koyu tema

###  Yapay Zeka Özellikleri
- Bütçeye ve süreye göre şehir önerisi
- Otomatik seyahat planı oluşturma
- Maliyet tahmini
- Aktivite, otel ve ulaşım önerileri

---

##  Kullanılan Teknolojiler

- **Python**
- **PyQt5**
- **SQLite**
- **QtWebEngine**
- **Leaflet.js**
- **Requests**

---

##  Yapay Zeka Sistemi

Uygulama içerisinde **kural tabanlı yerel bir AI sistemi** bulunmaktadır.

Bu sistem:

- Şehir önerileri yapar
- Seyahat planı oluşturur
- Aktivite ve konaklama önerir
- Tahmini maliyet hesaplar

> ⚠️ Gelecekte API tabanlı daha gelişmiş bir yapay zeka entegrasyonu yapılacaktır.

---

##  Veritabanı Yapısı

Uygulama **SQLite** kullanır.

Temel tablolar:

- kullanicilar  
- seyahatler  
- konaklamalar  
- aktiviteler  
- harcamalar  
- planlar  
- arkadaslar  
- bildirimler  
- ucuslar  

---

##  Mimari Yapı

Proje **modüler mimari** ile geliştirilmiştir:

###  Arayüz Katmanı
- `ui.py`  
Tüm ekran ve görsel bileşenleri yönetir  

###  İş Mantığı Katmanı
- `main.py`  
Uygulama akışı ve işlemler  

###  Veritabanı Katmanı
- `database.py`  
Veri işlemleri  

###  AI Katmanı
- `ai.py`  
Öneri ve planlama sistemi  

---

##  Veri Saklama (ÖNEMLİ)

Veri kaybını önlemek için veritabanı:

```
%LOCALAPPDATA%\SEYEHATApp\seyahat_planlama.db
```

konumunda saklanır.

İlk açılışta:
- Eski veriler otomatik taşınır

---

##  Demo Hesap

Uygulamayı test etmek için:

```
Kullanıcı adı: demo
Şifre: demo123
```

Demo içerikleri:

- Aktif seyahat: İstanbul  
- Yaklaşan: Kapadokya  
- Tamamlanan: Paris  

---

##  Çalışma Mantığı

1. Kullanıcı giriş yapar  
2. Ana ekranı görüntüler  
3. Yeni seyahat oluşturur veya mevcut olanı seçer  
4. Seyahat detaylarını yönetir  
5. İsterse AI ile plan oluşturur  
6. Veriler SQLite’a kaydedilir  

---

##  Kurulum

```bash
pip install -r requirements.txt
python main.py
```

Veya hazır **setup.exe** dosyası kullanılabilir.

---

##  Proje Amacı

TravelPlan:

- Temiz arayüz  
- Güçlü mimari  
- Akıllı planlama  
- AI destekli karar sistemi  

sunmayı hedefler.

---

##  Geliştirici

**Eser Çelik**  
Bilgisayar Programcılığı
---

## ⭐ Gelecek Geliştirmeler

- Gerçek AI API entegrasyonu  
- Bulut senkronizasyonu  
- Mobil uygulama  
- Çoklu kullanıcı desteği  
- Gelişmiş analiz sistemi  
