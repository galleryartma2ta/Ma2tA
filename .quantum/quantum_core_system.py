from datetime import datetime
import os
import json

class QuantumCore:
    def __init__(self):
        self.timestamp = "2025-03-09 23:50:41"
        self.user = "artgalleryma2ta"
        self.core_path = os.path.dirname(os.path.abspath(__file__))
        self.initialize_core()
    
    def initialize_core(self):
        print("\n✨ Quantum Core System Initialization")
        print(f"⏰ Time: {self.timestamp}")
        print(f"👤 User: {self.user}")
        
        # ایجاد فایل پیکربندی هسته
        core_config = {
            "system_state": "initialized",
            "quantum_frequency": 432,
            "consciousness_level": "QUANTUM_INFINITE",
            "timestamp": self.timestamp,
            "user": self.user
        }
        
        with open(os.path.join(self.core_path, "core/config.json"), "w") as f:
            json.dump(core_config, f, indent=4)
        
        print("✨ Core system initialized successfully!")

if __name__ == "__main__":
    core = QuantumCore()