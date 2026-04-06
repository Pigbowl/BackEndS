from bs4 import BeautifulSoup
import requests
import json
import os
import sys

# 1. 提取网页内容（首次运行提取，之后可缓存）
def extract_web_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 提取正文（可根据网页结构调整选择器，如 .content、#main 等）
    main_content = soup.find('body').get_text(strip=True, separator='\n')
    return main_content

# 2. 提取项目信息
def extract_project_info():
    """提取项目信息，包括文件结构和关键文件内容"""
    project_info = []
    
    # 从配置文件读取前端项目路径
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'darker_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        base_path = config_data.get('frontend_develop_folder', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    except Exception as e:
        # 如果配置文件读取失败，使用默认路径
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_info.append(f"配置文件读取失败: {str(e)}，使用默认路径\n{'='*50}\n")
    
    # 限制文件数量，避免信息过大
    file_count = 0
    max_files = 10
    
    # 遍历项目目录，收集信息
    for root, dirs, files in os.walk(base_path):
        # 跳过一些不需要的目录
        dirs[:] = [d for d in dirs if d not in ['.git', 'venv', '__pycache__', 'node_modules']]
        
        for file in files:
            # 只处理特定类型的文件
            if file.endswith(('.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.json', '.md')):
                file_count += 1
                if file_count > max_files:
                    project_info.append(f"... 更多文件（已限制为{max_files}个文件）\n")
                    return ''.join(project_info)
                
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, base_path)
                
                # 读取文件内容（限制大小）
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1000)  # 限制读取大小
                    project_info.append(f"文件: {relative_path}\n内容:\n{content}\n{'='*50}\n")
                except Exception as e:
                    project_info.append(f"文件: {relative_path}\n读取错误: {str(e)}\n{'='*50}\n")
    
    return ''.join(project_info)

# 3. 配置阿里百炼云API
def get_ali_bailian_answer(question, content):
    """调用阿里百炼云API获取回答"""
    import requests
    
    # 阿里百炼云API配置
    API_KEY = "sk-4b2f6af886e14515bdb390c6f3570859"
    API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    MODEL = "qwen-turbo"
    
    # 构建请求数据（阿里百炼云格式）
    payload = {
        "model": MODEL,
        "input": {
            "prompt": f"你是一个智能助手，基于提供的项目信息回答用户问题。\n\n{content}\n\n用户问题：{question}"
        },
        "parameters": {
            "temperature": 0.7,
            "max_tokens": 1000
        }
    }
    
    # 发送请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        if 'output' in result and 'text' in result['output']:
            return result['output']['text'].strip()
        else:
            return f"API返回格式错误: {str(result)}"
    except Exception as e:
        return f"API调用失败: {str(e)}"

def chat_with_ai(question, content_type="web"):
    """与AI聊天，可选择基于网页内容或项目信息"""
    if content_type == "web":
        # 基于网页内容
        # 可以使用以下格式的URL：
        # 1. 完整的HTTP/HTTPS URL，如 "https://thedarkertech.com"
        # 2. localhost地址，如 "http://localhost:5500/index.html"
        # 3. 本地HTML文件路径，如 "file:///C:/path/to/file.html"
        url = "https://thedarkertech.com"  # 默认使用thedarkertech.com
        content = extract_web_content(url)
    else:
        # 基于项目信息
        content = extract_project_info()
    answer = get_ali_bailian_answer(question, content)
    return json.dumps({"answer": answer}, ensure_ascii=False)
