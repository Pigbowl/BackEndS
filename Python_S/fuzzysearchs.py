import pandas as pd
from difflib import SequenceMatcher
from typing import List, Dict, Any, Optional, Tuple
from Python_S.ReadDBAndGenerateProtocol import extract_single_item
from Python_S.sql_operations import SQLOperations
import json
def similar(a: str, b: str) -> float:
    """计算两个字符串的相似度"""
    return SequenceMatcher(None, a, b).ratio()

def parse_range(range_str: str) -> Tuple[int, int]:
    """解析列范围参数，例如 "2,5" 转换为 (2, 5)"""
    try:
        parts = range_str.split(',')
        if len(parts) != 2:
            raise ValueError("范围参数格式错误，应为 'min_col,max_col'")
        min_col = int(parts[0])
        max_col = int(parts[1])
        if min_col >= max_col:
            raise ValueError("最小列数必须小于最大列数")
        return min_col, max_col
    except Exception as e:
        raise ValueError(f"解析列范围时出错: {e}")

def fuzzy_search(
    processed_results,lib_tables_data,
    table_name: str,
    search_keyword: str,
    thres: float = 0.7,
    top_n: int = None):
    try:
        
        db = SQLOperations()
        Item_group = {}
        Item_group["type"]=table_name
        Item_group["Catalogue"]={}
        search_keyword_lower = search_keyword.lower()
        TargetLines = db.read_data(table_name)
        for line in TargetLines:
            is_match = False
            result = extract_single_item(processed_results,lib_tables_data,table_name,line['Name'],'Name')
            target_str_lower = result.lower()
            # 检查完全匹配
            if target_str_lower == search_keyword_lower:
                is_match = True
            # 检查包含关系
            elif search_keyword_lower in target_str_lower or target_str_lower in search_keyword_lower:
                is_match = True
            # 检查相似度
            else:
                similarity = similar(search_keyword_lower, target_str_lower)
                if similarity >= thres:
                    is_match = True

            if is_match:
                result_dict = json.loads(result)
                Item_group["Catalogue"][line['Name']]=result_dict[line['Name']]

        
        return json.dumps(Item_group,ensure_ascii=False, indent=2)
    
    except Exception as e:
        return {"error": str(e)}

