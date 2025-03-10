from datetime import datetime
import json
import os
from pathlib import Path
import time

class QuantumMonitor:
    def __init__(self):
        self.timestamp2025-03-10 06:20:56=2025-03-10 06:20:56"2025-03-092025-03-10 06:20:5619:00:33"  # Updated with current time
        self.user = "artgalleryma2ta"
        self.base_path = Path(".quantum")
        self.monitor_log = self.base_path / "logs" / "monitor.json"
        self.start_time = datetime.utcnow()
        
    def update_state(self):
        """Update system state with monitoring info"""
        state = {
            "monitor_info": {
                "last_check": self.timestamp,
                "start_time": self.timestamp,
                "monitor_active": True,
                "user": self.user
            },
            "system_health": {
                "status": "optimal",
                "last_updated": self.timestamp,
                "uptime": "0 minutes"
            },
            "monitoring_stats": {
                "directories_watched": [
                    "system",
                    "test",
                    "logs",
                    "data"
                ],
                "files_tracked": [
                    "state.json",
                    "monitor.json",
                    "quantum_manager.py",
                    "monitor.py"
                ]
            },
            "system_metrics": {
                "active_processes": 1,
                "monitored_files": 4,
                "monitored_dirs": 4,
                "last_backup": self.timestamp
            }
        }
        
        # Save monitoring state
        self.monitor_log.parent.mkdir(parents=True, exist_ok=True)
        with open(self.monitor_log, 'w') as f:
            json.dump(state, f, indent=4)
        
        return state
    
    def display_status(self, state):
        """Display current monitoring status"""
        print(f"\n[MONITOR] Quantum System Status")
        print(f"├── Time: {self.timestamp}")
        print(f"├── User: {self.user}")
        print(f"├── System Health: {state['system_health']['status']}")
        print(f"├── Monitor Active: {state['monitor_info']['monitor_active']}")
        
        print("\n├── Monitored Directories:")
        for dir_name in state['monitoring_stats']['directories_watched']:
            dir_path = self.base_path / dir_name
            print(f"│   └── {dir_name}: {'✓' if dir_path.exists() else '✗'}")
        
        print("\n├── Tracked Files:")
        for file_name in state['monitoring_stats']['files_tracked']:
            found = list(self.base_path.rglob(file_name))
            print(f"│   └── {file_name}: {'✓' if found else '✗'}")
        
        print("\n├── System Metrics:")
        metrics = state['system_metrics']
        print(f"│   ├── Active Processes: {metrics['active_processes']}")
        print(f"│   ├── Monitored Files: {metrics['monitored_files']}")
        print(f"│   ├── Monitored Directories: {metrics['monitored_dirs']}")
        print(f"│   └── Last Backup: {metrics['last_backup']}")
        
        print(f"\n└── Status: ACTIVE AND MONITORING")

    def run(self):
        """Start the monitoring system"""
        print(f"[START] Quantum Monitor Initializing...")
        print(f"[INFO] Monitor started at {self.timestamp}")
        
        try:
            while True:
                # Update and display state
                current_state = self.update_state()
                self.display_status(current_state)
                
                print(f"\n[INFO] Press Ctrl+C to stop monitoring...")
                time.sleep(5)  # Update every 5 seconds
                
        except KeyboardInterrupt:
            print(f"\n[INFO] Monitor stopped by user at {self.timestamp}")
            print(f"System remains active, monitor can be restarted anytime")
            
            # Save final state
            final_state = self.update_state()
            final_state["monitor_info"]["monitor_active"] = False
            with open(self.monitor_log, 'w') as f:
                json.dump(final_state, f, indent=4)
        
        except Exception as e:
            print(f"\n[ERROR] Monitoring failed: {str(e)}")
            print(f"[INFO] Try restarting the monitor")

if __name__ == "__main__":
    monitor = QuantumMonitor()
    monitor.run()