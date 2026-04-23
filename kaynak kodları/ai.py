"""
Seyahat Planlama Uygulaması - AI Modülü
========================================
Sınıflar: SeyahatAsistani
"""

import random
import unicodedata
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════════
#  SINIF: SeyahatAsistani (AI Önerileri)
# ═══════════════════════════════════════════════════════════════════

class SeyahatAsistani:
    """AI destekli seyahat öneri motoru"""

    SEHIR_VERILERI = {
        "İstanbul": {
            "ulke": "Türkiye", "lat": 41.0082, "lon": 28.9784,
            "aciklama": "Doğu ile Batı'nın buluştuğu eşsiz metropol",
            "aktiviteler": [
                "Ayasofya Camii", "Topkapı Sarayı", "Kapalıçarşı", "Galata Kulesi",
                "Boğaz Turu", "Yerebatan Sarnıcı", "Sultanahmet Camii",
                "İstiklal Caddesi", "Balat Turu", "Adalar Gezisi",
                "Dolmabahçe Sarayı", "Miniaturk", "Kız Kulesi"
            ],
            "oteller": [
                {"ad": "Four Seasons Sultanahmet", "fiyat": 3000, "yildiz": 5},
                {"ad": "Pera Palace Hotel", "fiyat": 2500, "yildiz": 5},
                {"ad": "The Marmara Taksim", "fiyat": 1500, "yildiz": 4},
                {"ad": "Hotel Amira Istanbul", "fiyat": 800, "yildiz": 3},
                {"ad": "Cheers Hostel", "fiyat": 300, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 200, "orta": 500, "yüksek": 1200},
            "yemekler": ["Kebap", "Balık Ekmek", "Kokoreç", "Kumpir", "Künefe", "Baklava"],
            "ulasim": ["Metro", "Tramvay", "Vapur", "Taksi", "Marmaray"]
        },
        "Paris": {
            "ulke": "Fransa", "lat": 48.8566, "lon": 2.3522,
            "aciklama": "Işıklar şehri, sanat ve romantizmin başkenti",
            "aktiviteler": [
                "Eyfel Kulesi", "Louvre Müzesi", "Notre-Dame", "Champs-Élysées",
                "Montmartre", "Versailles Sarayı", "Seine Nehri Turu",
                "Orsay Müzesi", "Disneyland Paris", "Arc de Triomphe"
            ],
            "oteller": [
                {"ad": "Le Meurice", "fiyat": 5000, "yildiz": 5},
                {"ad": "Hotel Plaza Athénée", "fiyat": 4000, "yildiz": 5},
                {"ad": "Hotel Le Marais", "fiyat": 1800, "yildiz": 4},
                {"ad": "Hôtel Des Arts", "fiyat": 900, "yildiz": 3},
                {"ad": "Generator Paris", "fiyat": 400, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 400, "orta": 800, "yüksek": 2000},
            "yemekler": ["Crêpe", "Croissant", "Escargot", "Ratatouille", "Macaron"],
            "ulasim": ["Metro", "RER", "Otobüs", "Taksi"]
        },
        "Roma": {
            "ulke": "İtalya", "lat": 41.9028, "lon": 12.4964,
            "aciklama": "Antik Roma'nın izlerini taşıyan ebedi şehir",
            "aktiviteler": [
                "Kolezyum", "Vatikan Müzesi", "Trevi Çeşmesi", "Pantheon",
                "İspanyol Merdivenleri", "Roma Forumu", "Sistine Şapeli",
                "Piazza Navona", "Trastevere", "Villa Borghese"
            ],
            "oteller": [
                {"ad": "Hotel de Russie", "fiyat": 4500, "yildiz": 5},
                {"ad": "Hotel Artemide", "fiyat": 1500, "yildiz": 4},
                {"ad": "Hotel Lancelot", "fiyat": 800, "yildiz": 3},
                {"ad": "Hotel Cosmo", "fiyat": 500, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 350, "orta": 700, "yüksek": 1800},
            "yemekler": ["Pizza", "Pasta", "Gelato", "Tiramisu", "Risotto"],
            "ulasim": ["Metro", "Otobüs", "Tramvay", "Taksi"]
        },
        "Tokyo": {
            "ulke": "Japonya", "lat": 35.6762, "lon": 139.6503,
            "aciklama": "Geleneksel kültür ile teknolojinin muhteşem uyumu",
            "aktiviteler": [
                "Sensoji Tapınağı", "Shibuya Geçidi", "Tokyo Kulesi",
                "Meiji Türbesi", "Akihabara", "Tsukiji Balık Pazarı",
                "Ueno Parkı", "Shinjuku", "Harajuku", "Tokyo Disneyland"
            ],
            "oteller": [
                {"ad": "The Peninsula Tokyo", "fiyat": 5000, "yildiz": 5},
                {"ad": "Hotel Gracery Shinjuku", "fiyat": 1500, "yildiz": 4},
                {"ad": "Shinjuku Granbell", "fiyat": 800, "yildiz": 3},
                {"ad": "Sakura Hotel", "fiyat": 400, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 500, "orta": 1000, "yüksek": 2500},
            "yemekler": ["Sushi", "Ramen", "Tempura", "Takoyaki", "Onigiri"],
            "ulasim": ["Shinkansen", "Metro", "Otobüs", "Taksi"]
        },
        "Barcelona": {
            "ulke": "İspanya", "lat": 41.3851, "lon": 2.1734,
            "aciklama": "Gaudi'nin eserleriyle süslü Akdeniz cenneti",
            "aktiviteler": [
                "Sagrada Familia", "Park Güell", "La Rambla", "Camp Nou",
                "Casa Batlló", "Gotik Mahalle", "Barceloneta Plajı",
                "Casa Milà", "Montjuïc", "Barselona Akvaryumu"
            ],
            "oteller": [
                {"ad": "Hotel Arts Barcelona", "fiyat": 4000, "yildiz": 5},
                {"ad": "Hotel Casa Fuster", "fiyat": 2000, "yildiz": 4},
                {"ad": "Hotel Jazz", "fiyat": 900, "yildiz": 3},
                {"ad": "TOC Hostel", "fiyat": 350, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 300, "orta": 700, "yüksek": 1800},
            "yemekler": ["Paella", "Tapas", "Churros", "Sangria", "Jamón"],
            "ulasim": ["Metro", "Otobüs", "Tramvay", "Taksi"]
        },
        "Londra": {
            "ulke": "İngiltere", "lat": 51.5074, "lon": -0.1278,
            "aciklama": "Tarihi ve modern yaşamın iç içe geçtiği başkent",
            "aktiviteler": [
                "Big Ben", "Tower Bridge", "British Museum", "Buckingham Sarayı",
                "London Eye", "Hyde Park", "Westminster Abbey",
                "Covent Garden", "Camden Market", "Tate Modern"
            ],
            "oteller": [
                {"ad": "The Ritz London", "fiyat": 6000, "yildiz": 5},
                {"ad": "The Langham", "fiyat": 3000, "yildiz": 4},
                {"ad": "Hub by Premier Inn", "fiyat": 1200, "yildiz": 3},
                {"ad": "YHA London", "fiyat": 500, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 500, "orta": 900, "yüksek": 2200},
            "yemekler": ["Fish & Chips", "Sunday Roast", "Afternoon Tea", "Pie & Mash"],
            "ulasim": ["Tube", "Bus", "Black Cab", "DLR"]
        },
        "Dubai": {
            "ulke": "BAE", "lat": 25.2048, "lon": 55.2708,
            "aciklama": "Lüks ve ihtişamın sembolü çöl metropolü",
            "aktiviteler": [
                "Burj Khalifa", "Dubai Mall", "Çöl Safarisi", "Palm Jumeirah",
                "Gold Souk", "Dubai Marina", "Burj Al Arab",
                "Miracle Garden", "Ski Dubai", "Dubai Çerçevesi"
            ],
            "oteller": [
                {"ad": "Burj Al Arab", "fiyat": 10000, "yildiz": 5},
                {"ad": "Atlantis The Palm", "fiyat": 5000, "yildiz": 5},
                {"ad": "Rove Downtown", "fiyat": 1500, "yildiz": 3},
                {"ad": "Premier Inn", "fiyat": 600, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 400, "orta": 1000, "yüksek": 3000},
            "yemekler": ["Shawarma", "Hummus", "Al Machboos", "Luqaimat"],
            "ulasim": ["Metro", "Taksi", "Uber", "Otobüs"]
        },
        "Antalya": {
            "ulke": "Türkiye", "lat": 36.8969, "lon": 30.7133,
            "aciklama": "Turkuaz sulara ve antik kalıntılara sahip tatil cenneti",
            "aktiviteler": [
                "Kaleiçi", "Düden Şelalesi", "Konyaaltı Plajı", "Aspendos",
                "Perge Antik Kenti", "Antalya Müzesi", "Olimpos",
                "Tahtalı Dağı Teleferik", "Kursunlu Şelalesi", "Lara Plajı"
            ],
            "oteller": [
                {"ad": "Mardan Palace", "fiyat": 3500, "yildiz": 5},
                {"ad": "Rixos Downtown", "fiyat": 2000, "yildiz": 5},
                {"ad": "Akra Hotel", "fiyat": 1200, "yildiz": 4},
                {"ad": "White Garden Hotel", "fiyat": 500, "yildiz": 3},
                {"ad": "Kaleiçi Pansiyon", "fiyat": 200, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 150, "orta": 400, "yüksek": 1000},
            "yemekler": ["Piyaz", "Tandır", "Şiş Köfte", "Balık", "Dondurma"],
            "ulasim": ["Tramvay", "Otobüs", "Dolmuş", "Taksi"]
        },
        "New York": {
            "ulke": "ABD", "lat": 40.7128, "lon": -74.0060,
            "aciklama": "Dünyanın en ikonik şehri, asla uyumayan metropol",
            "aktiviteler": [
                "Özgürlük Heykeli", "Times Square", "Central Park",
                "Empire State Building", "Brooklyn Köprüsü",
                "Metropolitan Müzesi", "Broadway", "5th Avenue",
                "Top of the Rock", "Wall Street"
            ],
            "oteller": [
                {"ad": "The Plaza Hotel", "fiyat": 7000, "yildiz": 5},
                {"ad": "The Standard", "fiyat": 3000, "yildiz": 4},
                {"ad": "Pod 51 Hotel", "fiyat": 1500, "yildiz": 3},
                {"ad": "HI NYC Hostel", "fiyat": 600, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 600, "orta": 1200, "yüksek": 3000},
            "yemekler": ["Hamburger", "NY Pizza", "Bagel", "Cheesecake", "Hot Dog"],
            "ulasim": ["Subway", "Bus", "Yellow Cab", "Ferry"]
        },
        "Kapadokya": {
            "ulke": "Türkiye", "lat": 38.6431, "lon": 34.8289,
            "aciklama": "Peribacalarıyla ünlü masalsı coğrafya",
            "aktiviteler": [
                "Balon Turu", "Göreme Açık Hava Müzesi", "Uçhisar Kalesi",
                "Derinkuyu Yeraltı Şehri", "Ihlara Vadisi", "Paşabağı",
                "Avanos Çömlekçilik", "Güvercinlik Vadisi", "ATV Turu"
            ],
            "oteller": [
                {"ad": "Museum Hotel", "fiyat": 4000, "yildiz": 5},
                {"ad": "Sultan Cave Suites", "fiyat": 2000, "yildiz": 4},
                {"ad": "Koza Cave Hotel", "fiyat": 1000, "yildiz": 3},
                {"ad": "Göreme Inn", "fiyat": 400, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 200, "orta": 500, "yüksek": 1500},
            "yemekler": ["Testi Kebabı", "Mantı", "Tandır", "Gözleme", "Pekmez"],
            "ulasim": ["Minibüs", "Kiralık Araba", "ATV", "Taksi"]
        },
        "Amsterdam": {
            "ulke": "Hollanda", "lat": 52.3676, "lon": 4.9041,
            "aciklama": "Kanalları, müzeleri ve özgür ruhuyla büyüleyen şehir",
            "aktiviteler": [
                "Anne Frank Evi", "Van Gogh Müzesi", "Rijksmuseum",
                "Kanal Turu", "Vondelpark", "Dam Meydanı",
                "Jordaan Mahallesi", "Albert Cuyp Pazarı"
            ],
            "oteller": [
                {"ad": "Waldorf Astoria", "fiyat": 4500, "yildiz": 5},
                {"ad": "NH Collection", "fiyat": 1800, "yildiz": 4},
                {"ad": "Hotel V Nesplein", "fiyat": 900, "yildiz": 3},
                {"ad": "The Flying Pig", "fiyat": 350, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 400, "orta": 800, "yüksek": 1800},
            "yemekler": ["Stroopwafel", "Bitterballen", "Herring", "Poffertjes"],
            "ulasim": ["Tramvay", "Bisiklet", "Metro", "Vapur"]
        },
        "Prag": {
            "ulke": "Çekya", "lat": 50.0755, "lon": 14.4378,
            "aciklama": "Gotik mimarisi ve masalsı atmosferiyle büyüleyen şehir",
            "aktiviteler": [
                "Charles Köprüsü", "Prag Kalesi", "Eski Şehir Meydanı",
                "Astronomik Saat", "Petřín Kulesi", "Josefov",
                "Vltava Nehri Turu", "Vyšehrad Kalesi"
            ],
            "oteller": [
                {"ad": "Four Seasons Prague", "fiyat": 3500, "yildiz": 5},
                {"ad": "Hotel Paris Prague", "fiyat": 1500, "yildiz": 4},
                {"ad": "Hotel Černý Slon", "fiyat": 700, "yildiz": 3},
                {"ad": "Czech Inn", "fiyat": 250, "yildiz": 2},
            ],
            "gunluk_maliyet": {"düşük": 200, "orta": 500, "yüksek": 1200},
            "yemekler": ["Trdelník", "Svíčková", "Gulaş", "Knedlík"],
            "ulasim": ["Metro", "Tramvay", "Otobüs", "Taksi"]
        },
    }

    SEHIR_VERILERI.update({

        "Bursa": {
            "ulke": "Türkiye", "lat": 40.1828, "lon": 29.0667,
            "aciklama": "Osmanlı'nın ilk başkenti, yeşili ve tarihiyle büyüleyici",
            "aktiviteler": ["Ulu Cami", "Yeşil Türbe", "Kozahan", "Uludağ Teleferik", "Cumalıkızık", "Tophane", "Irgandı Köprüsü", "Bursa Kent Müzesi"],
            "oteller": [{"ad": "Almira Hotel", "fiyat": 2500, "yildiz": 5}, {"ad": "Kitapevi Hotel", "fiyat": 1800, "yildiz": 4}, {"ad": "Bursa City Hotel", "fiyat": 800, "yildiz": 3}, {"ad": "Güner Hotel", "fiyat": 400, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 200, "orta": 500, "yüksek": 1100},
            "yemekler": ["İskender Kebap", "Pideli Köfte", "Kestane Şekeri", "Cantık", "İnegöl Köfte"],
            "ulasim": ["Metro", "Otobüs", "Teleferik", "Minibüs"]
        },
        "Trabzon": {
            "ulke": "Türkiye", "lat": 41.0027, "lon": 39.7168,
            "aciklama": "Doğa ve tarihin kucaklaştığı Karadeniz incisi",
            "aktiviteler": ["Sümela Manastırı", "Uzungöl", "Boztepe", "Ayasofya Müzesi", "Atatürk Köşkü", "Çal Mağarası", "Zağnos Vadisi"],
            "oteller": [{"ad": "Zorlu Grand Hotel", "fiyat": 2200, "yildiz": 5}, {"ad": "Novotel Trabzon", "fiyat": 1600, "yildiz": 4}, {"ad": "Usta Park Hotel", "fiyat": 900, "yildiz": 3}, {"ad": "Doğu Kaptan", "fiyat": 450, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 180, "orta": 450, "yüksek": 950},
            "yemekler": ["Kuymak", "Akçaabat Köftesi", "Hamsi Tava", "Mısır Ekmeği", "Karalahana Çorbası"],
            "ulasim": ["Otobüs", "Dolmuş", "Taksi", "Minibüs"]
        },
        "Gaziantep": {
            "ulke": "Türkiye", "lat": 37.0662, "lon": 37.3833,
            "aciklama": "Lezzetleri ve tarihi dokusuyla gastronomi şehri",
            "aktiviteler": ["Zeugma Mozaik Müzesi", "Gaziantep Kalesi", "Bakırcılar Çarşısı", "Emine Göğüş Mutfak Müzesi", "Tarihi Gümrük Hanı", "Zincirli Bedesten", "Rumkale"],
            "oteller": [{"ad": "Divan Gaziantep", "fiyat": 2100, "yildiz": 5}, {"ad": "Tuğcan Hotel", "fiyat": 1500, "yildiz": 4}, {"ad": "Gaziantep Şirehan", "fiyat": 1000, "yildiz": 3}, {"ad": "Efe Bey Konağı", "fiyat": 500, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 250, "orta": 600, "yüksek": 1200},
            "yemekler": ["Baklava", "Ali Nazik", "Beyran Çorbası", "Katmere", "Patlıcan Kebabı"],
            "ulasim": ["Tramvay", "Otobüs", "Taksi", "Minibüs"]
        },
        "Mardin": {
            "ulke": "Türkiye", "lat": 37.3122, "lon": 40.7339,
            "aciklama": "Taş evleri ve dar sokaklarıyla masalsı bir Mezopotamya şehri",
            "aktiviteler": ["Deyrulzafaran Manastırı", "Kasımiye Medresesi", "Mardin Kalesi", "Zinciriye Medresesi", "Mardin Müzesi", "Eski Mardin Sokakları", "Dara Antik Kenti"],
            "oteller": [{"ad": "Mardius Tarihi Konak", "fiyat": 3500, "yildiz": 5}, {"ad": "Artuklu Kervansarayı", "fiyat": 1800, "yildiz": 4}, {"ad": "Maridin Otel", "fiyat": 1200, "yildiz": 3}, {"ad": "Erdoba Konağı", "fiyat": 600, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 200, "orta": 550, "yüksek": 1300},
            "yemekler": ["Mardin Kebabı", "Semsek", "İrok", "Kaburga Dolması", "Süryani Şarabı"],
            "ulasim": ["Minibüs", "Taksi", "Yürüyüş"]
        },
        "Eskişehir": {
            "ulke": "Türkiye", "lat": 39.7767, "lon": 30.5206,
            "aciklama": "Porsuk boyunda genç, dinamik ve kültürel şehir",
            "aktiviteler": ["Odunpazarı Evleri", "Sazova Parkı", "Porsuk Çayı Tekne Turu", "Balmumu Müzesi", "Atlıhan El Sanatları Çarşısı", "Kurşunlu Camii", "Eskişehir Modern Müze"],
            "oteller": [{"ad": "Tasigo Hotels", "fiyat": 2800, "yildiz": 5}, {"ad": "Sennacity Hotel", "fiyat": 1600, "yildiz": 4}, {"ad": "The Merlot Hotel", "fiyat": 900, "yildiz": 3}, {"ad": "Omm Inn", "fiyat": 500, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 150, "orta": 400, "yüksek": 900},
            "yemekler": ["Çiğ Börek", "Balaban Köfte", "Met Helvası", "Haşhaşlı Çörek", "Boza"],
            "ulasim": ["Tramvay", "Otobüs", "Taksi", "Bot"]
        },
        "Çanakkale": {
            "ulke": "Türkiye", "lat": 40.1451, "lon": 26.4086,
            "aciklama": "Destanların yazıldığı, tarihi ve doğası zengin şehir",
            "aktiviteler": ["Gelibolu Yarımadası", "Truva Antik Kenti", "Aynalı Çarşı", "Çanakkale Şehitler Abidesi", "Bozcaada", "Assos Antik Kenti", "Kilitbahir Kalesi"],
            "oteller": [{"ad": "Kolin Hotel", "fiyat": 2000, "yildiz": 5}, {"ad": "Akol Hotel", "fiyat": 1400, "yildiz": 4}, {"ad": "Büyük Truva Hotel", "fiyat": 850, "yildiz": 3}, {"ad": "Anzac Hotel", "fiyat": 400, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 180, "orta": 450, "yüksek": 1000},
            "yemekler": ["Peynir Helvası", "Ezine Peyniri", "Deniz Mahsulleri", "Sardalya", "Biga Köftesi"],
            "ulasim": ["Vapur", "Otobüs", "Minibüs", "Taksi"]
        },
        "Şanlıurfa": {
            "ulke": "Türkiye", "lat": 37.1674, "lon": 38.7955,
            "aciklama": "Peygamberler şehri, tarihin sıfır noktası",
            "aktiviteler": ["Balıklıgöl", "Göbeklitepe", "Harran Evleri", "Şanlıurfa Arkeoloji Müzesi", "Gümrük Hanı", "Halil-ür Rahman Camii", "Halfeti"],
            "oteller": [{"ad": "Nevali Hotel", "fiyat": 1900, "yildiz": 5}, {"ad": "El-Ruha Hotel", "fiyat": 1500, "yildiz": 4}, {"ad": "Harran Hotel", "fiyat": 800, "yildiz": 3}, {"ad": "Cevahir Konuk Evi", "fiyat": 450, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 160, "orta": 420, "yüksek": 850},
            "yemekler": ["Çiğ Köfte", "Urfa Kebabı", "Şıllık Tatlısı", "Ciğer Kebabı", "Mırra"],
            "ulasim": ["Otobüs", "Minibüs", "Taksi"]
        }
,
        "İzmir": {
            "ulke": "Türkiye", "lat": 38.4237, "lon": 27.1428,
            "aciklama": "Kordon, tarih ve Ege ritmini bir araya getiren sahil şehri",
            "aktiviteler": ["Kordon Yürüyüşü", "Saat Kulesi", "Kemeraltı", "Asansör", "Kadifekale", "Efes Turu", "Alaçatı Gezisi", "Urla Bağ Rotası"],
            "oteller": [{"ad": "Swissotel Büyük Efes", "fiyat": 2600, "yildiz": 5}, {"ad": "Mövenpick İzmir", "fiyat": 1800, "yildiz": 4}, {"ad": "Park Inn Alsancak", "fiyat": 950, "yildiz": 3}, {"ad": "Lotus Garden Hostel", "fiyat": 350, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 220, "orta": 550, "yüksek": 1200},
            "yemekler": ["Boyoz", "Kumru", "Deniz mahsulleri", "İzmir köfte", "Söğüş"],
            "ulasim": ["İZBAN", "Vapur", "Metro", "Tramvay"]
        },
        "Ankara": {
            "ulke": "Türkiye", "lat": 39.9334, "lon": 32.8597,
            "aciklama": "Müzeleri, anıtları ve sakin temposuyla kültür odaklı başkent",
            "aktiviteler": ["Anıtkabir", "Anadolu Medeniyetleri Müzesi", "Hamamönü", "Ankara Kalesi", "Kuğulu Park", "Atakule", "CerModern", "Eymir Gölü"],
            "oteller": [{"ad": "Sheraton Ankara", "fiyat": 2400, "yildiz": 5}, {"ad": "Divan Çukurhan", "fiyat": 1700, "yildiz": 4}, {"ad": "Hotel Ickale", "fiyat": 900, "yildiz": 3}, {"ad": "Deeps Hostel", "fiyat": 280, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 180, "orta": 450, "yüksek": 900},
            "yemekler": ["Ankara tava", "Beypazarı güveci", "Döner", "Aspava", "Baklava"],
            "ulasim": ["Metro", "EGO otobüs", "Ankaray", "Taksi"]
        },
        "Berlin": {
            "ulke": "Almanya", "lat": 52.52, "lon": 13.405,
            "aciklama": "Tarih, gece hayatı ve çağdaş sanatın birlikte aktığı dinamik şehir",
            "aktiviteler": ["Brandenburg Kapısı", "Berlin Duvarı", "Museum Island", "Reichstag", "Alexanderplatz", "Tiergarten", "East Side Gallery", "Potsdamer Platz"],
            "oteller": [{"ad": "Hotel Adlon", "fiyat": 4200, "yildiz": 5}, {"ad": "Scandic Potsdamer Platz", "fiyat": 1600, "yildiz": 4}, {"ad": "Motel One Berlin", "fiyat": 950, "yildiz": 3}, {"ad": "Generator Berlin", "fiyat": 320, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 320, "orta": 750, "yüksek": 1600},
            "yemekler": ["Currywurst", "Pretzel", "Schnitzel", "Döner", "Apple strudel"],
            "ulasim": ["U-Bahn", "S-Bahn", "Tramvay", "Otobüs"]
        },
        "Viyana": {
            "ulke": "Avusturya", "lat": 48.2082, "lon": 16.3738,
            "aciklama": "Klasik müzik, saraylar ve kahve kültürüyle zarif Avrupa şehri",
            "aktiviteler": ["Schönbrunn Sarayı", "Belvedere", "Stephansdom", "Prater", "Hofburg", "Naschmarkt", "Albertina", "Tuna Kanalı"],
            "oteller": [{"ad": "Hotel Sacher", "fiyat": 4300, "yildiz": 5}, {"ad": "Austria Trend Savoyen", "fiyat": 1700, "yildiz": 4}, {"ad": "Motel One Wien", "fiyat": 980, "yildiz": 3}, {"ad": "Wombat's City Hostel", "fiyat": 340, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 340, "orta": 780, "yüksek": 1700},
            "yemekler": ["Wiener schnitzel", "Sachertorte", "Apfelstrudel", "Goulash", "Käsekrainer"],
            "ulasim": ["U-Bahn", "Tramvay", "Otobüs", "Bisiklet"]
        },
        "Lizbon": {
            "ulke": "Portekiz", "lat": 38.7223, "lon": -9.1393,
            "aciklama": "Yokuşlu sokakları, tramvayı ve okyanus manzaralarıyla sıcak bir kaçamak",
            "aktiviteler": ["Alfama", "Belém Kulesi", "Tram 28", "Jerónimos Manastırı", "LX Factory", "Time Out Market", "Sintra Günübirlik", "Miradouro da Senhora do Monte"],
            "oteller": [{"ad": "Bairro Alto Hotel", "fiyat": 3600, "yildiz": 5}, {"ad": "Lisboa Pessoa Hotel", "fiyat": 1500, "yildiz": 4}, {"ad": "My Story Hotel", "fiyat": 850, "yildiz": 3}, {"ad": "Yes Lisbon Hostel", "fiyat": 300, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 280, "orta": 650, "yüksek": 1500},
            "yemekler": ["Pastel de nata", "Bacalhau", "Bifana", "Sardalya", "Caldo verde"],
            "ulasim": ["Tramvay", "Metro", "Vapur", "Otobüs"]
        },
        "Atina": {
            "ulke": "Yunanistan", "lat": 37.9838, "lon": 23.7275,
            "aciklama": "Antik miras ile Akdeniz yaşamını aynı rotada sunan tarih şehri",
            "aktiviteler": ["Akropolis", "Plaka", "Parthenon", "Monastiraki", "Likavitos Tepesi", "Ulusal Arkeoloji Müzesi", "Pire Limanı", "Anafiotika"],
            "oteller": [{"ad": "Hotel Grande Bretagne", "fiyat": 3900, "yildiz": 5}, {"ad": "Electra Metropolis", "fiyat": 1700, "yildiz": 4}, {"ad": "Attalos Hotel", "fiyat": 900, "yildiz": 3}, {"ad": "Athens Hawks", "fiyat": 280, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 260, "orta": 620, "yüksek": 1450},
            "yemekler": ["Gyros", "Souvlaki", "Moussaka", "Greek salad", "Baklava"],
            "ulasim": ["Metro", "Otobüs", "Tramvay", "Taksi"]
        },
        "Budapeşte": {
            "ulke": "Macaristan", "lat": 47.4979, "lon": 19.0402,
            "aciklama": "Termal banyoları ve Tuna kıyısıyla romantik ama ekonomik şehir",
            "aktiviteler": ["Parlamento Binası", "Buda Kalesi", "Zincir Köprü", "Fisherman's Bastion", "Széchenyi Termal", "Ruin Barlar", "Andrassy Caddesi", "Margaret Adası"],
            "oteller": [{"ad": "Four Seasons Gresham", "fiyat": 3600, "yildiz": 5}, {"ad": "Hotel Moments", "fiyat": 1450, "yildiz": 4}, {"ad": "D8 Hotel", "fiyat": 780, "yildiz": 3}, {"ad": "Maverick City Lodge", "fiyat": 260, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 220, "orta": 520, "yüksek": 1200},
            "yemekler": ["Gulaş", "Langos", "Kürtőskalács", "Paprikash", "Dobos pasta"],
            "ulasim": ["Metro", "Tramvay", "Otobüs", "Tuna teknesi"]
        },
        "Bangkok": {
            "ulke": "Tayland", "lat": 13.7563, "lon": 100.5018,
            "aciklama": "Tapınaklar, sokak lezzetleri ve canlı gece hayatıyla yoğun Asya deneyimi",
            "aktiviteler": ["Grand Palace", "Wat Arun", "Chatuchak Market", "Chao Phraya Tekne Turu", "Asiatique", "Jim Thompson House", "Khao San Road", "Lumphini Park"],
            "oteller": [{"ad": "Mandarin Oriental", "fiyat": 4200, "yildiz": 5}, {"ad": "Amara Bangkok", "fiyat": 1500, "yildiz": 4}, {"ad": "ibis Styles Bangkok", "fiyat": 700, "yildiz": 3}, {"ad": "Lub d Bangkok", "fiyat": 240, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 180, "orta": 500, "yüksek": 1300},
            "yemekler": ["Pad Thai", "Tom Yum", "Mango sticky rice", "Green curry", "Satay"],
            "ulasim": ["BTS", "MRT", "Tuk Tuk", "Nehir teknesi"]
        },
        "Seul": {
            "ulke": "Güney Kore", "lat": 37.5665, "lon": 126.978,
            "aciklama": "Teknoloji, sokak modası ve saray kültürünü birleştiren hızlı şehir",
            "aktiviteler": ["Gyeongbokgung", "Bukchon Hanok Köyü", "Myeongdong", "N Seoul Tower", "Hongdae", "Dongdaemun", "Han Nehri", "COEX Library"],
            "oteller": [{"ad": "Lotte Hotel Seoul", "fiyat": 3800, "yildiz": 5}, {"ad": "Nine Tree Premier", "fiyat": 1600, "yildiz": 4}, {"ad": "Hotel Midcity", "fiyat": 850, "yildiz": 3}, {"ad": "Step Inn Myeongdong", "fiyat": 290, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 300, "orta": 760, "yüksek": 1700},
            "yemekler": ["Bibimbap", "Korean BBQ", "Tteokbokki", "Kimchi", "Hotteok"],
            "ulasim": ["Metro", "Otobüs", "AREX", "Taksi"]
        },
        "Singapur": {
            "ulke": "Singapur", "lat": 1.3521, "lon": 103.8198,
            "aciklama": "Düzenli şehir yaşamı, gökdelenler ve bahçelerle kompakt ama güçlü rota",
            "aktiviteler": ["Marina Bay Sands", "Gardens by the Bay", "Sentosa", "Chinatown", "Little India", "Clarke Quay", "Merlion Park", "Universal Studios Singapore"],
            "oteller": [{"ad": "Marina Bay Sands", "fiyat": 5200, "yildiz": 5}, {"ad": "Paradox Singapore", "fiyat": 2200, "yildiz": 4}, {"ad": "Hotel Mi", "fiyat": 1100, "yildiz": 3}, {"ad": "The Pod Boutique", "fiyat": 420, "yildiz": 2}],
            "gunluk_maliyet": {"düşük": 420, "orta": 900, "yüksek": 2100},
            "yemekler": ["Hainanese chicken rice", "Laksa", "Chili crab", "Satay", "Kaya toast"],
            "ulasim": ["MRT", "Otobüs", "Taksi", "Yürüyüş"]
        },
    })
    TEMA_SABLONLARI = [
        ("Tarihi Merkez", {"Tarihi", "Kültür"}),
        ("Şehir Ritmi", {"Keşif", "Deneyim"}),
        ("Manzara ve Fotoğraf", {"Doğa", "Keşif"}),
        ("Yerel Yaşam", {"Kültür", "Keşif"}),
    ]

    @staticmethod
    def _normalize_text(text):
        text = (text or "").strip().lower()
        text = text.replace("ı", "i").replace("İ", "i")
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

    @classmethod
    def _sehir_bul(cls, sehir):
        if sehir in cls.SEHIR_VERILERI:
            return sehir, cls.SEHIR_VERILERI[sehir]

        hedef = cls._normalize_text(sehir)
        if not hedef:
            return None, None

        for ad, veri in cls.SEHIR_VERILERI.items():
            if cls._normalize_text(ad) == hedef:
                return ad, veri

        adaylar = []
        for ad, veri in cls.SEHIR_VERILERI.items():
            norm = cls._normalize_text(ad)
            if hedef in norm or norm in hedef:
                adaylar.append((abs(len(norm) - len(hedef)), ad, veri))
        if adaylar:
            _, ad, veri = sorted(adaylar, key=lambda x: x[0])[0]
            return ad, veri
        return None, None

    @classmethod
    def _aktivite_kategorisi(cls, aktivite_adi):
        ad = cls._normalize_text(aktivite_adi)
        harita = {
            "Tarihi": ["muze", "museum", "saray", "camii", "cathedral", "church", "tapinak", "kale", "fort", "palace", "manastir", "forum", "bridge"],
            "Doğa": ["plaj", "beach", "park", "bahce", "garden", "vadi", "ada", "golu", "nehri", "waterfall", "dag", "tepe"],
            "Keşif": ["cadde", "street", "market", "carsi", "mahalle", "meydan", "square", "mall", "road", "factory"],
            "Deneyim": ["tur", "cruise", "safari", "disney", "teleferik", "balon", "atv", "tekne", "universal", "termal"],
        }
        for kategori, kelimeler in harita.items():
            if any(kelime in ad for kelime in kelimeler):
                return kategori
        return "Kültür"

    @classmethod
    def _aktivite_fiyati(cls, kategori, seviye):
        taban = {"Tarihi": 320, "Doğa": 120, "Keşif": 160, "Deneyim": 520, "Kültür": 240}
        katsayi = {"düşük": 0.7, "orta": 1.0, "yüksek": 1.35}[seviye]
        return int(round(taban[kategori] * katsayi, -1))

    @classmethod
    def _otel_sec(cls, oteller, gunluk_butce):
        oteller = sorted(oteller, key=lambda x: x["fiyat"])
        hedef = max(gunluk_butce * 0.45, oteller[0]["fiyat"])
        uygunlar = [otel for otel in oteller if otel["fiyat"] <= gunluk_butce * 0.6]
        if uygunlar:
            return sorted(uygunlar, key=lambda x: (-x["yildiz"], -x["fiyat"]))[0]
        return sorted(oteller, key=lambda x: (abs(x["fiyat"] - hedef), -x["yildiz"]))[0]

    @classmethod
    def _siradaki_aktivite(cls, havuz, kullanilanlar, tercih_kategorileri):
        for aktivite in havuz:
            if aktivite["ad"] in kullanilanlar:
                continue
            if aktivite["kategori"] in tercih_kategorileri:
                kullanilanlar.add(aktivite["ad"])
                return aktivite
        for aktivite in havuz:
            if aktivite["ad"] not in kullanilanlar:
                kullanilanlar.add(aktivite["ad"])
                return aktivite
        return None

    @classmethod
    def _ideal_gun_sayisi(cls, veri):
        return max(2, min(6, round(len(veri["aktiviteler"]) / 2.5)))

    @classmethod
    def sehir_listesi(cls):
        """Mevcut şehirlerin listesini döndür"""
        return sorted(cls.SEHIR_VERILERI.keys(), key=cls._normalize_text)

    @classmethod
    def sehir_oner(cls, butce, gun_sayisi):
        """Bütçeye uygun şehirleri öner"""
        uygun = []
        for sehir, veri in cls.SEHIR_VERILERI.items():
            min_otel = min(o["fiyat"] for o in veri["oteller"])
            orta_otel = sorted(o["fiyat"] for o in veri["oteller"])[len(veri["oteller"]) // 2]
            minimum = (veri["gunluk_maliyet"]["düşük"] + min_otel) * gun_sayisi
            hedef = (veri["gunluk_maliyet"]["orta"] + orta_otel) * gun_sayisi
            if minimum > butce * 1.15:
                continue

            ideal = cls._ideal_gun_sayisi(veri)
            butce_puani = max(0, 100 - abs(hedef - butce) / max(hedef, 1) * 70)
            sure_puani = max(0, 100 - abs(ideal - gun_sayisi) * 18)
                        # Yapay zeka ile dinamik skorlama ve zengin öneri algoritması
            aktivite_cesitliligi = len(veri["aktiviteler"]) / 10.0
            puan = round((butce_puani * 0.5) + (sure_puani * 0.3) + (aktivite_cesitliligi * 20), 1)
            puan = min(100, puan)

            uygun.append({
                "sehir": sehir,
                "ulke": veri["ulke"],
                "aciklama": veri.get("aciklama", ""),
                "tahmini_maliyet": int(hedef),
                "uyum_puani": puan,
                "neden": f"{gun_sayisi} günlük gezi için uygun tempo, tahmini bütçe ≈ ₺{hedef:,.0f}",
                "lat": veri["lat"],
                "lon": veri["lon"]
            })
        return sorted(uygun, key=lambda x: (-x["uyum_puani"], x["tahmini_maliyet"]))

    @classmethod
    def plan_olustur(cls, sehir, butce, gun_sayisi, baslangic_tarihi=None, ozel_kategoriler=None):
        sehir_adi, veri = cls._sehir_bul(sehir)
        if not sehir_adi or not veri:
            return None

        plan_baslangici = None
        if baslangic_tarihi:
            try:
                plan_baslangici = datetime.strptime(baslangic_tarihi, "%Y-%m-%d")
            except ValueError:
                plan_baslangici = None

        gunluk_butce = butce / max(gun_sayisi, 1)
        if gunluk_butce < veri["gunluk_maliyet"]["orta"]:
            seviye = "düşük"
        elif gunluk_butce < veri["gunluk_maliyet"]["yüksek"]:
            seviye = "orta"
        else:
            seviye = "yüksek"

        rastgele = random.Random(f"{sehir_adi}-{int(butce)}-{gun_sayisi}")
        otel = cls._otel_sec(veri["oteller"], gunluk_butce)
        aktiviteler = []
        for aktivite_adi in veri["aktiviteler"]:
            kategori = cls._aktivite_kategorisi(aktivite_adi)
            aktiviteler.append({
                "ad": aktivite_adi,
                "kategori": kategori,
                "fiyat": cls._aktivite_fiyati(kategori, seviye),
                "aciklama": f"{aktivite_adi} için {kategori.lower()} odaklı ziyaret önerisi.",
                "konum": aktivite_adi
            })
        rastgele.shuffle(aktiviteler)

        kullanilanlar = set()
        gunluk_plan = []
        hedef_aktivite = 2 if seviye == "düşük" or gun_sayisi >= 5 else 3
        toplam_aktivite_maliyeti = 0

        for gun in range(1, gun_sayisi + 1):
            tema, tercihler = cls.TEMA_SABLONLARI[(gun - 1) % len(cls.TEMA_SABLONLARI)]
            if ozel_kategoriler:
                tercihler = set(ozel_kategoriler)
                tema = "Kişiselleştirilmiş"
            tarih_label = f"Gün {gun}"
            if plan_baslangici:
                tarih_label = (plan_baslangici + timedelta(days=gun - 1)).strftime("%Y-%m-%d")
            gun_plani = [{
                "tur": "plan",
                "kategori": "Ulaşım",
                "saat": "09:00",
                "baslik": f"{tema} rotasına başlangıç",
                "aciklama": f"Güne {rastgele.choice(veri['ulasim'])} ile başlayıp bölge odaklı rota kurulması önerilir.",
                "konum": sehir_adi,
                "fiyat": 0
            }]

            secilenler = []
            for saat in ["10:30", "15:00", "18:30"][:hedef_aktivite]:
                aktivite = cls._siradaki_aktivite(aktiviteler, kullanilanlar, tercihler)
                if aktivite:
                    secilenler.append((saat, aktivite))

            for saat, aktivite in secilenler[:1]:
                gun_plani.append({
                    "tur": "aktivite",
                    "kategori": aktivite["kategori"],
                    "saat": saat,
                    "baslik": aktivite["ad"],
                    "aciklama": aktivite["aciklama"],
                    "konum": aktivite["konum"],
                    "fiyat": aktivite["fiyat"]
                })
                toplam_aktivite_maliyeti += aktivite["fiyat"]

            gun_plani.append({
                "tur": "plan",
                "kategori": "Yemek",
                "saat": "13:00",
                "baslik": f"Öğle molası: {rastgele.choice(veri['yemekler'])}",
                "aciklama": "Şehir temposunu bölmeden yerel tatlarla kısa mola önerilir.",
                "konum": sehir_adi,
                "fiyat": 0
            })

            for saat, aktivite in secilenler[1:]:
                gun_plani.append({
                    "tur": "aktivite",
                    "kategori": aktivite["kategori"],
                    "saat": saat,
                    "baslik": aktivite["ad"],
                    "aciklama": aktivite["aciklama"],
                    "konum": aktivite["konum"],
                    "fiyat": aktivite["fiyat"]
                })
                toplam_aktivite_maliyeti += aktivite["fiyat"]

            gun_plani.append({
                "tur": "plan",
                "kategori": "Yemek",
                "saat": "20:00",
                "baslik": f"Akşam programı: {rastgele.choice(veri['yemekler'])}",
                "aciklama": "Akşamı daha sakin bir tempoyla kapatmak için yerel lezzet odaklı mola.",
                "konum": sehir_adi,
                "fiyat": 0
            })

            gunluk_plan.append({
                "gun": gun,
                "tarih_label": tarih_label,
                "tema": tema,
                "plan": sorted(gun_plani, key=lambda x: x["saat"])
            })

        otel_toplam = otel["fiyat"] * gun_sayisi
        gunluk_maliyet = veri["gunluk_maliyet"][seviye]
        yemek_t = int(gunluk_maliyet * 0.28 * gun_sayisi)
        ulasim_t = int(gunluk_maliyet * 0.18 * gun_sayisi)
        diger_t = int(gunluk_maliyet * 0.12 * gun_sayisi)

        return {
            "sehir": sehir_adi,
            "ulke": veri["ulke"],
            "aciklama": veri.get("aciklama", ""),
            "gun_sayisi": gun_sayisi,
            "butce": butce,
            "seviye": seviye,
            "otel": otel,
            "otel_toplam": otel_toplam,
            "gunluk_plan": gunluk_plan,
            "oneriler": [
                f"Şehir içi ulaşım için öne çıkan seçenek: {rastgele.choice(veri['ulasim'])}",
                f"Günlük tempo: {'yoğun' if hedef_aktivite == 3 else 'dengeli'}",
                f"Önerilen konaklama seviyesi: {otel['yildiz']} yıldız"
            ],
            "tahmini_maliyet": {
                "Konaklama": otel_toplam,
                "Yemek": yemek_t,
                "Ulaşım": ulasim_t,
                "Aktivite": toplam_aktivite_maliyeti,
                "Diğer": diger_t,
                "toplam": otel_toplam + yemek_t + ulasim_t + toplam_aktivite_maliyeti + diger_t
            },
            "ulasim_onerileri": veri["ulasim"],
            "yemek_onerileri": veri["yemekler"],
            "koordinatlar": {"lat": veri["lat"], "lon": veri["lon"]}
        }
        """Detaylı AI seyahat planı oluştur"""
        if sehir not in cls.SEHIR_VERILERI:
            return None

        v = cls.SEHIR_VERILERI[sehir]

        # Bütçe seviyesi belirle
        gunluk_butce = butce / max(gun_sayisi, 1)
        if gunluk_butce < v["gunluk_maliyet"]["orta"]:
            seviye = "düşük"
        elif gunluk_butce < v["gunluk_maliyet"]["yüksek"]:
            seviye = "orta"
        else:
            seviye = "yüksek"

        # Uygun otel seç
        oteller = sorted(v["oteller"], key=lambda x: x["fiyat"])
        if seviye == "düşük":
            otel = oteller[0]
        elif seviye == "orta":
            otel = oteller[len(oteller) // 2]
        else:
            otel = oteller[-1]

        # Günlük plan oluştur
        aktiviteler = list(v["aktiviteler"])
        random.shuffle(aktiviteler)
        saatler = ["09:00", "10:30", "12:30", "14:30", "16:30", "19:00"]
        etiketler = ["🏛️", "📸", "🍽️", "🎭", "🌅", "🍽️"]

        gunluk_plan = []
        for gun in range(1, gun_sayisi + 1):
            gun_plani = []
            for i, saat in enumerate(saatler):
                if i == 2:  # öğle
                    yemek = random.choice(v["yemekler"])
                    gun_plani.append({
                        "saat": saat,
                        "baslik": f"🍽️ Öğle: {yemek}",
                        "aciklama": f"Yerel restoranda {yemek} deneyimi",
                        "konum": sehir
                    })
                elif i == 5:  # akşam
                    yemek = random.choice(v["yemekler"])
                    gun_plani.append({
                        "saat": saat,
                        "baslik": f"🍽️ Akşam: {yemek}",
                        "aciklama": f"Akşam yemeği - {yemek}",
                        "konum": sehir
                    })
                else:
                    if aktiviteler:
                        akt = aktiviteler.pop(0)
                    else:
                        akt = "Serbest Keşif"
                    gun_plani.append({
                        "saat": saat,
                        "baslik": f"{etiketler[i]} {akt}",
                        "aciklama": f"{akt} ziyareti ve keşfi",
                        "konum": sehir
                    })
            gunluk_plan.append({"gun": gun, "tarih_label": f"Gün {gun}", "plan": gun_plani})

        # Maliyet dağılımı
        otel_toplam = otel["fiyat"] * gun_sayisi
        gm = v["gunluk_maliyet"][seviye]
        yemek_t = gm * 0.35 * gun_sayisi
        ulasim_t = gm * 0.20 * gun_sayisi
        aktivite_t = gm * 0.30 * gun_sayisi
        diger_t = gm * 0.15 * gun_sayisi

        return {
            "sehir": sehir, "ulke": v["ulke"],
            "aciklama": v.get("aciklama", ""),
            "gun_sayisi": gun_sayisi, "butce": butce, "seviye": seviye,
            "otel": otel, "otel_toplam": otel_toplam,
            "gunluk_plan": gunluk_plan,
            "tahmini_maliyet": {
                "Konaklama": otel_toplam, "Yemek": yemek_t,
                "Ulaşım": ulasim_t, "Aktivite": aktivite_t,
                "Diğer": diger_t,
                "toplam": otel_toplam + yemek_t + ulasim_t + aktivite_t + diger_t
            },
            "ulasim_onerileri": v["ulasim"],
            "yemek_onerileri": v["yemekler"],
            "koordinatlar": {"lat": v["lat"], "lon": v["lon"]}
        }


