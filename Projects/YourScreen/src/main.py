import sys
import threading
import keyboard
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.system_tray import SystemTray
from ui.toggle_window import ExpandWidget

def register_global_shortcut(main_window: MainWindow):
    """Registers backtick (`) to toggle main window."""
    keyboard.add_hotkey('`', lambda: main_window.toggle_visibility_signal.emit())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.hide()

    ExpandWidget(main_window)
    SystemTray(main_window)

    threading.Thread(
        target=register_global_shortcut,
        args=(main_window,),
        daemon=True
    ).start()

    sys.exit(app.exec())