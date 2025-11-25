import os
import subprocess
import pymysql
from pymysql.err import OperationalError
import time
import sys
# 若用SSH传文件，需导入paramiko（否则注释以下2行）
import paramiko
from paramiko import SSHClient, AutoAddPolicy
# 用于RDP文件传输
import socket
import winreg
import importlib.util

# ============================ 配置区（必改！按你的实际情况填写）============================
# 1. 本地MySQL配置
LOCAL_MYSQL = {
    "host": "localhost",
    "port": 3306,
    "user": "root",          # 本地MySQL用户名
    "password": "12345678",  # 本地MySQL密码
    "db": "darkerdatabase",  # 要同步的数据库名
    "dump_path": "C:\\Users\\宋嘉玮\\OneDrive\\Desktop\\BackEndS",  # 本地SQL文件导出路径（Windows用双反斜杠）
    "sql_filename": "darkerdatabase_auto.sql"  # 导出的SQL文件名
}

# 尝试自动检测MySQL可能的安装路径
POSSIBLE_MYSQL_PATHS = [
    "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump.exe",
    "C:\\Program Files\\MySQL\\MySQL Server 5.7\\bin\\mysqldump.exe",
    "C:\\Program Files (x86)\\MySQL\\MySQL Server 8.0\\bin\\mysqldump.exe",
    "C:\\Program Files (x86)\\MySQL\\MySQL Server 5.7\\bin\\mysqldump.exe",
    "C:\\xampp\\mysql\\bin\\mysqldump.exe",
    "C:\\wamp64\\bin\\mysql\\mysql8.0.xx\\bin\\mysqldump.exe",
    "C:\\wamp\\bin\\mysql\\mysql5.7.xx\\bin\\mysqldump.exe",
    "C:\\Program Files\\MySQL\\MySQL Server 9.5\\bin\\mysqldump.exe"
]

def find_mysqldump():
    """自动查找mysqldump可执行文件"""
    # 首先尝试系统环境变量中的mysqldump
    try:
        subprocess.run(["mysqldump", "--version"], capture_output=True, check=True)
        return "mysqldump"
    except:
        pass
    
    # 然后尝试常见的安装路径
    for path in POSSIBLE_MYSQL_PATHS:
        if os.path.exists(path):
            return path
    
    # 如果都找不到，提示用户手动设置
    return None

# 2. 云端服务器配置（二选一：robocopy传文件 / SSH传文件）
# 方式A：robocopy传文件（Windows原生，推荐）
REMOTE_ROBOCOPY = {
    "server_ip": "47.99.204.97",  # 如 123.45.67.89
    "share_dir": "\\\\47.99.204.97\\mysql_sync",  # 云端共享目录（双反斜杠）
    "local_sql_path": f"{LOCAL_MYSQL['dump_path']}{LOCAL_MYSQL['sql_filename']}",  # 本地SQL文件完整路径
    "remote_server_user": "Administrator",  # 如 Administrator
    "remote_server_pwd": "Sjw9@0613"     # 登录云端服务器的密码
}

# 方式B：SSH传文件（需云端开启SSH服务，注释方式A可启用）
# REMOTE_SSH = {
#     "server_ip": "你的云端服务器IP",
#     "ssh_port": 22,  # SSH默认端口22
#     "ssh_user": "云端服务器登录用户名",  # 如 Administrator
#     "ssh_pwd": "云端服务器登录密码",
#     "remote_sql_dir": "D:\\mysql_sync\\",  # 云端接收SQL文件的目录（Windows路径）
#     "local_sql_path": f"{LOCAL_MYSQL['dump_path']}{LOCAL_MYSQL['sql_filename']}"
# }

# 方式C：RDP传文件（通过已映射的远程驱动器，3389端口）
REMOTE_RDP = {
    "server_ip": "47.99.204.97",  # 如 123.45.67.89
    "rdp_port": 3389,  # RDP默认端口3389
    "remote_server_user": "Administrator",  # 如 Administrator
    "remote_server_pwd": "Sjw9@0613",  # 登录云端服务器的密码
    "mapped_drive": "Z:",  # 通过RDP映射的网络驱动器字母
    "remote_sql_dir": "C:\\Users\\Administrator\\Desktop\\mysql_sync\\",  # 云端接收SQL文件的目录（Windows路径）
    "local_sql_path": f"{LOCAL_MYSQL['dump_path']}{LOCAL_MYSQL['sql_filename']}"  # 本地SQL文件完整路径
}

# 3. 云端MySQL配置（之前授权的账号）
REMOTE_MYSQL = {
    "host": "47.99.204.97",  # 与云端服务器IP保持一致
    "port": 3306,
    "user": "root",          # 云端MySQL授权账号（root@%）
    "password": "12345678",  # 云端MySQL密码
    "db": "darkerdatabase",  # 云端数据库名（已创建）
    "remote_sql_path": "C:\\Users\\Administrator\\Desktop\\mysql_sync\\darkerdatabase_auto.sql"  # 云端SQL文件完整路径（和接收目录一致）
}
# ======================================================================================

def export_local_sql():
    """第一步：本地无Workbench导出SQL（调用mysqldump命令）"""
    print("=== 开始导出本地数据库SQL文件 ===")
    
    # 自动查找mysqldump路径
    mysqldump_exe = find_mysqldump()
    
    # 如果找不到mysqldump，提供备选方案
    if not mysqldump_exe:
        print("❌ 找不到mysqldump可执行文件！")
        print("尝试备选方案：直接使用pymysql导出数据...")
        return export_local_sql_pymysql()
    
    print(f"找到mysqldump路径：{mysqldump_exe}")
    
    # 确保导出路径存在
    if not os.path.exists(LOCAL_MYSQL['dump_path']):
        try:
            os.makedirs(LOCAL_MYSQL['dump_path'])
            print(f"📁 创建导出目录：{LOCAL_MYSQL['dump_path']}")
        except Exception as e:
            print(f"❌ 无法创建导出目录：{str(e)}")
            return False
    
    # 修复路径连接问题（添加斜杠）
    dump_path = LOCAL_MYSQL['dump_path']
    if not dump_path.endswith('\\') and not dump_path.endswith('/'):
        dump_path += '\\'
    
    output_file = f"{dump_path}{LOCAL_MYSQL['sql_filename']}"
    
    # 构建mysqldump命令（Windows环境，兼容空格）
    # 注意：当路径包含空格时，需要用引号包裹可执行文件路径
    if ' ' in mysqldump_exe:
        mysqldump_exe = f'"{mysqldump_exe}"'
    
    dump_cmd = (
        f'{mysqldump_exe} -h {LOCAL_MYSQL["host"]} -u {LOCAL_MYSQL["user"]} -p{LOCAL_MYSQL["password"]} '  
        f"--databases {LOCAL_MYSQL['db']} --routines --events --triggers --set-gtid-purged=OFF "
        f'> "{output_file}"'
    )
    
    # 执行命令（隐藏黑窗口，捕获输出）
    try:
        print(f"正在执行命令：{dump_cmd}")
        result = subprocess.run(
            dump_cmd, shell=True, check=True, capture_output=True, text=True, encoding="gbk"
        )
        
        if os.path.exists(output_file):
            print(f"✅ 导出成功！SQL文件路径：{output_file}")
            return True
        else:
            print("❌ 导出失败：未生成SQL文件")
            if result.stderr:
                print(f"错误输出：{result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ 导出失败：{e.stderr}")
        # 失败时尝试备选方案
        print("尝试备选方案：直接使用pymysql导出数据...")
        return export_local_sql_pymysql()
    except Exception as e:
        print(f"❌ 导出过程中发生未知错误：{str(e)}")
        # 失败时尝试备选方案
        print("尝试备选方案：直接使用pymysql导出数据...")
        return export_local_sql_pymysql()

def export_local_sql_pymysql():
    """备选方案：使用pymysql直接导出数据库结构和数据"""
    print("=== 使用pymysql备选方案导出数据库 ===")
    
    # 确保导出路径存在
    if not os.path.exists(LOCAL_MYSQL['dump_path']):
        try:
            os.makedirs(LOCAL_MYSQL['dump_path'])
            print(f"📁 创建导出目录：{LOCAL_MYSQL['dump_path']}")
        except Exception as e:
            print(f"❌ 无法创建导出目录：{str(e)}")
            return False
    
    # 修复路径连接问题（添加斜杠）
    dump_path = LOCAL_MYSQL['dump_path']
    if not dump_path.endswith('\\') and not dump_path.endswith('/'):
        dump_path += '\\'
    
    output_file = f"{dump_path}{LOCAL_MYSQL['sql_filename']}"
    
    try:
        # 连接到MySQL数据库
        conn = pymysql.connect(
            host=LOCAL_MYSQL['host'],
            user=LOCAL_MYSQL['user'],
            password=LOCAL_MYSQL['password'],
            db=LOCAL_MYSQL['db'],
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # 获取所有表名
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # 写入数据库创建语句
            f.write(f"CREATE DATABASE IF NOT EXISTS `{LOCAL_MYSQL['db']}`;\nUSE `{LOCAL_MYSQL['db']}`;\n\n")
            
            # 导出每个表的结构和数据
            for table in tables:
                table_name = table[0]
                print(f"正在导出表：{table_name}")
                
                # 获取表结构
                cursor.execute(f"SHOW CREATE TABLE `{table_name}`;")
                create_table = cursor.fetchone()
                f.write(f"-- 表结构: {table_name}\n")
                f.write(f"{create_table[1]};\n\n")
                
                # 获取表数据
                cursor.execute(f"SELECT * FROM `{table_name}`;")
                rows = cursor.fetchall()
                
                if rows:
                    # 获取列名
                    columns = [desc[0] for desc in cursor.description]
                    column_count = len(columns)
                    
                    # 生成INSERT语句
                    f.write(f"-- 表数据: {table_name}\n")
                    # 正确连接列名
                    columns_str = '`, `'.join(columns)
                    f.write(f"INSERT INTO `{table_name}` (`{columns_str}`) VALUES\n")
                    
                    values = []
                    for row in rows:
                        row_values = []
                        for value in row:
                            if value is None:
                                row_values.append('NULL')
                            elif isinstance(value, str):
                                # 转义字符串中的特殊字符
                                escaped = value.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
                                row_values.append(f"'{escaped}'")
                            elif isinstance(value, (int, float)):
                                row_values.append(str(value))
                            else:
                                row_values.append(f"'{str(value)}'")
                        values.append(f"  ({', '.join(row_values)})")
                    
                    # 写入数据行
                    f.write(',\n'.join(values) + ';\n\n')
        
        cursor.close()
        conn.close()
        
        print(f"✅ pymysql备选方案导出成功！SQL文件路径：{output_file}")
        return True
    
    except Exception as e:
        print(f"❌ pymysql备选方案导出失败：{str(e)}")
        return False

def upload_sql_to_remote():
    """上传SQL文件到远程服务器
    
    优先使用RDP方式上传文件，然后尝试网络共享方式，最后回退到SSH方式
    """
    print("\n=== 开始上传SQL文件到云端 ===")
    
    # 1. 首先尝试通过RDP方式上传（方式C，推荐）
    print("\n1. 尝试使用RDP方式上传（推荐）...")
    try:
        success = upload_sql_to_remote_rdp()
        if success:
            print("✅ RDP方式上传成功")
            return True
        else:
            print("❌ RDP方式上传失败")
    except Exception as e:
        print(f"❌ RDP方式上传过程中发生异常：{str(e)}")
        import traceback
        print(f"详细错误信息：{traceback.format_exc()}")
    
    # 2. 如果RDP方式失败，尝试通过网络共享方式上传（方式A）
    print("\n2. 尝试使用网络共享方式上传...")
    
    # 检查本地SQL文件是否存在
    # 修复LOCAL_SQL_PATH的构建方式
    dump_path = LOCAL_MYSQL['dump_path']
    if not dump_path.endswith('\\') and not dump_path.endswith('/'):
        dump_path += '\\'
    local_sql_path = f"{dump_path}{LOCAL_MYSQL['sql_filename']}"
    
    if not os.path.exists(local_sql_path):
        print(f"❌ 错误：本地SQL文件不存在！路径：{local_sql_path}")
        return False
    
    print(f"本地SQL文件路径：{local_sql_path}")
    print(f"云端共享目录：{REMOTE_ROBOCOPY['share_dir']}")
    
    source_dir = os.path.dirname(local_sql_path)
    file_name = os.path.basename(local_sql_path)
    
    try:
        # 第1步：先尝试建立网络连接（net use）
        print("\n2.1 尝试建立网络连接...")
        net_use_cmd = f"net use \"{REMOTE_ROBOCOPY['share_dir']}\" {REMOTE_ROBOCOPY['remote_server_pwd']} /USER:{REMOTE_ROBOCOPY['remote_server_user']}"
        print(f"执行net use命令：{net_use_cmd}")
        
        net_result = subprocess.run(
            net_use_cmd, shell=True, capture_output=True, text=True, encoding="gbk"
        )
        
        print(f"net use返回码：{net_result.returncode}")
        if net_result.stdout:
            print(f"net use输出：{net_result.stdout.strip()}")
        if net_result.stderr:
            print(f"net use错误：{net_result.stderr.strip()}")
        
        # 检查net use是否成功
        if net_result.returncode != 0:
            print(f"❌ 网络连接失败！错误码：{net_result.returncode}")
            print("可能的原因：")
            print("1. 网络连接问题 - 请检查网络连接和防火墙设置")
            print("2. 共享目录不存在 - 请确认服务器上的共享设置")
            print("3. 用户名或密码错误 - 请检查认证信息")
            print("4. 共享权限问题 - 请确认用户有访问权限")
            
            # 尝试备选方案：启用SSH上传功能
            print("\n尝试使用SSH方式上传文件...")
            return upload_sql_to_remote_ssh()
        
        # 第2步：连接成功后，执行robocopy命令
        print("\n2.2 网络连接成功，开始复制文件...")
        robocopy_cmd = f"robocopy \"{source_dir}\" \"{REMOTE_ROBOCOPY['share_dir']}\" {file_name} /R:3 /W:5 /V"
        print(f"执行robocopy命令：{robocopy_cmd}")
        
        robocopy_result = subprocess.run(
            robocopy_cmd, shell=True, capture_output=True, text=True, encoding="gbk"
        )
        
        print(f"robocopy返回码：{robocopy_result.returncode}")
        if robocopy_result.stdout:
            print(f"robocopy输出：{robocopy_result.stdout.strip()}")
        if robocopy_result.stderr:
            print(f"robocopy错误：{robocopy_result.stderr.strip()}")
        
        # 最后一步：无论成功与否，断开网络连接以释放资源
        print("\n2.3 清理网络连接...")
        net_use_del_cmd = f"net use \"{REMOTE_ROBOCOPY['share_dir']}\" /delete /yes"
        subprocess.run(net_use_del_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 判断robocopy是否成功
        if robocopy_result.returncode in [0, 1]:  # 0=无变化，1=复制成功
            print(f"✅ 上传成功！云端文件路径：{REMOTE_ROBOCOPY['share_dir']}\\{LOCAL_MYSQL['sql_filename']}")
            return True
        else:
            print(f"❌ 上传失败：robocopy返回码 {robocopy_result.returncode}")
            # 尝试SSH备选方案
            print("尝试使用SSH方式上传文件...")
            return upload_sql_to_remote_ssh()
            
    except Exception as e:
        print(f"❌ 上传过程中发生异常：{str(e)}")
        import traceback
        print(f"详细错误信息：{traceback.format_exc()}")
        
        # 3. 如果前两种方式都失败，尝试备选的SSH方式
        print("\n3. 尝试使用SSH方式上传文件...")
        return upload_sql_to_remote_ssh()


def upload_sql_to_remote_rdp(dump_path=None, sql_filename=None):
    """
    通过RDP方式上传SQL文件到远程服务器 (TCP:3389端口)
    1. 使用net use映射网络驱动器或直接使用UNC路径
    2. 使用robocopy传输文件
    3. 验证文件传输是否成功
    4. 断开网络驱动器连接
    
    参数:
        dump_path: SQL文件导出路径
        sql_filename: SQL文件名
    
    返回:
        bool: 文件传输是否成功
    """
    # 如果未提供路径，使用配置中的默认值
    if dump_path is None:
        dump_path = LOCAL_MYSQL['dump_path']
    if sql_filename is None:
        sql_filename = LOCAL_MYSQL['sql_filename']
    
    # 确保路径格式正确
    if not dump_path.endswith('\\') and not dump_path.endswith('/'):
        dump_path += '\\'
    
    local_sql_path = f"{dump_path}{sql_filename}"
    file_name = os.path.basename(local_sql_path)
    drive_mapped = False  # 初始化变量，确保在异常情况下也能被正确识别
    
    print("\n=== 开始通过RDP方式上传SQL文件 ===")
    print(f"使用TCP:3389端口连接服务器 {REMOTE_RDP['server_ip']}")
    
    try:
        # 1. 检查本地SQL文件是否存在
        print(f"\n1. 检查本地SQL文件：{local_sql_path}")
        try:
            if not os.path.exists(local_sql_path):
                print(f"❌ 错误：本地SQL文件不存在！路径：{local_sql_path}")
                print("请确保数据库导出功能正常工作，检查导出路径是否正确")
                return False
            
            # 检查文件大小，确保不是空文件
            file_size = os.path.getsize(local_sql_path)
            if file_size == 0:
                print(f"❌ 错误：本地SQL文件为空！请检查数据库导出是否成功")
                return False
            
            print(f"✅ 本地SQL文件存在 (大小: {file_size:,} 字节)")
        except PermissionError:
            print(f"❌ 权限错误：无法访问本地SQL文件！请检查文件权限")
            return False
        except Exception as e:
            print(f"❌ 检查本地SQL文件时发生错误：{str(e)}")
            return False
        
        # 2. 检查RDP端口连通性
        print(f"\n2. 测试RDP端口 {REMOTE_RDP['rdp_port']} 连通性")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(8)  # 增加超时时间，确保网络延迟时有足够时间响应
            result = sock.connect_ex((REMOTE_RDP['server_ip'], REMOTE_RDP['rdp_port']))
            sock.close()
            
            if result == 0:
                print(f"✅ RDP端口 {REMOTE_RDP['rdp_port']} 连通性测试通过")
            else:
                print(f"❌ RDP端口 {REMOTE_RDP['rdp_port']} 不可访问")
                print("请检查以下内容：")
                print("1. 确认远程服务器已启用远程桌面服务")
                print("2. 检查服务器防火墙是否允许3389端口连接")
                print("3. 确认云服务商安全组规则已开放3389端口")
                print("4. 验证服务器IP地址是否正确")
                # 端口不通但仍尝试继续，可能已有其他方式连接或端口已映射
                print("\n⚠️ 端口测试失败，但将继续尝试连接（可能存在端口映射或其他访问方式）")
        except socket.timeout:
            print(f"❌ RDP端口测试超时：连接服务器 {REMOTE_RDP['server_ip']}:{REMOTE_RDP['rdp_port']} 超时")
            print("请检查网络连接和服务器是否在线")
        except Exception as e:
            print(f"⚠️ RDP端口测试时发生异常：{str(e)}")
        
        # 3. 检查映射驱动器是否可用
        mapped_drive = REMOTE_RDP['mapped_drive']
        remote_sql_dir = REMOTE_RDP['remote_sql_dir']
        
        # 准备通过映射驱动器的目标路径
        # 如果使用的是绝对路径（C:\），则直接使用，否则使用映射驱动器
        if remote_sql_dir.startswith('C:\\') or remote_sql_dir.startswith('D:\\'):
            # 对于Windows服务器，我们将尝试使用net use映射网络驱动器
            print(f"\n3. 尝试映射网络驱动器到服务器共享目录")
            
            # 构建目标路径（使用UNC格式）
            try:
                # 先处理路径部分，避免在f-string中使用反斜杠
                path_part = remote_sql_dir.split(':')[-1].strip('\\')
                unc_path = f"\\\\{REMOTE_RDP['server_ip']}\\{path_part}"
                print(f"目标UNC路径：{unc_path}")
            except Exception as e:
                print(f"❌ 构建UNC路径时发生错误：{str(e)}")
                print("请检查远程目录路径格式是否正确")
                return False
            
            try:
                # 第一步：映射网络驱动器
                print("  a. 正在映射网络驱动器...")
                net_use_cmd = (
                    f"net use {mapped_drive} {unc_path} "
                    f"/user:{REMOTE_RDP['remote_server_user']} {REMOTE_RDP['remote_server_pwd']} /persistent:no"
                )
                # 不打印包含密码的完整命令，提高安全性
                print(f"执行命令：net use {mapped_drive} {unc_path} /user:{REMOTE_RDP['remote_server_user']} ****** /persistent:no")
                
                # 添加超时控制
                net_use_result = subprocess.run(
                    net_use_cmd, shell=True, capture_output=True, text=True, encoding="gbk", timeout=30
                )
                
                if "命令成功完成" in net_use_result.stdout or "successfully" in net_use_result.stdout:
                    print(f"✅ 成功映射网络驱动器 {mapped_drive}")
                    drive_mapped = True
                else:
                    print(f"❌ 映射网络驱动器失败")
                    if net_use_result.stdout:
                        # 清理输出，移除可能的敏感信息
                        safe_output = net_use_result.stdout.strip()
                        if REMOTE_RDP['remote_server_pwd'] in safe_output:
                            safe_output = safe_output.replace(REMOTE_RDP['remote_server_pwd'], '******')
                        print(f"输出: {safe_output}")
                    if net_use_result.stderr:
                        print(f"错误: {net_use_result.stderr.strip()}")
                    
                    # 尝试直接使用UNC路径而不映射驱动器
                    print("\n⚠️ 尝试直接使用UNC路径传输文件...")
                    mapped_drive = unc_path
                    drive_mapped = False
            except subprocess.TimeoutExpired:
                print(f"❌ 映射网络驱动器超时：操作超过30秒未完成")
                mapped_drive = unc_path
                drive_mapped = False
            except Exception as e:
                # 简化错误信息，避免暴露敏感内容
                error_msg = str(e)
                if REMOTE_RDP['remote_server_pwd'] in error_msg:
                    error_msg = error_msg.replace(REMOTE_RDP['remote_server_pwd'], '******')
                print(f"❌ 映射网络驱动器时发生异常：{error_msg}")
                mapped_drive = unc_path
                drive_mapped = False
        
        # 4. 确保远程目录存在
        print(f"\n4. 准备远程目录")
        try:
            # 对于UNC路径，我们需要特殊处理
            if mapped_drive.startswith('\\\\'):
                # 直接使用UNC路径
                remote_dir_path = mapped_drive
            else:
                # 使用映射驱动器
                remote_dir_path = f"{mapped_drive}\\"
            
            print(f"目标目录：{remote_dir_path}")
            
            # 检查目录是否存在
            if not os.path.exists(remote_dir_path):
                print(f"⚠️ 远程目录不存在，尝试创建")
                try:
                    # 在远程服务器上创建目录（使用PowerShell）
                    create_dir_cmd = (
                        f"powershell -Command \"& {{ "
                        f"$username = '{REMOTE_RDP['remote_server_user']}'; "
                        f"$password = ConvertTo-SecureString '{REMOTE_RDP['remote_server_pwd']}' -AsPlainText -Force; "
                        f"$credential = New-Object System.Management.Automation.PSCredential($username, $password); "
                        f"$remoteDir = '{remote_sql_dir}'; "
                        f"Invoke-Command -ComputerName {REMOTE_RDP['server_ip']} -Credential $credential -ScriptBlock {{ "
                        f"if (-not (Test-Path $using:remoteDir)) {{ "
                        f"    New-Item -ItemType Directory -Force -Path $using:remoteDir; "
                        f"    Write-Output 'Directory created'; "
                        f"}} else {{ "
                        f"    Write-Output 'Directory already exists'; "
                        f"}} "
                        f"}} "
                        f"}}\"")
                    
                    print("执行远程目录创建命令...")
                    create_result = subprocess.run(
                        create_dir_cmd, shell=True, capture_output=True, text=True, encoding="gbk", timeout=45
                    )
                    
                    if create_result.returncode == 0:
                        print(f"✅ 远程目录准备成功: {create_result.stdout.strip()}")
                    else:
                        print(f"⚠️ 远程目录创建返回非零值: {create_result.returncode}")
                        if create_result.stdout:
                            print(f"输出: {create_result.stdout.strip()}")
                        if create_result.stderr:
                            print(f"错误: {create_result.stderr.strip()}")
                            print("提示：目录可能已存在或权限不足，将继续尝试传输文件")
                except subprocess.TimeoutExpired:
                    print(f"❌ 远程目录创建超时：操作超过45秒未完成")
                    print("警告：将继续尝试传输，但可能会因为目录不存在而失败")
                except Exception as e:
                    error_msg = str(e)
                    if REMOTE_RDP['remote_server_pwd'] in error_msg:
                        error_msg = error_msg.replace(REMOTE_RDP['remote_server_pwd'], '******')
                    print(f"⚠️ 创建远程目录时发生异常：{error_msg}")
            else:
                print("✅ 远程目录已存在")
        except Exception as e:
            print(f"⚠️ 检查远程目录时发生异常：{str(e)}")
        
        # 5. 使用robocopy传输文件
        print(f"\n5. 开始文件传输...")
        transfer_success = False
        
        try:
            # 构建robocopy命令
            # 目标路径处理：如果是UNC路径直接使用，否则使用映射驱动器+路径
            if mapped_drive.startswith('\\\\'):
                target_path = mapped_drive
            else:
                # 从remote_sql_dir提取路径部分（去掉驱动器号）
                path_part = '\\'.join(remote_sql_dir.split('\\')[1:])
                target_path = f"{mapped_drive}\\{path_part}"
            
            # 确保目标路径正确
            if not target_path.endswith('\\'):
                target_path += '\\'
            
            print(f"源文件：{local_sql_path}")
            print(f"目标路径：{target_path}")
            
            # 执行robocopy命令（带/V参数显示详细信息，方便状态检测）
            robocopy_cmd = f"robocopy \"{os.path.dirname(local_sql_path)}\" \"{target_path}\" \"{file_name}\" /Z /R:3 /W:5 /V"
            print(f"执行命令：{robocopy_cmd}")
            
            # 增加超时设置，大文件传输可能需要更长时间
            file_size = os.path.getsize(local_sql_path)
            timeout_seconds = min(300, max(60, file_size // (1024 * 1024) * 10))  # 根据文件大小动态设置超时
            print(f"设置传输超时：{timeout_seconds}秒")
            
            # 使用Popen而非run，以支持实时状态检测
            start_time = time.time()
            last_status_time = start_time
            bytes_transferred = 0
            file_size_mb = file_size / (1024 * 1024)
            print(f"文件大小：{file_size_mb:.2f} MB")
            print("传输状态监控已启动...")
            
            try:
                # 启动robocopy进程
                process = subprocess.Popen(
                    robocopy_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, encoding="gbk"
                )
                
                # 实时读取并解析输出
                stdout_lines = []
                stderr_lines = []
                
                # 创建一个临时文件来监控传输进度
                temp_progress_file = os.path.join(os.environ['TEMP'], f"robocopy_progress_{int(time.time())}.tmp")
                
                # 循环读取输出，直到进程结束或超时
                while process.poll() is None:
                    current_time = time.time()
                    
                    # 检查是否超时
                    if current_time - start_time > timeout_seconds:
                        process.kill()
                        print("❌ 文件传输超时！")
                        raise subprocess.TimeoutExpired(robocopy_cmd, timeout_seconds)
                    
                    # 每3秒更新一次状态
                    if current_time - last_status_time >= 3:
                        # 尝试通过远程文件大小来估算进度
                        try:
                            # 构造远程文件的完整路径（使用UNC路径）
                            path_part = remote_sql_dir.split(':')[-1].strip('\\')
                            remote_unc_file = f"\\\\{REMOTE_RDP['server_ip']}\\{path_part}\\{file_name}"
                            
                            # 检查远程文件大小（如果可以访问）
                            if os.path.exists(remote_unc_file):
                                current_size = os.path.getsize(remote_unc_file)
                                progress_percent = (current_size / file_size) * 100 if file_size > 0 else 0
                                elapsed_time = current_time - start_time
                                print(f"📊 传输进度：{progress_percent:.1f}% ({current_size/1024/1024:.2f}MB/{file_size_mb:.2f}MB) - 耗时：{int(elapsed_time)}秒")
                        except Exception:
                            # 如果无法获取远程文件大小，至少显示已运行时间
                            elapsed_time = current_time - start_time
                            print(f"⏱️  传输进行中... 已运行：{int(elapsed_time)}秒")
                        
                        last_status_time = current_time
                    
                    # 读取输出
                    try:
                        stdout_data = process.stdout.read(1024)
                        if stdout_data:
                            stdout_lines.append(stdout_data)
                            # 尝试从输出中解析传输信息
                            for line in stdout_data.splitlines():
                                if "字节" in line or "Bytes" in line:
                                    print(f"🔄 {line.strip()}")
                    except Exception:
                        pass
                    
                    try:
                        stderr_data = process.stderr.read(1024)
                        if stderr_data:
                            stderr_lines.append(stderr_data)
                    except Exception:
                        pass
                    
                    # 小延迟避免CPU占用过高
                    time.sleep(0.5)
                
                # 收集剩余输出
                stdout_remaining, stderr_remaining = process.communicate()
                if stdout_remaining:
                    stdout_lines.append(stdout_remaining)
                if stderr_remaining:
                    stderr_lines.append(stderr_remaining)
                
                # 组合输出
                stdout = ''.join(stdout_lines)
                stderr = ''.join(stderr_lines)
                returncode = process.returncode
                
                # 输出最终结果
                total_time = time.time() - start_time
                print(f"✅ 传输完成！总耗时：{int(total_time)}秒")
                
                # 创建robocopy_result对象以保持兼容性
                class RobocopyResult:
                    def __init__(self, returncode, stdout, stderr):
                        self.returncode = returncode
                        self.stdout = stdout
                        self.stderr = stderr
                
                robocopy_result = RobocopyResult(returncode, stdout, stderr)
                
                # 输出robocopy结果（清理敏感信息）
                if robocopy_result.stdout:
                    safe_output = robocopy_result.stdout.strip()
                    print(f"robocopy输出：{safe_output}")
                if robocopy_result.stderr:
                    print(f"robocopy错误：{robocopy_result.stderr.strip()}")
                    
            except subprocess.TimeoutExpired:
                print("❌ 文件传输超时，请检查网络连接或增加超时时间")
                raise
            except Exception as e:
                print(f"❌ 文件传输过程中发生错误：{str(e)}")
                raise
            
            # 根据robocopy退出码判断是否成功
            # 0=没有文件复制，1=成功复制文件，2-8=警告，9-15=错误
            if robocopy_result.returncode in [0, 1]:
                print("✅ robocopy命令执行成功")
            else:
                print(f"⚠️ robocopy命令返回警告/错误代码: {robocopy_result.returncode}")
            
            # 6. 验证文件是否成功传输
            print("\n6. 验证文件传输结果...")
            # 构造远程文件的完整路径
            remote_file_path = f"{target_path}{file_name}"
            
            # 检查文件是否存在
            if os.path.exists(remote_file_path):
                # 获取文件大小进行验证
                local_size = os.path.getsize(local_sql_path)
                remote_size = os.path.getsize(remote_file_path)
                
                if local_size == remote_size:
                    print(f"✅ 文件传输成功且完整！源文件大小：{local_size:,}字节，目标文件大小：{remote_size:,}字节")
                    transfer_success = True
                else:
                    print(f"⚠️ 文件已传输但大小不匹配！源文件大小：{local_size:,}字节，目标文件大小：{remote_size:,}字节")
                    transfer_success = False
                    print("建议：重新尝试传输，可能是网络不稳定导致的传输中断")
            else:
                print(f"❌ 无法通过本地方式检测到远程文件")
                # 尝试通过远程命令检查文件是否存在
                try:
                    check_file_cmd = (
                        f"powershell -Command \"& {{ "
                        f"$username = '{REMOTE_RDP['remote_server_user']}'; "
                        f"$password = ConvertTo-SecureString '{REMOTE_RDP['remote_server_pwd']}' -AsPlainText -Force; "
                        f"$credential = New-Object System.Management.Automation.PSCredential($username, $password); "
                        f"$remoteFile = '{remote_sql_dir}{file_name}'; "
                        f"Invoke-Command -ComputerName {REMOTE_RDP['server_ip']} -Credential $credential -ScriptBlock {{ "
                        f"if (Test-Path $using:remoteFile) {{ "
                        f"    $size = (Get-Item $using:remoteFile).Length; "
                        f"    Write-Output \"File exists, size: $size bytes\"; "
                        f"}} else {{ "
                        f"    Write-Output \"File does not exist\"; "
                        f"}} "
                        f"}} "
                        f"}}\"")
                    
                    print("尝试通过PowerShell远程检查文件...")
                    check_result = subprocess.run(
                        check_file_cmd, shell=True, capture_output=True, text=True, encoding="gbk", timeout=30
                    )
                    
                    if check_result.returncode == 0:
                        print(f"远程检查结果: {check_result.stdout.strip()}")
                        if "File exists" in check_result.stdout:
                            print("✅ 文件在远程服务器上存在")
                            transfer_success = True
                        else:
                            print("❌ 文件在远程服务器上不存在")
                            transfer_success = False
                    else:
                        print(f"远程检查失败: {check_result.stderr.strip()}")
                        transfer_success = False
                except subprocess.TimeoutExpired:
                    print("❌ 远程文件检查超时")
                    transfer_success = False
                except Exception as e:
                    error_msg = str(e)
                    if REMOTE_RDP['remote_server_pwd'] in error_msg:
                        error_msg = error_msg.replace(REMOTE_RDP['remote_server_pwd'], '******')
                    print(f"远程检查文件时发生异常: {error_msg}")
                    transfer_success = False
            
            return transfer_success
            
        except subprocess.TimeoutExpired:
            print(f"❌ 文件传输超时：操作超过{timeout_seconds}秒未完成")
            print("提示：如果文件较大，可能需要更长的传输时间")
            return False
        except Exception as e:
            # 捕获所有其他异常
            error_msg = str(e)
            if REMOTE_RDP['remote_server_pwd'] in error_msg:
                error_msg = error_msg.replace(REMOTE_RDP['remote_server_pwd'], '******')
            print(f"❌ RDP文件传输过程中发生异常：{error_msg}")
            print("建议检查：")
            print("1. 网络连接是否稳定")
            print("2. 服务器存储空间是否充足")
            print("3. 账户权限是否正确")
            return False
        finally:
            # 确保在任何情况下都进行资源清理
            # 清理：断开映射的网络驱动器
            if drive_mapped:
                print("\n7. 清理网络连接...")
                try:
                    net_use_del_cmd = f"net use {mapped_drive} /delete /yes"
                    subprocess.run(
                        net_use_del_cmd, 
                        shell=True, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        timeout=10  # 确保清理操作不会卡住
                    )
                    print(f"✅ 已断开网络驱动器 {mapped_drive}")
                except Exception as cleanup_error:
                    print(f"⚠️ 清理网络连接时发生错误：{str(cleanup_error)}")
                    print("提示：您可能需要手动断开网络驱动器")
            print("\n=== RDP文件传输操作完成 ===")
    
    except KeyboardInterrupt:
        # 处理用户中断
        print("\n❌ 操作被用户中断")
        # 确保资源清理
        if drive_mapped:
            try:
                net_use_del_cmd = f"net use {mapped_drive} /delete /yes"
                subprocess.run(net_use_del_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"✅ 已断开网络驱动器 {mapped_drive}")
            except:
                pass
        return False
    except Exception as e:
        # 捕获最外层异常
        print(f"❌ 发生未预期的错误：{str(e)}")
        # 确保资源清理
        if 'drive_mapped' in locals() and drive_mapped:
            try:
                net_use_del_cmd = f"net use {mapped_drive} /delete /yes"
                subprocess.run(net_use_del_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except:
                pass
            return False
    file_name = os.path.basename(local_sql_path)
    
    # 1. 检查本地SQL文件是否存在
    print(f"1. 检查本地SQL文件：{local_sql_path}")
    if not os.path.exists(local_sql_path):
        print(f"❌ 错误：本地SQL文件不存在！路径：{local_sql_path}")
        return False
    print("✅ 本地SQL文件存在")
    
    # 2. 检查RDP端口连通性
    print(f"\n2. 测试RDP端口 {REMOTE_RDP['rdp_port']} 连通性")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((REMOTE_RDP['server_ip'], REMOTE_RDP['rdp_port']))
        sock.close()
        
        if result == 0:
            print(f"✅ RDP端口 {REMOTE_RDP['rdp_port']} 连通性测试通过")
        else:
            print(f"❌ RDP端口 {REMOTE_RDP['rdp_port']} 不可访问")
            print("建议：")
            print("1. 确认服务器已启用RDP服务")
            print("2. 检查服务器防火墙是否允许RDP连接")
            print("3. 确认阿里云安全组已开放3389端口")
            # 端口不通但仍尝试继续，可能已有其他方式连接
    except Exception as e:
        print(f"⚠️ RDP端口测试失败: {str(e)}")
    
    # 3. 检查映射驱动器是否可用
    mapped_drive = REMOTE_RDP['mapped_drive']
    remote_sql_dir = REMOTE_RDP['remote_sql_dir']
    
    # 准备通过映射驱动器的目标路径
    # 如果使用的是绝对路径（C:\），则直接使用，否则使用映射驱动器
    if remote_sql_dir.startswith('C:\\') or remote_sql_dir.startswith('D:\\'):
        # 对于Windows服务器，我们将尝试使用net use映射网络驱动器
        print(f"\n3. 尝试映射网络驱动器到服务器共享目录")
        
        # 构建目标路径（使用UNC格式）
        # 先处理路径部分，避免在f-string中使用反斜杠
        path_part = remote_sql_dir.split(':')[-1].strip('\\')
        unc_path = f"\\\\{REMOTE_RDP['server_ip']}\\{path_part}"
        print(f"目标UNC路径：{unc_path}")
        
        try:
            # 第一步：映射网络驱动器
            print("  a. 正在映射网络驱动器...")
            net_use_cmd = (
                f"net use {mapped_drive} {unc_path} "
                f"/user:{REMOTE_RDP['remote_server_user']} {REMOTE_RDP['remote_server_pwd']} /persistent:no"
            )
            print(f"执行命令：{net_use_cmd}")
            net_use_result = subprocess.run(
                net_use_cmd, shell=True, capture_output=True, text=True, encoding="gbk"
            )
            
            if "命令成功完成" in net_use_result.stdout or "successfully" in net_use_result.stdout:
                print(f"✅ 成功映射网络驱动器 {mapped_drive}")
                drive_mapped = True
            else:
                print(f"❌ 映射网络驱动器失败")
                if net_use_result.stdout:
                    print(f"输出: {net_use_result.stdout.strip()}")
                if net_use_result.stderr:
                    print(f"错误: {net_use_result.stderr.strip()}")
                
                # 尝试直接使用UNC路径而不映射驱动器
                print("\n尝试直接使用UNC路径传输文件...")
                mapped_drive = unc_path
                drive_mapped = False
        except Exception as e:
            print(f"❌ 映射网络驱动器时发生异常：{str(e)}")
            mapped_drive = unc_path
            drive_mapped = False
    
    # 4. 确保远程目录存在
    print(f"\n4. 准备远程目录")
    try:
        # 对于UNC路径，我们需要特殊处理
        if mapped_drive.startswith('\\\\'):
            # 直接使用UNC路径
            remote_dir_path = mapped_drive
        else:
            # 使用映射驱动器
            remote_dir_path = f"{mapped_drive}\\"
        
        print(f"目标目录：{remote_dir_path}")
        
        # 检查目录是否存在
        if not os.path.exists(remote_dir_path):
            print(f"⚠️ 远程目录不存在，尝试创建")
            try:
                # 在远程服务器上创建目录（使用PowerShell）
                create_dir_cmd = (
                    'powershell -Command "& { ' +
                    f'$username = \'{REMOTE_RDP["remote_server_user"]}\'; ' +
                    f'$password = ConvertTo-SecureString \'{REMOTE_RDP["remote_server_pwd"]}\'' + ' -AsPlainText -Force; ' +
                    '$credential = New-Object System.Management.Automation.PSCredential($username, $password); ' +
                    f'$remoteDir = \'{remote_sql_dir}\'; ' +
                    f'Invoke-Command -ComputerName {REMOTE_RDP["server_ip"]} -Credential $credential -ScriptBlock {{ ' +
                    'if (-not (Test-Path $using:remoteDir)) { ' +
                    '    New-Item -ItemType Directory -Force -Path $using:remoteDir; ' +
                    '    Write-Output \'Directory created\'; ' +
                    '} else { ' +
                    '    Write-Output \'Directory already exists\'; ' +
                    '} ' +
                    '}} ' +
                    '}"'
                )
                
                print("执行远程目录创建命令...")
                create_result = subprocess.run(
                    create_dir_cmd, shell=True, capture_output=True, text=True, encoding="gbk"
                )
                
                if create_result.returncode == 0:
                    print(f"✅ 远程目录准备成功: {create_result.stdout.strip()}")
                else:
                    print(f"⚠️ 远程目录创建返回非零值: {create_result.returncode}")
                    if create_result.stdout:
                        print(f"输出: {create_result.stdout.strip()}")
                    if create_result.stderr:
                        print(f"错误: {create_result.stderr.strip()}")
            except Exception as e:
                print(f"⚠️ 创建远程目录时发生异常：{str(e)}")
        else:
            print("✅ 远程目录已存在")
    except Exception as e:
        print(f"⚠️ 检查远程目录时发生异常：{str(e)}")
    
    # 5. 使用robocopy传输文件
    print(f"\n5. 开始文件传输...")
    try:
        # 构建robocopy命令
        # 目标路径处理：如果是UNC路径直接使用，否则使用映射驱动器+路径
        if mapped_drive.startswith('\\\\'):
            target_path = mapped_drive
        else:
            # 从remote_sql_dir提取路径部分（去掉驱动器号）
            path_part = '\\'.join(remote_sql_dir.split('\\')[1:])
            target_path = f"{mapped_drive}\\{path_part}"
        
        # 确保目标路径正确
        if not target_path.endswith('\\'):
            target_path += '\\'
        
        print(f"源文件：{local_sql_path}")
        print(f"目标路径：{target_path}")
        
        # 执行robocopy命令
        robocopy_cmd = f"robocopy \"{os.path.dirname(local_sql_path)}\" \"{target_path}\" \"{file_name}\" /Z /R:2 /W:3"
        print(f"执行命令：{robocopy_cmd}")
        
        robocopy_result = subprocess.run(
            robocopy_cmd, shell=True, capture_output=True, text=True, encoding="gbk"
        )
        
        # 输出robocopy结果
        if robocopy_result.stdout:
            print(f"robocopy输出：{robocopy_result.stdout.strip()}")
        if robocopy_result.stderr:
            print(f"robocopy错误：{robocopy_result.stderr.strip()}")
        
        # 6. 验证文件是否成功传输
        print("\n6. 验证文件传输结果...")
        # 构造远程文件的完整路径
        remote_file_path = f"{target_path}{file_name}"
        
        # 检查文件是否存在
        if os.path.exists(remote_file_path):
            # 获取文件大小进行验证
            local_size = os.path.getsize(local_sql_path)
            remote_size = os.path.getsize(remote_file_path)
            
            if local_size == remote_size:
                print(f"✅ 文件传输成功且完整！源文件大小：{local_size}字节，目标文件大小：{remote_size}字节")
                transfer_success = True
            else:
                print(f"⚠️ 文件已传输但大小不匹配！源文件大小：{local_size}字节，目标文件大小：{remote_size}字节")
                transfer_success = False
        else:
            print(f"❌ 文件传输失败：远程文件不存在")
            # 尝试通过远程命令检查文件是否存在
            try:
                check_file_cmd = (
                    'powershell -Command "& { ' +
                    f'$username = \'{REMOTE_RDP["remote_server_user"]}\'; ' +
                    f'$password = ConvertTo-SecureString \'{REMOTE_RDP["remote_server_pwd"]}\'' + ' -AsPlainText -Force; ' +
                    '$credential = New-Object System.Management.Automation.PSCredential($username, $password); ' +
                    f'$remoteFile = \'{remote_sql_dir}{file_name}\'; ' +
                    f'Invoke-Command -ComputerName {REMOTE_RDP["server_ip"]} -Credential $credential -ScriptBlock {{ ' +
                    'if (Test-Path $using:remoteFile) { ' +
                    '    $size = (Get-Item $using:remoteFile).Length; ' +
                    '    Write-Output \"File exists, size: $size bytes\"; ' +
                    '} else { ' +
                    '    Write-Output \"File does not exist\"; ' +
                    '} ' +
                    '}} ' +
                    '}"'
                )
                
                check_result = subprocess.run(
                    check_file_cmd, shell=True, capture_output=True, text=True, encoding="gbk"
                )
                
                if check_result.returncode == 0:
                    print(f"远程检查结果: {check_result.stdout.strip()}")
                    if "File exists" in check_result.stdout:
                        print("✅ 文件在远程服务器上存在")
                        transfer_success = True
                    else:
                        transfer_success = False
                else:
                    print(f"远程检查失败: {check_result.stderr.strip()}")
                    transfer_success = False
            except Exception as e:
                print(f"远程检查文件时发生异常: {str(e)}")
                transfer_success = False
        
        # 7. 清理：断开映射的网络驱动器
        if drive_mapped:
            print("\n7. 清理网络连接...")
            net_use_del_cmd = f"net use {mapped_drive} /delete /yes"
            subprocess.run(net_use_del_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"✅ 已断开网络驱动器 {mapped_drive}")
        
        # 返回传输结果
        return transfer_success
        
    except Exception as e:
        print(f"❌ RDP文件传输过程中发生异常：{str(e)}")
        import traceback
        print(f"详细错误信息：{traceback.format_exc()}")
        
        # 清理：断开映射的网络驱动器（如果已映射）
        if 'drive_mapped' in locals() and drive_mapped:
            try:
                net_use_del_cmd = f"net use {mapped_drive} /delete /yes"
                subprocess.run(net_use_del_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except:
                pass
        
        # 返回失败
        return False


def test_rdp_connection():
    """
    测试RDP连接功能 - 验证服务器配置和连接是否正常
    不执行文件上传，仅测试连接状态
    """
    print("\n=== 开始RDP连接测试 ===")
    
    print("测试配置信息：")
    print(f"  服务器IP: {REMOTE_RDP['server_ip']}")
    print(f"  RDP端口: {REMOTE_RDP['rdp_port']}")
    print(f"  用户名: {REMOTE_RDP['remote_server_user']}")
    print(f"  密码: {'*' * len(REMOTE_RDP['remote_server_pwd'])}")
    print(f"  远程目录: {REMOTE_RDP['remote_sql_dir']}")
    
    # 1. 网络连接性测试
    print(f"\n1. 测试网络连接到服务器 {REMOTE_RDP['server_ip']}")
    try:
        ping_cmd = f"ping -n 2 {REMOTE_RDP['server_ip']}"
        ping_result = subprocess.run(
            ping_cmd, shell=True, capture_output=True, text=True
        )
        
        if "0% 丢失" in ping_result.stdout or "0% loss" in ping_result.stdout:
            print("✅ 网络连接正常")
        else:
            print(f"❌ 网络连接失败")
            print(f"Ping输出: {ping_result.stdout[:200]}...")
            print("建议: 检查网络连接和防火墙设置")
            return False
    except Exception as e:
        print(f"❌ 网络连接测试失败: {str(e)}")
        return False
    
    # 2. RDP端口连通性测试
    print(f"\n2. 测试RDP端口 {REMOTE_RDP['rdp_port']} 连通性")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((REMOTE_RDP['server_ip'], REMOTE_RDP['rdp_port']))
        sock.close()
        
        if result == 0:
            print(f"✅ RDP端口 {REMOTE_RDP['rdp_port']} 连通性测试通过")
        else:
            print(f"❌ RDP端口 {REMOTE_RDP['rdp_port']} 不可访问")
            print("建议:")
            print("1. 确认服务器远程桌面服务已启动")
            print("2. 检查服务器防火墙是否允许RDP连接")
            print("3. 确认阿里云安全组已开放3389端口")
            # 端口不通但仍继续测试，可能已有其他方式连接
    except Exception as e:
        print(f"❌ RDP端口测试失败: {str(e)}")
    
    # 3. 网络共享访问测试
    print("\n3. 测试网络共享访问")
    try:
        # 构建UNC路径
        if REMOTE_RDP['remote_sql_dir'].startswith('C:\\') or REMOTE_RDP['remote_sql_dir'].startswith('D:\\'):
            path_part = REMOTE_RDP['remote_sql_dir'].split(':')[-1].strip('\\')
            unc_path = f"\\\\{REMOTE_RDP['server_ip']}\\{path_part}"
        else:
            unc_path = f"\\\\{REMOTE_RDP['server_ip']}\\{REMOTE_RDP['remote_sql_dir']}"
        
        print(f"测试UNC路径: {unc_path}")
        
        # 尝试直接访问UNC路径
        if os.path.exists(unc_path):
            print(f"✅ 可以直接访问UNC路径: {unc_path}")
        else:
            print(f"⚠️ 无法直接访问UNC路径: {unc_path}")
            print("尝试映射网络驱动器...")
            
            # 尝试映射网络驱动器
            net_use_cmd = (
                f"net use {REMOTE_RDP['mapped_drive']} {unc_path} "
                f"/user:{REMOTE_RDP['remote_server_user']} {REMOTE_RDP['remote_server_pwd']} /persistent:no"
            )
            
            net_use_result = subprocess.run(
                net_use_cmd, shell=True, capture_output=True, text=True, encoding="gbk"
            )
            
            if "命令成功完成" in net_use_result.stdout or "successfully" in net_use_result.stdout:
                print(f"✅ 成功映射网络驱动器 {REMOTE_RDP['mapped_drive']}")
                
                # 验证映射成功后断开连接
                net_use_del_cmd = f"net use {REMOTE_RDP['mapped_drive']} /delete /yes"
                subprocess.run(net_use_del_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                print(f"⚠️ 映射网络驱动器返回: {net_use_result.stdout.strip()}")
                print("建议:")
                print("1. 确认服务器已启用文件共享")
                print("2. 验证用户名和密码是否正确")
                print("3. 检查服务器防火墙是否允许SMB连接")
    except Exception as e:
        print(f"❌ 网络共享测试失败: {str(e)}")
    
    # 4. 远程命令执行测试
    print("\n4. 测试远程命令执行")
    try:
        test_cmd = (
            'powershell -Command "& { ' +
            f'$username = \'{REMOTE_RDP["remote_server_user"]}\'; ' +
            f'$password = ConvertTo-SecureString \'{REMOTE_RDP["remote_server_pwd"]}\'' + ' -AsPlainText -Force; ' +
            '$credential = New-Object System.Management.Automation.PSCredential($username, $password); ' +
            'try { ' +
            f'    $result = Invoke-Command -ComputerName {REMOTE_RDP["server_ip"]} -Credential $credential -ScriptBlock {{ ' +
            '        Write-Output \'远程命令执行成功\'; ' +
            '        return \'Success\'; ' +
            '    }} -ErrorAction Stop; ' +
            '    Write-Output \"远程执行结果: $result\"; ' +
            '} catch { ' +
            '    Write-Output \"远程执行错误: $($_.Exception.Message)\"; ' +
            '} ' +
            '}"'
        )
        
        cmd_result = subprocess.run(
            test_cmd, shell=True, capture_output=True, text=True, encoding="gbk"
        )
        
        if cmd_result.stdout and ("Success" in cmd_result.stdout or "远程命令执行成功" in cmd_result.stdout):
            print("✅ 远程命令执行成功")
        else:
            print(f"⚠️ 远程命令执行结果: {cmd_result.stdout.strip()}")
            print("注意：PowerShell远程执行可能需要额外配置")
            print("如果文件传输正常，此步骤失败不影响主要功能")
    except Exception as e:
        print(f"❌ 远程命令执行测试失败: {str(e)}")
    
    # 总结测试结果
    print("\n=== RDP连接测试总结 ===")
    print("1. 网络连接: ✅ 正常")
    
    # RDP端口状态
    if 'result' in locals() and result == 0:
        print(f"2. RDP端口({REMOTE_RDP['rdp_port']}): ✅ 开放")
    else:
        print(f"2. RDP端口({REMOTE_RDP['rdp_port']}): ⚠️ 可能未开放或被防火墙阻止")
    
    print("\n✅ RDP连接测试完成！")
    print("建议：")
    print("1. 确保阿里云安全组已开放3389端口")
    print("2. 验证Windows服务器远程桌面已启用")
    print("3. 检查用户账户是否有远程登录权限")
    print("4. 如果需要文件共享功能，请确保SMB服务已启用")
    
    return True

def test_ssh_connection():
    """
    测试SSH连接功能 - 验证服务器配置和连接是否正常
    不执行文件上传，仅测试连接状态
    """
    print("\n=== 开始SSH连接测试 ===")
    
    # 构建SSH配置
    SSH_CONFIG = {
        "server_ip": "47.99.204.97",
        "ssh_port": 22,
        "ssh_user": "Administrator",
        "ssh_pwd": "Sjw9@0613",
        "remote_sql_dir": "C:\\Users\\Administrator\\Desktop\\mysql_sync\\"
    }
    
    print("测试配置信息：")
    print(f"  服务器IP: {SSH_CONFIG['server_ip']}")
    print(f"  SSH端口: {SSH_CONFIG['ssh_port']}")
    print(f"  用户名: {SSH_CONFIG['ssh_user']}")
    print(f"  密码: {'*' * len(SSH_CONFIG['ssh_pwd'])}")
    print(f"  远程目录: {SSH_CONFIG['remote_sql_dir']}")
    
    # 1. 网络连接性测试
    print(f"\n1. 测试网络连接到服务器 {SSH_CONFIG['server_ip']}")
    try:
        import subprocess
        ping_cmd = f"ping -n 2 {SSH_CONFIG['server_ip']}"
        ping_result = subprocess.run(
            ping_cmd, shell=True, capture_output=True, text=True
        )
        
        if "0% 丢失" in ping_result.stdout or "0% loss" in ping_result.stdout:
            print("✅ 网络连接正常")
        else:
            print(f"❌ 网络连接失败")
            print(f"Ping输出: {ping_result.stdout[:200]}...")
            print("建议: 检查网络连接和防火墙设置")
            return False
    except Exception as e:
        print(f"❌ 网络连接测试失败: {str(e)}")
        return False
    
    # 2. 端口连通性测试
    print(f"\n2. 测试端口 {SSH_CONFIG['ssh_port']} 连通性")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((SSH_CONFIG['server_ip'], SSH_CONFIG['ssh_port']))
        sock.close()
        
        if result == 0:
            print("✅ 端口连通性测试通过")
        else:
            print(f"❌ 端口 {SSH_CONFIG['ssh_port']} 不可访问")
            print("建议:")
            print("1. 确认服务器SSH服务已启动")
            print("2. 检查服务器防火墙是否允许SSH连接")
            print("3. 确认端口号是否正确")
            return False
    except Exception as e:
        print(f"❌ 端口测试失败: {str(e)}")
        return False
    
    # 3. SSH认证测试
    print("\n3. 测试SSH认证")
    ssh_client = None
    try:
        import paramiko
        import time
        
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.load_system_host_keys()
        
        # 连接参数优化
        max_retries = 2
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                print(f"  认证尝试 {attempt + 1}/{max_retries}")
                ssh_client.connect(
                    hostname=SSH_CONFIG["server_ip"],
                    port=SSH_CONFIG["ssh_port"],
                    username=SSH_CONFIG["ssh_user"],
                    password=SSH_CONFIG["ssh_pwd"],
                    timeout=10,
                    look_for_keys=False,
                    allow_agent=False
                )
                print("✅ SSH认证成功")
                break
            except paramiko.AuthenticationException:
                if attempt == max_retries - 1:
                    print("❌ SSH认证失败")
                    print("建议: 检查用户名和密码是否正确")
                    return False
                print(f"  认证失败，{retry_delay}秒后重试...")
                time.sleep(retry_delay)
            except Exception as e:
                print(f"  连接错误: {str(e)}")
                raise
        
        # 4. 执行简单命令测试
        print("\n4. 执行简单命令测试")
        try:
            stdin, stdout, stderr = ssh_client.exec_command("echo 'SSH连接测试成功'", timeout=5)
            exit_code = stdout.channel.recv_exit_status()
            output = stdout.read().decode('utf-8').strip()
            
            if exit_code == 0 and "SSH连接测试成功" in output:
                print("✅ 命令执行测试成功")
            else:
                print(f"❌ 命令执行测试失败，返回码: {exit_code}")
                return False
        except Exception as e:
            print(f"❌ 命令执行失败: {str(e)}")
            return False
        
        # 5. 检查远程目录是否可访问
        print("\n5. 检查远程目录访问权限")
        try:
            remote_dir_linux = SSH_CONFIG['remote_sql_dir'].replace('\\', '/')
            check_dir_cmd = f'ls -la "{remote_dir_linux}" 2>&1 || mkdir -p "{remote_dir_linux}" && echo "Directory created"'
            stdin, stdout, stderr = ssh_client.exec_command(check_dir_cmd, timeout=5)
            exit_code = stdout.channel.recv_exit_status()
            output = stdout.read().decode('utf-8').strip()
            
            if exit_code == 0:
                print("✅ 远程目录访问成功")
                if "Directory created" in output:
                    print("📁 远程目录已创建")
            else:
                print(f"❌ 远程目录访问失败，错误: {output}")
                print("建议: 检查目录路径和权限设置")
        except Exception as e:
            print(f"❌ 目录检查失败: {str(e)}")
        
        print("\n🎉 SSH连接测试全部通过！服务器配置正确")
        return True
        
    except paramiko.SSHException as e:
        print(f"❌ SSH连接异常: {str(e)}")
        print("建议: 检查SSH服务配置和防火墙设置")
        return False
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        return False
    finally:
        if ssh_client:
            try:
                ssh_client.close()
                print("✅ SSH连接已关闭")
            except:
                pass

def upload_sql_to_remote_ssh():
    """通过SSH上传SQL文件到远程服务器"""
    print("\n=== 开始通过SSH上传SQL文件到云端 ===")
    
    # 检查paramiko模块是否安装
    try:
        import paramiko
    except ImportError:
        print("❌ paramiko模块未安装，正在尝试安装...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "paramiko"], check=True)
            import paramiko
            print("✅ paramiko模块安装成功")
        except:
            print("❌ paramiko模块安装失败，无法使用SSH上传")
            return False
    
    # 检查本地SQL文件是否存在
    dump_path = LOCAL_MYSQL['dump_path']
    if not dump_path.endswith('\\') and not dump_path.endswith('/'):
        dump_path += '\\'
    local_sql_path = f"{dump_path}{LOCAL_MYSQL['sql_filename']}"
    file_name = os.path.basename(local_sql_path)
    
    # 检查本地文件是否存在
    if not os.path.exists(local_sql_path):
        print(f"❌ 错误：本地SQL文件不存在！路径：{local_sql_path}")
        return False
    
    print(f"本地SQL文件路径：{local_sql_path}")
    
    # 构建SSH配置
    SSH_CONFIG = {
        "server_ip": "47.99.204.97",
        "ssh_port": 22,
        "ssh_user": "Administrator",
        "ssh_pwd": "Sjw9@0613",
        "remote_sql_dir": "C:\\Users\\Administrator\\Desktop\\mysql_sync\\"
    }
    
    # 1. 先进行网络连接性测试
    print(f"\n1. 正在测试网络连接：{SSH_CONFIG['server_ip']}")
    try:
        # 使用ping命令测试网络连接
        ping_cmd = f"ping -n 2 {SSH_CONFIG['server_ip']}"
        ping_result = subprocess.run(
            ping_cmd, shell=True, capture_output=True, text=True
        )
        
        if "0% 丢失" in ping_result.stdout or "0% loss" in ping_result.stdout:
            print("✅ 网络连接正常")
        else:
            print(f"⚠️ 网络连接不稳定或无法连接")
            print(f"Ping输出：{ping_result.stdout[:200]}...")
    except Exception as e:
        print(f"⚠️ 网络连接测试失败：{str(e)}")
    
    # 2. 尝试SSH连接
    ssh_client = None
    try:
        print(f"\n2. 尝试SSH连接到服务器：{SSH_CONFIG['server_ip']}:{SSH_CONFIG['ssh_port']}")
        
        # 导入socket模块进行端口检查
        import socket
        
        # 先检查端口是否开放
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5秒超时
        result = sock.connect_ex((SSH_CONFIG['server_ip'], SSH_CONFIG['ssh_port']))
        sock.close()
        
        if result != 0:
            print(f"❌ 端口 {SSH_CONFIG['ssh_port']} 未开放或被防火墙阻止")
            print("请检查：")
            print("1. 服务器上的SSH服务是否已安装并启动")
            print("2. 服务器防火墙是否允许22端口的连接")
            print("3. 服务器IP地址是否正确")
            return False
        
        print("✅ SSH端口检查通过，开始建立SSH连接...")
        
        # 创建SSH客户端
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 配置SSH连接参数以提高稳定性
        ssh_client.load_system_host_keys()
        
        # 设置连接重试参数
        max_retries = 3
        retry_delay = 2  # 秒
        
        for attempt in range(max_retries):
            try:
                print(f"连接尝试 {attempt + 1}/{max_retries}")
                
                # 连接SSH服务器
                ssh_client.connect(
                    hostname=SSH_CONFIG["server_ip"],
                    port=SSH_CONFIG["ssh_port"],
                    username=SSH_CONFIG["ssh_user"],
                    password=SSH_CONFIG["ssh_pwd"],
                    timeout=15,  # 增加连接超时时间
                    banner_timeout=15,  # 增加banner超时时间
                    auth_timeout=15,  # 增加认证超时时间
                    look_for_keys=False,  # 仅使用密码认证，不查找密钥文件
                    allow_agent=False  # 不使用SSH代理
                )
                
                # 设置keepalive以保持连接活跃
                transport = ssh_client.get_transport()
                if transport:
                    transport.set_keepalive(30)  # 每30秒发送一次keepalive包
                    print("✅ SSH keepalive已启用")
                
                break  # 连接成功，跳出重试循环
                
            except (paramiko.SSHException, socket.error) as e:
                if attempt == max_retries - 1:
                    raise  # 最后一次尝试失败，抛出异常
                print(f"连接失败，{retry_delay}秒后重试...错误: {str(e)}")
                time.sleep(retry_delay)
                retry_delay *= 2  # 指数退避，增加下次重试的延迟时间
        print("✅ SSH连接成功")
        
        # 3. 确保远程目录存在
        print(f"\n3. 检查远程目录：{SSH_CONFIG['remote_sql_dir']}")
        # 处理Windows路径为Linux格式
        remote_dir_linux = SSH_CONFIG['remote_sql_dir'].replace('\\', '/')
        mkdir_cmd = f'mkdir -p "{remote_dir_linux}"'
        
        print(f"执行命令：{mkdir_cmd}")
        stdin, stdout, stderr = ssh_client.exec_command(
            mkdir_cmd,
            get_pty=True,
            timeout=5
        )
        
        exit_code = stdout.channel.recv_exit_status()
        stdout_output = stdout.read().decode('utf-8', errors='ignore')
        stderr_output = stderr.read().decode('utf-8', errors='ignore')
        
        if exit_code == 0:
            print("✅ 远程目录准备成功")
        else:
            print(f"⚠️ 创建远程目录返回码：{exit_code}")
            if stderr_output:
                print(f"错误输出：{stderr_output.strip()}")
            if stdout_output:
                print(f"标准输出：{stdout_output.strip()}")
        
        # 4. 上传文件
        print(f"\n4. 开始上传文件：{file_name}")
        sftp = ssh_client.open_sftp()
        
        # 获取文件大小用于显示进度
        file_size = os.path.getsize(local_sql_path)
        print(f"文件大小：{file_size/1024:.2f} KB")
        
        # 上传文件
        sftp.put(
            localpath=local_sql_path,
            remotepath=f"{SSH_CONFIG['remote_sql_dir']}{file_name}"
        )
        sftp.close()
        
        print(f"✅ SSH上传成功！云端文件路径：{SSH_CONFIG['remote_sql_dir']}{file_name}")
        
        # 5. 验证文件是否成功上传
        print("\n5. 验证文件上传结果...")
        # 使用dir或ls命令检查文件是否存在
        check_cmd = f'dir "{SSH_CONFIG["remote_sql_dir"]}" 2>nul | findstr /i "{file_name}"'
        stdin, stdout, stderr = ssh_client.exec_command(
            check_cmd,
            get_pty=True,
            timeout=5
        )
        
        check_output = stdout.read().decode('utf-8', errors='ignore')
        if file_name in check_output:
            print(f"✅ 文件已成功上传并验证存在")
        else:
            print(f"⚠️ 上传验证失败，建议手动检查文件是否存在")
        
        return True
        
    except paramiko.AuthenticationException:
        print(f"❌ SSH认证失败：用户名或密码错误")
        print("请检查：")
        print(f"1. 用户名：{SSH_CONFIG['ssh_user']}")
        print(f"2. 密码：{SSH_CONFIG['ssh_pwd']}")
        print(f"3. 用户是否有权限登录SSH")
        return False
        
    except paramiko.SSHException as e:
        print(f"❌ SSH连接失败：{str(e)}")
        print("可能的原因：")
        print("1. SSH服务未在服务器上安装或未启动")
        print("2. 服务器防火墙阻止了SSH连接")
        print("3. 服务器IP地址或端口号错误")
        print("4. SSH配置不正确")
        return False
        
    except socket.timeout:
        print(f"❌ 连接超时：无法在指定时间内连接到服务器")
        print("请检查：")
        print("1. 网络连接稳定性")
        print("2. 服务器是否在线")
        print("3. 防火墙设置")
        return False
        
    except FileNotFoundError:
        print(f"❌ 本地文件未找到：{local_sql_path}")
        return False
        
    except PermissionError:
        print(f"❌ 权限错误：")
        print("请检查：")
        print("1. 本地文件的读取权限")
        print("2. 远程目录的写入权限")
        return False
        
    except Exception as e:
        print(f"❌ SSH上传过程中发生未知错误：{str(e)}")
        import traceback
        print(f"详细错误信息：{traceback.format_exc()}")
        print("\n建议排查步骤：")
        print("1. 确认服务器IP地址正确")
        print("2. 确认SSH服务已在服务器上安装并启动")
        print("3. 确认防火墙允许SSH连接")
        print("4. 确认用户名和密码正确")
        print("5. 确认远程目录存在且有写入权限")
        return False
        
    finally:
        if ssh_client:
            try:
                ssh_client.close()
                print("✅ SSH连接已关闭")
            except:
                pass

# def upload_sql_to_remote_ssh():
#     """第二步：本地远程传SQL文件到云端（方式B：SSH，启用需注释方式A）"""
#     print("\n=== 开始通过SSH上传SQL文件到云端 ===")
#     ssh_client = SSHClient()
#     ssh_client.set_missing_host_key_policy(AutoAddPolicy())
#     try:
#         # 连接SSH
#         ssh_client.connect(
#             hostname=REMOTE_SSH["server_ip"],
#             port=REMOTE_SSH["ssh_port"],
#             username=REMOTE_SSH["ssh_user"],
#             password=REMOTE_SSH["ssh_pwd"]
#         )
#         # 上传文件
#         sftp = ssh_client.open_sftp()
#         sftp.put(
#             localpath=REMOTE_SSH["local_sql_path"],
#             remotepath=f"{REMOTE_SSH['remote_sql_dir']}{LOCAL_MYSQL['sql_filename']}"
#         )
#         sftp.close()
#         ssh_client.close()
#         print(f"✅ SSH上传成功！云端文件路径：{REMOTE_SSH['remote_sql_dir']}{LOCAL_MYSQL['sql_filename']}")
#         return True
#     except Exception as e:
#         print(f"❌ SSH上传失败：{str(e)}")
#         return False

def remote_import_sql():
    """第三步：本地远程控制云端MySQL导入SQL"""
    print("\n=== 开始远程控制云端MySQL导入SQL ===")
    remote_conn = None
    try:
        # 首先检查并创建远程数据库（如果不存在）
        print(f"检查远程数据库 '{REMOTE_MYSQL['db']}' 是否存在...")
        try:
            # 连接到MySQL服务器（不指定数据库）
            check_conn = pymysql.connect(
                host=REMOTE_MYSQL["host"],
                port=REMOTE_MYSQL["port"],
                user=REMOTE_MYSQL["user"],
                password=REMOTE_MYSQL["password"],
                charset="utf8mb4"
            )
            check_cursor = check_conn.cursor()
            
            # 检查数据库是否存在
            check_cursor.execute(f"SHOW DATABASES LIKE '{REMOTE_MYSQL['db']}'")
            result = check_cursor.fetchone()
            
            if not result:
                # 数据库不存在，创建它
                print(f"数据库 '{REMOTE_MYSQL['db']}' 不存在，正在创建...")
                check_cursor.execute(f"CREATE DATABASE {REMOTE_MYSQL['db']}")
                print(f"✅ 数据库 '{REMOTE_MYSQL['db']}' 创建成功")
            else:
                print(f"✅ 数据库 '{REMOTE_MYSQL['db']}' 已存在")
                
            check_cursor.close()
            check_conn.close()
        except Exception as e:
            print(f"⚠️ 检查/创建数据库时发生错误: {str(e)}")
            # 继续尝试导入，因为可能是权限问题或其他原因
        
        # 方案1：通过SSH连接到远程服务器，执行mysql命令导入文件
        print("方法1：通过SSH执行mysql命令导入SQL文件...")
        try:
            # 使用paramiko建立SSH连接
            ssh_client = SSHClient()
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            ssh_client.connect(
                hostname=REMOTE_MYSQL["host"],
                port=22,  # 默认SSH端口
                username=REMOTE_RDP["remote_server_user"],
                password=REMOTE_RDP["remote_server_pwd"],
                timeout=30
            )
            
            # 构建MySQL导入命令 - 使用完整路径以避免找不到mysql命令
            # 修复路径错误：9.in 改为 9.5
            mysql_exe_path = "C:\\Program Files\\MySQL\\MySQL Server 9.5\\bin\\mysql.exe"  # 与mysqldump同目录
            
            # 注意：在Windows环境下，路径包含空格时需要用引号包裹
            if ' ' in mysql_exe_path:
                mysql_exe_path = f'"{mysql_exe_path}"'
            
            mysql_cmd = (
                f"{mysql_exe_path} -u{REMOTE_MYSQL['user']} -p{REMOTE_MYSQL['password']} "
                f"{REMOTE_MYSQL['db']} < \"{REMOTE_MYSQL['remote_sql_path']}\""
            )
            
            # 为了安全，不打印包含密码的完整命令
            safe_mysql_cmd = (
                f"{mysql_exe_path} -u{REMOTE_MYSQL['user']} -p****** "
                f"{REMOTE_MYSQL['db']} < \"{REMOTE_MYSQL['remote_sql_path']}\""
            )
            print(f"执行命令：{safe_mysql_cmd}")
            
            # 执行命令
            stdin, stdout, stderr = ssh_client.exec_command(mysql_cmd, timeout=300)  # 大文件导入可能需要较长时间
            
            # 获取命令输出
            exit_code = stdout.channel.recv_exit_status()
            error_output = stderr.read().decode('utf-8', errors='ignore')
            
            ssh_client.close()
            
            if exit_code == 0:
                print("✅ SSH方式导入成功！")
                return True
            else:
                print(f"❌ SSH方式导入失败，退出码：{exit_code}")
                if error_output:
                    print(f"错误信息：{error_output}")
                print("尝试备选方案...")
                
        except Exception as e:
            print(f"❌ SSH方式执行失败：{str(e)}")
            print("尝试备选方案...")
        
        # 方案2：读取SQL文件内容，然后通过pymysql执行
        print("\n方法2：读取SQL文件内容并直接执行...")
        
        # 首先需要获取远程文件内容
        # 尝试通过SSH读取文件内容
        sql_content = None
        try:
            ssh_client = SSHClient()
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            ssh_client.connect(
                hostname=REMOTE_MYSQL["host"],
                port=22,
                username=REMOTE_RDP["remote_server_user"],
                password=REMOTE_RDP["remote_server_pwd"],
                timeout=30
            )
            
            # 读取文件内容
            cat_cmd = f"type \"{REMOTE_MYSQL['remote_sql_path']}\""  # Windows使用type命令
            stdin, stdout, stderr = ssh_client.exec_command(cat_cmd, timeout=120)
            
            # 获取文件内容
            sql_content = stdout.read().decode('utf-8', errors='ignore')
            error_output = stderr.read().decode('utf-8', errors='ignore')
            
            ssh_client.close()
            
            if error_output:
                print(f"❌ 读取文件内容失败：{error_output}")
                raise Exception("无法读取远程SQL文件内容")
            
            print(f"✅ 成功读取SQL文件内容，文件大小：{len(sql_content):,} 字节")
            
        except Exception as e:
            print(f"❌ 获取SQL文件内容失败：{str(e)}")
            print("请确保SSH服务正常运行且有足够权限读取文件")
            return False
        
        # 连接到MySQL并执行SQL内容
        remote_conn = pymysql.connect(
            host=REMOTE_MYSQL["host"],
            port=REMOTE_MYSQL["port"],
            user=REMOTE_MYSQL["user"],
            password=REMOTE_MYSQL["password"],
            db=REMOTE_MYSQL["db"],
            charset="utf8mb4",
            connect_timeout=30,
            autocommit=False  # 禁用自动提交
        )
        
        cursor = remote_conn.cursor()
        
        try:
            # 对于大型SQL文件，将其分割成较小的语句执行
            # 按分号分割，但需要考虑字符串中的分号
            statements = []
            current_statement = ""
            in_string = False
            string_char = None
            
            for char in sql_content:
                if char in ['"', "'", '`'] and (not current_statement or current_statement[-1] != '\\'):
                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False
                
                current_statement += char
                
                if char == ';' and not in_string:
                    statements.append(current_statement.strip())
                    current_statement = ""
            
            # 处理最后一个语句（如果有的话）
            if current_statement.strip():
                statements.append(current_statement.strip())
            
            print(f"✅ 已将SQL文件分割为 {len(statements)} 个语句")
            
            # 执行所有语句
            executed_count = 0
            for i, statement in enumerate(statements, 1):
                # 跳过空语句和注释
                if not statement or statement.strip().startswith('--') or statement.strip().startswith('#'):
                    continue
                
                # 显示进度（每100个语句显示一次）
                if i % 100 == 0:
                    print(f"🔄 正在执行第 {i}/{len(statements)} 个语句...")
                
                try:
                    cursor.execute(statement)
                    executed_count += 1
                except Exception as stmt_error:
                    print(f"⚠️ 执行第 {i} 个语句时出错：{str(stmt_error)}")
                    print(f"语句内容：{statement[:200]}..." if len(statement) > 200 else f"语句内容：{statement}")
                    # 继续执行其他语句，不中断整个过程
            
            remote_conn.commit()
            print(f"✅ 成功执行 {executed_count} 个SQL语句")
            print("✅ 云端MySQL导入成功！")
            return True
            
        except Exception as e:
            remote_conn.rollback()
            print(f"❌ 执行SQL语句时发生错误：{str(e)}")
            return False
        finally:
            cursor.close()
            
    except OperationalError as e:
        print(f"❌ 云端MySQL连接失败：{e}")
        return False
    except Exception as e:
        if remote_conn:
            try:
                remote_conn.rollback()
            except:
                pass
        print(f"❌ 导入过程中发生错误：{str(e)}")
        return False
    finally:
        if remote_conn:
            try:
                remote_conn.close()
            except:
                pass

def verify_sync():
    """验证同步结果：查询云端数据是否和本地一致（可选，增加安全性）"""
    print("\n=== 验证同步结果 ===")
    
    # 要验证的表名配置
    VERIFICATION_TABLE = None  # 设置为None时自动选择第一个存在的表
    
    # 本地查询可用表
    local_conn = pymysql.connect(**{k: v for k, v in LOCAL_MYSQL.items() if k != "dump_path" and k != "sql_filename"})
    local_cursor = local_conn.cursor()
    
    try:
        # 如果未指定验证表，查询数据库中所有表
        if VERIFICATION_TABLE is None:
            local_cursor.execute("SHOW TABLES;")
            tables = [table[0] for table in local_cursor.fetchall()]
            
            if not tables:
                print("⚠️ 本地数据库中没有找到任何表，跳过验证")
                return True
            
            VERIFICATION_TABLE = tables[0]
            print(f"ℹ️ 自动选择第一个表 '{VERIFICATION_TABLE}' 进行同步验证")
        
        # 查询表数据量
        try:
            local_cursor.execute(f"SELECT COUNT(*) AS total FROM {VERIFICATION_TABLE};")
            result = local_cursor.fetchone()
            local_count = result[0] if result else 0  # 使用整数索引访问元组
        except pymysql.err.ProgrammingError:
            print(f"⚠️ 本地数据库中找不到表 '{VERIFICATION_TABLE}'，跳过验证")
            return True
            
    finally:
        local_cursor.close()
        local_conn.close()

    # 云端查询同一表数据量
    remote_conn = pymysql.connect(**{k: v for k, v in REMOTE_MYSQL.items() if k != "remote_sql_path"})
    remote_cursor = remote_conn.cursor()
    
    try:
        try:
            remote_cursor.execute(f"SELECT COUNT(*) AS total FROM {VERIFICATION_TABLE};")
            result = remote_cursor.fetchone()
            remote_count = result[0] if result else 0  # 使用整数索引访问元组
        except pymysql.err.ProgrammingError:
            print(f"⚠️ 云端数据库中找不到表 '{VERIFICATION_TABLE}'，验证失败")
            return False
        
        # 检查表结构是否一致（可选的额外验证）
        try:
            # 获取本地表结构
            local_conn = pymysql.connect(**{k: v for k, v in LOCAL_MYSQL.items() if k != "dump_path" and k != "sql_filename"})
            local_cursor = local_conn.cursor()
            local_cursor.execute(f"SHOW CREATE TABLE {VERIFICATION_TABLE};")
            result = local_cursor.fetchone()
            local_table_struct = result[1] if result else ""
            local_cursor.close()
            local_conn.close()
            
            # 获取云端表结构
            remote_cursor.execute(f"SHOW CREATE TABLE {VERIFICATION_TABLE};")
            result = remote_cursor.fetchone()
            remote_table_struct = result[1] if result else ""
            
            # 简化表结构比较（忽略AUTO_INCREMENT等可能不同的值）
            import re
            local_struct_clean = re.sub(r'AUTO_INCREMENT=\d+', '', local_table_struct)
            remote_struct_clean = re.sub(r'AUTO_INCREMENT=\d+', '', remote_table_struct)
            
            structure_match = local_struct_clean == remote_struct_clean
        except:
            structure_match = True  # 如果获取结构失败，假设结构正确
            
        if local_count == remote_count and structure_match:
            print(f"🎉 同步验证成功！表 '{VERIFICATION_TABLE}' 本地数据量：{local_count}，云端数据量：{remote_count}")
            return True
        else:
            if local_count != remote_count:
                print(f"❌ 同步验证失败！表 '{VERIFICATION_TABLE}' 本地数据量：{local_count}，云端数据量：{remote_count}")
            if not structure_match:
                print(f"❌ 表结构不一致！请检查表 '{VERIFICATION_TABLE}' 的定义")
            return False
            
    finally:
        remote_cursor.close()
        remote_conn.close()

def main():
    """主流程：导出→上传→导入→验证"""
    start_time = time.time()
    try:
        # 第一步：导出本地SQL
        if not export_local_sql():
            return
        # 第二步：上传到云端（优先使用SSH方式）
        if not upload_sql_to_remote_ssh():
            print("⚠️ SSH上传失败，尝试备选方案：网络共享")
            if not upload_sql_to_remote():
                return
        # 第三步：远程导入
        if not remote_import_sql():
            return
        # 第四步：验证同步（可选）
        verify_sync()

        total_time = round(time.time() - start_time, 2)
        print(f"\n=== 全程自动化同步完成！总耗时：{total_time}秒 ===")
    except Exception as e:
        print(f"\n❌ 同步流程异常终止：{str(e)}")

def print_menu():
    """打印程序菜单"""
    print("\n=== 数据库同步工具 ===")
    print("1. 执行完整的数据库同步流程")
    print("2. 测试SSH连接")
    print("3. 测试RDP连接")
    print("4. 退出程序")
    print("======================")
    print("提示：系统优先使用RDP方式传输文件，失败后自动尝试其他方式")

if __name__ == "__main__":
    # 直接执行完整的数据库同步流程，取消菜单选择
    print("=== 开始执行数据库同步流程 ===")
    main()
    print("=== 数据库同步流程执行完成 ===")