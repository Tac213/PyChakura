# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import sys
import os
import argparse

import const
import dependency
import log_manager
import ninjutsu


logger = None
ninjutsu_thread = None


def _init_logger():
    """
    初始化logger
    Returns:
        None
    """
    global logger
    log_dir_path = os.path.join(const.ROOT_DIR, const.LOG_DIR_NAME)
    # 创建log目录
    if not os.path.exists(log_dir_path):
        os.mkdir(log_dir_path)
    log_manager.LogManager.tag = const.LOGGER_NAME
    logger = log_manager.LogManager.get_logger(const.LOGGER_NAME, save_file=True, dirname=log_dir_path)
    log_manager.LogManager.set_handler(log_manager.STREAM)


def get_parser():
    """
    初始化argument parser
    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    # 需要执行的python入口脚本名
    parser.add_argument('--main', '-m', default='', help='python script to be executed')
    # 给入口脚本传的参数
    parser.add_argument('--args', '-p', default='', help='argument in string to be parsed of the script')
    # 窗口名字
    parser.add_argument('--window_name', default='', help='window name of PyChakura')
    return parser


def main(args):
    """
    主函数，打开应用窗口
    Args:
        args: 解析完成的参数
    Returns:
        None
    """
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QIcon
    from PyQt6.QtCore import QDir
    from gui.main_window import MainWindow

    app = QApplication(sys.argv)

    # 设置应用基础信息
    app_name = args.window_name if args.window_name else const.APP_NAME
    app.setApplicationName(app_name)
    app.setApplicationDisplayName(app_name)
    app.setDesktopFileName(app_name)
    QDir.setSearchPaths(const.RES_DIR, [os.path.normpath(os.path.join(const.ROOT_DIR, const.RES_DIR))])
    app.setWindowIcon(QIcon(const.APP_ICON))

    # 显示主窗口, 如果不用一个变量勾住这个窗口的实例，这个窗口将无法被显示出来，即使在类里面写self.show()也没用
    main_window = MainWindow()
    main_window.on_window_ready()
    main_window.show()
    global ninjutsu_thread
    ninjutsu_thread = ninjutsu.exec_python_script(args.main, args.args, app_name)

    sys.exit(app.exec())


if __name__ == '__main__':
    dependency.check_dependency()
    args = get_parser().parse_args(sys.argv[1:])
    main(args)
else:
    # 要在__main__外面初始化logger，否则外部模块拿不到logger
    # 而且__main__的时候也不要初始化logger
    _init_logger()
