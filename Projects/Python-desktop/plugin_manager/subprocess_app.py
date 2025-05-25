import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mod_name = sys.argv[1] if len(sys.argv) > 1 else "Unknown Mod"

    window = QMainWindow()
    window.setWindowTitle(f"Mod: {mod_name}")
    window.setWindowFlag(Qt.WindowStaysOnTopHint, True)

    label = QLabel(f"Mod process running: {mod_name}")
    label.setAlignment(Qt.AlignCenter)
    window.setCentralWidget(label)

    window.resize(300, 200)
    window.show()

    sys.exit(app.exec())