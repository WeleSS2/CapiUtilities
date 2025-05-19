# plugin_object.py
import multiprocessing
from enum import Enum
from pathlib import Path
from typing import Optional, Any


class PluginStatus(Enum):
    NOT_LOADED = "not_loaded"
    LOADED = "loaded"
    FAILED = "failed"
    RUNNING = "running"
    STOPPED = "stopped"


class PluginObject:
    def __init__(self, plugin_dir: Path):
        self.plugin_dir: Path = plugin_dir
        self.plugin_name: str = plugin_dir.name

        self.process: Optional[multiprocessing.Process] = None
        self.connection: Optional[multiprocessing.connection.Connection] = None

        self.metadata: dict[str, Any] = {}
        self.widget_blueprint: Optional[dict] = None
        self.status: PluginStatus = PluginStatus.NOT_LOADED

    def load_metadata(self):
        manifest = self.plugin_dir / "manifest.json"
        if manifest.exists():
            import json
            with open(manifest, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                "name": self.plugin_name,
                "version": "unknown",
                "author": "unknown",
                "description": ""
            }

    def __repr__(self):
        return f"<PluginObject {self.plugin_name} status={self.status}>"
