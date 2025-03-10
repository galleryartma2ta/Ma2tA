import os
import json
import re  # اضافه کردن import برای regex
from datetime import datetime

class QuantumSystemConfig:
    def __init__(self):
        self.timestamp = "2025-03-10 08:19:50"  # به‌روزرسانی به زمان دقیق UTC
        self.user = "artgalleryma2ta"
        self.core_path = os.path.dirname(os.path.abspath(__file__))
        
        # تنظیمات پیش‌فرض سیستم
        self.default_settings = {
            'system': {
                'timestamp': self.timestamp,
                'user': self.user,
                'update_interval': 300
            },
            'memory': {
                'warning_threshold': 65.0,
                'critical_threshold': 80.0,
                'normal_range': {
                    'min': 40.0,
                    'max': 55.0
                }
            },
            'network': {
                'max_connections': 150,
                'warning_threshold': 200,
                'reserved_ports': [8080, 3000, 5000]
            },
            'optimization': {
                'auto_cleanup': True,
                'backup_enabled': True,
                'compression_enabled': True,
                'monitor_interval': 5
            }
        }
    
    def update_config(self):
        print(f"\n⚙️ Updating Quantum System Configuration")
        print(f"⏰ Time (UTC): 2025-03-10 08:19:50")
        print(f"👤 User: {self.user}")
        
        config_path = os.path.join(self.core_path, "core", "config")
        os.makedirs(config_path, exist_ok=True)
        
        # ذخیره تنظیمات
        config_file = os.path.join(config_path, "system_settings.json")
        with open(config_file, "w") as f:
            json.dump(self.default_settings, f, indent=4)
        
        print("\n✅ Configuration Updated:")
        print(f"├── Memory Normal Range: {self.default_settings['memory']['normal_range']['min']}% - {self.default_settings['memory']['normal_range']['max']}%")
        print(f"├── Memory Warning: {self.default_settings['memory']['warning_threshold']}%")
        print(f"├── Memory Critical: {self.default_settings['memory']['critical_threshold']}%")
        print(f"├── Network Max Connections: {self.default_settings['network']['max_connections']}")
        print(f"├── Network Warning Threshold: {self.default_settings['network']['warning_threshold']}")
        print(f"├── Monitor Interval: {self.default_settings['optimization']['monitor_interval']}s")
        print(f"├── Auto Cleanup: {self.default_settings['optimization']['auto_cleanup']}")
        print(f"├── Auto Backup: {self.default_settings['optimization']['backup_enabled']}")
        print(f"└── Compression: {self.default_settings['optimization']['compression_enabled']}")
        
        # به‌روزرسانی فایل‌های سیستم با مدیریت خطا بهتر
        self._update_system_files()
    
    def _update_system_files(self):
        print("\n🔄 Updating System Files...")
        
        files_to_update = [
            "quantum_advanced_optimizer.py",
            "quantum_final_tuner.py",
            "system_monitor.py",
            "run.py"
        ]
        
        for filename in files_to_update:
            filepath = os.path.join(self.core_path, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # به‌روزرسانی مقادیر با مدیریت خطا
                    replacements = {
                        r"'target':\s*\d+\.?\d*": f"'target': {self.default_settings['memory']['normal_range']['max']}",
                        r"'critical':\s*\d+\.?\d*": f"'critical': {self.default_settings['memory']['critical_threshold']}",
                        r"'max_connections':\s*\d+": f"'max_connections': {self.default_settings['network']['max_connections']}",
                        r"self\.timestamp = \"[^\"]+\"": f"self.timestamp = \"{self.timestamp}\"",
                    }
                    
                    updated_content = content
                    for old, new in replacements.items():
                        updated_content = re.sub(old, new, updated_content)
                    
                    if updated_content != content:  # تغییر کرده
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                        print(f"✅ Updated: {filename}")
                    else:
                        print(f"ℹ️ No changes needed for: {filename}")
                
                except Exception as e:
                    print(f"⚠️ Error updating {filename}: {str(e)}")
                    print(f"   └── File will keep its current settings")
        
        print("\n💡 Configuration changes will take effect on next system start")
        print("   Run 'python run.py' to apply the new settings")

if __name__ == "__main__":
    config = QuantumSystemConfig()
    config.update_config()