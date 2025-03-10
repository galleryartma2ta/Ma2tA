import json
from datetime import datetime
from typing import Dict, Any

class QuantumMemoryStats:
    def __init__(self, memory):
        self.memory = memory
        self.stats_file = f"{memory.data_dir}/memory_stats.json"
        self.load_stats()
    
    def load_stats(self):
        """بارگذاری آمار"""
        self.stats = self.memory._load_json(self.stats_file, {
            "total_messages": 0,
            "unique_topics": 0,
            "learned_patterns": 0,
            "successful_responses": 0,
            "last_update": self.memory.timestamp,
            "monthly_stats": {},
            "topic_frequency": {},
            "pattern_usage": {},
            "response_quality": {
                "excellent": 0,
                "good": 0,
                "fair": 0,
                "poor": 0
            }
        })
    
    def save_stats(self):
        """ذخیره آمار"""
        self.memory._save_json(self.stats_file, self.stats)
    
    def update_conversation_stats(self, message: str, response: str, quality: str):
        """به‌روزرسانی آمار مکالمات"""
        self.stats["total_messages"] += 2
        self.stats["response_quality"][quality] += 1
        
        # آمار ماهانه
        current_month = datetime.now().strftime("%Y-%m")
        if current_month not in self.stats["monthly_stats"]:
            self.stats["monthly_stats"][current_month] = {
                "messages": 0,
                "topics": {},
                "patterns": 0
            }
        
        self.stats["monthly_stats"][current_month]["messages"] += 2
        
        self.save_stats()
    
    def update_learning_stats(self, query: str, results: list):
        """به‌روزرسانی آمار یادگیری"""
        self.stats["unique_topics"] += 1
        
        # به‌روزرسانی فراوانی موضوعات
        keywords = self.memory.patterns.extract_keywords(query)
        for keyword in keywords:
            if keyword not in self.stats["topic_frequency"]:
                self.stats["topic_frequency"][keyword] = 0
            self.stats["topic_frequency"][keyword] += 1
        
        self.save_stats()
    
    def update_response_stats(self, query: str, response: str, similarity: float):
        """به‌روزرسانی آمار پاسخ‌ها"""
        self.stats["successful_responses"] += 1
        
        # تعیین کیفیت پاسخ
        if similarity > 0.8:
            quality = "excellent"
        elif similarity > 0.6:
            quality = "good"
        elif similarity > 0.4:
            quality = "fair"
        else:
            quality = "poor"
        
        self.stats["response_quality"][quality] += 1
        
        self.save_stats()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """دریافت آمار کلی حافظه"""
        return {
            "total_messages": self.stats["total_messages"],
            "unique_topics": self.stats["unique_topics"],
            "successful_responses": self.stats["successful_responses"],
            "response_quality": self.stats["response_quality"],
            "most_common_topics": sorted(
                self.stats["topic_frequency"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }