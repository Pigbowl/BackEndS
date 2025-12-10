import requests


def test_stopserver():
    """
    测试/stopserver端点是否能够正常关闭服务器
    """
    try:
        # 发送POST请求到/stopserver端点
        response = requests.post('http://localhost:5000/stopserver', json={}, timeout=5)
        
        # 检查响应
        if response.status_code == 200:
            print("请求成功，服务器正在关闭...")
            print(f"服务器响应: {response.json()}")
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {str(e)}")


if __name__ == "__main__":
    test_stopserver()
