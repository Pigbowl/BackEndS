import os
import pandas as pd
import json
import difflib



def calculate_similarity(str1, str2):
    """
    计算两个字符串的相似度
    使用difflib的ratio方法，返回0-1之间的相似度值
    """
    # 将字符串转换为小写以进行不区分大小写的比较
    str1_lower = str1.lower()
    str2_lower = str2.lower()
    
    # 计算相似度
    similarity = difflib.SequenceMatcher(None, str1_lower, str2_lower).ratio()
    return similarity

def process_regulation_matrix(result_dict, data_storage_path):
    """
    根据regulation_first_row.json和regulation_process_data生成regulation_matrix对象。
    regulation_first_row中的每个成员作为key，value默认为"/"
    对于regulation_process_data中的每个key，进行匹配处理并更新regulation_matrix
    """
    first_row_json_path = os.path.join(data_storage_path, 'regulation_first_row.json')
    output_matrix_path = os.path.join(data_storage_path, 'regulation_matrix.json')
    
    # 检查文件是否存在
    if not os.path.exists(first_row_json_path):
        print(f"错误：{first_row_json_path} 文件不存在")
        return
    
    try:
        # 读取regulation_first_row.json文件
        with open(first_row_json_path, 'r', encoding='utf-8') as json_file:
            first_row_data = json.load(json_file)
        
        # 将first_row_data转换为字符串列表以便比较
        first_row_strings = [str(item) for item in first_row_data]
        
        # 生成regulation_matrix对象，每个key的value默认为"/"
        regulation_matrix = {}
        for item in first_row_strings:
            regulation_matrix[item] = "/"
        
        print(f"\n成功读取 {len(first_row_strings)} 个第一行数据项")
        print(f"已生成regulation_matrix，共 {len(regulation_matrix)} 个key")
        
        # 处理regulation_process_data中的每个key
        for key, value in result_dict.items():
            key_str = str(key)
            
            # 检查是否存在完全匹配
            if key_str in regulation_matrix:
                # 完全匹配，直接更新value
                regulation_matrix[key_str] = value
                print(f"\nkey '{key}' 在regulation_matrix中找到完全匹配，已更新value为: '{value}'")
                continue
            
            print(f"\n正在为key '{key}' 查找相似匹配项...")
            
            # 计算与每个first_row数据项的相似度
            similarities = []
            for item in first_row_strings:
                similarity = calculate_similarity(key, item)
                similarities.append((item, similarity))
            
            # 按相似度降序排序
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # 取前3个最相似的匹配项
            top_matches = similarities[:3]
            
            # 显示给用户并让用户选择
            print(f"\n为 '{key}' 找到的3个最相似匹配项:")
            for i, (match, similarity) in enumerate(top_matches, 1):
                print(f"{i}. '{match}' (相似度: {similarity:.4f})")
            
            # 获取用户输入
            selected_match = None
            while True:
                try:
                    user_input = input("请选择匹配的项 (输入1-3): ")
                    choice = int(user_input)
                    if 1 <= choice <= len(top_matches):
                        selected_match = top_matches[choice-1][0]
                        print(f"您选择了: '{selected_match}'")
                        break
                    else:
                        print("请输入1-3之间的数字")
                except ValueError:
                    print("请输入有效的数字")
            
            # 更新regulation_matrix中对应key的value
            if selected_match:
                regulation_matrix[selected_match] = value
                print(f"已将regulation_matrix中 '{selected_match}' 的value更新为: '{value}'")
        
        # 保存regulation_matrix为JSON文件
        with open(output_matrix_path, 'w', encoding='utf-8') as json_file:
            json.dump(regulation_matrix, json_file, ensure_ascii=False, indent=2)
        
        print(f"\n所有key处理完成！")
        print(f"regulation_matrix已保存至：{output_matrix_path}")
        print(f"总共处理了 {len(result_dict)} 个key")
        print(f"成功匹配并更新了 {sum(1 for v in regulation_matrix.values() if v != '/')} 个值")
        
    except json.JSONDecodeError:
        print(f"错误：无法解析 {first_row_json_path} 文件，请检查文件格式")
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
    
    except json.JSONDecodeError:
        print(f"错误：无法解析 {first_row_json_path} 文件，请检查文件格式")
    except Exception as e:
        print(f"处理相似度匹配时发生错误: {str(e)}")

def process_regulation_data():
    """
    读取Regulation.xlsx中Country Overview工作表的G列数据，按照规则处理并生成JSON格式数据。
    
    规则：
    1. 从第6行开始读取G列数据
    2. 若值含有In drafting, Regulated, Mandatory，则保存F列数据为key，G列数据为value
    3. 若值不为空且不包含上述内容，则保存该值为key，value为"Mandatory"
    4. 若值为空则跳过
    """
    # 设置文件路径
    data_storage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'DataStorage')
    excel_file_path = os.path.join(data_storage_path, 'Regulation.xlsx')
    output_json_path = os.path.join(data_storage_path, 'regulation_processed.json')
    
    try:
        # 检查Excel文件是否存在
        if not os.path.exists(excel_file_path):
            print(f"错误：Excel文件 {excel_file_path} 不存在")
            return
        
        # 重要：不设置header参数，直接读取所有数据
        # 这样我们可以完全控制数据的读取方式
        df = pd.read_excel(excel_file_path, sheet_name='Country Overview', header=None)
        
        # print(f"数据框形状: {df.shape}")
        # print(f"数据框的前10行:\n{df.head(10)}")
        
        # 创建结果字典
        result_dict = {}
        
        # 从第6行开始处理数据（注意pandas索引从0开始，所以第6行是索引5）
        for index in range(6, len(df)):
            try:
                # 使用索引访问列：F列是第6列（索引5），G列是第7列（索引6）
                f_value = df.iloc[index, 5] if index < len(df) and 5 < len(df.columns) else ''
                g_value = df.iloc[index, 6] if index < len(df) and 6 < len(df.columns) else ''
                
                # print(f"行{index+1} - F列(索引5): {f_value}, G列(索引6): {g_value}")
                
                # 检查G列是否为空
                if pd.isna(g_value) or (isinstance(g_value, str) and g_value.strip() == ''):
                    # print(f"  跳过：G列值为空")
                    continue
                
                # 将值转换为字符串
                g_value_str = str(g_value)
                f_value_str = str(f_value) if pd.notna(f_value) else ''
                
                # 检查G列值是否包含特定关键词
                keywords = ['in drafting', 'Regulated', 'Mandatory']
                contains_keyword = any(keyword in g_value_str for keyword in keywords)
                
                if contains_keyword:
                    # 检查F列数据是否为0或"-"
                    f_stripped = f_value_str.strip()
                    if f_stripped == '' or f_stripped == '0' or f_stripped == '-':
                        print(f"  跳过：F列数据为0或'-'")
                        continue
                    # 包含关键词且F列数据有效，使用F列作为key，G列作为value
                    result_dict[f_stripped] = g_value_str.strip()
                    # print(f"  添加: {f_stripped} -> {g_value_str.strip()}")
                elif not contains_keyword and g_value_str.strip() != '' and g_value_str.strip() != '-':
                    # 不包含关键词，使用G列作为key，value为Mandatory
                    if f_stripped == '' or f_stripped == '0' or f_stripped == '-':
                        print(f"  跳过：F列数据为0或'-'")
                        continue
                    result_dict[g_value_str.strip()] = 'Mandatory'
                    print("the key is",g_value_str.strip())
                    # print(f"  添加: {g_value_str.strip()} -> 'Mandatory'")
                else:
                    print(f"  跳过：不符合条件")
                    
            except Exception as e:
                print(f"处理行{index+1}时出错: {str(e)}")
        
        # 将结果保存为JSON文件
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(result_dict, json_file, ensure_ascii=False, indent=2)
        
        print(f"\n成功处理 {len(result_dict)} 条数据")
        print(f"JSON文件已保存至：{output_json_path}")
        
        # 处理并生成regulation_matrix
        process_regulation_matrix(result_dict, data_storage_path)
        
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    process_regulation_data()