import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

# JSON文件路径
ADVICE_LIST_FILE = 'DataStorage/AdviceList.json'

def _load_advice() -> Dict[str, Any]:
    """加载建议列表数据"""
    if os.path.exists(ADVICE_LIST_FILE):
        try:
            with open(ADVICE_LIST_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 确保数据结构完整
                if 'advice' not in data:
                    data['advice'] = []
                if 'statistics' not in data:
                    data['statistics'] = {}
                return data
        except:
            # 文件格式错误时返回默认结构
            return {'advice': [], 'statistics': {}}
    else:
        # 文件不存在时创建默认结构
        return {'advice': [], 'statistics': {}}

def _save_advice(data: Dict[str, Any]) -> None:
    """保存建议列表数据"""
    with open(ADVICE_LIST_FILE, 'w', encoding='utf-8') as f:    
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

def get_all_advice() -> Dict[str, Any]:
    """
    核心函数1：提供建议列表的所有数据
    无输入参数，读取AdviceList.json中的所有数据并返回
    """
    data = _load_advice()
    # 更新每个问题的持续时间
    for advice in data['advice']:
        if 'submit_time' in advice:
            advice['duration'] = _calculate_days_passed(advice['submit_time'])
    return (json.dumps(data, ensure_ascii=False))

def get_advice_number() -> Dict[str, Any]:
    """
    核心函数1：提供建议列表的所有数据
    无输入参数，读取AdviceList.json中的所有数据并返回
    """
    data = _load_advice()
    data = organize_advice(data)
    
    statistics = data['statistics']
    number = statistics['total_advice']
    # 更新每个问题的持续时间
    for advice in data['advice']:
        if 'submit_time' in advice:
            advice['duration'] = _calculate_days_passed(advice['submit_time'])
    return (json.dumps(number, ensure_ascii=False))

def add_advice(advice_data: Dict[str, Any]) -> str:
    """
    核心函数2：增加建议
    输入：json格式的数据，包含建议编号，建议描述，提交时间等字段
    输出：成功返回"success"字符串
    """
    data = _load_advice()
    
    # 验证必要字段
    required_fields = ['id', 'description', 'submit_time']
    for field in required_fields:
        if field not in advice_data:
            raise ValueError(f"缺少必要字段: {field}")
    
    # 构建完整的建议数据
    advice = {
        'id': advice_data['id'],
        'title': advice_data.get('title', '无标题'),
        'description': advice_data['description'],
        'submit_time': advice_data['submit_time'],
        'status': '待处理',
        'duration': _calculate_days_passed(advice_data['submit_time']),
        'submitter_name': advice_data.get('submitter', '匿名用户'),
        'submitter_email': advice_data.get('submitter_email', '未提供'),
    }
    
    # 添加到建议列表
    data['advice'].append(advice)
    
    # 整理数据
    data = organize_advice(data)
    
    # 保存数据
    _save_advice(data)
    
    return "success"

def manage_advice(advice_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    核心函数3：管理建议
    输入：包含建议编号等字段的数据
    输出：更新后的建议数据  
    """
    data = _load_advice()
    
    # 验证必要字段
    if 'id' not in advice_data:
        raise ValueError("缺少建议编号")
    
    advice_id = advice_data['id']
    updated = False
    
    # 查找并更新建议
    for i, advice in enumerate(data['advice']):
        if advice['id'] == advice_id:
            # 更新字段
            for key, value in advice_data.items():  
                if key != 'id':  # 不允许修改ID
                    data['advice'][i][key] = value
            
            # 更新持续时间
            if 'submit_time' in data['advice'][i]:
                data['advice'][i]['duration'] = _calculate_days_passed(data['advice'][i]['submit_time'])
            
            updated = True
            break
    
    if not updated:
        raise ValueError(f"未找到ID为 {advice_id} 的建议")
    
    # 整理数据
    data = organize_advice(data)
    
    # 保存数据
    _save_advice(data)
    return (json.dumps(data['advice'][i], ensure_ascii=False))
    # return data['advice'][i]  # 返回更新后的建议

def organize_advice(data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    整理建议函数：对建议进行统计分析
    输入：建议数据（可选，不提供则从文件加载）
    输出：包含统计信息的完整数据
    """
    if data is None:
        data = _load_advice()
    
    advices = data['advice']
    statistics = {}
    
    # 计算基本统计信息
    total_advice = len(advices)
    solved_advice = sum(1 for advice in advices if advice.get('status') == '已解决')+sum(1 for advice in advices if advice.get('status') == '已关闭')
    pending_advice = sum(1 for advice in advices if advice.get('status') == '待处理')
    in_progress_advice = sum(1 for advice in advices if advice.get('status') == '处理中')   
    
    # 计算当前月份和上个月份解决的建议数
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
    
    # 统计当月解决的建议
    current_month_solved = 0
    last_month_solved = 0
    
    for advice in advices:
        if advice.get('status') == '已解决' and 'solve_time' in advice:
            try:
                solve_date = datetime.fromisoformat(advice['solve_time'].replace('Z', '+00:00'))    
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
        'total_advice': total_advice,
        'solved_advice': solved_advice,
        'pending_advice': pending_advice,
        'in_progress_advice': in_progress_advice,
        'current_month_solved': current_month_solved,
        'last_month_solved': last_month_solved,
        'solve_increase_percent': round(solve_increase_percent, 2),
        'last_updated': datetime.now().isoformat()
    })
    
    # 更新每个建议的持续时间
    for advice in advices:
        if 'submit_time' in advice:
            advice['duration'] = _calculate_days_passed(advice['submit_time'])
    
    # 更新数据
    data['statistics'] = statistics
    
    return data
    
# 保持向后兼容的函数名
AdviceManagement = manage_advice
