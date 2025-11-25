import pandas as pd
import re
import json

def build_nested_dict(flat_dict):
    nested_dict = {}
    for key, value in flat_dict.items():
        parts = key.split(':')
        current = nested_dict
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                # 处理属性值
                parsed_value = parse_complex_value(value)
                # 检查是否有类型冲突
                if part in current:
                    existing_value = current[part]
                    if not isinstance(existing_value, dict):
                        # 如果已存在的值不是字典，将其转换为字典
                        current[part] = {'value': existing_value}
                current[part] = parsed_value
            else:
                if part not in current or not isinstance(current[part], dict):
                    current[part] = {}
                current = current[part]
    return nested_dict


def parse_complex_value(value):
    if not isinstance(value, str):
        return value
    
    # 使用正则表达式分割不在方括号内的逗号
    parts = [p.strip() for p in re.split(r',(?![^\[]*\])', value) if p.strip()]
    # 如果只有一个部分且不包含特殊格式，直接返回该值
    if len(parts) == 1:
        part = parts[0]
        # 检查是否包含特殊格式
        if not (re.match(r'^([^:]+):(.*)$', part) or re.match(r'^\d+\*.*$', part)):
            return part
    
    result = {}
    # 初始化A*B格式结果字典
    result['ITEMS'] = {}
    item_count = 1  # 用于生成序号键
    
    for part in parts:
        # 处理 A:B 格式
        ab_match = re.match(r'^([^:]+):(.*)$', part)
        if ab_match:
            key = ab_match.group(1).strip()
            value = ab_match.group(2).strip()
            result[key] = value
            continue
        
        # 处理 A*B 格式
        ab_match = re.match(r'^(\d+)\*(.*)$', part)
        if ab_match:
            number = int(ab_match.group(1).strip())
            name = ab_match.group(2).strip()
            # 使用序号作为键存储到字典
            result[str(item_count)] = {'NAME': name, 'NUMBER': number}
            item_count += 1
            continue
        
        # 如果没有匹配的格式，直接作为值
        result[part] = True
    
    # 如果没有A*B结果，移除ITEMS键
    if not result['ITEMS']:
        del result['ITEMS']
    
    return result if result else value

def create_sensor_catalogue(file_path):
    # 读取SENSOR CHOICE工作表
    df = pd.read_excel(file_path, sheet_name='SENSOR CHOICE')

    sensor_catalogue = {}
    # 初始化统计字典
    type_counts = {}
    
    # 嵌套的build_nested_dict函数
    def build_nested_dict(nested_dict, parts, value):
        current = nested_dict
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                current[part] = value
            else:
                if part not in current or not isinstance(current[part], dict):
                    current[part] = {}
                current = current[part]
    
    for _, row in df.iterrows():
        # 跳过空行
        if all(pd.isna(row[col]) for col in df.columns):
            continue
        
        # 获取PRODUCT_NAME作为key（表格第一列）
        product_name = row.iloc[0]  # 使用iloc[0]获取第一列值
        if pd.isna(product_name):
            continue
        
        item = {}
        
        # 添加PRODUCT_NAME作为NAME属性
        item['NAME'] = product_name
        
        for col in df.columns:
            if pd.isna(row[col]):
                continue
            if col.startswith('PROP:'):
                prop_parts = col.split(':')[1:]
                value = parse_complex_value(row[col])
                build_nested_dict(item, prop_parts, value)
        
        # 获取TYPE属性值作为分类键
        type_value = item.get('TYPE')
        if not type_value:
            continue
        
        # 更新TYPE统计
        type_counts[type_value] = type_counts.get(type_value, 0) + 1
        
        # 按TYPE分类存储，使用PRODUCT_NAME作为key
        if type_value not in sensor_catalogue:
            sensor_catalogue[type_value] = {}
        sensor_catalogue[type_value][product_name] = item
    
    # 构建返回结构
    sensor_product = {
        'sensor_catalogue': sensor_catalogue,
        'TYPE': type_counts
    }
    print(sensor_product)
    return json.dumps(sensor_product)

