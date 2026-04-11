import sys
import os
import json
import random
import threading
import datetime
import webbrowser
from typing import List, Optional, Dict, Any

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QSpinBox, QTextEdit, QDialog, 
    QFrame, QMessageBox, QCheckBox, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QSize, Signal, QObject, Slot, QTimer, QUrl
from PySide6.QtGui import QIcon, QFont, QMovie, QDesktopServices, QAction, QCursor, QTextCursor, QPixmap

from managers.config_manager import ConfigManager
from managers.asset_manager import AssetManager
from managers.voice_manager import VoiceManager

# --- 主题管理 ---
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
            # 暗色主题
            bg = "#1e1e1e"
            fg = "#dcdcdc"
            accent = "#4a90e2"
            sec_bg = "#2d2d2d"
            entry_bg = "#3c3c3c"
            border = "#3e3e3e"
        else:
            # 亮色主题
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
            
            /* 按钮样式 */
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

            /* 文本框样式 */
            QTextEdit {{
                background-color: {sec_bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 4px;
            }}
            
            /* 数字输入框样式 */
            QSpinBox {{
                background-color: {entry_bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 4px;
                padding: 5px;
                font-size: 16pt;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                width: 30px; /* 加大按钮 */
            }}
            
            /* 设置窗口的开关按钮 (使用 QCheckBox 模拟) */
            QCheckBox {{
                spacing: 10px;
                font-size: 14pt;
            }}
            QCheckBox::indicator {{
                width: 40px;
                height: 25px;
            }}
        """

# --- 设置对话框 ---
class SettingsDialog(QDialog):
    def __init__(self, parent, config: ConfigManager, theme_manager: ThemeManager):
        super().__init__(parent)
        self.config = config
        self.theme_manager = theme_manager
        self.setWindowTitle("设置")
        self.setFixedSize(450, 500)
        self.parent_window = parent  # type: MainWindow

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # 顶部区域：标题 + 右上角图片
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        # 标题
        title_label = QLabel("功能设置")
        title_label.setFont(QFont("微软雅黑", 14, QFont.Bold))
        top_layout.addWidget(title_label)
        top_layout.addStretch()

        # 右上角图片 cfd.png (原尺寸 319x226，缩放至最长边 200)
        cfd_path = self.parent_window.assets.check_file("cfd.png")
        if cfd_path:
            cfd_label = QLabel()
            pixmap = QPixmap(cfd_path)
            # 缩放至最长边 200，保持宽高比，平滑变换
            max_size = 200
            scaled_pixmap = pixmap.scaled(max_size, max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            cfd_label.setPixmap(scaled_pixmap)
            cfd_label.setFixedSize(scaled_pixmap.size())
            cfd_label.setAlignment(Qt.AlignCenter)
            top_layout.addWidget(cfd_label)

        main_layout.addLayout(top_layout)

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

        # 加载 itn.png 图片 (原尺寸 149x153，无需缩放直接显示)
        itn_path = self.parent_window.assets.check_file("itn.png")
        if itn_path:
            website_label = QLabel()
            pixmap = QPixmap(itn_path)
            # itn.png 本身较小，不进行缩放，保持原始清晰度
            website_label.setPixmap(pixmap)
            website_label.setFixedSize(pixmap.size())
            website_label.setCursor(Qt.PointingHandCursor)
            website_label.mousePressEvent = lambda e: webbrowser.open("https://Beggars-Group.github.io/bgrd")
            official_layout.addWidget(website_label)
        else:
            # 若图片不存在，显示文字链接
            website_text = QLabel("访问官网")
            website_text.setStyleSheet("color: #4a90e2; text-decoration: underline;")
            website_text.setCursor(Qt.PointingHandCursor)
            website_text.mousePressEvent = lambda e: webbrowser.open("https://Beggars-Group.github.io/bgrd")
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
        # 更新主窗口和自己的样式
        self.parent_window.apply_theme()
        self.update_style()

    def update_style(self):
        self.setStyleSheet(self.theme_manager.get_style_sheet())
        # 设置标题字体
        for child in self.findChildren(QLabel, "HeaderLabel"):
            child.setFont(QFont("微软雅黑", 14, QFont.Bold))# --- 主窗口 ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.version = "5.1a"
        self.config = ConfigManager()
        self.assets = AssetManager()
        self.theme_manager = ThemeManager(self.config)
        self.voice = VoiceManager(self.config)
        
        self.setWindowTitle("丐点名将")
        self.resize(self.config.get("window_width"), self.config.get("window_height"))
        self.setMinimumSize(500, 400)

        # 设置图标
        icon_path = self.assets.check_file("dec.ico")
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))

        # 主界面布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(20, 10, 20, 20)
        self.main_layout.setSpacing(10)

        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        # 1. 标题栏区域
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

        # 2. 结果显示区域 (包含 GIF 和 文本)
        self.result_container = QFrame()
        self.result_container.setObjectName("ResultContainer")
        self.result_container.setFrameShape(QFrame.StyledPanel)
        self.result_layout = QVBoxLayout(self.result_container)
        self.result_layout.setContentsMargins(0, 0, 0, 0)
        
        # GIF 标签
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.hide() # 默认隐藏
        self.result_layout.addWidget(self.gif_label)

        # 文本结果
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("微软雅黑", 36, QFont.Bold))
        self.result_text.setAlignment(Qt.AlignCenter)
        self.result_text.setPlaceholderText("\n\n等待抽选...")
        self.result_layout.addWidget(self.result_text)

        self.main_layout.addWidget(self.result_container, 1) # stretch=1

        # 3. 控制区域
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 20, 0, 0)
        
        count_label = QLabel("抽选人数:")
        count_label.setFont(QFont("微软雅黑", 14))
        control_layout.addWidget(count_label)
        
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 10)
        self.count_spin.setValue(1)
        self.count_spin.setFixedWidth(100)
        self.count_spin.setFixedHeight(40) # 增大输入框
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
        # 应用全局样式表
        self.setStyleSheet(self.theme_manager.get_style_sheet())

    def open_settings(self):
        dlg = SettingsDialog(self, self.config, self.theme_manager)
        dlg.exec()

    def load_names(self) -> Optional[List[str]]:
        path = self.assets.resource_path("names.txt")
        if not os.path.exists(path):
            QMessageBox.information(self, "提示", "未找到'names.txt'文件。\n请在程序目录下创建该文件，每行一个名字。")
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                names = [line.strip() for line in f if line.strip()]
            if not names:
                QMessageBox.warning(self, "警告", "名单文件为空！")
                return None
            return names
        except Exception as e:
            QMessageBox.critical(self, "错误", f"读取名单失败: {e}")
            return None

    def start_pick(self):
        names = self.load_names()
        if not names:
            return

        count = self.count_spin.value()
        if count > len(names):
            QMessageBox.warning(self, "警告", f"抽选人数({count})超过名单总数({len(names)})！")
            return

        # 1. 切换到 GIF 模式
        self.result_text.hide()
        self.gif_label.show()
        
        # 随机选择 GIF
        gif_names = ["gt4-loading.gif", "now-loading.gif"]
        valid_gifs = [g for g in gif_names if self.assets.check_file(g)]
        
        movie = None
        if valid_gifs:
            gif_path = self.assets.resource_path(random.choice(valid_gifs))
            movie = QMovie(gif_path)
            # 保持原始大小，不缩放
            movie.setCacheMode(QMovie.CacheAll) 
            self.gif_label.setMovie(movie)
            movie.start()
        else:
            self.gif_label.setText("正在抽选...")
            self.gif_label.setFont(QFont("微软雅黑", 24))

        self.start_btn.setEnabled(False)

        # 2. 延迟显示结果 (2秒后)
        QTimer.singleShot(2000, lambda: self.show_result(names, count, movie))

    def show_result(self, names, count, movie):
        # 停止动画
        if movie:
            movie.stop()
        
        self.gif_label.hide()
        self.result_text.show()
        
        selected = random.sample(names, count)
        
        # 构建结果文本 (增加一些换行让它好看点)
        text_content = "\n" + "\n".join(selected) + "\n"
        self.result_text.setPlainText(text_content)
        self.result_text.setAlignment(Qt.AlignCenter)
        
        # 修复：使用正确的 MoveOperation.Start 而不是错误的 QTextCursor.Start
        self.result_text.moveCursor(QTextCursor.MoveOperation.Start)
        self.result_text.ensureCursorVisible()

        self.start_btn.setEnabled(True)
        
        # 语音播报
        self.voice.speak(selected)

    def closeEvent(self, event):
        # 保存窗口大小
        self.config.set("window_width", self.width())
        self.config.set("window_height", self.height())
        self.voice.shutdown()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置默认字体
    font = QFont("微软雅黑", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())