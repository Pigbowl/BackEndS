import pandas as pd
from difflib import SequenceMatcher
import argparse
import json
import sys
from typing import List, Dict, Any, Optional, Tuple
import logging
from Python_S.path_utils import resource_path
import os
from fpdf import FPDF
from datetime import datetime

# 配置日志记录
logging.basicConfig(
    filename='debug.log',  # 日志文件路径
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def parse_input_dict4func(input_dict):
    """
    解析输入字典，生成EUF列表
    
    参数:
        input_dict (dict): 包含FUNCTION和FEATURE的输入字典
    
    返回:
        list: EUF字符串列表
    """
    try:
        # 获取FUNCTION和FEATURE数据
        main_cards = input_dict.get('mainCards', [])
        sub_cards = input_dict.get('subCards', {})
        euf_list = []
        
        for func in main_cards:
            features = sub_cards.get(func, [])
            
            if not features:
                # 如果没有子特性，默认为"Basic"
                euf_list.append(f"{func}-Basic")
            else:
                # 每个子特性生成一个EUF
                for feature in features:
                    euf_list.append(f"{feature}")

        return euf_list
        
    except Exception as e:
        print(f"解析输入字典时出错: {e}")
        return []

def parse_input_dict(input_dict,table_path):
    """
    解析输入字典，生成EUF列表
    
    参数:
        input_dict (dict): 包含FUNCTION和FEATURE的输入字典
    
    返回:
        list: EUF字符串列表
    """
    try:
        # 获取FUNCTION和FEATURE数据
        main_cards = input_dict.get('mainCards', [])
        sub_cards = input_dict.get('subCards', {})
        df_component_pool = pd.read_excel(table_path, sheet_name='COMPONENT_POOL')
        euf_list = []
        
        for func in main_cards:
            features = sub_cards.get(func, [])
            
            if not features:
                # 如果没有子特性，默认为"Basic"
                # euf_list.append(f"{func}")
                for _, hw_name in df_component_pool.iterrows(): 
                    if hw_name["SUPPLIER"] == func:
                        product = hw_name["PRODUCT_NAME"]
                        euf_list.append(f"{product}")
                
            else:
                # 每个子特性生成一个EUF
                for feature in features:
                    euf_list.append(f"{feature}")

        return euf_list
        
    except Exception as e:
        print(f"解析输入字典时出错: {e}")
        return []

def parse_soc_cell(cell_value):
    """
    解析可能包含多个SoC的单元格值
    
    参数:
    cell_value: 单元格中的值，可能是字符串、数值或空值
    
    返回:
    list: 解析后的SoC列表，如果单元格表示无SoC属性，则返回空列表
    """
    if pd.isna(cell_value):
        return []
        
    # 转换为字符串并去除首尾空格
    cell_str = str(cell_value).strip()
    
    # 处理无SoC属性的情况
    if cell_str == 'X':
        return []
        
    # 分割单元格值
    items = cell_str.split(',')
    socs = []
    
    for item in items:
        item = item.strip()
        if not item:
            continue
            
        # 处理带数量的情况，如 "A*2"
        if '*' in item:
            parts = item.split('*')
            if len(parts) == 2:
                try:
                    count = int(parts[1])
                    socs.extend([parts[0]])
                    continue
                except ValueError:
                    pass  # 不是有效的数字，按普通名称处理
        
        # 普通情况，直接添加
        socs.append(item)
    
    return socs

def find_supported_sw_products(table_path, input_dict):
    """
    根据输入的EUF列表，查找支持所有EUF的软件产品
    
    参数:
        table_path (str): Excel文件路径
        input_dict (dict): 包含FUNCTION和FEATURE的输入字典
    
    返回:
        list: 支持所有EUF的软件产品列表
    """
    try:
        # 步骤1: 解析输入字典，生成EUF列表
        euf_list = parse_input_dict4func(input_dict)
        if not euf_list:
            print('No Function is provided')
            return [],False
        # 步骤2: 读取Excel数据
        df = pd.read_excel(table_path, sheet_name='SW_PRODUCT2FEATURE')
        # 确保数据有效
        if df.empty:
            print("错误: SW_PRODUCT2FEATURE表为空")
            return [],False
        
        # 步骤3: 验证EUF是否存在于表格中
        available_eufs = set(df.columns[1:])  # 第一列是产品名，其余是EUF
        missing_eufs = [euf for euf in euf_list if euf not in available_eufs]
        
        if missing_eufs:
            print(f"警告: 以下EUF在表格中不存在: {missing_eufs}")
            return []
        
        # 步骤4: 筛选支持所有EUF的产品
        supported_products = []
        
        for _, row in df.iterrows():
            product_name = row.iloc[0]
            # 检查该产品是否支持所有EUF
            if all(row[euf] == 'Y' for euf in euf_list):
                supported_products.append(product_name)
        return supported_products,True
    
    except Exception as e:
        print(f"处理过程中出错: {e}")
        return []

def find_supported_hw_products(table_path, input_dict):
    """
    根据输入的EUF列表，查找支持所有EUF的软件产品
    
    参数:
        table_path (str): Excel文件路径
        input_dict (dict): 包含FUNCTION和FEATURE的输入字典
    
    返回:
        list: 支持所有EUF的软件产品列表
    """
    try:
        search_result = ''
        # 步骤1: 解析输入字典，生成EUF列表
        soc_list = parse_input_dict(input_dict,table_path)
        if not soc_list:
            search_result = "没有收到硬件输入"
            print("No hardware requirement given")
            return [],False,search_result
        
        
        # 步骤2: 读取Excel数据
        df = pd.read_excel(table_path, sheet_name='HW_PRODUCT')
        product_name_col = df.columns[0]
        # 确保数据有效
        if df.empty:
            search_result = "错误: HW_PRODUCT表为空"
            print("错误: HW_PRODUCT表为空")
            return [],False,search_result
        
        # 查找所有格式为"COMPONENT:SoC:*"的列
        soc_columns = []
        for col in df.columns[1:]:  # 跳过第一列(产品名称)
            parts = col.split(':')
            if len(parts) >= 2 and parts[0] == 'COMPONENT' and parts[1] == 'SoC':
                soc_columns.append(col)
                    # 如果没有找到符合条件的列，返回空DataFrame
        if not soc_columns:
            print("未找到符合条件的SoC列")
            return pd.DataFrame()
        
        # 创建筛选条件
        conditions = pd.Series([False] * len(df))
        for col in soc_columns:
            # 处理每个单元格，检查是否包含任何目标SoC
            
            col_conditions = df[col].apply(lambda x: any(soc in parse_soc_cell(x) for soc in soc_list))
            conditions = conditions | col_conditions
        
        if not df[conditions][product_name_col].tolist():
            search_result = '当前方案中没有能够支持' + str(soc_list)+" 产品的方案"
            print('当前方案中没有能够支持' + str(soc_list)+" 产品的方案")
            return [],True,search_result

        return df[conditions][product_name_col].tolist(),True,search_result
    
    except Exception as e:
        print(f"处理过程中出错: {e}")
        return []



def find_compatible_solutions(table_path, supported_sw_products,supported_hw_products,sw_req,hw_req):
    """查找兼容的Solution并清理ECU信息，同时补充组件和软件详情"""
    try:
        # 读取SOLUTION表
        df_solution = pd.read_excel(table_path, sheet_name='SOLUTION')
        
        if df_solution.empty:
            print("Error: SOLUTION table is empty")
            return []
            
        # 查找ECU和SW列
        ecu_columns = []
        sw_column = None
        
        for col in df_solution.columns:
            if col.strip().upper().startswith('ECU'):
                ecu_columns= col
            elif col.strip().upper().startswith('SW'):
                sw_column = col
                
        if not ecu_columns or not sw_column:
            print("Error: ECU or SW column not found in SOLUTION table")
            return []
            
        # 筛选兼容的Solutions
        compatible_solutions = []
        for _, row in df_solution.iterrows():
            solution_sw = str(row[sw_column]).strip()
            solution_hw = parse_soc_cell(row[ecu_columns])

            if (not sw_req or solution_sw in supported_sw_products) and (not hw_req or any(element in supported_hw_products for element in solution_hw)):
                solution_data = row.to_dict()
                
                # 处理ECU属性，将'X'转换为None
                for ecu_col in ecu_columns:
                    if ecu_col in solution_data:
                        value = str(solution_data[ecu_col]).strip()
                        solution_data[ecu_col] = None if value == 'X' else value
                
                compatible_solutions.append(solution_data)

        # 读取HW_PRODUCT表（用于查找组件详情和传感器信息） ->信息读取，独立于删选
        df_hw = pd.read_excel(table_path, sheet_name='HW_PRODUCT')
        hw_dict = {}
        if not df_hw.empty and 'PRODUCT NAME' in df_hw.columns:
            hw_dict = {row['PRODUCT NAME']: row.to_dict() for _, row in df_hw.iterrows()}
        else:
            print("Warning: HW_PRODUCT table does not exist or is missing 'PRODUCT NAME' column")

        # 读取SW_PRODUCT表（用于查找软件详情、外部依赖和技术栈）
        df_sw = pd.read_excel(table_path, sheet_name='SW_PRODUCT')
        sw_dict = {}
        if not df_sw.empty and 'PRODUCT NAME' in df_sw.columns:
            sw_dict = {row['PRODUCT NAME']: row.to_dict() for _, row in df_sw.iterrows()}
        else:
            print("Warning: SW_PRODUCT table does not exist or is missing 'PRODUCT NAME' column")
            
        # 读取SW_PRODUCT2FEATURE表（用于查找软件支持的特性）
        df_sw2feature = pd.read_excel(table_path, sheet_name='SW_PRODUCT2FEATURE')
        sw2feature_dict = {}
        if not df_sw2feature.empty and 'PRODUCT NAME' in df_sw2feature.columns:  # 修改1
            for _, row in df_sw2feature.iterrows():
                sw_product = str(row['PRODUCT NAME']).strip()  # 修改2
                if sw_product not in sw2feature_dict:
                    sw2feature_dict[sw_product] = {}
                for col in df_sw2feature.columns:
                    if col != 'PRODUCT NAME':  # 修改3
                        feature_name = col.strip()
                        support_status = str(row[col]).strip()
                        if support_status == 'Y':
                            sw2feature_dict[sw_product][feature_name] = True
        else:
            print("Warning: SW_PRODUCT2FEATURE table does not exist or is missing 'PRODUCT NAME' column")
            
        # 读取SUBFEATURES表（用于查找特性说明和功能列表）
        df_subfeatures = pd.read_excel(table_path, sheet_name='SUBFEATURES')
        feature_description_dict = {}
        feature_functions_dict = {}
        if not df_subfeatures.empty and 'FEATURE_NAME' in df_subfeatures.columns:  # 修改4
            for _, row in df_subfeatures.iterrows():
                feature_name = str(row['FEATURE_NAME']).strip()  # 修改5
                feature_description = str(row.get('FEATURE_DESCRIPTION', '')).strip()
                euf_name = str(row.get('EUF_NAME', '')).strip()
                
                if feature_name:
                    # 存储特性描述
                    if feature_description:
                        feature_description_dict[feature_name] = feature_description
                    
                    # 存储特性对应的功能
                    if euf_name:
                        if feature_name not in feature_functions_dict:
                            feature_functions_dict[feature_name] = set()
                        feature_functions_dict[feature_name].add(euf_name)
        else:
            print("Warning: SUBFEATURES table does not exist or is missing 'FEATURE_NAME' column")
            
        # 读取EUF表（用于查找功能的SAE等级）
        df_euf = pd.read_excel(table_path, sheet_name='EUF')
        function_sae_dict = {}
        if not df_euf.empty and 'FUNCTION NAME' in df_euf.columns:  # 修改6
            for _, row in df_euf.iterrows():
                function_name = str(row['FUNCTION NAME']).strip()  # 修改7
                sae_level = str(row.get('SAE FUNCTION LEVEL', '')).strip()
                
                if function_name and sae_level:
                    function_sae_dict[function_name] = sae_level
        else:
            print("Warning: EUF table does not exist or is missing 'FUNCTION NAME' column")
            

        # 清理ECU信息并补充组件和软件详情
        cleaned_solutions = []
        
        for solution in compatible_solutions:
            component_list = []
            
            # 收集所有非空的ECU值
            for key, value in solution.items():
                if key.upper().startswith('ECU') and value is not None: 
                    if "," in value:
                        items = value.split(',')# 分割单元格值
                        for item in items:
                            component_details = hw_dict.get(item, {"PRODUCT NAME": item, "details": "Not found"})
                            component_list.append(component_details)
                    component_details = hw_dict.get(value, {"PRODUCT NAME": value, "details": "Not found"})
                    component_list.append(component_details)
            # print(component_details)
            # 添加标准化的组件信息
            solution['numberOfComponents'] = len(component_list)
            solution['componentList'] = component_list
            
            # 替换SW值为软件详情（创建独立副本）
            sw_value = solution.get(sw_column)
            if sw_value and sw_value in sw_dict:
                solution['SW'] = sw_dict[sw_value].copy()  # 创建独立副本
            else:
                solution['SW'] = {"PRODUCT NAME": sw_value, "details": "Not found"}
            
            # 提取当前解决方案的SW需要的传感器列表（完整属性名）
            sw_required_sensors = set()
            if sw_value and sw_value in sw_dict:
                sw_details = sw_dict[sw_value]
                for attr_name, attr_value in sw_details.items():
                    if attr_name.startswith('SENSOR:') and attr_value.strip() == 'Y':
                        sw_required_sensors.add(attr_name)  # 保留完整属性名
            
            # 从所有组件中提取并聚合传感器信息（经过SW校验）
            sensorInfo = {}
            for component in component_list:
                # 从HW_PRODUCT中提取该组件的传感器信息
                for attr_name, attr_value in component.items():
                    if attr_name.startswith('SENSOR:') and attr_value.strip() != 'X':
                        # 检查该传感器是否被SW需要
                        if attr_name not in sw_required_sensors:
                            continue  # 跳过SW不需要的传感器
                        
                        parts = attr_name.split(':')
                        if len(parts) >= 4:  # 至少包含类型、属性和位置
                            sensorType = parts[1].strip()
                            sensorAttribute = parts[2].strip()
                            sensorPosition = parts[3].strip()
                            sensorModel = attr_value.strip()  # 传感器型号
                            
                            # 提取可选的传感器特征
                            sensorFeature = parts[4].strip() if len(parts) > 4 else None
                            
                            # 更新该类型传感器的信息
                            if sensorType not in sensorInfo:
                                sensorInfo[sensorType] = {
                                    "count": 0,
                                    "attributes": {}
                                }
                            
                            sensorInfo[sensorType]["count"] += 1
                            
                            # 更新属性信息，保留每个位置的详细信息
                            if sensorAttribute not in sensorInfo[sensorType]["attributes"]:
                                sensorInfo[sensorType]["attributes"][sensorAttribute] = []
                            
                            sensorInfo[sensorType]["attributes"][sensorAttribute].append({
                                "position": sensorPosition,
                                "model": sensorModel,
                                "feature": sensorFeature
                            })
            
            # 整理传感器信息
            for sensorType, info in sensorInfo.items():
                # 为每个属性添加计数
                for attr, details in info["attributes"].items():
                    info["attributes"][attr] = {
                        "count": len(details),
                        "details": details
                    }
            
            # 添加聚合后的传感器信息到solution
            solution['sensorInfo'] = sensorInfo
            
            # 提取外部依赖信息（直接作为solution的顶级成员）
            optionalDependencies = []
            strongDependencies = []
            
            if sw_value and sw_value in sw_dict:
                sw_details = sw_dict[sw_value]
                for attr_name, attr_value in sw_details.items():
                    if attr_name.startswith('EXT:'):
                        dependencyType = attr_name.split(':')[1].strip()
                        if attr_value == 'O':
                            optionalDependencies.append(dependencyType)
                        elif attr_value == 'Y':
                            strongDependencies.append(dependencyType)
            
            # 直接将依赖列表添加为solution的顶级成员
            solution['optionalDependencies'] = optionalDependencies
            solution['strongDependencies'] = strongDependencies
            
            # 提取技术栈信息
            techStackInfo = []
            
            if sw_value and sw_value in sw_dict:
                sw_details = sw_dict[sw_value]
                for attr_name, attr_value in sw_details.items():
                    if attr_name.startswith('TECH_STACK:') and attr_value.strip() == 'Y':
                        techStackType = attr_name.split(':')[1].strip()
                        techStackInfo.append(techStackType)
            
            # 添加技术栈信息到solution
            solution['techStackInfo'] = techStackInfo
            
            # 生成传感器集字符串
            sensorSet = ""
            
            # 按类型映射缩写
            type_mapping = {
                "CAM": "V",
                "RDR": "R",
                "LIDAR": "L",
                # 可添加其他类型映射
            }
            
            # 按特定顺序处理主要类型
            ordered_types = ["CAM", "RDR", "LIDAR"]
            
            # 处理主要类型
            for sensor_type in ordered_types:
                if sensor_type in sensorInfo:
                    count = sensorInfo[sensor_type]["count"]
                    abbreviation = type_mapping.get(sensor_type, sensor_type[0])  # 默认取首字母
                    sensorSet += f"{count}{abbreviation}"
            
            # 处理剩余类型
            remaining_types = [t for t in sensorInfo.keys() if t not in ordered_types]
            for sensor_type in sorted(remaining_types):
                count = sensorInfo[sensor_type]["count"]
                abbreviation = type_mapping.get(sensor_type, sensor_type[0])  # 默认取首字母
                sensorSet += f"{count}{abbreviation}"
            
            # 添加传感器集字符串到solution
            solution['sensorSet'] = sensorSet
            
            # 提取计算单元信息（合并SoC/SIP和MCU的值）
            calculateunitInfo = []
            
            for component in component_list:
                # 添加SoC/SIP信息
                soc_sip_value = component.get("COMPONENT:SoC")
                if soc_sip_value and soc_sip_value.strip() != 'X':
                    calculateunitInfo.append(soc_sip_value.strip())
                
                # 添加MCU信息
                mcu_value = component.get("COMPONENT:MCU")
                if mcu_value and mcu_value.strip() != 'X':
                    calculateunitInfo.append(mcu_value.strip())
            # 添加计算单元信息到solution
            solution['calculateunitInfo'] = calculateunitInfo
            
            # 提取支持的特性信息
            supportfeature = {}
            if sw_value and sw_value in sw2feature_dict:
                supported_features = sw2feature_dict[sw_value]
                for feature_name in supported_features:
                    description = feature_description_dict.get(feature_name, "No description available")
                    supportfeature[feature_name] = description
            
            # 添加支持的特性到solution
            solution['supportfeature'] = supportfeature
            
            # 提取支持的功能列表（去重）
            function_list = set()
            for feature_name in supported_features:
                if feature_name in feature_functions_dict:
                    functions = feature_functions_dict[feature_name]
                    function_list.update(functions)
            
            # 转换为有序列表
            function_list = sorted(function_list)
            
            # 添加功能列表到solution
            solution['functionList'] = function_list
            
            # 计算最高SAE等级
            highest_level = "L0"
            
            # 使用外部定义的compare_sae_levels函数
            for function_name in function_list:
                if function_name in function_sae_dict:
                    sae_level = function_sae_dict[function_name]
                    highest_level = compare_sae_levels(highest_level, sae_level)
            
            # 添加最高SAE等级到solution
            solution['highestLevel'] = highest_level
            
            # 从SW属性中删除传感器、外部依赖和技术栈相关属性
            if 'SW' in solution and isinstance(solution['SW'], dict):
                keys_to_delete = [
                    k for k in solution['SW'].keys()
                    if k.startswith('SENSOR:') or k.startswith('EXT:') or k.startswith('TECH_STACK:')
                ]
                for key in keys_to_delete:
                    del solution['SW'][key]
            
            # 只删除原始ECU列，保留新添加的 component_list 和 numberofcomponents
            original_ecu_keys = [k for k in solution.keys() if k.upper().startswith('ECU')]
            solution = {k: v for k, v in solution.items() if k not in original_ecu_keys}
            
            file_path = resource_path("DoC/" + str(solution["SOLUTION NAME"]) +"_report.pdf")

            if os.path.exists(file_path):
                exist = 1
            else:
                exist = 0

            solution['file_status'] = exist


            cleaned_solutions.append(solution)
        
        return cleaned_solutions
        
    except Exception as e:
        print(f"Error finding compatible solutions: {e}")
        return []


def result_summerizing(sw_req,hw_req,number,search_result_hw):

    if number == 0:
        solution_phrase = "没有找到可用方案, "
    else:
        solution_phrase = "一共找到:" + str(number) + "个方案, "    
    
    if number > 4:
        suggest_starter = "方案过多，建议添加"
        if not hw_req:
            hw_req_phrase = "硬件,"
        else:
            hw_req_phrase = ""

        if not sw_req:
            sw_req_phrase = "功能, "
        else:
            sw_req_phrase = ""

        suggest_finisher = "需求，以获取更精准的方案"
        suggesttion = suggest_starter + hw_req_phrase + sw_req_phrase + suggest_finisher
    else:
        suggesttion = ""

    summerizing = solution_phrase + suggesttion + search_result_hw
    
    return summerizing
    


# 辅助函数：比较SAE等级
def compare_sae_levels(level1, level2):
    """比较两个SAE等级，返回较高的等级"""
    # 提取基础等级（如L2）
    base1 = level1[0:2] if len(level1) >= 2 and level1[0] == 'L' else "L0"
    base2 = level2[0:2] if len(level2) >= 2 and level2[0] == 'L' else "L0"
    
    # 提取加号数量
    plus1 = level1.count('+')
    plus2 = level2.count('+')
    
    # 比较基础等级
    if base1 > base2:
        return level1
    elif base1 < base2:
        return level2
    else:
        # 基础等级相同，比较加号数量
        return level1 if plus1 > plus2 else level2


def solution_hunting(search_input,table_address):
    try:
        logging.debug('===============Here is a new day ================')
        # 从命令行获取参数
        search_content = json.loads(search_input)
        [sw_product,sw_req] = find_supported_sw_products(table_address,search_content["EUF"])
        print("Supported SW:" + str(sw_product) + "SW req stat " + str(sw_req))

        [hw_product,hw_req,search_result_hw] = find_supported_hw_products(table_address,search_content["HW"])
        print(search_result_hw)
        print("Supported HW:" + str(hw_product)+ "HW req stat " + str(hw_req))

       
        solution = find_compatible_solutions(table_address, sw_product,hw_product,sw_req,hw_req)
        note = result_summerizing(sw_req,hw_req,len(solution),search_result_hw)
        solution = [solution,note]
        return (json.dumps(solution))


    except Exception as e:
        sys.exit(1)
        return (json.dumps({"error": str(e)}))
        

# if __name__ == "__main__":
#     solution_hunting()