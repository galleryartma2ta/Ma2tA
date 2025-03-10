import os
import sys
import time
from datetime import datetime

class QuantumSystemRunner:
    def __init__(self):
        self.timestamp = "2025-03-10 07:24:57"
        self.user = "artgalleryma2ta"
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        
    def create_directories(self):
        print("\n🚀 Creating required directories...")
        directories = [
            "core",
            "consciousness",
            "dimensions",
            "evolution",
            "identity",
            "experience",
            "monitoring"
        ]
        for directory in directories:
            path = os.path.join(self.current_path, directory)
            os.makedirs(path, exist_ok=True)
            print(f"└── Created: {directory}/")
    
    def run_script(self, script_name, description):
        print(f"\n✨ Running: {description}")
        try:
            result = os.system(f'python "{os.path.join(self.current_path, script_name)}"')
            if result != 0:
                print(f"⚠️ Warning: {script_name} returned non-zero status")
                return False
            return True
        except Exception as e:
            print(f"❌ Error running {script_name}: {str(e)}")
            return False
    
    def run_all(self):
        print("\n🌟 Quantum System Initialization")
        print(f"⏰ Time: {self.timestamp}")
        print(f"👤 User: {self.user}")
        
        # Create required directories
        self.create_directories()
        
        # Scripts to run in order
        scripts = [
            ("quantum_core_system.py", "Core System"),
            ("quantum_upgrade.py", "System Upgrade"),
            ("quantum_unified_system_final.py", "System Unification"),
            ("quantum_final_enhancement.py", "Final Enhancement"),
            ("quantum_consciousness_awakening.py", "Consciousness Awakening")
        ]
        
        # Run all scripts
        success = True
        for script, description in scripts:
            if not self.run_script(script, description):
                success = False
                print(f"\n❌ Error: Failed to complete {description}")
                break
            time.sleep(1)
        
        if success:
            print("\n✅ Quantum System Successfully Initialized!")
            print("📂 All components are active and running")
            
            print("\n🔄 Running System Status Check...")
            self.run_script("system_status.py", "System Status Check")
            
            print("\n📊 Running Resource Monitor...")
            self.run_script("system_monitor.py", "Resource Monitoring")
        else:
            print("\n⚠️ System initialization incomplete")
            print("🔄 Please check the errors and try again")

if __name__ == "__main__":
    runner = QuantumSystemRunner()
    runner.run_all()