import os
import json
import glob
from datetime import datetime

class QuantumTimeSync:
    def __init__(self):
        self.current_time = "2025-03-10 07:52:35"  # زمان فعلی UTC
        self.user = "artgalleryma2ta"
        self.core_path = os.path.dirname(os.path.abspath(__file__))
    
    def sync_all_timestamps(self):
        print("\n🕒 Quantum Time Synchronization")
        print(f"⏰ Current Time (UTC): {self.current_time}")
        print(f"👤 User: {self.user}")
        
        # همه فایل‌های JSON را پیدا می‌کنیم
        json_files = []
        for root, dirs, files in os.walk(self.core_path):
            for file in files:
                if file.endswith('.json'):
                    json_files.append(os.path.join(root, file))
        
        print(f"\n📊 Found {len(json_files)} files to synchronize")
        
        # همگام‌سازی timestamp در همه فایل‌ها
        synced_files = 0
        for file_path in json_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, dict):
                    if "timestamp" in data:
                        data["timestamp"] = self.current_time
                        
                        # به‌روزرسانی timestamp های تو در تو
                        self._update_nested_timestamps(data)
                        
                        with open(file_path, 'w') as f:
                            json.dump(data, f, indent=4)
                        
                        rel_path = os.path.relpath(file_path, self.core_path)
                        print(f"✅ Synchronized: {rel_path}")
                        synced_files += 1
            
            except Exception as e:
                rel_path = os.path.relpath(file_path, self.core_path)
                print(f"⚠️ Error syncing {rel_path}: {str(e)}")
        
        # به‌روزرسانی فایل‌های کانفیگ اصلی
        self._update_main_configs()
        
        print(f"\n✨ Time synchronization completed!")
        print(f"📊 Synchronized {synced_files} files")
    
    def _update_nested_timestamps(self, data):
        """به‌روزرسانی timestamp های تو در تو در دیکشنری"""
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "timestamp":
                    data[key] = self.current_time
                elif isinstance(value, (dict, list)):
                    self._update_nested_timestamps(value)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self._update_nested_timestamps(item)
    
    def _update_main_configs(self):
        """به‌روزرسانی فایل‌های کانفیگ اصلی"""
        main_configs = {
            "run.py": {"timestamp_var": "self.timestamp"},
            "quantum_core_system.py": {"timestamp_var": "self.timestamp"},
            "system_monitor.py": {"timestamp_var": "self.timestamp"},
            "quantum_logger.py": {"timestamp_var": "self.timestamp"}
        }
        
        print("\n🔄 Updating main configuration files...")
        
        for filename, config in main_configs.items():
            file_path = os.path.join(self.core_path, filename)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # جایگزینی timestamp در متغیرهای مشخص شده
                    for var_name in config.values():
                        old_timestamp = f'{var_name} = "20[0-9][0-9]-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]"'
                        new_timestamp = f'{var_name} = "{self.current_time}"'
                        content = content.replace(old_timestamp, new_timestamp)
                    
                    with open(file_path, 'w') as f:
                        f.write(content)
                    
                    print(f"✅ Updated timestamps in: {filename}")
                
                except Exception as e:
                    print(f"⚠️ Error updating {filename}: {str(e)}")
        
        print("\n💡 Note: Please restart the system for time sync to take full effect")

if __name__ == "__main__":
    sync = QuantumTimeSync()
    sync.sync_all_timestamps()