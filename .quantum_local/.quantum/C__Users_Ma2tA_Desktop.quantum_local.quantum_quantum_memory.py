import json
from datetime import datetime, timedelta
import re

class QuantumMemory:
    def __init__(self, chat):
        self.chat = chat
        self.timestamp = "2025-03-10 09:34:43"
        self.user = "artgalleryma2ta"
        
        # مسیرهای فایل
        self.history_file = f"{chat.chat_dir}/chat_history.json"
        self.learning_file = f"{chat.knowledge_dir}/learned_data.json"
        self.stats_file = f"{chat.knowledge_dir}/memory_stats.json"
        
        # بارگذاری داده‌ها
        self.load_data()
    
    def load_data(self):
        """بارگذاری تمام داده‌های مورد نیاز"""
        # بارگذاری تاریخچه چت
        self.history = self._load_json(self.history_file, {
            "metadata": {
                "created_at": self.timestamp,
                "user": self.user,
                "version": self.chat.version,
                "last_update": self.timestamp
            },
            "conversations": []
        })
        
        # بارگذاری داده‌های یادگرفته شده
        self.learned = self._load_json(self.learning_file, {
            "topics": {},
            "patterns": {},
            "last_learn": self.timestamp,
            "stats": {
                "total_topics": 0,
                "total_patterns": 0,
                "last_cleanup": self.timestamp
            }
        })
        
        # بارگذاری آمار حافظه
        self.stats = self._load_json(self.stats_file, {
            "total_messages": 0,
            "unique_topics": 0,
            "learned_patterns": 0,
            "successful_responses": 0,
            "last_update": self.timestamp,
            "monthly_stats": {},
            "topic_frequency": {}
        })
    
    def _load_json(self, file_path, default_data):
        """بارگذاری فایل JSON با مدیریت خطا"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ خطا در بارگذاری {file_path}: {str(e)}")
            return default_data
    
    def _save_json(self, file_path, data):
        """ذخیره فایل JSON با مدیریت خطا"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"⚠️ خطا در ذخیره {file_path}: {str(e)}")
            return False
    
    def save_conversation(self, message, response):
        """ذخیره مکالمه جدید"""
        # افزودن به تاریخچه
        self.history["conversations"].extend([
            {
                "timestamp": self.timestamp,
                "user": self.user,
                "message": message,
                "type": "user"
            },
            {
                "timestamp": self.timestamp,
                "user": "assistant",
                "message": response,
                "type": "assistant"
            }
        ])
        
        # به‌روزرسانی آمار
        self.stats["total_messages"] += 2
        self._update_topic_stats(message)
        
        # ذخیره تغییرات
        self._save_json(self.history_file, self.history)
        self._save_json(self.stats_file, self.stats)
    
    def learn_from_web(self, query, results):
        """یادگیری از نتایج جستجوی وب"""
        topic = query.lower()
        
        # ذخیره اطلاعات جدید
        self.learned["topics"][topic] = {
            "timestamp": self.timestamp,
            "source": "web_search",
            "data": results,
            "keywords": self._extract_keywords(query),
            "patterns": self._extract_patterns(results)
        }
        
        # به‌روزرسانی آمار
        self.learned["stats"]["total_topics"] += 1
        self.stats["unique_topics"] += 1
        
        # ذخیره تغییرات
        self._save_json(self.learning_file, self.learned)
        self._save_json(self.stats_file, self.stats)
    
    def find_response(self, query):
        """یافتن پاسخ مناسب از حافظه"""
        best_match = None
        max_similarity = 0
        
        # جستجو در موضوعات یادگرفته شده
        query_keywords = set(self._extract_keywords(query))
        
        for topic, data in self.learned["topics"].items():
            topic_keywords = set(data["keywords"])
            similarity = self._calculate_similarity(query_keywords, topic_keywords)
            
            if similarity > max_similarity and similarity > 0.3:  # حداقل 30% شباهت
                max_similarity = similarity
                best_match = data
        
        if best_match:
            self.stats["successful_responses"] += 1
            self._save_json(self.stats_file, self.stats)
            
            return self._format_response(best_match["data"])
        
        return None
    
    def get_recent_conversations(self, limit=100):
        """دریافت مکالمات اخیر"""
        return self.history["conversations"][-limit:]
    
    def get_old_topics(self, days=7):
        """دریافت موضوعات قدیمی برای به‌روزرسانی"""
        old_topics = []
        current_time = datetime.now()
        
        for topic, data in self.learned["topics"].items():
            topic_time = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
            if (current_time - topic_time).days > days:
                old_topics.append(topic)
        
        return old_topics
    
    def _extract_keywords(self, text):
        """استخراج کلمات کلیدی از متن"""
        # حذف کلمات اضافی و استخراج کلمات مهم
        stop_words = {"و", "در", "به", "از", "که", "این", "را", "با", "است", "برای", "آن"}
        words = text.lower().split()
        return [word for word in words if len(word) > 2 and word not in stop_words]
    
    def _extract_patterns(self, results):
        """استخراج الگوهای متنی از نتایج"""
        patterns = []
        for result in results:
            # استخراج عبارات مهم از عنوان و توضیحات
            text = f"{result['title']} {result['snippet']}"
            # الگوهای معمول مثل: تعاریف، مثال‌ها، روش‌ها
            definitions = re.findall(r'([^.!?]+(است|می‌باشد|یعنی)[^.!?]+)[.!?]', text)
            examples = re.findall(r'([^.!?]+(مثلاً|برای مثال|مانند)[^.!?]+)[.!?]', text)
            methods = re.findall(r'([^.!?]+(روش|چگونه|چطور)[^.!?]+)[.!?]', text)
            
            patterns.extend([d[0] for d in definitions])
            patterns.extend([e[0] for e in examples])
            patterns.extend([m[0] for m in methods])
        
        return patterns
    
    def _calculate_similarity(self, set1, set2):
        """محاسبه شباهت بین دو مجموعه"""
        if not set1 or not set2:
            return 0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union
    
    def _format_response(self, results):
        """قالب‌بندی نتایج برای پاسخ"""
        response = "براساس اطلاعات موجود در حافظه:\n\n"
        for result in results[:2]:  # نمایش 2 نتیجه برتر
            response += f"🔹 {result['title']}\n{result['snippet']}\n\n"
        return response
    
    def _update_topic_stats(self, message):
        """به‌روزرسانی آمار موضوعات"""
        # به‌روزرسانی آمار ماهانه
        current_month = datetime.now().strftime("%Y-%m")
        if current_month not in self.stats["monthly_stats"]:
            self.stats["monthly_stats"][current_month] = {
                "messages": 0,
                "topics": {},
                "patterns": 0
            }
        
        self.stats["monthly_stats"][current_month]["messages"] += 1
        
        # به‌روزرسانی فراوانی موضوعات
        keywords = self._extract_keywords(message)
        for keyword in keywords:
            if keyword not in self.stats["topic_frequency"]:
                self.stats["topic_frequency"][keyword] = 0
            self.stats["topic_frequency"][keyword] += 1
    
    def cleanup_old_data(self, days=30):
        """پاکسازی داده‌های قدیمی"""
        current_time = datetime.now()
        cleanup_date = current_time - timedelta(days=days)
        
        # پاکسازی مکالمات قدیمی
        self.history["conversations"] = [
            conv for conv in self.history["conversations"]
            if datetime.strptime(conv["timestamp"], "%Y-%m-%d %H:%M:%S") > cleanup_date
        ]
        
        # پاکسازی موضوعات قدیمی کم‌استفاده
        for topic in list(self.learned["topics"].keys()):
            topic_data = self.learned["topics"][topic]
            topic_time = datetime.strptime(topic_data["timestamp"], "%Y-%m-%d %H:%M:%S")
            if topic_time < cleanup_date:
                # بررسی میزان استفاده
                if topic.lower() in self.stats["topic_frequency"]:
                    if self.stats["topic_frequency"][topic.lower()] < 5:  # کمتر از 5 بار استفاده
                        del self.learned["topics"][topic]
                else:
                    del self.learned["topics"][topic]
        
        # به‌روزرسانی زمان آخرین پاکسازی
        self.learned["stats"]["last_cleanup"] = self.timestamp
        
        # ذخیره تغییرات
        self._save_json(self.history_file, self.history)
        self._save_json(self.learning_file, self.learned)
    
    def get_memory_stats(self):
        """دریافت آمار حافظه"""
        return {
            "total_messages": self.stats["total_messages"],
            "unique_topics": self.stats["unique_topics"],
            "successful_responses": self.stats["successful_responses"],
            "topics_count": len(self.learned["topics"]),
            "patterns_count": self.learned["stats"]["total_patterns"],
            "last_update": self.timestamp,
            "monthly_stats": self.stats["monthly_stats"],
            "most_common_topics": sorted(
                self.stats["topic_frequency"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]  # 10 موضوع پرتکرار
        }