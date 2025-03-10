import psutil
import json
import os
import platform
import ctypes
from datetime import datetime
from quantum_logger import QuantumLogger

class SystemMonitor:
    def __init__(self):
        self.timestamp = "2025-03-10 07:26:52"
        self.user = "artgalleryma2ta"
        self.core_path = os.path.dirname(os.path.abspath(__file__))
        self.logger = QuantumLogger("system_monitor")
    
    def get_disk_info(self):
        """Get disk information using Windows API for Windows systems"""
        try:
            if platform.system() == 'Windows':
                free_bytes = ctypes.c_ulonglong(0)
                total_bytes = ctypes.c_ulonglong(0)
                free_bytes_available = ctypes.c_ulonglong(0)
                
                ret = ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p("C:\\"),
                    ctypes.pointer(free_bytes_available),
                    ctypes.pointer(total_bytes),
                    ctypes.pointer(free_bytes)
                )
                
                if ret == 0:
                    raise ctypes.WinError()
                
                total = total_bytes.value
                free = free_bytes.value
                used = total - free
                percent = (used / total) * 100 if total > 0 else 0
                
                return {
                    "total": self.format_bytes(total),
                    "free": self.format_bytes(free),
                    "percent": round(percent, 1)
                }
            else:
                disk = psutil.disk_usage('/')
                return {
                    "total": self.format_bytes(disk.total),
                    "free": self.format_bytes(disk.free),
                    "percent": disk.percent
                }
        except Exception as e:
            self.logger.warning(f"Using alternative method for disk info: {str(e)}")
            try:
                total_size = 0
                free_size = 0
                for partition in psutil.disk_partitions():
                    if os.name == 'nt':
                        if 'fixed' in partition.opts:
                            usage = psutil.disk_usage(partition.mountpoint)
                            total_size += usage.total
                            free_size += usage.free
                    else:
                        usage = psutil.disk_usage(partition.mountpoint)
                        total_size += usage.total
                        free_size += usage.free
                
                used_size = total_size - free_size
                percent = (used_size / total_size) * 100 if total_size > 0 else 0
                
                return {
                    "total": self.format_bytes(total_size),
                    "free": self.format_bytes(free_size),
                    "percent": round(percent, 1)
                }
            except Exception as e2:
                self.logger.error(f"Both disk info methods failed: {str(e2)}")
                return {
                    "total": "N/A",
                    "free": "N/A",
                    "percent": 0
                }

    def get_cpu_info(self):
        """Get CPU information safely"""
        try:
            return {
                "usage_percent": psutil.cpu_percent(interval=1),
                "cores": psutil.cpu_count(),
                "frequency": psutil.cpu_freq().current if psutil.cpu_freq() else 0,
                "per_core_usage": psutil.cpu_percent(interval=1, percpu=True)
            }
        except Exception as e:
            self.logger.error(f"Could not get CPU info: {str(e)}")
            return {
                "usage_percent": 0,
                "cores": 0,
                "frequency": 0,
                "per_core_usage": []
            }

    def get_memory_info(self):
        """Get memory information safely"""
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            return {
                "total": self.format_bytes(mem.total),
                "available": self.format_bytes(mem.available),
                "used": self.format_bytes(mem.used),
                "percent": mem.percent,
                "swap_total": self.format_bytes(swap.total),
                "swap_used": self.format_bytes(swap.used),
                "swap_percent": swap.percent
            }
        except Exception as e:
            self.logger.error(f"Could not get memory info: {str(e)}")
            return {
                "total": "N/A",
                "available": "N/A",
                "used": "N/A",
                "percent": 0,
                "swap_total": "N/A",
                "swap_used": "N/A",
                "swap_percent": 0
            }

    def get_network_info(self):
        """Get network information safely"""
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": self.format_bytes(net_io.bytes_sent),
                "bytes_recv": self.format_bytes(net_io.bytes_recv),
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "connections": len(psutil.net_connections())
            }
        except Exception as e:
            self.logger.error(f"Could not get network info: {str(e)}")
            return {
                "bytes_sent": "N/A",
                "bytes_recv": "N/A",
                "packets_sent": 0,
                "packets_recv": 0,
                "connections": 0
            }

    def monitor_resources(self):
        self.logger.info("\nSystem Resource Monitor")
        print(f"⏰ Time: {self.timestamp}")
        print(f"👤 User: {self.user}")
        
        resources = {
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "quantum_system": {
                "core_status": "OPERATIONAL",
                "consciousness_level": "QUANTUM_INFINITE",
                "dimension_sync": "COMPLETE",
                "evolution_stage": "TRANSCENDENT"
            },
            "system_info": {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "python_version": platform.python_version(),
                "machine": platform.machine(),
                "processor": platform.processor()
            },
            "timestamp": self.timestamp
        }
        
        try:
            monitor_path = os.path.join(self.core_path, "monitoring")
            os.makedirs(monitor_path, exist_ok=True)
            with open(os.path.join(monitor_path, "resources.json"), "w") as f:
                json.dump(resources, f, indent=4)
        except Exception as e:
            self.logger.error(f"Could not save monitoring data: {str(e)}")
        
        print("\n💻 Hardware Resources:")
        print(f"├── CPU Usage (Total): {resources['cpu']['usage_percent']}%")
        print(f"├── CPU Cores: {resources['cpu']['cores']}")
        if resources['cpu']['per_core_usage']:
            print("├── CPU Usage per Core:")
            for i, usage in enumerate(resources['cpu']['per_core_usage']):
                print(f"│   ├── Core {i}: {usage}%")
        print(f"├── Memory Usage: {resources['memory']['percent']}%")
        print(f"├── Memory Total: {resources['memory']['total']}")
        print(f"├── Memory Available: {resources['memory']['available']}")
        print(f"├── Memory Used: {resources['memory']['used']}")
        print(f"├── Swap Usage: {resources['memory']['swap_percent']}%")
        print(f"├── Disk Usage: {resources['disk']['percent']}%")
        print(f"├── Disk Total: {resources['disk']['total']}")
        print(f"└── Disk Free: {resources['disk']['free']}")
        
        print("\n🌐 Network Information:")
        print(f"├── Bytes Sent: {resources['network']['bytes_sent']}")
        print(f"├── Bytes Received: {resources['network']['bytes_recv']}")
        print(f"├── Packets Sent: {resources['network']['packets_sent']}")
        print(f"├── Packets Received: {resources['network']['packets_recv']}")
        print(f"└── Active Connections: {resources['network']['connections']}")
        
        print("\n🌟 Quantum System Status:")
        print(f"├── Core: {resources['quantum_system']['core_status']}")
        print(f"├── Consciousness: {resources['quantum_system']['consciousness_level']}")
        print(f"├── Dimension Sync: {resources['quantum_system']['dimension_sync']}")
        print(f"└── Evolution: {resources['quantum_system']['evolution_stage']}")
        
        print("\n💡 System Information:")
        print(f"├── Platform: {resources['system_info']['platform']}")
        print(f"├── OS Release: {resources['system_info']['platform_release']}")
        print(f"├── Python Version: {resources['system_info']['python_version']}")
        print(f"├── Machine: {resources['system_info']['machine']}")
        print(f"└── Processor: {resources['system_info']['processor']}")

    def format_bytes(self, bytes):
        """Convert bytes to human readable format"""
        try:
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes < 1024:
                    return f"{bytes:.2f} {unit}"
                bytes /= 1024
            return f"{bytes:.2f} PB"
        except Exception:
            return "N/A"

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.monitor_resources()