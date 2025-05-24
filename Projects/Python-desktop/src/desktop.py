# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

# This file is example code of qt using basic PySide6 functionality.

from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QRegion, QGuiApplication

import os
import json
from pysite.q_widget import q_widget

class ToggleWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        screen_geometry = QGuiApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        print (f"Screen size: {screen_width}x{screen_height}")
        self.setFixedSize(screen_width, screen_height)

        self.expanded = False  # Start in compact mode

        # Button for expanded mode
        self.button = QPushButton("Click Me", self)
        self.button.move(100, 80)
        self.button.clicked.connect(lambda: (
            print("Button clicked"),
            setattr(self, 'expanded', False),
            self.apply_compact_mode()
        ))
        self.button.hide()  # Hidden in compact mode

        self.apply_compact_mode()

    def apply_compact_mode(self):
        """Only top-left 10x10 is active and visible"""
        self.setMask(QRegion(QRect(0, 0, 10, 10)))
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.button.hide()
        self.update()

    def apply_expanded_mode(self):
        """Whole window is visible and interactive"""
        self.setMask(QRegion(self.rect()))
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.button.show()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.expanded:
            # Semi-transparent black background
            painter.fillRect(self.rect(), QColor(0, 0, 0, 160))
        else:
            # Only small red square
            painter.setBrush(QColor(255, 0, 0, 255))
            painter.setPen(Qt.NoPen)
            painter.drawRect(0, 0, 10, 10)

    def mousePressEvent(self, event):
        if not self.expanded and QRect(0, 0, 10, 10).contains(event.pos()):
            self.expanded = True
            self.apply_expanded_mode()

# -------------------------------------------------------------------------

def load_plugins(plugins_dir='plugins'):
    """
    Load plugins from the specified directory.
    Each plugin should be a directory containing a config.json file.
    """
    if not os.path.isdir(plugins_dir):
        print(f"[load_plugins] Plugins directory not found: {plugins_dir}")
        return []

    widgets = []
    for name in os.listdir(plugins_dir):
        path = os.path.join(plugins_dir, name)
        if os.path.isdir(path):
            cfg = os.path.join(path, 'config.json')
            if os.path.isfile(cfg):
                try:
                    with open(cfg, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    widget = q_widget(**config)
                    widgets.append(widget)
                    print(f"[load_plugins] Load plugin '{name}': {widget}")
                except Exception as e:
                    print(f"[load_plugins] Failed to load plugin '{name}': {e}")
            else:
                print(f"[load_plugins] config.json not found for plugin '{name}', skip.")
    return widgets

if __name__ == "__main__":
    app = QApplication([])
    window = ToggleWindow()
    window.show()

    load_plugins(os.path.join(os.path.dirname(__file__), 'plugins'))

    app.exec()
