from config_manager import ConfigManager

class ThemeManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.is_dark = config.get("theme") == "dark"

    def toggle(self):
        self.is_dark = not self.is_dark
        self.config.set("theme", "dark" if self.is_dark else "light")
        return self.is_dark

    def get_style_sheet(self) -> str:
        if self.is_dark:
            bg = "#1e1e1e"
            fg = "#dcdcdc"
            accent = "#4a90e2"
            sec_bg = "#2d2d2d"
            entry_bg = "#3c3c3c"
            border = "#3e3e3e"
        else:
            bg = "#f5f5f5"
            fg = "#333333"
            accent = "#007acc"
            sec_bg = "#ffffff"
            entry_bg = "#ffffff"
            border = "#cccccc"

        return f"""
            QMainWindow, QDialog {{ background-color: {bg}; color: {fg}; }}
            QWidget {{ background-color: {bg}; color: {fg}; }}
            QLabel {{ color: {fg}; }}
            QLabel#TitleLabel {{ color: {accent}; font-weight: bold; }}
            QLabel#ResultPlaceholder {{ color: {fg}; font-weight: bold; }}
            
            QPushButton {{
                background-color: {sec_bg};
                border: 1px solid {border};
                border-radius: 4px;
                padding: 5px;
                color: {fg};
            }}
            QPushButton:hover {{ background-color: {accent}; color: white; border: 1px solid {accent}; }}
            QPushButton#StartButton {{
                background-color: {accent};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 10px 30px;
            }}
            QPushButton#StartButton:hover {{ background-color: #357abd; }}
            QPushButton#StartButton:pressed {{ background-color: #2a6298; }}
            
            QPushButton#SettingsButton {{
                background-color: transparent;
                border: none;
                color: {accent};
                font-size: 24px;
            }}
            QPushButton#SettingsButton:hover {{ color: {fg}; }}

            QTextEdit {{
                background-color: {sec_bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 4px;
            }}
            
            QSpinBox {{
                background-color: {entry_bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 4px;
                padding: 5px;
                font-size: 16pt;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                width: 30px;
            }}
            
            QCheckBox {{
                spacing: 10px;
                font-size: 14pt;
            }}
            QCheckBox::indicator {{
                width: 40px;
                height: 25px;
            }}
        """