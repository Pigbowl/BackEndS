import json
import os
from datetime import datetime, timedelta

# 数据文件路径
DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'DataStorage', 'page_visits_data.json')

def _ensure_data_file_exists():
    """
    确保数据文件存在，如果不存在则创建
    """
    # 确保DataStorage目录存在
    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
    
    # 如果数据文件不存在，创建初始结构
    if not os.path.exists(DATA_FILE_PATH):
        initial_data = {
            "visits": [],
            "statistic": {
                "total_visits": 0,
                "unique_visitors": 0,
                "pages": {},
                "daily_stats": {},
                "monthly_stats": {},
                "referrer_stats": {},
                "time_distribution": {}
            }
        }
        with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)

def _load_data():
    """
    加载数据文件内容
    """
    _ensure_data_file_exists()
    with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def _save_data(data):
    """
    保存数据到文件
    """
    with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_visit(visit_data):
    """
    添加访问记录
    
    Args:
        visit_data: 包含页面访问信息的字典，格式如下：
            {
                "page_url": str,  # 页面路径
                "user_id": str,   # 用户ID
                "session_id": str, # 会话ID
                "timestamp": int,  # 时间戳
                "referrer": str    # 来源页面
            }
    
    Returns:
        str: "success" 表示添加成功
    """
    try:
        # 验证必要字段
        required_fields = ["page_url", "user_id", "session_id", "timestamp", "referrer"]
        for field in required_fields:
            if field not in visit_data:
                raise ValueError(f"Missing required field: {field}")
        
        # 加载现有数据
        data = _load_data()
        
        # 添加新的访问记录
        data["visits"].append(visit_data)
        
        # 保存数据
        _save_data(data)
        
        # 进行数据分析
        data_analysis()
        
        return "success"
    except Exception as e:
        print(f"Error adding visit: {e}")
        return "error"

def get_statistic():
    """
    获取统计数据
    
    Returns:
        dict: 统计数据字典
    """
    try:
        bigdata = _load_data()
        data = bigdata["statistic"]
        print('data')
        return (json.dumps(data, ensure_ascii=False))
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return {"error": str(e)}

def data_analysis():
    """
    数据分析函数，在每次add_visit后调用
    计算并更新统计数据
    """
    try:
        data = _load_data()
        visits = data["visits"]
        
        # 初始化统计数据结构
        stats = {
            "total_visits": 0,
            "unique_visitors": 0,
            "pages": {},
            "daily_stats": {},
            "monthly_stats": {},
            "referrer_stats": {},
            "time_distribution": {}
        }
        
        # 计算总访问量和独立访客数
        stats["total_visits"] = len(visits)
        unique_users = set(visit["user_id"] for visit in visits)
        stats["unique_visitors"] = len(unique_users)
        
        # 为每个页面计算访问量和独立访客数
        page_visitors = {}
        for visit in visits:
            page_url = visit["page_url"]
            user_id = visit["user_id"]
            
            # 初始化页面数据
            if page_url not in stats["pages"]:
                stats["pages"][page_url] = {
                    "visits": 0,
                    "unique_visitors": 0,
                    "visits_percentage": 0,
                    "visitors_percentage": 0
                }
                page_visitors[page_url] = set()
            
            # 更新页面访问量
            stats["pages"][page_url]["visits"] += 1
            page_visitors[page_url].add(user_id)
            
            # 统计来源页面
            referrer = visit["referrer"]

            if referrer not in stats["referrer_stats"]:
                stats["referrer_stats"][referrer] = 0
            stats["referrer_stats"][referrer] += 1

            
            # 按小时统计访问分布
            visit_time = datetime.fromtimestamp(visit["timestamp"] / 1000)
            hour_key = f"{visit_time.hour:02d}:00"
            if hour_key not in stats["time_distribution"]:
                stats["time_distribution"][hour_key] = 0
            stats["time_distribution"][hour_key] += 1

            # 按日期统计
            date_key = visit_time.strftime("%Y-%m-%d")
            if date_key not in stats["daily_stats"]:
                stats["daily_stats"][date_key] = {
                    "visits": 0,
                    "unique_visitors": 0,
                    "pages": {}
                }
            stats["daily_stats"][date_key]["visits"] += 1
            
            # 按月份统计
            month_key = visit_time.strftime("%Y-%m")
            if month_key not in stats["monthly_stats"]:
                stats["monthly_stats"][month_key] = {
                    "visits": 0,
                    "unique_visitors": 0,
                    "pages": {}
                }
            stats["monthly_stats"][month_key]["visits"] += 1
            
            # 按日期统计页面访问
            if page_url not in stats["daily_stats"][date_key]["pages"]:
                stats["daily_stats"][date_key]["pages"][page_url] = {
                    "visits": 0,
                    "unique_visitors": 0
                }
            stats["daily_stats"][date_key]["pages"][page_url]["visits"] += 1
            
            # 按月份统计页面访问
            if page_url not in stats["monthly_stats"][month_key]["pages"]:
                stats["monthly_stats"][month_key]["pages"][page_url] = {
                    "visits": 0,
                    "unique_visitors": 0
                }
            stats["monthly_stats"][month_key]["pages"][page_url]["visits"] += 1
        
        # 计算每个页面的独立访客数和百分比
        for page_url in stats["pages"]:
            stats["pages"][page_url]["unique_visitors"] = len(page_visitors[page_url])
            stats["pages"][page_url]["visits_percentage"] = round(
                (stats["pages"][page_url]["visits"] / stats["total_visits"]) * 100, 2
            ) if stats["total_visits"] > 0 else 0
            stats["pages"][page_url]["visitors_percentage"] = round(
                (stats["pages"][page_url]["unique_visitors"] / stats["unique_visitors"]) * 100, 2
            ) if stats["unique_visitors"] > 0 else 0
        
        # 计算每日和每月的独立访客数
        daily_users = {}
        monthly_users = {}
        
        for visit in visits:
            user_id = visit["user_id"]
            visit_time = datetime.fromtimestamp(visit["timestamp"] / 1000)
            date_key = visit_time.strftime("%Y-%m-%d")
            month_key = visit_time.strftime("%Y-%m")
            page_url = visit["page_url"]
            
            # 初始化每日用户集合
            if date_key not in daily_users:
                daily_users[date_key] = set()
                daily_users[date_key + "_" + page_url] = set()
            
            # 初始化每月用户集合
            if month_key not in monthly_users:
                monthly_users[month_key] = set()
                monthly_users[month_key + "_" + page_url] = set()
            
            # 添加用户到对应集合
            daily_users[date_key].add(user_id)
            daily_users[date_key + "_" + page_url].add(user_id)
            monthly_users[month_key].add(user_id)
            monthly_users[month_key + "_" + page_url].add(user_id)
        
        # 更新每日统计的独立访客数
        for date_key in stats["daily_stats"]:
            stats["daily_stats"][date_key]["unique_visitors"] = len(daily_users.get(date_key, set()))
            for page_url in stats["daily_stats"][date_key]["pages"]:
                combined_key = date_key + "_" + page_url
                stats["daily_stats"][date_key]["pages"][page_url]["unique_visitors"] = len(
                    daily_users.get(combined_key, set())
                )
        
        # 更新每月统计的独立访客数
        for month_key in stats["monthly_stats"]:
            stats["monthly_stats"][month_key]["unique_visitors"] = len(monthly_users.get(month_key, set()))
            for page_url in stats["monthly_stats"][month_key]["pages"]:
                combined_key = month_key + "_" + page_url
                stats["monthly_stats"][month_key]["pages"][page_url]["unique_visitors"] = len(
                    monthly_users.get(combined_key, set())
                )
        
        # 获取今天和昨天的日期
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # 获取当月和上个月的月份
        current_month = datetime.now().strftime("%Y-%m")
        last_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
        
        # 添加今天、昨天、当月、上个月的快速访问数据
        stats["today"] = stats["daily_stats"].get(today, {
            "visits": 0,
            "unique_visitors": 0,
            "pages": {}
        })
        
        stats["yesterday"] = stats["daily_stats"].get(yesterday, {
            "visits": 0,
            "unique_visitors": 0,
            "pages": {}
        })
        
        stats["current_month"] = stats["monthly_stats"].get(current_month, {
            "visits": 0,
            "unique_visitors": 0,
            "pages": {}
        })
        
        stats["last_month"] = stats["monthly_stats"].get(last_month, {
            "visits": 0,
            "unique_visitors": 0,
            "pages": {}
        })
        
        # 更新数据文件中的统计信息
        data["statistic"] = stats
        _save_data(data)
        
        return stats
    except Exception as e:
        print(f"Error analyzing data: {e}")
        return None

# 模块初始化时确保数据文件存在
_ensure_data_file_exists()