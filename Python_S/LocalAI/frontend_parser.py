import os
import re
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import hashlib

class FrontendParser:
    def __init__(self, frontend_path: str):
        self.frontend_path = frontend_path
        self.pages_info = {}
        self.components_info = {}
        self.js_modules_info = {}
        self.site_structure = {}
        
    def parse_all(self) -> Dict[str, Any]:
        self.parse_html_files()
        self.parse_js_files()
        self.build_site_structure()
        return {
            "pages": self.pages_info,
            "components": self.components_info,
            "js_modules": self.js_modules_info,
            "site_structure": self.site_structure
        }
    
    def parse_html_files(self):
        html_files = []
        for root, dirs, files in os.walk(self.frontend_path):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.trae', 'libs', 'js']]
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                relative_path = os.path.relpath(html_file, self.frontend_path)
                page_info = self._parse_html_content(content, relative_path)
                
                if 'components' in relative_path.lower():
                    self.components_info[relative_path] = page_info
                else:
                    self.pages_info[relative_path] = page_info
                    
            except Exception as e:
                print(f"Error parsing {html_file}: {e}")
    
    def _parse_html_content(self, content: str, file_path: str) -> Dict[str, Any]:
        soup = BeautifulSoup(content, 'html.parser')
        
        title = soup.find('title')
        title_text = title.get_text() if title else os.path.basename(file_path)
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ''
        
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = h.get_text(strip=True)
            if text:
                headings.append({
                    'level': h.name,
                    'text': text
                })
        
        sections = []
        for section in soup.find_all('section'):
            section_id = section.get('id', '')
            section_class = section.get('class', [])
            section_text = section.get_text(strip=True)[:500]
            if section_text:
                sections.append({
                    'id': section_id,
                    'class': section_class,
                    'preview': section_text
                })
        
        scripts = []
        for script in soup.find_all('script'):
            src = script.get('src', '')
            if src:
                scripts.append(src)
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a.get('href', '')
            text = a.get_text(strip=True)
            if text and href:
                links.append({'text': text, 'href': href})
        
        buttons = []
        for btn in soup.find_all(['button', 'input']):
            if btn.name == 'button':
                text = btn.get_text(strip=True)
                onclick = btn.get('onclick', '')
            else:
                text = btn.get('value', '')
                onclick = btn.get('onclick', '')
            if text:
                buttons.append({'text': text, 'onclick': onclick})
        
        forms = []
        for form in soup.find_all('form'):
            form_id = form.get('id', '')
            action = form.get('action', '')
            inputs = []
            for inp in form.find_all('input'):
                inputs.append({
                    'name': inp.get('name', ''),
                    'type': inp.get('type', ''),
                    'placeholder': inp.get('placeholder', '')
                })
            forms.append({
                'id': form_id,
                'action': action,
                'inputs': inputs
            })
        
        main_content = soup.find('body')
        text_content = main_content.get_text(separator=' ', strip=True) if main_content else ''
        text_content = re.sub(r'\s+', ' ', text_content)[:2000]
        
        return {
            'file_path': file_path,
            'title': title_text,
            'description': description,
            'headings': headings,
            'sections': sections,
            'scripts': scripts,
            'links': links[:20],
            'buttons': buttons[:20],
            'forms': forms,
            'text_content': text_content,
            'content_hash': hashlib.md5(content.encode()).hexdigest()[:8]
        }
    
    def parse_js_files(self):
        js_files = []
        for root, dirs, files in os.walk(self.frontend_path):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.trae', 'libs', 'js']]
            for file in files:
                if file.endswith('.js') and not file.endswith('.min.js'):
                    js_files.append(os.path.join(root, file))
        
        for js_file in js_files:
            try:
                with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                relative_path = os.path.relpath(js_file, self.frontend_path)
                js_info = self._parse_js_content(content, relative_path)
                self.js_modules_info[relative_path] = js_info
                
            except Exception as e:
                print(f"Error parsing {js_file}: {e}")
    
    def _parse_js_content(self, content: str, file_path: str) -> Dict[str, Any]:
        functions = re.findall(r'function\s+(\w+)\s*\([^)]*\)', content)
        arrow_functions = re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>', content)
        
        classes = re.findall(r'class\s+(\w+)', content)
        
        exports = re.findall(r'export\s+(?:default\s+)?(?:function\s+)?(\w+)', content)
        
        api_calls = re.findall(r'fetch\s*\(\s*[\'"]([^\'"]+)[\'"]', content)
        api_calls += re.findall(r'axios\.[a-z]+\s*\(\s*[\'"]([^\'"]+)[\'"]', content)
        
        event_handlers = re.findall(r'(?:addEventListener|on)\s*\(\s*[\'"](\w+)[\'"]', content)
        
        return {
            'file_path': file_path,
            'functions': functions[:30],
            'arrow_functions': arrow_functions[:20],
            'classes': classes,
            'exports': exports,
            'api_calls': list(set(api_calls)),
            'event_handlers': list(set(event_handlers)),
            'line_count': len(content.split('\n'))
        }
    
    def build_site_structure(self):
        self.site_structure = {
            'main_pages': [],
            'feature_pages': [],
            'tools': [],
            'components': list(self.components_info.keys())
        }
        
        for path, info in self.pages_info.items():
            title = info.get('title', '').lower()
            
            if path == 'index.html' or 'index' in path:
                self.site_structure['main_pages'].append({
                    'path': path,
                    'title': info.get('title', ''),
                    'description': info.get('text_content', '')[:200]
                })
            elif any(keyword in title for keyword in ['tool', 'builder', 'configurator', 'platform']):
                self.site_structure['tools'].append({
                    'path': path,
                    'title': info.get('title', ''),
                    'description': info.get('text_content', '')[:200]
                })
            else:
                self.site_structure['feature_pages'].append({
                    'path': path,
                    'title': info.get('title', ''),
                    'description': info.get('text_content', '')[:200]
                })
    
    def get_page_chunks(self, chunk_size: int = 1000) -> List[Dict[str, Any]]:
        chunks = []
        
        for path, info in self.pages_info.items():
            text = f"页面: {info['title']}\n"
            text += f"路径: {path}\n"
            
            if info.get('description'):
                text += f"描述: {info['description']}\n"
            
            if info.get('headings'):
                text += "标题结构:\n"
                for h in info['headings']:
                    text += f"  {h['level']}: {h['text']}\n"
            
            if info.get('text_content'):
                text += f"\n内容摘要:\n{info['text_content'][:500]}\n"
            
            if info.get('buttons'):
                text += "\n按钮功能:\n"
                for btn in info['buttons'][:10]:
                    text += f"  - {btn['text']}\n"
            
            if info.get('forms'):
                text += "\n表单:\n"
                for form in info['forms']:
                    text += f"  表单ID: {form['id']}\n"
                    for inp in form['inputs']:
                        text += f"    输入: {inp['name']} ({inp['type']})\n"
            
            chunks.append({
                'content': text,
                'metadata': {
                    'source': path,
                    'type': 'page',
                    'title': info['title']
                }
            })
        
        for path, info in self.js_modules_info.items():
            text = f"JavaScript模块: {path}\n"
            
            if info.get('functions'):
                text += f"函数: {', '.join(info['functions'][:20])}\n"
            
            if info.get('api_calls'):
                text += f"API调用: {', '.join(info['api_calls'])}\n"
            
            if info.get('event_handlers'):
                text += f"事件处理: {', '.join(info['event_handlers'])}\n"
            
            chunks.append({
                'content': text,
                'metadata': {
                    'source': path,
                    'type': 'javascript',
                    'title': path
                }
            })
        
        return chunks


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        frontend_path = sys.argv[1]
    else:
        frontend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    parser = FrontendParser(frontend_path)
    result = parser.parse_all()
    
    print(f"解析完成:")
    print(f"  - 页面数量: {len(result['pages'])}")
    print(f"  - 组件数量: {len(result['components'])}")
    print(f"  - JS模块数量: {len(result['js_modules'])}")
    
    chunks = parser.get_page_chunks()
    print(f"  - 生成的文本块数量: {len(chunks)}")
