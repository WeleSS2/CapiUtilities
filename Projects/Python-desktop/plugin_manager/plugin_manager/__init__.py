"""
capi_manager - GUI process manager with overlay and system tray integration.
"""

from .main_window import MainWindow
from .toggle_window import ExpandWidget
from .system_tray import SystemTray

__all__ = ["MainWindow", "ExpandWidget", "SystemTray"]