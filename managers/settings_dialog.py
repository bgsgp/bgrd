# managers/settings_dialog.py
import datetime
import webbrowser

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap

from managers.config_manager import ConfigManager
from managers.theme_manager import ThemeManager  # 假设也将 ThemeManager 移到了单独文件


class SettingsDialog(QDialog):
    def __init__(self, parent, config: ConfigManager, theme_manager: ThemeManager):
        super().__init__(parent)
        self.config = config
        self.theme_manager = theme_manager
        self.setWindowTitle("设置")
        self.setFixedSize(450, 500)
        self.parent_window = parent  # 主窗口引用，用于获取 assets 和 version

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title_label = QLabel("功能设置")
        title_label.setFont(QFont("微软雅黑", 14, QFont.Bold))
        main_layout.addWidget(title_label)

        # 功能设置：语音播报开关
        self.voice_cb = QCheckBox("语音播报")
        self.voice_cb.setChecked(self.config.get("voice_enabled", True))
        self.voice_cb.toggled.connect(lambda v: self.config.set("voice_enabled", v))
        self.voice_cb.setCursor(Qt.PointingHandCursor)
        main_layout.addWidget(self.voice_cb)

        # 主题开关
        self.theme_cb = QCheckBox("暗夜模式")
        self.theme_cb.setChecked(self.theme_manager.is_dark)
        self.theme_cb.toggled.connect(self.on_theme_toggled)
        self.theme_cb.setCursor(Qt.PointingHandCursor)
        main_layout.addWidget(self.theme_cb)

        # 分割线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # “其它”标题
        other_label = QLabel("其它")
        other_label.setFont(QFont("微软雅黑", 14, QFont.Bold))
        main_layout.addWidget(other_label)

        # 官方网站（图片链接）
        official_layout = QHBoxLayout()
        official_label = QLabel("官方网站:")
        official_label.setStyleSheet("font-weight: bold;")
        official_layout.addWidget(official_label)

        # 加载 itn.png 图片，缩小至原尺寸的 1/4
        itn_path = self.parent_window.assets.check_file("itn.png")
        if itn_path:
            website_label = QLabel()
            pixmap = QPixmap(itn_path)
            # 原尺寸 149x153，缩小为 1/4：约 37x38
            scaled_pixmap = pixmap.scaled(
                pixmap.width() // 4,
                pixmap.height() // 4,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            website_label.setPixmap(scaled_pixmap)
            website_label.setFixedSize(scaled_pixmap.size())
            website_label.setCursor(Qt.PointingHandCursor)
            website_label.mousePressEvent = lambda e: webbrowser.open(
                "https://Beggars-Group.github.io/bgrd"
            )
            official_layout.addWidget(website_label)
        else:
            # 若图片不存在，显示文字链接
            website_text = QLabel("访问官网")
            website_text.setStyleSheet("color: #4a90e2; text-decoration: underline;")
            website_text.setCursor(Qt.PointingHandCursor)
            website_text.mousePressEvent = lambda e: webbrowser.open(
                "https://Beggars-Group.github.io/bgrd"
            )
            official_layout.addWidget(website_text)

        official_layout.addStretch()
        main_layout.addLayout(official_layout)

        # 版本信息
        ver_layout = QHBoxLayout()
        ver_label = QLabel("版本:")
        ver_label.setStyleSheet("font-weight: bold;")
        ver_layout.addWidget(ver_label)
        ver_layout.addWidget(QLabel(self.parent_window.version))
        ver_layout.addStretch()
        main_layout.addLayout(ver_layout)

        main_layout.addStretch()

        # 版权
        year = datetime.datetime.now().year
        copy_label = QLabel(f"©2019-{year}, Beggars' Group LLC™. All Rights Reserved.")
        copy_label.setAlignment(Qt.AlignCenter)
        copy_label.setStyleSheet("font-size: 10pt; color: gray;")
        main_layout.addWidget(copy_label)

        # 初始样式应用
        self.update_style()

    def on_theme_toggled(self, checked):
        self.theme_manager.toggle()
        self.parent_window.apply_theme()
        self.update_style()

    def update_style(self):
        self.setStyleSheet(self.theme_manager.get_style_sheet())
        for child in self.findChildren(QLabel, "HeaderLabel"):
            child.setFont(QFont("微软雅黑", 14, QFont.Bold))