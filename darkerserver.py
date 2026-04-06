from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
import os
import re
import sys
import time
import logging
import threading
import cgi
from Python_S.fuzzysearchs import fuzzy_search
from urllib.parse import urlparse  # 新增：用于解析GET请求路径
from Python_S.cache_manager import check_and_update_cache
from Python_S.AutoScene3D_height_onefunc import process_map_data
from Python_S.json_to_sql_processor import database_manipulate
from Python_S.sql_operations import SQLOperations
from Python_S.emailing import send_single_email
from Python_S.LocalAI.ollama_client import OllamaClient, LocalAIRAG
from Python_S.LocalAI.vector_store import VectorIndexManager
from Python_S.ReadDBAndGenerateProtocol import (
    update_action,
    fetch_actions,
    config_searching,
    create_task,
    extract_item_group,
    fetch_siteproduct_info,
    export_table_columns_with_foreign_key,
    extract_entire_network,
    add_subscribers,
    submit_issue,
    manage_login,
    fetch_advice_recording,
    update_recordings,
    update_productStatus,
    delete_recordings,
    get_all_users,
    manage_register,
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
    extrac_function_breakdown_group,
    extract_single_feature,
    modify_user_level,
    create_action,
    modify_user,
    mark_modification,
)
from Python_S.PageExplain import chat_with_ai



# 配置日志记录
logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 定义.glb文件的固定名称和路径（与process_map_data生成的文件一致）
GLB_FILENAME = "3D_environment_output.glb"

class MyHandler(BaseHTTPRequestHandler):
    # API路径白名单
    ALLOWED_PATHS = {
        # 产品数据相关
        '/get_regulation',
        '/knockknock',
        '/get_function_list',
        '/search_function',
        '/init_config_func',
        '/config_searching',
        '/extract_Know_net',
        '/get_solution_list',
        '/fbssearching',
        '/function_breakdown_full',
        '/extract_item_group',
        '/db_summary',
        '/table_summary',
        '/generate_new_item',
        '/modifyitems',
        '/deleteitem',
        '/extract_item',
        '/createnewsql',
        # 运营数据相关
        '/add_user',
        '/manage_login',
        '/manage_register',
        '/add_issue',
        '/add_action',
        '/transfer_bug2action',
        '/update_recordings',
        '/update_productStatus',
        '/delete_recordings',
        '/get_all_recording',
        '/get_all_actions',
        '/get_siteproduct_info',
        '/get_all_users',
        '/get_tasks_tobepub',
        '/update_action',
        '/update_tasks',
        '/get_visit_stat',
        '/create_new_tasks',
        '/add_visit',
        '/modify_user_level',
        '/modify_user_data',
        # 配置管理相关
        '/save_user_product_config',
        '/get_user_product_config_list',
        '/load_user_product_config',
        # 其他
        '/process_map_data',
        '/stopserver',
        '/upload_avatar',
        # AI相关
        '/online_AI',
        '/local_AI',
        '/ai_health',
        '/ai_rebuild',
    }

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
            
    # 添加处理函数


    def _handle_ai_health(self):
        try:
            ollama_client = OllamaClient()
            is_connected = ollama_client.check_connection()
            models = ollama_client.list_models() if is_connected else []
            
            self._send_response({
                'status': 'healthy' if is_connected else 'degraded',
                'ollama_connected': is_connected,
                'index_built': self.ai_index.index_built if hasattr(self, 'ai_index') else False,
                'available_models': models
            })
        except Exception as e:
            self._send_response({'status': 'error', 'message': str(e)}, 500)

    def _handle_ai_rebuild(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            force_rebuild = data.get('force_rebuild', False)
            
            success = self.ai_index.build_index(force_rebuild=force_rebuild)
            self._send_response({
                'success': success,
                'message': '索引构建成功' if success else '索引构建失败'
            })
        except Exception as e:
            logging.error(f'重建索引出错: {str(e)}')
            self._send_response({'success': False, 'message': str(e)}, 500)

    def _handle_avatar_upload(self):
        """处理头像上传请求"""
        try:
            # 解析multipart/form-data请求
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            # 获取用户ID
            user_id = form.getvalue('userId')
            if not user_id:
                self._send_response({'success': False, 'message': '缺少用户ID'}, 400)
                return
            
            # 获取上传的文件
            avatar_file = form.getvalue('avatar')
            if not avatar_file:
                self._send_response({'success': False, 'message': '缺少头像文件'}, 400)
                return
            
            # 确定DarkerUserData文件夹路径（与BackEndS同级）
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            darker_user_data_dir = os.path.join(os.path.dirname(backend_dir), 'DarkerUserData')
            
            # 创建用户目录
            user_dir = os.path.join(darker_user_data_dir, str(user_id))
            if not os.path.exists(user_dir):
                os.makedirs(user_dir, exist_ok=True)
            
            # 保存头像文件
            avatar_path = os.path.join(user_dir, 'profile_photo.png')
            with open(avatar_path, 'wb') as f:
                f.write(avatar_file)
            
            # 返回成功响应
            self._send_response({'success': True, 'message': '头像上传成功'})
            
        except Exception as e:
            # 处理错误
            logging.error(f'头像上传失败: {str(e)}')
            self._send_response({'success': False, 'message': f'头像上传失败: {str(e)}'}, 500)
            
    def _handle_save_fov_config(self, data):
        """处理保存配置请求"""
        try:
            # 获取请求数据
            user_id = data.get('userId')
            config_name = data.get('configName')
            config_data = data.get('configData')
            filetype = data.get('filetype')
            
            if not user_id or not config_name or not config_data:
                self._send_response({'success': False, 'message': '缺少必要参数'}, 400)
                return
            
            # 确定DarkerUserData文件夹路径（与BackEndS同级）
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            darker_user_data_dir = os.path.join(os.path.dirname(backend_dir), 'DarkerUserData')
            
            # 根据filetype选择文件夹
            user_dir = os.path.join(darker_user_data_dir, str(user_id))
            if filetype == 'mapfile':
                project_dir = os.path.join(user_dir, 'MapProjectFile')
                if not os.path.exists(project_dir):
                    os.makedirs(project_dir, exist_ok=True)
            elif filetype == 'phyarchifile':
                project_dir = os.path.join(user_dir, 'PhyArchiProjectFile')
                if not os.path.exists(project_dir):
                    os.makedirs(project_dir, exist_ok=True)
            else:  # 默认fovfile
                project_dir = os.path.join(user_dir, 'FoVProjectFile')
                if not os.path.exists(project_dir):
                    os.makedirs(project_dir, exist_ok=True)
            
            # 读取indexing.json文件
            indexing_path = os.path.join(project_dir, 'indexing.json')
            if os.path.exists(indexing_path):
                with open(indexing_path, 'r', encoding='utf-8') as f:
                    indexing_data = json.load(f)
            else:
                # 如果文件不存在，创建默认结构
                indexing_data = {'templates': []}
            
            # 检查templates数组中是否有与configName相同的名称
            templates = indexing_data.get('templates', [])
            original_config_name = config_name
            counter = 1
            
            # 生成唯一的配置名称
            while config_name in templates:
                config_name = f"{original_config_name}_{counter}"
                counter += 1
            
            # 保存配置文件
            config_file_path = os.path.join(project_dir, f"{config_name}.json")
            with open(config_file_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            
            # 更新indexing.json文件
            templates.append(config_name)
            indexing_data['templates'] = templates
            with open(indexing_path, 'w', encoding='utf-8') as f:
                json.dump(indexing_data, f, ensure_ascii=False, indent=2)
            
            # 返回成功响应，包含保存的文件名
            self._send_response({'success': True, 'message': '配置保存成功', 'filename': config_name})
            
        except Exception as e:
            # 处理错误
            logging.error(f'保存配置失败: {str(e)}')
            self._send_response({'success': False, 'message': f'保存配置失败: {str(e)}'}, 500)
            
    def _handle_get_fov_config_list(self, data):
        """处理获取配置列表请求"""
        try:
            # 获取请求数据
            user_id = data.get('userId')
            filetype = data.get('filetype')
            
            if not user_id:
                self._send_response({'success': False, 'message': '缺少用户ID'}, 400)
                return
            
            # 确定DarkerUserData文件夹路径（与BackEndS同级）
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            darker_user_data_dir = os.path.join(os.path.dirname(backend_dir), 'DarkerUserData')
            
            # 根据filetype选择文件夹
            user_dir = os.path.join(darker_user_data_dir, str(user_id))
            if filetype == 'mapfile':
                project_dir = os.path.join(user_dir, 'MapProjectFile')
            elif filetype == 'phyarchifile':
                project_dir = os.path.join(user_dir, 'PhyArchiProjectFile')
            else:  # 默认fovfilef
                project_dir = os.path.join(user_dir, 'FoVProjectFile')
            
            # 读取indexing.json文件
            indexing_path = os.path.join(project_dir, 'indexing.json')
            if os.path.exists(indexing_path):
                with open(indexing_path, 'r', encoding='utf-8') as f:
                    indexing_data = json.load(f)
                templates = indexing_data.get('templates', [])
            else:
                # 如果文件不存在，返回空数组
                templates = []
            
            # 返回成功响应，包含templates数组
            self._send_response({'success': True, 'message': '获取配置列表成功', 'templates': templates})
            
        except Exception as e:
            # 处理错误
            logging.error(f'获取配置列表失败: {str(e)}')
            self._send_response({'success': False, 'message': f'获取配置列表失败: {str(e)}'}, 500)
            
    def _handle_load_fov_config(self, data):
        """处理加载配置文件请求"""
        try:
            # 获取请求数据
            user_id = data.get('userId')
            config_name = data.get('configName')
            filetype = data.get('filetype')
            
            if not user_id or not config_name:
                self._send_response({'success': False, 'message': '缺少必要参数'}, 400)
                return
            
            # 确定DarkerUserData文件夹路径（与BackEndS同级）
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            darker_user_data_dir = os.path.join(os.path.dirname(backend_dir), 'DarkerUserData')
            
            # 根据filetype选择文件夹
            user_dir = os.path.join(darker_user_data_dir, str(user_id))
            if filetype == 'mapfile':
                project_dir = os.path.join(user_dir, 'MapProjectFile')
            elif filetype == 'phyarchifile':
                project_dir = os.path.join(user_dir, 'PhyArchiProjectFile')
            else:  # 默认fovfile
                project_dir = os.path.join(user_dir, 'FoVProjectFile')
            
            # 读取配置文件
            config_file_path = os.path.join(project_dir, f"{config_name}.json")
            if os.path.exists(config_file_path):
                with open(config_file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            else:
                # 如果文件不存在，返回错误
                self._send_response({'success': False, 'message': '配置文件不存在'}, 404)
                return
            
            # 返回成功响应，包含配置数据
            self._send_response({'success': True, 'message': '加载配置成功', 'configData': config_data})
            
        except Exception as e:
            # 处理错误
            logging.error(f'加载配置失败: {str(e)}')
            self._send_response({'success': False, 'message': f'加载配置失败: {str(e)}'}, 500)

    def do_GET(self):
        """处理GET请求（新增下载逻辑）"""
        try:
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
        except ConnectionResetError as e:
            # 处理客户端连接重置错误
            logging.warning(f"客户端连接重置: {e} 来自 IP: {self.client_address[0]}")
        except Exception as e:
            # 处理其他异常
            logging.error(f"处理GET请求时发生错误: {e} 来自 IP: {self.client_address[0]}")

    def do_OPTIONS(self):
        """处理预检请求（允许GET方法）"""
        try:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')  # 新增GET支持
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            return
        except ConnectionResetError as e:
            # 处理客户端连接重置错误
            logging.warning(f"客户端连接重置: {e} 来自 IP: {self.client_address[0]}")
        except Exception as e:
            # 处理其他异常
            logging.error(f"处理OPTIONS请求时发生错误: {e} 来自 IP: {self.client_address[0]}")

    def do_POST(self):
        """处理POST请求（保留原有所有功能）"""
        database = None
        try:
            # 检查路径是否在白名单中
            if self.path not in self.ALLOWED_PATHS:
                # 记录非法请求
                logging.warning(f"非法请求路径: {self.path} 来自 IP: {self.client_address[0]}")
                # 返回403 Forbidden
                self._send_response({'error': '访问被拒绝'}, 403)
                return
            
            # 调试日志：打印请求路径
            print(f"接收到POST请求，路径: {self.path}")
            
            # 处理头像上传请求
            if self.path == '/upload_avatar':
                self._handle_avatar_upload()
                return
            elif self.path == '/online_AI':
                # 处理与AI聊天的请求
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data)
                    question = data.get('question', '')
                    content_type = data.get('content_type', 'project')  # 默认为基于项目信息
                    if not question:
                        self._send_response({'success': False, 'message': '缺少问题参数'}, 400)
                        return
                    # 调用AI聊天功能
                    result = chat_with_ai(question, content_type)
                    self._send_response({'success': True, 'output': json.loads(result)})
                except json.JSONDecodeError as e:
                    self._send_response({'error': f'JSON解析错误: {str(e)}'}, 400)
                except Exception as e:
                    logging.error(f'处理AI聊天请求时出错: {str(e)}')
                    self._send_response({'success': False, 'message': f'处理请求时出错: {str(e)}'}, 500)
                return
            elif self.path == '/local_AI':
                # 处理与AI聊天的请求（使用本地Ollama）
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data)
                    question = data.get('question', '')
                    use_context = data.get('use_context', True)
                    if not question:
                        self._send_response({'success': False, 'message': '缺少问题参数'}, 400)
                        return
                    
                    # 检查AI系统是否初始化
                    if not hasattr(self, 'ai_rag') or not self.ai_rag:
                        self._send_response({'success': False, 'message': 'AI系统未初始化'}, 500)
                        return
                    
                    # 检查Ollama连接
                    ollama_client = self.ai_rag.ollama
                    if not ollama_client.check_connection():
                        self._send_response({'success': False, 'message': 'Ollama服务连接失败，请确保服务正在运行'}, 500)
                        return
                    
                    # 调用AI聊天功能
                    result = self.ai_rag.ask(question, use_context=use_context)
                    result = json.dumps({"answer": result}, ensure_ascii=False)
                    self._send_response({'success': True, 'output': json.loads(result)})
                except json.JSONDecodeError as e:
                    self._send_response({'error': f'JSON解析错误: {str(e)}'}, 400)
                except Exception as e:
                    logging.error(f'处理AI聊天请求时出错: {str(e)}')
                    self._send_response({'success': False, 'message': f'处理请求时出错: {str(e)}'}, 500)
                return

            elif self.path == '/ai_health':
                self._handle_ai_health()

            elif self.path == '/ai_rebuild':
                self._handle_ai_rebuild()
                
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
            if 'datatype' not in data:
                datamode = "product"
            else:
                datamode = data.get('datatype')

            if deploy_mode == "test":
                db_product = SQLOperations(develop_product_config)
                db_operation = SQLOperations(develop_operation_config)
            elif deploy_mode == "full":
                #若当前代码部署在服务器端，则产品数据不允许写入，故意设置错误密码
                db_product = SQLOperations(server_product_config)
                #若当前代码部署在服务器端，则运营数据写入服务器数据库（既相对的）
                db_operation = SQLOperations(server_operation_config)

            if datamode =='product':
                database = db_product
                database_name = develop_product_config['database']
                processed_results, lib_tables_data = export_table_columns_with_foreign_key(database,database_name)
            else:
                database = db_operation
                # database_name = develop_operation_config['database']

            ####################################### PRODUCT DATA RELATED ##################################################
            if self.path =='/get_regulation':  #根据国家列表获取法规列表 #Done
                resulting = fetch_regulation_list(database,processed_results,lib_tables_data,"country",data.get('countries'),"Name")
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/knockknock': #验证服务器工作状态 #Done
                self._send_response({'success': True, 'output': 'HelloThere'})
            elif self.path == '/get_function_list':   # 获取用户功能列表  #Done
                # processed_results, lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = extract_item_group(database,processed_results,lib_tables_data,data.get('table_name'),data.get('item_cate'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/search_function':   # 模糊搜索函数  #Done
                # processed_results, lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = fuzzy_search(database,processed_results,lib_tables_data,data.get('table_name'),data.get('searchtext'), float(0.8))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/init_config_func':  #初始化产品配置器选项  #Done
                # processed_results, lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = initiate_configurator(database,processed_results,lib_tables_data)
                self._send_response({'success': True, 'output': resulting})
            elif self.path =='/config_searching':   # 配置搜索 #Done
                # processed_results, lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = config_searching(database,processed_results,lib_tables_data,data.get('search_condition'))
                self._send_response({'success': True, 'output': resulting}) 
            elif self.path == '/extract_Know_net':   # 提取知识网络 #Done
                # processed_results, lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = extract_entire_network(database,processed_results,lib_tables_data,'work')
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/get_solution_list':   # 配置搜索  ??????????????
                # processed_results, lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = extract_item_group(database,processed_results,lib_tables_data,data.get('table_name'),data.get('item_cate'))
                self._send_response({'success': True, 'output': resulting}) 
            elif self.path == '/fbssearching':   # FBS搜索 #Done
                resulting = extract_single_feature(database,data.get('intputdata'))
                self._send_response({'success': True, 'output': resulting}) 
            elif self.path == '/function_breakdown_full':   # 功能分解 #Done
                # processed_results, lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = extrac_function_breakdown_group(database,processed_results,lib_tables_data," ",data.get('item_cate'))
                self._send_response({'success': True, 'output': resulting}) 
            elif self.path == '/extract_item_group': # 提取数据组
                # processed_results, lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = extract_item_group(database,processed_results,lib_tables_data,data.get('table_name'),data.get('item_cate'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/db_summary':  # 数据库摘要 #Done
                resulting = fetch_db_summary(database)
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/table_summary':  # 表摘要 #Done
                resulting = fetch_table_sumary(database,data.get('data'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/generate_new_item':  # 生成新项目 #Done
                # processed_results,lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = generate_new_object_data_structure(processed_results,lib_tables_data,data['tablename'])
                mark_modification(database,data['tablename'])
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/modifyitems':  # 修改项目 #Done
                data2 = data.get('data')
                first_key, first_value = next(iter(data2['rowdata'].items()))
                # processed_results,lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = generate_target_object_data_structure(database,processed_results,lib_tables_data,data2['tablename'],first_value,first_key)
                # mark_modification(database,data2['tablename'])
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/deleteitem':  # 删除项目 #Done
                data2 = data.get('data')
                first_key, first_value = next(iter(data2['rowdata'].items()))
                # processed_results, lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = perform_group_delete_operation(database,processed_results, lib_tables_data,data2['tablename'],first_value,first_key) 
                mark_modification(database,data2['tablename'])
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/extract_item':  # 提取项目 #Done
                data2 = data.get('data')
                first_key, first_value = next(iter(data2['rowdata'].items()))
                # processed_results, lib_tables_data = export_table_columns_with_foreign_key(database)
                resulting = extract_single_item(database,processed_results,lib_tables_data,data2['tablename'],first_value,first_key)
                self._send_response({'success': True, 'output': resulting})    
            elif self.path == '/createnewsql': #Done
                if deploy_mode == "test":
                    try:
                        resulting = database_manipulate(database,data.get('data'))
                        mark_modification(database,"")
                        self._send_response({'success': True, 'output': resulting})
                    except Exception as e:
                        logging.error(f"处理数据库操作错误: {str(e)}")
                        self._send_response({'success': False, "message": f"服务器内部错误: {str(e)}"})  
                else:
                    self._send_response({'success': False, "message": f"服务器内部错误: 非测试模式下不允许创建新SQL"})  


            ####################################### OPERATION DATA RELATED ##################################################
            elif self.path == '/add_user':
                resulting = add_subscribers(database,data.get('user'))
                self._send_response({'success': True, 'output': resulting})
                # 在新线程中异步发送邮件，避免阻塞HTTP响应
                if resulting["status"]:
                    def send_emails_async():
                        try:
                            userdata = resulting["userdata"]
                            logging.info(f"开始异步发送订阅确认邮件给: {userdata['email']}")
                            send_single_email(userdata["email"], "subscription_notification",userdata)
                            logging.info(f"开始异步发送管理员通知邮件给: {admin_email}")
                            send_single_email(recipient_email=admin_email,email_type="admin_notification",user_data=userdata,notiftype="subscribe")
                            logging.info("所有邮件发送完成")
                        except Exception as e:
                            logging.error(f"异步邮件发送失败: {str(e)}")
                    
                    # 启动新线程发送邮件
                    email_thread = threading.Thread(target=send_emails_async, daemon=True)
                    email_thread.start()
            elif self.path == '/manage_login':
                resulting = manage_login(database,data.get('login'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/manage_register':
                resulting = manage_register(database,data.get('registration'),deploy_mode)
                self._send_response({'success': True, 'output': resulting})
                # 在新线程中异步发送邮件，避免阻塞HTTP响应
                if resulting["status"]:
                    def send_emails_async():
                        try:
                            user_info = resulting["userinfo"]
                            send_single_email(recipient_email=user_info["Email"],email_type="registration_confirmation",user_data=user_info)
                            send_single_email(recipient_email=admin_email,email_type="admin_notification",user_data=user_info,notiftype="registration")
                        except Exception as e:
                            logging.error(f"异步邮件发送失败: {str(e)}")
                    # 启动新线程发送邮件
                    email_thread = threading.Thread(target=send_emails_async, daemon=True)
                    email_thread.start()
            elif self.path == '/add_issue':
                resulting = submit_issue(database,data.get('issue'))
                self._send_response({'success': True, 'output': resulting})
                # 在新线程中异步发送邮件，避免阻塞HTTP响应
                if resulting["status"]:
                    def send_emails_async():
                        try:
                            issuedata = resulting["issuedata"]
                            send_single_email(recipient_email=issuedata["Email"],email_type="issue_recieve_confirm",user_data=issuedata)
                            send_single_email(recipient_email=admin_email,email_type="admin_check_notif",user_data=issuedata)
                        except Exception as e:
                            logging.error(f"异步邮件发送失败: {str(e)}")
                    # 启动新线程发送邮件
                    email_thread = threading.Thread(target=send_emails_async, daemon=True)
                    email_thread.start()
            elif self.path == '/add_action':
                resulting = create_action(database,data.get('actiondata'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/transfer_bug2action':
                resulting = create_action(database,data.get('actiondata'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/update_recordings':
                resulting = update_recordings(database,data.get('to_update'),data.get('ID'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/update_productStatus':
                resulting = update_productStatus(database,data.get('to_update'),data.get('ID'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/delete_recordings':
                resulting = delete_recordings(database,data.get('ID'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/get_all_recording':
                resulting = fetch_advice_recording(database)
                self._send_response({'success': True, 'output': resulting}) 
            elif self.path == '/get_all_actions':
                resulting = fetch_actions(database)
                self._send_response({'success': True, 'output': resulting}) 
            elif self.path =='/get_siteproduct_info':
                resulting = fetch_siteproduct_info(database)
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/get_all_users':
                resulting = get_all_users(database)
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/get_tasks_tobepub':
                resulting = get_task_tobepub(database)
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/update_action':
                resulting = update_action(database,data.get('actiondata'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/update_tasks':
                resulting = update_task(database,data)
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/get_visit_stat':
                resulting = visit_statistic(database)
                self._send_response({'success': True, 'output': resulting}) 
            elif self.path == '/create_new_tasks':
                resulting = create_task(database,data.get('taskdata'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/add_visit':
                resulting = visit_management(database,data.get('data'),data.get('uservisit'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/modify_user_level':
                resulting = modify_user_level(database,data.get('userdata'))
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/modify_user_data':
                user_id = data.get('userId')
                modify_item = data.get('modifyitem')
                content = data.get('content')
                resulting = modify_user(database, user_id, modify_item, content)
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/save_user_product_config':
                self._handle_save_fov_config(data)
            elif self.path == '/get_user_product_config_list':
                self._handle_get_fov_config_list(data)
            elif self.path == '/load_user_product_config':
                self._handle_load_fov_config(data)

            ####################################### NO DATABASED RELATED ##################################################
            elif self.path == '/process_map_data':
                global GLB_FILENAME
                GLB_FILENAME='3DModels/' + data.get('fileName')+'.glb'
                resulting = process_map_data(data.get('mapdata'),GLB_FILENAME)
                self._send_response({'success': True, 'output': resulting})
            elif self.path == '/stopserver':
                # 关闭服务器逻辑
                self._send_response({'success': True, 'output': 'Server is shutting down...'})
                # 导入全局变量httpd
                global httpd
                # 发送响应后关闭服务器
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

            if database:
                database.close()
                
        except ConnectionResetError as e:
            # 处理客户端连接重置错误
            logging.warning(f"客户端连接重置: {e} 来自 IP: {self.client_address[0]}")
            # 确保数据库连接关闭
            if database:
                try:
                    database.close()
                except:
                    pass
        except Exception as e:
            # 处理其他异常
            logging.error(f"处理POST请求时发生错误: {e} 来自 IP: {self.client_address[0]}")
            # 确保数据库连接关闭
            if database:
                try:
                    database.close()
                except:
                    pass
        
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
    global deploy_mode,server_product_config,server_operation_config,develop_product_config,develop_operation_config,admin_email,serverLocation
    # 初始化 frontend_path
    frontend_path = None
    
    try:
        with open('darker_config.json', 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            deploy_mode = config_data.get('deploy_mode', 'test')  # 默认值为'test'
            server_product_config = config_data.get('server_product_config')
            server_operation_config = config_data.get('server_operation_config')
            develop_product_config = config_data.get('develop_product_config')
            develop_operation_config = config_data.get('develop_operation_config')
            admin_email = config_data.get('admin_email', 'admin@example.com')
            CN_com_port = config_data.get('Server_comPort').get('CN')
            US_com_port = config_data.get('Server_comPort').get('US')
            test_com_port = config_data.get('test_com_port')
            serverLocation = config_data.get('serverLocation')
            frontend_path = config_data.get('frontend_develop_folder')
    except FileNotFoundError:
        print(f"配置文件 darker_config.json 不存在，使用默认值 'test'")
        deploy_mode = "test"
    except json.JSONDecodeError:
        print(f"配置文件 darker_config.json 格式错误，使用默认值 'test'")
        deploy_mode = "test"
    except Exception as e:
        print(f"读取配置文件时发生错误: {e}，使用默认值 'test'")
        deploy_mode = "test"
    
    # 如果 frontend_path 未设置，使用默认路径
    if not frontend_path:
        frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Darker-tech')
        print(f"使用默认前端路径: {frontend_path}")

    if deploy_mode == "test":
        server_address = ('localhost', test_com_port)
    elif deploy_mode == "full":
        if serverLocation == 'CN':
            server_address = ('0.0.0.0', CN_com_port)
        elif serverLocation == 'US':
            server_address = ('0.0.0.0', US_com_port)
        else:
            server_address = ('0.0.0.0', 7000)

        # 初始化AI系统
    # frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Darker-tech')
    print(f"前端路径: {frontend_path}")
    
    # 检查前端路径是否存在
    if not os.path.exists(frontend_path):
        print(f"⚠️  警告: 前端路径不存在: {frontend_path}")
        print("AI系统将无法构建索引，但其他功能仍可正常使用")
        frontend_path = None
    # 修改：只加载索引，不自动构建
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(backend_dir, 'Python_S', 'LocalAI', 'index_store.pkl')

    print(f"索引文件路径: {index_path}")

    # 检查索引文件是否存在
    if os.path.exists(index_path):
        print("✅ 向量索引文件已存在，将加载现有索引")
        ai_index = VectorIndexManager(frontend_path, store_path=index_path)
        ai_index.index_built = True
    else:
        print("⚠️  向量索引文件不存在，将在首次请求时自动构建")
        ai_index = VectorIndexManager(frontend_path, store_path=index_path)
        ai_index.index_built = False
    
    # 初始化Ollama客户端
    print("连接Ollama服务...")
    # 根据部署模式选择模型
    if deploy_mode == "full":
        model_name = "qwen2.5:1.5b"
        print(f"部署模式: {deploy_mode}，使用模型: {model_name}")
    else:  # test模式
        model_name = "qwen2.5:7b"
        print(f"部署模式: {deploy_mode}，使用模型: {model_name}")
    
    ollama_client = OllamaClient(model=model_name)
    ollama_connected = ollama_client.check_connection()
    
    if ollama_connected:
        print("✅ Ollama服务连接成功")
        models = ollama_client.list_models()
        print(f"可用模型: {', '.join(models) if models else '无'}")
    else:
        print("❌ Ollama服务连接失败")
        print("请确保Ollama服务正在运行: ollama serve")
        print("请下载模型: ollama pull qwen2.5:7b")
    
    # 初始化RAG系统
    ai_rag = LocalAIRAG(ollama_client, ai_index)
    print("✅ AI RAG系统已初始化")
    
    # 检查索引状态
    if ai_index.index_built:
        print("✅ 向量索引已存在，将加载现有索引")
    else:
        print("⏳ 向量索引不存在，将在首次请求时自动构建")
    
    # 创建handler实例
    handler = MyHandler
    
    # 传递AI系统给handler
    handler.ai_index = ai_index
    handler.ai_rag = ai_rag

    httpd = ThreadingHTTPServer(server_address, MyHandler)
    print(f'Starting DarkerTech backend server on {deploy_mode} mode port {server_address[1]}...')
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
