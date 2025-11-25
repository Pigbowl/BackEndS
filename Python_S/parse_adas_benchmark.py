import pandas as pd
import os
import json
import logging
import sys

# 配置日志记录
logging.basicConfig(
    filename='debug.log',  # 日志文件路径
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 递归计数传感器函数
def count_sensors_recursive(sensor_config, sensor_counts):
    # 在顶层识别传感器类型
    for key, value in sensor_config.items():
        sensor_type = None
        if key.startswith('CAM'):
            sensor_type = 'CAM'
        elif key.startswith('RDR'):
            sensor_type = 'RDR'
        elif key.startswith('LIDAR'):
            sensor_type = 'LIDAR'
        elif key.startswith('USS'):
            sensor_type = 'USS'
        
        if sensor_type:
            # 递归统计该传感器类型下非"/"的值的数量
            count = count_non_slash_values(value)
            sensor_counts[sensor_type] += count

def count_non_slash_values(data):
    # 递归统计非"/"的值的数量
    count = 0
    if isinstance(data, dict):
        for value in data.values():
            count += count_non_slash_values(value)
    elif data != '/':
        count += 1
    return count

def parse_adas_benchmark(file_path):
    # 读取Excel文件
    try:
        # 假设VEH_CONFIG是工作表名称
        df = pd.read_excel(file_path, sheet_name='VEH_CONFIG')
        print(f"成功读取工作表: VEH_CONFIG")
    except Exception as e:
        print(f"读取Excel文件失败: {str(e)}")
        return None

    # 创建结果字典
    result = {}

    # 获取车型名称列表（第一行数据）
    car_models = df.columns[1:].tolist()  # 跳过第一列（header列）

    # 遍历每一行数据
    for index, row in df.iterrows():
        header = row[0]  # 第一列是header

        # 跳过空header行
        if pd.isna(header):
            continue

        # 遍历每个车型
        for i, car_model in enumerate(car_models):
            value = row[i+1]  # 第一列是header，所以车型数据从第二列开始

            # 如果车型不在结果字典中，创建它
            if car_model not in result:
                result[car_model] = {}

            # 解析header为层次化结构
            parts = header.split(':')
            current_level = result[car_model]

            # 构建层次化字典
            for part in parts[:-1]:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]

            # 设置最终值
            current_level[parts[-1]] = value

    # 添加传感器统计功能
    for car_model in result:
        car_config = result[car_model]
        # 检查是否存在PROP:SENSOR节点
        if 'PROP' in car_config and 'SENSOR' in car_config['PROP']:
            sensor_config = car_config['PROP']['SENSOR']
            # 初始化传感器计数器
            sensor_counts = {
                'CAM': 0,
                'RDR': 0,
                'LIDAR': 0,
                'USS': 0
            }
            
            # 递归遍历所有传感器配置项
            count_sensors_recursive(sensor_config, sensor_counts)
            
            # 生成统计结果字符串（只包含数量大于0的传感器）
            parts = []
            if sensor_counts['CAM'] > 0:
                parts.append(f"{sensor_counts['CAM']}V")
            if sensor_counts['RDR'] > 0:
                parts.append(f"{sensor_counts['RDR']}R")
            if sensor_counts['LIDAR'] > 0:
                parts.append(f"{sensor_counts['LIDAR']}L")
            if sensor_counts['USS'] > 0:
                parts.append(f"{sensor_counts['USS']}U")
            total_str = ''.join(parts)
            
            detail_dict = {
                'CAM': str(sensor_counts['CAM']),
                'RDR': str(sensor_counts['RDR']),
                'LIDAR': str(sensor_counts['LIDAR']),
                'USS': str(sensor_counts['USS'])
            }
            # 将统计结果添加到SENSOR节点下
            sensor_config['STATISTICS'] = {
                'TOTAL': total_str,
                'DETAIL': detail_dict
            }

        # 添加SOC和MCU信息提取逻辑
        if 'PROP' in car_config:
            prop = car_config['PROP']
            unified = prop.get('UNIFIED', 'N')  # 默认非一体方案

            # 初始化SOC和MCU集合
            soc_set = set()
            mcu_set = set()

            # 提取AD系统的ECU信息
            if 'AD_SYSTEM' in prop and 'ECU' in prop['AD_SYSTEM']:
                ad_ecu = prop['AD_SYSTEM']['ECU']
                if isinstance(ad_ecu, dict):
                    # 从字典中提取SOC信息
                    if 'SOC' in ad_ecu and ad_ecu['SOC'] and ad_ecu['SOC'] != '/':
                        soc_set.add(ad_ecu['SOC'])
                    # 从字典中提取MCU信息
                    if 'MCU' in ad_ecu and ad_ecu['MCU'] and ad_ecu['MCU'] != '/':
                        mcu_set.add(ad_ecu['MCU'])

            # 提取AP系统的ECU信息
            if 'AP_SYSTEM' in prop and 'ECU' in prop['AP_SYSTEM']:
                ap_ecu = prop['AP_SYSTEM']['ECU']
                if isinstance(ap_ecu, dict):
                    # 从字典中提取SOC信息
                    if 'SOC' in ap_ecu and ap_ecu['SOC'] and ap_ecu['SOC'] != '/':
                        # 如果是一体方案且AD系统已有相同SOC，则不添加
                        if unified != 'Y' or ap_ecu['SOC'] not in soc_set:
                            soc_set.add(ap_ecu['SOC'])
                    # 从字典中提取MCU信息
                    if 'MCU' in ap_ecu and ap_ecu['MCU'] and ap_ecu['MCU'] != '/':
                        # 如果是一体方案且AD系统已有相同MCU，则不添加
                        if unified != 'Y' or ap_ecu['MCU'] not in mcu_set:
                            mcu_set.add(ap_ecu['MCU'])

            # 生成SOC和MCU字符串
            soc_str = ','.join(soc_set) if soc_set else ''
            mcu_str = ','.join(mcu_set) if mcu_set else ''

            # 组合成最终字符串
            parts = []
            if soc_str:
                parts.append(f"{soc_str}")
            # if mcu_str:
            #     parts.append(f"{mcu_str}")
            soc_mcu_str = ','.join(parts) if parts else ''

            # 添加到PROP字典
            if 'ECU_INFO' not in prop:
                prop['ECU_INFO'] = {}
            prop['ECU_INFO']['SOC_MCU'] = soc_mcu_str

    return result

def benchmarkinfofetch(file_path):
    # 解析Excel文件
    try:
        logging.debug('===============Here is a new day ================')
        result = parse_adas_benchmark(file_path)
    
        # 收集所有OEM信息
        oem_set = set()
        for car_model in result:
            car_config = result[car_model]
            if 'PROP' in car_config and 'BRAND' in car_config['PROP']:
                oem = car_config['PROP']['BRAND']
                if oem and oem != '/':
                    oem_set.add(oem)

        
        # 创建包含result和OEM集合的新字典
        final_result = {
            'result': result,
            'oem_array': list(oem_set)
        }
        
        return (json.dumps(final_result))
    except Exception as e:
        logging.error(f"处理Excel文件时出错: {str(e)}")
        return (json.dumps({"error": str(e)}))
