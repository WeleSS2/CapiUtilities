from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QRegion
from PySide6.QtCore import Qt

class ExpandWidget(QWidget):
    """Invisible overlay to capture global hotkey region for toggling window."""
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setFixedSize(1, 1)
        self.move(0, 0)
        self.setMask(QRegion(0, 0, 1, 1))
        self.show()

    def mousePressEvent(self, event):
        self.main_window.toggle_visibility()