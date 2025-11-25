import pandas as pd
from difflib import SequenceMatcher
import argparse
import json
import sys
from typing import List, Dict, Any, Optional, Tuple
import logging
from Python_S.path_utils import resource_path
import os


# 配置日志，将调试信息输出到标准错误而非标准输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # 关键修改：将日志输出到标准错误
)

def extracting_all(
    file_path: str,
    table_name: str
) -> List[Dict[str, Any]]:
    """
    在 Excel 表格的指定列范围内进行模糊搜索，并提取匹配行的完整数据
    （不区分大小写）
    
    参数:
        file_path (str): Excel 文件路径
        search_keyword (str): 搜索关键字
        table_name (str): 表格名（工作表名）
        column_range (Tuple[int, int]): 列范围 (min_col, max_col)，从0开始索引
        thres (float): 相似度阈值，默认 0.8
        top_n (int): 返回结果数量上限，默认 None 表示返回所有结果
    
    返回:
        list: 包含匹配行完整数据的字典列表
    """
    try:
        # 读取指定工作表
        df = pd.read_excel(file_path, sheet_name=table_name)
        logging.info(df)
        # logging.info(df)
        # # 检查列范围是否有效
        total_cols = len(df.columns)
        
        # data_rows = df[1:] if not df.empty else pd.DataFrame()
        
        valid_rows = len(df)
        logging.info(valid_rows)
        result_rows = []
        
        # 提取每一行的数据
        for df_idx in range(0,valid_rows):
            row_data = df.iloc[df_idx].to_dict()
            # 添加行索引信息（从1开始）
            row_data['_row_index'] = df_idx + 1
            row_data['_row_index'] = df_idx + 1
            file_path = resource_path("DoC/" + str(row_data["FUNCTION NAME"]) +".pdf")

            if os.path.exists(file_path):
                exist = 1
            else:
                exist = 0
            row_data['file_status'] = exist
            result_rows.append(row_data)
            df_idx += 1
        
        return result_rows
    
    except Exception as e:
        return {"error": str(e)}

def show_functions_main(file_path,table_name):
    try:
        # # 解析命令行参数
        # if len(sys.argv) < 5:
        #     print(json.dumps({"error": "参数不足。需要: 搜索关键字, 表格地址, 表格名, 列范围"}))
        #     sys.exit(1)
        
        # # 从命令行获取参数
        # search_keyword = sys.argv[1]         # 搜索关键字
        # table_address = sys.argv[2]          # 表格地址（Excel 文件路径）
        # table_name = sys.argv[3]             # 表格名（工作表名）
        # range_str = sys.argv[4]              # 列范围，格式为 "min_col,max_col"
        
        
        # 执行搜索
        results = extracting_all(file_path,table_name)
        
        # 输出 JSON 格式结果
        
        return(json.dumps(results))
    except Exception as e:
        sys.exit(1)
        return(json.dumps({"error": str(e)}))
        

# if __name__ == "__main__":
#     main()