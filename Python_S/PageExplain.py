from bs4 import BeautifulSoup
import requests
import openai  # 若用其他模型，替换为对应SDK（如讯飞、通义千问
import json

# 1. 提取网页内容（首次运行提取，之后可缓存）
def extract_web_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 提取正文（可根据网页结构调整选择器，如 .content、#main 等）
    main_content = soup.find('body').get_text(strip=True, separator='\n')
    return main_content


# 缓存网页内容（避免重复抓取）
WEB_CONTENT = extract_web_content("你的网页URL")  # 替换为你的网页地址

# 2. 配置大模型（以OpenAI为例，其他模型替换此部分）
openai.api_key = "你的API密钥"  # 替换为自己的密钥

def get_ai_answer(question):
    # 构建prompt，让模型仅基于网页内容回答
    prompt = f"""你是该网页的智能助手，仅基于以下网页内容回答用户问题，不泄露其他信息：
    网页内容：{WEB_CONTENT}
    用户问题：{question}
    回答要求：简洁准确，基于上述内容，无法回答则说明"该问题超出网页内容范围"
    """
    # 调用大模型
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def chat(question):
    answer = get_ai_answer(question)
    return (json.dumps(answer, ensure_ascii=False))
