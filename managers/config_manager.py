import os
import json
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.default_config = {
            "theme": "dark",
            "voice_enabled": True,
            "window_width": 700,
            "window_height": 600
        }
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    return {**self.default_config, **loaded}
        except Exception as e:
            print(f"配置加载失败: {e}")
        return self.default_config.copy()

    def save_config(self) -> None:
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"配置保存失败: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.save_config()