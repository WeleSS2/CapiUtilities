import sys
import ctypes

from ctypes import wintypes

from PySide6.QtWidgets import QWidget, QLabel, QApplication
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont

RIDEV_INPUTSINK        = 0x00000100
RID_INPUT              = 0x10000003
RIM_TYPEMOUSE          = 0
RIM_TYPEKEYBOARD       = 1
WM_INPUT               = 0x00FF

RI_MOUSE_BUTTON_1_DOWN = 0x0001
RI_MOUSE_BUTTON_2_DOWN = 0x0004

class RAWINPUTDEVICE(ctypes.Structure):
    _fields_ = [
        ("usUsagePage",   wintypes.USHORT),
        ("usUsage",       wintypes.USHORT),
        ("dwFlags",       wintypes.DWORD),
        ("hwndTarget",    wintypes.HWND),
    ]

class RAWINPUTHEADER(ctypes.Structure):
    _fields_ = [
        ("dwType",        wintypes.DWORD),
        ("dwSize",        wintypes.DWORD),
        ("hDevice",       wintypes.HANDLE),
        ("wParam",        wintypes.WPARAM),
    ]

class RAWMOUSE(ctypes.Structure):
    class _Data(ctypes.Union):
        _fields_ = [
            ("ulButtons",     wintypes.ULONG),
            ("usButtonFlags", wintypes.USHORT),
            ("usButtonData",  wintypes.USHORT),
        ]
    _anonymous_ = ("_data",)
    _fields_ = [
        ("usFlags",            wintypes.USHORT),
        ("_data",              _Data),
        ("ulRawButtons",       wintypes.ULONG),
        ("lLastX",             ctypes.c_long),
        ("lLastY",             ctypes.c_long),
        ("ulExtraInformation", wintypes.ULONG),
    ]

class RAWKEYBOARD(ctypes.Structure):
    _fields_ = [
        ("MakeCode",      wintypes.USHORT),
        ("Flags",         wintypes.USHORT),
        ("Reserved",      wintypes.USHORT),
        ("VKey",          wintypes.USHORT),
        ("Message",       wintypes.UINT),
        ("ExtraInformation", wintypes.ULONG),
    ]

class RAWINPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mouse",    RAWMOUSE),
        ("keyboard", RAWKEYBOARD),
    ]

class RAWINPUT(ctypes.Structure):
    _anonymous_ = ("data",)
    _fields_ = [
        ("header",   RAWINPUTHEADER),
        ("data",     RAWINPUT_UNION),
    ]

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

GetRawInputData = user32.GetRawInputData
GetRawInputData.argtypes = [
    wintypes.HANDLE,
    wintypes.UINT,
    wintypes.LPVOID,
    ctypes.POINTER(wintypes.UINT),
    wintypes.UINT
]
GetRawInputData.restype = wintypes.UINT

RegisterRawInputDevices = user32.RegisterRawInputDevices
RegisterRawInputDevices.argtypes = [
    ctypes.POINTER(RAWINPUTDEVICE),
    wintypes.UINT,
    wintypes.UINT
]
RegisterRawInputDevices.restype = wintypes.BOOL

class CounterWindow(QWidget):
    """
    Window that counts global mouse clicks and key presses,
    implemented using Raw Input (WM_INPUT). Does not require Administrator privileges.
    """
    global_click_signal = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Click Counter")
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(200, 80)

        self.counter = 0
        self.label = QLabel(f"{self.counter}", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 180);
                border-radius: 8px;
                padding: 5px;
            }
        """)
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setGeometry(0, 0, 200, 80)

        self._pressed_vkeys = set()

        self._move_to_top_center()

        self.global_click_signal.connect(self._increment_counter)

        ok = self._register_raw_input()
        if not ok:
            print("⚠️ RAWINPUT registration failed. Clicks and keys will not be counted.")
        else:
            print("✅ RAWINPUT registered: listening for mouse and keyboard.")

    def _move_to_top_center(self):
        """Moves the counter window (200×80) to the center of the screen, 10 px from the top."""
        screen_geom = QApplication.primaryScreen().availableGeometry()
        x = (screen_geom.width() - self.width()) // 2
        y = 10
        self.move(x, y)

    def _register_raw_input(self) -> bool:
        """
        Registers Raw Input for keyboard (UsagePage=1, Usage=6)
        and mouse (UsagePage=1, Usage=2) with the RIDEV_INPUTSINK flag.
        """
        rid = (RAWINPUTDEVICE * 2)()

        rid[0].usUsagePage = 0x01
        rid[0].usUsage     = 0x06
        rid[0].dwFlags     = RIDEV_INPUTSINK
        rid[0].hwndTarget  = wintypes.HWND(int(self.winId()))

        rid[1].usUsagePage = 0x01
        rid[1].usUsage     = 0x02
        rid[1].dwFlags     = RIDEV_INPUTSINK
        rid[1].hwndTarget  = wintypes.HWND(int(self.winId()))

        ok = RegisterRawInputDevices(rid, 2, ctypes.sizeof(RAWINPUTDEVICE))
        if not ok:
            err = kernel32.GetLastError()
            print(f"[CounterWindow] RegisterRawInputDevices error: {err}")
            return False
        return True

    def nativeEvent(self, eventType, message):
        """
        Intercepts native Windows messages; we're interested in WM_INPUT.
        Upon receiving WM_INPUT, calls _process_raw_input.
        """
        msg_ptr = ctypes.cast(int(message), ctypes.POINTER(wintypes.MSG))
        msg = msg_ptr.contents
        if msg.message == WM_INPUT:
            self._process_raw_input(msg.lParam)
        return False, 0

    def _process_raw_input(self, hRawInput):
        """
        Called on WM_INPUT: retrieves RAWINPUT and analyzes:
         • mouse → LMB/RMB Down?
         • keyboard → KeyDown (once per physical press)
        """
        size = wintypes.UINT(0)
        res = GetRawInputData(
            wintypes.HANDLE(hRawInput),
            wintypes.UINT(RID_INPUT),
            None,
            ctypes.byref(size),
            ctypes.sizeof(RAWINPUTHEADER)
        )
        if size.value == 0:
            return

        buf = ctypes.create_string_buffer(size.value)
        res = GetRawInputData(
            wintypes.HANDLE(hRawInput),
            wintypes.UINT(RID_INPUT),
            buf,
            ctypes.byref(size),
            ctypes.sizeof(RAWINPUTHEADER)
        )
        if res == 0 or res == wintypes.UINT(-1).value:
            return

        raw = ctypes.cast(buf, ctypes.POINTER(RAWINPUT)).contents

        if raw.header.dwType == RIM_TYPEMOUSE:
            mouse_data = raw.data.mouse
            flags = mouse_data.usButtonFlags
            if (flags & RI_MOUSE_BUTTON_1_DOWN) == RI_MOUSE_BUTTON_1_DOWN:
                self.global_click_signal.emit()
            elif (flags & RI_MOUSE_BUTTON_2_DOWN) == RI_MOUSE_BUTTON_2_DOWN:
                self.global_click_signal.emit()

        elif raw.header.dwType == RIM_TYPEKEYBOARD:
            key_data = raw.data.keyboard
            vkey = key_data.VKey
            msg  = key_data.Message
            if msg == 0x0100 or msg == 0x0104:
                if vkey not in self._pressed_vkeys:
                    self._pressed_vkeys.add(vkey)
                    self.global_click_signal.emit()
            elif msg == 0x0101 or msg == 0x0105:
                self._pressed_vkeys.discard(vkey)

    @Slot()
    def _increment_counter(self):
        """
        Qt slot in the GUI thread; increments the counter and refreshes the QLabel.
        """
        self.counter += 1
        self.label.setText(f"{self.counter}")

    def closeEvent(self, event):
        """
        On close, unbind Raw Input (not necessary since process ends, but done for completeness).
        """
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CounterWindow()
    w.show()
    sys.exit(app.exec())