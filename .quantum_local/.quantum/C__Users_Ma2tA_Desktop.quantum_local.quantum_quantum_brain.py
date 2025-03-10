import json
import time
from datetime import datetime
from collections import Counter

class QuantumBrain:
    def __init__(self, chat):
        self.chat = chat
        self.knowledge_file = f"{chat.knowledge_dir}/knowledge_base.json"
        self.load_knowledge()
    
    def load_knowledge(self):
        """بارگذاری پایگاه دانش"""
        try:
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge = json.load(f)
        except:
            self.knowledge = {
                "responses": {
                    "greeting": ["سلام! چطور می‌تونم کمکتون کنم؟"],
                    "unknown": ["متوجه نشدم، می‌شه بیشتر توضیح بدید؟"]
                },
                "keywords": {
                    "greeting": ["سلام", "درود", "صبح بخیر"],
                    "help": ["کمک", "راهنمایی", "چطور"]
                }
            }
            self.save_knowledge()
    
    def save_knowledge(self):
        """ذخیره پایگاه دانش"""
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, indent=4, ensure_ascii=False)
    
    def detect_intent(self, message):
        """تشخیص منظور کاربر"""
        message = message.lower()
        
        for intent, keywords in self.knowledge["keywords"].items():
            if any(keyword in message for keyword in keywords):
                return intent
        
        return "unknown"
    
    def get_default_response(self, message):
        """تولید پاسخ پیش‌فرض"""
        import random
        intent = self.detect_intent(message)
        responses = self.knowledge["responses"].get(intent, self.knowledge["responses"]["unknown"])
        return random.choice(responses)
    
    def process_command(self, message):
        """پردازش دستورات سیستمی"""
        command = message[1:].lower()
        
        if command == "exit":
            return "exit"
        elif command == "help":
            return self.show_help()
        elif command == "status":
            return self.show_status()
        
        return None
    
    def background_learning(self):
        """یادگیری در پس‌زمینه"""
        while self.chat.learning_active:
            try:
                # استخراج موضوعات پرتکرار
                topics = self.extract_common_topics()
                
                # یادگیری موضوعات جدید
                for topic in topics:
                    self.chat.web.learn_topic(topic)
                
                # به‌روزرسانی دانش قدیمی
                self.update_old_knowledge()
                
                time.sleep(3600)  # هر ساعت یکبار
            
            except Exception as e:
                print(f"⚠️ خطا در یادگیری پس‌زمینه: {str(e)}")
                time.sleep(300)
    
    def extract_common_topics(self):
        """استخراج موضوعات پرتکرار"""
        recent_messages = [
            conv["message"] 
            for conv in self.chat.memory.get_recent_conversations(100)
            if conv["type"] == "user"
        ]
        
        words = []
        for message in recent_messages:
            words.extend([word for word in message.lower().split() if len(word) > 3])
        
        return [word for word, _ in Counter(words).most_common(5)]
    
    def update_old_knowledge(self):
        """به‌روزرسانی دانش قدیمی"""
        old_topics = self.chat.memory.get_old_topics(days=7)
        for topic in old_topics:
            self.chat.web.learn_topic(topic)
    
    def show_help(self):
        """نمایش راهنما"""
        return """
💡 دستورات موجود:
├── /exit    - خروج از چت
├── /help    - نمایش این راهنما
├── /status  - وضعیت سیستم
└── /save    - ذخیره تاریخچه"""
    
    def show_status(self):
        """نمایش وضعیت سیستم"""
        import psutil
        
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return f"""
📊 وضعیت سیستم:
├── CPU: {cpu}%
├── RAM: استفاده شده {memory.percent}%
├── حافظه کل: {memory.total/1024/1024/1024:.1f} GB
├── دیسک: استفاده شده {disk.percent}%
└── فضای آزاد: {disk.free/1024/1024/1024:.1f} GB"""