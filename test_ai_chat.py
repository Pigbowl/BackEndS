import requests
import json

# 测试 /ai_chat 接口
def test_ai_chat():
    url = "http://localhost:5000/ai_chat"
    
    # 测试用例1: 正常请求
    print("测试1: 正常请求")
    payload = {
        "question": "网站的主要功能是什么？",
        "use_context": True
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    # 测试用例2: 缺少 question 参数
    print("\n测试2: 缺少 question 参数")
    payload2 = {
        "use_context": True
    }
    
    try:
        response = requests.post(url, json=payload2)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    # 测试用例3: 空 question 参数
    print("\n测试3: 空 question 参数")
    payload3 = {
        "question": "",
        "use_context": True
    }
    
    try:
        response = requests.post(url, json=payload3)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    # 测试用例4: 非 JSON 格式请求
    print("\n测试4: 非 JSON 格式请求")
    try:
        response = requests.post(url, data="不是 JSON 格式")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    test_ai_chat()
