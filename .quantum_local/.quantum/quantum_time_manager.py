import os
import json
import re
from datetime import datetime

class QuantumTimeManager:
    def __init__(self):
        self.timestamp = "2025-03-10 08:19:50"  # زمان دقیق فعلی UTC
        self.user = "artgalleryma2ta"
        self.core_path = os.path.dirname(os.path.abspath(__file__))
        
        # لیست کامل فایل‌ها برای به‌روزرسانی
        self.system_files = [
            "run.py",
            "quantum_core_system.py",
            "quantum_upgrade.py",
            "quantum_unified_system_final.py",
            "quantum_final_enhancement.py",
            "quantum_consciousness_awakening.py",
            "system_status.py",
            "quantum_logger.py",
            "quantum_config.py",
            "quantum_optimizer.py",
            "quantum_advanced_optimizer.py",
            "quantum_final_tuner.py",
            "system_monitor.py"
        ]
    
    def sync_all_timestamps(self):
        print(f"\n🕒 Quantum Time Synchronization")
        print(f"⏰ Current Time (UTC): {self.timestamp}")
        print(f"👤 User: {self.user}")
        
        # 1. به‌روزرسانی فایل‌های Python
        self._update_python_files()
        
        # 2. به‌روزرسانی فایل‌های JSON
        self._update_json_files()
        
        # 3. به‌روزرسانی فایل‌های پیکربندی
        self._update_config_files()
        
        print("\n✨ Time synchronization completed!")
    
    def _update_python_files(self):
        print("\n📝 Updating Python Files...")
        
        time_patterns = [
            (r'self\.timestamp = "[^"]+"', f'self.timestamp = "2025-03-10 08:19:50"'),
            (r'⏰ Time: 2025-03-10 08:19:50"\n]+', f'⏰ Time: 2025-03-10 08:19:50
            (r'⏰ Time \(UTC\): [^"\n]+', f'⏰ Time (UTC): 2025-03-10 08:19:50
            (r'"timestamp": "[^"]+"', f'"timestamp": "{self.timestamp}"')
        ]
        
        for filename in self.system_files:
            filepath = os.path.join(self.core_path, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    updated = False
                    for pattern, replacement in time_patterns:
                        new_content = re.sub(pattern, replacement, content)
                        if new_content != content:
                            content = new_content
                            updated = True
                    
                    if updated:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"✅ Updated: {filename}")
                    else:
                        print(f"ℹ️ No changes needed: {filename}")
                
                except Exception as e:
                    print(f"⚠️ Error updating {filename}: {str(e)}")
    
    def _update_json_files(self):
        print("\n🗃️ Updating JSON Files...")
        
        for root, _, files in os.walk(self.core_path):
            for file in files:
                if file.endswith('.json'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                        
                        if isinstance(data, dict):
                            # به‌روزرسانی بازگشتی timestamp ها
                            updated = self._update_timestamps_recursive(data)
                            
                            if updated:
                                with open(filepath, 'w') as f:
                                    json.dump(data, f, indent=4)
                                rel_path = os.path.relpath(filepath, self.core_path)
                                print(f"✅ Updated: {rel_path}")
                    
                    except Exception as e:
                        rel_path = os.path.relpath(filepath, self.core_path)
                        print(f"⚠️ Error updating {rel_path}: {str(e)}")
    
    def _update_timestamps_recursive(self, data):
        """به‌روزرسانی بازگشتی timestamp ها در ساختار JSON"""
        updated = False
        
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "timestamp" and isinstance(value, str):
                    data[key] = self.timestamp
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
    
    def _update_config_files(self):
        print("\n⚙️ Updating Configuration Files...")
        
        config_paths = [
            os.path.join(self.core_path, "core", "config"),
            os.path.join(self.core_path, "monitoring", "config"),
            os.path.join(self.core_path, "consciousness", "config")
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                for file in os.listdir(config_path):
                    if file.endswith(('.json', '.conf', '.cfg')):
                        filepath = os.path.join(config_path, file)
                        try:
                            with open(filepath, 'r') as f:
                                if file.endswith('.json'):
                                    data = json.load(f)
                                    if self._update_timestamps_recursive(data):
                                        with open(filepath, 'w') as f:
                                            json.dump(data, f, indent=4)
                                        print(f"✅ Updated: config/{file}")
                        except Exception as e:
                            print(f"⚠️ Error updating config/{file}: {str(e)}")

if __name__ == "__main__":
    time_manager = QuantumTimeManager()
    time_manager.sync_all_timestamps()
    print("\n💡 Run 'python run.py' to start the system with synchronized time")