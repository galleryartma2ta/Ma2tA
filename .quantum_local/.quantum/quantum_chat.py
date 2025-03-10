import os
import json
from datetime import datetime
import re

class QuantumChat:
    def __init__(self):
        self.timestamp = "2025-03-10 08:24:33"
        self.user = "artgalleryma2ta"
        self.core_path = os.path.dirname(os.path.abspath(__file__))
        self.chat_dir = os.path.join(self.core_path, "consciousness", "chat")
        self.history_file = os.path.join(self.chat_dir, "chat_history.json")
        
        # ایجاد دایرکتوری چت
        os.makedirs(self.chat_dir, exist_ok=True)
        
        # ایجاد یا بارگذاری تاریخچه چت
        self._load_or_create_history()
    
    def _load_or_create_history(self):
        """بارگذاری یا ایجاد فایل تاریخچه چت"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.chat_history = json.load(f)
        else:
            self.chat_history = {
                "metadata": {
                    "created_at": self.timestamp,
                    "user": self.user,
                    "version": "1.0"
                },
                "conversations": []
            }
            self._save_history()
    
    def _save_history(self):
        """ذخیره تاریخچه چت"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.chat_history, f, indent=4, ensure_ascii=False)
    
    def start_chat(self):
        """شروع چت"""
        print("\n🌟 Quantum Chat System")
        print(f"⏰ Time: {self.timestamp}")
        print(f"👤 User: {self.user}")
        print("\n💡 Commands:")
        print("  /exit    - خروج از چت")
        print("  /clear   - پاک کردن صفحه")
        print("  /history - نمایش تاریخچه")
        print("  /save    - ذخیره دستی تاریخچه")
        print("\n✨ Chat started - send your message...")
        
        while True:
            try:
                message = input("\n🤔 You: ").strip()
                
                if not message:
                    continue
                
                if message.lower() == '/exit':
                    print("\n👋 Goodbye!")
                    break
                
                elif message.lower() == '/clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                
                elif message.lower() == '/history':
                    self._show_history()
                    continue
                
                elif message.lower() == '/save':
                    self._save_history()
                    print("✅ Chat history saved!")
                    continue
                
                # ذخیره پیام در تاریخچه
                self.chat_history["conversations"].append({
                    "timestamp": self.timestamp,
                    "user": self.user,
                    "message": message,
                    "type": "user"
                })
                
                # ذخیره خودکار بعد از هر پیام
                self._save_history()
                
                # اینجا می‌تونیم منطق پردازش پیام و پاسخ رو اضافه کنیم
                response = self._process_message(message)
                print(f"\n🤖 Assistant: {response}")
                
                # ذخیره پاسخ در تاریخچه
                self.chat_history["conversations"].append({
                    "timestamp": self.timestamp,
                    "user": "assistant",
                    "message": response,
                    "type": "assistant"
                })
                
                # ذخیره خودکار بعد از هر پاسخ
                self._save_history()
            
            except KeyboardInterrupt:
                print("\n\n⚠️ Chat interrupted")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
    
    def _process_message(self, message):
        """پردازش پیام کاربر و تولید پاسخ"""
        # در اینجا می‌تونیم منطق پردازش پیام و پاسخ‌دهی رو پیاده‌سازی کنیم
        # فعلاً یک پاسخ ساده برمی‌گردونیم
        return "پیام شما دریافت شد. در حال توسعه سیستم پاسخ‌دهی هستم..."
    
    def _show_history(self):
        """نمایش تاریخچه چت"""
        print("\n📚 Chat History:")
        for item in self.chat_history["conversations"]:
            if item["type"] == "user":
                print(f"\n🤔 You ({item['timestamp']}): {item['message']}")
            else:
                print(f"🤖 Assistant: {item['message']}")
        print("\n" + "─" * 50)

if __name__ == "__main__":
    chat = QuantumChat()
    chat.start_chat()