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

def create_chipset_catalogue(file_path):
    df = pd.read_excel(file_path, sheet_name='COMPONENT_POOL')

    chipset_catalogue = {}
    # 初始化三个统计字典
    domain_counts = {}
    type_counts = {}
    supplier_counts = {}
    
        # 将build_nested_dict函数定义在循环外部
    def build_simple_dict(nested_dict, parts, value):
            nested_dict[parts] = value
    # 将build_nested_dict函数定义在循环外部
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
        product_name = row.get('PRODUCT_NAME')
        product_variant = row.get('PRODUCT_VARIANT')
        if pd.isna(product_name) or pd.isna(product_variant):
            continue
        if product_variant == "/":
            key = f"{product_name}"
        else:
            key = f"{product_name}_{product_variant}"
        item = {}
        
        for col in df.columns:
            if col.startswith('PRODUCT_NAME'):
                value =key
                name = "PRODUCT_NAME"
                item[name] = value
                # build_simple_dict(item,name,value)
                # build_nested_dict(item, name, value)
            elif col.startswith('PRODUCT_VARIANT'):
                continue
            if pd.isna(row[col]):
                continue
            if col.startswith('PROP:'):
                prop_parts = col.split(':')[1:]
                value = parse_complex_value(row[col])
                build_nested_dict(item, prop_parts, value)
            # elif col.startswith('PRODUCT_NAME'):
            #     value =row[col]
            #     name = "product_name"
            #     build_nested_dict(item, name, value)
        # 更新DOMAIN统计 - 支持逗号分隔的多个值
        domain_value = item.get('DOMAIN')

        if isinstance(domain_value, dict):
            domain_value = list(domain_value.keys()) if domain_value else None
        if isinstance(domain_value,list):
            for d in domain_value:
                if isinstance(d, (str, int, float)):
                    domain_counts[d] = domain_counts.get(d, 0) + 1
        elif domain_value and not pd.isna(domain_value):
            if isinstance(domain_value, str):
                # 拆分逗号分隔的多个值
                domains = [d.strip() for d in domain_value.split(',') if d.strip()]
                for d in domains:
                    if isinstance(d, (str, int, float)):
                        domain_counts[d] = domain_counts.get(d, 0) + 1
            elif isinstance(domain_value, (int, float)):
                domain_counts[domain_value] = domain_counts.get(domain_value, 0) + 1
        
        # 更新TYPE统计 - 添加类型检查
        type_value = item.get('TYPE')
        if isinstance(type_value, dict):
            type_value = next(iter(type_value.values())) if type_value else None
        if type_value and not pd.isna(type_value) and isinstance(type_value, (str, int, float)):
            type_counts[type_value] = type_counts.get(type_value, 0) + 1
        
        # 更新SUPPLIER统计 - 添加类型检查
        supplier_value = item.get('SUPPLIER')
        if isinstance(supplier_value, dict):
            supplier_value = next(iter(supplier_value.values())) if supplier_value else None
        if supplier_value and not pd.isna(supplier_value) and isinstance(supplier_value, (str, int, float)):
            supplier_counts[supplier_value] = supplier_counts.get(supplier_value, 0) + 1
        
        chipset_catalogue[key] = item
    
    # 创建包含所有四个字典的大字典
    chipset_product = {
        'chipset_catalogue': chipset_catalogue,
        'DOMAIN': domain_counts,
        'TYPE': type_counts,
        'SUPPLIER': supplier_counts
    }

    return (json.dumps(chipset_product))

