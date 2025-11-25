import pandas as pd
import sys
import json
import logging

# 配置日志，将调试信息输出到标准错误而非标准输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # 关键修改：将日志输出到标准错误
)

def find_function_in_excel(input_str: str, excel_path: str,sheetname: str,key:str):
    """
    在Excel表格中查找FUNCTION Name属性等于输入字符串的行
    
    参数:
    input_str (str): 需要匹配的FUNCTION Name值
    excel_path (str): Excel文件路径
    
    返回:
    pd.DataFrame: 匹配的行，如果没有找到则返回空DataFrame
    """
    try:
        # 读取指定工作表中的数据
        df = pd.read_excel(excel_path, sheet_name=sheetname)
        
        # 确保DataFrame不为空且包含FUNCTION Name列
        if df.empty:
            logging.info("错误: Excel表格为空")
            return pd.DataFrame()
            
        if key not in df.columns:
            logging.info("错误: Excel表格中不存在'FUNCTION Name'列")
            return pd.DataFrame()
            
        # 查找匹配的行
        result = df[df[key] == input_str]
        if result.empty:
            return f"未找到 {key} 为 '{input_str}' 的记录"
            
        # 将结果格式化为指定字符串格式
        formatted_results = []
        for _, row in result.iterrows():
            record_str = "<br>".join([f"{col}：{row[col]}" for col in df.columns])
            formatted_results.append(record_str)
        logging.info("shit")
        return "\n\n".join(formatted_results)
        
    except FileNotFoundError:
        return f"错误: 文件 {excel_path} 不存在"
    except Exception as e:
        return f"错误: 读取文件时发生异常: {e}"

def main():
    """主函数，处理命令行参数并执行查找"""
    if len(sys.argv) != 5:
        logging.info("用法: python excel_parser.py <FUNCTION_Name> <Excel文件路径>")
        sys.exit(1)
        
    # 获取命令行参数
    function_name = sys.argv[1]
    excel_path = sys.argv[2]
    sheetname = sys.argv[3]
    search_key = sys.argv[4]
    
    # 执行查找并获取格式化结果
    result = find_function_in_excel(function_name, excel_path,sheetname,search_key)
    
    # 输出结果
    print(result)

if __name__ == "__main__":
    main()  