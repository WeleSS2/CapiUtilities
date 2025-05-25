import os
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

class SystemTray(QSystemTrayIcon):
    """System tray icon with Show/Hide and Exit options."""

    def __init__(self, main_window):
        icon_path = os.path.join(
            os.path.dirname(__file__),
            os.pardir, 'assets', 'tray_icon.ico'
        )
        super().__init__(QIcon(icon_path), main_window)
        self.main_window = main_window

        menu = QMenu()
        show_hide = QAction("Show/Hide", main_window)
        show_hide.triggered.connect(self.main_window.toggle_visibility)
        exit_act = QAction("Exit", main_window)
        exit_act.triggered.connect(QApplication.quit)

        menu.addAction(show_hide)
        menu.addSeparator()
        menu.addAction(exit_act)

        self.setContextMenu(menu)
        self.setToolTip("Plugin Manager")
        self.activated.connect(self._on_activated)
        self.show()

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.main_window.toggle_visibility()