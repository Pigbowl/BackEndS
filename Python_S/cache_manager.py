# cache_manager.py
import os
import sys
import shutil
import tempfile
import hashlib
import time
import json

def get_app_hash():
    """计算应用程序的哈希值，用于判断应用是否更新"""
    exe_path = sys.executable
    try:
        with open(exe_path, 'rb') as f:
            return hashlib.sha256(f.read(4096)).hexdigest()
    except Exception:
        return str(time.time())  # 出错时使用时间戳

def get_cache_dir():
    """获取应用的缓存目录"""
    app_name = "Configurator"
    cache_base = os.environ.get("LOCALAPPDATA", tempfile.gettempdir())
    return os.path.join(cache_base, app_name, "cache")

def check_and_update_cache():
    """检查缓存是否有效，无效则更新"""
    app_hash = get_app_hash()
    cache_dir = get_cache_dir()
    cache_info_file = os.path.join(cache_dir, "cache_info.json")
    
    # 创建缓存目录
    os.makedirs(cache_dir, exist_ok=True)
    
    # 检查缓存信息
    valid = False
    if os.path.exists(cache_info_file):
        try:
            with open(cache_info_file, 'r') as f:
                cache_info = json.load(f)
                if cache_info.get("app_hash") == app_hash:
                    valid = True
        except Exception:
            pass
    
    # 如果缓存无效，清空缓存目录
    if not valid:
        print("缓存无效，清理并重新创建...")
        for item in os.listdir(cache_dir):
            item_path = os.path.join(cache_dir, item)
            if item != "cache_info.json":
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
        
        # 更新缓存信息
        with open(cache_info_file, 'w') as f:
            json.dump({"app_hash": app_hash, "timestamp": time.time()}, f)
    
    return cache_dir