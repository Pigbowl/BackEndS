import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

# JSON文件路径
ISSUE_LIST_FILE = 'DataStorage/IssueList.json'

def _load_issues() -> Dict[str, Any]:
    """加载问题列表数据"""
    if os.path.exists(ISSUE_LIST_FILE):
        try:
            with open(ISSUE_LIST_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 确保数据结构完整
                if 'issues' not in data:
                    data['issues'] = []
                if 'statistics' not in data:
                    data['statistics'] = {}
                return data
        except:
            # 文件格式错误时返回默认结构
            return {'issues': [], 'statistics': {}}
    else:
        # 文件不存在时创建默认结构
        return {'issues': [], 'statistics': {}}

def _save_issues(data: Dict[str, Any]) -> None:
    """保存问题列表数据"""
    with open(ISSUE_LIST_FILE, 'w', encoding='utf-8') as f:
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

def get_all_issues() -> Dict[str, Any]:
    """
    核心函数1：提供问题列表的所有数据
    无输入参数，读取IssueList.json中的所有数据并返回
    """
    data = _load_issues()
    # 更新每个问题的持续时间
    for issue in data['issues']:
        if 'submit_time' in issue:
            issue['duration'] = _calculate_days_passed(issue['submit_time'])
    return (json.dumps(data, ensure_ascii=False))

def get_issue_number() -> Dict[str, Any]:
    """
    核心函数1：提供问题列表的所有数据
    无输入参数，读取IssueList.json中的所有数据并返回
    """
    data = _load_issues()
    data = organize_issues(data)
    
    statistics = data['statistics']
    number = statistics['total_issues']
    # 更新每个问题的持续时间
    for issue in data['issues']:
        if 'submit_time' in issue:
            issue['duration'] = _calculate_days_passed(issue['submit_time'])
    return (json.dumps(number, ensure_ascii=False))

def add_issue(issue_data: Dict[str, Any]) -> str:
    """
    核心函数2：增加问题
    输入：json格式的数据，包含问题编号，问题描述，提交时间等字段
    输出：成功返回"success"字符串
    """
    data = _load_issues()
    
    # 验证必要字段
    required_fields = ['id', 'description', 'submit_time']
    for field in required_fields:
        if field not in issue_data:
            raise ValueError(f"缺少必要字段: {field}")
    
    # 构建完整的问题数据
    issue = {
        'id': issue_data['id'],
        'title': issue_data.get('title', '无标题'),
        'description': issue_data['description'],
        'submit_time': issue_data['submit_time'],
        'status': '待处理',
        'duration': _calculate_days_passed(issue_data['submit_time']),
        'submitter_name': issue_data.get('submitter', '匿名用户'),
        'submitter_email': issue_data.get('submitter_email', '未提供'),
    }
    
    # 添加到问题列表
    data['issues'].append(issue)
    
    # 整理数据
    data = organize_issues(data)
    
    # 保存数据
    _save_issues(data)
    
    return "success"

def manage_issue(issue_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    核心函数3：管理问题
    输入：包含问题编号等字段的数据
    输出：更新后的问题数据
    """
    data = _load_issues()
    
    # 验证必要字段
    if 'id' not in issue_data:
        raise ValueError("缺少问题编号")
    
    issue_id = issue_data['id']
    updated = False
    
    # 查找并更新问题
    for i, issue in enumerate(data['issues']):
        if issue['id'] == issue_id:
            # 更新字段
            for key, value in issue_data.items():
                if key != 'id':  # 不允许修改ID
                    data['issues'][i][key] = value
            
            # 更新持续时间
            if 'submit_time' in data['issues'][i]:
                data['issues'][i]['duration'] = _calculate_days_passed(data['issues'][i]['submit_time'])
            
            updated = True
            break
    
    if not updated:
        raise ValueError(f"未找到ID为 {issue_id} 的问题")
    
    # 整理数据
    data = organize_issues(data)
    
    # 保存数据
    _save_issues(data)
    return (json.dumps(data['issues'][i], ensure_ascii=False))
    # return data['issues'][i]  # 返回更新后的问题

def organize_issues(data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    整理问题函数：对问题进行统计分析
    输入：问题数据（可选，不提供则从文件加载）
    输出：包含统计信息的完整数据
    """
    if data is None:
        data = _load_issues()
    
    issues = data['issues']
    statistics = {}
    
    # 计算基本统计信息
    total_issues = len(issues)
    solved_issues = sum(1 for issue in issues if issue.get('status') == '已解决')+sum(1 for issue in issues if issue.get('status') == '已关闭')
    pending_issues = sum(1 for issue in issues if issue.get('status') == '待处理')
    in_progress_issues = sum(1 for issue in issues if issue.get('status') == '处理中')
    
    # 计算当前月份和上个月份解决的问题数
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # 计算上个月
    if current_month == 1:
        last_month = 12
        last_year = current_year - 1
    else:
        last_month = current_month - 1
        last_year = current_year
    
    # 统计当月解决的问题
    current_month_solved = 0
    last_month_solved = 0
    
    for issue in issues:
        if issue.get('status') == '已解决' and 'solve_time' in issue:
            try:
                solve_date = datetime.fromisoformat(issue['solve_time'].replace('Z', '+00:00'))
                if solve_date.year == current_year and solve_date.month == current_month:
                    current_month_solved += 1
                elif solve_date.year == last_year and solve_date.month == last_month:
                    last_month_solved += 1
            except:
                pass
    
    # 计算相比上月的解决数量变化百分比
    if last_month_solved > 0:
        solve_increase_percent = ((current_month_solved - last_month_solved) / last_month_solved) * 100
    else:
        solve_increase_percent = 100 if current_month_solved > 0 else 0
    
    # 更新统计信息
    statistics.update({
        'total_issues': total_issues,
        'solved_issues': solved_issues,
        'pending_issues': pending_issues,
        'in_progress_issues': in_progress_issues,
        'current_month_solved': current_month_solved,
        'last_month_solved': last_month_solved,
        'solve_increase_percent': round(solve_increase_percent, 2),
        'last_updated': datetime.now().isoformat()
    })
    
    # 更新每个问题的持续时间
    for issue in issues:
        if 'submit_time' in issue:
            issue['duration'] = _calculate_days_passed(issue['submit_time'])
    
    # 更新数据
    data['statistics'] = statistics
    
    return data

# 保持向后兼容的函数名
IssueManagement = manage_issue