import pandas as pd
import re
import json

# 保留原有的解析复杂值的函数，用于处理INTERFACE属性
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
    if 'ITEMS' in result and not result['ITEMS']:
        del result['ITEMS']
    
    return result if result else value

# 保留build_nested_dict函数，用于处理嵌套属性
def build_nested_dict(nested_dict, parts, value):
    current = nested_dict
    for i, part in enumerate(parts):
        if i == len(parts) - 1:
            current[part] = value
        else:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]

def create_part_catalogue(file_path):
    # 读取Excel文件中的PART_POOL表格
    df = pd.read_excel(file_path, sheet_name='PART_POOL')
    
    # 创建按PRODUCT_TYPE分组的结果字典
    part_catalogue = {}
    
    # 遍历表格中的每一行
    for _, row in df.iterrows():
        # 获取产品名称和类型
        product_name = row.get('PRODUCT_NAME')
        product_type = row.get('PRODUCT_TYPE')
        
        # 跳过空行
        if pd.isna(product_name) or pd.isna(product_type):
            continue
        
        # 确保PRODUCT_TYPE对应的数组存在
        if product_type not in part_catalogue:
            part_catalogue[product_type] = []
        
        # 为当前产品创建条目
        product_item = {
            'PRODUCT_NAME': product_name
        }
        
        # 获取并添加PRODUCT_TAGS属性
        product_tags = row.get('PRODUCT_TAGS')
        if not pd.isna(product_tags):
            product_item['PRODUCT_TAGS'] = product_tags
        
        # 处理以PROP:开头的属性列，特别是INTERFACE相关的属性
        for col in df.columns:
            if col.startswith('PROP:') and not pd.isna(row[col]):
                # 分割属性路径
                prop_parts = col.split(':')[1:]
                # 解析属性值
                value = parse_complex_value(row[col])
                # 构建嵌套属性
                build_nested_dict(product_item, prop_parts, value)
        
        # 将产品条目添加到对应类型的数组中
        part_catalogue[product_type].append(product_item)
    
    # 返回JSON格式的结果
    return json.dumps(part_catalogue)

