# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import sys
import os
import importlib
import threading

import py_chakura
from log_manager import MockStdOut
from gui import main_window


def exec_python_script(script_name, script_args, thread_name):
    """
    开启另一个线程执行python脚本
    Args:
        script_name: [str]脚本名字, 比如'test.py', 也可以没有'.py'后缀
        script_args: [str]脚本参数，比如'-a 123 -b 456 789'
        thread_name: [str]脚本执行现成名字，通常取调用者传的参数
    Returns:
        threading.Thread
    """
    if not script_name:
        return
    cwd = os.getcwd()
    full_path = script_name
    if not os.path.isabs(full_path):
        full_path = os.path.join(cwd, full_path)
    else:
        script_name = os.path.basename(script_name)
    if full_path == os.path.splitext(full_path)[0]:
        full_path = os.extsep.join((full_path, 'py'))
    sys_argv = [full_path]
    if script_args:
        sys_argv.extend(script_args.split())
    sys.argv = sys_argv
    sys.path.insert(0, cwd)
    script_name = os.path.splitext(script_name)[0]
    try:
        module = importlib.import_module(script_name)
    except (ImportError, ModuleNotFoundError):
        py_chakura.logger.error('Cannot import \'%s\', cwd=\'%s\'', script_name, cwd)
        py_chakura.logger.log_last_except()
        main_window.main_window.toggle_console()
        return
    py_chakura.logger.info('Start to execute python script: \'%s\', cwd=\'%s\'', script_name, cwd)
    output_window = main_window.main_window.create_python_output_window()
    sys.stdout = MockStdOut('stdout', sys.__stdout__, output_window)
    sys.stderr = MockStdOut('stderr', sys.__stderr__, output_window)
    thread = None
    if hasattr(module, 'main'):
        if not callable(module.main):
            py_chakura.logger.error('main is not callable!!!!')
            main_window.main_window.toggle_console()
            return
        try:
            thread = threading.Thread(target=module.main, name=thread_name)
            thread.start()
        except TypeError:
            py_chakura.logger.log_last_except()
            main_window.main_window.toggle_console()
            return
    return thread
