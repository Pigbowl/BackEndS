# from ast import main
# from enum import Flag
# from nt import access
# from operator import is_
# from pipes import quote
# from re import T
# from sqlite3 import Row
# from xml.etree.ElementTree import tostring
# from matplotlib import table
# from numpy import concat
# from numpy.polynomial.legendre import legline
# from pandas._libs.groupby import group_any_all
# import pymysql
# import csv
import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional
from Python_S.emailing import send_single_email
from Python_S.sql_operations import SQLOperations
# 用于SSH远程操作
import paramiko
# from pymysql.cursors import DictCursorMixin

from collections import Counter
# 从adminconfig.json加载remotecode
with open('adminconfig.json', 'r', encoding='utf-8') as f:
    code_data = json.load(f)
    admin_email = code_data['admin_email']
    server_code = code_data['server_code']
    server_pseudo = code_data['server_pseudo']
    server_ip = code_data['server_ip']
    server_sshport = code_data['server_sshport']

def export_table_columns_with_foreign_key(db) -> List[Dict[str, str]]:
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
        # db = SQLOperations()
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
                        except Exception as e:
                            print(f"  提取枚举表{referenced_table}数据时出错：{str(e)}")


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
        elif extra_data[0].get(column_name)==0:
            return 0
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
        db: 数据库连接对象
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

def generate_new_object_data_structure_layer(processed_results,lib_tables_data,target_table):
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
    extra_data = [" ", " "]
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
        extra_data = [" ", " "]
        # 处理子表的每一列
        for row in child_table_rows:
            column_object = generate_colunm_data(row,target_table,lib_tables_data,"new",processed_results,extra_data,is_template=True)
            template_row["children"].append(column_object)
        
        # 将模板行添加到子表对象
        child_table_object["children"].append(template_row)
        
        # 3. 查找并处理关联到当前子表的孙表
        grandchild_tables = set()
        for row in processed_results:
            if row['是否外键'] == '是' and row['关联主表名'] == child_table and row['关联主表列名']=="ID":
                grandchild_tables.add(row['表名'])
        
        # 处理每个孙表
        for grandchild_table in grandchild_tables:
            grandchild_table_rows = [row for row in processed_results if row['表名'] == grandchild_table]
            # 创建孙表格结构体
            grandchild_table_object = generate_table_object(grandchild_table,type="child",generate_type="new",itemlevel="table")
            # 创建孙表格 模板行数据结构
            grandchild_template_row = generate_table_object(grandchild_table,type="template",generate_type="new",itemlevel="row")
            extra_data = [" ", " "]
            # 处理孙表的每一列
            for row in grandchild_table_rows:
                column_object = generate_colunm_data(row,target_table,lib_tables_data,"new",processed_results,extra_data,is_template=True)
                grandchild_template_row["children"].append(column_object)
            
            # 将孙表模板行添加到孙表对象
            grandchild_table_object["children"].append(grandchild_template_row)
            # 将孙表对象添加到子表对象的children中
            child_table_object["children"].append(grandchild_table_object)
        
        # 将子表对象添加到主数据结构
        object_data["children"].append(child_table_object)
    
    # # 保存生成的数据结构到JSON文件
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

def fetch_db_summary(db):
    """
    从数据库中获取所有表的列信息
    
    Returns:
        包含所有表列信息的列表
    """
    result = {}
    result['顶层对象'] = db.read_data('objects')
    result['独立非顶层对象']= db.read_data('subobjects')
    result['辅助数据']= db.read_data('supportobjects')
    return result

def fetch_table_sumary(db,input_data):
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
    # db = SQLOperations()
    
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

def generate_targetted_object_data_fordisplay(db,processed_results,lib_tables_data,target_table: str, target_item: str, column_name: str):
    """
    生成类似object_data.json格式的数据结构，支持递归提取多层级表格数据
    
    Args:
        target_table: 目标表名
        target_item: 目标项名
        column_name: 用于匹配项的列名
    
    Returns:
        包含主表和递归子表数据的元组
    """
    # db = SQLOperations()

    # 递归提取表格数据的内部函数
    def fetch_table_data_recursive(table_name,colunm_name,parent_id,child_tables_data):
        child_tables_data[table_name] = []                                                  #为该表格创建子表格对象,类型为空数组
        attached_rows = db.read_data(table_name, {colunm_name: parent_id})                  #获取子表格中，从属于父表格的所有信息
        table_rows = [row for row in processed_results if row['表名'] == table_name]        #获取当前表格所有所有列的信息
        index = 0                                                                           #创建index
        for row in attached_rows:                                                           #在返回的数组中提取字典成员
            child_tables_data[table_name].append(row)                                       #为子表格添加当前成员
            current_row = row                                                               #fetch the row information as current row, as row is used as indexing name everywhere
            for row in table_rows: #在当前表格的所有列中查找是否有外键引用  
                if row["是否外键"]=="是" and not row['关联主表名'].endswith("_enum") and not row['关联主表名'].endswith("_lib") and not row['关联主表名'].endswith("_enum_sub") and not row['关联主表列名']=="ID":  #判断当前表格的引用表格，如果是引用表格
                    if not current_row[row['列名']] =="":
                        replacement = db.read_data(row['关联主表名'],{row['关联主表列名']:current_row[row['列名']]})[0]
                        child_tables_data[table_name][index][row['列名']]=replacement
                    quote_key = row['列名']
                    quote_table_name = row['关联主表名']
                    quote_table_rows = [row for row in processed_results if row['表名'] == quote_table_name]

                    for subrow_2 in quote_table_rows:
                        if subrow_2["是否外键"]=="是" and not subrow_2['关联主表名'].endswith("_enum") and not subrow_2['关联主表名'].endswith("_lib") and not subrow_2['关联主表名'].endswith("_enum_sub") and not subrow_2['关联主表列名']=="ID":  #判断当前表格的引用表格，如果是引用表格
                            subreplacement = db.read_data(subrow_2['关联主表名'],{"Name":child_tables_data[table_name][index][row['列名']][subrow_2['列名']]})[0]
                            child_tables_data[table_name][index][row['列名']][subrow_2['列名']]=subreplacement

                    for subrow in processed_results: #寻找应用的表格中的关联件信息
                        if subrow['是否外键'] == '是' and subrow['关联主表名'] == quote_table_name and subrow['关联主表列名'] == "ID":
                            sub_child_tables_data = child_tables_data[table_name][index]
                            new_parent_id = db.read_data(quote_table_name,{"Name":current_row[quote_key]['Name']})[0]["ID"]
                            fetch_table_data_recursive(subrow['表名'],subrow['列名'],new_parent_id,sub_child_tables_data)


            for row in processed_results:
                if row['是否外键'] == '是' and row['关联主表名'] == table_name and row['关联主表列名'] == "ID":
                    current_row_id = current_row['ID']
                    fetch_table_data_recursive(row['表名'],row['列名'],current_row_id,child_tables_data[table_name][index])
            index += 1

    main_table_rows = [row for row in processed_results if row['表名'] == target_table]
    import_tables_data = {}
    # print(target_table,db.read_data(target_table,{column_name:target_item}))
    main_row = db.read_data(target_table,{column_name:target_item})[0]

    if main_row is None:
        print(f"未找到 {column_name} 为 {target_item} 的行")
        return None
    main_row_key = "ID"
    main_row_index = main_row[main_row_key]

    child_tables_data = {}
    child_tables_foreign_key_column = {}

    if main_table_rows:
        # 处理主表的每一列
        for row in main_table_rows:            
            if row["是否外键"]=="是" and not row['关联主表名'].endswith("_enum") and not row['关联主表名'].endswith("_lib") and not row['关联主表名'].endswith("_enum_sub") and not row['关联主表列名']=="ID":  #判断当前表格的引用表格，如果是引用表格
                if main_row[row['列名']] is not None and not main_row[row['列名']]=="":
                    replacement = db.read_data(row['关联主表名'],{'Name':main_row[row['列名']]})[0]
                    main_row[row['列名']] = replacement
                quote_key = row['列名']
                quote_table_name = row['关联主表名']
                quote_table_rows = [row for row in processed_results if row['表名'] == quote_table_name]
                for subrow_2 in quote_table_rows:
                    if subrow_2["是否外键"]=="是" and not subrow_2['关联主表名'].endswith("_enum") and not subrow_2['关联主表名'].endswith("_lib") and not subrow_2['关联主表名'].endswith("_enum_sub") and not subrow_2['关联主表列名']=="ID":  #判断当前表格的引用表格，如果是引用表格
                        subreplacement = db.read_data(subrow_2['关联主表名'],{"Name":main_row[row['列名']][subrow_2['列名']]})[0]
                        main_row[row['列名']][subrow_2['列名']]=subreplacement

                for subrow in processed_results: #寻找应用的表格中的关联件信息
                    if subrow['是否外键'] == '是' and subrow['关联主表名'] == quote_table_name and subrow['关联主表列名'] == "ID":
                        newparentid= main_row[quote_key][subrow['关联主表列名']]
                        fetch_table_data_recursive(subrow['表名'],subrow['列名'],newparentid,main_row[row['列名']])


    for row in processed_results:  
        if row['是否外键'] == '是' and row['关联主表名'] == target_table and row['关联主表列名'] == "ID":    #row['表名']表格为被查询表格的子表格，进行递归处理
            fetch_table_data_recursive(row['表名'],row["列名"],main_row_index,child_tables_data)


    # with open("generated_object_data.json", 'w', encoding='utf-8') as json_file:
    #     json.dump(child_tables_data, json_file, ensure_ascii=False, indent=2)
    
    # print(f"\n已生成类似object_data.json格式的数据结构，保存到 generated_object_data.json")
    return main_row,child_tables_data,lib_tables_data


def generate_targetted_object_data(db,processed_results,lib_tables_data,target_table: str,target_item: str,column_name: str):
    """
    生成类似object_data.json格式的数据结构
    
    Args:
        processed_results: 处理后的数据库表结构信息
        target_table: 目标表名
        target_item: 目标项名

    """

    # db = SQLOperations()
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
        attached_row = db.read_data(child_table_name, {foreign_key_column: main_row_index})

        child_tables_data[child_table_name] = attached_row
        child_tables_foreign_key_column[child_table_name] = foreign_key_column

    # db.delete_data(target_table, {main_row_key: main_row_index})
    return main_row_key,main_row_index,main_row,child_tables_data,main_table_rows,lib_tables_data,processed_results,child_tables_foreign_key_column


def perform_group_delete_operation(db,processed_results,lib_tables_data,target_table: str,target_item: str,column_name: str):
    """
    执行删除操作
    
    Args:
        target_table: 目标表名
        target_item: 目标项名
        column_name: 用于匹配项的列名
    """
    main_row_key,main_row_index,main_row,child_tables_data,main_table_rows,lib_tables_data,processed_results,child_tables_foreign_key_column = generate_targetted_object_data(db,processed_results,lib_tables_data,target_table,target_item,column_name)
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

def generate_target_object_data_structure(db,processed_results,lib_tables_data,target_table: str,target_item: str,column_name: str):
    """

    生成类似object_data.json格式的数据结构
    
    Args:
        processed_results: 处理后的数据库表结构信息
        target_table: 主表名称
        lib_tables_data: 包含_lib/_enum表数据的字典
    """

    main_row_key,main_row_index,main_row,child_tables_data,main_table_rows,lib_tables_data,processed_results,child_tables_foreign_key_column = generate_targetted_object_data(db,processed_results,lib_tables_data,target_table,target_item,column_name)
    
    name_tag = next((item['NAME'] for item in TargetDict if item['OBJECT'] == target_table), None)
    # 创建基础数据结构
    object_data = {
        "id": target_table + "_" +main_row['Name'] + "_showing",
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

def fetch_regulation_list(db,processed_results,lib_tables_data,target_table: str,target_item: list,column_name: str):
        # db = SQLOperations()
    regulation_dict = {}
    regulation_list = []
    region_list = []
    for country in target_item:
        table_data = extract_single_item(db,processed_results,lib_tables_data,target_table,country,column_name)
        new_regions = json.loads(table_data)[country]["region_group"]
        for region in new_regions:
            if region not in regulation_dict:
                regulation_dict[region] = {}
                regulation_dict[region]["country"] = []
                regulation_dict[region]["regulation"] = []

            regulation_dict[region]["country"].append(country)
            regulation_dict[region]["regulation"]=(db.read_data("regulation",{"Region_Name":region}))

    with open("generated_object_data.json", 'w', encoding='utf-8') as json_file:
        json.dump(regulation_dict, json_file, ensure_ascii=False, indent=2)
    print(f"\n已生成类似object_data.json格式的数据结构，保存到 generated_object_data.json")

    return json.dumps(regulation_dict, ensure_ascii=False, indent=2)

def extract_single_item(db,processed_result,lib_tables_data,target_table: str,target_item: str,column_name: str):
    result = {}
    searchkeyname = ""
    main_row,child_tables_data,lib_tables_data = generate_targetted_object_data_fordisplay(db,processed_result,lib_tables_data,target_table,target_item,column_name)

    searchkeyname = main_row['Name']
    if child_tables_data == {}:
        result = {searchkeyname:main_row}
    else:
        for key,value in child_tables_data.items():
            if value == ():
                print("Impossible, but yet it's there")
            else:
                main_row[key] = value

            result = {searchkeyname:main_row}

            
    def recursivelooking(data,checkkey,container):
        if not isinstance(data, dict):
            return
        for row,value in data.items():
            if row ==checkkey:
                if isinstance(value, list):
                    container.extend(value)
                elif isinstance(value, dict):
                    container.append(value)
            else:
                if isinstance(value, list):
                    for element in value:
                        recursivelooking(element,checkkey,container)
                elif isinstance(value, dict):
                    recursivelooking(value,checkkey,container)
    def dataregroup(target_group):
        if not target_group == []:
            group = {}
            for target in target_group:
                for key,value in target.items():    
                    if key == "Type":
                        if value not in group:
                            group[value] = []
                        group[value].append(target)
            return group
        else:
            return None

    def dealwithsolution(main_row):

        db = SQLOperations()
        main_row["briefing"]={}
        sensor_set =""
        browsing_list = ["camera_input","radar_input","lidar_input","ultrasonic_input"]
        sensor_short_cut =['V','R','L','U']
        for sensor_type in browsing_list:
            sensor_kit = []
            recursivelooking(main_row,sensor_type,sensor_kit)
            sensor_set = sensor_set + str(len(sensor_kit))+sensor_short_cut[browsing_list.index(sensor_type)] if len(sensor_kit) != 0 else sensor_set
        main_row["briefing"]["sensor_set"] = sensor_set

        calculator_kit = []
        calculator_group = []
        calculator_number = []
        recursivelooking(main_row,"calculator_Name",calculator_kit)
        for item in calculator_kit:
            if item["Name"] not in calculator_group:
                calculator_group.append(item["Name"])
                calculator_number.append(1)
            elif item["Name"] in calculator_group:
                calculator_number[calculator_group.index(item["Name"])] = calculator_number[calculator_group.index(item["Name"])] + 1
                
        main_row["briefing"]["calculator_group"] = calculator_group
        # 构造 calculator_sum 数组：每个元素为 calculator_group[index] + "*" + str(calculator_number[index])
        main_row["briefing"]["calculator_sum"] = [
            f"{group}*{num}" for group, num in zip(calculator_group, calculator_number)
        ]

        
        ecu_kit=[]
        ecu_group = []
        recursivelooking(main_row,"ECU_Name",ecu_kit)
        for item in ecu_kit:
            if item["Name"] not in ecu_group:
                ecu_group.append(item["Name"])
        main_row["briefing"]["ecu_group"] = ecu_group

        tag_kit=[]
        tag_group = []
        recursivelooking(main_row,"tags_Tag",tag_kit)
        for item in tag_kit:
            if item["Tag"] not in tag_group:
                tag_group.append(item["Tag"])
        main_row["briefing"]["tags"] = tag_group
        
        algo_kit=[]
        algorithm_group = []
        recursivelooking(main_row,"Algo_Name",algo_kit)
        for item in algo_kit:
            if item["Name"] not in algorithm_group:
                algorithm_group.append(item["Name"])
        main_row["briefing"]["algorithm_group"] = algorithm_group

        interface_kit=[]
        interface_group = []
        recursivelooking(main_row,"solution_interface",interface_kit)
        for item in interface_kit:
            if item["SubType"] not in interface_group:
                interface_group.append(item["SubType"])
        main_row["briefing"]["interface_group"] = interface_group

        total_tops_power = 0.0
        total_cpu_power = 0.0
        total_gpu_power= 0.0

        processor_kit = []
        recursivelooking(main_row,"processor",processor_kit)
        for processor in processor_kit:
            if processor["Unit"] == "TOPS":
                total_tops_power = total_tops_power + float(processor["Power"])
            if processor["Unit"]=="KDMIPS":
                total_cpu_power = total_cpu_power + float(processor["Power"])
            if processor["Unit"] == "GFLOPS":
                total_gpu_power = total_gpu_power + float(processor["Power"])
        
        main_row["briefing"]["AI_RESOURCE"] = str(total_tops_power)+" TOPS"
        main_row["briefing"]["CPU_RESOURCE"] = str(total_cpu_power)+" KDMIPS"
        main_row["briefing"]["GPU_RESOURCE"] = str(total_gpu_power)+" GFLOPS"
        
        # euf_list = db.read_data("euf")
        level = "L0"
        level_array = []
        level_vector = ["L0","L1","L2","L2+","L2++","L3","L4","L5"]
        for item in main_row["solution_euf_group"][0]:
            if (not item == "id" and not item.endswith("ID")) and main_row["solution_euf_group"][0][item] == 1:
                level = db.read_data("euf",{"Name":item})[0]["SAE"]
                level_array.append(level_vector.index(level))

        main_row["briefing"]["SAE"] = level_vector[max(level_array)]



    if target_table =="work":
        db = SQLOperations()
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
    elif target_table == "euf":
        """
        for end user function, we need to extract and summerizing sensor set: 1. extract all the sensors to a new array, name as sensor_group,sort and merge according to the shit
        """
        sensor_group = []
        recursivelooking(child_tables_data,"sensors_equipement",sensor_group)
        sensor_count = {"V":0,"R": 0,"L": 0,"U": 0}
        sensor_summary = None
        group = dataregroup(sensor_group)
        if group != None:
            for key,value in group.items():
                group[key] = merge_dicts_by_keys(value)
                if key =="Camera_PH" or key =="Camera_FE":
                    sensor_count["V"] = sensor_count["V"] + len(group[key])
                elif key == "Radar":
                    sensor_count["R"] = sensor_count["R"] + len(group[key])
                elif key =="Lidar":
                    sensor_count["L"] = sensor_count["L"] + len(group[key])
                elif key == "Ultrasonic_Sensor":
                    sensor_count["U"] = sensor_count["U"] + len(group[key]) 
        
        sensor_summary = generate_param_string(sensor_count["V"],sensor_count["R"],sensor_count["L"],sensor_count["U"]) 
        main_row["sensor_summary"] = sensor_summary
        main_row["sensors_equipement"] = group

    elif target_table == "calculator":
        interface_group=[]
        recursivelooking(child_tables_data,"interface",interface_group)
        grouped_interface = dataregroup(interface_group)
        main_row["interface_group"] = grouped_interface

        processor_group = []
        recursivelooking(child_tables_data,"processor",processor_group)
        grouped_processor = dataregroup(processor_group)
        main_row["processor_group"] = grouped_processor
    elif target_table == "country":
        region_group=[]
        recursivelooking(child_tables_data,"Region_Name",region_group)
        region_list = []
        for item in region_group:
            if item["Name"] not in region_list:
                region_list.append(item["Name"])
        # grouped_region = dataregroup(region_group)
        main_row["region_group"] = region_list

    elif target_table == "vehiclemodel":
        dealwithsolution(result[searchkeyname]["Adas_Solution"])

        # brand_kit = []
        # recursivelooking(main_row,"brand",brand_kit)
        # main_row["briefing"]["brand_group"] = brand_kit




    elif target_table == "system_solution":
        """
        summerize sensor set
        """
        dealwithsolution(result[searchkeyname])

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

def initiate_configurator(db,processed_results,lib_tables_data):
    Result = {}
    # Item_group = 
    Result["calculator"]=json.loads(extract_item_group(db,processed_results,lib_tables_data,"calculator","hardware"))
    Result["euf"]=json.loads(extract_item_group(db,processed_results,lib_tables_data,"euf","function"))
    Result["sensors"] = {}
    Result["sensors"]["camera"]=json.loads(extract_item_group(db,processed_results,lib_tables_data,"camera","hardware"))
    Result["sensors"]["radar"]=json.loads(extract_item_group(db,processed_results,lib_tables_data,"radar","hardware"))
    Result["sensors"]["lidar"]=json.loads(extract_item_group(db,processed_results,lib_tables_data,"lidar","hardware"))
    Result["sensors"]["uss"]=json.loads(extract_item_group(db,processed_results,lib_tables_data,"uss","hardware"))

    return json.dumps(Result, ensure_ascii=False, indent=2)

def config_searching(db,processed_results,lib_tables_data,search_condition):
    function_check = False
    calculator_check = False
    calculator_supplier_check = False
    sensor_type_check = False
    sensor_subtype_check = False
    comply_solution = []
    ## determiner the effecitve function verification condition
    func_checklist = []
    function_condition = search_condition["function"]
    if function_condition == {}:
        print("No function condition")
    else:
        function_check = True
        for euf in function_condition:
            func_checklist.append(euf)

    cal_supplier_checklist = []
    cal_checklist = []
    calculator_condition = search_condition["calculators"]
    if calculator_condition == {}:
        print("No calculator condition")
    else:
        for calculator in calculator_condition:
            if calculator_condition[calculator] == ["all"]:
                cal_supplier_checklist.append(calculator)
                calculator_supplier_check = True
            else:
                cal_checklist.extend(calculator_condition[calculator])
                calculator_check = True


    sensor_condition = search_condition["sensors"]

    sensor_type_checklist = []
    sensor_subtype_checklist = []
    if sensor_condition == {}:
        print("No sensor condition")
    else:
        for sensor in sensor_condition:
            if sensor_condition[sensor] == ["all"]:
                sensor_type_checklist.append(sensor)
                sensor_type_check = True
            else:
                sensor_subtype_checklist.extend(sensor_condition[sensor])
                sensor_subtype_check = True

    print("function_check:",function_check)
    print("calculator_check:",calculator_check)
    print("calculator_supplier_check:",calculator_supplier_check)
    print("sensor_type_check:",sensor_type_check)
    print("sensor_subtype_check:",sensor_subtype_check)

    solution_list = extract_item_group(db,processed_results,lib_tables_data,"system_solution","solution")
    solution_list = json.loads(solution_list)["Catalogue"]
    sensordict = {"camera_input":["Camera_Name","camera"],"radar_input":["Radar_Name","radar"],"lidar_input":["Lidar_Name","lidar"],"Uss_input":["Uss_Name","uss"]}
    # with open("generated_object_data.json", 'w', encoding='utf-8') as json_file:
    #     json.dump(solution_list, json_file, ensure_ascii=False, indent=2)
    # print(f"\n已生成类似object_data.json格式的数据结构，保存到 generated_object_data.json")

    for solution in solution_list:
        solution_calculator_supplier_list = []
        solution_calculator_list = []
        solution_euf_list = []
        solution_sensor_type_list = []
        solution_sensor_subtype_list = []
        # print(solution_list[solution]["ecu_input"])
        for ecu in solution_list[solution]["ecu_input"]:
            for calculator in (ecu["calculator_ecu_input"]):  #获取当前solution calculator的所有信息
                solution_calculator_supplier_list.append(calculator["calculator_Name"]['Supplier_Name']['Name'])
                solution_calculator_list.append(calculator["calculator_Name"]["Name"])
        for euf in (solution_list[solution]["solution_euf_group"][0]):
            if solution_list[solution]["solution_euf_group"][0][euf] == 1 and not euf == "id" :
                solution_euf_list.append(euf)
        for sensortype in solution_list[solution]:
            if sensortype in sensordict and not solution_list[solution][sensortype] == []:
                solution_sensor_type_list.append(sensordict[sensortype][1])
                for sensor in solution_list[solution][sensortype]:
                    if sensor[sensordict[sensortype][0]]['Type'] not in solution_sensor_subtype_list:
                        solution_sensor_subtype_list.append(sensor[sensordict[sensortype][0]]['Type'])


        if function_check:
            function_confirm = all(item in solution_euf_list for item in func_checklist)
        else:
            function_confirm = True

        if calculator_check:
            calculator_confirm = all(item in solution_calculator_list for item in cal_checklist)
        else:
            calculator_confirm = True

        if calculator_supplier_check:
            calculator_supplier_confirm = all(item in solution_calculator_supplier_list for item in cal_supplier_checklist)
        else:
            calculator_supplier_confirm = True

        if sensor_type_check:
            sensor_type_confirm = all(item in solution_sensor_subtype_list for item in sensor_type_checklist)
        else:
            sensor_type_confirm = True

        if sensor_subtype_check:
            sensor_subtype_confirm = all(item in solution_sensor_subtype_list for item in sensor_subtype_checklist)
        else:
            sensor_subtype_confirm = True

        # 统一检查
        solution_confirm = all([
            function_confirm,
            calculator_confirm,
            calculator_supplier_confirm,
            sensor_type_confirm,
            sensor_subtype_confirm
        ])

        # 收集未通过的项
        failed_checks = []
        if not function_confirm:
            failed_checks.append("function_confirm")
        if not calculator_confirm:
            failed_checks.append("calculator_confirm")
        if not calculator_supplier_confirm:
            failed_checks.append("calculator_supplier_confirm")
        if not sensor_type_confirm:
            failed_checks.append("sensor_type_confirm")
        if not sensor_subtype_confirm:
            failed_checks.append("sensor_subtype_confirm")

        if solution_confirm:
            comply_solution.append(solution_list[solution])
        
    return json.dumps(comply_solution,ensure_ascii=False, indent=2)

def extract_single_feature(db,input_feature_name):
    """提取单个FEATURE的信息，为每个TF添加顺序编号"""
    try:
        # db = SQLOperations()

        
        # 读取SUBFEATURES工作表，筛选目标FEATURE
        df_subfeatures = db.read_data('function_features',{"Name":input_feature_name})
        if len(df_subfeatures) == 0:
            raise ValueError(f"未找到FEATURE: {input_feature_name}")
                
        # 初始化FEATURE数据结构
        feature_data = {
            'FUNCTION_NAME': input_feature_name,
            'FUNCTION_INDEX':"Feature 1.1",
            'mf_functions': []  # 数组存储MF
        }
        
        feature_id = df_subfeatures[0]["ID"]

        # 提取该FEATURE关联的MF（有序数组）

        mf_list = db.read_data('feautre_mf_input',{"function_features_ID":feature_id})

        # mf_names = []

        # 初始化MF数组
        for mf_name in mf_list:
            tf_functions = []
            main_data = db.read_data('mainfunctions',{"Name":mf_name['mainfunctions_Name']})[0]
            feature_data['mf_functions'].append({
                'FUNCTION_NAME': main_data['Name'],
                'FUNCTION_INDEX': main_data['FullName'],
                'Detail':db.read_data('mainfunctions',{"Name":mf_name['mainfunctions_Name']})[0],
                'tf_functions': tf_functions  # 数组存储TF
            })
        # 读取MAIN FUNCTION，提取MF的TF映射
        # df_mainfunc = db.read_data('mainfunctions')
        # 为每个MF填充信息
            tf_list = db.read_data('mf_tf_input',{"mainfunctions_ID":main_data['ID']})
            for tf in tf_list:
                tf_data = db.read_data('technicalfunction',{"Name":tf['technicalfunction_Name']})[0]
                tf_functions.append({
                    'FUNCTION_NAME': tf_data['Name'],
                    'FUNCTION_INDEX': tf_data['FullName'],
                    'Detail':tf_data
                })

        
        # # 读取TECHNICAL FUNCTION，提取TF详情
        # df_techfunc = pd.read_excel(excel_path, sheet_name='TECHNICAL FUNCTION')
        # if not df_techfunc.empty:
        #     techfunc_index_col = next(
        #         (col for col in df_techfunc.columns if col.strip().upper() == 'FUNCTION_INDEX'),
        #         None
        #     )
            
        #     if techfunc_index_col:
        #         # 构建TF索引到详情的映射
        #         tf_detail_map = {
        #             str(row[techfunc_index_col]).strip(): row.to_dict()
        #             for _, row in df_techfunc.iterrows()
        #         }
        #         # 为每个MF填充TF详情（有序数组）
        #         for mf_data in feature_data['mf_functions']:
        #             if '_temp_tf_mappings' in mf_data:
        #                 for tf_index in mf_data['_temp_tf_mappings']:
        #                     if tf_index in tf_detail_map:
        #                         tf_details = {
        #                             k: str(v).strip()
        #                             for k, v in tf_detail_map[tf_index].items()
        #                             # if k != techfunc_index_col
        #                         }
        #                         mf_data['tf_functions'].append(tf_details)
        #                         print(tf_details)
        #                 # 移除临时字段
        #                 mf_data.pop('_temp_tf_mappings')
        
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
        
        return json.dumps(feature_data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        print(f"处理过程中出错：{str(e)}")
        return None

def extrac_function_breakdown_group(db,processed_results,lib_tables_data,target_table: str,category):
    Result = {}
    EUF_LIST = []
    EUF2FFS = {}
    euf_list = json.loads(extract_item_group(db,processed_results,lib_tables_data,"euf","functs"))['Catalogue']
    for euf in euf_list:
        euf_dict ={'name':f'EUF{euf_list[euf]["ID"]}','desc':euf_list[euf]["Name"],'feature':euf_list[euf]["function_features"]}
        EUF_LIST.append(euf_dict)
        if len(euf_list[euf]['function_features']) > 0:
            ffs_list = []
            for ff in euf_list[euf]['function_features']:
                ffs_list.append(f'FFS{ff["ID"]}')
            EUF2FFS[f'EUF{euf_list[euf]["ID"]}']=ffs_list

    
    FFS_LIST = []
    FFS2MF = {}
    ffs_list = json.loads(extract_item_group(db,processed_results,lib_tables_data,"function_features","functs"))['Catalogue']
    for ff in ffs_list:
        ffs_dict ={'name':f'FFS{ffs_list[ff]["ID"]}','desc':ffs_list[ff]["Name"]}
        FFS_LIST.append(ffs_dict)
        if len(ffs_list[ff]['feautre_mf_input']) > 0:
            mf_input_list = []
            for mf_input in ffs_list[ff]['feautre_mf_input']:
                mf_input_list.append(f'MF{mf_input["mainfunctions_Name"]["idmainfunc"]}')
            FFS2MF[f'FFS{ffs_list[ff]["ID"]}']=mf_input_list
        
    MF_LIST = []
    MF2TF = {}
    mf_list= json.loads(extract_item_group(db,processed_results,lib_tables_data,"mainfunctions","functs"))['Catalogue']
    for mf in mf_list:
        mf_dict ={'name':f'MF{mf_list[mf]["idmainfunc"]}','desc':mf_list[mf]["Name"]}
        MF_LIST.append(mf_dict)
        if len(mf_list[mf]['mf_tf_input']) > 0:
            tf_input_list = []
            for tf_input in mf_list[mf]['mf_tf_input']:
                tf_input_list.append(f'TF{tf_input["technicalfunction_Name"]["idfunc"]}')   
            MF2TF[f'MF{mf_list[mf]["ID"]}']=tf_input_list

    TF_LIST = []
    tf_list = json.loads(extract_item_group(db,processed_results,lib_tables_data,"technicalfunction","functs"))['Catalogue']
    for tf in tf_list:
        tf_dict ={'name':f'TF{tf_list[tf]["idfunc"]}','desc':tf_list[tf]["Name"]}
        TF_LIST.append(tf_dict)

    # for euf in json.loads(euf_list)["Catalogue"]:
    Result["EUF_LIST"]=EUF_LIST
    Result["EUF2FFS"]=EUF2FFS
    Result["FFS_LIST"]=FFS_LIST
    Result["FFS2MF"]=FFS2MF
    Result["MF_LIST"]=MF_LIST
    Result["MF2TF"]=MF2TF
    Result["TF_LIST"]=TF_LIST

    return json.dumps(Result,ensure_ascii=False, indent=2)
    

def extract_item_group(db,processed_results,lib_tables_data,target_table: str,category):
    # db = SQLOperations()
    Item_group = {}
    Item_group["type"]=target_table
    Item_group["Catalogue"]={}
    if category == "hardware":
        Item_group["Supplier"]={}
        Item_group["Type"]={}
        if target_table == "calculator":
            Item_group["Domain"]={}
    elif category == "vehicle":
        Item_group["Brand"]=[]
        Item_group["OEM"]=[]
        Item_group["Year"]=[]
        Item_group["PowerType"]=[]
    TargetLines = db.read_data(target_table)
    for line in TargetLines:
        result = extract_single_item(db,processed_results,lib_tables_data,target_table,line['Name'],'Name')
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
                processors = result_dict[line['Name']]["processor_group"]

                for processor in processors:
                    for item in (processors[processor]):
                        if item["Unit"] == "TOPS":
                            total_tops_power = total_tops_power + float(item["Power"])
                        if item["Unit"]=="KDMIPS":
                            total_cpu_power = total_cpu_power + float(item["Power"])
                result_dict[line['Name']]["AI_RESOURCE"] = str(total_tops_power)+" TOPS"
                result_dict[line["Name"]]["CPU_RESOURCE"] = str(total_cpu_power)+" KDMIPS"
                # Item_group["total_tops_power"] = total_tops_power
                Item_group["Catalogue"][line['Name']]=result_dict[line['Name']]
        elif category == "vehicle":
            # print(line)
            if line['Brand'] not in Item_group["Brand"]:
                Item_group["Brand"].append(line['Brand'])
                for item in result_dict[line['Name']]["Brand"]["corperate_input"]:
                    if item['Corperate_Name']["Name"] not in Item_group["OEM"]:
                        Item_group["OEM"].append(item['Corperate_Name']["Name"])

            if line['Launch_Time'] not in Item_group["Year"]:
                Item_group["Year"].append(line['Launch_Time'])
            if line["PowerType"] not in Item_group["PowerType"]:
                Item_group["PowerType"].append(line["PowerType"])
                        

    #     # 保存生成的数据结构到JSON文件
    # with open("generated_object_data.json", 'w', encoding='utf-8') as json_file:
    #     json.dump(Item_group, json_file, ensure_ascii=False, indent=2)
    
    # print(f"\n已生成类似object_data.json格式的数据结构，保存到 generated_object_data.json")

    return json.dumps(Item_group,ensure_ascii=False, indent=2)

def extract_entire_network(db,processed_results,lib_tables_data,target_table: str):
    # db = SQLOperations()
    Item_group = {}
    Item_group["type"]="Ele"
    Item_group["Element"]=[]
    TargetLines = db.read_data(target_table)
    for line in TargetLines:
        result = extract_single_item(db,processed_results,lib_tables_data,target_table,line['Name'],'Name')
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

def add_subscribers(db,data):
    # db = SQLOperations()
    userdata = {"Name": data['name'], "email": data["submitter_email"], "isSubscribe": True}
    # 尝试插入数据
    result = db.insert_data("user", userdata)
    if isinstance(result, int) and result > 0:
        # 向用户发送订阅确认邮件
        send_single_email(userdata["email"], "subscription_notification",userdata)
        
        # 向管理员发送新用户提醒邮件
        # admin_email = "darkerassistance@thedarker-tech.com"
        
        # 发送管理员提醒邮件，使用新的admin_notification邮件类型
        send_single_email(recipient_email=admin_email,email_type="admin_notification",user_data=userdata,notiftype="subscribe")
                
        return {"status": True, "insert_id": result}
    else:
        if "email" in result:
            exist_name = db.read_data("user",{"email":userdata["email"]})[0]["Name"]
            if exist_name == userdata['Name']:
                return {"status": False, "error": 1}
            else:
                return {"status": False, "error": 2,"name":exist_name}
        elif "Name" in result:
            exist_email = db.read_data("user",{"Name":userdata["Name"]})[0]["email"]
            if exist_email == userdata['email']:
                return {"status": False, "error": 1}
            else:
                return {"status": False, "error": 3,"name":data['name']}    

def submit_issue(db,data):
    # db = SQLOperations('dynamic')
        
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


def create_folder_local(base_path, template_name, target_name):
    """
    在本地创建文件夹，复制模板文件夹到目标位置
    
    Args:
        base_path: 基础路径
        template_name: 模板文件夹名称
        target_name: 目标文件夹名称
        user_data: 用户数据字典，包含email, UserLevel, RegisterTime，用于修改JSON文件
    
    Returns:
        bool: 创建是否成功
    """
    try:
        # 构建模板文件夹路径和目标文件夹路径
        template_path = os.path.join(base_path, template_name)
        target_path = os.path.join(base_path, str(target_name))
        
        # 检查模板文件夹是否存在
        if not os.path.exists(template_path):
            print(f"模板文件夹 {template_path} 不存在")
            return False
        
        # 检查目标文件夹是否已存在，如果存在则先删除
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
            print(f"已删除已存在的目标文件夹: {target_path}")
        
        # 复制模板文件夹到目标位置
        shutil.copytree(template_path, target_path)
        print(f"成功创建文件夹: {target_path}")
        
        return True
    except Exception as e:
        print(f"本地创建文件夹失败: {str(e)}")
        return False


def create_folder_remote(ssh_host, ssh_port, ssh_username, ssh_password, base_path, template_name, target_name):
    """
    通过SSH远程创建文件夹，复制模板文件夹到目标位置
    
    Args:
        ssh_host: SSH主机地址
        ssh_port: SSH端口
        ssh_username: SSH用户名
        ssh_password: SSH密码
        base_path: 基础路径
        template_name: 模板文件夹名称
        target_name: 目标文件夹名称
        user_data: 用户数据字典，包含email, UserLevel, RegisterTime，用于修改JSON文件
    
    Returns:
        bool: 创建是否成功
    """
    try:
        # 构建模板文件夹路径和目标文件夹路径
        template_path = os.path.join(base_path, template_name)
        target_path = os.path.join(base_path, str(target_name))
        
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 连接SSH服务器
        ssh.connect(ssh_host, ssh_port, ssh_username, ssh_password)
        
        # 执行命令：检查模板文件夹是否存在
        stdin, stdout, stderr = ssh.exec_command(f"if exist \"{template_path}\" (echo 1) else (echo 0)")
        template_exists = stdout.read().decode().strip() == "1"
        
        if not template_exists:
            print(f"远程模板文件夹 {template_path} 不存在")
            ssh.close()
            return False
        
        # 执行命令：删除已存在的目标文件夹（如果存在）
        ssh.exec_command(f"if exist \"{target_path}\" rmdir /s /q \"{target_path}\"")
        
        # 执行命令：复制模板文件夹到目标位置
        # 使用xcopy命令复制文件夹，/E 复制所有子目录和文件，/I 假设目标是目录
        stdin, stdout, stderr = ssh.exec_command(f"xcopy \"{template_path}\" \"{target_path}\" /E /I /Y")
        
        # 检查命令执行结果
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            print(f"成功远程创建文件夹: {target_path}")
            
        ssh.close()
        
        if exit_status == 0:
            return True
        else:
            error_msg = stderr.read().decode().strip()
            print(f"远程创建文件夹失败: {error_msg}")
            return False
    except Exception as e:
        print(f"SSH操作失败: {str(e)}")
        return False


def manage_register(db,data,deploy_mode):
    # print(data,deploy_mode) 
    current_id = None
    user_info = {}

    if data["regi_mode"] == "renew":
        userdata = {"email": data["email"], "Password": data["password"],"is_user":1,"UserLevel":"Normal"}
        current_id = db.read_data("user",{"email":data["email"]})[0]["ID"]
        if not current_id:
            return {"status": False, "error": 1}
        else:
            db.update_data("user",userdata,{"ID":current_id})
            result = db.read_data("user",{"ID":current_id})
    elif data["regi_mode"] == "new":
        userdata = {"email": data["email"], "Password": data["password"],"is_user":1,"UserLevel":"Normal","Name":data["name"],"isSubscribe":1}
        current_id = db.insert_data("user", userdata)
        if isinstance(current_id, int) and current_id > 0:
            # 获取新创建用户的current_id
            result = db.read_data("user",{"ID":current_id})
        else:
            return {"status": False, "error": "服务器故障，请稍后重试"}
                # 准备用户数据，用于修改userbasicinfo.json文件
    if isinstance(current_id, int) and current_id > 0:
        user_info = {
            "Email": result[0]["email"],
            "UserLevel": result[0]["UserLevel"],
            "Name": result[0]["Name"],
            "ID": result[0]["ID"],
            "RegisterTime":result[0]["create_time"],
            "Password":result[0]["Password"]
        }
        planetdata= {
            "AdasBenchmark":0,
            "ArchitectureBuild":0,
            "comparison":0,
            "Configurator":0,
            "EcoSystem_net":0,
            "Forum":0,
            "FoV_build":0,
            "FunctionHall":0,
            "HardWareHall":0,
            "Knowledgenet":0,
            "markettrend":0,
            "PhyArchiTool":0,
            "RegulationMap":0,
            "RoadBuilder":0,
            "SensorHall":0,
            "SensorInspector":0,
            "SimulationPlatform":0,
            "solutionbenchmark":0,
            "user_ID":current_id
        }
        db.insert_data("lightplanet",planetdata)
    # 创建文件夹
    if current_id:
        base_path = "C:\\DarkerUserData"
        template_name = "Template"
        
        if deploy_mode == "test":
            ssh_host = server_ip
            ssh_port = server_sshport
            ssh_username = server_pseudo
            ssh_password = server_code
            create_folder_remote(ssh_host, ssh_port, ssh_username, ssh_password, base_path, template_name, current_id)
        else:
            # 本地模式：直接在本地创建文件夹
            create_folder_local(base_path, template_name, current_id)

        send_single_email(recipient_email=user_info["Email"],email_type="registration_confirmation",user_data=user_info)
        send_single_email(recipient_email=admin_email,email_type="admin_notification",user_data=user_info,notiftype="registration")
        return {"status": True, "error": 0}


def manage_login(db,data):
    # db = SQLOperations()
    if data["mode"] == "email":
        result = db.read_data("user",{"Name":data["name"]})
    elif data["mode"] == "username":
        result = db.read_data("user",{"Name":data["name"]})

    if not result:
        return {"status": False, "error": 1}
    else:
        if (result[0]["Password"] == data["password"]) and (result[0]["is_user"] == 1):
            userinfo = result[0]
            if userinfo["UserLevel"].startswith("Manager"):
                userinfo = convert_datetime_to_str(userinfo)
                Final = {"status": True, "error": 0,"UserInfo":userinfo}
            else:
                userinfo["userdata"]={}
                userinfo["userdata"]['lightplanet'] = db.read_data('lightplanet',{"user_ID":userinfo["ID"]})[0]
                userinfo["userdata"]["planetdictionary"] = db.read_data('productfeatures')
                userinfo = convert_datetime_to_str(userinfo)
                Final = {"status": True, "error": 0,"UserInfo":userinfo}
            return json.dumps(Final, ensure_ascii=False, indent=2)
            
        else:
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

def fetch_advice_recording(db):
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
    # finally:
    #     # 确保数据库连接关闭
    #     try:
            
    #     except:
    #         pass

def fetch_siteproduct_info(db):
    Result = {}
    product_features = db.read_data("productfeatures")
    
    # 按Category列进行分类
    categorized_features = {}
    for feature in product_features:
        category = feature.get("Category", "未分类")
        if category not in categorized_features:
            categorized_features[category] = []
        categorized_features[category].append(feature)
    
    # 添加Result结果
    Result["productfeatures"] = product_features
    Result["categorized_features"] = categorized_features
    
    # 保留原有的status枚举量
    Status_info = db.read_data("online_enum")
    Result["status"] = []
    for item in Status_info:
        Result["status"].append(item["status"])

    Feedback = {"status": True, "error": 0,"Result":Result}
    return json.dumps(Feedback, ensure_ascii=False, indent=2)

def update_recordings(db,data,id):
    row=db.update_data("issuesandadvice", data,{"ID": id})
    Result = fetch_advice_recording(db)
    Feedback = {"status": True, "error": 0,"Result":json.loads(Result)}

    return json.dumps(Feedback, ensure_ascii=False, indent=2)

def update_productStatus(db,data,id):
    row=db.update_data("productfeatures", data,{"ID": id})
    Result = fetch_siteproduct_info(db)
    Feedback = {"status": True, "error": 0,"Result":json.loads(Result)}

    return json.dumps(Feedback, ensure_ascii=False, indent=2)

def delete_recordings(db,id):
    row=db.delete_data("issuesandadvice", {"ID": id})
    Result = fetch_advice_recording(db) 
    Feedback = {"status": True, "error": 0,"Result":json.loads(Result)}

    return json.dumps(Feedback, ensure_ascii=False, indent=2)

def get_all_users(db):
    Result = {}
    users = db.read_data("user")
    Result["user"] = users
    Result["user_count"] = len(users)
    Result = convert_datetime_to_str(Result)
    Feedback = {"status": True, "error": 0,"Result":Result}
    
    return json.dumps(Feedback, ensure_ascii=False, indent=2)

def create_task(db,data):

    Result = db.insert_data("release_content",data)
    if data["Content_Type"]=="creation":
        db.update_data("release_content",{"Bug_ID": "NO-"+str(Result)},{"ID":Result})
        # db.update_data("release_content",{"ID":Result},{"Bug_ID": "No-"+tostring(Result)})


    Feedback = {"status": True, "error": 0,"Result":Result}
    return json.dumps(Feedback, ensure_ascii=False, indent=2)

def update_task(db,data):
    if data["table"] == "task":
        id = data["content"]["Task_ID"]
        columns = data["content"]["Column"]
        value = data["content"]["Value"]

    elif data["table"] == "bug_fix":
        id = db.read_data("release_content",{"Bug_ID":data["content"]["Task_ID"]})[0]["ID"]
        columns = data["content"]["Column"]
        value = data["content"]["Value"]
    

    row=db.update_data("release_content",{columns:value},{"ID": id})
    Feedback = {"status": True, "error": 0,"Result":row}
    return json.dumps(Feedback, ensure_ascii=False, indent=2)

def get_task_tobepub(db):
    Result = {}
    content = db.read_data("release_content")
    Result["content"] = content
    Result["content_count"] = sum(1 for item in content if item.get("Item_Status") != "已上线")
    Result = convert_datetime_to_str(Result)
    Feedback = {"status": True, "error": 0,"Result":Result}
    
    return json.dumps(Feedback, ensure_ascii=False, indent=2)

def visit_management(db,data,uservisit):

    Result = db.insert_data("visit",data)
    Feedback = {"status": True, "error": 0,"Result":Result}
    if uservisit:
        funclist = db.read_data("lightplanet",{"user_ID":uservisit["userid"]})[0]
        for key in funclist:
            if key not in ("ID", "user_ID"):
                if key.lower() in uservisit["page"].lower():
                    db.update_data("lightplanet",{key:funclist[key]+1},{"user_ID":uservisit["userid"]})

    return json.dumps(Feedback, ensure_ascii=False, indent=2)


def visit_statistic(db):
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