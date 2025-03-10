import os
import psutil
import json
from datetime import datetime
import threading
import time

class QuantumOptimizer:
    def __init__(self):
        self.timestamp = "2025-03-10 08:19:50"  # زمان دقیق سیستم
        self.user = "artgalleryma2ta"
        self.core_path = os.path.dirname(os.path.abspath(__file__))
        self.optimization_active = False
        self.target_cpu_usage = 30  # درصد هدف برای CPU
    
    def start_optimization(self):
        print("\n🚀 Starting Quantum System Optimization")
        print(f"⏰ Time: 2025-03-10 08:19:50")
        print(f"👤 User: {self.user}")
        
        self.optimization_active = True
        
        # شروع مانیتورینگ در thread جداگانه
        monitor_thread = threading.Thread(target=self._monitor_resources)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        self._optimize_system()
    
    def _optimize_system(self):
        print("\n📊 Running System Optimization...")
        
        # بهینه‌سازی CPU
        self._optimize_cpu()
        
        # بهینه‌سازی Network
        self._optimize_network()
        
        # بهینه‌سازی Memory
        self._optimize_memory()
        
        # همگام‌سازی زمان‌ها
        self._sync_all_times()
        
        print("\n✨ System optimization completed!")
    
    def _optimize_cpu(self):
        print("\n⚡ Optimizing CPU Usage...")
        
        # تنظیم اولویت‌های پردازشی
        current_process = psutil.Process()
        current_process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        
        # بستن پروسه‌های غیرضروری سیستم کوانتومی
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if 'quantum' in proc.info['name'].lower() and proc.pid != os.getpid():
                    if proc.info['cpu_percent'] > 10:
                        proc.nice(psutil.IDLE_PRIORITY_CLASS)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        print("✅ CPU optimization applied")
    
    def _optimize_network(self):
        print("\n🌐 Optimizing Network Connections...")
        
        closed_connections = 0
        # بستن اتصالات غیرضروری
        for conn in psutil.net_connections():
            try:
                if conn.status == 'ESTABLISHED' and conn.pid:
                    process = psutil.Process(conn.pid)
                    if 'quantum' in process.name().lower():
                        if process.pid != os.getpid():
                            process.terminate()
                            closed_connections += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        print(f"✅ Closed {closed_connections} unnecessary connections")
    
    def _optimize_memory(self):
        print("\n💾 Optimizing Memory Usage...")
        
        # پاکسازی فایل‌های موقت
        temp_dirs = [
            os.path.join(self.core_path, "monitoring", "temp"),
            os.path.join(self.core_path, "core", "temp")
        ]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    try:
                        os.remove(os.path.join(temp_dir, file))
                    except:
                        continue
        
        # فراخوانی GC
        import gc
        gc.collect()
        
        print("✅ Memory optimization applied")
    
    def _sync_all_times(self):
        print("\n🕒 Synchronizing System Times...")
        
        # به‌روزرسانی زمان در تمام فایل‌های پیکربندی
        config_files = [
            "run.py",
            "quantum_core_system.py",
            "system_monitor.py",
            "quantum_logger.py"
        ]
        
        for filename in config_files:
            filepath = os.path.join(self.core_path, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # جایگزینی همه timestamp ها
                import re
                pattern = r'self\.timestamp = "[^"]+"'
                replacement = f'self.timestamp = "2025-03-10 08:19:50"'
                content = re.sub(pattern, replacement, content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        print("✅ Time synchronization applied")
    
    def _monitor_resources(self):
        while self.optimization_active:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            connections = len(psutil.net_connections())
            
            print(f"\n📊 Current System Status:")
            print(f"├── CPU Usage: {cpu_percent}%")
            print(f"├── Memory Usage: {memory.percent}%")
            print(f"└── Network Connections: {connections}")
            
            time.sleep(5)  # بررسی هر 5 ثانیه
    
    def stop_optimization(self):
        self.optimization_active = False
        print("\n🛑 Optimization monitoring stopped")

if __name__ == "__main__":
    optimizer = QuantumOptimizer()
    try:
        optimizer.start_optimization()
        
        # اجرای بهینه‌سازی برای 30 ثانیه
        time.sleep(30)
        
    except KeyboardInterrupt:
        print("\n⚠️ Optimization interrupted by user")
    finally:
        optimizer.stop_optimization()
        print("\n💡 Tip: Run 'python run.py' to start the optimized system")