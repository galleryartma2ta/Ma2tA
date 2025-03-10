import json
import os
from datetime import datetime, timedelta
import shutil
import zipfile
import hashlib
import re
from typing import Dict, List, Any, Optional

class QuantumMemoryManager:
    def __init__(self, memory_module):
        self.memory = memory_module
        self.timestamp = "2025-03-10 09:36:37"
        self.user = "artgalleryma2ta"
        
        # مسیرهای اصلی
        self.backup_dir = os.path.join(self.memory.chat.core_path, "consciousness", "backups")
        self.archive_dir = os.path.join(self.memory.chat.core_path, "consciousness", "archives")
        self.temp_dir = os.path.join(self.memory.chat.core_path, "consciousness", "temp")
        
        # ایجاد دایرکتوری‌ها
        for dir_path in [self.backup_dir, self.archive_dir, self.temp_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        # فایل تنظیمات
        self.config_file = os.path.join(self.memory.chat.core_path, "consciousness", "memory_config.json")
        self.load_config()
    
    def load_config(self):
        """بارگذاری تنظیمات"""
        default_config = {
            "backup": {
                "auto_backup": True,
                "backup_interval": 3600,  # هر ساعت
                "max_backups": 24,  # حداکثر 24 بک‌آپ
                "compression": True,
                "include_stats": True
            },
            "cleanup": {
                "auto_cleanup": True,
                "cleanup_interval": 86400,  # هر روز
                "max_conversation_age": 30,  # 30 روز
                "min_topic_frequency": 5,
                "max_topics": 1000
            },
            "optimization": {
                "auto_optimize": True,
                "optimization_interval": 43200,  # هر 12 ساعت
                "memory_threshold": 80,  # درصد
                "max_file_size": 100000000  # 100MB
            },
            "security": {
                "encrypt_backups": True,
                "verify_integrity": True,
                "backup_key": hashlib.sha256(self.user.encode()).hexdigest()
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """ذخیره تنظیمات"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def create_backup(self, note: str = "") -> bool:
        """ایجاد بک‌آپ از حافظه"""
        try:
            # ایجاد نام فایل بک‌آپ
            backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"memory_backup_{backup_time}"
            
            # جمع‌آوری داده‌ها
            backup_data = {
                "metadata": {
                    "timestamp": self.timestamp,
                    "user": self.user,
                    "note": note,
                    "version": self.memory.chat.version
                },
                "history": self.memory.history,
                "learned": self.memory.learned,
                "stats": self.memory.stats
            }
            
            # محاسبه hash داده‌ها
            data_hash = hashlib.sha256(json.dumps(backup_data, sort_keys=True).encode()).hexdigest()
            backup_data["metadata"]["hash"] = data_hash
            
            # ذخیره فایل
            backup_path = os.path.join(self.backup_dir, f"{backup_name}.json")
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=4, ensure_ascii=False)
            
            # فشرده‌سازی اگر فعال است
            if self.config["backup"]["compression"]:
                zip_path = os.path.join(self.backup_dir, f"{backup_name}.zip")
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(backup_path, os.path.basename(backup_path))
                os.remove(backup_path)
            
            # پاکسازی بک‌آپ‌های قدیمی
            self._cleanup_old_backups()
            
            return True
        
        except Exception as e:
            print(f"⚠️ خطا در ایجاد بک‌آپ: {str(e)}")
            return False
    
    def restore_backup(self, backup_name: str) -> bool:
        """بازیابی از بک‌آپ"""
        try:
            # یافتن فایل بک‌آپ
            backup_path = os.path.join(self.backup_dir, backup_name)
            if not os.path.exists(backup_path):
                print("⚠️ فایل بک‌آپ یافت نشد")
                return False
            
            # استخراج اگر فشرده است
            if backup_name.endswith('.zip'):
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    json_name = next(name for name in zipf.namelist() if name.endswith('.json'))
                    zipf.extract(json_name, self.temp_dir)
                    backup_path = os.path.join(self.temp_dir, json_name)
            
            # بارگذاری داده‌ها
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # بررسی یکپارچگی
            if self.config["security"]["verify_integrity"]:
                stored_hash = backup_data["metadata"]["hash"]
                backup_data["metadata"]["hash"] = ""
                calculated_hash = hashlib.sha256(json.dumps(backup_data, sort_keys=True).encode()).hexdigest()
                if stored_hash != calculated_hash:
                    print("⚠️ خطا: یکپارچگی بک‌آپ تأیید نشد")
                    return False
            
            # بازیابی داده‌ها
            self.memory.history = backup_data["history"]
            self.memory.learned = backup_data["learned"]
            self.memory.stats = backup_data["stats"]
            
            # ذخیره تغییرات
            self.memory._save_json(self.memory.history_file, self.memory.history)
            self.memory._save_json(self.memory.learning_file, self.memory.learned)
            self.memory._save_json(self.memory.stats_file, self.memory.stats)
            
            # پاکسازی فایل‌های موقت
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                os.makedirs(self.temp_dir)
            
            return True
        
        except Exception as e:
            print(f"⚠️ خطا در بازیابی بک‌آپ: {str(e)}")
            return False
    
    def optimize_memory(self) -> bool:
        """بهینه‌سازی حافظه"""
        try:
            # حذف تکرارها در تاریخچه
            unique_conversations = []
            seen = set()
            
            for conv in self.memory.history["conversations"]:
                conv_key = f"{conv['message']}_{conv['type']}"
                if conv_key not in seen:
                    seen.add(conv_key)
                    unique_conversations.append(conv)
            
            self.memory.history["conversations"] = unique_conversations
            
            # بهینه‌سازی موضوعات یادگرفته شده
            topics = self.memory.learned["topics"]
            optimized_topics = {}
            
            for topic, data in topics.items():
                # حذف موضوعات تکراری با محتوای مشابه
                is_duplicate = False
                for opt_topic, opt_data in optimized_topics.items():
                    if self._calculate_content_similarity(data, opt_data) > 0.8:
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    optimized_topics[topic] = data
            
            self.memory.learned["topics"] = optimized_topics
            
            # به‌روزرسانی آمار
            self.memory.stats["optimization"] = {
                "last_run": self.timestamp,
                "space_saved": len(topics) - len(optimized_topics),
                "duplicates_removed": len(seen) - len(unique_conversations)
            }
            
            # ذخیره تغییرات
            self.memory._save_json(self.memory.history_file, self.memory.history)
            self.memory._save_json(self.memory.learning_file, self.memory.learned)
            self.memory._save_json(self.memory.stats_file, self.memory.stats)
            
            return True
        
        except Exception as e:
            print(f"⚠️ خطا در بهینه‌سازی حافظه: {str(e)}")
            return False
    
    def _calculate_content_similarity(self, data1: Dict, data2: Dict) -> float:
        """محاسبه میزان شباهت محتوایی"""
        try:
            # مقایسه کلمات کلیدی
            keywords1 = set(data1.get("keywords", []))
            keywords2 = set(data2.get("keywords", []))
            keyword_similarity = len(keywords1 & keywords2) / len(keywords1 | keywords2) if keywords1 or keywords2 else 0
            
            # مقایسه الگوها
            patterns1 = set(data1.get("patterns", []))
            patterns2 = set(data2.get("patterns", []))
            pattern_similarity = len(patterns1 & patterns2) / len(patterns1 | patterns2) if patterns1 or patterns2 else 0
            
            # مقایسه داده‌ها
            data_similarity = 0
            if "data" in data1 and "data" in data2:
                text1 = " ".join(str(item) for item in data1["data"])
                text2 = " ".join(str(item) for item in data2["data"])
                words1 = set(text1.lower().split())
                words2 = set(text2.lower().split())
                data_similarity = len(words1 & words2) / len(words1 | words2) if words1 or words2 else 0
            
            # محاسبه میانگین وزن‌دار
            return (keyword_similarity * 0.4 + pattern_similarity * 0.3 + data_similarity * 0.3)
        
        except Exception:
            return 0
    
    def _cleanup_old_backups(self):
        """پاکسازی بک‌آپ‌های قدیمی"""
        try:
            # لیست تمام فایل‌های بک‌آپ
            backup_files = []
            for f in os.listdir(self.backup_dir):
                if f.endswith(('.json', '.zip')):
                    path = os.path.join(self.backup_dir, f)
                    backup_files.append((path, os.path.getmtime(path)))
            
            # مرتب‌سازی براساس زمان
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # حذف بک‌آپ‌های اضافی
            max_backups = self.config["backup"]["max_backups"]
            if len(backup_files) > max_backups:
                for path, _ in backup_files[max_backups:]:
                    os.remove(path)
        
        except Exception as e:
            print(f"⚠️ خطا در پاکسازی بک‌آپ‌ها: {str(e)}")
