import requests
from bs4 import BeautifulSoup
import urllib.parse
import hashlib
from datetime import datetime

class QuantumWeb:
    def __init__(self, chat):
        self.chat = chat
        self.cache_file = f"{chat.cache_dir}/web_cache.json"
        self.load_cache()
    
    def load_cache(self):
        """بارگذاری cache"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                self.cache = json.load(f)
        except:
            self.cache = {"searches": {}, "last_update": self.chat.timestamp}
            self.save_cache()
    
    def save_cache(self):
        """ذخیره cache"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=4, ensure_ascii=False)
    
    def search_web(self, query, max_results=5):
        """جستجو در وب"""
        cache_key = hashlib.md5(query.encode()).hexdigest()
        
        # بررسی cache
        if cache_key in self.cache["searches"]:
            cache_data = self.cache["searches"][cache_key]
            # اگر cache کمتر از 1 ساعت قدیمی است
            if (datetime.now() - datetime.strptime(cache_data["timestamp"], "%Y-%m-%d %H:%M:%S")).seconds < 3600:
                return cache_data["results"]
        
        try:
            url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.find_all('div', {'class': 'result__body'})[:max_results]:
                title = result.find('a', {'class': 'result__a'})
                snippet = result.find('a', {'class': 'result__snippet'})
                
                if title and snippet:
                    results.append({
                        'title': title.text,
                        'snippet': snippet.text,
                        'url': title['href']
                    })
            
            # ذخیره در cache
            self.cache["searches"][cache_key] = {
                "timestamp": self.chat.timestamp,
                "query": query,
                "results": results
            }
            self.save_cache()
            
            return results
        
        except Exception as e:
            print(f"⚠️ خطا در جستجوی وب: {str(e)}")
            return []
    
    def search_and_learn(self, query):
        """جستجو و یادگیری"""
        results = self.search_web(query)
        if results:
            # ذخیره در حافظه
            self.chat.memory.learn_from_web(query, results)
            
            # ساخت پاسخ
            response = "براساس جستجو در اینترنت:\n\n"
            for result in results[:2]:
                response += f"🔹 {result['title']}\n{result['snippet']}\n\n"
            return response
        
        return None
    
    def learn_topic(self, topic):
        """یادگیری موضوع جدید"""
        results = self.search_web(topic)
        if results:
            self.chat.memory.learn_from_web(topic, results)