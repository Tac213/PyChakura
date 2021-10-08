# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget

from .output_window import OutputWindow
import py_chakura

main_window = None  # MainWindow的实例


class MainWindow(QMainWindow):
    """
    gui界面的主窗口
    """

    def __init__(self, parent=None):
        """
        构造器
        Args:
            parent: 父Widget
        """
        super(MainWindow, self).__init__(parent)
        self.output_window = OutputWindow(self)

        self._setup_ui()
        global main_window
        main_window = self

    def _setup_ui(self):
        """
        setup界面
        Returns:
            None
        """
        self.resize(800, 400)
        central_widget = QWidget(self)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.output_window)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_window_ready(self):
        """
        main window准备完成回调
        Returns:
            None
        """
        from log_manager import OutputWindowHandler
        OutputWindowHandler.main_window_ready = True
        py_chakura.logger.info(self.tr('第一步：选择需要导表的Excel'))
        py_chakura.logger.info(self.tr('第二步：点击导表按钮，开始导表'))
