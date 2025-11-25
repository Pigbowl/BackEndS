import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

# JSON文件路径
USER_LIST_FILE = 'DataStorage/UserList.json'

def _load_users() -> Dict[str, Any]:
    """加载用户列表数据"""
    if os.path.exists(USER_LIST_FILE):
        try:
            with open(USER_LIST_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 确保数据结构完整
                if 'users' not in data:
                    data['users'] = []
                if 'statistics' not in data:
                    data['statistics'] = {}
                    data['statistics']['total_users'] = len(data['users'])
                return data
        except:
            # 文件格式错误时返回默认结构
            return {'users': [], 'statistics': {}}
    else:
        # 文件不存在时创建默认结构
        return {'users': [], 'statistics': {}}

def _save_users(data: Dict[str, Any]) -> None:
    """保存用户列表数据"""
    with open(USER_LIST_FILE, 'w', encoding='utf-8') as f:  
        json.dump(data, f, ensure_ascii=False, indent=2)

def _calculate_days_passed(submit_time: str) -> int:
    """计算从提交时间到现在的天数"""
    try:
        submit_date = datetime.fromisoformat(submit_time.replace('Z', '+00:00'))
        current_date = datetime.now()
        days_passed = (current_date - submit_date).days
        return max(0, days_passed)
    except:
        return 0

def get_all_users() -> Dict[str, Any]:
    """
    核心函数1：提供问题列表的所有数据
    无输入参数，读取IssueList.json中的所有数据并返回
    """
    data = _load_users()
    # 更新每个用户的持续时间
    for user in data['users']:
        if 'submit_time' in user:
            user['duration'] = _calculate_days_passed(user['submit_time'])
    return (json.dumps(data, ensure_ascii=False))

def get_user_number() -> Dict[str, Any]:
    """
    核心函数1：提供用户列表的所有数据
    无输入参数，读取UserList.json中的所有数据并返回 
    """
    data = _load_users()
    data = organize_users(data)
    
    statistics = data['statistics']
    number = statistics['total_users']
    # 更新每个用户的持续时间
    for user in data['users']:
        if 'submit_time' in user:
            user['duration'] = _calculate_days_passed(user['submit_time'])
    return (json.dumps(number, ensure_ascii=False))

def add_user(user_data: Dict[str, Any]) -> str:
    """
    核心函数2：增加用户
    输入：json格式的数据，包含用户编号，用户名，提交时间等字段
    输出：成功返回"success"字符串，存在重复用户名或邮箱返回"redandunt"
    """
    data = _load_users()
    
    # 验证必要字段
    required_fields = ['id', 'name', 'submit_time']
    for field in required_fields:
        if field not in user_data:
            raise ValueError(f"缺少必要字段: {field}")
    
    # 检查用户名或邮箱是否已存在
    new_name = user_data['name']
    new_email = user_data.get('submitter_email', '未提供')
    
    for existing_user in data['users']:
        # 检查用户名是否重复
        if existing_user['name'] == new_name:
            return "redandunt"
        # 检查邮箱是否重复（如果邮箱不是默认值）
        if new_email != '未提供' and existing_user.get('submitter_email', '未提供') == new_email:
            return "redandunt"
    
    # 构建完整的用户数据
    user = {
        'id': user_data['id'],
        'name': user_data['name'],
        'submit_time': user_data['submit_time'],
        'duration': _calculate_days_passed(user_data['submit_time']),
        'submitter_email': new_email,
    }
    
    # 添加到用户列表
    data['users'].append(user)
    
    # 整理数据
    data = organize_users(data)
    
    # 保存数据
    _save_users(data)
    
    return "success"

def manage_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    核心函数3：管理用户
    输入：包含用户编号等字段的数据
    输出：更新后的用户数据
    """
    data = _load_users()
    
    # 验证必要字段
    if 'id' not in user_data:
        raise ValueError("缺少用户编号")
    
    user_id = user_data['id']
    updated = False
    
    # 查找并更新用户
    for i, user in enumerate(data['users']):
        if user['id'] == user_id:
            # 更新字段
            for key, value in user_data.items():
                if key != 'id':  # 不允许修改ID
                    data['users'][i][key] = value
            
            # 更新持续时间
            if 'submit_time' in data['users'][i]:
                data['users'][i]['duration'] = _calculate_days_passed(data['users'][i]['submit_time'])
            
            updated = True
            break
    
    if not updated:
        raise ValueError(f"未找到ID为 {user_id} 的用户")
    
    # 整理数据
    data = organize_users(data)
    
    # 保存数据
    _save_users(data)
    return (json.dumps(data['users'][i], ensure_ascii=False))
    # return data['users'][i]  # 返回更新后的用户

def organize_users(data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    整理用户函数：对用户进行统计分析
    输入：用户数据（可选，不提供则从文件加载）
    输出：包含统计信息的完整数据
    """
    if data is None:
        data = _load_users()
    
    users = data['users']
    statistics = {}
    
    # 计算基本统计信息
    total_users = len(users)
    # active_users = sum(1 for user in users if user.get('status') == '活跃')
    # pending_users = sum(1 for user in users if user.get('status') == '待处理')
    # in_progress_users = sum(1 for user in users if user.get('status') == '处理中')
    # solved_users = sum(1 for user in users if user.get('status') == '已解决')
    # pending_users = sum(1 for user in users if user.get('status') == '待处理')
    
    # # 计算当前月份和上个月份解决的问题数
    # current_date = datetime.now()
    # current_month = current_date.month
    # current_year = current_date.year
    
    # # 计算上个月
    # if current_month == 1:
    #     last_month = 12
    #     last_year = current_year - 1
    # else:
    #     last_month = current_month - 1
    #     last_year = current_year
    
    # # 统计当月解决的问题
    # current_month_solved = 0
    # last_month_solved = 0
    
    # for issue in issues:
    #     if issue.get('status') == '已解决' and 'solve_time' in issue:
    #         try:
    #             solve_date = datetime.fromisoformat(issue['solve_time'].replace('Z', '+00:00'))
    #             if solve_date.year == current_year and solve_date.month == current_month:
    #                 current_month_solved += 1
    #             elif solve_date.year == last_year and solve_date.month == last_month:
    #                 last_month_solved += 1
    #         except:
    #             pass
    
    # # 计算相比上月的解决数量变化百分比
    # if last_month_solved > 0:
    #     solve_increase_percent = ((current_month_solved - last_month_solved) / last_month_solved) * 100
    # else:
    #     solve_increase_percent = 100 if current_month_solved > 0 else 0
    
    # 更新统计信息
    statistics.update({
        # 'total_issues': total_issues,
        # 'solved_issues': solved_issues,
        # 'pending_issues': pending_issues,
        # 'in_progress_issues': in_progress_issues,
        # 'current_month_solved': current_month_solved,
        # 'last_month_solved': last_month_solved,
        # 'solve_increase_percent': round(solve_increase_percent, 2),
        # 'last_updated': datetime.now().isoformat(),
        'total_users': total_users,
        # 'active_users': active_users,
        # 'pending_users': pending_users,
    })
    
    # 更新每个用户的持续时间
    for user in users:
        if 'submit_time' in user:
            user['duration'] = _calculate_days_passed(user['submit_time'])
    
    # 更新数据
    data['statistics'] = statistics
    
    return data

# 保持向后兼容的函数名
UserManagement = manage_user
