import json
from typing import Dict, List, Any
from Python_S.sql_operations import SQLOperations

class JSONToSQLmaintarget:
    def __init__(self,data: dict = None):
        self.data = data  # 直接使用传入的数据
        self.db = None
        self.id_columns_map = {}  # 存储各表的ID列名映射
        self.operation_records = []  # 存储操作记录的数组
        
    def load_json_data(self):
        """加载JSON数据（如果数据未传入，则从文件加载）"""
        # 如果数据已经传入，则不需要加载文件
        if self.data is not None:
            print("直接使用传入的数据")
            return True
        
        # 否则从文件加载
        if not self.json_file_path:
            print("未提供JSON文件路径，无法加载数据")
            return False
            
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"成功加载JSON文件: {self.json_file_path}")
            return True
        except Exception as e:
            print(f"加载JSON文件失败: {str(e)}")
            return False
    
    def connect_to_database(self):
        """连接到数据库"""
        try:
            # 使用sql_operations.py中的示例连接信息
            self.db = SQLOperations(
            )
            print("成功连接到数据库")
            
            # 加载objects表信息，获取各表的ID列名
            self._load_id_columns_info()
            return True
        except Exception as e:
            print(f"连接数据库失败: {str(e)}")
            return False
    
    def _load_id_columns_info(self):
        """从objects表加载各表的ID列名信息"""
        try:
            objects_data = self.db.read_data('objects')
            for item in objects_data:
                self.id_columns_map[item['OBJECT']] = item['ID']
            print(f"加载的ID列名映射: {self.id_columns_map}")
        except Exception as e:
            print(f"加载ID列名信息失败: {str(e)}")
    
    def process_data(self):
        """处理JSON数据并执行相应的SQL操作"""
        if not self.data or not self.db:
            print("请先加载JSON数据并连接数据库")
            return False
        
        try:
            # 获取顶层children数据
            if 'children' not in self.data:
                print("JSON数据中没有children字段")
                return False
            
            children = self.data['children']
            
            # 存储已处理行的ID映射
            row_ids = {}
            
            # 首先处理所有主表（row类型）的数据
            for parent_item in children:
                # 递归处理所有row类型的数据
                self._process_item(parent_item, row_ids)
            
            return True
        except Exception as e:
            print(f"处理数据时出错: {str(e)}")
            return False
    
    def _process_item(self, item: Dict[str, Any], row_ids: Dict[str, Any], parent_table: str = None):
        """递归处理数据项"""
        # 处理row类型的数据
        if item.get('itemlevel') == 'row' and item.get('itemtype') == 'item':
            self._process_row(item, row_ids, parent_table)
        
        # 递归处理子项
        if 'children' in item:
            for child in item['children']:
                # 如果当前是table类型，传递表名给子项
                if item.get('itemlevel') == 'table':
                    self._process_item(child, row_ids, item.get('tablename'))
                else:
                    self._process_item(child, row_ids, parent_table)
    
    def _process_row(self, row_item: Dict[str, Any], row_ids: Dict[str, Any], parent_table: str = None):
        """处理row类型的数据"""

        table_name = row_item.get('tablename')
        modifystate = row_item.get('modifystate')
        
        if not table_name:
            print("跳过缺少表名的行数据")
            return
        if itemtype := row_item.get('itemtype'):
            if itemtype != 'item':
                print(f"跳过非item类型的行数据，类型: {itemtype}")
                return
        print(f"\n处理表 {table_name} 的行数据，操作类型: {modifystate}")

        # 获取该表的ID列名
        # 先从缓存映射中查找
        id_column = self.id_columns_map.get(table_name)

        if id_column is None:
            # 缓存未命中，查询数据库获取主键列名
            try:
                # 查询该表的主键列
                primary_key_info = self.db.read_data(
                    'information_schema.KEY_COLUMN_USAGE',
                    conditions={
                        'TABLE_SCHEMA': self.db.database,  # 使用数据库名而不是连接对象
                        'TABLE_NAME': table_name,
                        'CONSTRAINT_NAME': 'PRIMARY'
                    }
                )
                print(primary_key_info)
                if primary_key_info:
                    id_column = primary_key_info[0]['COLUMN_NAME']
                else:
                    # 如果查不到主键，默认使用ID
                    id_column = 'ID'
                # 将结果写入缓存
                self.id_columns_map[table_name] = id_column
            except Exception as e:
                print(f"查询表 {table_name} 主键列失败: {str(e)}，默认使用ID")
                id_column = 'ID'

        # 处理列数据
        columns_data = {}
        fetch_columns = {}
        
        if 'children' in row_item:

            for column_item in row_item['children']:
                
                if column_item.get('itemlevel') == 'column':

                    col_id = column_item.get('id')
                    col_type = column_item.get('type')
                    col_value = column_item.get('value')
                    insert_flag = column_item.get('insert', True)
                    col_modifystate = column_item.get('modifystate')

                    # 处理fetch类型的数据
                    if col_type == 'fetch':
                        fetch_columns[col_id] = col_value
                        continue

                    # 根据row的modifystate决定如何处理列数据
                    if modifystate == 'creation':
                        # 创建新行，只处理insert为True的列
                        if insert_flag:
                            columns_data[col_id] = col_value
                    elif modifystate == 'change':
                        # 修改现有行，只处理modifystate为change的列
                        if col_modifystate == 'change':
                            columns_data[col_id] = col_value
                    elif modifystate == 'todelete':
                        columns_data[col_id] = None

        # 处理fetch类型的列，从已处理的行中获取ID
        for fetch_col_id, fetch_ref_id in fetch_columns.items():
            # 查找对应的主表行ID

            for table_key, row_id in row_ids.items():

                if fetch_ref_id in table_key:

                    columns_data[fetch_col_id] = row_id
                    # print(f"为列 {fetch_col_id} 设置主表ID值: {row_id}")
                    break

        # 执行SQL操作
        if modifystate == 'creation':
            # 插入新行
            row_id = self.db.insert_data(table_name, columns_data)
            if row_id > 0:
                # 存储插入的行ID，用于后续的fetch类型列
                row_ids[f"{table_name}_{id_column}"] = row_id
                print(f"成功插入行，ID: {row_id}，表: {table_name}")
                
                # 记录操作
                record = {
                    "table_name": table_name,
                    "operation_type": "insert",
                    "success": True,
                    "data": columns_data,
                    "row_id": row_id
                }
                self.operation_records.append(record)
            else:
                print(f"插入行失败，表: {table_name}")
                
                # 记录操作
                record = {
                    "table_name": table_name,
                    "operation_type": "insert",
                    "success": False,
                    "data": columns_data,
                    "error": "插入失败"
                }
                self.operation_records.append(record)
        elif modifystate == 'change':

            # 修改现有行，需要知道主键值
            # 这里假设row_item中包含了主键信息
            row_id_value = None
            for column_item in row_item.get('children', []):
                if column_item.get('id') == id_column and column_item.get('itemlevel') == 'column':
                    row_id_value = column_item.get('value')
                    break
            
            if row_id_value is not None:
                conditions = {id_column: row_id_value}
                affected_rows = self.db.update_data(table_name, columns_data, conditions)
                if affected_rows > 0:
                    # 更新row_ids中的ID映射
                    row_ids[f"{table_name}_{id_column}"] = row_id_value
                    print(f"成功修改行，影响行数: {affected_rows}，表: {table_name}")
                    
                    # 记录操作
                    record = {
                        "table_name": table_name,
                        "operation_type": "update",
                        "success": True,
                        "data": columns_data,
                        "row_id": row_id_value,
                        "conditions": conditions
                    }
                    self.operation_records.append(record)
                else:
                    print(f"修改行失败，未找到匹配的行，表: {table_name}")
                    
                    # 记录操作
                    record = {
                        "table_name": table_name,
                        "operation_type": "update",
                        "success": False,
                        "data": columns_data,
                        "row_id": row_id_value,
                        "error": "未找到匹配的行"
                    }
                    self.operation_records.append(record)
            else:
                print(f"修改行失败，缺少主键信息，表: {table_name}")
                
                # 记录操作
                record = {
                    "table_name": table_name,
                    "operation_type": "update",
                    "success": False,
                    "data": columns_data,
                    "error": "缺少主键信息"
                }
                self.operation_records.append(record)
        elif modifystate == 'todelete':
            # 删除现有行，需要知道主键值
            row_id_value = None
            actual_id_column = id_column
            
            # 方法0: 检查id_columns_map中的主键信息
            print(f"当前表: {table_name}, 从id_columns_map获取的主键列: {id_column}")
            
            # 方法1: 直接从row_item的children中查找所有列，特别关注ID相关列
            for column_item in row_item.get('children', []):
                column_id = column_item.get('id')
                column_value = column_item.get('value')
                print(f"检查列: {column_id}, 值: {column_value}, 是否主键列匹配: {column_id == id_column}")
                
                # 优先检查是否匹配id_column
                if column_id == id_column and column_item.get('itemlevel') == 'column':
                    row_id_value = column_value
                    print(f"从children中获取到主键值: {row_id_value}")
                    break
                
                # 如果没有匹配，尝试查找表名_ID或ID相关列（作为备选方案）
                if row_id_value is None and (column_id == f"{table_name}_ID" or column_id.endswith('_ID') or "ID" in column_id):
                    if column_value and column_value != 0:
                        row_id_value = column_value
                        actual_id_column = column_id
                        print(f"从children中找到疑似主键列: {actual_id_column}, 值: {row_id_value}")
            
            # 方法2: 如果方法1失败，尝试从row_ids字典中查找
            if row_id_value is None:
                table_key = f"{table_name}_{id_column}"
                if table_key in row_ids:
                    row_id_value = row_ids[table_key]
                    print(f"从row_ids中获取到主键值: {row_id_value}")
                else:
                    # 尝试遍历row_ids查找可能匹配的表键
                    for key, value in row_ids.items():
                        if key.startswith(f"{table_name}_"):
                            row_id_value = value
                            print(f"从row_ids中通过前缀匹配获取到主键值: {row_id_value}")
                            break
            
            # 打印所有子列信息用于调试
            print(f"行 {row_item.get('id')} 的所有子列信息:")
            for column_item in row_item.get('children', []):
                print(f"  - {column_item.get('id')}: {column_item.get('value')} (modifystate: {column_item.get('modifystate')})")
            
            if row_id_value is not None:
                conditions = {actual_id_column: row_id_value}
                print(f"执行删除操作: 表={table_name}, 条件={conditions}")
                affected_rows = self.db.delete_data(table_name, conditions)
                if affected_rows > 0:
                    # 更新row_ids中的ID映射
                    for key in list(row_ids.keys()):
                        if key.startswith(f"{table_name}_"):
                            del row_ids[key]
                    print(f"成功删除行，影响行数: {affected_rows}，表: {table_name}")
                    # 记录操作
                    record = {
                        "table_name": table_name,
                        "operation_type": "delete",
                        "success": True,
                        "row_id": row_id_value,
                        "conditions": conditions
                    }
                    self.operation_records.append(record)
                else:
                    print(f"删除行失败，未找到匹配的行，表: {table_name}，主键列: {actual_id_column}，值: {row_id_value}")
                    # 记录操作
                    record = {
                        "table_name": table_name,
                        "operation_type": "delete",
                        "success": False,
                        "row_id": row_id_value,
                        "error": "未找到要删除的行"
                    }
                    self.operation_records.append(record)
            else:
                # 获取row_item的更多信息用于调试
                row_item_id = row_item.get('id', 'N/A')
                row_item_name = row_item.get('name', 'N/A')
                print(f"删除行失败，缺少主键信息，表: {table_name}，使用的主键列: {id_column}，行ID: {row_item_id}，行名称: {row_item_name}")
                # 记录操作
                record = {
                    "table_name": table_name,
                    "operation_type": "delete",
                    "success": False,
                    "data": columns_data,
                    "error": "缺少主键信息"
                }
                self.operation_records.append(record)
        else:
            print(f"当前表: {table_name}, 从id_columns_map获取的主键列: {id_column}")
            # 根据当前表名获取对应的主键列名
            # id_colum = self.id_columns_map.get(table_name, 'ID')
            # 在children列表中查找id等于id_colum的列，并提取其value
            row_id_value = next(
                (col['value'] for col in row_item['children'] if col.get('id') == id_column),
                None
            )
            # print(f"提取到主键列 {id_column} 的值为: {row_id_value}")
            row_ids[f"{table_name}_{id_column}"] = row_id_value
    def close(self):
        """关闭数据库连接"""
        if self.db:
            self.db.close()
            print("数据库连接已关闭")

def database_manipulate(input_data: dict = None):
    """
    处理数据库操作
    
    Args:
        input_data: 外部传入的数据字典，如果为None则从默认文件加载
    
    Returns:
        dict: 包含操作状态的字典，格式为{"success": bool, "message": str}
    """
    try:
        # 根据是否有传入数据创建处理器实例
        if input_data is not None:
            maintarget = JSONToSQLmaintarget(data=input_data)
        else:
            maintarget = JSONToSQLmaintarget('databasemanipinput.json')
        
        # 加载JSON数据
        if not maintarget.load_json_data():
            return {"success": False, "message": "数据加载失败"}
        
        # 连接数据库
        if not maintarget.connect_to_database():
            return {"success": False, "message": "数据库连接失败"}
        
        # 处理数据并执行SQL操作
        success = maintarget.process_data()
        if success:
            print("\n数据处理完成！")
            # 返回操作记录的JSON字符串
            return json.dumps(maintarget.operation_records)
        else:
            print("\n数据处理失败！")
            # 即使失败也返回已有的操作记录
            return json.dumps(maintarget.operation_records)
    except Exception as e:
        print(f"处理过程中发生异常: {str(e)}")
        return {"success": False, "message": f"处理异常: {str(e)}"}
    finally:
        # 关闭数据库连接
        if 'maintarget' in locals():
            maintarget.close()

if __name__ == "__main__":
    database_manipulate()
