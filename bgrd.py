import sys
import random
import datetime
import webbrowser
from typing import List

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox, QTextEdit, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QFont, QMovie, QTextCursor, QPixmap

from asset_manager import AssetManager
from config_manager import ConfigManager
from theme_manager import ThemeManager
from voice_manager import VoiceManager
from settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.version = "5.3"
        self.config = ConfigManager()
        self.assets = AssetManager()
        self.theme_manager = ThemeManager(self.config)
        self.voice = VoiceManager(self.config)

        self.setWindowTitle("丐点名将")
        self.resize(self.config.get("window_width", 800), self.config.get("window_height", 600))
        self.setMinimumSize(500, 400)

        icon_path = self.assets.check_file("dec.ico")
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(20, 10, 20, 20)
        self.main_layout.setSpacing(10)

        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        header_layout = QHBoxLayout()

        self.title_label = QLabel("丐点名将")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setFont(QFont("微软雅黑", 24, QFont.Bold))
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setObjectName("SettingsButton")
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.clicked.connect(self.open_settings)
        header_layout.addWidget(self.settings_btn)

        self.main_layout.addLayout(header_layout)

        # 结果显示容器
        self.result_container = QFrame()
        self.result_container.setObjectName("ResultContainer")
        self.result_container.setFrameShape(QFrame.StyledPanel)
        self.result_layout = QVBoxLayout(self.result_container)
        self.result_layout.setContentsMargins(0, 0, 0, 0)

        # GIF 标签
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.hide()
        self.result_layout.addWidget(self.gif_label)

        # 结果文本框
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("微软雅黑", 36, QFont.Bold))
        self.result_text.setAlignment(Qt.AlignCenter)
        self.result_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.result_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.result_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.result_text.setHtml("<p align='center' style='color: gray;'>别紧张！</p>")
        self.result_layout.addWidget(self.result_text)

        self.main_layout.addWidget(self.result_container, 1)

        # 控制区域
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 20, 0, 0)

        count_label = QLabel("抽选人数:")
        count_label.setFont(QFont("微软雅黑", 14))
        control_layout.addWidget(count_label)

        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 999)
        self.count_spin.setValue(1)
        self.count_spin.setFixedWidth(100)
        self.count_spin.setFixedHeight(40)
        self.count_spin.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(self.count_spin)

        control_layout.addStretch()

        self.start_btn = QPushButton("开始抽选")
        self.start_btn.setObjectName("StartButton")
        self.start_btn.setFont(QFont("微软雅黑", 14))
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.clicked.connect(self.start_pick)
        control_layout.addWidget(self.start_btn)

        self.main_layout.addLayout(control_layout)

    def apply_theme(self):
        self.setStyleSheet(self.theme_manager.get_style_sheet())

    def open_settings(self):
        dlg = SettingsDialog(self, self.config, self.theme_manager)
        dlg.exec()

    def load_names(self) -> List[str]:
        path = self.assets.resource_path("names.txt")
        with open(path, 'r', encoding='utf-8') as f:
            names = [line.strip() for line in f if line.strip()]
        return names

    def start_pick(self):
        names = self.load_names()
        count = self.count_spin.value()
        if count > len(names):
            self.count_spin.setMaximum(len(names))
            count = len(names)
            self.count_spin.setValue(count)

        self.result_text.hide()
        self.gif_label.show()

        gif_path = self.assets.resource_path("now-loading.gif")
        movie = QMovie(gif_path)
        movie.setCacheMode(QMovie.CacheAll)
        self.gif_label.setMovie(movie)
        movie.start()

        self.start_btn.setEnabled(False)
        QTimer.singleShot(2000, lambda: self.show_result(names, count, movie))

    def show_result(self, names, count, movie):
        movie.stop()
        self.gif_label.hide()
        self.result_text.show()

        selected = random.sample(names, count)
        text_content = "<p align='center'>" + "<br>".join(selected) + "</p>"
        self.result_text.setHtml(text_content)

        self.result_text.document().setTextWidth(self.result_text.viewport().width())
        self.result_text.moveCursor(QTextCursor.MoveOperation.Start)
        self.result_text.ensureCursorVisible()

        self.start_btn.setEnabled(True)
        self.voice.speak(selected)

    def closeEvent(self, event):
        self.config.set("window_width", self.width())
        self.config.set("window_height", self.height())
        self.voice.shutdown()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("微软雅黑", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())