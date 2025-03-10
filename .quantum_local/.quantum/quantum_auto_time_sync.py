import os
import json
import re
from datetime import datetime
import threading
import time

class QuantumAutoTimeSync:
    def __init__(self):
        self.current_time = "2025-03-10 08:19:50"  # زمان دقیق فعلی UTC
        self.user = "artgalleryma2ta"
        self.core_path = os.path.dirname(os.path.abspath(__file__))
        self.sync_interval = 60  # همگام‌سازی هر 60 ثانیه
        self.sync_active = False
        self.last_sync = None
        
        # بک‌آپ از آخرین زمان همگام‌سازی
        self.backup_file = os.path.join(self.core_path, "core", "time_sync_backup.json")
    
    def start_auto_sync(self):
        print(f"\n🕒 Starting Quantum Auto Time Sync")
        print(f"⏰ Current Time (UTC): {self.current_time}")
        print(f"👤 User: {self.user}")
        
        self.sync_active = True
        
        # ذخیره وضعیت اولیه
        self._save_sync_state()
        
        # شروع همگام‌سازی خودکار در thread جداگانه
        sync_thread = threading.Thread(target=self._auto_sync_loop)
        sync_thread.daemon = True
        sync_thread.start()
        
        try:
            self._perform_full_sync()
        except Exception as e:
            print(f"\n❌ Initial sync error: {str(e)}")
    
    def _auto_sync_loop(self):
        while self.sync_active:
            try:
                time.sleep(self.sync_interval)
                
                # به‌روزرسانی زمان فعلی
                self.current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                
                # همگام‌سازی فایل‌های حیاتی
                self._quick_sync_vital_files()
                
                # ذخیره وضعیت
                self._save_sync_state()
                
                print(f"\n🔄 Auto-sync completed at {self.current_time}")
            
            except Exception as e:
                print(f"\n⚠️ Auto-sync error: {str(e)}")
    
    def _quick_sync_vital_files(self):
        """همگام‌سازی سریع فایل‌های حیاتی سیستم"""
        vital_files = [
            "run.py",
            "quantum_core_system.py",
            "system_monitor.py",
            "core/state.json",
            "monitoring/status_report.json"
        ]
        
        for file in vital_files:
            filepath = os.path.join(self.core_path, file)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # به‌روزرسانی timestamp ها
                    if file.endswith('.py'):
                        patterns = [
                            (r'self\.timestamp = "[^"]+"', f'self.timestamp = "2025-03-10 08:19:50"'),
                            (r'⏰ Time: 2025-03-10 08:19:50"\n]+', f'⏰ Time: 2025-03-10 08:19:50
                            (r'⏰ Time \(UTC\): [^"\n]+', f'⏰ Time (UTC): 2025-03-10 08:19:50
                        ]
                        
                        for pattern, replacement in patterns:
                            content = re.sub(pattern, replacement, content)
                    
                    elif file.endswith('.json'):
                        data = json.loads(content)
                        if isinstance(data, dict):
                            if "timestamp" in data:
                                data["timestamp"] = self.current_time
                            content = json.dumps(data, indent=4)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                
                except Exception as e:
                    print(f"⚠️ Quick sync error for {file}: {str(e)}")
    
    def _perform_full_sync(self):
        """همگام‌سازی کامل تمام فایل‌ها"""
        print("\n📝 Performing Full System Sync...")
        
        # 1. به‌روزرسانی فایل‌های Python
        python_files = [f for f in os.listdir(self.core_path) if f.endswith('.py')]
        for file in python_files:
            filepath = os.path.join(self.core_path, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                patterns = [
                    (r'self\.timestamp = "[^"]+"', f'self.timestamp = "2025-03-10 08:19:50"'),
                    (r'⏰ Time: 2025-03-10 08:19:50"\n]+', f'⏰ Time: 2025-03-10 08:19:50
                    (r'⏰ Time \(UTC\): [^"\n]+', f'⏰ Time (UTC): 2025-03-10 08:19:50
                ]
                
                updated = False
                for pattern, replacement in patterns:
                    new_content = re.sub(pattern, replacement, content)
                    if new_content != content:
                        content = new_content
                        updated = True
                
                if updated:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Updated: {file}")
            
            except Exception as e:
                print(f"⚠️ Error updating {file}: {str(e)}")
        
        # 2. به‌روزرسانی فایل‌های JSON
        for root, _, files in os.walk(self.core_path):
            for file in files:
                if file.endswith('.json'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                        
                        if isinstance(data, dict):
                            if self._update_timestamps_recursive(data):
                                with open(filepath, 'w') as f:
                                    json.dump(data, f, indent=4)
                                rel_path = os.path.relpath(filepath, self.core_path)
                                print(f"✅ Updated: {rel_path}")
                    
                    except Exception as e:
                        rel_path = os.path.relpath(filepath, self.core_path)
                        print(f"⚠️ Error updating {rel_path}: {str(e)}")
    
    def _update_timestamps_recursive(self, data):
        """به‌روزرسانی بازگشتی timestamp ها"""
        updated = False
        
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "timestamp" and isinstance(value, str):
                    data[key] = self.current_time
                    updated = True
                elif isinstance(value, (dict, list)):
                    if self._update_timestamps_recursive(value):
                        updated = True
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    if self._update_timestamps_recursive(item):
                        updated = True
        
        return updated
    
    def _save_sync_state(self):
        """ذخیره وضعیت همگام‌سازی"""
        state = {
            "last_sync": self.current_time,
            "sync_status": "active" if self.sync_active else "inactive",
            "sync_interval": self.sync_interval
        }
        
        os.makedirs(os.path.dirname(self.backup_file), exist_ok=True)
        with open(self.backup_file, 'w') as f:
            json.dump(state, f, indent=4)
    
    def stop_sync(self):
        """توقف همگام‌سازی خودکار"""
        self.sync_active = False
        print("\n🛑 Auto-sync stopped")
        print("💡 Run 'python run.py' to start the system")

if __name__ == "__main__":
    auto_sync = QuantumAutoTimeSync()
    try:
        auto_sync.start_auto_sync()
        print("\n⏳ Auto-sync running. Press Ctrl+C to stop...")
        
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n⚠️ Sync interrupted by user")
    finally:
        auto_sync.stop_sync()