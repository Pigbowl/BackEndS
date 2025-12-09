import sys
import os

# 将当前目录添加到sys.path中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Python_S.ReadDBAndGenerateProtocol import export_table_columns_with_foreign_key, generate_new_object_data_structure_layer

# 调用export_table_columns_with_foreign_key获取测试数据
processed_results, lib_tables_data = export_table_columns_with_foreign_key()

# 选择一个存在的主表进行测试
# 这里假设数据库中有一个名为'work'的表，你可以根据实际情况修改
target_table = 'work'

# 调用修改后的函数生成数据结构
result = generate_new_object_data_structure_layer(processed_results, lib_tables_data, target_table)

# 打印结果
print("生成的数据结构：")
print(result)
