from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
import os
import sys
import time
import logging

from Python_S.fuzzysearchs import fuzzy_search
from urllib.parse import urlparse  # 新增：用于解析GET请求路径
from Python_S.path_utils import resource_path
from Python_S.solution_finding import solution_hunting
from Python_S.FBS_SEARCHING import fbsfindg, fbsbaseinit
from Python_S.cache_manager import check_and_update_cache
from Python_S.parse_adas_benchmark import benchmarkinfofetch
from Python_S.AutoScene3D_height_onefunc import process_map_data
from Python_S.read_part_catalogue import create_part_catalogue
from Python_S.json_to_sql_processor import database_manipulate
from Python_S.emailing import send_batch_email, send_single_email
from Python_S.sql_operations import deploy_mode  # 导入全局变量
from Python_S.ReadDBAndGenerateProtocol import (
    config_searching,
    create_task,
    extract_item_group,
    fetch_siteproduct_info,
    export_table_columns_with_foreign_key,
    extract_entire_network,
    add_users,
    submit_issue,
    manage_login,
    fetch_advice_recording,
    update_recordings,
    update_productStatus,
    delete_recordings,
    get_user_info,
    visit_management,
    visit_statistic,
    perform_group_delete_operation,
    generate_new_object_data_structure,
    generate_target_object_data_structure,
    fetch_db_summary,
    fetch_table_sumary,
    fetch_regulation_list,
    extract_single_item,
    initiate_configurator,
    get_task_tobepub,
    update_task,
)

# 配置日志记录
logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 定义.glb文件的固定名称和路径（与process_map_data生成的文件一致）
GLB_FILENAME = "3D_environment_output.glb"

class MyHandler(BaseHTTPRequestHandler):
    def _send_response(self, data, status=200):
        """发送JSON格式响应（原有功能，保持不变）"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')  # 新增GET方法支持
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _send_file(self, file_path, filename):
        """发送文件二进制流（新增：用于下载功能）"""
        try:
            # 读取文件二进制数据
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # 发送响应头
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'model/gltf-binary')  # .glb标准MIME类型
            # 触发浏览器下载（指定文件名）
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Content-Length', str(len(file_data)))  # 告知文件大小
            self.end_headers()

            # 发送文件数据
            self.wfile.write(file_data)

        except FileNotFoundError:
            # 文件不存在时返回404
            self._send_response({'error': f'文件 {filename} 不存在'}, 404)
        except Exception as e:
            # 其他错误（如读取失败）返回500
            self._send_response({'error': f'下载失败: {str(e)}'}, 500)

    def do_GET(self):
        """处理GET请求（新增下载逻辑）"""
        # 解析请求路径
        parsed_path = urlparse(self.path)

        # 处理.glb文件下载请求（路径为/download_glb）
        if parsed_path.path == '/download_glb':
            # 获取.glb文件的完整路径（与服务器运行目录同级别）
            # 服务器运行目录 = 当前脚本所在目录
            server_dir = os.path.dirname(os.path.abspath(__file__))
            glb_file_path = os.path.join(server_dir, GLB_FILENAME)
                # 调用发送文件方法
              
            self._send_file(glb_file_path, GLB_FILENAME)
            return

        # 原有GET请求响应（如服务器状态检查）
        self._send_response({'message': 'DarkerTech backend server is running'}, 200)

    def do_OPTIONS(self):
        """处理预检请求（允许GET方法）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')  # 新增GET支持
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

    def do_POST(self):
        """处理POST请求（保留原有所有功能）"""
        # 调试日志：打印请求路径
        print(f"接收到POST请求，路径: {self.path}")
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        try:
            data = json.loads(post_data)
        except json.JSONDecodeError as e:
            self._send_response({'error': f'JSON解析错误: {str(e)}'}, 400)
            return

        # 原有所有POST路径处理（保持不变）

        if self.path =='/get_regulation':
            processed_results, lib_tables_data = export_table_columns_with_foreign_key()
            countries = data.get('countries')
            resulting = fetch_regulation_list(processed_results,lib_tables_data,"country",countries,"Name")
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/knockknock':
            self._send_response({'success': True, 'output': 'HelloThere'})
        elif self.path == '/deploy_information':
            # 将deploy_mode的值赋给全局变量
            if 'deploy_mode' in data:
                from Python_S.sql_operations import deploy_mode  # 再次导入以修改其值
                import Python_S.sql_operations
                Python_S.sql_operations.deploy_mode = data.get('deploy_mode')
                print(f"已设置全局部署模式: {Python_S.sql_operations.deploy_mode}")
            self._send_response({'success': True, 'output': deploy_mode})
        elif self.path == '/search_function':   # 模糊搜索函数
            processed_results, lib_tables_data = export_table_columns_with_foreign_key()
            resulting = fuzzy_search(processed_results,lib_tables_data,data.get('table_name'),data.get('searchtext'), float(0.8))
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/init_config_func':
            processed_results, lib_tables_data = export_table_columns_with_foreign_key()
            resulting = initiate_configurator(processed_results,lib_tables_data)
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/get_function_list':   # 获取用户功能列表
            processed_results, lib_tables_data = export_table_columns_with_foreign_key()
            resulting = extract_item_group(processed_results,lib_tables_data,data.get('table_name'),data.get('item_cate'))
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/extract_Know_net':   # 提取知识网络
            processed_results, lib_tables_data = export_table_columns_with_foreign_key()
            resulting = extract_entire_network(processed_results,lib_tables_data,'work')
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/get_solution_list':   # 配置搜索
            processed_results, lib_tables_data = export_table_columns_with_foreign_key()
            resulting = extract_item_group(processed_results,lib_tables_data,data.get('table_name'),data.get('item_cate'))
            self._send_response({'success': True, 'output': resulting}) 
        elif self.path =='/config_searching':   # 配置搜索
            processed_results, lib_tables_data = export_table_columns_with_foreign_key()
            resulting = config_searching(processed_results,lib_tables_data,data.get('search_condition'))
            self._send_response({'success': True, 'output': resulting}) 
        elif self.path == '/fbssearching':   # FBS搜索
            fbs_input = data.get('intputdata')
            table_address = resource_path(r"DataStorage/database.xlsx")
            resulting = fbsfindg(fbs_input, table_address)
            self._send_response({'success': True, 'output': resulting}) 
        elif self.path == '/fbsnetinit':   # FBS网络初始化
            table_address = resource_path(r"DataStorage/database.xlsx")
            resulting = fbsbaseinit(table_address)
            self._send_response({'success': True, 'output': resulting}) 
        elif self.path == '/part_list_get':   # 获取零件列表
            table_address = resource_path(r"DataStorage/database.xlsx")
            resulting = create_part_catalogue(table_address)
            self._send_response({'success': True, 'output': resulting}) 
        elif self.path == '/add_issue':
            resulting = submit_issue(data.get('issue'))
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/manager_login':
            resulting = manage_login(data.get('login'))
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/update_recordings':
            resulting = update_recordings(data.get('to_update'),data.get('ID'))
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/update_productStatus':
            resulting = update_productStatus(data.get('to_update'),data.get('ID'))
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/delete_recordings':
            resulting = delete_recordings(data.get('ID'))
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/get_all_recording':
            resulting = fetch_advice_recording()
            self._send_response({'success': True, 'output': resulting}) 
        elif self.path =='/get_siteproduct_info':
            resulting = fetch_siteproduct_info()
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/get_user_info':
            resulting = get_user_info()
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/process_map_data':
            global GLB_FILENAME
            GLB_FILENAME='3DModels/' + data.get('fileName')+'.glb';
            resulting = process_map_data(data.get('mapdata'),GLB_FILENAME)
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/add_user':
            new_user = data.get('user')
            resulting = add_users(new_user)
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/add_visit':
            visit = data.get('data')
            resulting = visit_management(visit)
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/update_tasks':
            resulting = update_task(data)
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/get_visit_stat':
            resulting = visit_statistic()
            self._send_response({'success': True, 'output': resulting}) 
        elif self.path == '/get_tasks_tobepub':
            resulting = get_task_tobepub()
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/create_new_tasks':
            resulting = create_task(data)
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/extract_item_group':
            processed_results, lib_tables_data = export_table_columns_with_foreign_key()
            resulting = extract_item_group(processed_results,lib_tables_data,data.get('table_name'),data.get('item_cate'))
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/db_summary':
            resulting = fetch_db_summary()
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/table_summary':
            resulting = fetch_table_sumary(data)
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/generate_new_item':
            processed_results,lib_tables_data = export_table_columns_with_foreign_key()
            resulting = generate_new_object_data_structure(processed_results,lib_tables_data,data['tablename'])
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/createnewsql':
            try:
                resulting = database_manipulate(data)
                self._send_response({'success': True, 'output': resulting})
            except Exception as e:
                error_message = f"处理数据库操作错误: {str(e)}"
                # print(error_message)
                logging.error(error_message)
                self._send_response({'success': False, "message": f"服务器内部错误: {str(e)}"})  
        elif self.path == '/modifyitems':
            """处理修改项目的请求"""
            first_key, first_value = next(iter(data['rowdata'].items()))
            processed_results,lib_tables_data = export_table_columns_with_foreign_key()
            resulting = generate_target_object_data_structure(processed_results,lib_tables_data,data['tablename'],first_value,first_key)
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/deleteitem':
            """处理删除项目的请求"""
            first_key, first_value = next(iter(data['rowdata'].items()))
            processed_results, lib_tables_data = export_table_columns_with_foreign_key()
            resulting = perform_group_delete_operation(processed_results, lib_tables_data,data['tablename'],first_value,first_key) 
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/extract_item':
            first_key, first_value = next(iter(data['rowdata'].items()))
            processed_results, lib_tables_data = export_table_columns_with_foreign_key()
            resulting = extract_single_item(processed_results,lib_tables_data,data['tablename'],first_value,first_key)
            self._send_response({'success': True, 'output': resulting})
        elif self.path == '/stopserver':
            # 关闭服务器逻辑
            self._send_response({'success': True, 'output': 'Server is shutting down...'})
            # 导入全局变量httpd
            global httpd
            # 发送响应后关闭服务器
            import threading
            def shutdown_server():
                # 延迟执行，确保响应已发送
                time.sleep(1)
                print('\nShutting down server...')
                httpd.shutdown()
                httpd.server_close()
                print('Server stopped.')
            # 在新线程中执行关闭操作
            threading.Thread(target=shutdown_server).start()
        else:
            self._send_response({'error': '未知路径'}, 404)


        
def wait_for_file_creation(file_path: str) -> bool:
    MAX_WAIT_TIME = 5  # 5秒
    """等待文件创建，最多等待MAX_WAIT_TIME秒"""
    start_time = time.time()
    while time.time() - start_time < MAX_WAIT_TIME:
        if os.path.exists(file_path):
            # 确保文件内容已完全写入
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # 尝试读取文件以验证完整性
                    json.load(f)
                return True
            except (json.JSONDecodeError, IOError):
                # 文件存在但内容不完整，继续等待
                pass
        time.sleep(CHECK_INTERVAL)
    return False

# 全局变量，用于存储服务器实例
httpd = None

def main():
    global httpd
    # 初始化缓存
    cache_dir = check_and_update_cache()
    logging.info(f"使用缓存目录: {cache_dir}")
    deploy_mode = "full"
    if deploy_mode == "test":
        server_address = ('localhost', 5000)
    elif deploy_mode == "full":
        server_address = ('0.0.0.0', 5000)
    httpd = ThreadingHTTPServer(server_address, MyHandler)
    print('Starting DarkerTech backend server on port 5000...')  # 修正端口显示（原代码写的80，实际是5000）
    print('Server is ready to accept requests from frontend.')
    print('To stop the server, press Ctrl+C or send a POST request to /stopserver')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server...')
        httpd.server_close()
        print('Server stopped.')
    except Exception as e:
        print(f'\nServer error: {str(e)}')
        if httpd:
            httpd.server_close()
        print('Server stopped.')



if __name__ == '__main__':
    main()
