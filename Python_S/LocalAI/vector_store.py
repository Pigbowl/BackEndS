import os
import json
import pickle
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict, Counter
import hashlib
import re

class SimpleVectorStore:
    def __init__(self, store_path: str = None):
        self.store_path = store_path or os.path.join(os.path.dirname(__file__), 'vector_store.pkl')
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: np.ndarray = None
        self.metadata: List[Dict[str, Any]] = []
        self.embedder = None
        
    def _get_embedder(self):
        if self.embedder is None:
            self.embedder = SimpleEmbedder()
        return self.embedder
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        embedder = self._get_embedder()
        
        for doc in documents:
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            
            self.documents.append(content)
            self.metadata.append(metadata)
        
        all_texts = self.documents
        new_embeddings = embedder.encode(all_texts[-len(documents):], all_texts)
        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
    
    def similarity_search(self, query: str, k: int = 5, all_documents: List[str] = None) -> List[Tuple[Dict[str, Any], float]]:
        if self.embeddings is None or len(self.documents) == 0:
            return []
        
        embedder = self._get_embedder()
        query_embedding = embedder.encode_query(query, all_documents or self.documents)
        
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding) + 1e-8
        )
        
        top_indices = np.argsort(similarities)[::-1][:k]
        
        results = []
        for idx in top_indices:
            results.append({
                'content': self.documents[idx],
                'metadata': self.metadata[idx],
                'score': float(similarities[idx])
            })
        
        return results
    
    def save(self):
        data = {
            'documents': self.documents,
            'embeddings': self.embeddings,
            'metadata': self.metadata
        }
        with open(self.store_path, 'wb') as f:
            pickle.dump(data, f)
    
    def load(self) -> bool:
        if os.path.exists(self.store_path):
            with open(self.store_path, 'rb') as f:
                data = pickle.load(f)
            self.documents = data.get('documents', [])
            self.embeddings = data.get('embeddings')
            self.metadata = data.get('metadata', [])
            return True
        return False
    
    def clear(self):
        self.documents = []
        self.embeddings = None
        self.metadata = []
        if os.path.exists(self.store_path):
            os.remove(self.store_path)


class SimpleEmbedder:
    def __init__(self):
        self.vocabulary = {}
        self.idf = {}
        self.documents = []
        
    def fit(self, documents: List[str]):
        from collections import Counter
        
        doc_count = len(documents)
        word_doc_count = defaultdict(int)
        
        for doc in documents:
            words = self._tokenize(doc)
            unique_words = set(words)
            for word in unique_words:
                word_doc_count[word] += 1
        
        self.idf = {
            word: np.log(doc_count / (count + 1)) 
            for word, count in word_doc_count.items()
        }
        
        idx = 0
        for word in self.idf.keys():
            self.vocabulary[word] = idx
            idx += 1
    
    def _tokenize(self, text: str) -> List[str]:
        import re
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        return words
    
    def encode(self, texts: List[str], all_documents: List[str] = None) -> np.ndarray:
        if all_documents and not self.vocabulary:
            self.fit(all_documents)
        
        embeddings = []
        for text in texts:
            words = self._tokenize(text)
            word_counts = Counter(words)
            total_words = len(words)
            
            embedding = np.zeros(len(self.vocabulary))
            for word, count in word_counts.items():
                if word in self.vocabulary:
                    tf = count / total_words if total_words > 0 else 0
                    tfidf = tf * self.idf.get(word, 0)
                    embedding[self.vocabulary[word]] = tfidf
            
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            
            embeddings.append(embedding)
        
        return np.array(embeddings)
    
    def encode_query(self, query: str, all_documents: List[str] = None) -> np.ndarray:
        if not self.vocabulary:
            return self.encode([query], all_documents)[0]
        else:
            return self.encode([query])[0]


class VectorIndexManager:
    def __init__(self, frontend_path: str, store_path: str = None):

        self.frontend_path = frontend_path
        self.store_path = store_path or os.path.join(os.path.dirname(__file__), 'index_store.pkl')
        print(store_path)
        
        self.vector_store = SimpleVectorStore(self.store_path)
        self.index_built = False
        
    def build_index(self, force_rebuild: bool = False) -> bool:
        if not self.frontend_path:
            print("❌ 前端路径未设置，无法构建索引")
            return False
        
        if not os.path.exists(self.frontend_path):
            print(f"❌ 前端路径不存在: {self.frontend_path}")
            return False
        
        if not force_rebuild and self.vector_store.load():
            print("✅ 从磁盘加载现有索引")
            self.index_built = True
            return True
        
        from .frontend_parser import FrontendParser
        
        print("⏳ 开始构建新索引...")
        print(f"前端路径: {self.frontend_path}")
        
        try:
            parser = FrontendParser(self.frontend_path)
            parser.parse_all()
            chunks = parser.get_page_chunks()
            
            print(f"解析到 {len(chunks)} 个文档块")
            
            if chunks:
                self.vector_store.add_documents(chunks)
                self.vector_store.save()
                self.index_built = True
                print(f"✅ 索引构建成功，包含 {len(chunks)} 个文档")
                return True
            else:
                print("⚠️  没有解析到任何文档块，无法构建索引")
                return False
        except Exception as e:
            print(f"❌ 构建索引时出错: {str(e)}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        if not self.index_built:
            self.build_index()
        
        return self.vector_store.similarity_search(query, k, self.vector_store.documents)
    
    def get_context_for_query(self, query: str, max_tokens: int = 2000) -> str:
        results = self.search(query, k=5)
        
        context_parts = []
        total_length = 0
        
        for result in results:
            content = result['content']
            if total_length + len(content) > max_tokens:
                break
            context_parts.append(content)
            total_length += len(content)
        
        return "\n\n---\n\n".join(context_parts)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        frontend_path = sys.argv[1]
    else:
        frontend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    manager = VectorIndexManager(frontend_path)
    manager.build_index(force_rebuild=True)
    
    test_queries = [
        "网站有哪些功能？",
        "如何使用配置器？",
        "ADAS功能有哪些？"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        results = manager.search(query, k=3)
        for i, result in enumerate(results):
            print(f"  结果 {i+1} (相似度: {result['score']:.3f}):")
            print(f"    来源: {result['metadata'].get('source', 'unknown')}")
            print(f"    内容预览: {result['content'][:100]}...")
