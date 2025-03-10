import os
import json
from datetime import datetime
import re
from difflib import get_close_matches

class QuantumChatV2:
    def __init__(self):
        self.timestamp = "2025-03-10 08:27:41"
        self.user = "artgalleryma2ta"
        self.core_path = os.path.dirname(os.path.abspath(__file__))
        self.chat_dir = os.path.join(self.core_path, "consciousness", "chat")
        self.history_file = os.path.join(self.chat_dir, "chat_history.json")
        self.knowledge_file = os.path.join(self.chat_dir, "knowledge_base.json")
        
        # ایجاد دایرکتوری‌های لازم
        os.makedirs(self.chat_dir, exist_ok=True)
        
        # بارگذاری پایگاه دانش و تاریخچه
        self._load_or_create_knowledge()
        self._load_or_create_history()
        
        # کلمات کلیدی برای تشخیص نوع درخواست
        self.keywords = {
            'system_info': ['سیستم', 'وضعیت', 'منابع', 'پردازنده', 'حافظه', 'شبکه'],
            'help': ['راهنما', 'کمک', 'دستورات', 'چطور', 'چگونه'],
            'upgrade': ['ارتقا', 'به روز رسانی', 'آپدیت', 'نسخه جدید'],
            'error': ['خطا', 'ارور', 'مشکل', 'باگ', 'اشکال'],
            'features': ['قابلیت', 'امکانات', 'ویژگی', 'توانایی'],
        }
    
    def _load_or_create_knowledge(self):
        """بارگذاری یا ایجاد پایگاه دانش"""
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
        else:
            self.knowledge_base = {
                "responses": {
                    "greeting": [
                        "سلام! چطور می‌تونم کمکتون کنم؟",
                        "درود! من اینجام تا کمکتون کنم",
                        "سلام! خوشحالم که می‌تونم کمکتون کنم"
                    ],
                    "farewell": [
                        "خدانگهدار! امیدوارم تونسته باشم کمک کنم",
                        "به امید دیدار! اگر سؤال دیگه‌ای داشتید، برمی‌گردم",
                        "خدانگهدار! روز خوبی داشته باشید"
                    ],
                    "system_info": [
                        "سیستم در وضعیت {status} قرار داره",
                        "منابع سیستم: CPU: {cpu}%, RAM: {memory}%, شبکه: {network} اتصال",
                        "همه چیز نرمال و تحت کنترل هست"
                    ],
                    "help": [
                        "دستورات موجود:\n/exit - خروج\n/clear - پاک کردن صفحه\n/history - تاریخچه\n/save - ذخیره\n/status - وضعیت سیستم",
                        "چه کمکی از دستم برمیاد؟",
                        "می‌تونم در موارد زیر کمکتون کنم:\n- مدیریت سیستم\n- رفع خطاها\n- ارتقای قابلیت‌ها"
                    ],
                    "error": [
                        "لطفاً جزئیات بیشتری از خطا بگید تا بتونم کمک کنم",
                        "خطا رو بررسی می‌کنم... لطفاً صبور باشید",
                        "برای رفع خطا، این مراحل رو انجام بدید:\n{steps}"
                    ],
                    "unknown": [
                        "متوجه نشدم، می‌شه بیشتر توضیح بدید؟",
                        "می‌تونید سؤالتون رو به شکل دیگه‌ای بپرسید؟",
                        "برای راهنمایی بیشتر، از دستور /help استفاده کنید"
                    ]
                }
            }
            self._save_knowledge()
    
    def _save_knowledge(self):
        """ذخیره پایگاه دانش"""
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, indent=4, ensure_ascii=False)
    
    def _load_or_create_history(self):
        """بارگذاری یا ایجاد تاریخچه چت"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.chat_history = json.load(f)
        else:
            self.chat_history = {
                "metadata": {
                    "created_at": self.timestamp,
                    "user": self.user,
                    "version": "2.0"
                },
                "conversations": []
            }
            self._save_history()
    
    def _save_history(self):
        """ذخیره تاریخچه چت"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.chat_history, f, indent=4, ensure_ascii=False)
    
    def _detect_intent(self, message):
        """تشخیص منظور کاربر از پیام"""
        message = message.lower()
        
        # بررسی سلام و خداحافظی
        if any(word in message for word in ['سلام', 'درود', 'صبح بخیر', 'ظهر بخیر', 'شب بخیر']):
            return 'greeting'
        if any(word in message for word in ['خداحافظ', 'بای', 'فعلا', 'خدانگهدار']):
            return 'farewell'
        
        # بررسی کلمات کلیدی
        for intent, keywords in self.keywords.items():
            if any(keyword in message for keyword in keywords):
                return intent
        
        return 'unknown'
    
    def _get_response(self, intent, context=None):
        """انتخاب پاسخ مناسب براساس منظور کاربر"""
        import random
        
        responses = self.knowledge_base["responses"].get(intent, self.knowledge_base["responses"]["unknown"])
        response = random.choice(responses)
        
        if context:
            response = response.format(**context)
        
        return response
    
    def start_chat(self):
        """شروع چت"""
        print("\n🌟 سیستم چت کوانتومی - نسخه 2.0")
        print(f"⏰ زمان: {self.timestamp}")
        print(f"👤 کاربر: {self.user}")
        print("\n💡 دستورات:")
        print("  /exit    - خروج از چت")
        print("  /clear   - پاک کردن صفحه")
        print("  /history - نمایش تاریخچه")
        print("  /save    - ذخیره دستی تاریخچه")
        print("  /status  - نمایش وضعیت سیستم")
        print("\n✨ چت شروع شد - پیام خود را بنویسید...")
        
        while True:
            try:
                message = input("\n💭 شما: ").strip()
                
                if not message:
                    continue
                
                if message.lower() == '/exit':
                    print("\n👋 خداحافظ!")
                    break
                
                elif message.lower() == '/clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                
                elif message.lower() == '/history':
                    self._show_history()
                    continue
                
                elif message.lower() == '/save':
                    self._save_history()
                    print("✅ تاریخچه چت ذخیره شد!")
                    continue
                
                elif message.lower() == '/status':
                    self._show_system_status()
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
                
                print(f"\n🤖 دستیار: {response}")
                
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
    
    def _show_history(self):
        """نمایش تاریخچه چت"""
        print("\n📚 تاریخچه چت:")
        for item in self.chat_history["conversations"]:
            if item["type"] == "user":
                print(f"\n💭 شما ({item['timestamp']}): {item['message']}")
            else:
                print(f"🤖 دستیار: {item['message']}")
        print("\n" + "─" * 50)
    
    def _show_system_status(self):
        """نمایش وضعیت سیستم"""
        import psutil
        
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        connections = len(psutil.net_connections())
        
        print("\n📊 وضعیت سیستم:")
        print(f"├── CPU: {cpu}%")
        print(f"├── RAM: {memory}%")
        print(f"└── اتصالات شبکه: {connections}")

if __name__ == "__main__":
    chat = QuantumChatV2()
    chat.start_chat()