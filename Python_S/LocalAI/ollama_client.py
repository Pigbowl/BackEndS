import requests
import json
from typing import Optional, List, Dict, Any, Generator
import os

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5:7b"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.available_models = []
        
    def check_connection(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.available_models = [m['name'] for m in data.get('models', [])]
                return True
        except Exception as e:
            print(f"Cannot connect to Ollama: {e}")
        return False
    
    def list_models(self) -> List[str]:
        if not self.available_models:
            self.check_connection()
        return self.available_models
    
    def pull_model(self, model_name: str) -> bool:
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                timeout=300
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error pulling model: {e}")
            return False
    
    def generate(
        self, 
        prompt: str, 
        system_prompt: str = None,
        stream: bool = False,
        **kwargs
    ) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            **kwargs
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            if stream:
                return self._generate_stream(payload)
            else:
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=120
                )
                if response.status_code == 200:
                    result = response.json()
                    return result.get('response', '')
                else:
                    return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _generate_stream(self, payload: dict) -> Generator[str, None, None]:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            stream=True,
            timeout=120
        )
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if 'response' in data:
                    yield data['response']
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        **kwargs
    ) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        
        try:
            if stream:
                return self._chat_stream(payload)
            else:
                response = requests.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=120
                )
                if response.status_code == 200:
                    result = response.json()
                    return result.get('message', {}).get('content', '')
                else:
                    return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _chat_stream(self, payload: dict) -> Generator[str, None, None]:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            stream=True,
            timeout=120
        )
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if 'message' in data and 'content' in data['message']:
                    yield data['message']['content']


class LocalAIRAG:
    SYSTEM_PROMPT = """你是达客科技网站的智能助手，专门帮助用户了解和使用这个ADAS（高级驾驶辅助系统）知识网站。

你的职责：
1. 回答用户关于网站功能、页面内容的问题
2. 帮助用户找到他们需要的功能或信息
3. 解释网站上的ADAS相关概念和功能
4. 提供网站使用指导

回答要求：
- 基于提供的上下文信息准确回答
- 如果上下文中没有相关信息，诚实告知用户
- 回答要简洁明了，重点突出
- 使用中文回答
- 如果涉及页面路径，请提供具体的页面位置"""

    def __init__(self, ollama_client: OllamaClient, vector_store):
        self.ollama = ollama_client
        self.vector_store = vector_store
        self.conversation_history = []
        
    def ask(self, question: str, use_context: bool = True) -> str:
        context = ""
        if use_context:
            context = self.vector_store.get_context_for_query(question)
        
        if context:
            prompt = f"""基于以下网站信息回答用户问题。

网站信息：
{context}

用户问题：{question}

请基于以上信息回答问题。如果信息不足，请说明。"""
        else:
            prompt = f"""用户问题：{question}

请回答用户关于达客科技网站的问题。"""
        
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
        ]
        
        for msg in self.conversation_history[-6:]:
            messages.append(msg)
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.ollama.chat(messages)
        
        self.conversation_history.append({"role": "user", "content": question})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def ask_stream(self, question: str, use_context: bool = True):
        context = ""
        if use_context:
            context = self.vector_store.get_context_for_query(question)
        
        if context:
            prompt = f"""基于以下网站信息回答用户问题。

网站信息：
{context}

用户问题：{question}

请基于以上信息回答问题。如果信息不足，请说明。"""
        else:
            prompt = f"""用户问题：{question}

请回答用户关于达客科技网站的问题。"""
        
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
        ]
        
        for msg in self.conversation_history[-6:]:
            messages.append(msg)
        
        messages.append({"role": "user", "content": prompt})
        
        full_response = ""
        for chunk in self.ollama.chat(messages, stream=True):
            full_response += chunk
            yield chunk
        
        self.conversation_history.append({"role": "user", "content": question})
        self.conversation_history.append({"role": "assistant", "content": full_response})
    
    def clear_history(self):
        self.conversation_history = []


if __name__ == "__main__":
    client = OllamaClient()
    
    if client.check_connection():
        print("Ollama连接成功!")
        print(f"可用模型: {client.list_models()}")
        
        test_prompt = "你好，请简单介绍一下你自己。"
        print(f"\n测试问题: {test_prompt}")
        response = client.generate(test_prompt)
        print(f"回答: {response}")
    else:
        print("无法连接到Ollama，请确保Ollama正在运行")
        print("安装和启动方法:")
        print("1. 访问 https://ollama.ai 下载安装Ollama")
        print("2. 运行 'ollama serve' 启动服务")
        print("3. 运行 'ollama pull qwen2.5:7b' 下载模型")
