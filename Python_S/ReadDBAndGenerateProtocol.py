from enum import Flag
from nt import access
from operator import is_
from re import T
from sqlite3 import Row
from matplotlib import table
from pandas._libs.groupby import group_any_all
import pymysql
import csv
import json
from typing import List, Dict, Any, Optional

from pymysql.cursors import DictCursorMixin
from Python_S.sql_operations import SQLOperations
from collections import Counter


def export_table_columns_with_foreign_key() -> List[Dict[str, str]]:
    """
    导出数据库中所有表的：表名+列名+数据类型+键类型+完整外键信息
    修复：CONSTRAINT_TYPE 字段所在表错误的问题
    新增：生成表格对象，每个表作为对象，列名为属性，包含input、method和Type
    新增：处理外键关联_lib表的情况，设置为枚举类型
    新增：建立表格之间的父子关系，子表格作为父表格的子成员
    :param output_file: 输出CSV文件名
    :param target_db: 目标数据库名
    :return: 包含以_lib结尾的表数据的字典
    """
    """
    导出数据库中所有表的：表名+列名+数据类型+键类型+完整外键信息
    修复：CONSTRAINT_TYPE 字段所在表错误的问题
    新增：对于以_lib结尾的表，生成包含表中所有数据的数组
    :param output_file: 输出CSV文件名
    :param target_db: 目标数据库名
    :return: 包含以_lib结尾的表数据的字典
    """

    config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "12345678",
        "db": "darkerdatabase",
        "charset": "utf8mb4"
    }   
    # 用于存储以_lib或_enum结尾的表的数据（按需提取）
    lib_tables_data = {}

    # 用于存储表格之间的外键关联信息
    foreign_key_relations = []
    target_db = config["db"]
    children = []
    conn = None
    cursor = None
    try:
        db = SQLOperations()
        # 连接数据库
        cursor = db.conn.cursor()


        # 核心SQL：三表联合查询（修复CONSTRAINT_TYPE字段来源）
        # 1. REFERENTIAL_CONSTRAINTS：获取外键约束类型、名称、关联表信息
        # 2. KEY_COLUMN_USAGE：获取外键对应的列（子表列+主表列）
        # 3. COLUMNS：获取列的基本信息（数据类型、键类型等）
        sql = """
        SELECT
            -- 列基本信息
            c.TABLE_NAME AS `表名`,
            c.COLUMN_NAME AS `列名`,
            c.DATA_TYPE AS `数据类型`,
            c.COLUMN_KEY AS `键类型（PRI_UNI_MUL）`,
            c.IS_NULLABLE AS `是否允许为空`,
            c.EXTRA AS `额外属性（自增等）`,
            -- 外键关联信息（无外键则为NULL，后续替换为「无」）
            CASE WHEN tc.CONSTRAINT_TYPE = 'FOREIGN KEY' THEN '是' ELSE '无' END AS `是否外键`,
            tc.CONSTRAINT_NAME AS `外键名称`,
            kcu.REFERENCED_TABLE_NAME AS `关联主表名`,
            kcu.REFERENCED_COLUMN_NAME AS `关联主表列名`,
            tc.CONSTRAINT_SCHEMA AS `外键所在数据库`,
            kcu.REFERENCED_TABLE_SCHEMA AS `关联主表所在数据库`
        FROM
            information_schema.COLUMNS c
        -- 左连接：键列使用表（获取外键对应的列关联）
        LEFT JOIN information_schema.KEY_COLUMN_USAGE kcu
            ON c.TABLE_SCHEMA = kcu.TABLE_SCHEMA
            AND c.TABLE_NAME = kcu.TABLE_NAME
            AND c.COLUMN_NAME = kcu.COLUMN_NAME
            AND kcu.REFERENCED_TABLE_NAME IS NOT NULL  -- 只保留有主表关联的（外键）
        -- 左连接：约束表（获取外键约束类型和名称）
        LEFT JOIN information_schema.TABLE_CONSTRAINTS tc
            ON kcu.CONSTRAINT_SCHEMA = tc.CONSTRAINT_SCHEMA
            AND kcu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
            AND tc.CONSTRAINT_TYPE = 'FOREIGN KEY'  -- 只筛选外键约束
        WHERE
            c.TABLE_SCHEMA = %s  -- 只查目标数据库的列
        ORDER BY
            c.TABLE_NAME ASC,  -- 按表名排序
            c.ORDINAL_POSITION ASC;  -- 按列创建顺序排序
        """

        # 执行查询（传入目标数据库名）
        cursor.execute(sql, (target_db,))
        results: List[Dict[str, str]] = cursor.fetchall()
        
        # 处理结果：将所有NULL值替换为「无」，更易读
        processed_results: List[Dict[str, str]] = []
        for row in results:
            processed_row = {}
            for key, value in row.items():
                processed_row[key] = value if value is not None else "无"
            processed_results.append(processed_row)

        # 定义CSV表头（顺序清晰，包含所有字段）
        csv_headers = [
            "表名",
            "列名",
            "数据类型",
            "键类型（PRI_UNI_MUL）",
            "是否允许为空",
            "额外属性（自增等）",
            "是否外键",
            "外键名称",
            "关联主表名",
            "关联主表列名",
            "外键所在数据库",
            "关联主表所在数据库"
        ]
            # 处理所有行数据，记录外键关联信息
        for row in processed_results:
            table_name = row['表名']
            column_name = row['列名']
            is_foreign_key = row['是否外键'] == '是'
            referenced_table = row['关联主表名']
            referenced_column = row['关联主表列名']
            
            # 记录外键关联信息
            if is_foreign_key and referenced_table:
                foreign_key_relations.append({
                    'child_table': table_name,
                    'parent_table': referenced_table,
                    'foreign_key_column': column_name
                })
            
            # 检查是否是外键且关联到以_lib或_enum结尾的表
            if is_foreign_key and referenced_table:

                is_lib_reference = referenced_table.endswith('_lib')
                is_enum_reference = referenced_table.endswith('_enum')
                # 新增：处理外键关联到以 _enum_sub 结尾的表
                is_enum_sub_reference = referenced_table.endswith('_enum_sub')
                if is_enum_sub_reference:
                    # 如果还没有提取过这个 _enum_sub 表的数据，就提取它
                    if referenced_table not in lib_tables_data:
                        try:
                            # 查询表中的所有数据
                            cursor.execute(f"SELECT * FROM `{referenced_table}`")
                            rows = cursor.fetchall()
                            
                            # 检查列数是否为2
                            if len(rows) > 0 and len(rows[0]) != 2:
                                raise ValueError(f"表 {referenced_table} 列数不为2，无法处理为 key-value 对")
                            
                            # 提取为 key-value 对数组
                            key_value_pairs = []
                            # 检查该 _enum_sub 表是否有外键
                            cursor.execute("""
                                SELECT kcu.COLUMN_NAME, kcu.REFERENCED_TABLE_NAME, kcu.REFERENCED_COLUMN_NAME
                                FROM information_schema.KEY_COLUMN_USAGE kcu
                                JOIN information_schema.TABLE_CONSTRAINTS tc
                                  ON kcu.CONSTRAINT_SCHEMA = tc.CONSTRAINT_SCHEMA
                                 AND kcu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
                                WHERE kcu.TABLE_SCHEMA = %s
                                  AND kcu.TABLE_NAME = %s
                                  AND tc.CONSTRAINT_TYPE = 'FOREIGN KEY'
                                LIMIT 1
                            """, (target_db, referenced_table))
                            fk_info = cursor.fetchone()
                            if not fk_info:
                                raise ValueError(f"表 {referenced_table} 没有外键，无法生成 key-value 对")
                            # 使用当前 _enum_sub 表中作为外键的那列数据作为 key
                            key_column = fk_info['COLUMN_NAME']
                            # 获取除 key_column 外的另一列作为 value_column
                            cursor.execute(f"""
                                SELECT COLUMN_NAME
                                FROM information_schema.COLUMNS
                                WHERE TABLE_SCHEMA = %s
                                  AND TABLE_NAME = %s
                                  AND COLUMN_NAME != %s
                                LIMIT 1
                            """, (target_db, referenced_table, key_column))
                            value_column_row = cursor.fetchone()
                            if not value_column_row:
                                raise ValueError(f"表 {referenced_table} 无法确定 value 列")
                            value_column = value_column_row['COLUMN_NAME']

                            cursor.execute(f"SELECT `{key_column}`, `{value_column}` FROM `{referenced_table}`")
                            kv_rows = cursor.fetchall()
                            key_value_pairs = [
                                {"key": row[key_column], "value": row[value_column]}
                                for row in kv_rows
                            ]
                            if isinstance(row, dict):
                                keys = list(row.keys())
                                if len(keys) == 2:
                                    key_value_pairs.append({
                                        "key": row[keys[0]],
                                        "value": row[keys[1]]
                                    })
                            else:
                                if len(row) == 2:
                                    key_value_pairs.append({
                                        "key": row[0],
                                        "value": row[1]
                                    })
                            

                            # 对 key_value_pairs 进行合并：相同 key 的 value 合并为数组并去重
                            merged = {}
                            for kv in key_value_pairs:
                                k, v = kv["key"], kv["value"]
                                if k not in merged:
                                    merged[k] = []
                                if v not in merged[k]:
                                    merged[k].append(v)
                            # 重新生成 key-value 结构，value 为数组
                            key_value_pairs = {k: v for k, v in merged.items()}
                            lib_tables_data[referenced_table] = key_value_pairs
                            # print(f"  提取了枚举子表 {referenced_table} 的 key-value 数据，共 {len(key_value_pairs)} 条")
                        except Exception as e:
                            print(f"  提取枚举子表 {referenced_table} 数据时出错：{str(e)}")
                if is_lib_reference or is_enum_reference:
                    # 如果还没有提取过这个_lib或_enum表的数据，就提取它
                    if referenced_table not in lib_tables_data:
                        try:
                            # 查询表结构获取主键列名
                            cursor.execute(f"SHOW KEYS FROM `{referenced_table}` WHERE Key_name = 'PRIMARY'")
                            primary_key_info = cursor.fetchone()
                            primary_key_column = primary_key_info['Column_name'] if primary_key_info else None
                            # 查询表中的所有数据
                            cursor.execute(f"SELECT * FROM `{referenced_table}`")
                            # 提取每行的主键列value值
                            table_values = []
                            for lib_row in cursor.fetchall():
                                if isinstance(lib_row, dict):
                                    # 如果是字典
                                    if primary_key_column and primary_key_column in lib_row:
                                        # 如果有主键列，只提取主键列的值
                                        table_values.append(lib_row[primary_key_column])
                                    else:
                                        # 如果没有主键列，提取第一个值
                                        first_value = next(iter(lib_row.values()), None)
                                        if first_value is not None:
                                            table_values.append(first_value)
                                else:
                                    # 如果是元组，提取第一个值
                                    if lib_row:
                                        table_values.append(lib_row[0])
                            
                            lib_tables_data[referenced_table] = table_values
                            # print(f"  提取了枚举表{referenced_table}的数据，共{len(table_values)}条")
                        except Exception as e:
                            print(f"  提取枚举表{referenced_table}数据时出错：{str(e)}")

                if not is_lib_reference and not is_enum_reference and not is_enum_sub_reference and not column_name.endswith("ID"):
                    # 如果还没有提取过这个_lib或_enum表的数据，就提取
                    if referenced_table not in lib_tables_data:
                        try:
                            # 查询表结构获取主键列名
                            # cursor.execute(f"SHOW KEYS FROM `{referenced_table}` WHERE Key_name = 'PRIMARY'")
                            # primary_key_info = cursor.fetchone()
                            # primary_key_column = primary_key_info['Column_name'] if primary_key_info else None
                            # 查询表中的所有数据

                            cursor.execute(f"SELECT * FROM `{referenced_table}`")
                            # 提取每行的主键列value值
                            table_values = []
                            for lib_row in cursor.fetchall():
                                if isinstance(lib_row, dict):
                                    # 如果是字典
                                    if referenced_column and referenced_column in lib_row:
                                        table_values.append(lib_row[referenced_column])
                                    else:
                                        # 如果没有主键列，提取第一个值
                                        first_value = next(iter(lib_row.values()), None)
                                        if first_value is not None:
                                            table_values.append(first_value)
                                else:
                                    # 如果是元组，提取第一个值
                                    if lib_row:
                                        table_values.append(lib_row[0])
                            
                            lib_tables_data[referenced_table] = table_values
                            # print(f"  提取了枚举表{referenced_table}的数据，共{len(table_values)}条")
                        except Exception as e:
                            print(f"  提取枚举表{referenced_table}数据时出错：{str(e)}")

            # 不再需要处理tables_object，直接继续后续操作
        # output_file = "database_table_structure.csv"
        # try:
        #     with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        #         writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        #         # 写入表头
        #         writer.writeheader()
        #         # 写入数据行
        #         writer.writerows(processed_results)
        #     print(f"\n数据已成功写入CSV文件: {output_file}")
        #     print(f"共处理 {len(processed_results)} 条列信息")
        # except Exception as e:
        #     print(f"\n写入CSV文件时出错: {str(e)}")
        #     print(f"数据处理完成，但无法保存到文件，共处理 {len(processed_results)} 条列信息")
        
        # 定义CSV表头（顺序清晰，包含所有字段）
        csv_headers = [
            "表名",
            "列名",
            "数据类型",
            "键类型（PRI_UNI_MUL）",
            "是否允许为空",
            "额外属性（自增等）",
            "是否外键",
            "外键名称",
            "关联主表名",
            "关联主表列名",
            "外键所在数据库",
            "关联主表所在数据库"
        ]
    except Exception as e:
        print(f"\n导出失败：{str(e)}")
        raise
    finally:
        # 确保连接关闭
        if cursor:
            cursor.close()
        if conn and conn.open:
            conn.close()
        # print("\n数据库连接已关闭")
    
    # 输出表格关系信息

    # if foreign_key_relations:
        # print(f"\n成功建立了{len(foreign_key_relations)}个表格间的父子关系")
        # print(f"\n成功处理了 {len(processed_results)} 条数据")    

    global TargetDict
    TargetDict = db.read_data('objects')
    return processed_results,lib_tables_data

def generate_column_type(data_type,colum_attribute):
    if data_type == "int":
        if colum_attribute['is_to_fetch']:
            return "fetch"
        else:
            return "number"
    elif data_type == "float":
        return "float"
    elif data_type == "text":
        return "textarea"
    elif data_type == "tinyint":
        return "boolean"
    elif data_type == "timestamp":
        return "timestamp"
    elif data_type == "varchar":
        if colum_attribute['is_enum']:
            return "enum"
        elif colum_attribute['is_sub']:
            return "enum"
        elif colum_attribute['is_to_fetch']:
            return "fetch"
        elif colum_attribute['is_linked']:
            return "enum"   
        else:
            return "string"
    else:
        return "string"

def generate_colum_value(data_type, colum_attribute, referenced_table, type, lib_tables_data, referenced_column, extra_data, column_name):
    if type == "new":
        if data_type in ['int','float','text','timestamp']:
            if colum_attribute['is_to_fetch']:
                return referenced_column
            else:   
                return " " if type == "new" else 1  # 默认值    
        elif data_type == "tinyint":
            return False if type == "new" else False  # 默认值
        elif data_type == "varchar":
            if colum_attribute['is_enum']:
                options = lib_tables_data.get(referenced_table, [])
                return  options[0] if options else ""
            elif colum_attribute['is_sub']:
                return " "
            elif colum_attribute['is_to_fetch']:
                return referenced_column
            elif colum_attribute['is_linked']:
                options = lib_tables_data.get(referenced_table, [])
                return options[0] if options else ""
            else:
                return ""
    else:
        if colum_attribute['is_to_fetch']:
            return referenced_column
        elif extra_data[0].get(column_name):
            return extra_data[0].get(column_name)
        else:
            return " "

def generate_colum_option(data_type,colum_attribute,referenced_table,type,lib_tables_data,referenced_column):
    if data_type == "varchar":
        if colum_attribute['is_enum']:
            return lib_tables_data.get(referenced_table, [])
        elif colum_attribute['is_sub']:
            return " "
        elif colum_attribute['is_to_fetch']:
            return " "
        elif colum_attribute['is_linked']:
            return lib_tables_data.get(referenced_table, [])
    else:
        return ""

def Definedshowingstatus(colum_attribute,type,extra_data,column_name):
    if colum_attribute['is_primary_key'] or colum_attribute['is_to_fetch'] or colum_attribute['is_auto_increment'] or colum_attribute['is_generate']:
        editable = False
        visible = False
        insert = False
    else:
        editable = True
        if extra_data[1] == column_name:
            visible = False
        else:
            visible = True
        insert = True

    return {
        "editable": editable,
        "visible": visible,
        "insert": insert
    }

def generate_table_object(table_name,type,generate_type,itemlevel):
    if type == "main":
        id = f"{table_name}_basic"
        addingType = False
        itemtype = "item"
    elif type == "child":
        id = table_name
        # if generate_type == "new":
        #     addingType = True
        # else:
        addingType = True
        itemtype = "item"
    elif type == "childdata":    
        id = table_name
        addingType = False
        itemtype = "item"
    elif type == "template":
        id = table_name
        addingType = False
        itemtype = "template"

    table_object = {
        "itemlevel": itemlevel,
        "modifystate": "creation" if generate_type == "new" else "none",
        "tablename": table_name,
        "addingType": addingType,
        "itemtype": itemtype,
        "id": id,
        "children": []
    }
    return table_object

def generate_colunm_data(row,target_table,lib_tables_data,type,processed_results,extra_data,is_template):
    column_name = row['列名']
    data_type = row['数据类型']
    referenced_table = row['关联主表名']
    referenced_column = row['关联主表列名']
    father =""
    fathervalue = []
    colum_attribute = {}
    colum_attribute['is_primary_key'] = row['键类型（PRI_UNI_MUL）'] == 'PRI'
    colum_attribute['is_foreign_key'] = row['是否外键'] == '是'
    colum_attribute['is_auto_increment'] = row['额外属性（自增等）'] == 'auto_increment'
    colum_attribute['is_generate'] = row['额外属性（自增等）'] == 'STORED GENERATED' or row['额外属性（自增等）'] == 'VIRTUAL GENERATED' or data_type == "timestamp"
    colum_attribute['is_sub'] = colum_attribute['is_foreign_key'] and referenced_table and referenced_table.endswith('_enum_sub')
    colum_attribute['is_enum'] = colum_attribute['is_foreign_key'] and referenced_table and referenced_table.endswith('_enum')
    colum_attribute['is_to_fetch'] = colum_attribute['is_foreign_key'] and referenced_table == target_table and (not referenced_table.endswith('_enum')) and(not referenced_table.endswith('_enum_sub'))
    colum_attribute['is_linked'] = colum_attribute['is_foreign_key'] and referenced_table != target_table and (not referenced_table.endswith('_enum')) and(not referenced_table.endswith('_enum_sub'))
    column_type = generate_column_type(data_type,colum_attribute)  # 默认类型
    column_value = generate_colum_value(data_type,colum_attribute,referenced_table,type,lib_tables_data,referenced_column,extra_data,column_name)
    options = generate_colum_option(data_type,colum_attribute,referenced_table,type,lib_tables_data,referenced_column)
    if colum_attribute['is_sub']:
        foreign_key_columns = [
            r['列名'] for r in processed_results
            if r['表名'] == referenced_table and r['是否外键'] == '是'
        ]
        father=foreign_key_columns[0]
        fathervalue = lib_tables_data.get(referenced_table, [])
    showingstatus = Definedshowingstatus(colum_attribute,type,extra_data,column_name)
    
    # 创建列对象
    column_object = {
        "id": column_name,
        "type": column_type,
        "editable": showingstatus["editable"],
        "display": showingstatus["visible"],
        "insert": showingstatus["insert"],
        "itemlevel": "column",
        "modifystate": "none",
        "value": column_value
    }
    if is_template:
        column_object["vectorindex"] = 0
    # 如果是枚举类型，添加options

    if column_type == "enum":
        if options and not options ==" ":
            column_object["options"] = options
        else:
            column_object["options"] = []
            column_object["parentField"] = father
            column_object["parentValues"] = fathervalue
    
    return column_object


def generate_new_object_data_structure(processed_results,lib_tables_data,target_table):
    """
    生成类似object_data.json格式的数据结构
    
    Args:
        processed_results: 处理后的数据库表结构信息
        target_table: 主表名称
        lib_tables_data: 包含_lib/_enum表数据的字典
    """
    # 创建基础数据结构——
    object_data = {
        "id": target_table + "_creation",
        "itemlevel": "object",
        "children": []
    }
    extra_data = [" "," "]
    # 1. 处理主表数据
    main_table_rows = [row for row in processed_results if row['表名'] == target_table]
    
    if main_table_rows:
        # 创建主表对象
        main_table_object = generate_table_object(target_table,type="main",generate_type="new",itemlevel="row")
        # 处理主表的每一列
        for row in main_table_rows:
            column_object = generate_colunm_data(row,target_table,lib_tables_data,"new",processed_results,extra_data,is_template=False)
            main_table_object["children"].append(column_object)        
        # 将主表对象添加到children数组
        object_data["children"].append(main_table_object)
    
    # 2. 查找并处理关联到主表的子表
    child_tables = set()
    for row in processed_results:
        if row['是否外键'] == '是' and row['关联主表名'] == target_table and row['关联主表列名']=="ID":
            child_tables.add(row['表名'])
    
    # 处理每个子表
    for child_table in child_tables:
        child_table_rows = [row for row in processed_results if row['表名'] == child_table]
        # 创建子表格结构体
        child_table_object = generate_table_object(child_table,type="child",generate_type="new",itemlevel="table")
        # 创建子表格 模板行数据结构
        template_row = generate_table_object(child_table,type="template",generate_type="new",itemlevel="row")
        extra_data = [" "," "]
        # 处理子表的每一列
        for row in child_table_rows:
            column_object = generate_colunm_data(row,target_table,lib_tables_data,"new",processed_results,extra_data,is_template=True)
            # child_table_object["children"].append(column_object)
            template_row["children"].append(column_object)
        
        # 将模板行添加到子表对象
        child_table_object["children"].append(template_row)
        # 将子表对象添加到主数据结构
        object_data["children"].append(child_table_object)
    
    # 保存生成的数据结构到JSON文件
    # with open("generated_object_data.json", 'w', encoding='utf-8') as json_file:
    #     json.dump(object_data, json_file, ensure_ascii=False, indent=2)
    
    return json.dumps(object_data, ensure_ascii=False, indent=2)

def _load_id_columns_info(self):
    """从objects表加载各表的ID列名信息"""
    try:

        for item in objects_data:
            self.id_columns_map[item['OBJECT']] = item['ID']
    except Exception as e:
        print(f"加载ID列名信息失败: {str(e)}")

def fetch_db_summary():
    """
    从数据库中获取所有表的列信息
    
    Returns:
        包含所有表列信息的列表
    """
    db = SQLOperations()
    return db.read_data('objects')

def fetch_table_sumary(input_data):
    """
    获取指定表的摘要信息
    
    Args:
        input_data: 包含表名和列信息的字典
            - tablename: 目标表名
            - columns: 可选，列信息列表
    
    Returns:
        包含指定表列信息的列表
    """
    # 获取表名，只使用tablename键
    tablename = input_data.get('tablename')
    
    # 验证必要参数
    if not tablename:
        raise ValueError("表名参数缺失，请提供'tablename'")
    
    # 创建数据库连接
    db = SQLOperations()
    
    # 从columns中提取查询条件
    conditions = {}
    if 'columns' in input_data and isinstance(input_data['columns'], list):
        # 处理列名列表格式
        if all(isinstance(col, str) for col in input_data['columns']):
            # 如果是字符串列表，直接作为查询的列名
            # 调用read_data时，我们使用空条件，但指定列名
            return db.read_data(tablename, None, input_data['columns'])
        # 处理字典格式的列
        for col in input_data['columns']:
            if isinstance(col, dict) and 'name' in col and 'value' in col:
                conditions[col['name']] = col['value']
    elif 'columns' in input_data and isinstance(input_data['columns'], dict):
        # 兼容原有的字典格式
        conditions = input_data['columns']
    
    # 调用db.read_data获取表信息
    result = db.read_data(tablename, conditions)
    return result

def generate_targetted_object_data_fordisplay(processed_results,lib_tables_data,target_table: str, target_item: str, column_name: str):
    """
    生成类似object_data.json格式的数据结构，支持递归提取多层级表格数据
    
    Args:
        target_table: 目标表名
        target_item: 目标项名
        column_name: 用于匹配项的列名
    
    Returns:
        包含主表和递归子表数据的元组
    """

    db = SQLOperations()
    
    # 递归提取表格数据的内部函数
    def fetch_table_data_recursive(table_name,colunm_name,parent_id):
        attached_rows = db.read_data(table_name, {colunm_name: parent_id})
        if attached_rows == ():
            attached_rows = []
        if (table_name in child_tables_data):
            child_tables_data[table_name].extend(attached_rows)
        else:
            child_tables_data[table_name]=attached_rows
        child_tables_foreign_key_column[table_name] = colunm_name
        for row in processed_results:
            if row["是否外键"]=="是" and not row['关联主表名'].endswith("_enum") and not row['关联主表名'].endswith("_lib") and not row['关联主表名'].endswith("_enum_sub"):
                # 使用字典更新而不是直接赋值，保留多个外键列信息
                if row['表名'] not in import_tables_data:
                    import_tables_data[row['表名']] = {}
                import_tables_data[row['表名']].update({row['列名']:{
                    "关联主表名": row['关联主表名'],
                    "关联主表列名": row['关联主表列名']
                }})
            if row['是否外键'] == '是' and row['关联主表名'] == table_name and row['关联主表列名'] == "ID":
                for attached_row in attached_rows:
                    current_row_id = attached_row['ID']
                    fetch_table_data_recursive(row['表名'],row['列名'],current_row_id)


                
    # 1. 查找主表中匹配目标项的记录
    # main_row = None
    # main_row_index = None
    main_table_rows = [row for row in processed_results if row['表名'] == target_table]
    import_tables_data = {}
    if main_table_rows:
        # 处理主表的每一列
        for row in main_table_rows:
            if row['键类型（PRI_UNI_MUL）'] == 'PRI':
                main_row_key = row['列名']
            
            if row["是否外键"]=="是" and not row['关联主表名'].endswith("_enum") and not row['关联主表名'].endswith("_lib") and not row['关联主表名'].endswith("_enum_sub"):
                # 确保表名键存在，再向其中添加列名键值对
                if row['表名'] not in import_tables_data:
                    import_tables_data[row['表名']] = {}
                    
                import_tables_data[row['表名']].update({row['列名']:{
                    "关联主表名": row['关联主表名'],
                    "关联主表列名": row['关联主表列名']
                }})



    read_data = db.read_data(target_table)
    for row in read_data:
        for key, value in row.items():
            if key == column_name and value == target_item:
                main_row = row
                main_row_index = row[main_row_key]
                break
    
    if main_row is None:
        print(f"未找到 {column_name} 为 {target_item} 的行")
        return None

    child_tables_data = {}
    child_tables_foreign_key_column = {}

    for row in processed_results:
        if row['是否外键'] == '是' and row['关联主表名'] == target_table and row['关联主表列名'] == "ID":
            fetch_table_data_recursive(row['表名'],row["列名"],main_row_index)
    
    return main_row_key, main_row_index, main_row, child_tables_data, main_table_rows, lib_tables_data, processed_results, child_tables_foreign_key_column, import_tables_data


def generate_targetted_object_data(processed_results,lib_tables_data,target_table: str,target_item: str,column_name: str):
    """
    生成类似object_data.json格式的数据结构
    
    Args:
        processed_results: 处理后的数据库表结构信息
        target_table: 目标表名
        target_item: 目标项名

    """

    db = SQLOperations()
    read_data = db.read_data(target_table)
    main_row = None
    main_row_index = None
    main_table_rows = [row for row in processed_results if row['表名'] == target_table]
    
    if main_table_rows:
        # 处理主表的每一列
        for row in main_table_rows:
            if row['键类型（PRI_UNI_MUL）'] == 'PRI':
                main_row_key = row['列名']


    for row in read_data:
        for key, value in row.items():
            if key == column_name and value == target_item:
                main_row = row
                main_row_index = row[main_row_key]
                break
    if main_row is None:
        print(f"未找到 {column_name} 为 {target_item} 的行")
        return None

    # 2. 查找并处理关联到主表的子表
    child_tables = set()
    for row in processed_results:
        if row['是否外键'] == '是' and row['关联主表名'] == target_table and row['关联主表列名'].endswith("ID"):
            # 使用元组存储 (子表名, 外键列名)
            child_tables.add((row['表名'], row['列名']))


    child_tables_data = {}
    child_tables_foreign_key_column = {}
    for table_tuple in child_tables:
        # 将元组 table_tuple 解包成两个变量：子表名 和 外键列名
        child_table_name, foreign_key_column = table_tuple
        # print(f"子表名: {child_table_name}, 外键列名: {foreign_key_column}",main_row_index)
        attached_row = db.read_data(child_table_name, {foreign_key_column: main_row_index})

        child_tables_data[child_table_name] = attached_row
        child_tables_foreign_key_column[child_table_name] = foreign_key_column

    # db.delete_data(target_table, {main_row_key: main_row_index})
    return main_row_key,main_row_index,main_row,child_tables_data,main_table_rows,lib_tables_data,processed_results,child_tables_foreign_key_column


def perform_group_delete_operation(processed_results,lib_tables_data,target_table: str,target_item: str,column_name: str):
    """
    执行删除操作
    
    Args:
        target_table: 目标表名
        target_item: 目标项名
        column_name: 用于匹配项的列名
    """
    main_row_key,main_row_index,main_row,child_tables_data,main_table_rows,lib_tables_data,processed_results,child_tables_foreign_key_column = generate_targetted_object_data(processed_results,lib_tables_data,target_table,target_item,column_name)
    db = SQLOperations()
    
    # 3. 处理关联到子表的行
    for child_table_name, attached_rows in child_tables_data.items():

        for attached_row in attached_rows:
            # 构建删除条件，使用外键列名和主表的索引值
            foreign_key_column = child_tables_foreign_key_column[child_table_name]
            delete_condition = {foreign_key_column: main_row_index}
            db.delete_data(child_table_name, delete_condition)
            print(f"已删除 {child_table_name} 中关联到 {target_table} 的行: {attached_row}")

    db.delete_data(target_table, {main_row_key: main_row_index})
    print(f"已删除 {target_table} 中 {column_name} 为 {target_item} 的行")

def generate_target_object_data_structure(processed_results,lib_tables_data,target_table: str,target_item: str,column_name: str):
    """

    生成类似object_data.json格式的数据结构
    
    Args:
        processed_results: 处理后的数据库表结构信息
        target_table: 主表名称
        lib_tables_data: 包含_lib/_enum表数据的字典
    """

    main_row_key,main_row_index,main_row,child_tables_data,main_table_rows,lib_tables_data,processed_results,child_tables_foreign_key_column = generate_targetted_object_data(processed_results,lib_tables_data,target_table,target_item,column_name)
    
    name_tag = next((item['NAME'] for item in TargetDict if item['OBJECT'] == target_table), None)
    # 创建基础数据结构
    object_data = {
        "id": target_table+ "_showing",
        "itemlevel": "object",
        "children": []
    }
    
    # 1. 处理主表数据
    # main_table_rows = [row for row in processed_results if row['表名'] == target_table]
    extra_data = [main_row,name_tag]
    if main_table_rows:
        # 创建主表对象
        main_table_object = generate_table_object(target_table,type="main",generate_type="modify",itemlevel="row")
        # 处理主表的每一列
        for row in main_table_rows:
            column_object = generate_colunm_data(row,target_table,lib_tables_data,"modify",processed_results,extra_data,is_template=False)
            main_table_object["children"].append(column_object)
        
        # 将主表对象添加到children数组
        object_data["children"].append(main_table_object)

    # 2. 查找并处理关联到主表的子表
    child_tables = set()
    for row in processed_results:
        if row['是否外键'] == '是' and row['关联主表名'] == target_table and row['关联主表列名']=="ID":
            child_tables.add(row['表名'])
    
    # 处理每个子表
    for child_table in child_tables:
        child_table_rows = [row for row in processed_results if row['表名'] == child_table]

        child_table_object = generate_table_object(child_table,type="child",generate_type="modify",itemlevel="table")

        template_row = generate_table_object(child_table,type="template",generate_type="new",itemlevel="row")

        extra_data = [" "," "]
        # 处理子表的每一列
        for row in child_table_rows:
            column_object = generate_colunm_data(row,target_table,lib_tables_data,"new",processed_results,extra_data,is_template=True)
            template_row["children"].append(column_object)
        
        # 将模板行添加到子表对象
        child_table_object["children"].append(template_row)
        index = 0

        child_data = child_tables_data.get(child_table)

        if child_data:
            for item in child_data:
                index = index +1
                data_row = generate_table_object(child_table,type="childdata",generate_type="modify",itemlevel="row")

                data_row["id"] = str(child_table) + str(index)

                extra_data = [item," "]
                # 处理子表的每一列
                for row in child_table_rows:
                    column_object = generate_colunm_data(row,target_table,lib_tables_data,"modify",processed_results,extra_data,is_template=False)
                    column_object['vectorindex'] = index
                    data_row["children"].append(column_object)
                child_table_object["children"].append(data_row)

        # 将子表对象添加到主数据结构
        object_data["children"].append(child_table_object)

    return json.dumps(object_data, ensure_ascii=False, indent=2)

def extract_single_item(processed_result,lib_tables_data,target_table: str,target_item: str,column_name: str):
    result = {}
    
    _,_,main_row,child_tables_data,_,lib_tables_data,_,_, import_tables_data = generate_targetted_object_data_fordisplay(processed_result,lib_tables_data,target_table,target_item,column_name)
    db = SQLOperations()
    if target_table == "work":
        main_row["to"]=[]
        main_row["from"]=[]
        connections = db.read_data("work_from")
        current_name = main_row['Name']
        current_id = main_row['ID']
        for connection in connections:
            if connection['isFROM'] == current_name:
                main_row["to"].append(db.read_data("work",{"ID":connection['work_ID']})[0]['Name'])
            if connection['work_ID'] == current_id:
                main_row["from"].append(connection['isFROM'])
    
    if target_table in import_tables_data:
        for column in main_row:
            if column in import_tables_data[target_table]:
                replacecontent = db.read_data(import_tables_data[target_table][column]['关联主表名'],{import_tables_data[target_table][column]['关联主表列名']:main_row[column]})
                if replacecontent:
                    main_row[column] = replacecontent[0]

    if child_tables_data == {}:

        result = {main_row['Name']:main_row}
    else:
        for key,value in child_tables_data.items():
            if value == ():
                print("Impossible, but yet it's there")
            else:
                if target_table == "calculator":
                    if isinstance(value, list) and any("Type" in item for item in value):
                        grouped = {}
                        for item in value:
                            t = item.get("Type")
                            if t not in grouped:
                                grouped[t] = []
                            grouped[t].append(item)
                        main_row[key] = grouped
                    else:
                        main_row[key] = value

                # elif target_table == "work":
                elif target_table == "euf":
                    V = 0
                    R = 0
                    L = 0
                    U = 0
                    if isinstance(value, list) and any("Type" in item for item in value):
                        grouped = {} #创建group结构体
                        for item in value:
                            t = item.get("Type")
                            if t not in grouped:
                                grouped[t] = []
                            grouped[t].append(item)
                        if key == "sensors_equipement":
                            for item in grouped:
                                grouped[item] = merge_dicts_by_keys(grouped[item])
                                if item =="Camera_PH" or item =="Camera_FE":
                                    V = V + len(grouped[item])
                                elif item == "Radar":
                                    R = R + len(grouped[item])
                                elif item =="Lidar":
                                    L = L + len(grouped[item])
                                elif item == "Ultrasonic_Sensor":
                                    U = U + len(grouped[item])

                        sensor_summary = generate_param_string(V,R,L,U)
                        main_row[key] = grouped
                        main_row['sensor_set'] = sensor_summary
                    else:
                        main_row[key] = value
                else:
                    main_row[key] = value
            result = {main_row['Name']:main_row}
    return json.dumps(result, ensure_ascii=False, indent=2)

def generate_param_string(V, R, L, U):
    """
    根据四个参数生成目标字符串：非0数值拼接「数值+参数名」，0值跳过
    :param A: 参数A的数值（int/float）
    :param B: 参数B的数值（int/float）
    :param C: 参数C的数值（int/float）
    :param D: 参数D的数值（int/float）
    :return: 拼接后的字符串
    """
    # 1. 按顺序定义参数名和对应数值（保证拼接顺序：A→B→C→D）
    params = [
        ('V', V),
        ('R', R),
        ('L', L),
        ('U', U)
    ]
    
    # 2. 筛选非0数值，拼接「数值+参数名」（数值转字符串避免类型错误）
    parts = []
    for param_name, value in params:
        if value != 0:  # 仅保留非0值
            parts.append(f"{value}{param_name}")
    
    # 3. 合并所有部分为最终字符串（无分隔符）
    return ''.join(parts)

def merge_dicts_by_keys(arr, key_fields=('POSITION', 'Type', 'SubType'), priority_field='Mandatory'):
    """
    按指定关键属性合并字典列表，保留优先级字段（Mandatory）最大的字典
    :param arr: 原始字典列表
    :param key_fields: 关键属性（用于分组的字段，需完全匹配才合并）
    :param priority_field: 优先级字段（值越大越优先保留）
    :return: 合并后的字典列表
    """
    # 临时字典：key=关键属性组成的元组，value=当前组最优字典（Mandatory最大）
    merged_dict = {}
    
    for item in arr:
        # 1. 生成分组键（关键属性的值组成元组，可哈希）
        # 若字典缺少关键属性，会抛出KeyError，确保所有字典都含关键属性
        group_key = tuple(item[field] for field in key_fields)
        
        # 2. 对比当前字典与组内已有字典的优先级，保留更优的
        if group_key not in merged_dict:
            # 组内无数据，直接加入
            merged_dict[group_key] = item
        else:
            # 组内已有数据，保留Mandatory更大的；若相等，保留后出现的（覆盖前一个）
            current_priority = item[priority_field]
            existing_priority = merged_dict[group_key][priority_field]
            if current_priority > existing_priority:
                merged_dict[group_key] = item
            elif current_priority == existing_priority:
                # 优先级相等时，保留最后一个（按原始列表顺序，后出现的覆盖前一个）
                merged_dict[group_key] = item
    
    # 3. 提取合并后的字典，返回列表（顺序与原始列表中首次出现的分组顺序一致）
    return list(merged_dict.values())

def extract_item_group(processed_results,lib_tables_data,target_table: str,category):
    db = SQLOperations()
    Item_group = {}
    Item_group["type"]=target_table
    Item_group["Catalogue"]={}
    if category == "hardware":
        Item_group["Supplier"]={}
        Item_group["Type"]={}
        if target_table == "calculator":
            Item_group["Domain"]={}

    TargetLines = db.read_data(target_table)
    for line in TargetLines:
        result = extract_single_item(processed_results,lib_tables_data,target_table,line['Name'],'Name')
        result_dict = json.loads(result)
        Item_group["Catalogue"][line['Name']]=result_dict[line['Name']]
        if category == "hardware":
            if line['Supplier_Name'] not in Item_group["Supplier"]:
                Item_group["Supplier"][line['Supplier_Name']] = 0
                Item_group["Supplier"][line['Supplier_Name']] += 1
            if line['Type'] not in Item_group["Type"]:
                Item_group["Type"][line['Type']] = 0
                Item_group["Type"][line['Type']] += 1

            if target_table == "calculator":
                # 仅统计该领域出现的次数
                if line['Domain'] not in Item_group["Domain"]:
                    Item_group["Domain"][line['Domain']] = 0
                Item_group["Domain"][line['Domain']] += 1


                # 新增：遍历Item_group中每一个line下的processor数组，提取Unit为TOPS的Power并累加
                total_tops_power = 0.0
                total_cpu_power = 0.0
                processors = result_dict[line['Name']]["processor"]

                for processor in processors:
                    for item in (processors[processor]):
                        if item["Unit"] == "TOPS":
                            total_tops_power = total_tops_power + float(item["Power"])
                        if item["Unit"]=="KDMIPS":
                            total_cpu_power = total_cpu_power + float(item["Power"])
                # for processor in processors:
                #     if processors[processor] == "DMIPS":
                #         total_cpu_power += float(processor["CPU_Power"])
                
                result_dict[line['Name']]["AI_RESOURCE"] = str(total_tops_power)+" TOPS"
                result_dict[line["Name"]]["CPU_RESOURCE"] = str(total_cpu_power)+" KDMIPS"
                # Item_group["total_tops_power"] = total_tops_power
                Item_group["Catalogue"][line['Name']]=result_dict[line['Name']]
        # else:
        #     Item_group["Catalogue"][line['Name']]=result_dict[line['Name']]

    #     # 保存生成的数据结构到JSON文件
    # with open("generated_object_data.json", 'w', encoding='utf-8') as json_file:
    #     json.dump(Item_group, json_file, ensure_ascii=False, indent=2)
    
    # print(f"\n已生成类似object_data.json格式的数据结构，保存到 generated_object_data.json")

    return json.dumps(Item_group,ensure_ascii=False, indent=2)

def extract_entire_network(processed_results,lib_tables_data,target_table: str):
    db = SQLOperations()
    Item_group = {}
    Item_group["type"]="Ele"
    Item_group["Element"]=[]
    TargetLines = db.read_data(target_table)
    for line in TargetLines:
        result = extract_single_item(processed_results,lib_tables_data,target_table,line['Name'],'Name')
        result_dict = json.loads(result)
        Item_group["Element"].append(result_dict[line['Name']])

    Item_group["connections"] = []
    connect_source = db.read_data("work_from")  
    for line in connect_source:
        fromitem = db.read_data("work",{"Name":line["isFROM"]})[0]["ID"]
        toitem = line["work_ID"]
        Item_group["connections"].append({
            "from": fromitem,
            "to": toitem,
        })
    return json.dumps(Item_group,ensure_ascii=False, indent=2)

def add_users(data):
    db = SQLOperations()
            
    userdata = {"Name": data['name'], "email": data["submitter_email"], "isSubscribe": True}
    
    # 尝试插入数据
    result = db.insert_data("user", userdata)
    if isinstance(result, int) and result > 0:
        return {"status": True, "insert_id": result}
    else:
        if "email" in result:
            exist_name = db.read_data("user",{"email":userdata["email"]})[0]["Name"]
            if exist_name == userdata['name']:
                return {"status": False, "error": 1}
            else:
                return {"status": False, "error": 2,"name":exist_name}
        elif "Name" in result:
            exist_email = db.read_data("user",{"Name":userdata["Name"]})[0]["email"]
            if exist_email == userdata['email']:
                return {"status": False, "error": 1}
            else:
                return {"status": False, "error": 3,"name":data['name']}    

def submit_issue(data):
    db = SQLOperations()
        
    issuedata = {
        "Type":data["type"],
        "Category":data["title"],
        "Description":data["description"],
        "UserName":data["submit_name"],
        "Email":data["submit_email"],
        "Status":"待处理",
    }
    
    # 尝试插入数据
    result = db.insert_data("issuesandadvice", issuedata)
    userlist = db.read_data("user",{"email":issuedata["Email"]})
    if not userlist: # 该邮箱没有订阅
        usernames = db.read_data('user',{"Name":issuedata["UserName"]})
        if not usernames:
            db.insert_data("user", {"Name": issuedata["UserName"], "email": issuedata["Email"], "isSubscribe": True})
        else:
            newname = usernames[0]["Name"]+"_1"
            db.insert_data("user", {"Name": newname, "email": issuedata["Email"], "isSubscribe": True})

    if isinstance(result, int) and result > 0:
        return {"status": True, "insert_id": result}
    else:
        return {"status": False, "insert_id": "shit nigger"}

def manage_login(data):
    db = SQLOperations()
    result = db.read_data("manager_account",{"Name":data["name"]})

    if not result:
        print("User Name doesn't exist")
        return {"status": False, "error": 1}
    else:
        if result[0]["Password"] == data["password"]:
            print("Bonjour monsieur manager",result[0])
            return {"status": True, "error": 0,"access":{"allright":result[0]["isAllRight"],"modification":result[0]["isModification"],"adding":result[0]["isAdding"]}}
        else:
            print("Get lost you fake imposter")
            return {"status": False, "error": 2}

def convert_datetime_to_str(obj):
    """将datetime对象转换为字符串格式"""
    if isinstance(obj, dict):
        return {key: convert_datetime_to_str(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime_to_str(item) for item in obj]
    elif hasattr(obj, 'isoformat'):
        # 处理datetime对象
        return obj.isoformat()
    else:
        return obj

def fetch_advice_recording():
    db = SQLOperations()
    try:
        Result = {}
        result = db.read_data("issuesandadvice")
        Result["advice"] = []
        Result["issue"] = []
        Result["statistic"]={}

        for line in result:
            # 转换每一行数据中的datetime对象
            converted_line = convert_datetime_to_str(line)
            if converted_line["Type"] == "suggestion":
                Result["advice"].append(converted_line)
            else:
                Result["issue"].append(converted_line)

        Result["statistic"]={
            "Total_advice":len(Result["advice"]),
            "Total_issue":len(Result["issue"]),
            "Total_issue_and_advice":len(result),
            "Unsolved_issue":len([item for item in Result["issue"] if item["Status"] == "待处理"]),
            "Solved_issue":len([item for item in Result["issue"] if item["Status"] == "已处理"]),
            "Unsolved_advice":len([item for item in Result["advice"] if item["Status"] == "待处理"]),
            "Solved_advice":len([item for item in Result["advice"] if item["Status"] == "已处理"]),
        }

        # 再次转换整个Result对象，确保所有datetime都被处理
        Result = convert_datetime_to_str(Result)
        return json.dumps(Result, ensure_ascii=False, indent=2)
    except Exception as e:
        # 捕获并返回错误信息
        error_result = {"success": False, "error": str(e)}
        return json.dumps(error_result, ensure_ascii=False, indent=2)
    finally:
        # 确保数据库连接关闭
        try:
            db.close()
        except:
            pass

def update_recordings(data,id):
    db = SQLOperations()
    row=db.update_data("issuesandadvice", data,{"ID": id})
    Result = fetch_advice_recording()
    Feedback = {"status": True, "error": 0,"Result":json.loads(Result)}

    return json.dumps(Feedback, ensure_ascii=False, indent=2)

def delete_recordings(id):
    db = SQLOperations()
    row=db.delete_data("issuesandadvice", {"ID": id})
    Result = fetch_advice_recording()
    Feedback = {"status": True, "error": 0,"Result":json.loads(Result)}

    return json.dumps(Feedback, ensure_ascii=False, indent=2)

def get_user_info():
    db = SQLOperations()
    Result = {}
    users = db.read_data("user")
    Result["user"] = users
    Result["user_count"] = len(users)
    Result = convert_datetime_to_str(Result)
    Feedback = {"status": True, "error": 0,"Result":Result}
    
    return json.dumps(Feedback, ensure_ascii=False, indent=2)

def visit_management(data):
    db = SQLOperations()

    Result = db.insert_data("visit",data)
    Feedback = {"status": True, "error": 0,"Result":Result}
    return json.dumps(Feedback, ensure_ascii=False, indent=2)


def visit_statistic():
    db = SQLOperations()
    Result = {}
    visit_data = db.read_data("visit")
    Result["visit"] = visit_data
    # 计算独立用户数（注意：这里假设'user_ad'是正确的字段名）
    Result["unique_user_count"] = len(set(visit.get("user_ad", "") for visit in visit_data if visit.get("user_ad")))
    Result["visit_count"] = len(visit_data)

    # 统计 page_url 出现次数 - 正确迭代visit_data列表
    page_counter = Counter(row['page_url'] for row in visit_data if 'page_url' in row and row['page_url'])
    page_count = [{'key': url, 'value': cnt} for url, cnt in page_counter.items()]

    # 转换datetime对象
    Result = convert_datetime_to_str(Result)
    Feedback = {"status": True, "error": 0, "Result": Result, "page_count": page_count}

    return json.dumps(Feedback, ensure_ascii=False, indent=2)
if __name__ == "__main__":
    # 运行导出（默认输出为 database_table_structure.csv）
    # 注意：现在该函数只返回处理后的CSV数据
    print("\n处理完成！")