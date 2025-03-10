import os
import json
from datetime import datetime
import threading
from quantum_brain import QuantumBrain
from quantum_web import QuantumWeb
from quantum_memory import QuantumMemory

class QuantumChatV4:
    def __init__(self):
        self.timestamp = "2025-03-10 09:32:47"
        self.user = "artgalleryma2ta"
        self.name = "کوانتوم"
        self.version = "4.0"
        
        # مسیرهای اصلی
        self.core_path = os.path.dirname(os.path.abspath(__file__))
        self.chat_dir = os.path.join(self.core_path, "consciousness", "chat")
        self.knowledge_dir = os.path.join(self.core_path, "consciousness", "knowledge")
        self.cache_dir = os.path.join(self.core_path, "consciousness", "cache")
        
        # ایجاد دایرکتوری‌ها
        for dir_path in [self.chat_dir, self.knowledge_dir, self.cache_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        # راه‌اندازی ماژول‌ها
        self.brain = QuantumBrain(self)
        self.web = QuantumWeb(self)
        self.memory = QuantumMemory(self)
        
        # شروع یادگیری در پس‌زمینه
        self.learning_active = True
        self.learning_thread = threading.Thread(target=self.brain.background_learning)
        self.learning_thread.daemon = True
        self.learning_thread.start()
    
    def process_message(self, message):
        """پردازش پیام و تولید پاسخ"""
        if message.startswith('/'):
            return self.brain.process_command(message)
        
        # جستجو در حافظه
        memory_response = self.memory.find_response(message)
        if memory_response:
            return memory_response
        
        # جستجو در وب
        web_response = self.web.search_and_learn(message)
        if web_response:
            return web_response
        
        # پاسخ پیش‌فرض
        return self.brain.get_default_response(message)
    
    def chat(self):
        """شروع چت"""
        print(f"\n🌟 {self.name} - نسخه {self.version}")
        print(f"⏰ زمان: {self.timestamp}")
        print(f"👤 کاربر: {self.user}")
        print("\n💡 قابلیت‌های جدید:")
        print("├── یادگیری از اینترنت")
        print("├── جستجوی خودکار")
        print("└── به‌روزرسانی دانش")
        print("\n✨ چت شروع شد - پیام خود را بنویسید...")
        
        while True:
            try:
                message = input("\n💭 شما: ").strip()
                
                if not message:
                    continue
                
                # پردازش پیام و دریافت پاسخ
                response = self.process_message(message)
                
                if response == "exit":
                    print("\n👋 خداحافظ!")
                    break
                elif response:
                    print(f"\n🤖 {self.name}: {response}")
                
                # ذخیره در حافظه
                self.memory.save_conversation(message, response)
            
            except KeyboardInterrupt:
                print("\n\n⚠️ چت قطع شد")
                break
            except Exception as e:
                print(f"\n❌ خطا: {str(e)}")
        
        # پایان یادگیری پس‌زمینه
        self.learning_active = False

if __name__ == "__main__":
    chat = QuantumChatV4()
    chat.chat()