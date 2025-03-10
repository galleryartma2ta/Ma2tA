import os
import sys
import ctypes
import winreg
from datetime import datetime

class WindowsMemoryFix:
    def __init__(self):
        self.timestamp = "2025-03-10 08:19:50"
        self.user = "artgalleryma2ta"
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def enable_perfcounter_service(self):
        print("\n🔧 Fixing Windows Performance Counters")
        print(f"⏰ Time: 2025-03-10 08:19:50")
        print(f"👤 User: {self.user}")
        
        if not self.is_admin():
            print("⚠️ This fix requires administrator privileges")
            print("Please run this script as administrator")
            return False
        
        try:
            # Method 1: Reset performance counters
            print("\n📊 Resetting performance counters...")
            os.system('lodctr /R')
            
            # Method 2: Enable performance counter service
            print("\n📊 Enabling performance counter service...")
            os.system('sc config "PerfHost" start= auto')
            os.system('net start PerfHost')
            
            # Method 3: Registry fix
            print("\n📊 Applying registry fixes...")
            reg_paths = [
                r"SYSTEM\CurrentControlSet\Services\PerfOS\Performance",
                r"SYSTEM\CurrentControlSet\Services\PerfProc\Performance",
                r"SYSTEM\CurrentControlSet\Services\PerfNet\Performance"
            ]
            
            for path in reg_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, 
                                       winreg.KEY_ALL_ACCESS)
                    winreg.SetValueEx(key, "Disable", 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(key)
                    print(f"✅ Fixed registry: {path}")
                except Exception as e:
                    print(f"⚠️ Could not fix registry {path}: {str(e)}")
            
            # Method 4: Reset WMI repository
            print("\n📊 Resetting WMI repository...")
            os.system('net stop winmgmt /y')
            os.system('winmgmt /resetrepository')
            os.system('net start winmgmt')
            
            print("\n✨ Performance counter fixes applied!")
            print("Please restart your computer for changes to take effect")
            return True
            
        except Exception as e:
            print(f"\n❌ Error during fix: {str(e)}")
            return False

if __name__ == "__main__":
    fix = WindowsMemoryFix()
    
    print("\n🚀 Windows Memory Monitor Fix Tool")
    print("This tool will fix performance counter issues.")
    
    if not fix.is_admin():
        print("\n⚠️ Please run this script as administrator!")
        print("Right-click on PowerShell/CMD and select 'Run as administrator'")
        print("Then navigate to this directory and run the script again")
        sys.exit(1)
    
    fix.enable_perfcounter_service()