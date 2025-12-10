import requests


def test_endpoints():
    """
    测试多个端点是否正常工作
    """
    # 测试根路径GET请求
    print("测试根路径GET请求...")
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
    except Exception as e:
        print(f"请求异常: {str(e)}")
    
    print("\n测试/knockknock POST请求...")
    # 测试/knockknock POST请求
    try:
        response = requests.post('http://localhost:5000/knockknock', json={}, timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
    except Exception as e:
        print(f"请求异常: {str(e)}")
    
    print("\n测试/stopserver POST请求...")
    # 测试/stopserver POST请求
    try:
        response = requests.post('http://localhost:5000/stopserver', json={}, timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
    except Exception as e:
        print(f"请求异常: {str(e)}")


if __name__ == "__main__":
    test_endpoints()
