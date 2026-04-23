"""
Seyahat Planlama Uygulaması - Veritabanı Modülü
================================================
SQLite veritabanı işlemleri: Kullanıcı, Seyahat, Konaklama,
Aktivite, Harcama, Plan, Arkadaş, Bildirim, Uçuş tabloları
"""

import hashlib
import os
import re
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta


class Database:
    """Veritabanı yönetim sınıfı - Tüm CRUD işlemlerini yönetir"""

    DEMO_USERNAME = "demo"
    DEMO_PASSWORD = "demo123"
    DEMO_EMAIL = "demo@travelplan.local"

    def __init__(self, db_name="seyahat_planlama.db"):
        self.db_path = self._resolve_db_path(db_name)
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.migrate_schema()
        self.create_indexes()

    @staticmethod
    def _data_dir():
        override = os.environ.get("SEYEHAT_DB_DIR")
        if override:
            return override

        root = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        if root:
            return os.path.join(root, "SEYEHATApp")

        if sys.platform == "darwin":
            return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "SEYEHATApp")

        return os.path.join(os.path.expanduser("~"), ".seyahat_app")

    @staticmethod
    def _legacy_db_candidates(db_name):
        candidates = []
        module_dir = os.path.dirname(os.path.abspath(__file__))
        candidates.append(os.path.join(module_dir, db_name))
        candidates.append(os.path.join(os.getcwd(), db_name))

        if getattr(sys, "frozen", False):
            candidates.append(os.path.join(os.path.dirname(sys.executable), db_name))
            bundle_dir = getattr(sys, "_MEIPASS", "")
            if bundle_dir:
                candidates.append(os.path.join(bundle_dir, db_name))

        unique = []
        for path in candidates:
            abs_path = os.path.abspath(path)
            if abs_path not in unique:
                unique.append(abs_path)
        return unique

    @classmethod
    def _resolve_db_path(cls, db_name):
        if db_name == ":memory:":
            return db_name

        if os.path.isabs(db_name):
            db_dir = os.path.dirname(db_name)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            return db_name

        data_dir = cls._data_dir()
        os.makedirs(data_dir, exist_ok=True)
        target = os.path.join(data_dir, db_name)
        target_abs = os.path.abspath(target)

        if not os.path.exists(target):
            for old_path in cls._legacy_db_candidates(db_name):
                if old_path == target_abs or not os.path.exists(old_path):
                    continue
                try:
                    if os.path.getsize(old_path) > 0:
                        shutil.copy2(old_path, target)
                        break
                except OSError:
                    continue

        return target

    def connect(self):
        """Veritabanına bağlan"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

    @staticmethod
    def _dict_or_none(row):
        return dict(row) if row else None

    @staticmethod
    def _list_dicts(rows):
        return [dict(row) for row in rows]

    @staticmethod
    def _placeholders(values):
        return ",".join("?" for _ in values)

    def create_tables(self):
        """Tüm tabloları oluştur"""
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS kullanicilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                sifre TEXT NOT NULL,
                ad_soyad TEXT DEFAULT '',
                telefon TEXT DEFAULT '',
                avatar_path TEXT DEFAULT '',
                tema TEXT DEFAULT 'dark',
                dil TEXT DEFAULT 'tr',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS seyahatler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_id INTEGER NOT NULL,
                sehir TEXT NOT NULL,
                ulke TEXT DEFAULT '',
                baslangic_tarihi TEXT NOT NULL,
                bitis_tarihi TEXT NOT NULL,
                butce REAL DEFAULT 0,
                seyahat_turu TEXT DEFAULT '',
                notlar TEXT DEFAULT '',
                kapak_foto TEXT DEFAULT '',
                durum TEXT DEFAULT 'planlanıyor',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id)
            );

            CREATE TABLE IF NOT EXISTS konaklamalar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seyahat_id INTEGER NOT NULL,
                otel_adi TEXT NOT NULL,
                konum TEXT DEFAULT '',
                giris_tarihi TEXT DEFAULT '',
                cikis_tarihi TEXT DEFAULT '',
                fiyat REAL DEFAULT 0,
                yildiz INTEGER DEFAULT 3,
                notlar TEXT DEFAULT '',
                FOREIGN KEY (seyahat_id) REFERENCES seyahatler(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS aktiviteler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seyahat_id INTEGER NOT NULL,
                aktivite_adi TEXT NOT NULL,
                tarih TEXT DEFAULT '',
                saat TEXT DEFAULT '',
                konum TEXT DEFAULT '',
                fiyat REAL DEFAULT 0,
                aciklama TEXT DEFAULT '',
                FOREIGN KEY (seyahat_id) REFERENCES seyahatler(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS harcamalar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seyahat_id INTEGER NOT NULL,
                kategori TEXT NOT NULL,
                tutar REAL NOT NULL,
                aciklama TEXT DEFAULT '',
                tarih TEXT DEFAULT '',
                FOREIGN KEY (seyahat_id) REFERENCES seyahatler(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS planlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seyahat_id INTEGER NOT NULL,
                gun TEXT DEFAULT '',
                saat TEXT DEFAULT '',
                baslik TEXT DEFAULT '',
                aciklama TEXT DEFAULT '',
                konum TEXT DEFAULT '',
                kaynak TEXT DEFAULT 'manuel',
                kategori TEXT DEFAULT 'Plan',
                sira INTEGER DEFAULT 0,
                FOREIGN KEY (seyahat_id) REFERENCES seyahatler(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS arkadaslar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seyahat_id INTEGER NOT NULL,
                arkadas_adi TEXT NOT NULL,
                email TEXT DEFAULT '',
                gorevler TEXT DEFAULT '',
                notlar TEXT DEFAULT '',
                FOREIGN KEY (seyahat_id) REFERENCES seyahatler(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS bildirimler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_id INTEGER NOT NULL,
                baslik TEXT NOT NULL,
                mesaj TEXT DEFAULT '',
                tur TEXT DEFAULT 'bilgi',
                okundu INTEGER DEFAULT 0,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id)
            );

            CREATE TABLE IF NOT EXISTS ucuslar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seyahat_id INTEGER NOT NULL,
                havayolu TEXT DEFAULT '',
                ucus_no TEXT DEFAULT '',
                kalkis_yeri TEXT DEFAULT '',
                varis_yeri TEXT DEFAULT '',
                kalkis_zamani TEXT DEFAULT '',
                varis_zamani TEXT DEFAULT '',
                fiyat REAL DEFAULT 0,
                notlar TEXT DEFAULT '',
                FOREIGN KEY (seyahat_id) REFERENCES seyahatler(id) ON DELETE CASCADE
            );
        ''')
        self.conn.commit()

    def migrate_schema(self):
        """Eski veritabanlarını yeni alanlarla uyumlu hale getir"""
        self._ensure_column("planlar", "kaynak", "TEXT DEFAULT 'manuel'")
        self._ensure_column("planlar", "kategori", "TEXT DEFAULT 'Plan'")
        self._ensure_column("planlar", "sira", "INTEGER DEFAULT 0")
        self._ensure_column("planlar", "tarih", "TEXT DEFAULT ''")
        self._ensure_column("planlar", "grup_kodu", "TEXT DEFAULT ''")
        self._ensure_column("aktiviteler", "kaynak", "TEXT DEFAULT 'manuel'")
        self._ensure_column("aktiviteler", "grup_kodu", "TEXT DEFAULT ''")
        self._migrate_plan_tarihleri()
        self._migrate_legacy_ai_planlari()

    def _ensure_column(self, table_name, column_name, definition):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = {row[1] for row in self.cursor.fetchall()}
        if column_name not in columns:
            self.cursor.execute(
                f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}"
            )
            self.conn.commit()

    def create_indexes(self):
        """Sık kullanılan filtre ve sıralamalar için indeksler oluştur"""
        self.cursor.executescript('''
            CREATE INDEX IF NOT EXISTS idx_seyahatler_kullanici_baslangic
            ON seyahatler(kullanici_id, baslangic_tarihi DESC);

            CREATE INDEX IF NOT EXISTS idx_konaklamalar_seyahat
            ON konaklamalar(seyahat_id);

            CREATE INDEX IF NOT EXISTS idx_aktiviteler_seyahat_tarih_saat
            ON aktiviteler(seyahat_id, tarih, saat);

            CREATE INDEX IF NOT EXISTS idx_harcamalar_seyahat_tarih
            ON harcamalar(seyahat_id, tarih DESC);

            CREATE INDEX IF NOT EXISTS idx_planlar_seyahat_tarih_sira_saat
            ON planlar(seyahat_id, tarih, sira, saat);

            CREATE INDEX IF NOT EXISTS idx_planlar_seyahat_kaynak_tarih_sira_saat
            ON planlar(seyahat_id, kaynak, tarih, sira, saat);

            CREATE INDEX IF NOT EXISTS idx_arkadaslar_seyahat
            ON arkadaslar(seyahat_id);

            CREATE INDEX IF NOT EXISTS idx_ucuslar_seyahat
            ON ucuslar(seyahat_id);

            CREATE INDEX IF NOT EXISTS idx_bildirimler_kullanici_okundu_tarih
            ON bildirimler(kullanici_id, okundu, tarih DESC);
        ''')
        self.conn.commit()

    def _coz_plan_tarihi(self, gun_degeri, baslangic_tarihi=""):
        gun_degeri = (gun_degeri or "").strip()
        if not gun_degeri:
            return ""

        try:
            return datetime.strptime(gun_degeri, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            pass

        eslesme = re.search(r"(\d+)", gun_degeri)
        if not eslesme or not baslangic_tarihi:
            return ""

        try:
            baslangic = datetime.strptime(baslangic_tarihi, "%Y-%m-%d")
            return (baslangic + timedelta(days=int(eslesme.group(1)) - 1)).strftime("%Y-%m-%d")
        except ValueError:
            return ""

    def _migrate_plan_tarihleri(self):
        self.cursor.execute('''
            SELECT p.id, p.gun, p.tarih, s.baslangic_tarihi
            FROM planlar p
            JOIN seyahatler s ON s.id = p.seyahat_id
        ''')
        guncellenecekler = []
        for row in self.cursor.fetchall():
            tarih = row["tarih"] or self._coz_plan_tarihi(row["gun"], row["baslangic_tarihi"])
            if tarih and tarih != (row["tarih"] or ""):
                guncellenecekler.append((tarih, row["id"]))

        if guncellenecekler:
            self.cursor.executemany(
                'UPDATE planlar SET tarih=? WHERE id=?',
                guncellenecekler
            )
            self.conn.commit()

    def _eski_ai_plan_mi(self, row):
        if (row["kaynak"] or "manuel") != "manuel":
            return False
        metin = f"{row['gun'] or ''} {row['baslik'] or ''} {row['aciklama'] or ''}".lower()
        ai_izleri = [
            "gün", "ziyareti", "keşfi", "yerel restoranda",
            "öğle", "ogle", "akşam", "aksam", "serbest keşif", "serbest kesif"
        ]
        return ("gün" in metin or "gun" in metin) and any(iz in metin for iz in ai_izleri[1:])

    def _ai_aktivitesi_mi(self, row):
        metin = f"{row['baslik'] or ''} {row['aciklama'] or ''}".lower()
        plan_kelimeleri = [
            "öğle", "ogle", "akşam", "aksam", "kahvaltı", "kahvalti",
            "restoran", "ulaşım", "ulasim", "serbest zaman", "check-in", "check out"
        ]
        if any(kelime in metin for kelime in plan_kelimeleri):
            return False
        return any(kelime in metin for kelime in ["ziyareti", "keşfi", "kesfi"])

    def _temiz_plan_basligi(self, baslik):
        return re.sub(r"^[^\w\d]+", "", baslik or "").strip()

    def _migrate_legacy_ai_planlari(self):
        self.cursor.execute('''
            SELECT p.*, s.baslangic_tarihi
            FROM planlar p
            JOIN seyahatler s ON s.id = p.seyahat_id
            ORDER BY p.id
        ''')
        degisti = False
        for row in self.cursor.fetchall():
            if not self._eski_ai_plan_mi(row):
                continue

            tarih = row["tarih"] or self._coz_plan_tarihi(row["gun"], row["baslangic_tarihi"])
            grup_kodu = row["grup_kodu"] or f"legacy-ai-{row['id']}"

            if self._ai_aktivitesi_mi(row):
                aktivite_adi = self._temiz_plan_basligi(row["baslik"])
                self.cursor.execute('''
                    SELECT id FROM aktiviteler
                    WHERE seyahat_id=? AND aktivite_adi=? AND tarih=? AND saat=?
                ''', (
                    row["seyahat_id"],
                    aktivite_adi,
                    tarih,
                    row["saat"] or ""
                ))
                if not self.cursor.fetchone():
                    self.cursor.execute('''
                        INSERT INTO aktiviteler
                        (seyahat_id, aktivite_adi, tarih, saat, konum, fiyat, aciklama, kaynak, grup_kodu)
                        VALUES (?,?,?,?,?,?,?,?,?)
                    ''', (
                        row["seyahat_id"],
                        aktivite_adi,
                        tarih,
                        row["saat"] or "",
                        row["konum"] or "",
                        0,
                        row["aciklama"] or "",
                        "ai",
                        grup_kodu
                    ))
                self.cursor.execute('DELETE FROM planlar WHERE id=?', (row["id"],))
                degisti = True
                continue

            self.cursor.execute('''
                UPDATE planlar
                SET tarih=?, kaynak='ai', kategori='Yemek', grup_kodu=?
                WHERE id=?
            ''', (tarih, grup_kodu, row["id"]))
            degisti = True

        if degisti:
            self.conn.commit()

    # ─── Kullanıcı İşlemleri ───────────────────────────────────────

    def kullanici_ekle(self, kullanici_adi, email, sifre, ad_soyad=""):
        """Yeni kullanıcı kaydet"""
        try:
            self.cursor.execute(
                'INSERT INTO kullanicilar (kullanici_adi, email, sifre, ad_soyad, tema) VALUES (?,?,?,?,?)',
                (kullanici_adi, email, sifre, ad_soyad, "dark"))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def kullanici_giris(self, kullanici_adi, sifre):
        """Kullanıcı girişi doğrula"""
        self.cursor.execute(
            'SELECT * FROM kullanicilar WHERE kullanici_adi=? AND sifre=?',
            (kullanici_adi, sifre))
        return self._dict_or_none(self.cursor.fetchone())

    def kullanici_getir(self, kullanici_id):
        """ID ile kullanıcı getir"""
        self.cursor.execute('SELECT * FROM kullanicilar WHERE id=?', (kullanici_id,))
        return self._dict_or_none(self.cursor.fetchone())

    def kullanici_guncelle(self, kullanici_id, **kwargs):
        """Kullanıcı bilgilerini güncelle"""
        for key, value in kwargs.items():
            self.cursor.execute(
                f'UPDATE kullanicilar SET {key}=? WHERE id=?', (value, kullanici_id))
        self.conn.commit()

    # ─── Seyahat İşlemleri ─────────────────────────────────────────

    def demo_verilerini_hazirla(self):
        """Demo hesabi ve ornek seyahatleri idempotent olarak hazirla."""
        sifre_hash = hashlib.sha256(self.DEMO_PASSWORD.encode()).hexdigest()

        self.cursor.execute(
            'SELECT id FROM kullanicilar WHERE kullanici_adi=?',
            (self.DEMO_USERNAME,)
        )
        row = self.cursor.fetchone()

        if row:
            kullanici_id = row["id"]
            self.cursor.execute(
                'UPDATE kullanicilar SET sifre=?, ad_soyad=? WHERE id=?',
                (sifre_hash, "Demo Kullanici", kullanici_id)
            )
            self.conn.commit()
        else:
            try:
                self.cursor.execute(
                    '''
                    INSERT INTO kullanicilar (kullanici_adi, email, sifre, ad_soyad, tema)
                    VALUES (?,?,?,?,?)
                    ''',
                    (self.DEMO_USERNAME, self.DEMO_EMAIL, sifre_hash, "Demo Kullanici", "dark")
                )
                self.conn.commit()
                kullanici_id = self.cursor.lastrowid
            except sqlite3.IntegrityError:
                self.conn.rollback()
                self.cursor.execute(
                    'SELECT id FROM kullanicilar WHERE email=?',
                    (self.DEMO_EMAIL,)
                )
                row = self.cursor.fetchone()
                if not row:
                    return None
                kullanici_id = row["id"]
                self.cursor.execute(
                    'UPDATE kullanicilar SET kullanici_adi=?, sifre=?, ad_soyad=? WHERE id=?',
                    (self.DEMO_USERNAME, sifre_hash, "Demo Kullanici", kullanici_id)
                )
                self.conn.commit()

        self._demo_seyahatleri_ekle(kullanici_id)
        return kullanici_id

    def _demo_seyahatleri_ekle(self, kullanici_id):
        self.cursor.execute(
            'SELECT COUNT(*) FROM seyahatler WHERE kullanici_id=?',
            (kullanici_id,)
        )
        if self.cursor.fetchone()[0] > 0:
            return

        bugun = datetime.now().date()

        def tarih(gun):
            return gun.strftime("%Y-%m-%d")

        ist_bas = bugun - timedelta(days=1)
        ist_bit = bugun + timedelta(days=2)
        istanbul_id = self.seyahat_ekle(
            kullanici_id, "Istanbul", "Turkiye", tarih(ist_bas), tarih(ist_bit),
            45000, "Kultur", "Demo aktif seyahat. Plan, harcama ve konaklama ornekleri icerir."
        )
        self.konaklama_ekle(
            istanbul_id, "Galata Demo Hotel", "Beyoglu", tarih(ist_bas), tarih(ist_bit),
            18000, 4, "Demo konaklama"
        )
        self.ucus_ekle(
            istanbul_id, "THY", "TK2026", "Ankara", "Istanbul",
            f"{tarih(ist_bas)} 09:15", f"{tarih(ist_bas)} 10:25", 3200
        )
        self.plan_ekle(
            istanbul_id, "Gun 1", "10:30", "Galata ve Karakoy turu",
            "Galata Kulesi, ara sokaklar ve sahil yuruyusu.", "Karakoy",
            "manuel", "Plan", 1, tarih(ist_bas)
        )
        self.plan_ekle(
            istanbul_id, "Gun 2", "19:00", "Bogazda aksam yemegi",
            "Demo butce takibi icin restoran plani.", "Besiktas",
            "manuel", "Yemek", 2, tarih(bugun)
        )
        self.aktivite_ekle(
            istanbul_id, "Topkapi Sarayi ziyareti", tarih(bugun), "11:00",
            "Sultanahmet", 950, "Muze ve tarihi yarimada gezisi"
        )
        self.harcama_ekle(istanbul_id, "Konaklama", 18000, "Galata Demo Hotel", tarih(ist_bas))
        self.harcama_ekle(istanbul_id, "Yemek", 1450, "Karakoy kahvalti", tarih(bugun))
        self.arkadas_ekle(istanbul_id, "Ayse Demo", "ayse.demo@example.com", "Muze biletleri", "Demo arkadas kaydi")

        kap_bas = bugun + timedelta(days=16)
        kap_bit = kap_bas + timedelta(days=3)
        kapadokya_id = self.seyahat_ekle(
            kullanici_id, "Kapadokya", "Turkiye", tarih(kap_bas), tarih(kap_bit),
            52000, "Macera", "Demo yaklasan seyahat. Harita ve takvim ekraninda gorunur."
        )
        self.konaklama_ekle(
            kapadokya_id, "Cave Demo Suites", "Goreme", tarih(kap_bas), tarih(kap_bit),
            22000, 5, "Demo konaklama"
        )
        self.plan_ekle(
            kapadokya_id, "Gun 1", "05:30", "Balon seyri",
            "Gun dogumunda balonlari izleme.", "Goreme",
            "manuel", "Aktivite", 1, tarih(kap_bas)
        )
        self.plan_ekle(
            kapadokya_id, "Gun 2", "14:00", "Yer alti sehri gezisi",
            "Derinkuyu rotasi ve fotograf molalari.", "Derinkuyu",
            "manuel", "Plan", 2, tarih(kap_bas + timedelta(days=1))
        )
        self.aktivite_ekle(
            kapadokya_id, "ATV vadi turu", tarih(kap_bas + timedelta(days=1)), "17:00",
            "Goreme", 1800, "Kizil vadi demo aktivitesi"
        )
        self.harcama_ekle(kapadokya_id, "Aktivite", 1800, "ATV on odeme", tarih(kap_bas))
        self.arkadas_ekle(kapadokya_id, "Mehmet Demo", "mehmet.demo@example.com", "Arac kiralama", "")

        par_bas = bugun - timedelta(days=45)
        par_bit = par_bas + timedelta(days=5)
        paris_id = self.seyahat_ekle(
            kullanici_id, "Paris", "Fransa", tarih(par_bas), tarih(par_bit),
            88000, "Romantik", "Demo tamamlanan seyahat. Gecmis seyahat filtreleri icin eklendi."
        )
        self.konaklama_ekle(
            paris_id, "Seine Demo Hotel", "Latin Quarter", tarih(par_bas), tarih(par_bit),
            36000, 4, "Demo konaklama"
        )
        self.ucus_ekle(
            paris_id, "Air France", "AF1391", "Istanbul", "Paris",
            f"{tarih(par_bas)} 12:40", f"{tarih(par_bas)} 15:25", 9800
        )
        self.plan_ekle(
            paris_id, "Gun 1", "16:30", "Seine nehri yuruyusu",
            "Otel check-in sonrasi kisa rota.", "Seine",
            "manuel", "Plan", 1, tarih(par_bas)
        )
        self.aktivite_ekle(
            paris_id, "Louvre Muzesi", tarih(par_bas + timedelta(days=2)), "10:00",
            "Louvre", 1200, "Onceden alinmis demo bilet"
        )
        self.harcama_ekle(paris_id, "Ulasim", 9800, "Gidis ucagi", tarih(par_bas))
        self.harcama_ekle(paris_id, "Muze", 1200, "Louvre bileti", tarih(par_bas + timedelta(days=2)))

    def seyahat_ekle(self, kullanici_id, sehir, ulke, baslangic, bitis,
                     butce=0, tur="", notlar="", kapak=""):
        """Yeni seyahat oluştur"""
        self.cursor.execute('''
            INSERT INTO seyahatler
            (kullanici_id, sehir, ulke, baslangic_tarihi, bitis_tarihi, butce, seyahat_turu, notlar, kapak_foto)
            VALUES (?,?,?,?,?,?,?,?,?)
        ''', (kullanici_id, sehir, ulke, baslangic, bitis, butce, tur, notlar, kapak))
        self.conn.commit()
        sid = self.cursor.lastrowid
        self.bildirim_ekle(kullanici_id, "Yeni Seyahat ✈️",
                           f"{sehir} seyahati başarıyla oluşturuldu!", "seyahat")
        return sid

    def seyahatleri_getir(self, kullanici_id):
        """Kullanıcının tüm seyahatlerini getir"""
        self.cursor.execute(
            'SELECT * FROM seyahatler WHERE kullanici_id=? ORDER BY baslangic_tarihi DESC',
            (kullanici_id,))
        return self._list_dicts(self.cursor.fetchall())

    def seyahat_getir(self, seyahat_id):
        """Tekil seyahat getir"""
        self.cursor.execute('SELECT * FROM seyahatler WHERE id=?', (seyahat_id,))
        return self._dict_or_none(self.cursor.fetchone())

    def seyahat_guncelle(self, seyahat_id, **kwargs):
        """Seyahat bilgilerini güncelle"""
        for key, value in kwargs.items():
            self.cursor.execute(
                f'UPDATE seyahatler SET {key}=? WHERE id=?', (value, seyahat_id))
        self.conn.commit()

    def seyahat_sil(self, seyahat_id):
        """Seyahati sil"""
        self.cursor.execute('DELETE FROM seyahatler WHERE id=?', (seyahat_id,))
        self.conn.commit()

    def seyahat_ara(self, kullanici_id, arama):
        """Seyahatlerde arama"""
        like = f'%{arama}%'
        self.cursor.execute('''
            SELECT * FROM seyahatler
            WHERE kullanici_id=? AND (sehir LIKE ? OR ulke LIKE ? OR notlar LIKE ?)
        ''', (kullanici_id, like, like, like))
        return self._list_dicts(self.cursor.fetchall())

    # ─── Konaklama İşlemleri ───────────────────────────────────────

    def konaklama_ekle(self, seyahat_id, otel_adi, konum="", giris="",
                       cikis="", fiyat=0, yildiz=3, notlar=""):
        self.cursor.execute('''
            INSERT INTO konaklamalar
            (seyahat_id, otel_adi, konum, giris_tarihi, cikis_tarihi, fiyat, yildiz, notlar)
            VALUES (?,?,?,?,?,?,?,?)
        ''', (seyahat_id, otel_adi, konum, giris, cikis, fiyat, yildiz, notlar))
        self.conn.commit()
        return self.cursor.lastrowid

    def konaklamalari_getir(self, seyahat_id):
        self.cursor.execute(
            'SELECT * FROM konaklamalar WHERE seyahat_id=?', (seyahat_id,))
        return self._list_dicts(self.cursor.fetchall())

    def konaklama_sil(self, konaklama_id):
        self.cursor.execute('DELETE FROM konaklamalar WHERE id=?', (konaklama_id,))
        self.conn.commit()

    def konaklama_guncelle(self, konaklama_id, **kwargs):
        for key, value in kwargs.items():
            self.cursor.execute(
                f'UPDATE konaklamalar SET {key}=? WHERE id=?', (value, konaklama_id))
        self.conn.commit()

    # ─── Aktivite İşlemleri ────────────────────────────────────────

    def aktivite_ekle(self, seyahat_id, aktivite_adi, tarih="", saat="",
                      konum="", fiyat=0, aciklama="", kaynak="manuel", grup_kodu=""):
        self.cursor.execute('''
            INSERT INTO aktiviteler
            (seyahat_id, aktivite_adi, tarih, saat, konum, fiyat, aciklama, kaynak, grup_kodu)
            VALUES (?,?,?,?,?,?,?,?,?)
        ''', (seyahat_id, aktivite_adi, tarih, saat, konum, fiyat, aciklama, kaynak, grup_kodu))
        self.conn.commit()
        return self.cursor.lastrowid

    def aktiviteleri_getir(self, seyahat_id):
        self.cursor.execute(
            '''
            SELECT * FROM aktiviteler
            WHERE seyahat_id=?
            ORDER BY
                COALESCE(NULLIF(tarih, ''), '9999-12-31'),
                COALESCE(NULLIF(saat, ''), '23:59'),
                id
            ''',
            (seyahat_id,))
        return self._list_dicts(self.cursor.fetchall())

    def aktiviteleri_toplu_getir(self, seyahat_idleri):
        if not seyahat_idleri:
            return []
        placeholders = self._placeholders(seyahat_idleri)
        self.cursor.execute(f'''
            SELECT * FROM aktiviteler
            WHERE seyahat_id IN ({placeholders})
            ORDER BY
                seyahat_id,
                COALESCE(NULLIF(tarih, ''), '9999-12-31'),
                COALESCE(NULLIF(saat, ''), '23:59'),
                id
        ''', tuple(seyahat_idleri))
        return self._list_dicts(self.cursor.fetchall())

    def aktivite_sil(self, aktivite_id):
        self.cursor.execute('DELETE FROM aktiviteler WHERE id=?', (aktivite_id,))
        self.conn.commit()

    def aktivite_guncelle(self, aktivite_id, **kwargs):
        for key, value in kwargs.items():
            self.cursor.execute(
                f'UPDATE aktiviteler SET {key}=? WHERE id=?', (value, aktivite_id))
        self.conn.commit()

    # ─── Harcama İşlemleri ─────────────────────────────────────────

    def harcama_ekle(self, seyahat_id, kategori, tutar, aciklama="", tarih=""):
        if not tarih:
            tarih = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute('''
            INSERT INTO harcamalar (seyahat_id, kategori, tutar, aciklama, tarih)
            VALUES (?,?,?,?,?)
        ''', (seyahat_id, kategori, tutar, aciklama, tarih))
        self.conn.commit()
        return self.cursor.lastrowid

    def harcamalari_getir(self, seyahat_id):
        self.cursor.execute(
            'SELECT * FROM harcamalar WHERE seyahat_id=? ORDER BY tarih DESC',
            (seyahat_id,))
        return self._list_dicts(self.cursor.fetchall())

    def harcama_sil(self, harcama_id):
        self.cursor.execute('DELETE FROM harcamalar WHERE id=?', (harcama_id,))
        self.conn.commit()

    def harcama_toplam(self, seyahat_id):
        self.cursor.execute(
            'SELECT COALESCE(SUM(tutar),0) FROM harcamalar WHERE seyahat_id=?',
            (seyahat_id,))
        return self.cursor.fetchone()[0]

    def harcama_kategori_toplam(self, seyahat_id):
        self.cursor.execute('''
            SELECT kategori, SUM(tutar) as toplam FROM harcamalar
            WHERE seyahat_id=? GROUP BY kategori ORDER BY toplam DESC
        ''', (seyahat_id,))
        return self._list_dicts(self.cursor.fetchall())

    # ─── Plan İşlemleri ────────────────────────────────────────────

    def plan_ekle(self, seyahat_id, gun, saat, baslik, aciklama="", konum="",
                  kaynak="manuel", kategori="Plan", sira=0, tarih="", grup_kodu=""):
        plan_tarihi = tarih or self._coz_plan_tarihi(gun)
        self.cursor.execute('''
            INSERT INTO planlar
            (seyahat_id, gun, saat, baslik, aciklama, konum, kaynak, kategori, sira, tarih, grup_kodu)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            seyahat_id, gun, saat, baslik, aciklama, konum,
            kaynak, kategori, sira, plan_tarihi, grup_kodu
        ))
        self.conn.commit()
        return self.cursor.lastrowid

    def planlari_getir(self, seyahat_id, kaynak=None):
        if kaynak:
            self.cursor.execute(
                '''
                SELECT * FROM planlar
                WHERE seyahat_id=? AND kaynak=?
                ORDER BY
                    COALESCE(NULLIF(tarih, ''), NULLIF(gun, ''), '9999-12-31'),
                    sira,
                    COALESCE(NULLIF(saat, ''), '23:59'),
                    id
                ''',
                (seyahat_id, kaynak))
        else:
            self.cursor.execute(
                '''
                SELECT * FROM planlar
                WHERE seyahat_id=?
                ORDER BY
                    COALESCE(NULLIF(tarih, ''), NULLIF(gun, ''), '9999-12-31'),
                    sira,
                    COALESCE(NULLIF(saat, ''), '23:59'),
                    id
                ''',
                (seyahat_id,))
        return self._list_dicts(self.cursor.fetchall())

    def planlari_toplu_getir(self, seyahat_idleri):
        if not seyahat_idleri:
            return []
        placeholders = self._placeholders(seyahat_idleri)
        self.cursor.execute(f'''
            SELECT * FROM planlar
            WHERE seyahat_id IN ({placeholders})
            ORDER BY
                seyahat_id,
                COALESCE(NULLIF(tarih, ''), NULLIF(gun, ''), '9999-12-31'),
                sira,
                COALESCE(NULLIF(saat, ''), '23:59'),
                id
        ''', tuple(seyahat_idleri))
        return self._list_dicts(self.cursor.fetchall())

    def plan_sil(self, plan_id):
        self.cursor.execute('DELETE FROM planlar WHERE id=?', (plan_id,))
        self.conn.commit()

    def planlari_temizle(self, seyahat_id, kaynak=None):
        if kaynak:
            self.cursor.execute(
                'DELETE FROM planlar WHERE seyahat_id=? AND kaynak=?',
                (seyahat_id, kaynak))
        else:
            self.cursor.execute('DELETE FROM planlar WHERE seyahat_id=?', (seyahat_id,))
        self.conn.commit()

    def ai_kayitlarini_temizle(self, seyahat_id):
        self.cursor.execute(
            "DELETE FROM planlar WHERE seyahat_id=? AND kaynak='ai'",
            (seyahat_id,)
        )
        self.cursor.execute(
            "DELETE FROM aktiviteler WHERE seyahat_id=? AND kaynak='ai'",
            (seyahat_id,)
        )
        self.cursor.execute(
            "DELETE FROM konaklamalar WHERE seyahat_id=? AND notlar='AI önerisi'",
            (seyahat_id,)
        )
        self.conn.commit()

    # ─── Arkadaş İşlemleri ────────────────────────────────────────

    def arkadas_ekle(self, seyahat_id, arkadas_adi, email="", gorevler="", notlar=""):
        self.cursor.execute('''
            INSERT INTO arkadaslar (seyahat_id, arkadas_adi, email, gorevler, notlar)
            VALUES (?,?,?,?,?)
        ''', (seyahat_id, arkadas_adi, email, gorevler, notlar))
        self.conn.commit()
        return self.cursor.lastrowid

    def arkadaslari_getir(self, seyahat_id):
        self.cursor.execute(
            'SELECT * FROM arkadaslar WHERE seyahat_id=?', (seyahat_id,))
        return self._list_dicts(self.cursor.fetchall())

    def arkadas_sil(self, arkadas_id):
        self.cursor.execute('DELETE FROM arkadaslar WHERE id=?', (arkadas_id,))
        self.conn.commit()

    def arkadas_guncelle(self, arkadas_id, **kwargs):
        for key, value in kwargs.items():
            self.cursor.execute(
                f'UPDATE arkadaslar SET {key}=? WHERE id=?', (value, arkadas_id))
        self.conn.commit()

    # ─── Bildirim İşlemleri ────────────────────────────────────────

    def bildirim_ekle(self, kullanici_id, baslik, mesaj, tur="bilgi"):
        self.cursor.execute('''
            INSERT INTO bildirimler (kullanici_id, baslik, mesaj, tur)
            VALUES (?,?,?,?)
        ''', (kullanici_id, baslik, mesaj, tur))
        self.conn.commit()

    def bildirimleri_getir(self, kullanici_id):
        self.cursor.execute('''
            SELECT * FROM bildirimler WHERE kullanici_id=?
            ORDER BY tarih DESC LIMIT 50
        ''', (kullanici_id,))
        return self._list_dicts(self.cursor.fetchall())

    def okunmamis_bildirimler(self, kullanici_id):
        self.cursor.execute(
            'SELECT COUNT(*) FROM bildirimler WHERE kullanici_id=? AND okundu=0',
            (kullanici_id,))
        return self.cursor.fetchone()[0]

    def bildirim_okundu(self, bildirim_id):
        self.cursor.execute(
            'UPDATE bildirimler SET okundu=1 WHERE id=?', (bildirim_id,))
        self.conn.commit()

    def tum_bildirimleri_oku(self, kullanici_id):
        self.cursor.execute(
            'UPDATE bildirimler SET okundu=1 WHERE kullanici_id=?', (kullanici_id,))
        self.conn.commit()

    # ─── Uçuş İşlemleri ───────────────────────────────────────────

    def ucus_ekle(self, seyahat_id, havayolu, ucus_no, kalkis_yeri,
                  varis_yeri, kalkis_zamani, varis_zamani, fiyat=0, notlar=""):
        self.cursor.execute('''
            INSERT INTO ucuslar
            (seyahat_id, havayolu, ucus_no, kalkis_yeri, varis_yeri,
             kalkis_zamani, varis_zamani, fiyat, notlar)
            VALUES (?,?,?,?,?,?,?,?,?)
        ''', (seyahat_id, havayolu, ucus_no, kalkis_yeri, varis_yeri,
              kalkis_zamani, varis_zamani, fiyat, notlar))
        self.conn.commit()
        return self.cursor.lastrowid

    def ucuslari_getir(self, seyahat_id):
        self.cursor.execute(
            'SELECT * FROM ucuslar WHERE seyahat_id=?', (seyahat_id,))
        return self._list_dicts(self.cursor.fetchall())

    def ucus_sil(self, ucus_id):
        self.cursor.execute('DELETE FROM ucuslar WHERE id=?', (ucus_id,))
        self.conn.commit()

    # ─── Bağlantı Yönetimi ────────────────────────────────────────

    def kapat(self):
        """Veritabanı bağlantısını kapat"""
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.kapat()
