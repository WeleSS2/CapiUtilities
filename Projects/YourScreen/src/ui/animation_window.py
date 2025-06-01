import os

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt, QSize

class AnimationWindow(QWidget):
    """
    A small window (frameless, always-on-top, transparent)
    that displays an animated GIF at its original size and positions itself
    in the bottom right corner of the screen. It can be freely dragged.
    """
    def __init__(self, gif_path: str):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._label = QLabel(self)
        self._label.setAttribute(Qt.WA_TransparentForMouseEvents)

        self._movie = QMovie(gif_path)
        if not self._movie.isValid():
            print(f"[AnimationWindow] Error: failed to load GIF: {gif_path}")
            return

        self._label.setMovie(self._movie)
        self._movie.start()

        self._initialized = False
        self._movie.frameChanged.connect(self._on_frame_changed)

        self._drag_offset = None

    def _on_frame_changed(self, frame_number: int):
        """Once the first frame is ready, set the window size and position."""
        if self._initialized:
            return

        pixmap = self._movie.currentPixmap()
        size = pixmap.size()

        self.setFixedSize(size)
        self._label.setFixedSize(size)

        screen_geom = self.screen().availableGeometry()
        x = screen_geom.x() + screen_geom.width() - size.width()
        y = screen_geom.y() + screen_geom.height() - size.height()
        self.move(x, y)

        self._initialized = True
        self._movie.frameChanged.disconnect(self._on_frame_changed)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_offset is not None and (event.buttons() & Qt.LeftButton):
            new_pos = event.globalPosition().toPoint() - self._drag_offset
            self.move(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_offset = None
            event.accept()