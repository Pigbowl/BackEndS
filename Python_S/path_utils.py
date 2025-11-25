# path_utils.py
import os
import sys

def resource_path(relative_path):
    """获取资源文件的正确路径，适配开发环境和打包环境"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)