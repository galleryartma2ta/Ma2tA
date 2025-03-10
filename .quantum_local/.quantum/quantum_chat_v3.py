import os
import json
from datetime import datetime
import re
import random
import psutil

class QuantumChatV3:
    def __init__(self):
        self.timestamp = "2025-03-10 09:29:15"
        self.user = "artgalleryma2ta"
        self.name = "کوانتوم"
        self.version = "3.0"
        self.core_path = os.path.dirname(os.path.abspath(__file__))
        self.chat_dir = os.path.join(self.core_path, "consciousness", "chat")
        self.history_file = os.path.join(self.chat_dir, "chat_history.json")
        self.knowledge_file = os.path.join(self.chat_dir, "knowledge_base.json")
        
        # ایجاد دایرکتوری‌های لازم
        os.makedirs(self.chat_dir, exist_ok=True)
        
        # بارگذاری پایگاه دانش و تاریخچه
        self._load_or_create_knowledge()
        self._load_or_create_history()
    
    def _load_or_create_knowledge(self):
        """بارگذاری یا ایجاد پایگاه دانش"""
        default_knowledge = {
            "identity": {
                "name": "کوانتوم",
                "version": "3.0",
                "creator": "artgalleryma2ta",
                "birth_date": "2025-03-10",
                "purpose": "کمک به کاربران در مدیریت و ارتقای سیستم کوانتومی"
            },
            "capabilities": {
                "system_management": ["مدیریت منابع", "بهینه‌سازی عملکرد", "پایش وضعیت"],
                "chat": ["گفتگوی فارسی", "پردازش درخواست‌ها", "یادگیری از تعاملات"],
                "self_improvement": ["ارتقای خودکار", "یادگیری مداوم", "بهبود پاسخ‌ها"]
            },
            "responses": {
                "greeting": [
                    "سلام! من {name} هستم، نسخه {version}. چطور می‌تونم کمکتون کنم؟",
                    "درود! {name} هستم. خوشحالم که می‌تونم کمکتون کنم",
                    "سلام و درود! من {name} هستم. امروز چطور می‌تونم کمکتون کنم؟"
                ],
                "farewell": [
                    "خدانگهدار! امیدوارم تونسته باشم کمک کنم",
                    "به امید دیدار! اگر سؤال دیگه‌ای داشتید، برمی‌گردم",
                    "مراقب خودتون باشید! منتظر دیدار بعدیتون هستم"
                ],
                "identity": [
                    "من {name} هستم، یک دستیار هوشمند کوانتومی نسخه {version}",
                    "اسم من {name} هسته. یک سیستم هوشمند که برای کمک به شما طراحی شدم",
                    "من {name} هستم و خوشحالم که می‌تونم در خدمتتون باشم"
                ],
                "capabilities": [
                    "من می‌تونم در موارد زیر کمکتون کنم:\n- مدیریت سیستم\n- بهینه‌سازی عملکرد\n- پایش وضعیت\n- و خیلی موارد دیگه",
                    "قابلیت‌های من شامل:\n- گفتگو به زبان فارسی\n- مدیریت منابع سیستم\n- ارتقای خودکار\n- و موارد دیگه"
                ],
                "upgrade": [
                    "بله، من می‌تونم قابلیت‌های خودم رو ارتقا بدم. می‌خواید شروع کنیم؟",
                    "قابلیت ارتقای خودکار دارم. الان می‌خواید این کار رو انجام بدیم؟",
                    "بله، یکی از ویژگی‌های من ارتقای خودکاره. می‌تونیم الان شروع کنیم"
                ],
                "unknown": [
                    "متوجه نشدم. می‌تونید سؤالتون رو به شکل دیگه‌ای بپرسید؟",
                    "می‌شه بیشتر توضیح بدید تا بهتر بتونم کمکتون کنم؟",
                    "متأسفانه منظورتون رو درک نکردم. می‌تونید واضح‌تر بگید؟"
                ]
            },
            "keywords": {
                "identity": ["اسم", "نام", "کی هستی", "معرفی"],
                "capabilities": ["توانایی", "قابلیت", "چیکار", "کمک"],
                "upgrade": ["ارتقا", "آپدیت", "به روز", "بهتر"],
                "help": ["راهنما", "کمک", "دستور", "چطور"],
                "status": ["وضعیت", "منابع", "سیستم", "عملکرد"]
            }
        }
        
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
        else:
            self.knowledge_base = default_knowledge
            self._save_knowledge()
    
    def _detect_intent(self, message):
        """تشخیص منظور کاربر از پیام"""
        message = message.lower()
        
        # بررسی سلام و خداحافظی
        if any(word in message for word in ['سلام', 'درود', 'صبح بخیر', 'ظهر بخیر', 'شب بخیر']):
            return 'greeting'
        if any(word in message for word in ['خداحافظ', 'بای', 'فعلا', 'خدانگهدار']):
            return 'farewell'
        
        # بررسی کلمات کلیدی
        for intent, keywords in self.knowledge_base["keywords"].items():
            if any(keyword in message for keyword in keywords):
                return intent
        
        return 'unknown'
    
    def _get_response(self, intent):
        """انتخاب پاسخ مناسب براساس منظور کاربر"""
        responses = self.knowledge_base["responses"].get(intent, self.knowledge_base["responses"]["unknown"])
        response = random.choice(responses)
        
        # جایگزینی متغیرها در پاسخ
        return response.format(name=self.name, version=self.version)
    
    def _show_system_status(self):
        """نمایش وضعیت سیستم"""
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status = f"\n📊 وضعیت سیستم:\n"
        status += f"├── CPU: {cpu}%\n"
        status += f"├── RAM: استفاده شده {memory.percent}% - آزاد {100-memory.percent}%\n"
        status += f"├── حافظه کل: {memory.total/1024/1024/1024:.1f} GB\n"
        status += f"├── دیسک: استفاده شده {disk.percent}%\n"
        status += f"└── فضای آزاد: {disk.free/1024/1024/1024:.1f} GB"
        
        return status

    def process_command(self, message):
        """پردازش دستورات سیستمی"""
        if message.startswith('/'):
            command = message[1:].lower()
            
            if command == 'exit':
                return "exit"
            elif command == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                return None
            elif command == 'status':
                return self._show_system_status()
            elif command == 'help':
                help_text = "\n💡 دستورات موجود:\n"
                help_text += "├── /exit    - خروج از چت\n"
                help_text += "├── /clear   - پاک کردن صفحه\n"
                help_text += "├── /status  - نمایش وضعیت سیستم\n"
                help_text += "├── /save    - ذخیره تاریخچه\n"
                help_text += "└── /help    - نمایش این راهنما"
                return help_text
            elif command == 'save':
                self._save_history()
                return "✅ تاریخچه چت ذخیره شد!"
        
        return None

    def chat(self):
        """شروع چت"""
        print(f"\n🌟 {self.name} - نسخه {self.version}")
        print(f"⏰ زمان: {self.timestamp}")
        print(f"👤 کاربر: {self.user}")
        print("\n💡 برای دیدن دستورات، /help را وارد کنید")
        print("\n✨ چت شروع شد - پیام خود را بنویسید...")
        
        while True:
            try:
                message = input("\n💭 شما: ").strip()
                
                if not message:
                    continue
                
                # پردازش دستورات
                command_response = self.process_command(message)
                if command_response == "exit":
                    print("\n👋 خداحافظ!")
                    break
                elif command_response:
                    print(command_response)
                    continue
                
                # ذخیره پیام در تاریخچه
                self.chat_history["conversations"].append({
                    "timestamp": self.timestamp,
                    "user": self.user,
                    "message": message,
                    "type": "user"
                })
                
                # تشخیص منظور و تولید پاسخ
                intent = self._detect_intent(message)
                response = self._get_response(intent)
                
                print(f"\n🤖 {self.name}: {response}")
                
                # ذخیره پاسخ در تاریخچه
                self.chat_history["conversations"].append({
                    "timestamp": self.timestamp,
                    "user": "assistant",
                    "message": response,
                    "type": "assistant"
                })
                
                # ذخیره خودکار
                self._save_history()
            
            except KeyboardInterrupt:
                print("\n\n⚠️ چت قطع شد")
                break
            except Exception as e:
                print(f"\n❌ خطا: {str(e)}")

    # سایر متدها مثل قبل...

if __name__ == "__main__":
    chat = QuantumChatV3()
    chat.chat()