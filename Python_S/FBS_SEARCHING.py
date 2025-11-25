import pandas as pd
import json

def process_feature_input(input_str):
    """
    处理输入的feature名称：
    - 若包含'-'则保持原样
    - 否则在末尾添加'-Basic'
    """
    if '-' in input_str:
        return input_str.strip()
    else:
        return f"{input_str.strip()}-Basic"

def fbsbaseinit(table_address):
    """
    处理Excel文件，提取三个sheet的数据并生成指定格式的字典
    """
    try:
        file_path = table_address
        # 读取三个sheet
        df_subfeatures = pd.read_excel(file_path, sheet_name='SUBFEATURES')
        df_mainfunc = pd.read_excel(file_path, sheet_name='MAIN FUNCTION')
        df_techfunc = pd.read_excel(file_path, sheet_name='TECHNICAL FUNCTION')
        
        # 1. 生成EUF_LIST
        euf_list = []
        if not df_subfeatures.empty:
            for _, row in df_subfeatures.iterrows():
                feature_index = str(row.get('FEATURE_INDEX', '')).strip()
                feature_name = str(row.get('FEATURE_NAME', '')).strip()
                
                if feature_index:  # 跳过空的INDEX
                    euf_entry = {
                        'id': feature_index,
                        'name': feature_index,  # 根据需求，name填充FEATURE_INDEX
                        'desc': feature_name
                    }
                    euf_list.append(euf_entry)
        
        # 2. 生成MF_LIST
        mf_list = []
        if not df_mainfunc.empty:
            for _, row in df_mainfunc.iterrows():
                func_index = str(row.get('FUNCTION_INDEX', '')).strip()
                func_name = str(row.get('FUNCTION_NAME', '')).strip()
                
                if func_index:  # 跳过空的INDEX
                    mf_entry = {
                        'id': func_index,
                        'name': func_index,  # 根据需求，name填充FUNCTION_INDEX
                        'desc': func_name
                    }
                    mf_list.append(mf_entry)
        
        # 3. 生成TF_LIST
        tf_list = []
        if not df_techfunc.empty:
            for _, row in df_techfunc.iterrows():
                func_index = str(row.get('FUNCTION_INDEX', '')).strip()
                func_name = str(row.get('FUNCTION_NAME', '')).strip()
                
                if func_index:  # 跳过空的INDEX
                    tf_entry = {
                        'id': func_index,
                        'name': func_index,  # 根据需求，name填充FUNCTION_INDEX
                        'desc': func_name
                    }
                    tf_list.append(tf_entry)
        
        # 4. 生成EUF2MF映射
        euf2mf = {}
        if not df_subfeatures.empty and not df_mainfunc.empty:
            # 构建FUNCTION_NAME到FUNCTION_INDEX的映射字典
            name_to_index = {
                str(row.get('FUNCTION_NAME', '')).strip(): str(row.get('FUNCTION_INDEX', '')).strip()
                for _, row in df_mainfunc.iterrows()
            }
            
            for _, row in df_subfeatures.iterrows():
                feature_index = str(row.get('FEATURE_INDEX', '')).strip()
                if not feature_index:
                    continue
                    
                # 查找所有FBS:MF:开头的列
                mf_indices = []
                for col in df_subfeatures.columns:
                    if col.startswith('FBS:MF:'):
                        mf_name = col.split(':', 2)[2].strip()
                        value = str(row[col]).strip().upper()
                        
                        if value == 'Y' and mf_name in name_to_index:
                            mf_indices.append(name_to_index[mf_name])
                
                if mf_indices:
                    euf2mf[feature_index] = mf_indices
        
        # 5. 生成MF2TF映射
        mf2tf = {}
        if not df_mainfunc.empty:
            for _, row in df_mainfunc.iterrows():
                func_index = str(row.get('FUNCTION_INDEX', '')).strip()
                if not func_index:
                    continue
                    
                # 查找所有FBS:TF:开头的列
                tf_indices = []
                for col in df_mainfunc.columns:
                    if col.startswith('FBS:TF:'):
                        tf_value = str(row[col]).strip()
                        
                        if tf_value and tf_value.upper() != 'X':
                            tf_indices.append(tf_value)
                
                if tf_indices:
                    mf2tf[func_index] = tf_indices
        
        # 构建最终结果字典
        result = {
            'EUF_LIST': euf_list,
            'MF_LIST': mf_list,
            'TF_LIST': tf_list,
            'EUF2MF': euf2mf,
            'MF2TF': mf2tf
        }
        
        return(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"处理Excel文件时出错: {str(e)}")
        return None

def extract_single_feature(input_feature_name,table_address):
    """提取单个FEATURE的信息，为每个TF添加顺序编号"""
    try:
        excel_path = table_address
        
        # 读取SUBFEATURES工作表，筛选目标FEATURE
        df_subfeatures = pd.read_excel(excel_path, sheet_name='SUBFEATURES')
        if df_subfeatures.empty:
            raise ValueError("SUBFEATURES工作表为空")
        if 'FEATURE_NAME' not in df_subfeatures.columns:
            raise ValueError("SUBFEATURES工作表缺少'FEATURE_NAME'列")
        
        # 筛选目标FEATURE
        target_rows = df_subfeatures[
            df_subfeatures['FEATURE_NAME'].astype(str).str.strip() == input_feature_name
        ]
        if target_rows.empty:
            raise ValueError(f"未找到FEATURE: {input_feature_name}")
        
        # 初始化FEATURE数据结构
        feature_data = {
            'FUNCTION_NAME': input_feature_name,
            'FUNCTION_INDEX':"EUF1.1",
            'mf_functions': []  # 数组存储MF
        }
        
        # 提取该FEATURE关联的MF（有序数组）
        mf_names = []
        for col in df_subfeatures.columns:
            if col.startswith('FBS:MF:') and str(target_rows.iloc[0][col]).strip().upper() == 'Y':
                mf_name = col.split(':', 2)[2].strip()
                mf_names.append(mf_name)
        
        # 初始化MF数组
        for mf_name in mf_names:
            feature_data['mf_functions'].append({
                'FUNCTION_NAME': mf_name,
                'FUNCTION_INDEX': None,
                'tf_functions': []  # 数组存储TF
            })
        
        # 读取MAIN FUNCTION，提取MF的TF映射
        df_mainfunc = pd.read_excel(excel_path, sheet_name='MAIN FUNCTION')
        if not df_mainfunc.empty:
            mainfunc_name_col = df_mainfunc.columns[0]
            function_index_col = next(
                (col for col in df_mainfunc.columns if col.strip().upper() == 'FUNCTION_INDEX'),
                None
            )
            
            # 为每个MF填充信息
            for mf_data in feature_data['mf_functions']:
                mf_name = mf_data['FUNCTION_NAME']
                mf_rows = df_mainfunc[
                    df_mainfunc[mainfunc_name_col].astype(str).str.strip() == mf_name
                ]
                
                if not mf_rows.empty:
                    mf_row = mf_rows.iloc[0]
                    
                    # 填充MF的FUNCTION_INDEX
                    if function_index_col:
                        mf_data['FUNCTION_INDEX'] = str(mf_row[function_index_col]).strip()
                    
                    # 提取TF映射并转为有序数组
                    tf_mappings = []
                    for col in df_mainfunc.columns:
                        if col.startswith('FBS:TF:'):
                            tf_name = col.split(':', 2)[2].strip()
                            tf_index = str(mf_row[col]).strip()
                            if tf_index and tf_index.upper() != 'X':
                                tf_mappings.append({
                                    'tf_name': tf_name,
                                    'tf_index': tf_index
                                })
                    
                    # 按原key排序（确保顺序稳定）
                    tf_mappings.sort(key=lambda x: x['tf_name'])
                    mf_data['_temp_tf_mappings'] = [item['tf_index'] for item in tf_mappings]
        
        # 读取TECHNICAL FUNCTION，提取TF详情
        df_techfunc = pd.read_excel(excel_path, sheet_name='TECHNICAL FUNCTION')
        if not df_techfunc.empty:
            techfunc_index_col = next(
                (col for col in df_techfunc.columns if col.strip().upper() == 'FUNCTION_INDEX'),
                None
            )
            
            if techfunc_index_col:
                # 构建TF索引到详情的映射
                tf_detail_map = {
                    str(row[techfunc_index_col]).strip(): row.to_dict()
                    for _, row in df_techfunc.iterrows()
                }
                # 为每个MF填充TF详情（有序数组）
                for mf_data in feature_data['mf_functions']:
                    if '_temp_tf_mappings' in mf_data:
                        for tf_index in mf_data['_temp_tf_mappings']:
                            if tf_index in tf_detail_map:
                                tf_details = {
                                    k: str(v).strip()
                                    for k, v in tf_detail_map[tf_index].items()
                                    # if k != techfunc_index_col
                                }
                                mf_data['tf_functions'].append(tf_details)
                                print(tf_details)
                        # 移除临时字段
                        mf_data.pop('_temp_tf_mappings')
        
        # 后处理：统计数量、编号、计算位置
        feature_data['mf_count'] = len(feature_data['mf_functions'])
        feature_data['tf_total_count'] = sum(len(mf['tf_functions']) for mf in feature_data['mf_functions'])
        
        # 为MF编号、计算位置，并为TF顺序编号（全局顺序）
        previous_end = 0
        global_tf_number = 1  # TF全局编号（从1开始）
        
        for idx, mf in enumerate(feature_data['mf_functions'], 1):
            mf['mf_number'] = idx
            mf['tf_count'] = len(mf['tf_functions'])
            
            # 位置计算
            start = 1 if previous_end == 0 else previous_end
            length = mf['tf_count']
            end = start + length
            mf['position'] = {
                'start': start,
                'length': length,
                'end': end
            }
            previous_end = end
            
            # 为当前MF的每个TF添加全局编号
            for tf in mf['tf_functions']:
                tf['tf_number'] = global_tf_number  # 全局顺序编号
                global_tf_number += 1
        
        return feature_data
        
    except Exception as e:
        print(f"处理过程中出错：{str(e)}")
        return None


def fbsfindg(input_feature,table_address):
    # 处理输入
    processed_feature = process_feature_input(input_feature)
    print(f"处理后的feature名称：{processed_feature}")
    
    # 提取单个feature信息
    result = extract_single_feature(processed_feature,table_address)
    # 输出结果
    if result:
        print("\n提取的FEATURE信息：")
        return(json.dumps(result, ensure_ascii=False, indent=2))
    
