"""
Seyahat Planlama Uygulaması - Ana Mantık Modülü
================================================
Sınıflar: Seyahat, Konaklama, Plan, SeyahatAsistani,
HavaDurumu, UygulamaYoneticisi
"""

import sys
import os
import hashlib
import random
import time
import unicodedata
from datetime import datetime, timedelta
from database import Database


# ═══════════════════════════════════════════════════════════════════
#  SINIF: Seyahat
# ═══════════════════════════════════════════════════════════════════

class Seyahat:
    """Seyahat bilgilerini temsil eden sınıf"""

    def __init__(self, seyahat_id=None, kullanici_id=None, sehir="", ulke="",
                 baslangic_tarihi="", bitis_tarihi="", butce=0,
                 seyahat_turu="", notlar="", kapak_foto=""):
        self.seyahat_id = seyahat_id
        self.kullanici_id = kullanici_id
        self.sehir = sehir
        self.ulke = ulke
        self.baslangic_tarihi = baslangic_tarihi
        self.bitis_tarihi = bitis_tarihi
        self.butce = butce
        self.seyahat_turu = seyahat_turu
        self.notlar = notlar
        self.kapak_foto = kapak_foto

    def gun_sayisi(self):
        """Seyahat süresini gün olarak hesapla"""
        try:
            bas = datetime.strptime(self.baslangic_tarihi, "%Y-%m-%d")
            bit = datetime.strptime(self.bitis_tarihi, "%Y-%m-%d")
            return (bit - bas).days + 1
        except Exception:
            return 0

    def durum(self):
        """Seyahat durumunu belirle: yaklaşan / aktif / tamamlanan"""
        try:
            bugun = datetime.now().date()
            bas = datetime.strptime(self.baslangic_tarihi, "%Y-%m-%d").date()
            bit = datetime.strptime(self.bitis_tarihi, "%Y-%m-%d").date()
            if bugun < bas:
                return "yaklaşan"
            elif bas <= bugun <= bit:
                return "aktif"
            else:
                return "tamamlanan"
        except Exception:
            return "belirsiz"

    def kalan_gun(self):
        """Seyahata kalan gün sayısı"""
        try:
            bugun = datetime.now().date()
            bas = datetime.strptime(self.baslangic_tarihi, "%Y-%m-%d").date()
            if bugun < bas:
                return (bas - bugun).days
            return 0
        except Exception:
            return 0

    def to_dict(self):
        return {
            'seyahat_id': self.seyahat_id, 'sehir': self.sehir,
            'ulke': self.ulke, 'baslangic_tarihi': self.baslangic_tarihi,
            'bitis_tarihi': self.bitis_tarihi, 'butce': self.butce,
            'seyahat_turu': self.seyahat_turu, 'notlar': self.notlar,
            'gun_sayisi': self.gun_sayisi(), 'durum': self.durum()
        }


# ═══════════════════════════════════════════════════════════════════
#  SINIF: Konaklama
# ═══════════════════════════════════════════════════════════════════

class Konaklama:
    """Otel ve konaklama bilgilerini temsil eden sınıf"""

    def __init__(self, konaklama_id=None, seyahat_id=None, otel_adi="",
                 konum="", giris_tarihi="", cikis_tarihi="",
                 fiyat=0, yildiz=3, notlar=""):
        self.konaklama_id = konaklama_id
        self.seyahat_id = seyahat_id
        self.otel_adi = otel_adi
        self.konum = konum
        self.giris_tarihi = giris_tarihi
        self.cikis_tarihi = cikis_tarihi
        self.fiyat = fiyat
        self.yildiz = yildiz
        self.notlar = notlar

    def gece_sayisi(self):
        """Konaklama gece sayısını hesapla"""
        try:
            g = datetime.strptime(self.giris_tarihi, "%Y-%m-%d")
            c = datetime.strptime(self.cikis_tarihi, "%Y-%m-%d")
            return (c - g).days
        except Exception:
            return 0

    def gecede_fiyat(self):
        """Gece başına ortalama fiyat"""
        gece = self.gece_sayisi()
        return self.fiyat / gece if gece > 0 else self.fiyat


# ═══════════════════════════════════════════════════════════════════
#  SINIF: Plan
# ═══════════════════════════════════════════════════════════════════

class Plan:
    """Seyahat rotası ve günlük planları temsil eden sınıf"""

    def __init__(self, plan_id=None, seyahat_id=None, gun="", saat="",
                 baslik="", aciklama="", konum=""):
        self.plan_id = plan_id
        self.seyahat_id = seyahat_id
        self.gun = gun
        self.saat = saat
        self.baslik = baslik
        self.aciklama = aciklama
        self.konum = konum

    def rota_bilgisi(self):
        return f"{self.gun} {self.saat} - {self.baslik} ({self.konum})"


from ai import SeyahatAsistani


# ═══════════════════════════════════════════════════════════════════
#  SINIF: HavaDurumu
# ═══════════════════════════════════════════════════════════════════

class HavaDurumu:
    """Hava durumu bilgi sınıfı"""

    CACHE_TTL = 600
    _CACHE = {}

    VERILER = {
        "İstanbul":  {"sicaklik": 18, "durum": "Parçalı Bulutlu", "nem": 65, "ruzgar": 12, "ikon": "⛅"},
        "Paris":     {"sicaklik": 15, "durum": "Yağmurlu",        "nem": 78, "ruzgar": 15, "ikon": "🌧️"},
        "Roma":      {"sicaklik": 22, "durum": "Güneşli",         "nem": 55, "ruzgar":  8, "ikon": "☀️"},
        "Tokyo":     {"sicaklik": 20, "durum": "Güneşli",         "nem": 60, "ruzgar": 10, "ikon": "☀️"},
        "Barcelona": {"sicaklik": 24, "durum": "Güneşli",         "nem": 50, "ruzgar": 14, "ikon": "☀️"},
        "Londra":    {"sicaklik": 12, "durum": "Bulutlu",          "nem": 82, "ruzgar": 18, "ikon": "☁️"},
        "Dubai":     {"sicaklik": 35, "durum": "Güneşli",         "nem": 40, "ruzgar":  6, "ikon": "☀️"},
        "Antalya":   {"sicaklik": 28, "durum": "Güneşli",         "nem": 45, "ruzgar": 10, "ikon": "☀️"},
        "New York":  {"sicaklik": 16, "durum": "Parçalı Bulutlu", "nem": 62, "ruzgar": 20, "ikon": "⛅"},
        "Kapadokya": {"sicaklik": 15, "durum": "Açık",            "nem": 35, "ruzgar":  8, "ikon": "☀️"},
        "Amsterdam": {"sicaklik": 13, "durum": "Bulutlu",          "nem": 75, "ruzgar": 22, "ikon": "☁️"},
        "Prag":      {"sicaklik": 14, "durum": "Parçalı Bulutlu", "nem": 60, "ruzgar": 12, "ikon": "⛅"},
    }

    @classmethod
    def hava_getir(cls, sehir):
        """Hava durumu bilgisi döndür (API + fallback)"""
        sehir = (sehir or "").strip()
        cache_key = sehir.casefold()
        now = time.monotonic()
        cached = cls._CACHE.get(cache_key)
        if cached and now - cached["ts"] < cls.CACHE_TTL:
            return dict(cached["data"])

        # Önce API dene
        try:
            import requests
            url = f"https://wttr.in/{sehir}?format=j1"
            r = requests.get(url, timeout=4)
            if r.status_code == 200:
                d = r.json()
                cc = d.get("current_condition", [{}])[0]
                sicaklik = int(cc.get("temp_C", 20))
                desc = cc.get("lang_tr", [{}])
                durum = desc[0].get("value", "Belirsiz") if desc else cc.get("weatherDesc", [{}])[0].get("value", "N/A")
                sonuc = {
                    "sicaklik": sicaklik,
                    "durum": durum,
                    "nem": int(cc.get("humidity", 50)),
                    "ruzgar": int(cc.get("windspeedKmph", 10)),
                    "ikon": cls._ikon(sicaklik, durum)
                }
                cls._CACHE[cache_key] = {"ts": now, "data": dict(sonuc)}
                return sonuc
        except Exception:
            pass

        # Fallback verileri
        if sehir in cls.VERILER:
            v = cls.VERILER[sehir].copy()
            v["sicaklik"] += random.randint(-2, 2)
            cls._CACHE[cache_key] = {"ts": now, "data": dict(v)}
            return v
        sonuc = {"sicaklik": 20, "durum": "Veri Yok", "nem": 50, "ruzgar": 10, "ikon": "🌤️"}
        cls._CACHE[cache_key] = {"ts": now, "data": dict(sonuc)}
        return sonuc

    @staticmethod
    def _ikon(sicaklik, durum):
        d = durum.lower()
        if "yağmur" in d or "rain" in d:
            return "🌧️"
        if "kar" in d or "snow" in d:
            return "❄️"
        if "bulut" in d or "cloud" in d:
            return "☁️"
        if "güneş" in d or "clear" in d or "sunny" in d:
            return "☀️"
        return "🌤️"


# ═══════════════════════════════════════════════════════════════════
#  SINIF: UygulamaYoneticisi
# ═══════════════════════════════════════════════════════════════════

class UygulamaYoneticisi:
    """Ana uygulama yöneticisi - İş mantığını koordine eder"""

    def __init__(self):
        self.db = Database()
        self.db.demo_verilerini_hazirla()
        self.aktif_kullanici = None
        self.aktif_kullanici_id = None

    def kayit_ol(self, kullanici_adi, email, sifre, ad_soyad=""):
        """Yeni kullanıcı kaydı"""
        sifre_hash = hashlib.sha256(sifre.encode()).hexdigest()
        uid = self.db.kullanici_ekle(kullanici_adi, email, sifre_hash, ad_soyad)
        if uid:
            self.db.bildirim_ekle(uid, "Hoş Geldiniz! 🎉",
                                  "Seyahat Planlama uygulamasına hoş geldiniz!", "bilgi")
        return uid

    def giris_yap(self, kullanici_adi, sifre):
        """Kullanıcı girişi"""
        sifre_hash = hashlib.sha256(sifre.encode()).hexdigest()
        k = self.db.kullanici_giris(kullanici_adi, sifre_hash)
        if k:
            self.aktif_kullanici = dict(k)
            self.aktif_kullanici_id = k["id"]
            return True
        return False

    def demo_giris_yap(self):
        """Tek tikla demo hesabina giris yap."""
        self.db.demo_verilerini_hazirla()
        return self.giris_yap(self.db.DEMO_USERNAME, self.db.DEMO_PASSWORD)

    def cikis_yap(self):
        self.aktif_kullanici = None
        self.aktif_kullanici_id = None

    def seyahat_olustur(self, sehir, ulke, baslangic, bitis,
                        butce=0, tur="", notlar="", kapak=""):
        if not self.aktif_kullanici_id:
            return None
        return self.db.seyahat_ekle(
            self.aktif_kullanici_id, sehir, ulke, baslangic, bitis,
            butce, tur, notlar, kapak)

    def seyahatleri_listele(self, filtre=None):
        """Filtrelenmiş seyahat listesi döndür"""
        if not self.aktif_kullanici_id:
            return []
        rows = self.db.seyahatleri_getir(self.aktif_kullanici_id)
        sonuc = []
        for s in rows:
            obj = Seyahat(
                seyahat_id=s["id"], kullanici_id=s["kullanici_id"],
                sehir=s["sehir"], ulke=s["ulke"] or "",
                baslangic_tarihi=s["baslangic_tarihi"],
                bitis_tarihi=s["bitis_tarihi"],
                butce=s["butce"] or 0, seyahat_turu=s["seyahat_turu"] or "",
                notlar=s["notlar"] or "", kapak_foto=s["kapak_foto"] or "")
            if filtre:
                if filtre == "yaklaşan" and obj.durum() != "yaklaşan":
                    continue
                elif filtre == "aktif" and obj.durum() != "aktif":
                    continue
                elif filtre == "tamamlanan" and obj.durum() != "tamamlanan":
                    continue
            sonuc.append(obj)
        return sonuc

    @staticmethod
    def _tarih_coz(tarih_str, varsayilan=None):
        try:
            return datetime.strptime(tarih_str, "%Y-%m-%d").date()
        except (TypeError, ValueError):
            return varsayilan

    def oncelikli_seyahat(self, seyahatler=None):
        """Ana sayfada gösterilecek en uygun aktif/yaklaşan seyahati seç."""
        seyahatler = list(seyahatler) if seyahatler is not None else self.seyahatleri_listele()
        if not seyahatler:
            return None

        uzak_tarih = datetime.max.date()
        aktifler = [s for s in seyahatler if s.durum() == "aktif"]
        if aktifler:
            return min(
                aktifler,
                key=lambda s: (
                    self._tarih_coz(s.bitis_tarihi, uzak_tarih),
                    self._tarih_coz(s.baslangic_tarihi, uzak_tarih),
                    s.seyahat_id or 0,
                ),
            )

        yaklasanlar = [s for s in seyahatler if s.durum() == "yaklaşan"]
        if yaklasanlar:
            return min(
                yaklasanlar,
                key=lambda s: (
                    self._tarih_coz(s.baslangic_tarihi, uzak_tarih),
                    self._tarih_coz(s.bitis_tarihi, uzak_tarih),
                    s.seyahat_id or 0,
                ),
            )

        return None

    def butce_durumu(self, seyahat_id):
        """Bütçe özet bilgisi"""
        s = self.db.seyahat_getir(seyahat_id)
        if not s:
            return None
        toplam = self.db.harcama_toplam(seyahat_id)
        butce = s["butce"] or 0
        return {
            "butce": butce, "toplam_harcama": toplam,
            "kalan": butce - toplam,
            "yuzde": (toplam / butce * 100) if butce > 0 else 0,
            "kategori_dagilim": [dict(r) for r in self.db.harcama_kategori_toplam(seyahat_id)]
        }

    def ai_plan_olustur(self, sehir, butce, gun_sayisi, baslangic_tarihi=None, ozel_kategoriler=None):
        return SeyahatAsistani.plan_olustur(sehir, butce, gun_sayisi, baslangic_tarihi, ozel_kategoriler)

    def ai_sehir_oner(self, butce, gun_sayisi):
        return SeyahatAsistani.sehir_oner(butce, gun_sayisi)

    def hava_durumu_getir(self, sehir):
        return HavaDurumu.hava_getir(sehir)


# ═══════════════════════════════════════════════════════════════════
#  Uygulama Başlatma
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt

    if hasattr(Qt, "AA_ShareOpenGLContexts"):
        QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)

    from ui import SeyahatApp

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    yonetici = UygulamaYoneticisi()
    pencere = SeyahatApp(yonetici)
    pencere.show()
    sys.exit(app.exec_())
