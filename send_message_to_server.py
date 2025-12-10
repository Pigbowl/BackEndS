import requests


def send_message_to_darkerserver(server_url):
    """
    向部署在远程服务器上的darkerserver发送消息
    :param server_url: 远程服务器的URL，例如 http://49749.71.168.1.100:5000
    :return: 如果成功接收响应，返回 "Hello there"，否则返回错误信息
    """
    try:
        # 发送GET请求到服务器根路径
        response = requests.get(server_url, timeout=5)
        
        # 检查响应状态码
        if response.status_code == 200:
            # 尝试解析JSON响应
            try:
                json_data = response.json()
                print(f"服务器响应: {json_data}")
            except ValueError:
                print(f"服务器响应不是JSON格式: {response.text}")
            
            # 如果成功接收响应，返回 "Hello there"
            return "Hello there"
        else:
            # 响应状态码不是200，返回错误信息
            return f"请求失败，状态码: {response.status_code}"
    except requests.exceptions.RequestException as e:
        # 发生网络异常，返回错误信息
        return f"请求异常: {str(e)}"


if __name__ == "__main__":
    # 示例使用 - 请替换为实际的服务器URL
    server_url = "http://localhost:5000"  # 本地测试使用
    # server_url = "http://your_server_ip:5000"  # 远程服务器使用
    
    result = send_message_to_darkerserver(server_url)
    print(result)
