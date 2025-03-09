from datetime import datetime
import json
import os
from pathlib import Path

class QuantumManager:
    def __init__(self):
        self.timestamp = "2025-03-09 18:54:08"
        self.user = "artgalleryma2ta"
        self.base_path = Path(".quantum")
        
    def init_directories(self):
        """Initialize required directories"""
        directories = [
            "system",
            "test",
            "logs",
            "data"
        ]
        
        for dir_name in directories:
            (self.base_path / dir_name).mkdir(parents=True, exist_ok=True)
            
        print(f"[INIT] Directories created successfully")
    
    def save_system_state(self):
        """Save current system state"""
        state = {
            "timestamp": self.timestamp,
            "user": self.user,
            "status": "ACTIVE",
            "last_operation": "system_initialization"
        }
        
        state_file = self.base_path / "system" / "state.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=4)
            
        print(f"[STATE] System state saved")
    
    def check_system(self):
        """Check system status"""
        try:
            print(f"\n[CHECK] Running system check at {self.timestamp}")
            print(f"├── User: {self.user}")
            
            # Check directories
            print("├── Directory Status:")
            for dir_name in ["system", "test", "logs", "data"]:
                exists = (self.base_path / dir_name).exists()
                print(f"│   └── {dir_name}: {'✓' if exists else '✗'}")
            
            # Check state file
            state_file = self.base_path / "system" / "state.json"
            state_exists = state_file.exists()
            print(f"├── State File: {'✓' if state_exists else '✗'}")
            
            if state_exists:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                print(f"└── System Status: {state['status']}")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] System check failed: {str(e)}")
            return False

    def run(self):
        """Run the Quantum Manager"""
        print(f"[START] Quantum Manager Starting...")
        self.init_directories()
        self.save_system_state()
        system_ok = self.check_system()
        
        if system_ok:
            print(f"\n[SUCCESS] Quantum Manager is ready!")
            print(f"System is now active and monitoring.")
        else:
            print(f"\n[FAILURE] System initialization failed!")

if __name__ == "__main__":
    manager = QuantumManager()
    manager.run()