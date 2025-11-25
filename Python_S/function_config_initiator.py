import pandas as pd
from typing import List, Dict, Any
import logging
import sys
from difflib import SequenceMatcher
import logging
from typing import List, Dict, Any, Optional, Tuple
import json
import os
# from path_utils import resource_path

# 配置日志，将调试信息输出到标准错误而非标准输出
# 配置日志记录
logging.basicConfig(
    filename='debug.log',  # 日志文件路径
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_excel_and_generate_hw_choice(file_path) -> List[Dict[str, Any]]:
    try:
        # 读取Excel文件
        excel_file = pd.ExcelFile(file_path)
        # 读取两个工作表
        hw_pool_df = excel_file.parse('COMPONENT_POOL')
        # 确保数据读取成功
        if hw_pool_df.empty:
            raise ValueError("工作表数据为空")
        
        # 按照PRODUCT TYPE + SUPPLIER 分组
        hw_name_by_type = {}
        for _, hw_name in hw_pool_df.iterrows(): # 遍历每一行，且每一行为一个hw_name
            if str(hw_name['PROP:TYPE']) == "SoC":
                hw_supplier = str(hw_name['PROP:SUPPLIER'])
                if hw_supplier not in hw_name_by_type:  #若 该供应商不存在
                    hw_name_by_type[hw_supplier] = [] 
                
                # 将Series转换为字典并添加到对应列表
                hw_content = hw_name.to_dict()
                if hw_content["PRODUCT_VARIANT"] == "/":
                    hw_content["PRODUCT_NAME"] = hw_content["PRODUCT_NAME"]
                else:
                    hw_content["PRODUCT_NAME"] = hw_content["PRODUCT_NAME"] +"_"+hw_content["PRODUCT_VARIANT"]
                hw_name_by_type[hw_supplier].append(hw_content)

        
        # 处理每个硬件生成结果
        hw_choice_data = []
        for hw_option in hw_name_by_type:
            hw_option_obj = {
                "id":hw_option,
                "name":hw_option,
                'icon':'fa fa-user',
                'description':"Following the SoC product from " + str(hw_option),
                'features': hw_name_by_type.get(hw_option, [])
            }
            hw_choice_data.append(hw_option_obj)

        return hw_choice_data
    
    except Exception as e:
        logging.debug(f"处理Excel文件时出错: {e}")
        return []


def read_excel_and_generate_sensor_choice(file_path) -> List[Dict[str, Any]]:
    try:
        # 读取Excel文件
        excel_file = pd.ExcelFile(file_path)
        # 读取两个工作表
        sensor_choice_df = excel_file.parse('SENSOR CHOICE')
        # 确保数据读取成功
        if sensor_choice_df.empty:
            raise ValueError("工作表数据为空")
        
        # 处理每个硬件生成结果
        sensor_choice_data = []
        for _, sensor_row in sensor_choice_df.iterrows():
            sensor_name = sensor_row['KEY WORD']

            #创建字典
            sensor_obj = {
                # 'type':"HW",
                'id':sensor_name,
                'name':sensor_name,
                'icon':'fa fa-user',
            }
            sensor_choice_data.append(sensor_obj)
        return sensor_choice_data
    except Exception as e:
        logging.debug(f"处理Excel文件时出错: {e}")
        return []


def read_excel_and_generate_regulation_choice(file_path) -> List[Dict[str, Any]]:
    try:
        # 读取Excel文件
        excel_file = pd.ExcelFile(file_path)
        # 读取两个工作表
        reg_choice_df = excel_file.parse('REGULATION')
        # 确保数据读取成功
        if reg_choice_df.empty:
            raise ValueError("工作表数据为空")
        
        # 处理每个硬件生成结果
        reg_choice_data = []
        for _, reg_row in reg_choice_df.iterrows():
            reg_name = reg_row['KEY WORD']

            #创建字典
            reg_obj = {
                # 'type':"HW",
                'id':reg_name,
                'name':reg_name,
                'icon':'fa fa-user',
            }
            reg_choice_data.append(reg_obj)
        return reg_choice_data
    except Exception as e:
        logging.debug(f"处理Excel文件时出错: {e}")
        return []


def read_excel_and_generate_data(file_path: str) -> List[Dict[str, Any]]:
    """
    读取Excel文件并生成功能和子功能的数据结构
    
    Args:
        file_path: Excel文件路径
    
    Returns:
        包含所有功能及其子功能的字典数组
    """
    try:
        # 读取Excel文件
        excel_file = pd.ExcelFile(file_path)
        # 读取两个工作表
        euf_df = excel_file.parse('EUF')
        subfeatures_df = excel_file.parse('SUBFEATURES')
        # 确保数据读取成功
        if euf_df.empty or subfeatures_df.empty:
            raise ValueError("工作表数据为空")
        
        # 按EUF_NAME分组子功能
        subfeatures_by_euf = {}
        for _, subfeature in subfeatures_df.iterrows():
            euf_name = subfeature['EUF_NAME']
            if euf_name not in subfeatures_by_euf:
                subfeatures_by_euf[euf_name] = []
            # 将Series转换为字典并添加到对应列表
            subfeatures_by_euf[euf_name].append(subfeature.to_dict())
        
        # 处理每个功能并生成结果
        functions_data = []
        for _, function_row in euf_df.iterrows():
            # 提取基本信息
            function_name = function_row['FUNCTION NAME']
            
            # 创建功能字典
            function_obj = {
                # 'type':"EUF",
                'id': function_name,
                'name': function_name,
                'fullName': function_row['FUNCTION FULL NAME'],
                'description': function_row['FUNCTION DESCRIPTION'],
                'icon': 'fa fa-rocket',
                'features': subfeatures_by_euf.get(function_name, [])
            }
            
            # # 添加其他属性
            # for col_name, value in function_row.items():
            #     if col_name not in ['FUNCTION NAME', 'FUNCTION FULL NAME', 'FUNCTION DESCRIPTION']:
            #         function_obj[col_name] = value
            
            functions_data.append(function_obj)
        
        return functions_data
    
    except Exception as e:
        logging.debug(f"处理Excel文件时出错: {e}")
        return []


# 使用示例
def search_init_main(file_path):
    try:
        result = read_excel_and_generate_data(file_path)
        
        hw_choice_data = read_excel_and_generate_hw_choice(file_path) 
        
        # sensor_choice_data = read_excel_and_generate_sensor_choice(file_path)

        # reg_choice_data = read_excel_and_generate_regulation_choice(file_path)
        final_result = {
            "EUF":result,
            "HW_choice":hw_choice_data,
            "Sensor_choice":[],
            "Regulation_choice":[],
        }
        # 打印结果（示例）
        if final_result:
            logging.debug(f"Reading {len(result)} function")

        return(json.dumps(final_result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

# if __name__ == "__main__":
#     search_init_main()