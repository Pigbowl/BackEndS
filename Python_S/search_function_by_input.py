import pandas as pd
from difflib import SequenceMatcher
import argparse
import json
import sys
from typing import List, Dict, Any, Optional, Tuple
import logging
import os
from Python_S.path_utils import resource_path


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

def fuzzy_search_excel(
    file_path: str,
    search_keyword: str,
    table_name: str,
    column_range: Tuple[int, int],
    thres: float = 0.8,
    top_n: int = None
) -> List[Dict[str, Any]]:
    try:
        # 读取指定工作表
        df = pd.read_excel(file_path, sheet_name=table_name)
        
        # 检查列范围是否有效
        min_col, max_col = column_range
        total_cols = len(df.columns)
        
        if min_col < 0 or max_col >= total_cols:
            raise ValueError(f"列范围超出表格边界。表格共有 {total_cols} 列，范围应为 0~{total_cols-1}")
        
        # 转换搜索关键字为小写（不区分大小写）
        search_keyword_lower = search_keyword.lower()
        
        # 选择指定列范围的数据（不包含表头）
        target_df = df.iloc[:, min_col:max_col+1]
        
        # 存储匹配的行索引（从1开始计数，不包含表头）
        matched_rows = set()
        
        # 遍历数据（跳过表头），查找匹配的单元格
        for row_idx, row in enumerate(target_df.itertuples(index=False), start=1):
            for col_idx, value in enumerate(row):
                # 跳过 NaN 值
                if pd.isna(value):
                    continue
                
                # 转换为字符串并转为小写
                cell_str_lower = str(value).lower()
                
                # 检查完全匹配
                if cell_str_lower == search_keyword_lower:
                    matched_rows.add(row_idx)
                    continue
                
                # 检查包含关系
                elif search_keyword_lower in cell_str_lower or cell_str_lower in search_keyword_lower:
                    matched_rows.add(row_idx)
                    continue
                
                # 检查相似度
                else:
                    similarity = similar(search_keyword_lower, cell_str_lower)
                    if similarity >= thres:
                        matched_rows.add(row_idx)
        
        # 将行索引转换为 DataFrame 中的索引（从0开始）
        df_row_indices = [idx - 1 for idx in sorted(matched_rows)]
        
        # 提取匹配行的完整数据
        result_rows = []
        if df_row_indices:
            # 获取表头作为属性名
            headers = df.columns.tolist()
            
            # 提取每一行的数据
            for df_idx in df_row_indices:
                row_data = df.iloc[df_idx].to_dict()
                # 添加行索引信息（从1开始）
                row_data['_row_index'] = df_idx + 1
                file_path = resource_path("DoC/" + str(row_data["FUNCTION NAME"]) +".pdf")

                if os.path.exists(file_path):
                    exist = 1
                else:
                    exist = 0
                row_data['file_status'] = exist

                result_rows.append(row_data)
        
        # 限制返回结果数量
        if top_n is not None and top_n > 0 and len(result_rows) > top_n:
            result_rows = result_rows[:top_n]
        
        return result_rows
    
    except Exception as e:
        return {"error": str(e)}

def fuzzy_search(search_keyword,file_path,table_name,range_str,thres):
    try:
        # 解析列范围
        column_range = parse_range(range_str)
        top_n = None
        
        # 执行搜索
        results = fuzzy_search_excel(file_path,search_keyword,table_name,column_range,thres,top_n)
        
        # 输出 JSON 格式结果
        
        return(json.dumps(results))
    
    except Exception as e:
        sys.exit(1)
        return(json.dumps({"error": str(e)}))
        

# if __name__ == "__main__":
#     main()