import os
import json
from datetime import datetime
import hashlib
from typing import Dict, List, Any, Optional
from .memory_manager import QuantumMemoryManager
from .memory_stats import QuantumMemoryStats
from .memory_patterns import QuantumMemoryPatterns
from .memory_relations import QuantumMemoryRelations

class QuantumMemory:
    def __init__(self, chat):
        self.chat = chat
        self.timestamp = "2025-03-10 09:53:09"
        self.user = "artgalleryma2ta"
        self.version = "4.0"
        
        # مسیرهای اصلی
        self.core_path = chat.core_path
        self.memory_dir = os.path.join(self.core_path, "consciousness", "memory")
        self.data_dir = os.path.join(self.memory_dir, "data")
        self.index_dir = os.path.join(self.memory_dir, "index")
        
        # ایجاد دایرکتوری‌ها
        for directory in [self.memory_dir, self.data_dir, self.index_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # راه‌اندازی ماژول‌ها
        self.manager = QuantumMemoryManager(self)
        self.stats = QuantumMemoryStats(self)
        self.patterns = QuantumMemoryPatterns(self)
        self.relations = QuantumMemoryRelations(self)
        
        # بارگذاری داده‌ها
        self.load_data()
    
    def load_data(self):
        """بارگذاری داده‌های اصلی"""
        self.history = self._load_json(
            os.path.join(self.data_dir, "chat_history.json"),
            {
                "metadata": {
                    "created_at": self.timestamp,
                    "user": self.user,
                    "version": self.version,
                    "last_update": self.timestamp
                },
                "conversations": []
            }
        )
        
        self.learned = self._load_json(
            os.path.join(self.data_dir, "learned_data.json"),
            {
                "topics": {},
                "last_learn": self.timestamp
            }
        )
    
    def _load_json(self, file_path: str, default_data: Dict) -> Dict:
        """بارگذاری فایل JSON"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ خطا در بارگذاری {file_path}: {str(e)}")
        return default_data
    
    def _save_json(self, file_path: str, data: Dict) -> bool:
        """ذخیره فایل JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"⚠️ خطا در ذخیره {file_path}: {str(e)}")
            return False
    
    def save_conversation(self, message: str, response: str, quality: str = "good"):
        """ذخیره مکالمه جدید"""
        # افزودن به تاریخچه
        conversation = [
            {
                "timestamp": self.timestamp,
                "user": self.user,
                "message": message,
                "type": "user",
                "hash": hashlib.sha256(message.encode()).hexdigest()
            },
            {
                "timestamp": self.timestamp,
                "user": "assistant",
                "message": response,
                "type": "assistant",
                "quality": quality,
                "hash": hashlib.sha256(response.encode()).hexdigest()
            }
        ]
        
        self.history["conversations"].extend(conversation)
        
        # به‌روزرسانی در همه ماژول‌ها
        self.stats.update_conversation_stats(message, response, quality)
        self.patterns.learn_new_patterns(message, response)
        self.relations.update_topic_relations(message)
        
        # ذخیره تغییرات
        self._save_json(
            os.path.join(self.data_dir, "chat_history.json"),
            self.history
        )
    
    def learn_from_web(self, query: str, results: List[Dict[str, str]]):
        """یادگیری از نتایج جستجوی وب"""
        # پردازش و ذخیره در موضوعات
        topic_data = {
            "timestamp": self.timestamp,
            "source": "web_search",
            "data": results,
            "keywords": self.patterns.extract_keywords(query),
            "patterns": self.patterns.extract_patterns(results),
            "hash": hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()
        }
        
        self.learned["topics"][query.lower()] = topic_data
        
        # به‌روزرسانی در سایر ماژول‌ها
        self.stats.update_learning_stats(query, results)
        self.patterns.learn_from_results(results)
        self.relations.add_web_learning(query, results)
        
        # ذخیره تغییرات
        self._save_json(
            os.path.join(self.data_dir, "learned_data.json"),
            self.learned
        )
    
    def find_response(self, query: str) -> Optional[str]:
        """یافتن پاسخ مناسب از حافظه"""
        # جستجو در موضوعات
        relevant_topics = self.relations.find_relevant_topics(query)
        if not relevant_topics:
            return None
        
        # انتخاب بهترین پاسخ
        best_response = None
        max_similarity = 0
        
        for topic, score in relevant_topics.items():
            if topic in self.learned["topics"]:
                topic_data = self.learned["topics"][topic]
                similarity = self.patterns.calculate_similarity(query, topic_data)
                
                if similarity > max_similarity and similarity > 0.3:
                    max_similarity = similarity
                    best_response = self._format_response(topic_data["data"])
        
        if best_response:
            self.stats.update_response_stats(query, best_response, max_similarity)
            return best_response
        
        return None
    
    def _format_response(self, results: List[Dict[str, str]]) -> str:
        """قالب‌بندی نتایج برای پاسخ"""
        response = "براساس اطلاعات موجود در حافظه:\n\n"
        for result in results[:2]:
            response += f"🔹 {result['title']}\n{result['snippet']}\n\n"
        return response