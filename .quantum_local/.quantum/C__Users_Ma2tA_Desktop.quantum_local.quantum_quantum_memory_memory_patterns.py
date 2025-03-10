import re
from typing import List, Dict, Set
import hashlib
from datetime import datetime

class QuantumMemoryPatterns:
    def __init__(self, memory):
        self.memory = memory
        self.timestamp = "2025-03-10 09:59:12"
        self.patterns_file = f"{memory.data_dir}/memory_patterns.json"
        self.load_patterns()
    
    def load_patterns(self):
        """بارگذاری الگوها"""
        self.patterns = self.memory._load_json(self.patterns_file, {
            "text_patterns": [],
            "question_patterns": [],
            "response_patterns": [],
            "topic_patterns": [],
            "pattern_relations": {},
            "pattern_stats": {
                "total": 0,
                "questions": 0,
                "responses": 0,
                "topics": 0
            },
            "last_update": self.timestamp
        })
    
    def save_patterns(self):
        """ذخیره الگوها"""
        self.patterns["last_update"] = self.timestamp
        self.memory._save_json(self.patterns_file, self.patterns)
    
    def extract_keywords(self, text: str) -> List[str]:
        """استخراج کلمات کلیدی"""
        stop_words = {
            "و", "در", "به", "از", "که", "این", "را", "با", "است", "برای", 
            "آن", "هم", "یا", "اما", "ولی", "پس", "چون", "زیرا", "اگر",
            "تا", "کنید", "کنم", "کند", "شود", "شد", "یک", "دو", "سه",
            "چهار", "پنج", "می", "های", "ها", "تر", "ترین", "شده"
        }
        
        # حذف کاراکترهای خاص و تقسیم به کلمات
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if len(word) > 2 and word not in stop_words]
    
    def extract_patterns(self, results: List[Dict[str, str]]) -> List[str]:
        """استخراج الگوهای متنی"""
        patterns = []
        for result in results:
            text = f"{result['title']} {result['snippet']}"
            
            # الگوهای تعریف
            definitions = re.findall(r'([^.!?]+(است|می‌باشد|یعنی|عبارت است از)[^.!?]+)[.!?]', text)
            patterns.extend([d[0] for d in definitions])
            
            # الگوهای مثال
            examples = re.findall(r'([^.!?]+(مثلاً|برای مثال|مانند|نظیر)[^.!?]+)[.!?]', text)
            patterns.extend([e[0] for e in examples])
            
            # الگوهای روش
            methods = re.findall(r'([^.!?]+(روش|چگونه|چطور|نحوه)[^.!?]+)[.!?]', text)
            patterns.extend([m[0] for m in methods])
            
            # الگوهای توصیه
            advice = re.findall(r'([^.!?]+(باید|نباید|می‌توان|بهتر است)[^.!?]+)[.!?]', text)
            patterns.extend([a[0] for a in advice])
            
            # الگوهای دسته‌بندی
            categories = re.findall(r'([^.!?]+(انواع|دسته|گروه|تقسیم می‌شود به)[^.!?]+)[.!?]', text)
            patterns.extend([c[0] for c in categories])
            
            # الگوهای مقایسه
            comparisons = re.findall(r'([^.!?]+(در مقایسه با|برخلاف|نسبت به)[^.!?]+)[.!?]', text)
            patterns.extend([c[0] for c in comparisons])
        
        return list(set(pattern for pattern in patterns if pattern))
    
    def learn_new_patterns(self, message: str, response: str):
        """یادگیری الگوهای جدید از مکالمه"""
        message_hash = hashlib.sha256(message.encode()).hexdigest()
        response_hash = hashlib.sha256(response.encode()).hexdigest()
        
        # الگوهای سؤال
        if "?" in message or any(word in message.lower() for word in [
            "چطور", "چگونه", "آیا", "چرا", "کی", "کجا", "چه", "چند",
            "کدام", "چیست", "کجاست", "چرا"
        ]):
            self.patterns["question_patterns"].append({
                "timestamp": self.timestamp,
                "pattern": message,
                "hash": message_hash,
                "keywords": self.extract_keywords(message),
                "type": self._detect_question_type(message)
            })
            self.patterns["pattern_stats"]["questions"] += 1
        
        # الگوهای پاسخ
        self.patterns["response_patterns"].append({
            "timestamp": self.timestamp,
            "pattern": response,
            "hash": response_hash,
            "keywords": self.extract_keywords(response),
            "type": self._detect_response_type(response)
        })
        self.patterns["pattern_stats"]["responses"] += 1
        
        # ایجاد ارتباط بین سؤال و پاسخ
        self.patterns["pattern_relations"][message_hash] = {
            "response_hash": response_hash,
            "timestamp": self.timestamp,
            "frequency": 1
        }
        
        self.patterns["pattern_stats"]["total"] += 2
        self.save_patterns()
    
    def learn_from_results(self, results: List[Dict[str, str]]):
        """یادگیری الگوها از نتایج جستجو"""
        new_patterns = self.extract_patterns(results)
        
        for pattern in new_patterns:
            pattern_hash = hashlib.sha256(pattern.encode()).hexdigest()
            
            # افزودن به الگوهای متنی
            self.patterns["text_patterns"].append({
                "timestamp": self.timestamp,
                "pattern": pattern,
                "hash": pattern_hash,
                "keywords": self.extract_keywords(pattern),
                "type": self._detect_pattern_type(pattern)
            })
            
            # افزودن به الگوهای موضوعی اگر مرتبط باشد
            if self._is_topic_pattern(pattern):
                self.patterns["topic_patterns"].append({
                    "timestamp": self.timestamp,
                    "pattern": pattern,
                    "hash": pattern_hash,
                    "keywords": self.extract_keywords(pattern)
                })
                self.patterns["pattern_stats"]["topics"] += 1
        
        self.patterns["pattern_stats"]["total"] += len(new_patterns)
        self.save_patterns()
    
    def calculate_similarity(self, query: str, topic_data: Dict) -> float:
        """محاسبه میزان شباهت بین پرسش و موضوع"""
        # شباهت کلمات کلیدی
        query_keywords = set(self.extract_keywords(query))
        topic_keywords = set(topic_data["keywords"])
        
        keyword_similarity = len(query_keywords & topic_keywords) / len(query_keywords | topic_keywords) if query_keywords or topic_keywords else 0
        
        # شباهت الگوها
        query_patterns = set(self.extract_patterns([{"title": query, "snippet": query}]))
        topic_patterns = set(topic_data["patterns"])
        
        pattern_similarity = len(query_patterns & topic_patterns) / len(query_patterns | topic_patterns) if query_patterns or topic_patterns else 0
        
        # محاسبه میانگین وزن‌دار
        return (keyword_similarity * 0.6) + (pattern_similarity * 0.4)
    
    def _detect_question_type(self, question: str) -> str:
        """تشخیص نوع سؤال"""
        question = question.lower()
        
        if any(word in question for word in ["چطور", "چگونه", "روش", "نحوه"]):
            return "how"
        elif any(word in question for word in ["چرا", "دلیل", "علت"]):
            return "why"
        elif any(word in question for word in ["آیا", "هست", "دارد"]):
            return "yes_no"
        elif any(word in question for word in ["کجا", "محل", "مکان"]):
            return "where"
        elif any(word in question for word in ["کی", "چه زمانی", "زمان"]):
            return "when"
        elif any(word in question for word in ["چه", "چیست", "کدام"]):
            return "what"
        elif any(word in question for word in ["چند", "مقدار", "تعداد"]):
            return "how_many"
        else:
            return "other"
    
    def _detect_response_type(self, response: str) -> str:
        """تشخیص نوع پاسخ"""
        response = response.lower()
        
        if any(word in response for word in ["است", "می‌باشد", "یعنی"]):
            return "definition"
        elif any(word in response for word in ["مثلاً", "برای مثال", "مانند"]):
            return "example"
        elif any(word in response for word in ["روش", "مراحل", "ابتدا"]):
            return "procedure"
        elif any(word in response for word in ["باید", "نباید", "توصیه"]):
            return "advice"
        elif any(word in response for word in ["انواع", "دسته", "گروه"]):
            return "category"
        else:
            return "information"
    
    def _detect_pattern_type(self, pattern: str) -> str:
        """تشخیص نوع الگو"""
        pattern = pattern.lower()
        
        if any(word in pattern for word in ["است", "می‌باشد", "یعنی"]):
            return "definition"
        elif any(word in pattern for word in ["مثلاً", "برای مثال", "مانند"]):
            return "example"
        elif any(word in pattern for word in ["روش", "چگونه", "چطور"]):
            return "method"
        elif any(word in pattern for word in ["باید", "نباید", "می‌توان"]):
            return "advice"
        elif any(word in pattern for word in ["انواع", "دسته", "گروه"]):
            return "category"
        elif any(word in pattern for word in ["در مقایسه", "برخلاف", "نسبت به"]):
            return "comparison"
        else:
            return "general"
    
    def _is_topic_pattern(self, pattern: str) -> bool:
        """بررسی اینکه آیا الگو مربوط به موضوع است"""
        return any(word in pattern.lower() for word in [
            "است", "می‌باشد", "یعنی", "عبارت است از",
            "انواع", "دسته", "گروه", "تقسیم می‌شود",
            "در مقایسه با", "برخلاف", "نسبت به"
        ])
    
    def get_pattern_stats(self) -> Dict:
        """دریافت آمار الگوها"""
        return {
            "total_patterns": self.patterns["pattern_stats"]["total"],
            "question_patterns": self.patterns["pattern_stats"]["questions"],
            "response_patterns": self.patterns["pattern_stats"]["responses"],
            "topic_patterns": self.patterns["pattern_stats"]["topics"],
            "last_update": self.patterns["last_update"]
        }