from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget,
    QHBoxLayout, QVBoxLayout, QSizePolicy, QCheckBox,
    QLabel, QScrollArea, QFrame, QListWidget, QGridLayout,
    QStackedLayout, QFrame, QLineEdit
)
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtCore import Qt, QSize, QTimer
import sys
import os

global base_Width, base_Height

class GameList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # ✨ Add this:
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        # Dummy game icons
        game_icons = ["game1.png", "game2.png", "game3.png"]

        for icon_path in game_icons:
            btn = QPushButton()
            btn.setFixedSize(64, 64)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(64, 64))
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.clicked.connect(lambda checked=False, p=icon_path: self.run_game(p))
            layout.addWidget(btn)

    def run_game(self, game_icon):
        print(f"TODO: Launch game with icon {game_icon}")

class ToolboxPanel(QWidget):
    def __init__(self, parent, on_sort_callback, on_search_callback):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        self.setLayout(layout)

        sort_name = QPushButton("Sort by Name")
        sort_name.clicked.connect(lambda: on_sort_callback("col2"))
        layout.addWidget(sort_name)

        sort_active = QPushButton("Sort by Active")
        sort_active.clicked.connect(lambda: on_sort_callback("active"))
        layout.addWidget(sort_active)

        sort_col3 = QPushButton("Sort by A")
        sort_col3.clicked.connect(lambda: on_sort_callback("col3"))
        layout.addWidget(sort_col3)

        sort_col4 = QPushButton("Sort by B")
        sort_col4.clicked.connect(lambda: on_sort_callback("col4"))
        layout.addWidget(sort_col4)

        sort_col5 = QPushButton("Sort by C")
        sort_col5.clicked.connect(lambda: on_sort_callback("col5"))
        layout.addWidget(sort_col5)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(on_search_callback)
        layout.addWidget(self.search_input)

        layout.addStretch()

class ModRow(QWidget):
    def __init__(self, row_index, entry):
        super().__init__()
        self.row_index = row_index
        self.entry = entry

        self.setFixedHeight(36)  # Or make dynamic
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(10)
        
        self.setLayout(layout)

        # First column - checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked {
                background-color: limegreen;
                border: 1px solid #aaa;
            }
            QCheckBox::indicator:unchecked {
                background-color: transparent;
                border: 1px solid #666;
            }
        """)
        self.checkbox.setChecked(entry["active"])
        layout.addWidget(self.checkbox)

        # Middle columns - labels (placeholder content)
        for i, key in enumerate(["col2", "col3", "col4", "col5"]):
            label = QLabel(entry[key])
            label.setStyleSheet("color: white;")
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            layout.addWidget(label)

        # Last column - move button
        self.move_button = QPushButton("⇅")
        self.move_button.setFixedSize(30, 25)
        self.move_button.clicked.connect(self.move_row)
        layout.addWidget(self.move_button)

        # Enable mouse tracking
        self.setMouseTracking(True)

    def move_row(self):
        print(f"TODO: Move row {self.row_index}")

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            print(f"TODO: Right-click action on row {self.row_index}")
        elif event.button() == Qt.LeftButton:
            print(f"TODO: Left-click toggle for row {self.row_index}")
            if not self.childAt(event.pos()) == self.move_button:
                self.checkbox.setChecked(not self.checkbox.isChecked())

class ModsList(QWidget):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(4)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.6);")
        self.container.setStyleSheet("background: transparent;")
        scroll.setWidget(self.container)

        # Use provided data or fallback to 30 placeholders
        if data is None:
            data = [
                {"active": False, "col2": f"Mod {i}", "col3": "A", "col4": "B", "col5": "C"}
                for i in range(30)
            ]
        self.all_mods_data = data or [ ... ]
        self.mods_data = self.all_mods_data.copy()
        self.populate_rows(self.mods_data)

    def set_data(self, new_data):
        self.all_mods_data = new_data
        self.mods_data = new_data.copy()
        self.populate_rows(self.mods_data)


    def populate_rows(self, data_list):
        # Clear layout
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for index, entry in enumerate(data_list):
            row = ModRow(index, entry)
            self.container_layout.addWidget(row)

            if index < len(data_list) - 1:
                separator = QFrame()
                separator.setFixedHeight(1)
                separator.setStyleSheet("background-color: rgba(255,255,255,0.15);")
                self.container_layout.addWidget(separator)

    def sync_data_from_ui(self):
        updated_data = []

        for i in range(self.container_layout.count()):
            widget = self.container_layout.itemAt(i).widget()
            if isinstance(widget, ModRow):
                updated = {
                    "active": widget.checkbox.isChecked(),
                    "col2": widget.entry["col2"],
                    "col3": widget.entry["col3"],
                    "col4": widget.entry["col4"],
                    "col5": widget.entry["col5"],
                }
                updated_data.append(updated)

        # ✅ Replace matching entries in all_mods_data
        name_to_row = {entry["col2"]: entry for entry in updated_data}
        for i, entry in enumerate(self.all_mods_data):
            if entry["col2"] in name_to_row:
                self.all_mods_data[i] = name_to_row[entry["col2"]]

        self.mods_data = updated_data  # optional: temporary current view




class EntryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(300, 300)  # Reserve total space

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

        # Container with fixed height
        self.list_container = QFrame()
        self.list_container.setFixedHeight(100)

        list_layout = QVBoxLayout(self.list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)

        self.entry_list = QListWidget()
        self.entry_list.addItems([f"Item {i}" for i in range(10)])
        list_layout.addWidget(self.entry_list)

        main_layout.addWidget(self.list_container)

        # Hide list content, keep space
        self.entry_list.setVisible(False)

        # Toggle button
        toggle_button = QPushButton("Show List")
        toggle_button.clicked.connect(self.toggle_list)
        main_layout.addWidget(toggle_button)

        # 2x2 grid for buttons
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        for i in range(2):
            for j in range(2):
                btn = QPushButton(f"Btn {i*2 + j + 1}")
                btn.setFixedSize(120, 40)
                grid_layout.addWidget(btn, i, j)

        main_layout.addLayout(grid_layout)

    def toggle_list(self):
        is_visible = self.entry_list.isVisible()
        self.entry_list.setVisible(not is_visible)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fullscreen Game Launcher")
        self.mods_data = [
            {"active": False, "col2": f"Mod {i}", "col3": "Value A", "col4": "Value B", "col5": "Value C"}
            for i in range(30)
        ]

        # Central layout
        self.central = QWidget(self)
        self.setCentralWidget(self.central)
        self.central.setObjectName("main_window")
        self.central.setStyleSheet("""
            #main_window {
                background-image: url('gfx/background_1142710.png');
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
            }
        """)
        self.main_layout = QVBoxLayout(self.central)

        # Game list (fixed height: 64px)
        self.game_list = GameList()

        self.game_list.setFixedHeight(64)
        self.main_layout.addWidget(self.game_list)

        # Toolbox Panel (sorting)
        self.toolbox = ToolboxPanel(self, self.sort_mods, self.search_mods)
        self.main_layout.addWidget(self.toolbox)

        # Mods list (expand to fill remaining space)
        self.mods_list = ModsList()
        self.mods_list.setFixedWidth(base_Width * 60)
        self.main_layout.addWidget(self.mods_list)

        # EntryPanel instance
        self.entry_panel = EntryPanel(self)
        self.entry_panel.resize(300, 300)  # Fixed size (can adjust later)

        # Close button
        self.close_button = QPushButton("X", self)
        self.close_button.setFixedSize(40, 30)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.close_button.setVisible(False)

        QTimer.singleShot(0, self.show_fullscreen_with_button)

    def show_fullscreen_with_button(self):
        self.showFullScreen()
        self.position_close_button()
        self.close_button.setVisible(True)
        self.close_button.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.mods_list.setFixedWidth(base_Width * 60)
        self.position_close_button()

        x = self.width() - self.entry_panel.width() - (base_Width * 2)
        y = self.height() - self.entry_panel.height() - (base_Height * 2)

        self.entry_panel.move(x, y)

    def position_close_button(self):
        margin = 10
        x = self.width() - self.close_button.width() - margin
        y = margin
        self.close_button.move(x, y)
        self.close_button.raise_()

    def sort_mods(self, key):
        self.mods_list.sync_data_from_ui()

        # Sort active mods first if sorting by 'active'
        reverse = key == "active"

        self.mods_list.mods_data.sort(key=lambda x: x[key], reverse=reverse)
        self.mods_list.populate_rows(self.mods_list.mods_data)

    def search_mods(self, text):
        text = text.lower().strip()
    
        # ✅ Always sync first
        self.mods_list.sync_data_from_ui()
    
        if not text:
            self.mods_list.populate_rows(self.mods_list.all_mods_data)
        else:
            filtered = [
                entry for entry in self.mods_list.all_mods_data
                if any(text in str(value).lower() for value in entry.values())
            ]
            self.mods_list.populate_rows(filtered)


def calculate_one_percent_of_screen():
    global base_Width, base_Height
    screen_geometry = QGuiApplication.primaryScreen().geometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()
    
    base_Width = screen_width * 0.01
    base_Height = screen_height * 0.01

if __name__ == "__main__":
    app = QApplication(sys.argv)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    calculate_one_percent_of_screen()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
