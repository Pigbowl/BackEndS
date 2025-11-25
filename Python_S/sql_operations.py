import pymysql
from typing import Dict, List, Any, Optional

# 全局变量：部署模式
deploy_mode = "test"  # 用于存储部署模式信息

class SQLOperations:
    def __init__(self):
        """
        初始化MySQL数据库连接
        
        Args:
            host: MySQL主机地址
            user: MySQL用户名
            password: MySQL密码
            database: MySQL数据库名
        """
        # 保存数据库名作为实例变量
        self.database = "darkerdatabase"
        if deploy_mode == "local" or deploy_mode == "full":
            host = '47.99.204.97'
            user = 'root'
            password = '12345678'
        elif deploy_mode == "test":
            host = 'localhost'
            user = 'root'
            password = '12345678'
        else:
            raise ValueError("无效的部署模式")
        
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=self.database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        # 设置自动提交
        self.conn.autocommit(True)
    
    def close(self):
        """
        关闭数据库连接
        """
        if self.conn:
            self.conn.close()
    
    def insert_data(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        向表格中插入数据
        
        Args:
            table_name: 表格名称
            data: 要插入的数据，字典格式 {列名: 值}
            
        Returns:
            插入的行ID
        """
        try:
            cursor = self.conn.cursor()
            
            # 构建插入语句
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            values = tuple(data.values())
            
            cursor.execute(sql, values)
            
            # 获取插入的行ID
            row_id = cursor.lastrowid
                
            cursor.close()
            return row_id
            
        except Exception as e:
            print(f"插入数据时出错: {str(e)}")
            return f"插入数据时出错: {str(e)}"
    
    def read_data(self, table_name: str, conditions: Optional[Dict[str, Any]] = None, 
                  columns: Optional[List[str]] = None, limit: int = 0) -> List[Dict[str, Any]]:
        """
        从表格中读取数据
        
        Args:
            table_name: 表格名称
            conditions: 查询条件，字典格式 {列名: 值}
            columns: 要查询的列名列表，None表示查询所有列
            limit: 返回结果的最大数量，0表示无限制
            
        Returns:
            查询结果列表
        """
        try:
            cursor = self.conn.cursor()
            
            # 构建查询语句
            if columns:
                cols = ', '.join(columns)
            else:
                cols = '*'
                
            sql = f"SELECT {cols} FROM {table_name}"
            
            values = []
            if conditions:
                where_clauses = []
                for key, value in conditions.items():
                    where_clauses.append(f"{key} = %s")
                    values.append(value)
                
                sql += " WHERE " + " AND ".join(where_clauses)
            
            if limit > 0:
                sql += f" LIMIT {limit}"
            
            cursor.execute(sql, values)
            
            # MySQL已经返回字典格式的结果
            result = cursor.fetchall()
            
            cursor.close()
            return result
            
        except Exception as e:
            print(f"读取数据时出错: {str(e)}")
            return []
    
    def update_data(self, table_name: str, data: Dict[str, Any], conditions: Dict[str, Any]) -> int:
        """
        修改表格中的数据
        
        Args:
            table_name: 表格名称
            data: 要更新的数据，字典格式 {列名: 新值}
            conditions: 更新条件，字典格式 {列名: 值}
            
        Returns:
            受影响的行数
        """
        try:
            # 检查data是否为空，如果为空则不需要更新
            if not data:
                print(f"警告: 没有要更新的数据，表名: {table_name}")
                return 0
                
            cursor = self.conn.cursor()
            
            # 构建更新语句
            set_clauses = []
            values = []
            
            for key, value in data.items():
                set_clauses.append(f"{key} = %s")
                values.append(value)
            
            where_clauses = []
            for key, value in conditions.items():
                where_clauses.append(f"{key} = %s")
                values.append(value)
            
            # 确保set_clauses不为空
            if not set_clauses:
                print(f"警告: 无法构建有效的UPDATE语句，没有要设置的列，表名: {table_name}")
                cursor.close()
                return 0
                
            sql = f"UPDATE {table_name} SET " + ", ".join(set_clauses)
            sql += " WHERE " + " AND ".join(where_clauses)
            
            cursor.execute(sql, values)
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
            
        except Exception as e:
            print(f"更新数据时出错: {str(e)}")
            return 0
    
    def overwrite_entry(self, table_name: str, data: Dict[str, Any], primary_key: Dict[str, Any]) -> bool:
        """
        覆盖表格中的条目（先检查是否存在，存在则更新，不存在则插入）
        
        Args:
            table_name: 表格名称
            data: 要保存的数据，字典格式 {列名: 值}
            primary_key: 主键条件，字典格式 {主键列: 值}
            
        Returns:
            操作是否成功
        """
        try:
            # 检查条目是否存在
            existing_data = self.read_data(table_name, primary_key)
            
            if existing_data:
                # 存在则更新
                # 合并主键和要更新的数据
                update_data = {**data}
                # 确保主键列不被更新
                for key in primary_key:
                    update_data.pop(key, None)
                
                self.update_data(table_name, update_data, primary_key)
                return True
            else:
                # 不存在则插入
                # 合并主键和数据
                insert_data = {**primary_key, **data}
                self.insert_data(table_name, insert_data)
                return True
                
        except Exception as e:
            print(f"覆盖条目时出错: {str(e)}")
            return False
    
    def delete_data(self, table_name: str, conditions: Dict[str, Any]) -> int:
        """
        从表格中删除数据
        
        Args:
            table_name: 表格名称
            conditions: 删除条件，字典格式 {列名: 值}
            
        Returns:
            受影响的行数
        """
        try:
            cursor = self.conn.cursor()
            
            # 构建删除语句
            where_clauses = []
            values = []
            
            for key, value in conditions.items():
                where_clauses.append(f"{key} = %s")
                values.append(value)
            
            sql = f"DELETE FROM {table_name}"
            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)
            
            cursor.execute(sql, values)
            affected_rows = cursor.rowcount
            cursor.close()
            print(f"删除数据，影响行数: {affected_rows}")
            return affected_rows
            
        except Exception as e:
            print(f"删除数据时出错: {str(e)}")
            return 0

# 使用示例
def example_usage():
    # MySQL示例
    print("MySQL示例:")
    # 请根据实际情况修改数据库连接信息
    db = SQLOperations(
        host='47.99.204.97',    # MySQL主机地址
        user='root',         # MySQL用户名
        password='12345678',         # MySQL密码
        database='darkerdatabase'   # MySQL数据库名
    )
    
    # 创建测试表
    cursor = db.conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT,
        email VARCHAR(255)
    )
    ''')
    cursor.close()
    
    # 插入数据
    insert_id = db.insert_data('users', {'name': '张ER', 'age': 30, 'email': 'zhangsan@example.com'})
    print(f"插入数据，ID: {insert_id}")
    
    # 读取数据
    users = db.read_data('users')
    print(f"读取所有用户: {users}")
    
    # 根据条件读取
    young_users = db.read_data('users', {'age': 30})
    print(f"读取30岁的用户: {young_users}")
    
    # # 更新数据
    affected = db.update_data('users', {'age': 31}, {'name': '张三'})
    print(f"更新数据，影响行数: {affected}")
    
    # 覆盖条目
    db.overwrite_entry('users', {'email': 'newemail@example.com'}, {'id': 1})
    print("覆盖条目")
    
    # 再次读取
    updated_user = db.read_data('users', {'id': 1})
    print(f"更新后的用户: {updated_user}")
    
    # 关闭连接
    db.close()

if __name__ == "__main__":
    # 注意：运行前请确保已安装pymysql库
    # pip install pymysql
    # 并且已经创建了MySQL数据库
    example_usage()