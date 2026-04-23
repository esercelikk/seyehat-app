"""
Seyahat Planlama Uygulaması - Arayüz Modülü (PyQt5)
=====================================================
Modern, profesyonel kullanıcı arayüzü - Premium Obsidian Tema
"""

import sys, os, math, random, tempfile
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QFrame, QScrollArea,
    QStackedWidget, QTabWidget, QComboBox, QSpinBox, QDoubleSpinBox,
    QDateEdit, QFileDialog, QMessageBox, QGraphicsDropShadowEffect,
    QSizePolicy, QGridLayout, QDialog, QTimeEdit, QCalendarWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QProgressBar, QCheckBox
)
from PyQt5.QtCore import (
    Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer,
    QDate, QTime, QRect, QRectF, QPoint, QPointF, QUrl, pyqtSignal
)
from PyQt5.QtGui import (
    QFont, QColor, QPainter, QPen, QBrush, QLinearGradient,
    QRadialGradient, QPainterPath, QPixmap, QIcon, QFontDatabase,
    QPalette, QConicalGradient, QTextCharFormat, QDesktopServices
)

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    HAS_WEBENGINE = True
except ImportError:
    HAS_WEBENGINE = False


# ═══════════════════════════════════════════════════════════════════
#  TEMA — Premium Obsidian
# ═══════════════════════════════════════════════════════════════════

class T:
    """Renk paleti — sakin, modern ve daha nötr bir premium tema"""
    BG        = "#0a0f1a"
    BG2       = "#141b2d"
    BG3       = "#1c2540"
    CARD      = "#151d31"
    CARD_H    = "#1d2740"
    SIDEBAR   = "#0d1324"

    PRIMARY   = "#6f8cff"
    PRIMARY_L = "#97aafc"
    PRIMARY_D = "#4d69da"
    G1        = "#6f8cff"
    G2        = "#5bb7d6"

    CYAN      = "#69c4d4"
    EMERALD   = "#68b79e"
    AMBER     = "#d7b16f"
    ROSE      = "#c98e98"
    ORANGE    = "#d59b6d"
    PINK      = "#b79ac9"
    SKY       = "#76a8dd"
    LIME      = "#a5c185"
    INDIGO    = "#90a1e6"

    TEXT      = "#eef2f7"
    TEXT2     = "#a8b3c8"
    TEXT3     = "#5f6b86"

    KAT = {
        "Yemek": "#d7b16f", "Ulaşım": "#76a8dd", "Eğlence": "#90a1e6",
        "Alışveriş": "#68b79e", "Konaklama": "#97aafc", "Aktivite": "#69c4d4",
        "Diğer": "#71717a", "Müze": "#fb923c"
    }
    DURUM = {"yaklaşan": "#38bdf8", "aktif": "#34d399", "tamamlanan": "#52525b", "belirsiz": "#3f3f46"}
    GRAD = [
        ("#6f8cff", "#5bb7d6"), ("#68b79e", "#69c4d4"), ("#76a8dd", "#90a1e6"),
        ("#d7b16f", "#d59b6d"), ("#7b8eb8", "#5f789c"), ("#8aa39a", "#7faeb3"),
        ("#6f8cff", "#68b79e"), ("#90a1e6", "#69c4d4"), ("#7c8fb3", "#a5c185"),
        ("#7697c2", "#8fb7af"),
    ]
    AKTIF = "dark"


THEME_PRESETS = {
    "dark": {
        "BG": "#0a0f1a", "BG2": "#141b2d", "BG3": "#1c2540", "CARD": "#151d31",
        "CARD_H": "#1d2740", "SIDEBAR": "#0d1324", "PRIMARY": "#6f8cff",
        "PRIMARY_L": "#97aafc", "PRIMARY_D": "#4d69da", "G1": "#6f8cff",
        "G2": "#5bb7d6", "CYAN": "#69c4d4", "EMERALD": "#68b79e",
        "AMBER": "#d7b16f", "ROSE": "#c98e98", "ORANGE": "#d59b6d",
        "PINK": "#b79ac9", "SKY": "#76a8dd", "LIME": "#a5c185",
        "INDIGO": "#90a1e6", "TEXT": "#eef2f7", "TEXT2": "#a8b3c8", "TEXT3": "#5f6b86",
        "GRAD": [
            ("#6f8cff", "#5bb7d6"), ("#68b79e", "#69c4d4"), ("#76a8dd", "#90a1e6"),
            ("#d7b16f", "#d59b6d"), ("#7b8eb8", "#5f789c"), ("#8aa39a", "#7faeb3"),
            ("#6f8cff", "#68b79e"), ("#90a1e6", "#69c4d4"), ("#7c8fb3", "#a5c185"),
            ("#7697c2", "#8fb7af"),
        ],
    },
    "light": {
        "BG": "#f6f1ea", "BG2": "#fffbf6", "BG3": "#ebe4da", "CARD": "#fffdf9",
        "CARD_H": "#f5eee5", "SIDEBAR": "#efe7dc", "PRIMARY": "#7894b4",
        "PRIMARY_L": "#9bb4cf", "PRIMARY_D": "#5f7898", "G1": "#8eabc8",
        "G2": "#a8c2b0", "CYAN": "#7fb4be", "EMERALD": "#94b69f",
        "AMBER": "#c9a876", "ROSE": "#c8a09a", "ORANGE": "#d1a781",
        "PINK": "#b8a5bf", "SKY": "#9bb9d7", "LIME": "#acc09a",
        "INDIGO": "#9caad0", "TEXT": "#495360", "TEXT2": "#77808b", "TEXT3": "#b2b8bd",
        "GRAD": [
            ("#8eabc8", "#a8c2b0"), ("#9bb9d7", "#9caad0"), ("#94b69f", "#7fb4be"),
            ("#c9a876", "#d1a781"), ("#a5b1bf", "#94b69f"), ("#b2becd", "#9bb9d7"),
            ("#8eabc8", "#94b69f"), ("#9caad0", "#7fb4be"), ("#acc09a", "#a5b1bf"),
            ("#adc0d7", "#bfd0c3"),
        ],
    },
}


def tema_paleti_uygula(tema):
    palet = THEME_PRESETS["light" if tema == "light" else "dark"]
    for anahtar, deger in palet.items():
        setattr(T, anahtar, deger)
    T.AKTIF = "light" if tema == "light" else "dark"


def shadow(w, blur=24, ox=0, oy=6, color=QColor(0, 0, 0, 100)):
    fx = QGraphicsDropShadowEffect()
    fx.setBlurRadius(blur)
    fx.setOffset(ox, oy)
    fx.setColor(color)
    w.setGraphicsEffect(fx)
    return fx


def dairesel_avatar_pixmap(image_path, size, dolgu_orani=0.82):
    if not image_path or not os.path.exists(image_path):
        return QPixmap()

    kaynak = QPixmap(image_path)
    if kaynak.isNull():
        return QPixmap()

    canvas = QPixmap(size, size)
    canvas.fill(Qt.transparent)

    painter = QPainter(canvas)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)

    arka_plan = QLinearGradient(0, 0, size, size)
    arka_plan.setColorAt(0, QColor(T.BG2))
    arka_plan.setColorAt(1, QColor(T.BG3))

    daire = QPainterPath()
    daire.addEllipse(0, 0, size, size)
    painter.fillPath(daire, arka_plan)
    painter.setClipPath(daire)

    hedef_boyut = max(8, int(size * dolgu_orani))
    olcekli = kaynak.scaled(
        hedef_boyut,
        hedef_boyut,
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation
    )
    x = int((size - olcekli.width()) / 2)
    y = int((size - olcekli.height()) / 2)
    painter.drawPixmap(x, y, olcekli)

    painter.setClipping(False)
    painter.end()
    return canvas


def avatar_label_uygula(lbl, image_path, size, yazi="👤", yazi_boyutu=36):
    pix = dairesel_avatar_pixmap(image_path, size)
    if not pix.isNull():
        lbl.clear()
        lbl.setPixmap(pix)
        lbl.setScaledContents(False)
        lbl.setStyleSheet("background:transparent;border:none;")
        return

    lbl.setPixmap(QPixmap())
    lbl.setText(yazi)
    lbl.setScaledContents(False)
    lbl.setStyleSheet(
        f"background:qlineargradient(x1:0,y1:0,x2:1,y2:1,"
        f"stop:0 {T.G1},stop:1 {T.G2});"
        f"border:none;border-radius:{size // 2}px;font-size:{yazi_boyutu}px;"
    )


# ═══════════════════════════════════════════════════════════════════
#  GLOBAL QSS — Sınırsız, Temiz
# ═══════════════════════════════════════════════════════════════════

LIGHT_QSS = """
* { font-family: 'Segoe UI', Arial; }
QMainWindow, QWidget { background: #f6f1ea; color: #495360; }
QScrollArea { border: none; background: transparent; }
QScrollBar:vertical { background: transparent; width: 5px; }
QScrollBar::handle:vertical { background: rgba(120,148,180,0.20); border-radius: 2px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: rgba(120,148,180,0.32); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; height: 0; }
QScrollBar:horizontal { background: transparent; height: 5px; }
QScrollBar::handle:horizontal { background: rgba(120,148,180,0.20); border-radius: 2px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit {
    background: #fffbf6; border: none; border-radius: 12px;
    padding: 11px 16px; color: #495360; font-size: 13px;
    selection-background-color: #9bb4cf;
}
QLineEdit:focus, QTextEdit:focus { background: #f2f6f3; }
QComboBox::drop-down { border: none; width: 30px; }
QComboBox::down-arrow { image: none; }
QComboBox QAbstractItemView {
    background: #fffbf6; border: none; border-radius: 8px;
    selection-background-color: rgba(155,180,207,0.20); color: #495360; padding: 4px;
}
QTabWidget::pane { border: none; }
QTabBar::tab {
    background: transparent; color: #98a1a9; padding: 10px 18px;
    font-size: 13px; font-weight: 600; border: none; border-radius: 12px;
    margin-right: 4px;
}
QTabBar::tab:selected { color: #5f7898; background: #e8eef2; }
QTabBar::tab:hover { color: #495360; background: #f1f3ef; }
QTableWidget {
    background: #fffbf6; border: none; border-radius: 12px;
    gridline-color: transparent; color: #495360; font-size: 13px;
    selection-background-color: rgba(155,180,207,0.14);
}
QTableWidget::item { padding: 8px; border: none; }
QHeaderView::section {
    background: #f2ece5; color: #77808b; font-weight: 600;
    padding: 10px 8px; border: none;
}
QCalendarWidget { background: #fffbf6; border: none; border-radius: 14px; }
QCalendarWidget QWidget { background: transparent; color: #495360; }
QCalendarWidget QToolButton {
    color: #495360; background: transparent; border-radius: 8px; padding: 8px;
    font-size: 14px; font-weight: 700;
}
QCalendarWidget QToolButton:hover { background: rgba(155,180,207,0.16); }
QCalendarWidget QAbstractItemView {
    selection-background-color: #9bb4cf; selection-color: white;
    font-size: 13px; outline: none;
}
QCalendarWidget QAbstractItemView::item { border-radius: 6px; padding: 4px; }
QProgressBar {
    background: #e5e1d8; border: none; border-radius: 6px; height: 10px; color: transparent;
}
QProgressBar::chunk {
    border-radius: 6px;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #8eabc8,stop:1 #a8c2b0);
}
QToolTip {
    background: #fffbf6; color: #495360; border: none;
    border-radius: 8px; padding: 8px 12px; font-size: 12px;
}
QMessageBox { background: #fffbf6; }
QMessageBox QLabel { color: #495360; font-size: 13px; }
QMessageBox QPushButton {
    background: #7894b4; color: white; border: none; border-radius: 10px;
    padding: 10px 28px; font-weight: 600; min-width: 80px;
}
QDialog { background: #f6f1ea; }
QFrame { border: none; }
"""

DARK_QSS = f"""
* {{ font-family: 'Segoe UI', Arial; }}
QMainWindow, QWidget {{ background: {T.BG}; color: {T.TEXT}; }}
QScrollArea {{ border: none; background: transparent; }}

/* Scrollbar */
QScrollBar:vertical {{ background: transparent; width: 5px; }}
QScrollBar::handle:vertical {{
    background: rgba(255,255,255,0.10); border-radius: 2px; min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{ background: rgba(255,255,255,0.20); }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; height: 0; }}
QScrollBar:horizontal {{ background: transparent; height: 5px; }}
QScrollBar::handle:horizontal {{ background: rgba(255,255,255,0.10); border-radius: 2px; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}

/* Inputs */
QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit {{
    background: {T.BG2}; border: none; border-radius: 12px;
    padding: 11px 16px; color: {T.TEXT}; font-size: 13px;
    selection-background-color: {T.PRIMARY};
}}
QLineEdit:focus, QTextEdit:focus {{ background: {T.BG3}; }}
QComboBox::drop-down {{ border: none; width: 30px; }}
QComboBox::down-arrow {{ image: none; }}
QComboBox QAbstractItemView {{
    background: {T.BG2}; border: none; border-radius: 8px;
    selection-background-color: rgba(139,92,246,0.25); color: {T.TEXT}; padding: 4px;
}}

/* Tabs */
QTabWidget::pane {{ border: none; }}
QTabBar::tab {{
    background: transparent; color: {T.TEXT2}; padding: 10px 18px;
    font-size: 13px; font-weight: 600; border: none; border-radius: 12px;
    margin-right: 4px;
}}
QTabBar::tab:selected {{ color: {T.PRIMARY_L}; background: rgba(139,92,246,0.14); }}
QTabBar::tab:hover {{ color: {T.TEXT}; background: rgba(255,255,255,0.05); }}

/* Table */
QTableWidget {{
    background: {T.BG}; border: none; border-radius: 12px;
    gridline-color: transparent; color: {T.TEXT}; font-size: 13px;
    selection-background-color: rgba(139,92,246,0.18);
}}
QTableWidget::item {{ padding: 8px; border: none; }}
QHeaderView::section {{
    background: {T.BG2}; color: {T.TEXT2}; font-weight: 600;
    padding: 10px 8px; border: none;
}}

/* Calendar */
QCalendarWidget {{ background: {T.BG2}; border: none; border-radius: 14px; }}
QCalendarWidget QWidget {{ background: transparent; color: {T.TEXT}; }}
QCalendarWidget QToolButton {{
    color: {T.TEXT}; background: transparent; border-radius: 8px; padding: 8px;
    font-size: 14px; font-weight: 700;
}}
QCalendarWidget QToolButton:hover {{ background: rgba(139,92,246,0.15); }}
QCalendarWidget QAbstractItemView {{
    selection-background-color: {T.PRIMARY}; selection-color: white;
    font-size: 13px; outline: none;
}}
QCalendarWidget QAbstractItemView::item {{ border-radius: 6px; padding: 4px; }}

/* Progress */
QProgressBar {{
    background: {T.BG3}; border: none; border-radius: 6px;
    height: 10px; color: transparent;
}}
QProgressBar::chunk {{
    border-radius: 6px;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {T.G1},stop:1 {T.G2});
}}

QToolTip {{
    background: {T.BG3}; color: {T.TEXT}; border: none;
    border-radius: 8px; padding: 8px 12px; font-size: 12px;
}}
QMessageBox {{ background: {T.BG2}; }}
QMessageBox QLabel {{ color: {T.TEXT}; font-size: 13px; }}
QMessageBox QPushButton {{
    background: {T.PRIMARY}; color: white; border: none; border-radius: 10px;
    padding: 10px 28px; font-weight: 600; min-width: 80px;
}}
QDialog {{ background: {T.BG}; }}
"""


# ═══════════════════════════════════════════════════════════════════
#  YARDIMCI
# ═══════════════════════════════════════════════════════════════════

def make_btn(text, primary=True, icon_text="", w=None, h=42):
    btn = QPushButton(f"  {icon_text}  {text}  " if icon_text else f"  {text}  ")
    btn.setCursor(Qt.PointingHandCursor)
    btn.setFixedHeight(h)
    if w: btn.setFixedWidth(w)
    r = h // 3
    secondary_hover = "#3f3f46" if T.AKTIF == "dark" else "#e7edf0"
    if primary:
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {T.G1},stop:1 {T.G2});
                color: white; border: none; border-radius: {r}px;
                font-size: 13px; font-weight: 600; padding: 0 22px;
            }}
            QPushButton:hover {{ background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {T.PRIMARY_L},stop:1 {T.G2}); }}
            QPushButton:pressed {{ padding-top: 2px; }}
        """)
    else:
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {T.BG3}; color: {T.TEXT2}; border: none;
                border-radius: {r}px; font-size: 13px; font-weight: 500; padding: 0 22px;
            }}
            QPushButton:hover {{ background: {secondary_hover}; color: {T.TEXT}; }}
        """)
    return btn


def make_label(text, size=14, bold=False, color=None):
    lbl = QLabel(text)
    c = color or T.TEXT
    w = "700" if bold else "400"
    lbl.setStyleSheet(f"color:{c};font-size:{size}px;font-weight:{w};background:transparent;")
    return lbl


def make_card():
    card = QFrame()
    card.setStyleSheet(f"""
        QFrame {{ background: {T.CARD}; border: none; border-radius: 22px; }}
        QFrame:hover {{ background: {T.CARD_H}; }}
    """)
    shadow(card, 28, 0, 8, QColor(0, 0, 0, 60 if T.AKTIF == 'dark' else 25))
    return card


def make_input(placeholder="", echo=False):
    inp = QLineEdit()
    inp.setPlaceholderText(placeholder)
    if echo: inp.setEchoMode(QLineEdit.Password)
    inp.setFixedHeight(46)
    return inp


def make_sep():
    s = QFrame()
    s.setFixedHeight(10)
    s.setStyleSheet("background:transparent;")
    return s


def alpha_color(color, alpha):
    qcolor = QColor(color)
    return f"rgba({qcolor.red()},{qcolor.green()},{qcolor.blue()},{alpha})"


def open_html_in_browser(html, stem="seyahat-map"):
    safe_stem = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in stem).strip("-") or "seyahat-map"
    preview_dir = os.path.join(tempfile.gettempdir(), "SEYEHATApp", "maps")
    os.makedirs(preview_dir, exist_ok=True)
    html_path = os.path.join(preview_dir, f"{safe_stem}.html")
    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html)
    return QDesktopServices.openUrl(QUrl.fromLocalFile(html_path)), html_path


class DonutChart(QWidget):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.data = data or []
        self.setMinimumSize(200, 200)
        self.setMaximumSize(260, 260)

    def set_data(self, d): self.data = d; self.update()

    def paintEvent(self, e):
        if not self.data: return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        s = min(self.width(), self.height())
        m = 12
        rect = QRectF(m, m, s-2*m, s-2*m)
        total = sum(v for _, v, _ in self.data)
        if total <= 0: return
        start = 90 * 16
        for _, val, col in self.data:
            span = int((val / total) * 360 * 16)
            p.setPen(Qt.NoPen); p.setBrush(QColor(col))
            p.drawPie(rect, start, -span)
            start -= span
        inner = s * 0.55
        ir = QRectF((self.width()-inner)/2, (self.height()-inner)/2, inner, inner)
        p.setBrush(QColor(T.CARD)); p.drawEllipse(ir)
        p.setPen(QColor(T.TEXT)); p.setFont(QFont("Segoe UI", 13, QFont.Bold))
        p.drawText(ir, Qt.AlignCenter, f"₺{total:,.0f}")
        p.end()

class StatCard(QFrame):
    def __init__(self, title, value, icon, color, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"QFrame {{ background: {T.CARD}; border-radius: 16px; }}"
            f"QFrame:hover {{ background: {T.CARD_H}; }}"
        )
        l = QVBoxLayout(self)
        l.addWidget(make_label(f"{icon} {title}", 11, False, T.TEXT2))
        l.addWidget(make_label(value, 20, True, color))

class AgendaCalendar(QWidget):
    secim_degisti = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._gun_ogeleri = {}
        self._seyahat_gunleri = set()
        self._secili = QDate.currentDate()
        self._gosterilen_ay = QDate.currentDate().month()
        self._gosterilen_yil = QDate.currentDate().year()
        self._hover_date = None
        self.setMinimumHeight(300)
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)

    def veri_ayarla(self, gun_ogeleri, seyahat_gunleri):
        self._gun_ogeleri = gun_ogeleri
        self._seyahat_gunleri = set(seyahat_gunleri)
        self.update()

    def setSelectedDate(self, date):
        if not isinstance(date, QDate) or not date.isValid():
            return
        self._secili = date
        self._gosterilen_ay = date.month()
        self._gosterilen_yil = date.year()
        self.update()

    def selectedDate(self):
        return self._secili

    def _onceki_ay(self):
        d = QDate(self._gosterilen_yil, self._gosterilen_ay, 1).addMonths(-1)
        self._gosterilen_ay = d.month()
        self._gosterilen_yil = d.year()
        self.update()

    def _sonraki_ay(self):
        d = QDate(self._gosterilen_yil, self._gosterilen_ay, 1).addMonths(1)
        self._gosterilen_ay = d.month()
        self._gosterilen_yil = d.year()
        self.update()

    def mousePressEvent(self, event):
        pos = event.pos()
        # Nav buttons
        if pos.y() < 40:
            if pos.x() < 50:
                self._onceki_ay(); return
            elif pos.x() > self.width() - 50:
                self._sonraki_ay(); return
        # Day cells
        date = self._hit_test(pos)
        if date and date.isValid():
            self._secili = date
            self.secim_degisti.emit(date.toString("yyyy-MM-dd"))
            self.update()

    def mouseMoveEvent(self, event):
        date = self._hit_test(event.pos())
        if date != self._hover_date:
            self._hover_date = date
            self.update()

    def leaveEvent(self, event):
        self._hover_date = None
        self.update()

    def _hit_test(self, pos):
        header_h = 68
        if pos.y() < header_h:
            return None
        w = self.width()
        h = self.height() - header_h
        cell_w = w / 7
        cell_h = h / 6.0
        col = int(pos.x() / cell_w)
        row = int((pos.y() - header_h) / cell_h)
        if col < 0 or col > 6 or row < 0 or row > 5:
            return None
        ilk = QDate(self._gosterilen_yil, self._gosterilen_ay, 1)
        dow = ilk.dayOfWeek()
        gun = row * 7 + col - (dow - 1) + 1
        if gun < 1 or gun > ilk.daysInMonth():
            return None
        return QDate(self._gosterilen_yil, self._gosterilen_ay, gun)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()
        header_h = 68

        # Background
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(T.CARD))
        p.drawRoundedRect(self.rect(), 18, 18)

        ay_ad = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran",
                  "Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]

        # ── Nav arrows ──
        p.setPen(QColor(T.TEXT2))
        af = QFont("Segoe UI", 18, QFont.Bold)
        p.setFont(af)
        p.drawText(QRectF(8, 6, 36, 32), Qt.AlignCenter, "‹")
        p.drawText(QRectF(w - 44, 6, 36, 32), Qt.AlignCenter, "›")

        # ── Month title ──
        p.setPen(QColor(T.TEXT))
        tf = QFont("Segoe UI", 15, QFont.Bold)
        p.setFont(tf)
        p.drawText(QRectF(50, 6, w - 100, 32), Qt.AlignCenter,
                   f"{ay_ad[self._gosterilen_ay - 1]} {self._gosterilen_yil}")

        # ── Weekday headers ──
        gun_ad = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        cell_w = w / 7
        cell_h = (h - header_h) / 6.0
        hf = QFont("Segoe UI", 10, QFont.DemiBold)
        p.setFont(hf)
        p.setPen(QColor(T.TEXT3))
        for i, ad in enumerate(gun_ad):
            p.drawText(QRectF(i * cell_w, 42, cell_w, 22), Qt.AlignCenter, ad)

        # ── Day cells ──
        ilk = QDate(self._gosterilen_yil, self._gosterilen_ay, 1)
        dow = ilk.dayOfWeek()
        son = ilk.daysInMonth()
        bugun = QDate.currentDate()
        df = QFont("Segoe UI", 12)
        dbf = QFont("Segoe UI", 12, QFont.Bold)

        for gun in range(1, son + 1):
            date = QDate(self._gosterilen_yil, self._gosterilen_ay, gun)
            ts = date.toString("yyyy-MM-dd")
            off = dow - 1 + gun - 1
            row = off // 7
            col = off % 7
            cx = col * cell_w + cell_w / 2
            cr = QRectF(col * cell_w + 4, header_h + row * cell_h + 3, cell_w - 8, cell_h - 6)

            sec = date == self._secili
            bg = date == bugun
            sey = ts in self._seyahat_gunleri
            oge = self._gun_ogeleri.get(ts, [])
            hov = self._hover_date == date and not sec

            # Hover
            if hov:
                p.setPen(Qt.NoPen)
                p.setBrush(QColor(T.BG3))
                p.drawRoundedRect(cr, 12, 12)

            # Seyahat bg
            if sey and not sec:
                p.setPen(Qt.NoPen)
                p.setBrush(QColor(139, 92, 246, 18))
                p.drawRoundedRect(cr, 12, 12)

            # Selected
            if sec:
                g = QLinearGradient(cr.topLeft(), cr.bottomRight())
                g.setColorAt(0, QColor(T.G1))
                g.setColorAt(1, QColor(T.G2))
                p.setPen(Qt.NoPen)
                p.setBrush(g)
                p.drawRoundedRect(cr, 12, 12)
            elif bg:
                p.setPen(Qt.NoPen)
                p.setBrush(QColor(139, 92, 246, 15))
                p.drawRoundedRect(cr, 12, 12)

            # Text
            if sec:
                p.setPen(QColor("white"))
                p.setFont(dbf)
            elif bg:
                p.setPen(QColor(T.PRIMARY_L))
                p.setFont(dbf)
            else:
                p.setPen(QColor(T.TEXT))
                p.setFont(df)

            tr = QRectF(col * cell_w, header_h + row * cell_h, cell_w, cell_h - 10)
            p.drawText(tr, Qt.AlignCenter, str(gun))

            # Dots
            if oge and not sec:
                dy = header_h + row * cell_h + cell_h - 9
                dots = []
                if any(o.get("tur") == "plan" for o in oge): dots.append(T.CYAN)
                if any(o.get("tur") == "aktivite" for o in oge): dots.append(T.EMERALD)
                if not dots: dots.append(T.PRIMARY)
                tw = len(dots) * 6 + (len(dots) - 1) * 2
                sx = cx - tw / 2
                for i, c in enumerate(dots[:3]):
                    p.setPen(Qt.NoPen)
                    p.setBrush(QColor(c))
                    p.drawEllipse(QPointF(sx + i * 8 + 3, dy), 3, 3)

        p.end()


# ═══════════════════════════════════════════════════════════════════
#  GİRİŞ
# ═══════════════════════════════════════════════════════════════════

class GirisSayfasi(QWidget):
    giris_basarili = pyqtSignal()
    kayit_goster = pyqtSignal()

    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedSize(440, 620)
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 {T.BG2},stop:1 {T.BG});
                border: none; border-radius: 28px;
            }}
        """)
        shadow(card, 50, 0, 15, QColor(139, 92, 246, 35))
        cl = QVBoxLayout(card)
        cl.setSpacing(14)
        cl.setContentsMargins(44, 40, 44, 40)

        logo = QLabel("✈️")
        logo.setStyleSheet("font-size:52px;background:transparent;")
        logo.setAlignment(Qt.AlignCenter)
        cl.addWidget(logo)
        t = QLabel("TravelPlan")
        t.setStyleSheet(f"font-size:28px;font-weight:800;color:{T.TEXT};background:transparent;")
        t.setAlignment(Qt.AlignCenter)
        cl.addWidget(t)
        s = QLabel("Hesabınıza giriş yapın")
        s.setStyleSheet(f"font-size:13px;color:{T.TEXT2};background:transparent;")
        s.setAlignment(Qt.AlignCenter)
        cl.addWidget(s)
        cl.addSpacing(12)

        cl.addWidget(make_label("Kullanıcı Adı", 12, color=T.TEXT2))
        self.user_inp = make_input("Kullanıcı adınızı girin")
        cl.addWidget(self.user_inp)
        cl.addWidget(make_label("Şifre", 12, color=T.TEXT2))
        self.pass_inp = make_input("Şifrenizi girin", echo=True)
        cl.addWidget(self.pass_inp)
        cl.addSpacing(4)

        self.hata = QLabel("")
        self.hata.setStyleSheet(f"color:{T.ROSE};font-size:12px;background:transparent;")
        self.hata.setAlignment(Qt.AlignCenter)
        cl.addWidget(self.hata)

        btn = make_btn("Giriş Yap", True, "→", h=50)
        btn.clicked.connect(self._giris)
        cl.addWidget(btn)
        cl.addSpacing(4)

        demo_btn = make_btn("Demo Giris", False, ">>", h=44)
        demo_btn.clicked.connect(self._demo_giris)
        cl.addWidget(demo_btn)
        demo_info = make_label("Demo: demo / demo123", 11, color=T.TEXT3)
        demo_info.setAlignment(Qt.AlignCenter)
        cl.addWidget(demo_info)
        cl.addSpacing(2)

        rr = QHBoxLayout()
        rr.setAlignment(Qt.AlignCenter)
        rr.addWidget(make_label("Hesabınız yok mu?", 12, color=T.TEXT3))
        rb = QPushButton("Kayıt Ol")
        rb.setCursor(Qt.PointingHandCursor)
        rb.setStyleSheet(f"""QPushButton{{background:transparent;border:none;color:{T.PRIMARY_L};
            font-size:12px;font-weight:600;}}QPushButton:hover{{color:{T.PRIMARY};}}""")
        rb.clicked.connect(self.kayit_goster.emit)
        rr.addWidget(rb)
        cl.addLayout(rr)
        cl.addStretch()
        lay.addWidget(card)

        self.pass_inp.returnPressed.connect(self._giris)
        self.user_inp.returnPressed.connect(lambda: self.pass_inp.setFocus())

    def _giris(self):
        u, p = self.user_inp.text().strip(), self.pass_inp.text().strip()
        if not u or not p:
            self.hata.setText("Tüm alanları doldurun!"); return
        if self.yon.giris_yap(u, p):
            self.hata.setText(""); self.giris_basarili.emit()
        else:
            self.hata.setText("Kullanıcı adı veya şifre hatalı!")


    def _demo_giris(self):
        if self.yon.demo_giris_yap():
            self.hata.setText("")
            self.giris_basarili.emit()
        else:
            self.hata.setText("Demo hesabi acilamadi.")


class KayitSayfasi(QWidget):
    kayit_basarili = pyqtSignal()
    giris_goster = pyqtSignal()

    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignCenter)
        card = QFrame()
        card.setFixedSize(440, 620)
        card.setStyleSheet(f"QFrame{{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,"
                           f"stop:0 {T.BG2},stop:1 {T.BG});border:none;border-radius:28px;}}")
        shadow(card, 50, 0, 15, QColor(139, 92, 246, 35))
        cl = QVBoxLayout(card)
        cl.setSpacing(10)
        cl.setContentsMargins(44, 35, 44, 35)

        logo = QLabel("🌍")
        logo.setStyleSheet("font-size:44px;background:transparent;")
        logo.setAlignment(Qt.AlignCenter)
        cl.addWidget(logo)
        t = QLabel("Hesap Oluştur")
        t.setStyleSheet(f"font-size:24px;font-weight:800;color:{T.TEXT};background:transparent;")
        t.setAlignment(Qt.AlignCenter)
        cl.addWidget(t)
        cl.addSpacing(8)

        for lbl_text, attr, ph, echo in [
            ("Ad Soyad", "name_inp", "Adınız Soyadınız", False),
            ("Kullanıcı Adı", "user_inp", "Kullanıcı adı seçin", False),
            ("E-posta", "email_inp", "ornek@mail.com", False),
            ("Şifre", "pass_inp", "En az 6 karakter", True),
        ]:
            cl.addWidget(make_label(lbl_text, 12, color=T.TEXT2))
            inp = make_input(ph, echo)
            setattr(self, attr, inp)
            cl.addWidget(inp)

        self.hata = QLabel("")
        self.hata.setStyleSheet(f"color:{T.ROSE};font-size:12px;background:transparent;")
        self.hata.setAlignment(Qt.AlignCenter)
        cl.addWidget(self.hata)

        btn = make_btn("Kayıt Ol", True, "✓", h=50)
        btn.clicked.connect(self._kayit)
        cl.addWidget(btn)

        rr = QHBoxLayout()
        rr.setAlignment(Qt.AlignCenter)
        rr.addWidget(make_label("Zaten hesabınız var mı?", 12, color=T.TEXT3))
        lb = QPushButton("Giriş Yap")
        lb.setCursor(Qt.PointingHandCursor)
        lb.setStyleSheet(f"QPushButton{{background:transparent;border:none;color:{T.PRIMARY_L};"
                         f"font-size:12px;font-weight:600;}}QPushButton:hover{{color:{T.PRIMARY};}}")
        lb.clicked.connect(self.giris_goster.emit)
        rr.addWidget(lb)
        cl.addLayout(rr)
        cl.addStretch()
        lay.addWidget(card)

    def _kayit(self):
        n = self.name_inp.text().strip()
        u = self.user_inp.text().strip()
        e = self.email_inp.text().strip()
        p = self.pass_inp.text().strip()
        if not all([n, u, e, p]): self.hata.setText("Tüm alanları doldurun!"); return
        if len(p) < 6: self.hata.setText("Şifre en az 6 karakter!"); return
        if "@" not in e: self.hata.setText("Geçerli e-posta girin!"); return
        uid = self.yon.kayit_ol(u, e, p, n)
        if uid:
            self.hata.setText("")
            QMessageBox.information(self, "Başarılı", "Kayıt başarılı! Giriş yapabilirsiniz.")
            self.kayit_basarili.emit()
        else:
            self.hata.setText("Bu kullanıcı adı veya e-posta zaten mevcut!")


# ═══════════════════════════════════════════════════════════════════
#  YAN MENÜ
# ═══════════════════════════════════════════════════════════════════

class YanMenu(QFrame):
    sayfa_degisti = pyqtSignal(int)
    ITEMS = [("🏠", "Ana Sayfa", 0), ("✈️", "Seyahatler", 1), ("➕", "Yeni Seyahat", 2),
             ("🗺️", "Harita", 3), ("⚙️", "Ayarlar", 6)]

    def __init__(self, parent=None): 
        super().__init__(parent)
        self.setFixedWidth(220)
        self.setStyleSheet(f"QFrame{{background:{T.SIDEBAR};border:none;}}")
        self.aktif = 0
        self.buttons = []
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 20, 12, 20)
        lay.setSpacing(3)

        lr = QHBoxLayout()
        lr.addWidget(make_label("✈️", 24))
        l = QLabel("TravelPlan")
        l.setStyleSheet(f"font-size:18px;font-weight:800;color:{T.TEXT};background:transparent;")
        lr.addWidget(l); lr.addStretch()
        lay.addLayout(lr)
        lay.addSpacing(28)

        for i, (icon, text, sid) in enumerate(self.ITEMS):
            btn = QPushButton(f"  {icon}   {text}")
            btn.setFixedHeight(44)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda c, idx=i, sayfa_id=sid: self._tiklandi(idx, sayfa_id))
            self.buttons.append(btn)
            lay.addWidget(btn)

        lay.addStretch()
        lay.addWidget(make_sep())
        lay.addSpacing(6)
        cb = QPushButton("  🚪   Çıkış Yap")
        cb.setFixedHeight(44); cb.setCursor(Qt.PointingHandCursor)
        cb.setStyleSheet(f"""QPushButton{{background:transparent;border:none;border-radius:12px;
            color:{T.ROSE};font-size:13px;font-weight:500;text-align:left;padding-left:14px;}}
            QPushButton:hover{{background:rgba(251,113,133,0.08);}}""")
        cb.clicked.connect(lambda: self.sayfa_degisti.emit(-1))
        lay.addWidget(cb)
        self._stil()

    def _tiklandi(self, idx, sid):
        self.aktif = idx; self._stil(); self.sayfa_degisti.emit(sid)

    def _stil(self):
        for i, btn in enumerate(self.buttons):
            if i == self.aktif:
                btn.setStyleSheet(f"""QPushButton{{
                    background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {T.G1},stop:1 {T.G2});
                    color:white;border:none;border-radius:12px;font-size:13px;font-weight:600;
                    text-align:left;padding-left:14px;}}""")
            else:
                btn.setStyleSheet(f"""QPushButton{{background:transparent;border:none;border-radius:12px;
                    color:{T.TEXT2};font-size:13px;font-weight:500;text-align:left;padding-left:14px;}}
                    QPushButton:hover{{background:rgba(139,92,246,0.06);color:{T.PRIMARY_L};}}""")

    def set_aktif(self, sid):
        idx = -1
        for i, item in enumerate(self.ITEMS):
            if item[2] == sid:
                idx = i
                break
        self.aktif = idx
        self._stil()


# ═══════════════════════════════════════════════════════════════════
#  ANA SAYFA
# ═══════════════════════════════════════════════════════════════════

class AnaSayfa(QWidget):
    seyahat_detay = pyqtSignal(int)
    yeni_seyahat = pyqtSignal()
    profil_goster = pyqtSignal()
    bildirim_goster = pyqtSignal()

    # Şehir koordinatları (harita için)
    SEHIR_COORDS = {
        "İstanbul": (41.0082, 28.9784), "Istanbul": (41.0082, 28.9784),
        "Paris": (48.8566, 2.3522), "Roma": (41.9028, 12.4964),
        "Tokyo": (35.6762, 139.6503), "Barcelona": (41.3851, 2.1734),
        "Londra": (51.5074, -0.1278), "London": (51.5074, -0.1278),
        "Dubai": (25.2048, 55.2708), "Antalya": (36.8969, 30.7133),
        "New York": (40.7128, -74.0060), "Kapadokya": (38.6431, 34.8289),
        "Amsterdam": (52.3676, 4.9041), "Prag": (50.0755, 14.4378),
        "Berlin": (52.5200, 13.4050), "Madrid": (40.4168, -3.7038),
        "Viyana": (48.2082, 16.3738), "Lizbon": (38.7169, -9.1399),
        "Budapeşte": (47.4979, 19.0402), "Varşova": (52.2297, 21.0122),
        "Seul": (37.5665, 126.9780), "Bangkok": (13.7563, 100.5018),
        "Bali": (-8.3405, 115.0920), "Sydney": (-33.8688, 151.2093),
        "Maldivler": (3.2028, 73.2207), "Santorini": (36.3932, 25.4615),
        "Bern": (46.9480, 7.4474), "Zürich": (47.3769, 8.5417),
        "Floransa": (43.7696, 11.2558), "Venedik": (45.4408, 12.3155),
        "Bodrum": (37.0344, 27.4305), "Alanya": (36.5441, 32.0059),
        "Trabzon": (41.0015, 39.7178), "Ankara": (39.9334, 32.8597),
        "İzmir": (38.4237, 27.1428), "Bursa": (40.1885, 29.0610),
    }

    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon

        ml = QVBoxLayout(self)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(0)

        # ── Header ──
        self.header_w = QWidget()
        self.header_w.setFixedHeight(72)
        self.header_w.setStyleSheet("background:transparent;")
        hl = QHBoxLayout(self.header_w)
        hl.setContentsMargins(32, 0, 32, 0)

        self.sel_lbl = QLabel("")
        self.sel_lbl.setStyleSheet(f"color:{T.TEXT};font-size:22px;font-weight:800;background:transparent;")
        hl.addWidget(self.sel_lbl)
        hl.addSpacing(20)

        self.search_bar = make_input("🔍  Seyahatlerde ara...")
        self.search_bar.setFixedWidth(280)
        hl.addWidget(self.search_bar)
        hl.addStretch()

        self.notif_btn = QPushButton("🔔")
        self.notif_btn.setFixedSize(44, 44)
        self.notif_btn.setCursor(Qt.PointingHandCursor)
        self.notif_btn.setStyleSheet(
            f"QPushButton{{background:{T.BG2};border-radius:22px;font-size:18px;border:none;}}"
            f"QPushButton:hover{{background:rgba(139,92,246,0.15);}}")
        self.notif_btn.clicked.connect(self.bildirim_goster.emit)
        hl.addWidget(self.notif_btn)
        hl.addSpacing(10)

        self.prof_btn = QPushButton("👤")
        self.prof_btn.setFixedSize(56, 56)
        self.prof_btn.setCursor(Qt.PointingHandCursor)
        self.prof_btn.setToolTip("Profili aç")
        self.prof_btn.clicked.connect(self.profil_goster.emit)
        shadow(self.prof_btn, 24, 0, 5, QColor(139, 92, 246, 90))
        self.prof_badge = QLabel("✎", self.prof_btn)
        self.prof_badge.setFixedSize(18, 18)
        self.prof_badge.setAlignment(Qt.AlignCenter)
        self.prof_badge.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.prof_badge.move(36, 36)
        self._profil_butonunu_guncelle()
        hl.addWidget(self.prof_btn)
        ml.addWidget(self.header_w)

        # ── Scrollable Content ──
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.cw = QWidget()
        self.lay = QVBoxLayout(self.cw)
        self.lay.setContentsMargins(28, 12, 28, 28)
        self.lay.setSpacing(20)
        self.scroll.setWidget(self.cw)
        ml.addWidget(self.scroll, 1)

        # ── Floating AI Button ──
        self.ai_btn = QPushButton("🤖\nAI")
        self.ai_btn.setFixedSize(64, 64)
        self.ai_btn.setCursor(Qt.PointingHandCursor)
        self.ai_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {T.G1},stop:1 {T.G2});
                color: white; border: none; border-radius: 32px;
                font-size: 15px; font-weight: 800; border: none;
            }}
            QPushButton:hover {{ opacity: 0.9; }}
            QPushButton:pressed {{ padding-top: 2px; }}
        """)
        shadow(self.ai_btn, 35, 0, 10, QColor(139, 92, 246, 140))
        self.ai_btn.setParent(self)
        self.ai_btn.clicked.connect(self._ai_tiklandi)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.ai_btn.move(self.width() - 95, self.height() - 95)

    def _profil_butonunu_guncelle(self, user=None):
        user = user or self.yon.aktif_kullanici or {}
        avatar_path = user.get("avatar_path", "")
        boyut = self.prof_btn.width()
        yaricap = boyut // 2
        self.prof_btn.setIcon(QIcon())
        self.prof_btn.setIconSize(QSize(boyut - 8, boyut - 8))

        if avatar_path and os.path.exists(avatar_path):
            pix = dairesel_avatar_pixmap(avatar_path, boyut - 4, 0.8)
            self.prof_btn.setText("")
            self.prof_btn.setIcon(QIcon(pix))
            self.prof_btn.setStyleSheet(f"""
                QPushButton {{
                    background:{T.BG2};
                    border-radius:{yaricap}px;
                    padding:2px;
                }}
                QPushButton:hover {{
                    background:{T.BG3};
                }}
                QPushButton:pressed {{
                    background:{T.CARD_H};
                }}
            """)
        else:
            self.prof_btn.setText("👤")
            self.prof_btn.setStyleSheet(f"""
                QPushButton {{
                    background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {T.G1},stop:1 {T.G2});
                    color:white;
                    border-radius:{yaricap}px;
                    font-size:24px;
                    font-weight:700;
                }}
                QPushButton:hover {{
                    background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {T.PRIMARY_L},stop:1 {T.G2});
                }}
                QPushButton:pressed {{
                    padding-top:1px;
                }}
            """)

        self.prof_badge.setStyleSheet(
            f"background:{T.PRIMARY};color:white;border:none;"
            "border-radius:9px;font-size:10px;font-weight:800;"
        )
        self.prof_badge.raise_()

    def set_kullanici(self, user):
        ad = user.get("ad_soyad", user.get("kullanici_adi", "")) if user else ""
        saat = datetime.now().hour
        sel = "Günaydın" if saat < 12 else ("İyi Günler" if saat < 18 else "İyi Akşamlar")
        self.sel_lbl.setText(f"{sel}, {ad} 👋")
        self._profil_butonunu_guncelle(user)

    def set_bildirim(self, n):
        if n > 0:
            self.notif_btn.setText(f"🔔 {n}")
            self.notif_btn.setStyleSheet(
                f"QPushButton{{background:{T.BG2};border-radius:22px;font-size:14px;color:{T.ROSE};font-weight:bold;border:none;}}"
                f"QPushButton:hover{{background:rgba(139,92,246,0.15);}}")
        else:
            self.notif_btn.setText("🔔")
            self.notif_btn.setStyleSheet(
                f"QPushButton{{background:{T.BG2};border-radius:22px;font-size:18px;color:{T.TEXT};border:none;}}"
                f"QPushButton:hover{{background:rgba(139,92,246,0.15);}}")

    def _ai_tiklandi(self):
        AIAsistanDialog(self.yon, parent=self).exec_()

    def yukle(self):
        self._cl(self.lay)

        seyahatler = self.yon.seyahatleri_listele()
        ak = [s for s in seyahatler if s.durum() == "aktif"]
        oncelikli = self.yon.oncelikli_seyahat(seyahatler)
        oncelikli_aktif = bool(oncelikli and oncelikli.durum() == "aktif")
        th = self.yon.db.harcama_toplam(oncelikli.seyahat_id) if oncelikli else 0
        hedef_shr = oncelikli.sehir if oncelikli else "İstanbul"

        # ═══ 1. HERO BANNER ═══
        hero = QFrame()
        hero.setFixedHeight(160)
        hero.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 rgba(99,102,241,0.25), stop:0.4 rgba(139,92,246,0.18),
                    stop:0.7 rgba(217,70,239,0.15), stop:1 rgba(6,182,212,0.20));
                border: none;
                border-radius: 24px;
            }}
        """)
        shadow(hero, 30, 0, 8, QColor(139, 92, 246, 50))
        hl = QHBoxLayout(hero)
        hl.setContentsMargins(28, 20, 28, 20)

        # Sol: bilgi
        left_vl = QVBoxLayout(); left_vl.setSpacing(6)
        if oncelikli:
            status_lbl = QLabel(f"  {'🟢 AKTİF' if oncelikli_aktif else '⏳ YAKLAŞAN'}  ")
            status_lbl.setStyleSheet(
                f"background:{'rgba(52,211,153,0.18)' if oncelikli_aktif else 'rgba(56,189,248,0.18)'};"
                f"color:{'#34d399' if oncelikli_aktif else '#38bdf8'};border-radius:10px;"
                "font-size:11px;font-weight:700;padding:4px 10px;")
            left_vl.addWidget(status_lbl)
            dest_lbl = QLabel(f"{'🛫' if oncelikli_aktif else '✈️'}  {oncelikli.sehir}")
            dest_lbl.setStyleSheet(f"color:{T.TEXT};font-size:32px;font-weight:900;background:transparent;")
            left_vl.addWidget(dest_lbl)
            info_row = QHBoxLayout(); info_row.setSpacing(18)
            info_row.addWidget(make_label(f"📅 {oncelikli.baslangic_tarihi} → {oncelikli.bitis_tarihi}", 12, color=T.TEXT2))
            if oncelikli.kalan_gun() > 0:
                info_row.addWidget(make_label(f"⏰ {oncelikli.kalan_gun()} gün kaldı", 12, True, T.AMBER))
            info_row.addStretch()
            left_vl.addLayout(info_row)
        else:
            dest_lbl = QLabel("🌍  Dünyayı Keşfet")
            dest_lbl.setStyleSheet(f"color:{T.TEXT};font-size:30px;font-weight:900;background:transparent;")
            left_vl.addWidget(dest_lbl)
            left_vl.addWidget(make_label("Yeni bir seyahat planlamaya başlayın!", 14, color=T.TEXT2))

        hl.addLayout(left_vl, 1)
        hl.addSpacing(20)

        # Sağ: Hızlı istatistikler
        stats_mini = QHBoxLayout(); stats_mini.setSpacing(12)
        for icon, val, lbl_text, color in [
            ("🌍", str(len(seyahatler)), "Seyahat", T.PRIMARY_L),
            ("📍", str(len(ak)), "Aktif", T.EMERALD),
            ("💰", f"₺{th:,.0f}" if th < 1000000 else f"₺{th/1000:.0f}K", "Harcanan", T.AMBER),
        ]:
            sc = QFrame()
            sc.setStyleSheet(f"QFrame{{background:rgba(255,255,255,0.05);border-radius:16px;border:none;}}")
            scl = QVBoxLayout(sc); scl.setContentsMargins(16, 12, 16, 12); scl.setSpacing(2)
            scl.addWidget(make_label(icon, 22))
            scl.addWidget(make_label(val, 18, True, color))
            scl.addWidget(make_label(lbl_text, 10, color=T.TEXT2))
            stats_mini.addWidget(sc)

        new_btn = QPushButton("  ➕  Yeni Seyahat")
        new_btn.setFixedHeight(44)
        new_btn.setCursor(Qt.PointingHandCursor)
        new_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {T.G1},stop:1 {T.G2});
                color: white; border: none; border-radius: 22px;
                font-size: 13px; font-weight: 700; padding: 0 20px;
            }}
            QPushButton:hover {{ opacity:0.9; }}
        """)
        new_btn.clicked.connect(self.yeni_seyahat.emit)
        stats_mini.addWidget(new_btn)
        hl.addLayout(stats_mini)
        self.lay.addWidget(hero)

        # ═══ 2. ANA İÇERİK: İKİ KOLON ═══
        main_row = QHBoxLayout()
        main_row.setSpacing(20)

        # ── SOL KOLON ──
        left_col = QVBoxLayout()
        left_col.setSpacing(18)

        # Takvim kartı
        tc = make_card()
        tcl = QVBoxLayout(tc); tcl.setContentsMargins(14, 14, 14, 14); tcl.setSpacing(8)

        # Takvim header
        cal_header = QHBoxLayout()
        cal_header.addWidget(make_label("🗓️ Takvim", 15, True, T.PRIMARY_L))
        cal_header.addStretch()

        # Collect full plan data for popup
        gun_ogeleri = {}; seyahat_gunleri = set()
        seyahat_idleri = [s.seyahat_id for s in seyahatler]
        sehir_map = {s.seyahat_id: s.sehir for s in seyahatler}
        tum_planlar = self.yon.db.planlari_toplu_getir(seyahat_idleri)
        tum_aktiviteler = self.yon.db.aktiviteleri_toplu_getir(seyahat_idleri)
        total_plans = len(tum_planlar); total_akts = len(tum_aktiviteler)

        for p in tum_planlar:
            t = p.get("tarih") or p.get("gun")
            if t:
                gun_ogeleri.setdefault(t, []).append({
                    "tur": "plan", "kaynak": p.get("kaynak", "manuel"),
                    "baslik": p.get("baslik", "Plan"), "saat": p.get("saat", ""),
                    "konum": p.get("konum", ""), "sehir": sehir_map.get(p["seyahat_id"], "")
                })

        for a in tum_aktiviteler:
            if a.get("tarih"):
                gun_ogeleri.setdefault(a["tarih"], []).append({
                    "tur": "aktivite", "kaynak": a.get("kaynak", "manuel"),
                    "baslik": a.get("aktivite_adi", "Aktivite"), "saat": a.get("saat", ""),
                    "konum": a.get("konum", ""), "sehir": sehir_map.get(a["seyahat_id"], "")
                })

        for s_idx in seyahatler:
            b = QDate.fromString(s_idx.baslangic_tarihi, "yyyy-MM-dd")
            bit = QDate.fromString(s_idx.bitis_tarihi, "yyyy-MM-dd")
            if b.isValid() and bit.isValid():
                while b <= bit:
                    seyahat_gunleri.add(b.toString("yyyy-MM-dd"))
                    b = b.addDays(1)

        for lbl_t, val_t, col_t in [("📅", str(total_plans), T.CYAN), ("🎯", str(total_akts), T.EMERALD)]:
            badge = QLabel(f"  {lbl_t} {val_t}  ")
            badge.setStyleSheet(f"background:rgba(255,255,255,0.05);color:{col_t};border-radius:8px;"
                                "font-size:11px;font-weight:700;padding:3px;")
            cal_header.addWidget(badge)
        tcl.addLayout(cal_header)

        # Legend
        legend_row = QHBoxLayout(); legend_row.setSpacing(12)
        for col_l, txt_l in [(T.PRIMARY, "Seyahat"), (T.CYAN, "Plan"), (T.EMERALD, "Aktivite")]:
            lr = QHBoxLayout(); lr.setSpacing(4)
            dot = QFrame(); dot.setFixedSize(8, 8)
            dot.setStyleSheet(f"background:{col_l};border-radius:4px;")
            lr.addWidget(dot); lr.addWidget(make_label(txt_l, 10, color=T.TEXT2))
            legend_row.addLayout(lr)
        legend_row.addStretch()
        tcl.addLayout(legend_row)

        self.takvim = AgendaCalendar()
        self.takvim.veri_ayarla(gun_ogeleri, list(seyahat_gunleri))
        self.takvim.setMinimumHeight(280)
        tcl.addWidget(self.takvim)

        # ── Day detail popup panel (collapsible) ──
        self._day_panel = QFrame()
        self._day_panel.setStyleSheet(f"QFrame{{background:{T.BG2 if T.AKTIF == 'dark' else T.BG3};"
                                     f"border:none;border-radius:14px;}}")
        self._day_panel.setVisible(False)
        self._day_panel.setMaximumHeight(220)
        dpl = QVBoxLayout(self._day_panel)
        dpl.setContentsMargins(12, 10, 12, 10)
        dpl.setSpacing(6)

        day_hdr = QHBoxLayout()
        self._day_title = make_label("📆 Bugün", 13, True)
        day_hdr.addWidget(self._day_title)
        day_hdr.addStretch()
        day_close = QPushButton("✕")
        day_close.setFixedSize(24, 24)
        day_close.setCursor(Qt.PointingHandCursor)
        day_close.setStyleSheet(f"QPushButton{{background:{T.BG3};border:none;border-radius:12px;"
                                f"color:{T.TEXT2};font-size:12px;font-weight:700;}}"
                                f"QPushButton:hover{{background:{T.ROSE};color:white;}}")
        day_close.clicked.connect(lambda: self._day_panel.setVisible(False))
        day_hdr.addWidget(day_close)
        dpl.addLayout(day_hdr)

        self._day_content = QVBoxLayout()
        self._day_content.setSpacing(4)
        dpl.addLayout(self._day_content)
        tcl.addWidget(self._day_panel)

        self._gun_ogeleri_full = gun_ogeleri

        def _goster_gun_detay(tarih_str):
            self._day_title.setText(f"📆 {tarih_str}")
            # Clear old content
            while self._day_content.count():
                it = self._day_content.takeAt(0)
                if it.widget(): it.widget().deleteLater()
            ogeler = self._gun_ogeleri_full.get(tarih_str, [])
            if not ogeler:
                lbl = QLabel("Bu gün için plan yok")
                lbl.setStyleSheet(f"color:{T.TEXT3};font-size:12px;padding:6px;background:transparent;")
                self._day_content.addWidget(lbl)
            else:
                for oge in ogeler[:5]:
                    row = QFrame()
                    row.setFixedHeight(34)
                    tur = oge.get("tur", "plan")
                    renk = T.CYAN if tur == "plan" else T.EMERALD
                    try:
                        r = int(renk[1:3], 16)
                        g = int(renk[3:5], 16)
                        b = int(renk[5:7], 16)
                    except Exception:
                        r, g, b = 100, 100, 100
                    row.setStyleSheet(f"QFrame{{background:rgba({r},{g},{b},0.08);"
                                      f"border:none;border-radius:8px;}}")
                    rl = QHBoxLayout(row)
                    rl.setContentsMargins(10, 3, 10, 3)
                    rl.setSpacing(6)
                    icon = "📅" if tur == "plan" else "🎯"
                    rl.addWidget(make_label(icon, 11))
                    rl.addWidget(make_label(oge.get("baslik", "—"), 11, True), 1)
                    saat = oge.get("saat", "")
                    if saat:
                        rl.addWidget(make_label(f"🕐 {saat}", 10, color=T.TEXT2))
                    self._day_content.addWidget(row)
                if len(ogeler) > 5:
                    self._day_content.addWidget(make_label(f"... +{len(ogeler)-5} daha", 10, color=T.TEXT3))
            self._day_panel.setVisible(True)

        self.takvim.secim_degisti.connect(_goster_gun_detay)

        left_col.addWidget(tc)

        # Hava + Kart satırı
        bot_row = QHBoxLayout(); bot_row.setSpacing(14)
        hava = self.yon.hava_durumu_getir(hedef_shr)
        hw = QFrame()
        hw.setFixedHeight(130)
        hw.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 rgba(34,211,238,0.12), stop:1 rgba(56,189,248,0.06));
                border: none; border-radius: 20px;
            }}
        """)
        shadow(hw, 20, 0, 5, QColor(34, 211, 238, 30))
        hwl = QVBoxLayout(hw); hwl.setContentsMargins(16, 12, 16, 12); hwl.setSpacing(2)
        icon_temp = QHBoxLayout()
        icon_temp.addWidget(make_label(hava.get("ikon", "🌤️"), 32))
        icon_temp.addSpacing(8)
        tv = QVBoxLayout()
        tv.addWidget(make_label(f"{hava.get('sicaklik', '--')}°C", 28, True, T.CYAN))
        tv.addWidget(make_label(hedef_shr, 11, color=T.TEXT2))
        icon_temp.addLayout(tv)
        icon_temp.addStretch()
        hwl.addLayout(icon_temp)
        hwl.addWidget(make_label(f"{hava.get('durum','')}  💧{hava.get('nem','--')}%  💨{hava.get('ruzgar','--')}km/h", 10, color=T.TEXT2))
        bot_row.addWidget(hw, 1)

        if oncelikli:
            bot_row.addWidget(self._kart(oncelikli), 1)
        left_col.addLayout(bot_row)

        main_row.addLayout(left_col, 4)

        # ── SAĞ KOLON: İnteraktif Harita ──
        map_card = make_card()
        map_card.setMinimumHeight(480)
        map_layout = QVBoxLayout(map_card); map_layout.setContentsMargins(4, 4, 4, 4); map_layout.setSpacing(0)
        self._map_seyahatler = seyahatler

        if HAS_WEBENGINE:
            self.map_view = QWebEngineView()
            self.map_view.setStyleSheet("border-radius:20px; background:transparent;")
            map_layout.addWidget(self.map_view)
            QTimer.singleShot(0, self._load_map_html)
        else:
            no_map = QLabel("🗺️\nHarita için\nQtWebEngine gerekli")
            no_map.setAlignment(Qt.AlignCenter)
            no_map.setWordWrap(True)
            no_map.setStyleSheet(f"color:{T.TEXT2};font-size:16px;")
            open_btn = make_btn("Tarayicida Ac", False, "MAP", h=42)
            open_btn.clicked.connect(self._open_map_in_browser)
            map_layout.addStretch()
            map_layout.addWidget(no_map)
            map_layout.addSpacing(12)
            map_layout.addWidget(open_btn, alignment=Qt.AlignCenter)
            map_layout.addStretch()

        main_row.addWidget(map_card, 6)
        self.lay.addLayout(main_row)

        # ═══ 3. SEYAHATLER: Yatay Kayan Kartlar ═══
        if seyahatler:
            cards_header = QHBoxLayout()
            cards_header.addWidget(make_label("✈️ Seyahatlerim", 16, True))
            cards_header.addStretch()
            see_all = QPushButton("Tümünü Gör →")
            see_all.setCursor(Qt.PointingHandCursor)
            see_all.setStyleSheet(f"QPushButton{{background:transparent;border:none;color:{T.PRIMARY_L};"
                                  "font-size:13px;font-weight:600;}}QPushButton:hover{color:#fff;}")
            cards_header.addWidget(see_all)
            self.lay.addLayout(cards_header)

            scroll_w = QScrollArea()
            scroll_w.setFixedHeight(170)
            scroll_w.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_w.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_w.setWidgetResizable(True)
            cards_row_w = QWidget()
            cards_row = QHBoxLayout(cards_row_w)
            cards_row.setContentsMargins(0, 4, 0, 4); cards_row.setSpacing(14)

            for s in seyahatler[:8]:
                cards_row.addWidget(self._kart(s))
            cards_row.addStretch()
            scroll_w.setWidget(cards_row_w)
            scroll_w.setStyleSheet("QScrollArea{border:none;background:transparent;}")
            self.lay.addWidget(scroll_w)

        self.lay.addStretch()

    def _get_map_html(self, seyahatler=None):
        """Tüm seyahat destinasyonlarını haritada göster"""
        # Koordinat veritabanı (merkez + tüm destinasyonlar)
        coord_db = self.SEHIR_COORDS

        # Markerlar için veri
        markers_js = ""
        center_lat, center_lng = 39.0, 35.0  # Türkiye merkezi
        zoom = 4

        if seyahatler:
            valid_coords = []
            for s in seyahatler:
                sehir = s.sehir
                coords = coord_db.get(sehir, coord_db.get(sehir.strip(), None))
                if not coords:
                    # Kısmi eşleşme dene
                    for k, v in coord_db.items():
                        if k.lower() in sehir.lower() or sehir.lower() in k.lower():
                            coords = v; break
                if coords:
                    lat, lng = coords
                    valid_coords.append((lat, lng))
                    durum = s.durum()
                    renk = "#34d399" if durum == "aktif" else ("#38bdf8" if durum == "yaklaşan" else "#6366f1")
                    tarih_info = f"{s.baslangic_tarihi} → {s.bitis_tarihi}"
                    gun = s.gun_sayisi()
                    pulse = "true" if durum == "aktif" else "false"
                    markers_js += f"""
                    addDestinationMarker({lat}, {lng}, `{sehir}`, `{tarih_info}`, `{durum.upper()}`,
                        '{renk}', {gun}, {pulse});
                    """

            if valid_coords:
                center_lat = sum(c[0] for c in valid_coords) / len(valid_coords)
                center_lng = sum(c[1] for c in valid_coords) / len(valid_coords)
                if len(valid_coords) == 1:
                    zoom = 8
                elif len(valid_coords) <= 3:
                    zoom = 5
                else:
                    zoom = 3

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body, html {{ width:100%; height:100%; overflow:hidden; background:#f0f0f0; }}
  #map {{ width:100%; height:100%; }}
  .leaflet-container {{ background:#f0f0f0 !important; border-radius:20px; }}
  .custom-popup .leaflet-popup-content-wrapper {{
    background:rgba(255,255,255,0.96);
    border:none;
    border-radius:16px; color:#2d3047;
    box-shadow:0 8px 32px rgba(0,0,0,0.15);
    backdrop-filter: blur(12px);
  }}
  .custom-popup .leaflet-popup-tip {{ background:rgba(255,255,255,0.96); }}
  .custom-popup .leaflet-popup-close-button {{ color:#6b7194 !important; font-size:18px; top:8px; right:8px; }}
  .popup-inner {{ padding:4px 2px; }}
  .popup-city {{ font-size:16px; font-weight:800; margin-bottom:4px; color:#2d3047; }}
  .popup-dates {{ font-size:12px; color:#6b7194; margin-bottom:6px; }}
  .popup-status {{ display:inline-block; padding:2px 10px; border-radius:8px;
    font-size:11px; font-weight:700; }}
  .popup-days {{ font-size:12px; color:#6b7194; margin-top:4px; }}
  @keyframes pulseRing {{
    0% {{ transform:scale(1); opacity:0.8; }}
    100% {{ transform:scale(2.5); opacity:0; }}
  }}
  .pulse-marker {{
    animation: pulseRing 1.8s ease-out infinite;
  }}
  .leaflet-attribution-flag {{ display:none !important; }}
</style>
</head>
<body>
<div id="map"></div>
<script>
var map = L.map('map', {{
    zoomControl: true,
    attributionControl: false,
    zoomAnimation: true,
    fadeAnimation: true,
    preferCanvas: true
}}).setView([{center_lat}, {center_lng}], {zoom});

// Harita katmanları
var standard = L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
    maxZoom: 19, subdomains: 'abcd'
}});
var satellite = L.tileLayer('https://mt1.google.com/vt/lyrs=s,h&x={{x}}&y={{y}}&z={{z}}', {{
    maxZoom: 20
}});
standard.addTo(map);

// Katman kontrolü
L.control.layers({{
    '🗺️ Standart': standard,
    '🛰️ Uydu': satellite
}}, {{}}, {{position: 'topright'}}).addTo(map);

// Küçük atıf
L.control.attribution({{prefix: '© CartoDB'}}).addTo(map);

function addDestinationMarker(lat, lng, city, dates, status, color, days, pulse) {{
    var markerHtml = `
    <div style="position:relative;width:36px;height:44px;">
        ${{pulse ? '<div class="pulse-marker" style="position:absolute;top:2px;left:2px;width:32px;height:32px;border-radius:50%;background:' + color + ';opacity:0.4;"></div>' : ''}}
        <div style="position:absolute;top:0;left:0;width:36px;height:36px;border-radius:50% 50% 50% 0;
            background:linear-gradient(135deg,${{color}},rgba(0,0,0,0.3));
            box-shadow:0 4px 15px rgba(0,0,0,0.3);
            display:flex;align-items:center;justify-content:center;
            transform:rotate(-45deg);">
            <span style="transform:rotate(45deg);font-size:14px;">✈️</span>
        </div>
    </div>`;

    var icon = L.divIcon({{
        html: markerHtml,
        iconSize: [36, 44],
        iconAnchor: [18, 44],
        popupAnchor: [0, -44],
        className: ''
    }});

    var statusColors = {{'AKTİF':'#34d399','YAKLAŞAN':'#38bdf8','TAMAMLANAN':'#6366f1'}};
    var sc = statusColors[status] || color;

    var popup = L.popup({{className:'custom-popup', maxWidth:240}})
        .setContent(`
        <div class="popup-inner">
            <div class="popup-city">📍 ${{city}}</div>
            <div class="popup-dates">${{dates}}</div>
            <span class="popup-status" style="background:${{sc}}22;color:${{sc}};">
                ${{status}}
            </span>
            <div class="popup-days">🕐 ${{days}} gün</div>
        </div>`);

    L.marker([lat, lng], {{icon: icon}})
        .addTo(map)
        .bindPopup(popup);
}}

{markers_js}

var hasMarkers = {'true' if markers_js.strip() else 'false'};
if (!hasMarkers) {{
    var noDataHtml = '<div style="position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);' +
        'background:rgba(255,255,255,0.92);border:none;border-radius:16px;' +
        'padding:24px 32px;text-align:center;color:#6b7194;font-family:sans-serif;box-shadow:0 8px 24px rgba(0,0,0,0.1);">' +
        '<div style="font-size:36px;margin-bottom:8px;">🗺️</div>' +
        '<div style="font-size:15px;font-weight:700;color:#2d3047;margin-bottom:4px;">Harita Boş</div>' +
        '<div style="font-size:13px;">Seyahat ekledikçe haritada görünür</div></div>';
    document.body.insertAdjacentHTML('beforeend', noDataHtml);
}}
</script>
</body>
</html>"""
        return html

    def _load_map_html(self):
        """Lazy load map after UI is ready"""
        if hasattr(self, 'map_view') and hasattr(self, '_map_seyahatler'):
            html = self._get_map_html(self._map_seyahatler)
            self.map_view.setHtml(html)

    def _open_map_in_browser(self):
        html = self._get_map_html(getattr(self, "_map_seyahatler", []))
        opened, _ = open_html_in_browser(html, "anasayfa-harita")
        if not opened:
            QMessageBox.warning(self, "Harita", "Harita varsayilan tarayicida acilamadi.")

    def _kart(self, s):
        card = QFrame()
        card.setFixedSize(190, 130)
        card.setCursor(Qt.PointingHandCursor)
        g = T.GRAD[hash(s.sehir) % len(T.GRAD)]
        hp = s.kapak_foto and os.path.exists(s.kapak_foto)
        dr = T.DURUM.get(s.durum(), T.TEXT3)
        if hp:
            card.setStyleSheet(
                f"QFrame{{background:{T.CARD};border:none;border-radius:18px;}}"
                f"QFrame:hover{{background:{T.CARD_H};}}")
        else:
            card.setStyleSheet(
                f"QFrame{{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,"
                f"stop:0 {g[0]},stop:1 {g[1]});border:none;border-radius:18px;}}")
        cl = QVBoxLayout(card); cl.setContentsMargins(14, 12, 14, 12); cl.setSpacing(2)
        tc = T.TEXT if hp else "white"
        tc2 = T.TEXT2 if hp else "rgba(255,255,255,0.7)"
        cl.addWidget(make_label(s.sehir, 15, True, tc))
        if s.ulke: cl.addWidget(make_label(f"📍 {s.ulke}", 10, color=tc2))
        cl.addStretch()
        cl.addWidget(make_label(f"📆 {s.baslangic_tarihi}", 10, color=tc2))
        br = QHBoxLayout()
        badge = QLabel(f" {s.durum().capitalize()} ")
        badge.setStyleSheet(f"background:{dr};color:white;border:none;border-radius:7px;"
                            "font-size:10px;font-weight:600;padding:2px 8px;")
        br.addWidget(badge); br.addStretch()
        if s.butce > 0: br.addWidget(make_label(f"₺{s.butce:,.0f}", 10, True, tc))
        cl.addLayout(br)
        shadow(card, 18, 0, 5, QColor(0, 0, 0, 55))
        # Clickable overlay button instead of mousePressEvent
        overlay = QPushButton(card)
        overlay.setGeometry(0, 0, 190, 130)
        overlay.setStyleSheet("QPushButton{background:transparent;border:none;}")
        overlay.setCursor(Qt.PointingHandCursor)
        sid = s.seyahat_id
        overlay.clicked.connect(lambda checked, _sid=sid: self.seyahat_detay.emit(_sid))
        return card

    def _cl(self, layout):
        while layout.count():
            it = layout.takeAt(0)
            if it.widget(): it.widget().deleteLater()
            elif it.layout(): self._cl(it.layout())


# ═══════════════════════════════════════════════════════════════════
#  SEYAHATLER
# ═══════════════════════════════════════════════════════════════════

class SeyahatlerSayfasi(QWidget):
    seyahat_detay = pyqtSignal(int)
    yeni_seyahat = pyqtSignal()

    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon; self.filtre = None
        self._bekleyen_arama = ""
        self._arama_timer = QTimer(self)
        self._arama_timer.setSingleShot(True)
        self._arama_timer.timeout.connect(self._arama_uygula)
        ml = QVBoxLayout(self); ml.setContentsMargins(32, 28, 32, 28); ml.setSpacing(16)
        h = QHBoxLayout()
        h.addWidget(make_label("✈️ Seyahatlerim", 24, True)); h.addStretch()
        self.arama = make_input("🔍 Seyahat ara...")
        self.arama.setFixedWidth(260); self.arama.setFixedHeight(42)
        self.arama.textChanged.connect(self._ara)
        h.addWidget(self.arama); h.addSpacing(10)
        yeni_btn = make_btn("Yeni Seyahat", True, "➕", h=42)
        yeni_btn.clicked.connect(self.yeni_seyahat.emit)
        h.addWidget(yeni_btn)
        ml.addLayout(h)

        fb = QHBoxLayout(); fb.setSpacing(8)
        self.fbtns = []
        for txt, f in [("Tümü", None), ("Yaklaşan", "yaklaşan"), ("Aktif", "aktif"), ("Geçmiş", "tamamlanan")]:
            b = QPushButton(txt); b.setFixedHeight(38); b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda c, ff=f: self._filtrele(ff))
            self.fbtns.append((b, f)); fb.addWidget(b)
        fb.addStretch(); ml.addLayout(fb)

        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gw = QWidget(); self.gl = QGridLayout(self.gw); self.gl.setSpacing(14)
        scroll.setWidget(self.gw); ml.addWidget(scroll)

    def yukle(self): self._fsil(); self._listele()

    def _filtrele(self, f): self.filtre = f; self._fsil(); self._listele()

    def _fsil(self):
        for b, f in self.fbtns:
            if f == self.filtre:
                b.setStyleSheet(f"QPushButton{{background:{T.PRIMARY};color:white;border:none;"
                              f"border-radius:10px;font-size:13px;font-weight:600;padding:0 20px;}}")
            else:
                hover = "#3f3f46" if T.AKTIF == "dark" else "#edf2f0"
                b.setStyleSheet(f"QPushButton{{background:{T.BG3};color:{T.TEXT2};border:none;"
                              f"border-radius:10px;font-size:13px;padding:0 20px;}}"
                              f"QPushButton:hover{{background:{hover};color:{T.TEXT};}}")

    def _ara(self, t):
        self._bekleyen_arama = t
        self._arama_timer.start(220)

    def _arama_uygula(self):
        self._listele(self._bekleyen_arama)

    def _listele(self, arama=""):
        while self.gl.count():
            it = self.gl.takeAt(0)
            if it.widget(): it.widget().deleteLater()
        if arama:
            from main import Seyahat
            rows = self.yon.db.seyahat_ara(self.yon.aktif_kullanici_id, arama)
            sl = [Seyahat(s["id"], s["kullanici_id"], s["sehir"], s["ulke"] or "",
                          s["baslangic_tarihi"], s["bitis_tarihi"], s["butce"] or 0,
                          s["seyahat_turu"] or "", s["notlar"] or "", s["kapak_foto"] or "") for s in rows]
        else:
            sl = self.yon.seyahatleri_listele(self.filtre)
        if not sl:
            self.gl.addWidget(make_label("Seyahat bulunamadı 🔍", 16, color=T.TEXT3), 0, 0, 1, 3,
                            Qt.AlignCenter); return
        col, row = 0, 0
        for s in sl:
            c = self._kart(s); self.gl.addWidget(c, row, col)
            col += 1
            if col >= 3: col = 0; row += 1

    def _kart(self, s):
        card = QFrame(); card.setFixedSize(310, 175); card.setCursor(Qt.PointingHandCursor)
        g = T.GRAD[hash(s.sehir) % len(T.GRAD)]
        hp = s.kapak_foto and os.path.exists(s.kapak_foto)
        dr = T.DURUM.get(s.durum(), T.TEXT3)
        if hp:
            card.setStyleSheet(f"QFrame{{background:{T.CARD};border:none;border-radius:16px;}}"
                              f"QFrame:hover{{background:{T.CARD_H};}}")
        else:
            card.setStyleSheet(f"QFrame{{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,"
                              f"stop:0 {g[0]},stop:1 {g[1]});border:none;border-radius:16px;}}")
        cl = QVBoxLayout(card); cl.setContentsMargins(18, 14, 18, 14); cl.setSpacing(6)
        tc = T.TEXT if hp else "white"; tc2 = T.TEXT2 if hp else "rgba(255,255,255,0.7)"
        tr = QHBoxLayout()
        tr.addWidget(make_label(s.sehir, 18, True, tc)); tr.addStretch()
        badge = QLabel(f" {s.durum().capitalize()} ")
        badge.setStyleSheet(f"background:{dr};color:white;border:none;border-radius:8px;"
                           f"font-size:10px;font-weight:600;padding:3px 10px;")
        tr.addWidget(badge); cl.addLayout(tr)
        if s.ulke: cl.addWidget(make_label(f"📍 {s.ulke}", 12, color=tc2))
        cl.addStretch()
        cl.addWidget(make_label(f"📆 {s.baslangic_tarihi} → {s.bitis_tarihi}", 11, color=tc2))
        br = QHBoxLayout()
        br.addWidget(make_label(f"🕐 {s.gun_sayisi()} gün", 11, color=tc2)); br.addStretch()
        if s.butce > 0: br.addWidget(make_label(f"💰 ₺{s.butce:,.0f}", 11, True, tc))
        cl.addLayout(br)
        shadow(card, 20, 0, 6, QColor(0, 0, 0, 50))
        overlay = QPushButton(card)
        overlay.setGeometry(0, 0, 310, 175)
        overlay.setStyleSheet("QPushButton{background:transparent;border:none;}")
        overlay.setCursor(Qt.PointingHandCursor)
        sid = s.seyahat_id
        overlay.clicked.connect(lambda checked, _sid=sid: self.seyahat_detay.emit(_sid))
        return card


# ═══════════════════════════════════════════════════════════════════
#  YENİ SEYAHAT
# ═══════════════════════════════════════════════════════════════════

class YeniSeyahatSayfasi(QWidget):
    olusturuldu = pyqtSignal(int)

    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon; self.kapak_path = ""
        ml = QVBoxLayout(self); ml.setContentsMargins(32, 28, 32, 28)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content = QWidget()
        lay = QVBoxLayout(content); lay.setSpacing(18); lay.setContentsMargins(0, 0, 20, 0)
        scroll.setWidget(content); ml.addWidget(scroll)

        lay.addWidget(make_label("✈️ Yeni Seyahat Oluştur", 24, True))
        lay.addWidget(make_label("Maceraya başlayın!", 13, color=T.TEXT2))
        lay.addSpacing(8)

        fc = make_card()
        fl = QVBoxLayout(fc); fl.setContentsMargins(28, 24, 28, 24); fl.setSpacing(12)

        from main import SeyahatAsistani

        fl.addWidget(make_label("🏙️ Şehir", 13, True))
        self.sehir_combo = QComboBox()
        self.sehir_combo.setEditable(True)
        self.sehir_combo.addItems(SeyahatAsistani.sehir_listesi())
        self.sehir_combo.setFixedHeight(46)
        fl.addWidget(self.sehir_combo)

        fl.addWidget(make_label("🌍 Ülke", 13, True))
        self.ulke_inp = make_input("Ülke adını girin")
        fl.addWidget(self.ulke_inp)

        tr = QHBoxLayout()
        for lbl, attr, delta in [("📅 Başlangıç", "bas_tarih", 0), ("📅 Bitiş", "bit_tarih", 5)]:
            vl = QVBoxLayout(); vl.addWidget(make_label(lbl, 13, True))
            de = QDateEdit(); de.setCalendarPopup(True)
            de.setDate(QDate.currentDate().addDays(delta)); de.setFixedHeight(46)
            setattr(self, attr, de); vl.addWidget(de); tr.addLayout(vl)
        fl.addLayout(tr)

        br = QHBoxLayout()
        bl = QVBoxLayout(); bl.addWidget(make_label("💰 Bütçe (₺)", 13, True))
        self.butce_inp = QDoubleSpinBox()
        self.butce_inp.setRange(0, 9999999); self.butce_inp.setValue(5000)
        self.butce_inp.setFixedHeight(46); self.butce_inp.setPrefix("₺ ")
        bl.addWidget(self.butce_inp); br.addLayout(bl)
        tl = QVBoxLayout(); tl.addWidget(make_label("🏷️ Tür", 13, True))
        self.tur_combo = QComboBox()
        self.tur_combo.addItems(["Tatil", "İş", "Kültür", "Macera", "Romantik", "Aile", "Solo", "Diğer"])
        self.tur_combo.setFixedHeight(46); tl.addWidget(self.tur_combo); br.addLayout(tl)
        fl.addLayout(br)

        fl.addWidget(make_label("📝 Notlar", 13, True))
        self.notlar_inp = QTextEdit()
        self.notlar_inp.setPlaceholderText("Seyahat notlarınız...")
        self.notlar_inp.setMaximumHeight(90)
        fl.addWidget(self.notlar_inp)

        fr = QHBoxLayout()
        fr.addWidget(make_label("📸 Kapak Fotoğrafı", 13, True)); fr.addStretch()
        self.foto_lbl = QLabel("Fotoğraf seçilmedi")
        self.foto_lbl.setStyleSheet(f"color:{T.TEXT3};font-size:12px;background:transparent;")
        fr.addWidget(self.foto_lbl)
        fb = make_btn("Seç", False, "📁", h=38); fb.clicked.connect(self._foto_sec)
        fr.addWidget(fb)
        fl.addLayout(fr)
        fl.addSpacing(8)

        bbr = QHBoxLayout(); bbr.addStretch()
        ai = make_btn("🤖 AI Plan", False, h=48); ai.clicked.connect(self._ai)
        bbr.addWidget(ai); bbr.addSpacing(10)
        kb = make_btn("Seyahat Oluştur", True, "✈️", h=48); kb.clicked.connect(self._kaydet)
        bbr.addWidget(kb)
        fl.addLayout(bbr)
        lay.addWidget(fc); lay.addStretch()

    def _foto_sec(self):
        p, _ = QFileDialog.getOpenFileName(self, "Kapak Fotoğrafı", "",
                                            "Resimler (*.png *.jpg *.jpeg *.bmp *.webp)")
        if p:
            self.kapak_path = p
            self.foto_lbl.setText(os.path.basename(p))
            self.foto_lbl.setStyleSheet(f"color:{T.EMERALD};font-size:12px;background:transparent;")

    def _kaydet(self):
        sh = self.sehir_combo.currentText().strip()
        if not sh: QMessageBox.warning(self, "Uyarı", "Şehir girin!"); return
        bas = self.bas_tarih.date().toString("yyyy-MM-dd")
        bit = self.bit_tarih.date().toString("yyyy-MM-dd")
        if bas > bit: QMessageBox.warning(self, "Uyarı", "Bitiş tarihi başlangıçtan önce olamaz!"); return
        sid = self.yon.seyahat_olustur(sh, self.ulke_inp.text().strip(), bas, bit,
            self.butce_inp.value(), self.tur_combo.currentText(),
            self.notlar_inp.toPlainText().strip(), self.kapak_path)
        if sid:
            QMessageBox.information(self, "Başarılı", f"{sh} seyahati oluşturuldu! ✈️")
            self.olusturuldu.emit(sid)
            self.sehir_combo.setCurrentIndex(0); self.ulke_inp.clear()
            self.notlar_inp.clear(); self.kapak_path = ""
            self.foto_lbl.setText("Fotoğraf seçilmedi")
            self.foto_lbl.setStyleSheet(f"color:{T.TEXT3};font-size:12px;background:transparent;")

    def _ai(self):
        sh = self.sehir_combo.currentText().strip()
        b = self.butce_inp.value()
        g = self.bas_tarih.date().daysTo(self.bit_tarih.date()) + 1
        if not sh or g < 1: QMessageBox.warning(self, "Uyarı", "Şehir ve tarih seçin!"); return
        AIAsistanDialog(self.yon, sh, b, g, self).exec_()


# ═══════════════════════════════════════════════════════════════════
#  SEYAHAT DETAY
# ═══════════════════════════════════════════════════════════════════

class SeyahatDetaySayfasi(QWidget):
    geri = pyqtSignal()

    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon; self.sid = None
        self._detay_cache = {}
        self._aktif_seyahat = None
        self._tab_builderleri = []
        self._tab_yuklendi = set()
        self.tabs = None
        self.ml = QVBoxLayout(self)
        self.ml.setContentsMargins(0, 0, 0, 0); self.ml.setSpacing(0)

    def yukle(self, sid):
        self.sid = sid
        s = self.yon.db.seyahat_getir(sid)
        if not s: return
        self._aktif_seyahat = s
        self._detay_cache_temizle()
        while self.ml.count():
            it = self.ml.takeAt(0)
            if it.widget(): it.widget().deleteLater()

        # Header
        hdr = QFrame(); hdr.setFixedHeight(76)
        hdr.setStyleSheet(f"QFrame{{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
                         f"stop:0 rgba(139,92,246,0.10),stop:1 rgba(217,70,239,0.05));"
                         f"border:none;}}")
        hl = QHBoxLayout(hdr); hl.setContentsMargins(24, 0, 24, 0)
        gb = QPushButton("← Geri"); gb.setCursor(Qt.PointingHandCursor)
        gb.setStyleSheet(f"QPushButton{{background:transparent;border:none;color:{T.PRIMARY_L};"
                        f"font-size:14px;font-weight:600;}}QPushButton:hover{{color:{T.TEXT};}}")
        gb.clicked.connect(self.geri.emit)
        hl.addWidget(gb); hl.addSpacing(16)
        hl.addWidget(make_label(f"✈️ {s['sehir']}", 22, True))
        if s['ulke']: hl.addWidget(make_label(f"📍 {s['ulke']}", 14, color=T.TEXT2))
        hl.addStretch()
        hl.addWidget(make_label(f"📆 {s['baslangic_tarihi']} → {s['bitis_tarihi']}", 13, color=T.TEXT2))
        hl.addSpacing(14)
        if s['butce']: hl.addWidget(make_label(f"💰 ₺{s['butce']:,.0f}", 14, True, T.EMERALD))
        hl.addSpacing(10)
        db = make_btn("Sil", False, "🗑️", h=36)
        db.clicked.connect(lambda: self._sil(sid))
        hl.addWidget(db)
        self.ml.addWidget(hdr)

        self.tabs = QTabWidget()
        self._tab_builderleri = [
            lambda s=s: self._genel(s),
            self._konaklama,
            self._aktivite,
            lambda s=s: self._butce(s),
            self._plan,
            lambda s=s: self._takvim(s),
            lambda s=s: self._harita(s),
            self._arkadas,
            self._ucus,
            lambda s=s: self._notlar(s),
        ]
        self._tab_yuklendi = set()
        for etiket in [
            "📋 Genel",
            "🏨 Konaklama",
            "🎯 Aktiviteler",
            "💰 Bütçe",
            "📅 Plan",
            "🗓️ Takvim",
            "🗺️ Harita",
            "👥 Arkadaşlar",
            "✈️ Uçuşlar",
            "📝 Notlar",
        ]:
            sayfa = QWidget()
            sayfa_lay = QVBoxLayout(sayfa)
            sayfa_lay.setContentsMargins(0, 0, 0, 0)
            sayfa_lay.setSpacing(0)
            self.tabs.addTab(sayfa, etiket)
        self.tabs.currentChanged.connect(self._detay_tabini_yukle)
        self.ml.addWidget(self.tabs)
        self._detay_tabini_yukle(0)

    # ── Genel ─────────────────────────────────────────────────────
    def _detay_tabini_yukle(self, idx):
        if idx < 0 or idx in self._tab_yuklendi or idx >= len(self._tab_builderleri):
            return
        sayfa = self.tabs.widget(idx)
        if not sayfa:
            return
        sayfa_lay = sayfa.layout()
        if sayfa_lay is None:
            sayfa_lay = QVBoxLayout(sayfa)
            sayfa_lay.setContentsMargins(0, 0, 0, 0)
            sayfa_lay.setSpacing(0)
        sayfa_lay.addWidget(self._tab_builderleri[idx]())
        self._tab_yuklendi.add(idx)

    def _detay_cache_temizle(self):
        self._detay_cache = {}

    def _cacheli_veri(self, anahtar, yukleyici):
        if anahtar not in self._detay_cache:
            self._detay_cache[anahtar] = yukleyici()
        return self._detay_cache[anahtar]

    def _konaklama_verileri(self):
        return self._cacheli_veri("konaklamalar", lambda: self.yon.db.konaklamalari_getir(self.sid))

    def _aktivite_verileri(self):
        return self._cacheli_veri("aktiviteler", lambda: self.yon.db.aktiviteleri_getir(self.sid))

    def _harcama_verileri(self):
        return self._cacheli_veri("harcamalar", lambda: self.yon.db.harcamalari_getir(self.sid))

    def _plan_verileri(self):
        return self._cacheli_veri("planlar", lambda: self.yon.db.planlari_getir(self.sid))

    def _arkadas_verileri(self):
        return self._cacheli_veri("arkadaslar", lambda: self.yon.db.arkadaslari_getir(self.sid))

    def _ucus_verileri(self):
        return self._cacheli_veri("ucuslar", lambda: self.yon.db.ucuslari_getir(self.sid))

    def _butce_ozeti(self):
        return self._cacheli_veri("butce", lambda: self.yon.butce_durumu(self.sid))

    def _genel(self, s):
        w = QWidget(); scroll = QScrollArea(); scroll.setWidgetResizable(True)
        c = QWidget(); lay = QVBoxLayout(c); lay.setContentsMargins(24, 20, 24, 20); lay.setSpacing(16)
        scroll.setWidget(c); wl = QVBoxLayout(w); wl.setContentsMargins(0, 0, 0, 0); wl.addWidget(scroll)

        hava = self.yon.hava_durumu_getir(s['sehir'])
        hc = QFrame(); hc.setFixedHeight(100)
        hc.setStyleSheet(f"QFrame{{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
                        f"stop:0 rgba(34,211,238,0.10),stop:1 rgba(56,189,248,0.05));"
                        f"border:none;border-radius:16px;}}")
        shadow(hc, 18, 0, 5, QColor(0, 0, 0, 40))
        hcl = QHBoxLayout(hc); hcl.setContentsMargins(20, 12, 20, 12)
        hcl.addWidget(make_label(hava.get("ikon", "🌤️"), 42)); hcl.addSpacing(12)
        vl = QVBoxLayout()
        vl.addWidget(make_label("Hava Durumu", 14, True))
        vl.addWidget(make_label(hava.get("durum", ""), 12, color=T.TEXT2))
        hcl.addLayout(vl); hcl.addStretch()
        vr = QVBoxLayout(); vr.setAlignment(Qt.AlignRight)
        vr.addWidget(make_label(f"{hava.get('sicaklik', '--')}°C", 26, True, T.CYAN))
        hr = QHBoxLayout()
        hr.addWidget(make_label(f"💧 %{hava.get('nem', '--')}", 11, color=T.TEXT2))
        hr.addSpacing(8)
        hr.addWidget(make_label(f"💨 {hava.get('ruzgar', '--')} km/h", 11, color=T.TEXT2))
        vr.addLayout(hr); hcl.addLayout(vr)
        lay.addWidget(hc)

        ic = make_card()
        icl = QGridLayout(ic); icl.setContentsMargins(20, 16, 20, 16); icl.setSpacing(14)
        infos = [("🏙️ Şehir", s["sehir"]), ("🌍 Ülke", s["ulke"] or "—"),
                 ("📅 Başlangıç", s["baslangic_tarihi"]), ("📅 Bitiş", s["bitis_tarihi"]),
                 ("💰 Bütçe", f"₺{s['butce']:,.0f}" if s["butce"] else "—"),
                 ("🏷️ Tür", s["seyahat_turu"] or "—")]
        for i, (l, v) in enumerate(infos):
            r2, c2 = divmod(i, 3)
            vl2 = QVBoxLayout()
            vl2.addWidget(make_label(l, 11, color=T.TEXT3))
            vl2.addWidget(make_label(str(v), 14, True))
            icl.addLayout(vl2, r2, c2)
        lay.addWidget(ic)

        kn = self._konaklama_verileri()
        ak = self._aktivite_verileri()
        th = self.yon.db.harcama_toplam(self.sid)
        ar = self._arkadas_verileri()
        stats = [("🏨", "Konaklama", str(len(kn)), T.SKY), ("🎯", "Aktivite", str(len(ak)), T.EMERALD),
                 ("💰", "Harcama", f"₺{th:,.0f}", T.AMBER), ("👥", "Arkadaş", str(len(ar)), T.PINK)]
        sw = QWidget(); sr = QHBoxLayout(sw); sr.setSpacing(12); sr.setContentsMargins(0, 0, 0, 0)
        for ik, bs, vl3, rn in stats:
            sc = make_card(); sc.setFixedHeight(85)
            scl = QHBoxLayout(sc); scl.setContentsMargins(14, 10, 14, 10)
            scl.addWidget(make_label(ik, 26))
            svl = QVBoxLayout()
            svl.addWidget(make_label(bs, 11, color=T.TEXT3))
            svl.addWidget(make_label(vl3, 18, True, rn))
            scl.addLayout(svl); sr.addWidget(sc)
        lay.addWidget(sw); lay.addStretch()
        return w

    # ── Konaklama ─────────────────────────────────────────────────
    def _konaklama(self):
        w = QWidget(); wl = QVBoxLayout(w); wl.setContentsMargins(24, 20, 24, 20); wl.setSpacing(12)
        h = QHBoxLayout(); h.addWidget(make_label("🏨 Konaklamalar", 18, True)); h.addStretch()
        eb = make_btn("Ekle", True, "➕", h=38); eb.clicked.connect(lambda: self._kon_ekle_dlg(wl))
        h.addWidget(eb); wl.addLayout(h)
        self._kon_liste(wl); return w

    def _kon_liste(self, lay):
        for i in reversed(range(lay.count())):
            it = lay.itemAt(i)
            if it.widget() and it.widget().property("t") == "k": it.widget().deleteLater()
        konaklamalar = self._konaklama_verileri()
        for k in konaklamalar:
            c = make_card(); c.setProperty("t", "k"); c.setFixedHeight(110)
            cl = QHBoxLayout(c); cl.setContentsMargins(18, 12, 18, 12)
            left = QVBoxLayout()
            tr = QHBoxLayout(); tr.addWidget(make_label(k["otel_adi"], 16, True))
            y = "⭐" * (k["yildiz"] or 0)
            if y: tr.addWidget(make_label(y, 12))
            tr.addStretch(); left.addLayout(tr)
            left.addWidget(make_label(f"📍 {k['konum']}" if k['konum'] else "📍 —", 12, color=T.TEXT2))
            left.addWidget(make_label(f"📅 {k['giris_tarihi']} → {k['cikis_tarihi']}", 12, color=T.TEXT2))
            cl.addLayout(left, 1)
            right = QVBoxLayout(); right.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            right.addWidget(make_label(f"₺{k['fiyat']:,.0f}", 18, True, T.EMERALD))
            sb = QPushButton("🗑️"); sb.setCursor(Qt.PointingHandCursor); sb.setFixedSize(30, 30)
            sb.setStyleSheet("QPushButton{background:rgba(251,113,133,0.08);border:none;border-radius:8px;font-size:14px;}"
                            "QPushButton:hover{background:rgba(251,113,133,0.18);}")
            sb.clicked.connect(lambda _, kid=k["id"]: (
                self.yon.db.konaklama_sil(kid),
                self._detay_cache_temizle(),
                self._kon_liste(lay)
            ))
            right.addWidget(sb, alignment=Qt.AlignRight)
            cl.addLayout(right); lay.addWidget(c)
        if not konaklamalar:
            l = make_label("Henüz konaklama eklenmedi", 14, color=T.TEXT3)
            l.setProperty("t", "k"); l.setAlignment(Qt.AlignCenter); lay.addWidget(l)

    def _kon_ekle_dlg(self, lay):
        d = QDialog(self); d.setWindowTitle("Konaklama Ekle"); d.setFixedSize(420, 480)
        dl = QVBoxLayout(d); dl.setSpacing(10); dl.setContentsMargins(24, 20, 24, 20)
        dl.addWidget(make_label("🏨 Yeni Konaklama", 18, True)); dl.addSpacing(6)
        fields = {}
        for lbl, key, ph in [("Otel Adı", "otel", "Otel adı"), ("Konum", "konum", "Konum/Adres")]:
            dl.addWidget(make_label(lbl, 12, color=T.TEXT2))
            inp = make_input(ph); fields[key] = inp; dl.addWidget(inp)
        tr = QHBoxLayout()
        for lbl, key in [("Giriş", "giris"), ("Çıkış", "cikis")]:
            vl = QVBoxLayout(); vl.addWidget(make_label(lbl, 12, color=T.TEXT2))
            de = QDateEdit(); de.setCalendarPopup(True); de.setDate(QDate.currentDate()); de.setFixedHeight(42)
            fields[key] = de; vl.addWidget(de); tr.addLayout(vl)
        dl.addLayout(tr)
        fr = QHBoxLayout()
        vl = QVBoxLayout(); vl.addWidget(make_label("Fiyat ₺", 12, color=T.TEXT2))
        fi = QDoubleSpinBox(); fi.setRange(0, 999999); fi.setFixedHeight(42); fi.setPrefix("₺ ")
        fields["fiyat"] = fi; vl.addWidget(fi); fr.addLayout(vl)
        vl2 = QVBoxLayout(); vl2.addWidget(make_label("Yıldız", 12, color=T.TEXT2))
        yi = QSpinBox(); yi.setRange(1, 5); yi.setValue(3); yi.setFixedHeight(42)
        fields["yildiz"] = yi; vl2.addWidget(yi); fr.addLayout(vl2)
        dl.addLayout(fr)
        dl.addStretch()
        btn = make_btn("Ekle", True, "✓", h=46)
        def ekle():
            if not fields["otel"].text().strip(): QMessageBox.warning(d, "Uyarı", "Otel adı gerekli!"); return
            self.yon.db.konaklama_ekle(self.sid, fields["otel"].text().strip(), fields["konum"].text().strip(),
                fields["giris"].date().toString("yyyy-MM-dd"), fields["cikis"].date().toString("yyyy-MM-dd"),
                fields["fiyat"].value(), fields["yildiz"].value()); d.accept(); self._detay_cache_temizle(); self._kon_liste(lay)
        btn.clicked.connect(ekle); dl.addWidget(btn); d.exec_()

    # ── Aktivite ──────────────────────────────────────────────────
    def _scroll_wrap(self):
        w = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        c = QWidget()
        lay = QVBoxLayout(c)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(12)
        scroll.setWidget(c)
        wl = QVBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(scroll)
        return w, lay

    def _kaynak_badge(self, metin, renk):
        lbl = QLabel(f"  {metin}  ")
        lbl.setStyleSheet(
            f"background:{renk};color:white;border:none;border-radius:9px;"
            "font-size:10px;font-weight:700;padding:3px 8px;"
        )
        return lbl

    def _plan_tarihi(self, kayit):
        return kayit["tarih"] if "tarih" in kayit.keys() and kayit["tarih"] else kayit["gun"]

    def _plan_baslik_tarihi(self, tarih_str):
        tarih = QDate.fromString(tarih_str, "yyyy-MM-dd")
        return tarih.toString("dd MMMM yyyy") if tarih.isValid() else (tarih_str or "Belirsiz gün")

    def _seyahat_gunleri(self, s):
        gunler = []
        bas = QDate.fromString(s["baslangic_tarihi"], "yyyy-MM-dd")
        bit = QDate.fromString(s["bitis_tarihi"], "yyyy-MM-dd")
        if not bas.isValid() or not bit.isValid():
            return gunler
        tarih = bas
        while tarih <= bit:
            gunler.append(tarih.toString("yyyy-MM-dd"))
            tarih = tarih.addDays(1)
        return gunler

    def _takvim_ogeleri(self):
        ogeler = {}
        for p in self._plan_verileri():
            tarih = p["tarih"] if "tarih" in p.keys() and p["tarih"] else p["gun"]
            if not tarih:
                continue
            ogeler.setdefault(tarih, []).append({
                "tur": "plan",
                "kaynak": p["kaynak"] if "kaynak" in p.keys() else "manuel",
                "saat": p["saat"] or "",
                "baslik": p["baslik"] or "Plan",
                "aciklama": p["aciklama"] or "",
                "konum": p["konum"] or "",
                "fiyat": 0,
            })
        for a in self._aktivite_verileri():
            tarih = a["tarih"] or ""
            if not tarih:
                continue
            ogeler.setdefault(tarih, []).append({
                "tur": "aktivite",
                "kaynak": a["kaynak"] if "kaynak" in a.keys() else "manuel",
                "saat": a["saat"] or "",
                "baslik": a["aktivite_adi"] or "Aktivite",
                "aciklama": a["aciklama"] or "",
                "konum": a["konum"] or "",
                "fiyat": a["fiyat"] or 0,
            })
        for tarih in ogeler:
            ogeler[tarih].sort(key=lambda x: (x["saat"] or "23:59", x["tur"]))
        return ogeler

    def _aktivite(self):
        w, wl = self._scroll_wrap()
        h = QHBoxLayout()
        h.addWidget(make_label("🎯 Aktiviteler", 18, True))
        h.addStretch()
        h.addWidget(self._kaynak_badge("AI + Manuel", T.PRIMARY))
        eb = make_btn("Aktivite Ekle", True, "➕", h=38)
        eb.clicked.connect(lambda: self._akt_ekle_dlg(wl))
        h.addWidget(eb)
        wl.addLayout(h)
        self._akt_liste(wl)
        return w
        w = QWidget(); wl = QVBoxLayout(w); wl.setContentsMargins(24, 20, 24, 20); wl.setSpacing(12)
        h = QHBoxLayout(); h.addWidget(make_label("🎯 Aktiviteler", 18, True)); h.addStretch()
        eb = make_btn("Ekle", True, "➕", h=38); eb.clicked.connect(lambda: self._akt_ekle_dlg(wl))
        h.addWidget(eb); wl.addLayout(h)
        self._akt_liste(wl); return w

    def _akt_liste(self, lay):
        for i in reversed(range(lay.count())):
            it = lay.itemAt(i)
            if it.widget() and it.widget().property("t") == "a":
                it.widget().deleteLater()

        aktiviteler = self._aktivite_verileri()
        if not aktiviteler:
            bos = make_card()
            bos.setProperty("t", "a")
            bl = QVBoxLayout(bos)
            bl.setContentsMargins(18, 18, 18, 18)
            bl.addWidget(make_label("Takvimde görünecek bir aktivite henüz eklenmedi.", 14, False, T.TEXT2))
            lay.addWidget(bos)
            return

        for a in aktiviteler:
            c = make_card()
            c.setProperty("t", "a")
            cl = QHBoxLayout(c)
            cl.setContentsMargins(16, 14, 16, 14)
            sol = QVBoxLayout()
            ust = QHBoxLayout()
            ust.addWidget(make_label(a["aktivite_adi"], 15, True))
            ust.addSpacing(6)
            kaynak = a["kaynak"] if "kaynak" in a.keys() else "manuel"
            ust.addWidget(self._kaynak_badge("AI" if kaynak == "ai" else "MANUEL", T.PRIMARY if kaynak == "ai" else T.SKY))
            ust.addStretch()
            sol.addLayout(ust)

            bilgiler = []
            if a["tarih"]:
                bilgiler.append(f"📅 {self._plan_baslik_tarihi(a['tarih'])}")
            if a["saat"]:
                bilgiler.append(f"🕐 {a['saat']}")
            if a["konum"]:
                bilgiler.append(f"📍 {a['konum']}")
            if bilgiler:
                sol.addWidget(make_label("  ".join(bilgiler), 12, False, T.TEXT2))
            if a["aciklama"]:
                sol.addWidget(make_label(a["aciklama"], 12, False, T.TEXT3))
            cl.addLayout(sol, 1)

            sag = QVBoxLayout()
            sag.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if a["fiyat"] > 0:
                sag.addWidget(make_label(f"₺{a['fiyat']:,.0f}", 14, True, T.AMBER))
            sil = QPushButton("✕")
            sil.setCursor(Qt.PointingHandCursor)
            sil.setFixedSize(26, 26)
            sil.setStyleSheet("QPushButton{background:transparent;border:none;color:#94a3b8;font-size:14px;}"
                              "QPushButton:hover{color:#fb7185;}")
            sil.clicked.connect(lambda _, aid=a["id"]: (
                self.yon.db.aktivite_sil(aid),
                self._detay_cache_temizle(),
                self._akt_liste(lay)
            ))
            sag.addWidget(sil, alignment=Qt.AlignRight)
            cl.addLayout(sag)
            lay.addWidget(c)
        return
        for i in reversed(range(lay.count())):
            it = lay.itemAt(i)
            if it.widget() and it.widget().property("t") == "a": it.widget().deleteLater()
        colors = [T.PRIMARY, T.CYAN, T.EMERALD, T.AMBER, T.PINK, T.SKY, T.ORANGE]
        for j, a in enumerate(self._aktivite_verileri()):
            c = make_card(); c.setProperty("t", "a"); c.setFixedHeight(85)
            cl = QHBoxLayout(c); cl.setContentsMargins(16, 10, 16, 10)
            dot = QFrame(); dot.setFixedSize(4, 55)
            dot.setStyleSheet(f"background:{colors[j % len(colors)]};border:none;border-radius:2px;")
            cl.addWidget(dot); cl.addSpacing(12)
            left = QVBoxLayout()
            left.addWidget(make_label(a["aktivite_adi"], 15, True))
            info_parts = []
            if a['tarih']: info_parts.append(f"📅 {a['tarih']}")
            if a['saat']: info_parts.append(f"🕐 {a['saat']}")
            if a['konum']: info_parts.append(f"📍 {a['konum']}")
            if info_parts: left.addWidget(make_label("  ".join(info_parts), 12, color=T.TEXT2))
            cl.addLayout(left, 1)
            right = QVBoxLayout(); right.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if a['fiyat'] > 0: right.addWidget(make_label(f"₺{a['fiyat']:,.0f}", 14, True, T.AMBER))
            sb = QPushButton("✕"); sb.setCursor(Qt.PointingHandCursor); sb.setFixedSize(26, 26)
            sb.setStyleSheet("QPushButton{background:transparent;border:none;color:#52525b;font-size:14px;}"
                            "QPushButton:hover{color:#fb7185;}")
            sb.clicked.connect(lambda _, aid=a["id"]: (self.yon.db.aktivite_sil(aid), self._akt_liste(lay)))
            right.addWidget(sb, alignment=Qt.AlignRight); cl.addLayout(right); lay.addWidget(c)
        if not aktiviteler:
            l = make_label("Henüz aktivite eklenmedi", 14, color=T.TEXT3)
            l.setProperty("t", "a"); l.setAlignment(Qt.AlignCenter); lay.addWidget(l)

    def _akt_ekle_dlg(self, lay):
        d = QDialog(self); d.setWindowTitle("Aktivite Ekle"); d.setFixedSize(420, 480)
        dl = QVBoxLayout(d); dl.setSpacing(10); dl.setContentsMargins(24, 20, 24, 20)
        dl.addWidget(make_label("🎯 Yeni Aktivite", 18, True)); dl.addSpacing(4)
        dl.addWidget(make_label("Aktivite Adı", 12, color=T.TEXT2))
        ad = make_input("Aktivite adı"); dl.addWidget(ad)
        tr = QHBoxLayout()
        vl = QVBoxLayout(); vl.addWidget(make_label("Tarih", 12, color=T.TEXT2))
        td = QDateEdit(); td.setCalendarPopup(True); td.setDate(QDate.currentDate()); td.setFixedHeight(42)
        vl.addWidget(td); tr.addLayout(vl)
        vl2 = QVBoxLayout(); vl2.addWidget(make_label("Saat", 12, color=T.TEXT2))
        st = QTimeEdit(); st.setTime(QTime(10, 0)); st.setFixedHeight(42)
        vl2.addWidget(st); tr.addLayout(vl2); dl.addLayout(tr)
        dl.addWidget(make_label("Konum", 12, color=T.TEXT2))
        kon = make_input("Konum"); dl.addWidget(kon)
        dl.addWidget(make_label("Fiyat ₺", 12, color=T.TEXT2))
        fi = QDoubleSpinBox(); fi.setRange(0, 999999); fi.setFixedHeight(42); fi.setPrefix("₺ ")
        dl.addWidget(fi)
        dl.addWidget(make_label("Açıklama", 12, color=T.TEXT2))
        ac = make_input("Opsiyonel"); dl.addWidget(ac)
        dl.addStretch()
        btn = make_btn("Ekle", True, "✓", h=46)
        def ekle():
            if not ad.text().strip(): QMessageBox.warning(d, "Uyarı", "Ad gerekli!"); return
            self.yon.db.aktivite_ekle(self.sid, ad.text().strip(), td.date().toString("yyyy-MM-dd"),
                st.time().toString("HH:mm"), kon.text().strip(), fi.value(), ac.text().strip())
            d.accept(); self._detay_cache_temizle(); self._akt_liste(lay)
        btn.clicked.connect(ekle); dl.addWidget(btn); d.exec_()

    # ── Bütçe ─────────────────────────────────────────────────────
    def _butce(self, s):
        w = QWidget(); scroll = QScrollArea(); scroll.setWidgetResizable(True)
        c = QWidget(); lay = QVBoxLayout(c); lay.setContentsMargins(24, 20, 24, 20); lay.setSpacing(14)
        scroll.setWidget(c); wl = QVBoxLayout(w); wl.setContentsMargins(0, 0, 0, 0); wl.addWidget(scroll)

        h = QHBoxLayout(); h.addWidget(make_label("💰 Bütçe & Harcamalar", 18, True)); h.addStretch()
        eb = make_btn("Harcama Ekle", True, "➕", h=38)
        eb.clicked.connect(lambda: self._harc_ekle_dlg(lay)); h.addWidget(eb); lay.addLayout(h)

        dur = self._butce_ozeti()
        if dur:
            ow = QWidget(); orl = QHBoxLayout(ow); orl.setSpacing(12); orl.setContentsMargins(0, 0, 0, 0)
            for ik, lb, vl, rn in [("💰", "Bütçe", f"₺{dur['butce']:,.0f}", T.SKY),
                                    ("🧾", "Harcama", f"₺{dur['toplam_harcama']:,.0f}", T.AMBER),
                                    ("💵", "Kalan", f"₺{dur['kalan']:,.0f}",
                                     T.EMERALD if dur['kalan'] >= 0 else T.ROSE)]:
                sc = make_card(); sc.setFixedHeight(85)
                scl = QHBoxLayout(sc); scl.setContentsMargins(14, 10, 14, 10)
                scl.addWidget(make_label(ik, 26)); svl = QVBoxLayout()
                svl.addWidget(make_label(lb, 11, color=T.TEXT3))
                svl.addWidget(make_label(vl, 18, True, rn)); scl.addLayout(svl); orl.addWidget(sc)
            lay.addWidget(ow)

            if dur['butce'] > 0:
                pb = QProgressBar(); pb.setMaximum(100); pb.setValue(min(int(dur['yuzde']), 100))
                pb.setFixedHeight(10)
                if dur['yuzde'] > 90:
                    pb.setStyleSheet(f"QProgressBar{{background:{T.BG3};border:none;border-radius:5px;}}"
                                    f"QProgressBar::chunk{{border-radius:5px;background:{T.ROSE};}}")
                lay.addWidget(pb)
                lay.addWidget(make_label(f"Bütçenin %{dur['yuzde']:.1f}'i kullanıldı", 12, color=T.TEXT2))

            if dur['kategori_dagilim']:
                crw = QHBoxLayout(); crw.setSpacing(18)
                cd = [(k["kategori"], k["toplam"], T.KAT.get(k["kategori"], "#71717a"))
                      for k in dur['kategori_dagilim']]
                chart = DonutChart(cd); crw.addWidget(chart)
                kc = make_card(); kcl = QVBoxLayout(kc); kcl.setContentsMargins(16, 12, 16, 12)
                kcl.addWidget(make_label("Kategori Dağılımı", 14, True)); kcl.addSpacing(4)
                for kt in dur['kategori_dagilim']:
                    kr = QHBoxLayout()
                    dot = QFrame(); dot.setFixedSize(10, 10)
                    rn = T.KAT.get(kt["kategori"], "#71717a")
                    dot.setStyleSheet(f"background:{rn};border:none;border-radius:5px;")
                    kr.addWidget(dot); kr.addWidget(make_label(kt["kategori"], 13)); kr.addStretch()
                    kr.addWidget(make_label(f"₺{kt['toplam']:,.0f}", 13, True, rn)); kcl.addLayout(kr)
                kcl.addStretch(); crw.addWidget(kc, 1)
                cw = QWidget(); cw.setLayout(crw); lay.addWidget(cw)

        lay.addWidget(make_label("📋 Harcama Listesi", 16, True))
        harc = self._harcama_verileri()
        if harc:
            tbl = QTableWidget(); tbl.setColumnCount(5)
            tbl.setHorizontalHeaderLabels(["Kategori", "Tutar", "Açıklama", "Tarih", ""])
            tbl.setRowCount(len(harc)); tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tbl.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed); tbl.setColumnWidth(4, 50)
            tbl.verticalHeader().setVisible(False)
            tbl.setShowGrid(False)
            tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
            tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
            for row, hr in enumerate(harc):
                kr = T.KAT.get(hr["kategori"], "#71717a")
                ki = QTableWidgetItem(f"  {hr['kategori']}"); ki.setForeground(QColor(kr))
                tbl.setItem(row, 0, ki)
                tbl.setItem(row, 1, QTableWidgetItem(f"₺{hr['tutar']:,.0f}"))
                tbl.setItem(row, 2, QTableWidgetItem(hr["aciklama"] or "—"))
                tbl.setItem(row, 3, QTableWidgetItem(hr["tarih"] or "—"))
                sb = QPushButton("🗑️"); sb.setCursor(Qt.PointingHandCursor)
                sb.setStyleSheet("QPushButton{background:transparent;border:none;font-size:14px;}"
                                "QPushButton:hover{background:rgba(251,113,133,0.12);border-radius:4px;}")
                sb.clicked.connect(lambda _, hid=hr["id"]: (self.yon.db.harcama_sil(hid), self.yukle(self.sid)))
                tbl.setCellWidget(row, 4, sb); tbl.setRowHeight(row, 44)
            lay.addWidget(tbl)
        else:
            lay.addWidget(make_label("Henüz harcama yok", 13, color=T.TEXT3))
        lay.addStretch(); return w

    def _harc_ekle_dlg(self, lay):
        d = QDialog(self); d.setWindowTitle("Harcama Ekle"); d.setFixedSize(400, 400)
        dl = QVBoxLayout(d); dl.setSpacing(10); dl.setContentsMargins(24, 20, 24, 20)
        dl.addWidget(make_label("💰 Yeni Harcama", 18, True))
        dl.addWidget(make_label("Kategori", 12, color=T.TEXT2))
        kc = QComboBox()
        kc.addItems(["Yemek", "Ulaşım", "Alışveriş", "Eğlence", "Konaklama", "Aktivite", "Diğer"])
        kc.setFixedHeight(42); dl.addWidget(kc)
        dl.addWidget(make_label("Tutar ₺", 12, color=T.TEXT2))
        ti = QDoubleSpinBox(); ti.setRange(0, 999999); ti.setFixedHeight(42); ti.setPrefix("₺ "); dl.addWidget(ti)
        dl.addWidget(make_label("Açıklama", 12, color=T.TEXT2))
        ai = make_input("Opsiyonel"); dl.addWidget(ai)
        dl.addWidget(make_label("Tarih", 12, color=T.TEXT2))
        td = QDateEdit(); td.setCalendarPopup(True); td.setDate(QDate.currentDate()); td.setFixedHeight(42)
        dl.addWidget(td); dl.addStretch()
        btn = make_btn("Ekle", True, "✓", h=46)
        def ekle():
            if ti.value() <= 0: QMessageBox.warning(d, "Uyarı", "Tutar > 0 olmalı!"); return
            self.yon.db.harcama_ekle(self.sid, kc.currentText(), ti.value(), ai.text().strip(),
                td.date().toString("yyyy-MM-dd")); d.accept(); self.yukle(self.sid)
        btn.clicked.connect(ekle); dl.addWidget(btn); d.exec_()

    # ── Plan ──────────────────────────────────────────────────────
    def _ai_plan_ac(self):
        s = self.yon.db.seyahat_getir(self.sid)
        if not s:
            return
        gun = max(1, QDate.fromString(s["baslangic_tarihi"], "yyyy-MM-dd").daysTo(
            QDate.fromString(s["bitis_tarihi"], "yyyy-MM-dd")
        ) + 1)
        dlg = AIAsistanDialog(self.yon, s["sehir"], s["butce"] or 5000, gun, self)
        if dlg.exec_():
            self.yukle(self.sid)

    def _plan(self):
        w, wl = self._scroll_wrap()
        h = QHBoxLayout()
        h.addWidget(make_label("📅 Plan Akışı", 18, True))
        h.addStretch()
        ai_btn = make_btn("AI Plan", False, "🤖", h=38)
        ai_btn.clicked.connect(self._ai_plan_ac)
        ekle_btn = make_btn("Plan Ekle", True, "➕", h=38)
        ekle_btn.clicked.connect(lambda: self._plan_ekle_dlg(wl))
        h.addWidget(ai_btn)
        h.addWidget(ekle_btn)
        wl.addLayout(h)
        self._plan_liste(wl)
        return w
        w = QWidget(); wl = QVBoxLayout(w); wl.setContentsMargins(24, 20, 24, 20); wl.setSpacing(12)
        h = QHBoxLayout(); h.addWidget(make_label("📅 Günlük Plan", 18, True)); h.addStretch()
        eb = make_btn("Plan Ekle", True, "➕", h=38)
        eb.clicked.connect(lambda: self._plan_ekle_dlg(wl))
        h.addWidget(eb); wl.addLayout(h)
        self._plan_liste(wl); return w

    def _plan_liste(self, lay):
        for i in reversed(range(lay.count())):
            it = lay.itemAt(i)
            if it.widget() and it.widget().property("t") == "p":
                widget = it.widget()
                lay.removeWidget(widget)
                widget.deleteLater()
            elif it.spacerItem():
                lay.takeAt(i)

        planlar = self._plan_verileri()
        if not planlar:
            bos = QFrame()
            bos.setProperty("t", "p")
            bos.setFixedHeight(126)
            bos.setStyleSheet(f"""
                QFrame {{
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 {alpha_color(T.PRIMARY, 0.10)},
                        stop:1 {alpha_color(T.CYAN, 0.05)});
                    border-radius: 20px;
                }}
            """)
            bl = QVBoxLayout(bos)
            bl.setContentsMargins(20, 18, 20, 18)
            bl.setAlignment(Qt.AlignCenter)
            bl.setSpacing(6)
            bl.addWidget(make_label("📅", 30))
            bl.addWidget(make_label("Henüz plan yok", 15, True))
            bl.addWidget(make_label("AI ile tek tıkla daha düzenli bir akış oluşturabilirsiniz.", 12, False, T.TEXT2))
            lay.addWidget(bos)
            return

        KAT_ICONS = {
            "Ulaşım": ("🚗", T.SKY), "Yemek": ("🍽️", T.AMBER),
            "Konaklama": ("🏨", T.PRIMARY_L), "Hatırlatma": ("⏰", T.ROSE),
            "Müze": ("🏛️", T.ORANGE), "Aktivite": ("🎯", T.EMERALD),
            "Genel": ("📌", T.CYAN), "Plan": ("📋", T.INDIGO),
        }

        gunler = {}
        for p in planlar:
            tarih = self._plan_tarihi(p) or "Belirsiz gün"
            gunler.setdefault(tarih, []).append(p)

        for tarih, items in sorted(gunler.items()):
            day_header = QFrame()
            day_header.setProperty("t", "p")
            day_header.setFixedHeight(54)
            day_header.setStyleSheet(f"""
                QFrame {{
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                        stop:0 {alpha_color(T.PRIMARY, 0.12)},
                        stop:1 {alpha_color(T.CYAN, 0.03)});
                    border-radius: 16px;
                }}
            """)
            dhl = QHBoxLayout(day_header)
            dhl.setContentsMargins(14, 10, 14, 10)
            dhl.setSpacing(10)
            icon_chip = QLabel("📆")
            icon_chip.setFixedSize(32, 32)
            icon_chip.setAlignment(Qt.AlignCenter)
            icon_chip.setStyleSheet(
                f"background:{alpha_color(T.PRIMARY, 0.14)};"
                "border-radius:10px;font-size:15px;"
            )
            dhl.addWidget(icon_chip)

            baslik_kolonu = QVBoxLayout()
            baslik_kolonu.setSpacing(0)
            tarih_qd = QDate.fromString(tarih, "yyyy-MM-dd")
            if tarih_qd.isValid():
                gun_adi = tarih_qd.toString("dddd")
                tarih_fmt = tarih_qd.toString("dd MMMM yyyy")
                baslik_kolonu.addWidget(make_label(gun_adi, 13, True, T.PRIMARY_L))
                baslik_kolonu.addWidget(make_label(tarih_fmt, 11, color=T.TEXT2))
            else:
                baslik_kolonu.addWidget(make_label(tarih, 13, True, T.PRIMARY_L))
                baslik_kolonu.addWidget(make_label("Belirsiz tarih", 11, color=T.TEXT2))
            dhl.addLayout(baslik_kolonu)
            dhl.addStretch()
            sayi_badge = QLabel(f" {len(items)} etkinlik ")
            sayi_badge.setStyleSheet(
                f"background:{alpha_color(T.BG3, 0.85)};"
                f"color:{T.TEXT2};border:none;border-radius:9px;"
                "font-size:11px;font-weight:600;padding:4px 10px;"
            )
            dhl.addWidget(sayi_badge)
            lay.addWidget(day_header)
            lay.addSpacing(4)

            sirali_items = sorted(
                items,
                key=lambda kayit: ((kayit.get("saat") or "99:99"), kayit.get("id", 0))
            )

            for p in sirali_items:
                kat = p.get("kategori", "Genel") or "Genel"
                icon_t, kat_color = KAT_ICONS.get(kat, ("📌", T.CYAN))
                kaynak = p.get("kaynak", "manuel") if "kaynak" in (p.keys() if hasattr(p, "keys") else {}) else "manuel"

                row_w = QFrame()
                row_w.setProperty("t", "p")
                row_w.setMinimumHeight(86)
                row_w.setCursor(Qt.PointingHandCursor)
                row_w.setStyleSheet(f"""
                    QFrame {{
                        background: {alpha_color(T.BG2, 0.96)};
                        border-radius: 18px;
                    }}
                    QFrame:hover {{
                        background: {T.CARD_H};
                    }}
                """)
                row_l = QHBoxLayout(row_w)
                row_l.setContentsMargins(16, 14, 16, 14)
                row_l.setSpacing(14)

                ikon_lbl = QLabel(icon_t)
                ikon_lbl.setFixedSize(42, 42)
                ikon_lbl.setAlignment(Qt.AlignCenter)
                ikon_lbl.setStyleSheet(
                    f"background:{alpha_color(kat_color, 0.14)};"
                    "border-radius:13px;font-size:18px;"
                )
                row_l.addWidget(ikon_lbl, alignment=Qt.AlignTop)

                orta = QVBoxLayout()
                orta.setSpacing(6)

                ust = QHBoxLayout()
                ust.setSpacing(8)
                saat_str = p.get("saat") or "--:--"
                time_badge = QLabel(saat_str)
                time_badge.setAlignment(Qt.AlignCenter)
                time_badge.setStyleSheet(
                    f"background:{alpha_color(kat_color, 0.14)};"
                    f"color:{kat_color};border:none;border-radius:8px;"
                    "font-size:11px;font-weight:700;padding:4px 8px;"
                )
                ust.addWidget(time_badge)
                baslik_lbl = make_label(p.get("baslik") or "Plan", 14, True)
                baslik_lbl.setWordWrap(True)
                ust.addWidget(baslik_lbl, 1)
                if kaynak == "ai":
                    ai_badge = QLabel("  🤖 AI  ")
                    ai_badge.setStyleSheet(
                        f"background:{alpha_color(T.PRIMARY, 0.16)};"
                        f"color:{T.PRIMARY_L};border:none;border-radius:8px;"
                        "font-size:10px;font-weight:700;padding:3px 0;"
                    )
                    ust.addWidget(ai_badge)
                orta.addLayout(ust)

                if p.get("aciklama"):
                    aciklama_lbl = make_label(p["aciklama"], 11, False, T.TEXT3)
                    aciklama_lbl.setWordWrap(True)
                    orta.addWidget(aciklama_lbl)

                bot_info = QHBoxLayout()
                bot_info.setSpacing(8)
                if p.get("konum"):
                    loc_lbl = QLabel(f"📍 {p['konum']}")
                    loc_lbl.setStyleSheet(
                        f"background:{alpha_color(T.TEXT2, 0.10)};"
                        f"color:{T.TEXT2};border:none;border-radius:8px;"
                        "font-size:11px;padding:4px 8px;"
                    )
                    bot_info.addWidget(loc_lbl)
                kat_lbl = QLabel(f" {kat} ")
                kat_lbl.setStyleSheet(
                    f"background:{alpha_color(kat_color, 0.14)};"
                    f"color:{kat_color};border:none;border-radius:8px;"
                    "font-size:10px;font-weight:700;padding:4px 8px;"
                )
                bot_info.addWidget(kat_lbl)
                bot_info.addStretch()
                orta.addLayout(bot_info)
                row_l.addLayout(orta, 1)

                sil = QPushButton("✕")
                sil.setCursor(Qt.PointingHandCursor)
                sil.setFixedSize(26, 26)
                sil.setStyleSheet(
                    f"QPushButton{{background:transparent;border:none;color:{T.TEXT3};font-size:12px;}}"
                    f"QPushButton:hover{{color:{T.ROSE};background:{alpha_color(T.ROSE, 0.12)};border-radius:8px;}}"
                )
                sil.clicked.connect(lambda _, pid=p["id"]: (
                    self.yon.db.plan_sil(pid),
                    self._detay_cache_temizle(),
                    self._plan_liste(lay)
                ))
                row_l.addWidget(sil, alignment=Qt.AlignTop)

                lay.addWidget(row_w)

            lay.addSpacing(10)

        lay.addStretch()

    def _plan_ekle_dlg(self, lay):
        s = self.yon.db.seyahat_getir(self.sid)
        d = QDialog(self); d.setWindowTitle("Plan Ekle"); d.setFixedSize(430, 460)
        dl = QVBoxLayout(d); dl.setSpacing(10); dl.setContentsMargins(24, 20, 24, 20)
        dl.addWidget(make_label("📅 Yeni Plan", 18, True))
        dl.addWidget(make_label("Tarih", 12, color=T.TEXT2))
        td = QDateEdit(); td.setCalendarPopup(True); td.setFixedHeight(42)
        if s:
            tarih = QDate.fromString(s["baslangic_tarihi"], "yyyy-MM-dd")
            td.setDate(tarih if tarih.isValid() else QDate.currentDate())
        else:
            td.setDate(QDate.currentDate())
        dl.addWidget(td)
        dl.addWidget(make_label("Saat", 12, color=T.TEXT2))
        st = QTimeEdit(); st.setTime(QTime(10, 0)); st.setFixedHeight(42); dl.addWidget(st)
        dl.addWidget(make_label("Başlık", 12, color=T.TEXT2))
        bi = make_input("Örn. Müze bileti al"); dl.addWidget(bi)
        dl.addWidget(make_label("Kategori", 12, color=T.TEXT2))
        kc = QComboBox(); kc.addItems(["Genel", "Ulaşım", "Yemek", "Konaklama", "Hatırlatma"]); kc.setFixedHeight(42)
        dl.addWidget(kc)
        dl.addWidget(make_label("Açıklama", 12, color=T.TEXT2))
        ai = make_input("Opsiyonel"); dl.addWidget(ai)
        dl.addWidget(make_label("Konum", 12, color=T.TEXT2))
        ki = make_input("Opsiyonel"); dl.addWidget(ki)
        dl.addStretch()
        btn = make_btn("Ekle", True, "✓", h=46)
        def ekle():
            if not bi.text().strip():
                QMessageBox.warning(d, "Uyarı", "Başlık gerekli!")
                return
            tarih_str = td.date().toString("yyyy-MM-dd")
            self.yon.db.plan_ekle(
                self.sid,
                tarih_str,
                st.time().toString("HH:mm"),
                bi.text().strip(),
                ai.text().strip(),
                ki.text().strip(),
                kategori=kc.currentText(),
                tarih=tarih_str,
            )
            d.accept(); self._detay_cache_temizle(); self._plan_liste(lay)
        btn.clicked.connect(ekle); dl.addWidget(btn); d.exec_()

    def _takvim(self, s):
        gun_ogeleri = self._takvim_ogeleri()
        seyahat_gunleri = self._seyahat_gunleri(s)
        secili = QDate.fromString(s["baslangic_tarihi"], "yyyy-MM-dd")
        if not secili.isValid():
            secili = QDate.currentDate()

        w = QWidget()
        wl = QHBoxLayout(w); wl.setContentsMargins(20, 16, 20, 16); wl.setSpacing(20)

        sol = QVBoxLayout(); sol.setSpacing(12)
        sol.addWidget(make_label("🗓️ Takvim", 18, True))

        # Özet istatistik kartları
        ozet = make_card()
        ozl = QHBoxLayout(ozet); ozl.setContentsMargins(16, 12, 16, 12); ozl.setSpacing(4)
        plan_sayisi = len(self._plan_verileri())
        akt_sayisi = len(self._aktivite_verileri())
        ai_sayisi = len([1 for g in gun_ogeleri.values() for o in g if o.get('kaynak') == 'ai'])
        for ikon, baslik, deger, renk in [
            ("📅", "Plan", str(plan_sayisi), T.CYAN),
            ("🎯", "Aktivite", str(akt_sayisi), T.EMERALD),
            ("🤖", "AI", str(ai_sayisi), T.PRIMARY),
        ]:
            kart_f = QFrame()
            kart_f.setStyleSheet(f"QFrame{{background:rgba({int(renk[1:3],16) if len(renk)==7 else 139},{int(renk[3:5],16) if len(renk)==7 else 92},{int(renk[5:7],16) if len(renk)==7 else 246},0.10);"
                                 f"border-radius:12px;}}")
            kf_l = QHBoxLayout(kart_f); kf_l.setContentsMargins(12,8,12,8); kf_l.setSpacing(8)
            kf_l.addWidget(make_label(ikon, 18))
            vv = QVBoxLayout(); vv.setSpacing(0)
            vv.addWidget(make_label(deger, 18, True, renk))
            vv.addWidget(make_label(baslik, 10, color=T.TEXT3))
            kf_l.addLayout(vv)
            ozl.addWidget(kart_f)
            ozl.addSpacing(8)
        ozl.addStretch()
        sol.addWidget(ozet)

        # Premium takvim kartı
        takvim_card = make_card()
        tcl = QVBoxLayout(takvim_card); tcl.setContentsMargins(14, 14, 14, 14); tcl.setSpacing(8)
        self._agenda_calendar = AgendaCalendar(self)
        self._agenda_calendar.setSelectedDate(secili)
        self._agenda_calendar.veri_ayarla(gun_ogeleri, seyahat_gunleri)
        self._agenda_calendar.setMinimumHeight(300)
        tcl.addWidget(self._agenda_calendar)

        # Legend
        legend = QHBoxLayout(); legend.setSpacing(14)
        for renk, txt in [(T.PRIMARY, "Seyahat"), (T.CYAN, "Plan"), (T.EMERALD, "Aktivite"), (T.PRIMARY_L, "AI")]:
            lr = QHBoxLayout(); lr.setSpacing(5)
            dot = QFrame(); dot.setFixedSize(9, 9)
            dot.setStyleSheet(f"background:{renk};border-radius:4px;")
            lr.addWidget(dot); lr.addWidget(make_label(txt, 11, color=T.TEXT2))
            legend.addLayout(lr)
        legend.addStretch()
        tcl.addLayout(legend)
        sol.addWidget(takvim_card)
        sol.addStretch()
        wl.addLayout(sol)

        # ── SAĞ: Seçili gün detay paneli ──
        sag = QVBoxLayout(); sag.setSpacing(10)

        detay_header = QHBoxLayout()
        self._takvim_baslik_lbl = QLabel("Bir gün seçin")
        self._takvim_baslik_lbl.setStyleSheet(f"color:{T.TEXT};font-size:16px;font-weight:800;background:transparent;")
        detay_header.addWidget(self._takvim_baslik_lbl)
        detay_header.addStretch()
        sag.addLayout(detay_header)

        self._takvim_detay_scroll = QScrollArea()
        self._takvim_detay_scroll.setWidgetResizable(True)
        self._takvim_detay_w = QWidget()
        self._takvim_detay_lay = QVBoxLayout(self._takvim_detay_w)
        self._takvim_detay_lay.setSpacing(8)
        self._takvim_detay_lay.setContentsMargins(0, 0, 4, 0)
        self._takvim_detay_scroll.setWidget(self._takvim_detay_w)
        sag.addWidget(self._takvim_detay_scroll, 1)
        wl.addLayout(sag, 1)

        KAT_ICONS = {
            "Ulaşım": ("🚗", T.SKY), "Yemek": ("🍽️", T.AMBER),
            "Konaklama": ("🏨", T.PRIMARY_L), "Hatırlatma": ("⏰", T.ROSE),
            "Müze": ("🏛️", T.ORANGE), "Aktivite": ("🎯", T.EMERALD),
            "Genel": ("📌", T.CYAN), "Plan": ("📋", T.INDIGO),
        }

        def gun_goster(tarih_str):
            self._takvim_baslik_lbl.setText(
                QDate.fromString(tarih_str, "yyyy-MM-dd").toString("dddd, dd MMMM yyyy")
                if QDate.fromString(tarih_str, "yyyy-MM-dd").isValid() else tarih_str
            )
            while self._takvim_detay_lay.count():
                it = self._takvim_detay_lay.takeAt(0)
                if it.widget(): it.widget().deleteLater()

            ogeler = gun_ogeleri.get(tarih_str, [])
            if not ogeler:
                bos = QFrame()
                bos.setFixedHeight(80)
                bos.setStyleSheet(f"QFrame{{background:rgba(255,255,255,0.02);border:none;border-radius:14px;}}")
                bl = QVBoxLayout(bos); bl.setAlignment(Qt.AlignCenter)
                bl.addWidget(make_label("Bu gün için etkinlik yok", 13, color=T.TEXT3))
                self._takvim_detay_lay.addWidget(bos)
                self._takvim_detay_lay.addStretch()
                return

            for oelem in ogeler:
                tur = oelem.get("tur", "plan")
                kat = oelem.get("kategori", "Aktivite" if tur == "aktivite" else "Plan")
                icon_t, kat_color = KAT_ICONS.get(kat, ("📋", T.CYAN))
                if tur == "aktivite": icon_t, kat_color = ("🎯", T.EMERALD)

                kart = QFrame()
                kart.setMinimumHeight(68)
                kart.setStyleSheet(f"""
                    QFrame {{
                        background: {T.CARD};
                        border: none;
                        border-radius: 12px;
                    }}
                """)
                kl = QHBoxLayout(kart); kl.setContentsMargins(14, 10, 14, 10); kl.setSpacing(12)

                # İkon
                ik = QLabel(icon_t)
                ik.setFixedSize(36, 36)
                ik.setAlignment(Qt.AlignCenter)
                ik.setStyleSheet(f"font-size:18px;background:rgba({int(kat_color[1:3],16) if len(kat_color)==7 else 34},"
                                 f"{int(kat_color[3:5],16) if len(kat_color)==7 else 211},"
                                 f"{int(kat_color[5:7],16) if len(kat_color)==7 else 153},0.15);"
                                 f"border-radius:10px;")
                kl.addWidget(ik)

                orta = QVBoxLayout(); orta.setSpacing(2)
                baslik_r = QHBoxLayout()
                baslik_r.addWidget(make_label(oelem.get("baslik", "—"), 13, True))
                if oelem.get("kaynak") == "ai":
                    ai_b = QLabel("AI")
                    ai_b.setStyleSheet(f"background:rgba(139,92,246,0.2);color:{T.PRIMARY_L};"
                                       "border-radius:5px;font-size:10px;font-weight:700;padding:1px 6px;")
                    baslik_r.addWidget(ai_b)
                baslik_r.addStretch()
                orta.addLayout(baslik_r)

                info = []
                if oelem.get("saat"): info.append(f"🕐 {oelem['saat']}")
                if oelem.get("konum"): info.append(f"📍 {oelem['konum']}")
                if oelem.get("fiyat", 0) > 0: info.append(f"₺{oelem['fiyat']:,.0f}")
                if info: orta.addWidget(make_label("   ".join(info), 11, color=T.TEXT2))
                kl.addLayout(orta, 1)
                self._takvim_detay_lay.addWidget(kart)
            self._takvim_detay_lay.addStretch()

        self._agenda_calendar.secim_degisti.connect(gun_goster)
        gun_goster(secili.toString("yyyy-MM-dd"))
        return w
        for renk, metin in [(T.CYAN, "Plan"), (T.EMERALD, "Aktivite"), (T.PRIMARY, "AI")]:
            dot = QFrame(); dot.setFixedSize(9, 9)
            dot.setStyleSheet(f"background:{renk};border:none;border-radius:4px;")
            legend.addWidget(dot)
            legend.addWidget(make_label(metin, 11, False, T.TEXT2))
            legend.addSpacing(8)
        legend.addStretch()
        tcl.addLayout(legend)
        sol.addWidget(takvim_card, 1)
        wl.addLayout(sol, 1)

        sag = QVBoxLayout(); sag.setSpacing(10)
        self._takvim_detay_baslik = make_label("", 16, True)
        sag.addWidget(self._takvim_detay_baslik)
        detay_scroll = QScrollArea(); detay_scroll.setWidgetResizable(True)
        detay_w = QWidget()
        self._takvim_detay_lay = QVBoxLayout(detay_w)
        self._takvim_detay_lay.setContentsMargins(0, 0, 0, 0)
        self._takvim_detay_lay.setSpacing(10)
        detay_scroll.setWidget(detay_w)
        sag.addWidget(detay_scroll, 1)
        wl.addLayout(sag, 1)

        def gun_goster(tarih_str):
            self._takvim_detay_baslik.setText(f"📆 {self._plan_baslik_tarihi(tarih_str)}")
            while self._takvim_detay_lay.count():
                it = self._takvim_detay_lay.takeAt(0)
                if it.widget():
                    it.widget().deleteLater()

            ogeler = gun_ogeleri.get(tarih_str, [])
            if not ogeler:
                bos = make_card()
                bl = QVBoxLayout(bos); bl.setContentsMargins(18, 18, 18, 18)
                bl.addWidget(make_label("Bu gün için plan veya aktivite yok.", 14, False, T.TEXT2))
                self._takvim_detay_lay.addWidget(bos)
                self._takvim_detay_lay.addStretch()
                return

            for oge in ogeler:
                kart = make_card()
                kl = QHBoxLayout(kart); kl.setContentsMargins(16, 12, 16, 12)
                saat = QLabel(oge["saat"] or "—")
                saat.setFixedWidth(60)
                saat.setStyleSheet(f"color:{T.CYAN if oge['tur']=='plan' else T.EMERALD};font-size:13px;font-weight:700;background:transparent;")
                kl.addWidget(saat)
                orta = QVBoxLayout()
                ust = QHBoxLayout()
                ust.addWidget(make_label(oge["baslik"], 14, True))
                ust.addSpacing(6)
                ust.addWidget(self._kaynak_badge("AI" if oge.get("kaynak") == "ai" else "MANUEL", T.PRIMARY if oge.get("kaynak") == "ai" else T.SKY))
                ust.addWidget(self._kaynak_badge("PLAN" if oge["tur"] == "plan" else "AKTİVİTE", T.CYAN if oge["tur"] == "plan" else T.EMERALD))
                ust.addStretch()
                orta.addLayout(ust)
                alt = []
                if oge["konum"]:
                    alt.append(f"📍 {oge['konum']}")
                if oge["fiyat"]:
                    alt.append(f"₺{oge['fiyat']:,.0f}")
                if oge["aciklama"]:
                    alt.append(oge["aciklama"])
                if alt:
                    orta.addWidget(make_label("  ".join(alt), 12, False, T.TEXT2))
                kl.addLayout(orta, 1)
                self._takvim_detay_lay.addWidget(kart)
            self._takvim_detay_lay.addStretch()

        self._agenda_calendar.secim_degisti.connect(gun_goster)
        gun_goster(secili.toString("yyyy-MM-dd"))
        return w

    # ── TAKVİM (eski - artık kullanılmıyor) ────────────────────────
    def _takvim_legacy_placeholder(self, s):
        # Artık kullanılmıyor - _takvim() metodunu kullanın
        pass

    def _takvim_eski_kod_yer_tutucu(self, s):
        found = False
        for a in []:
            if a["tarih"] == "":
                found = True

    # ── Harita ────────────────────────────────────────────────────
    def _harita(self, s):
        w = QWidget(); wl = QVBoxLayout(w); wl.setContentsMargins(0, 0, 0, 0)
        container = QWidget()
        cl = QVBoxLayout(container)
        cl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(container)
        
        btn_container = QWidget()
        btn_lay = QVBoxLayout(btn_container)
        btn_lay.setAlignment(Qt.AlignCenter)
        load_btn = QPushButton("🗺️ Haritayı Yükle")
        load_btn.setFixedSize(220, 56)
        load_btn.setCursor(Qt.PointingHandCursor)
        load_btn.setStyleSheet(f"QPushButton{{background:{T.PRIMARY};color:white;border:none;border-radius:28px;font-size:16px;font-weight:bold;}} QPushButton:hover{{background:{T.PRIMARY_L};}}")
        btn_lay.addWidget(load_btn)
        
        info_lbl = QLabel("Haritayı açmak sistem kaynaklarını kullanır.")
        info_lbl.setStyleSheet(f"color:{T.TEXT2};font-size:13px;")
        info_lbl.setAlignment(Qt.AlignCenter)
        if not HAS_WEBENGINE:
            load_btn.setText("Tarayicida Ac")
            info_lbl.setText("Hafif surumde harita varsayilan tarayicida acilir.")
        btn_lay.addWidget(info_lbl)
        
        cl.addWidget(btn_container)

        def do_load():
            load_btn.setEnabled(False)
            info_lbl.setText("Yükleniyor...")
            
            from main import SeyahatAsistani
            coord_db = AnaSayfa.SEHIR_COORDS
            sehir = s["sehir"]
            lat, lon = 39.0, 35.0
            for k, v in coord_db.items():
                if k.lower() == sehir.lower() or k.lower() in sehir.lower():
                    lat, lon = v; break

            try:
                if sehir in SeyahatAsistani.SEHIR_VERILERI:
                    v = SeyahatAsistani.SEHIR_VERILERI[sehir]
                    if "lat" in v and "lon" in v:
                        lat, lon = v["lat"], v["lon"]
            except Exception:
                pass

            markers = []
            markers.append(f'addM({lat},{lon},"{sehir}","🏙️ Şehir Merkezi","#8b5cf6","center");')
            for k in self._konaklama_verileri():
                if k["otel_adi"]:
                    offset_lat = lat + random.uniform(-0.008, 0.008)
                    offset_lon = lon + random.uniform(-0.008, 0.008)
                    yildiz = "⭐" * (k.get("yildiz") or 0)
                    markers.append(f'addM({offset_lat},{offset_lon},"{k["otel_adi"]}","🏨 {k.get("konum","") or ""} {yildiz}","#38bdf8","hotel");')
            for a in self._aktivite_verileri():
                if a.get("konum"):
                    offset_lat = lat + random.uniform(-0.015, 0.015)
                    offset_lon = lon + random.uniform(-0.015, 0.015)
                    markers.append(f'addM({offset_lat},{offset_lon},"{a["aktivite_adi"]}","🎯 {a["konum"]}","#34d399","activity");')

            mk_js = "\\n".join(markers)
            html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  * {{ margin:0; padding:0; }}
  body, html {{ width:100%; height:100%; overflow:hidden; background:#f0f0f0; }}
  #map {{ width:100%; height:100%; }}
  .leaflet-container {{ background:#f0f0f0 !important; }}
  .custom-popup .leaflet-popup-content-wrapper {{
    background:rgba(255,255,255,0.96); color:#2d3047;
    border:none; border-radius:14px;
    box-shadow:0 8px 32px rgba(0,0,0,0.15);
  }}
  .custom-popup .leaflet-popup-tip {{ background:rgba(255,255,255,0.96); }}
</style>
</head>
<body>
<div id="map"></div>
<script>
var map = L.map('map', {{zoomControl:true, attributionControl:false, preferCanvas:true}}).setView([{lat},{lon}],13);
var std = L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png',
    {{maxZoom:19,subdomains:'abcd'}});
var sat = L.tileLayer('https://mt1.google.com/vt/lyrs=s,h&x={{x}}&y={{y}}&z={{z}}',{{maxZoom:20}});
std.addTo(map);
L.control.layers({{'\U0001f5fa\ufe0f Standart':std,'\U0001f6f0\ufe0f Uydu':sat}},{{}},{{position:'topright'}}).addTo(map);

var iconMap = {{
  center: '🏙️', hotel: '🏨', activity: '🎯'
}};

function addM(lat, lon, title, desc, color, type) {{
  var icon = iconMap[type] || '📍';
  var markerHtml = '<div style="width:38px;height:38px;border-radius:50%;' +
    'background:' + color + '22;' +
    'display:flex;align-items:center;justify-content:center;' +
    'font-size:18px;box-shadow:0 4px 16px rgba(0,0,0,0.2);">' + icon + '</div>';
  var divIcon = L.divIcon({{
    html: markerHtml, iconSize:[38,38], iconAnchor:[19,19],
    popupAnchor:[0,-19], className:''
  }});
  L.marker([lat,lon],{{icon:divIcon}}).addTo(map)
    .bindPopup(L.popup({{className:'custom-popup'}}).setContent(
      '<div style="padding:4px"><b style="font-size:14px;color:#2d3047">' + title + '</b>' +
      '<div style="color:#6b7194;font-size:12px;margin-top:3px">' + desc + '</div></div>'
    ));
}}
{mk_js}
</script>
</body></html>"""
            if HAS_WEBENGINE:
                cl.removeWidget(btn_container)
                btn_container.deleteLater()
                web = QWebEngineView()
                web.setHtml(html)
                cl.addWidget(web)
            else:
                opened, _ = open_html_in_browser(html, f"seyahat-detay-{self.sid or 'harita'}")
                load_btn.setEnabled(True)
                info_lbl.setText(
                    "Harita tarayicida acildi." if opened else
                    "Harita varsayilan tarayicida acilamadi."
                )
                if not opened:
                    QMessageBox.warning(self, "Harita", "Harita varsayilan tarayicida acilamadi.")

        load_btn.clicked.connect(do_load)
        return w

    # ── Arkadaşlar ────────────────────────────────────────────────
    def _arkadas(self):
        w = QWidget(); wl = QVBoxLayout(w); wl.setContentsMargins(24, 20, 24, 20); wl.setSpacing(12)
        h = QHBoxLayout(); h.addWidget(make_label("👥 Seyahat Arkadaşları", 18, True)); h.addStretch()
        eb = make_btn("Ekle", True, "➕", h=38); eb.clicked.connect(lambda: self._ark_ekle_dlg(wl))
        h.addWidget(eb); wl.addLayout(h)
        wl.addWidget(make_label("Arkadaş ekleyin, görevlerini belirleyin", 12, color=T.TEXT3))
        self._ark_liste(wl); return w

    def _ark_liste(self, lay):
        for i in reversed(range(lay.count())):
            it = lay.itemAt(i)
            if it.widget() and it.widget().property("t") == "f": it.widget().deleteLater()
        arkadaslar = self._arkadas_verileri()
        for a in arkadaslar:
            c = make_card(); c.setProperty("t", "f"); c.setMinimumHeight(70)
            cl = QHBoxLayout(c); cl.setContentsMargins(16, 12, 16, 12)
            av = QLabel("👤"); av.setFixedSize(44, 44); av.setAlignment(Qt.AlignCenter)
            av.setStyleSheet(f"background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {T.CYAN},stop:1 {T.SKY});"
                            f"border:none;border-radius:22px;font-size:20px;")
            cl.addWidget(av); cl.addSpacing(12)
            left = QVBoxLayout()
            left.addWidget(make_label(a["arkadas_adi"], 15, True))
            if a["email"]: left.addWidget(make_label(f"📧 {a['email']}", 12, color=T.TEXT2))
            if a["gorevler"]:
                lbl_g = make_label(f"📋 {a['gorevler']}", 12, color=T.TEXT2); lbl_g.setWordWrap(True); left.addWidget(lbl_g)
            if a["notlar"]:
                lbl_n = make_label(f"📝 {a['notlar']}", 11, color=T.TEXT3); lbl_n.setWordWrap(True); left.addWidget(lbl_n)
            cl.addLayout(left, 1)
            bc = QVBoxLayout(); bc.setAlignment(Qt.AlignTop)
            for ikon, col, fn in [("✏️", "rgba(56,189,248,0.08)", lambda _, aid=a["id"]: self._ark_edit(aid, lay)),
                                   ("🗑️", "rgba(251,113,133,0.08)", lambda _, aid=a["id"]: (
                                       self.yon.db.arkadas_sil(aid), self._detay_cache_temizle(), self._ark_liste(lay)))]:
                b = QPushButton(ikon); b.setCursor(Qt.PointingHandCursor); b.setFixedSize(30, 30)
                b.setStyleSheet(f"QPushButton{{background:{col};border:none;border-radius:8px;font-size:14px;}}")
                b.clicked.connect(fn); bc.addWidget(b)
            cl.addLayout(bc); lay.addWidget(c)
        if not arkadaslar:
            l = make_label("Henüz arkadaş eklenmedi", 14, color=T.TEXT3)
            l.setProperty("t", "f"); l.setAlignment(Qt.AlignCenter); lay.addWidget(l)

    def _ark_ekle_dlg(self, lay):
        d = QDialog(self); d.setWindowTitle("Arkadaş Ekle"); d.setFixedSize(400, 460)
        dl = QVBoxLayout(d); dl.setSpacing(10); dl.setContentsMargins(24, 20, 24, 20)
        dl.addWidget(make_label("👥 Arkadaş Ekle", 18, True))
        dl.addWidget(make_label("Ad Soyad", 12, color=T.TEXT2))
        ai = make_input("Arkadaşın adı"); dl.addWidget(ai)
        dl.addWidget(make_label("E-posta", 12, color=T.TEXT2))
        ei = make_input("opsiyonel"); dl.addWidget(ei)
        dl.addWidget(make_label("Görevler", 12, color=T.TEXT2))
        gi = QTextEdit(); gi.setPlaceholderText("Otel araştırması, bilet alımı vb."); gi.setFixedHeight(75)
        dl.addWidget(gi)
        dl.addWidget(make_label("Not", 12, color=T.TEXT2))
        ni = make_input("Opsiyonel"); dl.addWidget(ni)
        dl.addStretch()
        btn = make_btn("Ekle", True, "✓", h=46)
        def ekle():
            if not ai.text().strip(): QMessageBox.warning(d, "Uyarı", "Ad gerekli!"); return
            self.yon.db.arkadas_ekle(self.sid, ai.text().strip(), ei.text().strip(),
                gi.toPlainText().strip(), ni.text().strip()); d.accept(); self._detay_cache_temizle(); self._ark_liste(lay)
        btn.clicked.connect(ekle); dl.addWidget(btn); d.exec_()

    def _ark_edit(self, aid, lay):
        ark = None
        for a in self._arkadas_verileri():
            if a["id"] == aid: ark = a; break
        if not ark: return
        d = QDialog(self); d.setWindowTitle("Düzenle"); d.setFixedSize(400, 460)
        dl = QVBoxLayout(d); dl.setSpacing(10); dl.setContentsMargins(24, 20, 24, 20)
        dl.addWidget(make_label("✏️ Düzenle", 18, True))
        fields = {}
        for lbl, key, val in [("Ad", "ad", ark["arkadas_adi"]), ("E-posta", "email", ark["email"] or ""),
                               ("Not", "not", ark["notlar"] or "")]:
            dl.addWidget(make_label(lbl, 12, color=T.TEXT2))
            inp = make_input(""); inp.setText(val); fields[key] = inp; dl.addWidget(inp)
        dl.addWidget(make_label("Görevler", 12, color=T.TEXT2))
        gi = QTextEdit(); gi.setText(ark["gorevler"] or ""); gi.setFixedHeight(75)
        dl.addWidget(gi); dl.addStretch()
        btn = make_btn("Güncelle", True, "✓", h=46)
        def gunc():
            self.yon.db.arkadas_guncelle(aid, arkadas_adi=fields["ad"].text().strip(),
                email=fields["email"].text().strip(), gorevler=gi.toPlainText().strip(),
                notlar=fields["not"].text().strip()); d.accept(); self._detay_cache_temizle(); self._ark_liste(lay)
        btn.clicked.connect(gunc); dl.addWidget(btn); d.exec_()

    # ── Uçuşlar ──────────────────────────────────────────────────
    def _ucus(self):
        w = QWidget(); wl = QVBoxLayout(w); wl.setContentsMargins(24, 20, 24, 20); wl.setSpacing(12)
        h = QHBoxLayout(); h.addWidget(make_label("✈️ Uçuşlar", 18, True)); h.addStretch()
        eb = make_btn("Ekle", True, "➕", h=38); eb.clicked.connect(lambda: self._ucus_dlg(wl))
        h.addWidget(eb); wl.addLayout(h)
        self._ucus_liste(wl); return w

    def _ucus_liste(self, lay):
        for i in reversed(range(lay.count())):
            it = lay.itemAt(i)
            if it.widget() and it.widget().property("t") == "u": it.widget().deleteLater()
        ucuslar = self._ucus_verileri()
        for u in ucuslar:
            c = make_card(); c.setProperty("t", "u"); c.setFixedHeight(105)
            cl = QHBoxLayout(c); cl.setContentsMargins(18, 12, 18, 12)
            left = QVBoxLayout()
            tr = QHBoxLayout()
            tr.addWidget(make_label(f"✈️ {u['havayolu'] or '—'}", 15, True))
            if u['ucus_no']: tr.addWidget(make_label(f"#{u['ucus_no']}", 13, color=T.CYAN))
            tr.addStretch(); left.addLayout(tr)
            rr = QHBoxLayout()
            rr.addWidget(make_label(f"🛫 {u['kalkis_yeri'] or '—'}", 13))
            rr.addWidget(make_label("→", 13, color=T.TEXT3))
            rr.addWidget(make_label(f"🛬 {u['varis_yeri'] or '—'}", 13))
            rr.addStretch(); left.addLayout(rr)
            left.addWidget(make_label(f"⏰ {u['kalkis_zamani'] or '—'} → {u['varis_zamani'] or '—'}", 11, color=T.TEXT2))
            cl.addLayout(left, 1)
            right = QVBoxLayout(); right.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if u['fiyat'] > 0: right.addWidget(make_label(f"₺{u['fiyat']:,.0f}", 16, True, T.EMERALD))
            sb = QPushButton("🗑️"); sb.setCursor(Qt.PointingHandCursor); sb.setFixedSize(28, 28)
            sb.setStyleSheet("QPushButton{background:rgba(251,113,133,0.08);border:none;border-radius:6px;font-size:12px;}"
                            "QPushButton:hover{background:rgba(251,113,133,0.18);}")
            sb.clicked.connect(lambda _, uid=u["id"]: (
                self.yon.db.ucus_sil(uid),
                self._detay_cache_temizle(),
                self._ucus_liste(lay)
            ))
            right.addWidget(sb, alignment=Qt.AlignRight); cl.addLayout(right); lay.addWidget(c)
        if not ucuslar:
            l = make_label("Henüz uçuş eklenmedi", 14, color=T.TEXT3)
            l.setProperty("t", "u"); l.setAlignment(Qt.AlignCenter); lay.addWidget(l)

    def _ucus_dlg(self, lay):
        d = QDialog(self); d.setWindowTitle("Uçuş Ekle"); d.setFixedSize(440, 480)
        dl = QVBoxLayout(d); dl.setSpacing(8); dl.setContentsMargins(24, 18, 24, 18)
        dl.addWidget(make_label("✈️ Yeni Uçuş", 18, True))
        f = {}
        for r_items in [
            [("Havayolu", "ha", "THY"), ("Uçuş No", "no", "TK1234")],
            [("Kalkış", "ky", "İstanbul"), ("Varış", "vy", "Paris")],
            [("Kalkış Zamanı", "kz", "2024-05-15 08:30"), ("Varış Zamanı", "vz", "2024-05-15 12:30")]
        ]:
            rr = QHBoxLayout()
            for lbl, key, ph in r_items:
                vl = QVBoxLayout(); vl.addWidget(make_label(lbl, 12, color=T.TEXT2))
                inp = make_input(ph); f[key] = inp; vl.addWidget(inp); rr.addLayout(vl)
            dl.addLayout(rr)
        dl.addWidget(make_label("Fiyat ₺", 12, color=T.TEXT2))
        fi = QDoubleSpinBox(); fi.setRange(0, 999999); fi.setFixedHeight(42); fi.setPrefix("₺ "); dl.addWidget(fi)
        dl.addStretch()
        btn = make_btn("Ekle", True, "✓", h=46)
        def ekle():
            self.yon.db.ucus_ekle(self.sid, f["ha"].text().strip(), f["no"].text().strip(),
                f["ky"].text().strip(), f["vy"].text().strip(), f["kz"].text().strip(),
                f["vz"].text().strip(), fi.value()); d.accept(); self._detay_cache_temizle(); self._ucus_liste(lay)
        btn.clicked.connect(ekle); dl.addWidget(btn); d.exec_()

    # ── Notlar ────────────────────────────────────────────────────
    def _notlar(self, s):
        w = QWidget(); wl = QVBoxLayout(w); wl.setContentsMargins(24, 20, 24, 20); wl.setSpacing(12)
        wl.addWidget(make_label("📝 Seyahat Notları", 18, True))
        ne = QTextEdit(); ne.setText(s["notlar"] or "")
        ne.setPlaceholderText("Notlarınızı buraya yazın...")
        ne.setStyleSheet(f"QTextEdit{{background:{T.CARD};border:none;border-radius:14px;"
                        f"padding:16px;color:{T.TEXT};font-size:14px;}}")
        wl.addWidget(ne)
        kb = make_btn("Kaydet", True, "💾", h=44)
        kb.clicked.connect(lambda: (self.yon.db.seyahat_guncelle(self.sid, notlar=ne.toPlainText()),
                                    QMessageBox.information(self, "✓", "Notlar kaydedildi!")))
        wl.addWidget(kb, alignment=Qt.AlignRight); return w

    def _sil(self, sid):
        if QMessageBox.question(self, "Sil", "Bu seyahati silmek istediğinize emin misiniz?") == QMessageBox.Yes:
            self.yon.db.seyahat_sil(sid); self.geri.emit()


# ═══════════════════════════════════════════════════════════════════
#  HARİTA SAYFASI
# ═══════════════════════════════════════════════════════════════════

class HaritaSayfasi(QWidget):
    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon; self.lay = QVBoxLayout(self); self.lay.setContentsMargins(0, 0, 0, 0)
        self.web = None
        self.bos_lbl = None
        self.bos_btn = None

    def _tum_harita_html(self):
        from main import SeyahatAsistani
        sl = self.yon.seyahatleri_listele()
        mk = ""; fl, fo = 41.0082, 28.9784
        for i, s in enumerate(sl):
            if s.sehir in SeyahatAsistani.SEHIR_VERILERI:
                v = SeyahatAsistani.SEHIR_VERILERI[s.sehir]
                la, lo = v["lat"], v["lon"]
                if i == 0:
                    fl, fo = la, lo
                dur = s.durum()
                clr = {"yaklaÅŸan": "#38bdf8", "aktif": "#34d399", "tamamlanan": "#fb923c"}.get(dur, "#ef4444")
                mk += f'addM({la},{lo},"{s.sehir}","ğŸ“… {s.baslangic_tarihi}","{clr}");\n'
        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>body{{margin:0}}#map{{width:100%;height:100vh}}</style></head><body>
        <div id="map"></div><script>
        var map=L.map('map', {{preferCanvas:true}}).setView([{fl},{fo}],4);
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png',{{maxZoom:19,subdomains:'abcd'}}).addTo(map);
        function addM(a,b,t,d,c){{var i=L.divIcon({{className:'',iconSize:[30,30],iconAnchor:[15,15],
        html:'<div style="width:30px;height:30px;background:'+c+';border-radius:50%;border:3px solid white;box-shadow:0 2px 10px rgba(0,0,0,0.25)"></div>'}});
        L.marker([a,b],{{icon:i}}).addTo(map).bindPopup('<b>'+t+'</b><br>'+d);}}
        {mk}</script></body></html>"""

    def _open_map_in_browser(self):
        opened, _ = open_html_in_browser(self._tum_harita_html(), "tum-seyahatler-harita")
        if not opened:
            QMessageBox.warning(self, "Harita", "Harita varsayilan tarayicida acilamadi.")

    def yukle(self):
        if not HAS_WEBENGINE:
            if self.web is not None:
                self.lay.removeWidget(self.web)
                self.web.deleteLater()
                self.web = None
            if self.bos_lbl is None:
                self.bos_lbl = make_label("Harita hafif surumde varsayilan tarayicida acilir", 16, color=T.AMBER)
                self.bos_lbl.setAlignment(Qt.AlignCenter)
                self.lay.addWidget(self.bos_lbl, alignment=Qt.AlignCenter)
            if self.bos_btn is None:
                self.bos_btn = make_btn("Tarayicida Ac", False, "MAP", h=40)
                self.bos_btn.clicked.connect(self._open_map_in_browser)
                self.lay.addWidget(self.bos_btn, alignment=Qt.AlignCenter)
            return
        if self.bos_lbl is not None:
            self.lay.removeWidget(self.bos_lbl)
            self.bos_lbl.deleteLater()
            self.bos_lbl = None
        if self.bos_btn is not None:
            self.lay.removeWidget(self.bos_btn)
            self.bos_btn.deleteLater()
            self.bos_btn = None
        if self.web is None:
            self.web = QWebEngineView()
            self.lay.addWidget(self.web)
        from main import SeyahatAsistani
        sl = self.yon.seyahatleri_listele()
        mk = ""; fl, fo = 41.0082, 28.9784
        for i, s in enumerate(sl):
            if s.sehir in SeyahatAsistani.SEHIR_VERILERI:
                v = SeyahatAsistani.SEHIR_VERILERI[s.sehir]
                la, lo = v["lat"], v["lon"]
                if i == 0: fl, fo = la, lo
                dur = s.durum()
                clr = {"yaklaşan": "#38bdf8", "aktif": "#34d399", "tamamlanan": "#fb923c"}.get(dur, "#ef4444")
                mk += f'addM({la},{lo},"{s.sehir}","📅 {s.baslangic_tarihi}","{clr}");\n'
        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>body{{margin:0}}#map{{width:100%;height:100vh}}</style></head><body>
        <div id="map"></div><script>
        var map=L.map('map', {{preferCanvas:true}}).setView([{fl},{fo}],4);
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png',{{maxZoom:19,subdomains:'abcd'}}).addTo(map);
        function addM(a,b,t,d,c){{var i=L.divIcon({{className:'',iconSize:[30,30],iconAnchor:[15,15],
        html:'<div style="width:30px;height:30px;background:'+c+';border-radius:50%;border:3px solid white;box-shadow:0 2px 10px rgba(0,0,0,0.25)"></div>'}});
        L.marker([a,b],{{icon:i}}).addTo(map).bindPopup('<b>'+t+'</b><br>'+d);}}
        {mk}</script></body></html>"""
        self.web.setHtml(self._tum_harita_html())


# ═══════════════════════════════════════════════════════════════════
#  BİLDİRİMLER
# ═══════════════════════════════════════════════════════════════════

class BildirimlerSayfasi(QWidget):
    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon
        ml = QVBoxLayout(self); ml.setContentsMargins(32, 28, 32, 28); ml.setSpacing(16)
        h = QHBoxLayout(); h.addWidget(make_label("🔔 Bildirimler", 24, True)); h.addStretch()
        ob = make_btn("Tümünü Oku", False, "✓", h=38); ob.clicked.connect(self._tmoku)
        h.addWidget(ob); ml.addLayout(h)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        self.lw = QWidget(); self.ll = QVBoxLayout(self.lw); self.ll.setSpacing(8)
        scroll.setWidget(self.lw); ml.addWidget(scroll)

    def yukle(self):
        while self.ll.count():
            it = self.ll.takeAt(0)
            if it.widget(): it.widget().deleteLater()
        bl = self.yon.db.bildirimleri_getir(self.yon.aktif_kullanici_id)
        if not bl:
            self.ll.addWidget(make_label("Bildirim yok 🔕", 14, color=T.TEXT3), alignment=Qt.AlignCenter); return
        for b in bl:
            c = make_card(); c.setFixedHeight(75)
            ok = b["okundu"]
            if not ok:
                c.setStyleSheet(f"QFrame{{background:rgba(139,92,246,0.07);border:none;"
                               f"border-radius:14px;}}")
            cl = QHBoxLayout(c); cl.setContentsMargins(14, 10, 14, 10)
            ikon = {"seyahat": "✈️", "bilgi": "ℹ️"}.get(b["tur"], "🔔")
            cl.addWidget(make_label(ikon, 22)); cl.addSpacing(8)
            left = QVBoxLayout()
            left.addWidget(make_label(b["baslik"], 14, True))
            left.addWidget(make_label(b["mesaj"] or "", 12, color=T.TEXT2))
            cl.addLayout(left, 1)
            cl.addWidget(make_label(str(b["tarih"])[:16] if b["tarih"] else "", 11, color=T.TEXT3))
            if not ok:
                dot = QFrame(); dot.setFixedSize(8, 8)
                dot.setStyleSheet(f"background:{T.PRIMARY};border:none;border-radius:4px;")
                cl.addWidget(dot)
            self.ll.addWidget(c)
        self.ll.addStretch()

    def _tmoku(self):
        if self.yon.aktif_kullanici_id:
            self.yon.db.tum_bildirimleri_oku(self.yon.aktif_kullanici_id); self.yukle()


# ═══════════════════════════════════════════════════════════════════
#  PROFİL
# ═══════════════════════════════════════════════════════════════════

class ProfilSayfasi(QWidget):
    profil_guncellendi = pyqtSignal()

    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon
        ml = QVBoxLayout(self); ml.setContentsMargins(32, 28, 32, 28); ml.setSpacing(20)
        ml.addWidget(make_label("👤 Profil", 24, True))

        c = make_card()
        cl = QVBoxLayout(c); cl.setContentsMargins(32, 28, 32, 28); cl.setSpacing(12)

        # Avatar
        ar = QHBoxLayout(); ar.setAlignment(Qt.AlignCenter)
        self.avatar_lbl = QLabel("👤")
        self.avatar_lbl.setFixedSize(90, 90); self.avatar_lbl.setAlignment(Qt.AlignCenter)
        self.avatar_lbl.setStyleSheet(f"background:qlineargradient(x1:0,y1:0,x2:1,y2:1,"
                                     f"stop:0 {T.G1},stop:1 {T.G2});"
                                     f"border:none;border-radius:45px;font-size:40px;")
        ar.addWidget(self.avatar_lbl)
        cl.addLayout(ar)

        # Fotoğraf yükle butonu
        fb = make_btn("📷 Fotoğraf Yükle", False, h=36)
        fb.clicked.connect(self._foto_yukle)
        cl.addWidget(fb, alignment=Qt.AlignCenter)
        cl.addSpacing(8)

        for lbl, attr, ph, enabled in [
            ("Ad Soyad", "ad_inp", "Adınız", True),
            ("Kullanıcı Adı", "user_inp", "", False),
            ("E-posta", "email_inp", "E-posta", True),
            ("Telefon", "tel_inp", "Telefon", True),
        ]:
            cl.addWidget(make_label(lbl, 12, color=T.TEXT2))
            inp = make_input(ph); inp.setEnabled(enabled)
            setattr(self, attr, inp); cl.addWidget(inp)

        cl.addSpacing(8)
        btn = make_btn("Profili Güncelle", True, "💾", h=48)
        btn.clicked.connect(self._guncelle)
        cl.addWidget(btn)
        ml.addWidget(c); ml.addStretch()

    def yukle(self):
        u = self.yon.aktif_kullanici
        if u:
            self.ad_inp.setText(u.get("ad_soyad", ""))
            self.user_inp.setText(u.get("kullanici_adi", ""))
            self.email_inp.setText(u.get("email", ""))
            self.tel_inp.setText(u.get("telefon", ""))
            ap = u.get("avatar_path", "")
            if ap and os.path.exists(ap):
                pix = QPixmap(ap).scaled(90, 90, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                self.avatar_lbl.setPixmap(pix)
                self.avatar_lbl.setScaledContents(True)
                self.avatar_lbl.setStyleSheet("border:none;border-radius:45px;")
            else:
                self.avatar_lbl.setText("👤")
                self.avatar_lbl.setStyleSheet(f"background:qlineargradient(x1:0,y1:0,x2:1,y2:1,"
                                             f"stop:0 {T.G1},stop:1 {T.G2});"
                                             f"border:none;border-radius:45px;font-size:40px;")

            avatar_label_uygula(self.avatar_lbl, ap, 90, "👤", 40)


    def _foto_yukle(self):
        path, _ = QFileDialog.getOpenFileName(self, "Profil Fotoğrafı", "",
                                               "Resimler (*.png *.jpg *.jpeg *.bmp *.webp)")
        if path and self.yon.aktif_kullanici_id:
            self.yon.db.kullanici_guncelle(self.yon.aktif_kullanici_id, avatar_path=path)
            self.yon.aktif_kullanici = dict(self.yon.db.kullanici_getir(self.yon.aktif_kullanici_id))
            pix = QPixmap(path).scaled(90, 90, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.avatar_lbl.setPixmap(pix)
            self.avatar_lbl.setScaledContents(True)
            self.avatar_lbl.setStyleSheet("border:none;border-radius:45px;")
            avatar_label_uygula(self.avatar_lbl, path, 90, "👤", 40)
            self.profil_guncellendi.emit()

    def _guncelle(self):
        if not self.yon.aktif_kullanici_id: return
        self.yon.db.kullanici_guncelle(self.yon.aktif_kullanici_id,
            ad_soyad=self.ad_inp.text().strip(), email=self.email_inp.text().strip(),
            telefon=self.tel_inp.text().strip())
        self.yon.aktif_kullanici = dict(self.yon.db.kullanici_getir(self.yon.aktif_kullanici_id))
        QMessageBox.information(self, "✓", "Profil güncellendi!")
        self.profil_guncellendi.emit()


# ═══════════════════════════════════════════════════════════════════
#  AYARLAR
# ═══════════════════════════════════════════════════════════════════

class AyarlarSayfasi(QWidget):
    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon
        self._aktif_tema = (self.yon.aktif_kullanici or {}).get("tema", "dark") if self.yon.aktif_kullanici else "dark"
        ml = QVBoxLayout(self); ml.setContentsMargins(32, 28, 32, 28); ml.setSpacing(20)
        ml.addWidget(make_label("⚙️ Ayarlar", 24, True))

        tc = make_card(); tcl = QVBoxLayout(tc); tcl.setContentsMargins(24, 18, 24, 18); tcl.setSpacing(10)
        tcl.addWidget(make_label("🎨 Tema", 16, True))
        tcl.addWidget(make_label("Uygulama görünümünü özelleştirin", 12, color=T.TEXT2))
        tr = QHBoxLayout()
        self._koyu_btn = make_btn("🌙 Koyu Tema", True, h=42)
        self._acik_btn = make_btn("☀️ Açık Tema", False, h=42)
        self._koyu_btn.clicked.connect(lambda: self._tema_uygula("dark"))
        self._acik_btn.clicked.connect(lambda: self._tema_uygula("light"))
        tr.addWidget(self._koyu_btn); tr.addWidget(self._acik_btn)
        tr.addStretch(); tcl.addLayout(tr)
        ml.addWidget(tc)

        ac = make_card(); acl = QVBoxLayout(ac); acl.setContentsMargins(24, 18, 24, 18); acl.setSpacing(6)
        acl.addWidget(make_label("ℹ️ Hakkında", 16, True))
        acl.addWidget(make_label("Seyahat Planlama v1.0", 13, color=T.TEXT2))
        acl.addWidget(make_label("Python + PyQt5 + SQLite", 12, color=T.TEXT3))
        ml.addWidget(ac); ml.addStretch()
        self._tema_butonlarini_guncelle()

    def _tema_buton_stili(self, aktif=False):
        if aktif:
            return (
                f"QPushButton{{background:{T.PRIMARY};color:white;border:none;"
                "border-radius:14px;font-size:13px;font-weight:600;padding:0 22px;}}"
            )
        hover = "#3f3f46" if T.AKTIF == "dark" else "#e7edf0"
        return (
            f"QPushButton{{background:{T.BG3};color:{T.TEXT2};border:none;"
            "border-radius:14px;font-size:13px;padding:0 22px;}}"
            f"QPushButton:hover{{background:{hover};color:{T.TEXT};}}"
        )

    def _tema_butonlarini_guncelle(self):
        self._koyu_btn.setStyleSheet(self._tema_buton_stili(self._aktif_tema == "dark"))
        self._acik_btn.setStyleSheet(self._tema_buton_stili(self._aktif_tema == "light"))

    def _tema_uygula(self, tema):
        self._aktif_tema = tema
        self._tema_butonlarini_guncelle()
        pencere = self.window()
        if hasattr(pencere, "tema_degistir"):
            pencere.tema_degistir(tema)


# ═══════════════════════════════════════════════════════════════════
#  AI ASİSTAN
# ═══════════════════════════════════════════════════════════════════

class AIAsistanDialog(QDialog):
    def __init__(self, yon, sehir="", butce=5000, gun=5, parent=None):
        super().__init__(parent)
        self.yon = yon; self.sehir = sehir; self.butce = butce; self.gun = gun; self.plan = None
        self.setWindowTitle("🤖 AI Seyahat Asistanı"); self.setMinimumSize(720, 620)
        lay = QVBoxLayout(self); lay.setContentsMargins(24, 20, 24, 20); lay.setSpacing(14)

        h = QHBoxLayout()
        h.addWidget(make_label("🤖 AI Seyahat Asistanı", 22, True)); h.addStretch()
        kb = QPushButton("✕"); kb.setFixedSize(32, 32); kb.setCursor(Qt.PointingHandCursor)
        kb.setStyleSheet(f"QPushButton{{background:{T.BG3};border:none;border-radius:8px;color:{T.TEXT2};"
                        f"font-size:16px;}}QPushButton:hover{{color:white;}}")
        kb.clicked.connect(self.reject); h.addWidget(kb); lay.addLayout(h)
        lay.addWidget(make_label("Bütçe, süre ve şehir girerek AI plan oluşturun", 13, color=T.TEXT2))

        from main import SeyahatAsistani
        fr = QHBoxLayout(); fr.setSpacing(12)
        for lbl, attr, wid_fn in [
            ("🏙️ Şehir", "sc", lambda: self._mk_combo(SeyahatAsistani.sehir_listesi())),
            ("💰 Bütçe", "bi", lambda: self._mk_spin(100, 9999999, self.butce, "₺ ")),
            ("📅 Gün", "gi", lambda: self._mk_ispin(1, 30, self.gun)),
        ]:
            vl = QVBoxLayout(); vl.addWidget(make_label(lbl, 12, True))
            w = wid_fn(); setattr(self, attr, w); vl.addWidget(w); fr.addLayout(vl)
        lay.addLayout(fr)

        lay.addWidget(make_label("🎯 Odağınızı Seçin (Opsiyonel)", 12, True))
        kr = QHBoxLayout()
        self.kategori_cb = []
        for kat in ["Tarihi", "Doğa", "Keşif", "Deneyim", "Kültür"]:
            cb = QCheckBox(kat)
            cb.setStyleSheet("QCheckBox { color: " + T.TEXT + "; }")
            self.kategori_cb.append((kat, cb))
            kr.addWidget(cb)
        kr.addStretch()
        lay.addLayout(kr)

        br = QHBoxLayout()
        ob = make_btn("🔍 Şehir Öner", False, h=44); ob.clicked.connect(self._sehir_oner); br.addWidget(ob)
        pb = make_btn("🤖 Plan Oluştur", True, h=44); pb.clicked.connect(self._plan_olustur); br.addWidget(pb)
        lay.addLayout(br)

        self.ss = QScrollArea(); self.ss.setWidgetResizable(True)
        self.sw = QWidget(); self.sl = QVBoxLayout(self.sw); self.sl.setSpacing(10)
        self.ss.setWidget(self.sw); lay.addWidget(self.ss, 1)

        self.ub = make_btn("📋 Planı Uygula", True, h=48); self.ub.setVisible(False)
        self.ub.clicked.connect(self._uygula); lay.addWidget(self.ub)

    def _mk_combo(self, items):
        c = QComboBox(); c.setEditable(True); c.addItems(items); c.setFixedHeight(42)
        if self.sehir:
            idx = c.findText(self.sehir)
            if idx >= 0: c.setCurrentIndex(idx)
            else: c.setCurrentText(self.sehir)
        return c

    def _mk_spin(self, mn, mx, val, pf=""):
        s = QDoubleSpinBox(); s.setRange(mn, mx); s.setValue(val); s.setPrefix(pf); s.setFixedHeight(42); return s

    def _mk_ispin(self, mn, mx, val):
        s = QSpinBox(); s.setRange(mn, mx); s.setValue(val); s.setFixedHeight(42); return s

    def _badge(self, metin, renk):
        lbl = QLabel(f"  {metin}  ")
        lbl.setStyleSheet(
            f"background:{renk};color:white;border:none;border-radius:9px;"
            "font-size:10px;font-weight:700;padding:3px 8px;"
        )
        return lbl

    def _clear(self):
        while self.sl.count():
            it = self.sl.takeAt(0)
            if it.widget(): it.widget().deleteLater()

    def _sehir_oner(self):
        self._clear()
        oneriler = self.yon.ai_sehir_oner(self.bi.value(), self.gi.value())
        if not oneriler:
            self.sl.addWidget(make_label("❌ Uygun şehir bulunamadı. Bütçeyi artırın.", 14, color=T.ROSE)); return
        self.sl.addWidget(make_label("🌍 Önerilen Şehirler", 16, True))
        for o in oneriler[:6]:
            c = make_card(); c.setFixedHeight(65); c.setCursor(Qt.PointingHandCursor)
            cl = QHBoxLayout(c); cl.setContentsMargins(14, 8, 14, 8)
            cl.addWidget(make_label("✈️", 20)); cl.addSpacing(6)
            vl = QVBoxLayout()
            vl.addWidget(make_label(f"{o['sehir']}, {o['ulke']}", 14, True))
            vl.addWidget(make_label(o.get("aciklama", ""), 11, color=T.TEXT2))
            cl.addLayout(vl, 1)
            cl.addWidget(make_label(f"~₺{o['tahmini_maliyet']:,.0f}", 14, True, T.EMERALD))
            sb = QPushButton("Seç"); sb.setCursor(Qt.PointingHandCursor); sb.setFixedSize(55, 28)
            sb.setStyleSheet(f"QPushButton{{background:{T.PRIMARY};color:white;border:none;"
                            f"border-radius:6px;font-size:11px;font-weight:600;}}")
            sb.clicked.connect(lambda _, s=o['sehir']: self._sec(s)); cl.addWidget(sb)
            self.sl.addWidget(c)

    def _sec(self, s):
        idx = self.sc.findText(s)
        if idx >= 0: self.sc.setCurrentIndex(idx)
        else: self.sc.setCurrentText(s)
        self._plan_olustur()

    def _plan_olustur(self):
        self._clear()
        secilen_kategoriler = [kat for kat, cb in self.kategori_cb if cb.isChecked()]
        p = self.yon.ai_plan_olustur(self.sc.currentText().strip(), self.bi.value(), self.gi.value(), ozel_kategoriler=secilen_kategoriler)
        if not p:
            self.sl.addWidget(make_label("❌ Şehir AI veritabanında yok. 'Şehir Öner' kullanın.", 14, color=T.ROSE))
            self.ub.setVisible(False); return
        self.plan = p
        hc = QFrame(); hc.setFixedHeight(90)
        hc.setStyleSheet(f"QFrame{{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
                        f"stop:0 rgba(139,92,246,0.12),stop:1 rgba(34,211,238,0.08));"
                        f"border:none;border-radius:16px;}}")
        hcl = QHBoxLayout(hc); hcl.setContentsMargins(18, 12, 18, 12)
        hcl.addWidget(make_label("🤖", 28))
        hvl = QVBoxLayout()
        hvl.addWidget(make_label(f"{p['sehir']}, {p['ulke']} — AI Plan", 17, True))
        hvl.addWidget(make_label(f"{p['gun_sayisi']} gün | {p['seviye'].title()} bütçe seviyesi | 🏨 {p['otel']['ad']}", 12, color=T.TEXT2))
        hcl.addLayout(hvl, 1)
        hcl.addWidget(make_label(f"~₺{p['tahmini_maliyet']['toplam']:,.0f}", 18, True, T.EMERALD))
        self.sl.addWidget(hc)

        mc = make_card(); mcl = QVBoxLayout(mc); mcl.setContentsMargins(16, 12, 16, 12)
        mcl.addWidget(make_label("💰 Tahmini Maliyet", 14, True))
        for k, v in p['tahmini_maliyet'].items():
            if k == 'toplam':
                continue
            row = QHBoxLayout(); row.addWidget(make_label(k, 13)); row.addStretch()
            row.addWidget(make_label(f"₺{v:,.0f}", 13, True, T.AMBER)); mcl.addLayout(row)
        mcl.addWidget(make_sep())
        toplam_row = QHBoxLayout(); toplam_row.addWidget(make_label("Toplam", 14, True)); toplam_row.addStretch()
        toplam_row.addWidget(make_label(f"₺{p['tahmini_maliyet']['toplam']:,.0f}", 16, True, T.EMERALD))
        mcl.addLayout(toplam_row); self.sl.addWidget(mc)

        if p.get("oneriler"):
            oc = make_card(); ocl = QVBoxLayout(oc); ocl.setContentsMargins(16, 12, 16, 12)
            ocl.addWidget(make_label("✨ Akıllı Öneriler", 14, True))
            for oneri in p["oneriler"]:
                ocl.addWidget(make_label(f"• {oneri}", 12, False, T.TEXT2))
            self.sl.addWidget(oc)

        self.sl.addWidget(make_label("📅 Günlük Akış", 16, True))
        for gd in p['gunluk_plan']:
            gl = QLabel(f"  📆 {gd['tarih_label']} • {gd.get('tema', 'Plan')}"); gl.setFixedHeight(32)
            gl.setStyleSheet(f"background:rgba(139,92,246,0.05);color:{T.PRIMARY_L};"
                            f"font-size:13px;font-weight:700;border:none;border-radius:8px;padding-left:10px;")
            self.sl.addWidget(gl)
            for item in gd['plan']:
                row_w = make_card(); row_w.setMaximumHeight(62)
                row = QHBoxLayout(row_w); row.setContentsMargins(14, 10, 14, 10)
                saat = QLabel(item['saat']); saat.setFixedWidth(52)
                renk = T.EMERALD if item.get("tur") == "aktivite" else T.CYAN
                saat.setStyleSheet(f"color:{renk};font-size:12px;font-weight:700;background:transparent;")
                row.addWidget(saat)
                row.addWidget(self._badge("AKTİVİTE" if item.get("tur") == "aktivite" else "PLAN", renk))
                row.addSpacing(6)
                orta = QVBoxLayout()
                orta.addWidget(make_label(item['baslik'], 13, True))
                alt = []
                if item.get("konum"):
                    alt.append(f"📍 {item['konum']}")
                if item.get("fiyat"):
                    alt.append(f"₺{item['fiyat']:,.0f}")
                if alt:
                    orta.addWidget(make_label("  ".join(alt), 11, False, T.TEXT2))
                row.addLayout(orta, 1)
                self.sl.addWidget(row_w)
        self.sl.addStretch(); self.ub.setVisible(True)

    def _uygula(self):
        if not self.plan: return
        p = self.plan
        pw = self.parent()
        if hasattr(pw, 'sid') and pw.sid:
            sid = pw.sid
            seyahat = self.yon.db.seyahat_getir(sid)
            bas = seyahat["baslangic_tarihi"] if seyahat else datetime.now().strftime("%Y-%m-%d")
            bit = seyahat["bitis_tarihi"] if seyahat else (datetime.now() + timedelta(days=p['gun_sayisi'] - 1)).strftime("%Y-%m-%d")
            self.yon.db.ai_kayitlarini_temizle(sid)
        else:
            if hasattr(pw, "bas_tarih") and hasattr(pw, "bit_tarih"):
                bas = pw.bas_tarih.date().toString("yyyy-MM-dd")
                bit = pw.bit_tarih.date().toString("yyyy-MM-dd")
            else:
                bas = datetime.now().strftime("%Y-%m-%d")
                bit = (datetime.now() + timedelta(days=p['gun_sayisi'] - 1)).strftime("%Y-%m-%d")
            sid = self.yon.seyahat_olustur(p['sehir'], p['ulke'], bas, bit, p['butce'], "AI", "AI planı")

        if not sid:
            QMessageBox.warning(self, "Hata", "Oluşturulamadı!")
            return

        bas_q = QDate.fromString(bas, "yyyy-MM-dd")
        grup_kodu = f"ai-{sid}-{datetime.now().strftime('%H%M%S')}"
        self.yon.db.konaklama_ekle(sid, p['otel']['ad'], p['sehir'], bas, bit,
            p['otel']['fiyat'] * p['gun_sayisi'], p['otel']['yildiz'], "AI önerisi")
        for gd in p['gunluk_plan']:
            tarih = bas_q.addDays(gd['gun'] - 1).toString("yyyy-MM-dd") if bas_q.isValid() else gd['tarih_label']
            for sira, item in enumerate(gd['plan'], 1):
                if item.get("tur") == "aktivite":
                    self.yon.db.aktivite_ekle(
                        sid, item['baslik'], tarih, item['saat'],
                        item.get('konum', ''), item.get('fiyat', 0),
                        item.get('aciklama', ''), kaynak="ai", grup_kodu=grup_kodu
                    )
                else:
                    self.yon.db.plan_ekle(
                        sid, tarih, item['saat'], item['baslik'],
                        item.get('aciklama', ''), item.get('konum', ''),
                        kaynak="ai", kategori=item.get("kategori", "Plan"),
                        sira=sira, tarih=tarih, grup_kodu=grup_kodu
                    )
        self.yon.db.bildirim_ekle(self.yon.aktif_kullanici_id, "AI Plan 🤖",
            f"{p['sehir']} için {p['gun_sayisi']} günlük plan oluşturuldu!", "bilgi")
        QMessageBox.information(self, "✅", f"{p['sehir']} planı oluşturuldu!\n🏨 {p['otel']['ad']}\n"
                               f"💰 ~₺{p['tahmini_maliyet']['toplam']:,.0f}")
        if hasattr(pw, "olusturuldu"):
            pw.olusturuldu.emit(sid)
        elif hasattr(pw, "yukle") and hasattr(pw, "sid"):
            pw.yukle(sid)
        self.accept()


# ═══════════════════════════════════════════════════════════════════
#  PROFİL POPUP DİALOG
# ═══════════════════════════════════════════════════════════════════

class ProfilDialog(QDialog):
    profil_guncellendi = pyqtSignal()

    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon
        self.setWindowTitle("Profil")
        self.setFixedSize(520, 620)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: {T.CARD};
                border: none;
                border-radius: 24px;
            }}
        """)
        shadow(card, 50, 0, 15, QColor(0, 0, 0, 120 if T.AKTIF == 'dark' else 40))
        cl = QVBoxLayout(card)
        cl.setContentsMargins(32, 24, 32, 28)
        cl.setSpacing(12)

        # Header with close button
        hdr = QHBoxLayout()
        hdr.addWidget(make_label("👤 Profil", 20, True))
        hdr.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(36, 36)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: {T.BG3};
                border: none; border-radius: 18px;
                color: {T.TEXT2}; font-size: 16px; font-weight: 700;
            }}
            QPushButton:hover {{ background: {T.ROSE}; color: white; }}
        """)
        close_btn.clicked.connect(self.reject)
        hdr.addWidget(close_btn)
        cl.addLayout(hdr)
        cl.addSpacing(4)

        # Avatar
        ar = QHBoxLayout()
        ar.setAlignment(Qt.AlignCenter)
        self.avatar_lbl = QLabel("👤")
        self.avatar_lbl.setFixedSize(80, 80)
        self.avatar_lbl.setAlignment(Qt.AlignCenter)
        self.avatar_lbl.setStyleSheet(
            f"background:qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            f"stop:0 {T.G1},stop:1 {T.G2});"
            f"border:none;border-radius:40px;font-size:36px;"
        )
        ar.addWidget(self.avatar_lbl)
        cl.addLayout(ar)

        fb = make_btn("📷 Fotoğraf Yükle", False, h=34)
        fb.clicked.connect(self._foto_yukle)
        cl.addWidget(fb, alignment=Qt.AlignCenter)
        cl.addSpacing(4)

        for lbl, attr, ph, enabled in [
            ("Ad Soyad", "ad_inp", "Adınız", True),
            ("Kullanıcı Adı", "user_inp", "", False),
            ("E-posta", "email_inp", "E-posta", True),
            ("Telefon", "tel_inp", "Telefon", True),
        ]:
            cl.addWidget(make_label(lbl, 11, color=T.TEXT2))
            inp = make_input(ph)
            inp.setEnabled(enabled)
            inp.setFixedHeight(40)
            setattr(self, attr, inp)
            cl.addWidget(inp)

        cl.addSpacing(6)
        btn = make_btn("Profili Güncelle", True, "💾", h=44)
        btn.clicked.connect(self._guncelle)
        cl.addWidget(btn)

        outer.addWidget(card)
        self._yukle_veriler()

    def _yukle_veriler(self):
        u = self.yon.aktif_kullanici
        if u:
            self.ad_inp.setText(u.get("ad_soyad", ""))
            self.user_inp.setText(u.get("kullanici_adi", ""))
            self.email_inp.setText(u.get("email", ""))
            self.tel_inp.setText(u.get("telefon", ""))
            ap = u.get("avatar_path", "")
            if ap and os.path.exists(ap):
                pix = QPixmap(ap).scaled(80, 80, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                self.avatar_lbl.setPixmap(pix)
                self.avatar_lbl.setScaledContents(True)
                self.avatar_lbl.setStyleSheet("border:none;border-radius:40px;")
            avatar_label_uygula(self.avatar_lbl, ap, 80, "👤", 36)

    def _foto_yukle(self):
        path, _ = QFileDialog.getOpenFileName(self, "Profil Fotoğrafı", "",
                                               "Resimler (*.png *.jpg *.jpeg *.bmp *.webp)")
        if path and self.yon.aktif_kullanici_id:
            self.yon.db.kullanici_guncelle(self.yon.aktif_kullanici_id, avatar_path=path)
            self.yon.aktif_kullanici = dict(self.yon.db.kullanici_getir(self.yon.aktif_kullanici_id))
            pix = QPixmap(path).scaled(80, 80, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.avatar_lbl.setPixmap(pix)
            self.avatar_lbl.setScaledContents(True)
            self.avatar_lbl.setStyleSheet("border:none;border-radius:40px;")
            avatar_label_uygula(self.avatar_lbl, path, 80, "👤", 36)
            self.profil_guncellendi.emit()

    def _guncelle(self):
        if not self.yon.aktif_kullanici_id:
            return
        self.yon.db.kullanici_guncelle(
            self.yon.aktif_kullanici_id,
            ad_soyad=self.ad_inp.text().strip(),
            email=self.email_inp.text().strip(),
            telefon=self.tel_inp.text().strip()
        )
        self.yon.aktif_kullanici = dict(self.yon.db.kullanici_getir(self.yon.aktif_kullanici_id))
        QMessageBox.information(self, "✓", "Profil güncellendi!")
        self.profil_guncellendi.emit()
        self.accept()


# ═══════════════════════════════════════════════════════════════════
#  BİLDİRİM POPUP DİALOG
# ═══════════════════════════════════════════════════════════════════

class BildirimlerDialog(QDialog):
    def __init__(self, yon, parent=None):
        super().__init__(parent)
        self.yon = yon
        self.setWindowTitle("Bildirimler")
        self.setFixedSize(500, 550)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: {T.CARD};
                border: none;
                border-radius: 24px;
            }}
        """)
        shadow(card, 50, 0, 15, QColor(0, 0, 0, 120 if T.AKTIF == 'dark' else 40))
        cl = QVBoxLayout(card)
        cl.setContentsMargins(24, 20, 24, 24)
        cl.setSpacing(12)

        # Header with close button
        hdr = QHBoxLayout()
        hdr.addWidget(make_label("🔔 Bildirimler", 20, True))
        hdr.addStretch()
        ob = make_btn("Tümünü Oku", False, "✓", h=32)
        ob.clicked.connect(self._tmoku)
        hdr.addWidget(ob)
        hdr.addSpacing(8)
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(36, 36)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: {T.BG3};
                border: none; border-radius: 18px;
                color: {T.TEXT2}; font-size: 16px; font-weight: 700;
            }}
            QPushButton:hover {{ background: {T.ROSE}; color: white; }}
        """)
        close_btn.clicked.connect(self.reject)
        hdr.addWidget(close_btn)
        cl.addLayout(hdr)

        # Scroll area for notifications
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea{border:none;background:transparent;}")
        self.lw = QWidget()
        self.ll = QVBoxLayout(self.lw)
        self.ll.setSpacing(8)
        self.ll.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(self.lw)
        cl.addWidget(scroll, 1)

        outer.addWidget(card)
        self._yukle_liste()

    def _yukle_liste(self):
        while self.ll.count():
            it = self.ll.takeAt(0)
            if it.widget():
                it.widget().deleteLater()

        bl = self.yon.db.bildirimleri_getir(self.yon.aktif_kullanici_id)
        if not bl:
            empty = QLabel("Bildirim yok 🔕")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet(f"color:{T.TEXT3};font-size:14px;padding:40px;background:transparent;")
            self.ll.addWidget(empty)
            return

        for b in bl:
            c = QFrame()
            c.setFixedHeight(68)
            ok = b["okundu"]
            if not ok:
                c.setStyleSheet(
                    f"QFrame{{background:rgba(139,92,246,0.08);border:none;"
                    f"border-radius:14px;}}"
                )
            else:
                c.setStyleSheet(
                    f"QFrame{{background:{T.BG2 if T.AKTIF == 'dark' else T.BG3};"
                    f"border:none;border-radius:14px;}}"
                )
            row = QHBoxLayout(c)
            row.setContentsMargins(12, 8, 12, 8)
            ikon = {"seyahat": "✈️", "bilgi": "ℹ️"}.get(b["tur"], "🔔")
            row.addWidget(make_label(ikon, 20))
            row.addSpacing(6)
            left = QVBoxLayout()
            left.setSpacing(2)
            left.addWidget(make_label(b["baslik"], 13, True))
            left.addWidget(make_label(b["mesaj"] or "", 11, color=T.TEXT2))
            row.addLayout(left, 1)
            row.addWidget(make_label(str(b["tarih"])[:16] if b["tarih"] else "", 10, color=T.TEXT3))
            if not ok:
                dot = QFrame()
                dot.setFixedSize(8, 8)
                dot.setStyleSheet(f"background:{T.PRIMARY};border:none;border-radius:4px;")
                row.addWidget(dot)
            self.ll.addWidget(c)
        self.ll.addStretch()

    def _tmoku(self):
        if self.yon.aktif_kullanici_id:
            self.yon.db.tum_bildirimleri_oku(self.yon.aktif_kullanici_id)
            self._yukle_liste()


# ═══════════════════════════════════════════════════════════════════
#  ANA PENCERE
# ═══════════════════════════════════════════════════════════════════

class SeyahatApp(QMainWindow):
    def __init__(self, yon):
        super().__init__()
        self.yon = yon
        self._aktif_tema = "dark"
        tema_paleti_uygula(self._aktif_tema)
        self.setWindowTitle("✈️ TravelPlan — Seyahat Planlama")
        self.setMinimumSize(1200, 750); self.resize(1400, 850)
        QApplication.instance().setStyleSheet(DARK_QSS)
        self._build()

    def tema_degistir(self, tema):
        tema = "light" if tema == "light" else "dark"
        self._aktif_tema = tema
        tema_paleti_uygula(tema)
        if self.yon.aktif_kullanici_id:
            self.yon.db.kullanici_guncelle(self.yon.aktif_kullanici_id, tema=tema)
            if self.yon.aktif_kullanici:
                self.yon.aktif_kullanici["tema"] = tema

        hedef_ms = self.ms.currentIndex() if hasattr(self, "ms") else 0
        hedef_sayfa = self.cs.currentIndex() if hasattr(self, "cs") else 0
        detay_sid = self.pg[7].sid if hasattr(self, "pg") and len(self.pg) > 7 else None
        QApplication.instance().setStyleSheet(LIGHT_QSS if tema == "light" else DARK_QSS)

        eski = self.centralWidget()
        if eski:
            eski.deleteLater()
        self._build()

        if hedef_ms == 1:
            self.ms.setCurrentIndex(1)
            if hedef_sayfa == 7 and detay_sid:
                self._detay(detay_sid)
            else:
                self._sayfa(hedef_sayfa)
            self._profil_sidebar()
        else:
            self.ms.setCurrentIndex(0)

    def _build(self):
        cw = QWidget(); self.setCentralWidget(cw)
        ml = QHBoxLayout(cw); ml.setContentsMargins(0, 0, 0, 0); ml.setSpacing(0)

        self.auth = QStackedWidget()
        self.giris = GirisSayfasi(self.yon)
        self.kayit = KayitSayfasi(self.yon)
        self.auth.addWidget(self.giris); self.auth.addWidget(self.kayit)
        self.giris.giris_basarili.connect(self._giris_ok)
        self.giris.kayit_goster.connect(lambda: self.auth.setCurrentIndex(1))
        self.kayit.kayit_basarili.connect(lambda: self.auth.setCurrentIndex(0))
        self.kayit.giris_goster.connect(lambda: self.auth.setCurrentIndex(0))

        self.app_w = QWidget()
        al = QHBoxLayout(self.app_w); al.setContentsMargins(0, 0, 0, 0); al.setSpacing(0)
        self.sidebar = YanMenu(); self.sidebar.sayfa_degisti.connect(self._sayfa)
        al.addWidget(self.sidebar)

        self.cs = QStackedWidget()
        self.pg = [AnaSayfa(self.yon), SeyahatlerSayfasi(self.yon), YeniSeyahatSayfasi(self.yon),
                   HaritaSayfasi(self.yon), BildirimlerSayfasi(self.yon),
                   ProfilSayfasi(self.yon), AyarlarSayfasi(self.yon), SeyahatDetaySayfasi(self.yon)]
        for p in self.pg: self.cs.addWidget(p)
        al.addWidget(self.cs, 1)

        self.ms = QStackedWidget()
        self.ms.addWidget(self.auth); self.ms.addWidget(self.app_w)
        ml.addWidget(self.ms)

        self.pg[0].seyahat_detay.connect(self._detay)
        self.pg[0].yeni_seyahat.connect(lambda: self._sayfa(2))
        self.pg[0].profil_goster.connect(self._profil_popup)
        self.pg[0].bildirim_goster.connect(self._bildirim_popup)
        self.pg[1].seyahat_detay.connect(self._detay)
        self.pg[1].yeni_seyahat.connect(lambda: self._sayfa(2))
        self.pg[2].olusturuldu.connect(self._detay)
        self.pg[7].geri.connect(lambda: self._sayfa(1))
        self.pg[5].profil_guncellendi.connect(self._profil_sidebar)

    def _giris_ok(self):
        tema = (self.yon.aktif_kullanici or {}).get("tema", "dark")
        if tema not in {"dark", "light"}:
            tema = "dark"
        if tema != self._aktif_tema:
            self.tema_degistir(tema)
        self.ms.setCurrentIndex(1)
        self._yukle(0)
        self._bildirim()
        self._profil_sidebar()

    def _sayfa(self, idx):
        if idx == -1:
            self.yon.cikis_yap(); self.ms.setCurrentIndex(0); self.auth.setCurrentIndex(0); return
        self.sidebar.set_aktif(idx); self.cs.setCurrentIndex(idx); self._yukle(idx)

    def _yukle(self, idx):
        if idx == 0: self.pg[0].yukle()
        elif idx == 1: self.pg[1].yukle()
        elif idx == 3: self.pg[3].yukle()
        elif idx == 4: self.pg[4].yukle()
        elif idx == 5: self.pg[5].yukle()
        self._bildirim()

    def _detay(self, sid):
        self.pg[7].yukle(sid); self.cs.setCurrentIndex(7)

    def _bildirim(self):
        if self.yon.aktif_kullanici_id:
            n = self.yon.db.okunmamis_bildirimler(self.yon.aktif_kullanici_id)
            if hasattr(self.pg[0], "set_bildirim"):
                self.pg[0].set_bildirim(n)

    def _profil_sidebar(self):
        if self.yon.aktif_kullanici:
            if hasattr(self.pg[0], "set_kullanici"):
                self.pg[0].set_kullanici(self.yon.aktif_kullanici)

    def _profil_popup(self):
        dlg = ProfilDialog(self.yon, self)
        dlg.profil_guncellendi.connect(self._profil_sidebar)
        dlg.exec_()
        self._bildirim()

    def _bildirim_popup(self):
        dlg = BildirimlerDialog(self.yon, self)
        dlg.exec_()
        self._bildirim()
