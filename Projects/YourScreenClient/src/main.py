import sys
import os
import threading
import keyboard

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.system_tray import SystemTray
from ui.toggle_window import ExpandWidget
from ui.counter_window import CounterWindow
from ui.animation_window import AnimationWindow

def register_global_shortcut(main_window: MainWindow):
    """Registers backtick (`) to toggle main window."""
    keyboard.add_hotkey('`', lambda: main_window.toggle_visibility_signal.emit())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("YourScreen")

    main_window = MainWindow()
    main_window.hide()

    counter_window = CounterWindow()
    counter_window.show()

    ExpandWidget(main_window)
    SystemTray(main_window)

    src_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.normpath(os.path.join(src_dir, "assets", "gfx", "character.gif"))
    if not os.path.exists(gif_path):
        print(f"[main.py] GIF not found: {gif_path}")
    else:
        anim_window = AnimationWindow(gif_path)
        anim_window.show()

    threading.Thread(
        target=register_global_shortcut,
        args=(main_window,),
        daemon=True
    ).start()

    sys.exit(app.exec())