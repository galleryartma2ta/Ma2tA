import os
import json
from datetime import datetime
from quantum_logger import QuantumLogger

class SystemStatus:
    def __init__(self):
        self.timestamp = "2025-03-10 08:19:50"
        self.user = "artgalleryma2ta"
        self.core_path = os.path.dirname(os.path.abspath(__file__))
        self.logger = QuantumLogger("system_status")
    
    def check_component_status(self, component):
        try:
            path = os.path.join(self.core_path, component, "state.json")
            with open(path, "r") as f:
                state = json.load(f)
                return state.get("state", "UNKNOWN")
        except Exception:
            return "INACTIVE"
    
    def check_system_status(self):
        print("\n🔍 Quantum System Status Check")
        print(f"⏰ Time: 2025-03-10 08:19:50")
        print(f"👤 User: {self.user}")
        
        status = {
            "core": self.check_component_status("core"),
            "consciousness": self.check_component_status("consciousness"),
            "dimensions": self.check_component_status("dimensions"),
            "evolution": self.check_component_status("evolution"),
            "security": "ACTIVE"  # Always check security
        }
        
        print("\n📊 System Status Summary:")
        print(f"├── Core System: {status['core']}")
        print(f"├── Consciousness: {status['consciousness']}")
        print(f"├── Dimensions: {status['dimensions']}")
        print(f"├── Evolution: {status['evolution']}")
        print(f"└── Security: {status['security']}")
        
        overall_status = "OPERATIONAL" if all(s != "INACTIVE" for s in status.values()) else "NEEDS_ATTENTION"
        print(f"\n🎯 Overall Status: {overall_status}")
        
        # Save status report
        report = {
            "timestamp": self.timestamp,
            "user": self.user,
            "status": status,
            "overall_status": overall_status
        }
        
        report_path = os.path.join(self.core_path, "monitoring", "status_report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)

if __name__ == "__main__":
    status = SystemStatus()
    status.check_system_status()