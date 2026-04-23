# TravelPlan Uygulaması Kısa Dokümantasyon

## 1. Uygulama Tanımı

TravelPlan, kullanıcıların seyahatlerini tek bir masaüstü uygulaması üzerinden planlayıp yönetebilmesi için geliştirilmiş bir seyahat planlama uygulamasıdır. Uygulama; seyahat oluşturma, bütçe takibi, günlük planlama, konaklama ve uçuş yönetimi, harita görüntüleme ve AI destekli öneri üretme gibi işlevleri tek sistemde toplar.

## 2. Uygulamanın Temel Amacı

Uygulamanın amacı, seyahate ait tüm bilgileri tek bir merkezde toplamak ve kullanıcıya düzenli, takip edilebilir ve görsel olarak anlaşılır bir planlama deneyimi sunmaktır.

Bu kapsamda kullanıcı:

- seyahatlerini oluşturabilir ve listeleyebilir,
- seyahat detaylarını alt başlıklar halinde yönetebilir,
- bütçesini takip edebilir,
- plan ve aktivitelerini takvim üzerinde görebilir,
- harita üzerinden seyahat noktalarını inceleyebilir,
- AI desteği ile şehir ve plan önerisi alabilir.

## 3. Kullanılan Teknolojiler

Uygulamada kullanılan başlıca teknolojiler şunlardır:

- Python
- PyQt5
- SQLite
- QtWebEngine
- Leaflet.js
- Requests

## 4. Temel Özellikler

Uygulamanın mevcut özellikleri aşağıdaki gibidir:

- kullanıcı kayıt ve giriş sistemi
- profil güncelleme ve profil fotoğrafı yükleme
- açık ve koyu tema desteği
- yeni seyahat oluşturma
- seyahat listeleme, filtreleme ve arama
- seyahat detay ekranı
- konaklama ekleme ve silme
- aktivite ekleme ve silme
- bütçe ve harcama takibi
- manuel günlük plan oluşturma
- takvim görünümü
- seyahat haritası ve genel harita ekranı
- seyahat arkadaşları yönetimi
- uçuş bilgisi ekleme ve silme
- seyahat notları tutma
- bildirim sistemi
- AI ile şehir önerisi
- AI ile otomatik seyahat planı üretme
- hava durumu gösterimi

## 5. Ana Ekranlar

Uygulama aşağıdaki temel ekranlardan oluşur:

### Giriş ve Kayıt

Kullanıcının hesap oluşturduğu ve sisteme giriş yaptığı ekrandır.

### Ana Sayfa

Kullanıcının özet bilgi gördüğü ana paneldir. Burada öncelikli seyahat, takvim özeti, hava durumu, bildirimler ve genel harita görünümü yer alır.

### Seyahatler

Tüm seyahatlerin listelendiği, filtrelendiği ve arandığı ekrandır.

### Yeni Seyahat

Manuel seyahat oluşturma ekranıdır. Kullanıcı şehir, tarih, bütçe, tür, not ve kapak görseli bilgilerini girer.

### Seyahat Detay

Her seyahatin ayrıntılı yönetim ekranıdır. Bu alanda şu bölümler yer alır:

- genel bilgiler
- konaklama
- aktiviteler
- bütçe
- plan
- takvim
- harita
- arkadaşlar
- uçuşlar
- notlar

### Harita

Kullanıcının tüm seyahatlerini genel destinasyon haritası üzerinde görüntülediği sayfadır.

### Bildirimler

Sistemin oluşturduğu bildirimlerin listelendiği bölümdür.

### Profil

Kullanıcıya ait kişisel bilgilerin güncellendiği ekrandır.

### Ayarlar

Tema seçimi ve temel uygulama bilgilerini içeren bölümdür.

## 6. AI Destekli Özellikler

Uygulamada yerel veri seti ve kural tabanlı çalışan bir AI öneri sistemi bulunmaktadır.

AI modülü şu işlevleri sağlar:

- bütçe ve süreye göre şehir önerme
- seçilen şehir için günlük plan üretme
- otel, aktivite, yemek ve ulaşım önerileri sunma
- tahmini maliyet hesabı oluşturma

Üretilen AI planı, kullanıcı isterse doğrudan yeni bir seyahate veya mevcut bir seyahatin detayına uygulanabilir.

NOT: İlerleyen süreçte uygulamanın AI sistemi API sistemi kullanılarak geliştirilecektir. gerçek ve daha akıllı bir şekilde eğitilmiş bir yapay zeka olarak sunulacaktır .

## 7. Veritabanı Yapısı

Uygulama yerel SQLite veritabanı kullanır. Temel tablolar şunlardır:

- kullanicilar
- seyahatler
- konaklamalar
- aktiviteler
- harcamalar
- planlar
- arkadaslar
- bildirimler
- ucuslar

Bu yapı sayesinde kullanıcıya ait tüm seyahat verileri düzenli ve ilişkisel şekilde saklanır.


## NOT: 
Masaüstü kurulum (`setup.exe`) senaryosunda veri kaybını önlemek için veritabanı dosyası artık uygulama klasöründe değil, kullanıcıya ait kalıcı veri klasöründe saklanır. Windows üzerinde bu dosya `%LOCALAPPDATA%\SEYEHATApp\seyahat_planlama.db` yolunda tutulur. Uygulama ilk açılışta eski konumda bir veritabanı bulursa bunu yeni klasöre otomatik olarak kopyalayarak mevcut kayıtların korunmasını sağlar.

## Demo Hesap

Uygulama ilk acilista demo hesabi otomatik hazirlar.

- Kullanici adi: `demo`
- Sifre: `demo123`
- Demo seyahatler: aktif Istanbul, yaklasan Kapadokya ve tamamlanan Paris ornekleri

Demo verileri mevcut kullanici verilerini silmez. Demo hesabinda seyahat yoksa ornek seyahatleri tekrar olusturur.

## 8. Genel Mimari

Uygulama modüler bir mimari ile geliştirilmiştir. Ana yapı dört katmandan oluşur:

### Arayüz Katmanı

`ui.py` dosyasında yer alır. Tüm ekranlar, formlar, sekmeler, diyaloglar ve görsel bileşenler bu katmanda yönetilir.

### İş Mantığı Katmanı

`main.py` dosyasında yer alır. Kullanıcı işlemleri, seyahat yönetimi, bütçe özeti, hava durumu çağrıları ve genel uygulama kontrolü burada bulunur.

### Veritabanı Katmanı

`database.py` dosyasında yer alır. Tüm tablo yapıları, veri ekleme, silme, güncelleme ve sorgulama işlemleri bu katmanda yapılır.

### AI Katmanı

`ai.py` dosyasında yer alır. Şehir öneri sistemi ve plan üretme algoritması bu modülde çalışır.

## 9. Çalışma Mantığı

Uygulamanın genel akışı şu şekildedir:

1. Kullanıcı sisteme giriş yapar.
2. Ana ekrana geçer ve seyahatlerini görüntüler.
3. Yeni seyahat oluşturur veya mevcut bir seyahatin detayına girer.
4. Seyahatin alt modüllerini yönetir.
5. Gerekirse AI desteği ile plan oluşturur.
6. Veriler SQLite veritabanına kaydedilir ve arayüz buna göre güncellenir.

## 10. Sonuç

TravelPlan, seyahat planlama sürecini tek merkezden yönetmek için geliştirilmiş, kullanıcı yönetimi olan, veritabanı destekli, harita ve takvim bileşenleri içeren, AI destekli bir masaüstü uygulamasıdır. Proje; arayüz, iş mantığı, veritabanı ve AI katmanlarının ayrıldığı düzenli bir yapıya sahiptir ve temel seyahat planlama ihtiyaçlarını tek sistem içinde toplamayı hedefler.
