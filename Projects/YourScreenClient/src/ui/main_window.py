import sys
import os
import glob

from PySide6.QtWidgets import (QMainWindow, QWidget,
QVBoxLayout, QHBoxLayout, QScrollArea, QCheckBox, QFrame, QLabel)

from PySide6.QtCore import Qt, QProcess, Signal, QTimer, QSize

from PySide6.QtGui import (QPixmap, QMovie, QPainter, QPainterPath,
QColor, QPaintEvent)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBPROCESS_APP_PATH = os.path.join(BASE_DIR, "subprocess_app.py")

class RoundedBackground(QWidget):
    def __init__(self, image_path=None, radius=15, overlay_opacity=1.0, parent=None):
        super().__init__(parent)
        self.radius = radius
        self.overlay_opacity = overlay_opacity
        self.pixmap = None
        self.movie = None
        if image_path and os.path.exists(image_path):
            ext = os.path.splitext(image_path)[1].lower()
            if ext == '.gif':
                self.movie = QMovie(image_path)
                self.movie.setScaledSize(QSize(400, 600))
                self.movie.frameChanged.connect(self.update)
                self.movie.start()
            else:
                self.pixmap = QPixmap(image_path).scaled(
                    400, 600,
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, ev: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(rect, self.radius, self.radius)
        painter.setClipPath(path)

        painter.setOpacity(self.overlay_opacity)

        if self.movie:
            frame = self.movie.currentPixmap()
            painter.drawPixmap(rect, frame)
        elif self.pixmap:
            painter.drawPixmap(rect, self.pixmap)
        else:
            painter.fillPath(path, QColor(0, 0, 0, int(255 * self.overlay_opacity)))

        painter.setOpacity(1.0)
        painter.end()

class MainWindow(QMainWindow):
    toggle_visibility_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 600)
        self._drag_pos = None
        self.toggle_visibility_signal.connect(self.toggle_visibility)

        self.processes = {}
        self.checkboxes = {}

        central = QWidget(self)
        central.setObjectName("central")
        central.setStyleSheet("#central { background-color: transparent; }")
        central.setFixedSize(400, 600)
        self.setCentralWidget(central)

        bg = RoundedBackground(
            image_path=None,
            radius=15,
            overlay_opacity=0.4,
            parent=central
        )
        bg.setGeometry(0, 0, 400, 600)
        bg.lower()

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        container.setAttribute(Qt.WA_TranslucentBackground)
        grid = QVBoxLayout(container)

        for i in range(101):
            name = f"Mod {i}"
            row = QFrame()
            row.setFrameShape(QFrame.StyledPanel)
            row.setStyleSheet("background: transparent;")
            h = QHBoxLayout(row)
            h.setContentsMargins(5, 5, 5, 5)

            lbl = QLabel(name)
            lbl.setStyleSheet("background: transparent; color: white;")
            h.addWidget(lbl)
            h.addStretch()

            sw = QCheckBox()
            sw.setFixedSize(40, 20)
            sw.setStyleSheet(
                "QCheckBox::indicator{width:40px;height:20px;border-radius:10px;}"
                "QCheckBox::indicator:unchecked{background:darkred;}"
                "QCheckBox::indicator:checked{background:darkgreen;}"
            )
            sw.toggled.connect(lambda on, n=name: self.toggle_mod(n, on))
            self.checkboxes[name] = sw
            h.addWidget(sw)

            placeholder = QLabel("")
            placeholder.setFixedSize(60, 20)
            placeholder.setStyleSheet(
                "background: rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.3);"
            )
            h.addWidget(placeholder)

            grid.addWidget(row)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)

    def toggle_mod(self, mod, enabled):
        if enabled:
            p = QProcess(self)
            p.start(sys.executable, [SUBPROCESS_APP_PATH, mod])
            p.started.connect(lambda: None)
            p.finished.connect(lambda c, s, n=mod: self.cleanup_process(n))
            self.processes[mod] = p
        else:
            p = self.processes.get(mod)
            if p and p.state() != QProcess.NotRunning:
                p.terminate()
                QTimer.singleShot(2000, lambda pr=p: pr.kill())

    def cleanup_process(self, mod):
        cb = self.checkboxes.get(mod)
        if cb:
            cb.blockSignals(True)
            cb.setChecked(False)
            cb.blockSignals(False)
        self.processes.pop(mod, None)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
            e.accept()

    def mouseMoveEvent(self, e):
        if self._drag_pos and e.buttons() & Qt.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)
            e.accept()

    def mouseReleaseEvent(self, e):
        self._drag_pos = None
        e.accept()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def closeEvent(self, ev):
        for p in self.processes.values():
            if p.state() != QProcess.NotRunning:
                p.kill()
        super().closeEvent(ev)