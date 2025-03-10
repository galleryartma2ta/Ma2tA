from datetime import datetime
import json
import os
from pathlib import Path
import shutil

class QuantumBackup:
    def __init__(self):
        self.timestamp2025-03-10 06:20:56=2025-03-10 06:20:56"2025-03-092025-03-10 06:20:5619:02:40"  # Current time
        self.user = "artgalleryma2ta"
        self.base_path = Path(".quantum")
        self.backup_path = self.base_path / "backups"
        self.backup_log = self.base_path / "logs" / "backup_history.json"
        
    def create_backup(self):
        """Create a backup of important system files"""
        # Create backup directory
        backup_dir = self.backup_path / f"backup_{self.timestamp.replace(' ', '_').replace(':', '-')}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Files to backup
        critical_files = {
            "system/state.json": "System State",
            "system/monitor.py": "Monitor Script",
            "system/quantum_manager.py": "Manager Script",
            "logs/monitor.json": "Monitor Logs"
        }
        
        backup_info = {
            "timestamp": self.timestamp,
            "user": self.user,
            "backup_location": str(backup_dir),
            "files_backed_up": [],
            "backup_status": "success"
        }
        
        try:
            # Copy each file to backup location
            for file_path, description in critical_files.items():
                source = self.base_path / file_path
                if source.exists():
                    dest = backup_dir / source.name
                    shutil.copy2(source, dest)
                    backup_info["files_backed_up"].append({
                        "file": str(source),
                        "description": description,
                        "status": "success"
                    })
                else:
                    backup_info["files_backed_up"].append({
                        "file": str(source),
                        "description": description,
                        "status": "file_not_found"
                    })
            
            # Save backup log
            self.backup_log.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing history or create new
            if self.backup_log.exists():
                with open(self.backup_log, 'r') as f:
                    history = json.load(f)
            else:
                history = {"backups": []}
            
            # Add new backup to history
            history["backups"].append(backup_info)
            
            # Save updated history
            with open(self.backup_log, 'w') as f:
                json.dump(history, f, indent=4)
            
            return backup_info
            
        except Exception as e:
            backup_info["backup_status"] = f"failed: {str(e)}"
            return backup_info

    def display_backup_status(self, backup_info):
        """Display backup operation status"""
        print(f"\n[BACKUP] Quantum System Backup")
        print(f"├── Time: {backup_info['timestamp']}")
        print(f"├── User: {backup_info['user']}")
        print(f"├── Location: {backup_info['backup_location']}")
        print("\n├── Backed Up Files:")
        
        for file_info in backup_info['files_backed_up']:
            status_symbol = '✓' if file_info['status'] == 'success' else '✗'
            print(f"│   ├── {file_info['file']}")
            print(f"│   │   ├── Description: {file_info['description']}")
            print(f"│   │   └── Status: {status_symbol} {file_info['status']}")
        
        print(f"\n└── Backup Status: {backup_info['backup_status']}")

    def run(self):
        """Execute backup operation"""
        print(f"[START] Quantum Backup Initializing...")
        print(f"[INFO] Starting backup at {self.timestamp}")
        
        try:
            # Create backup
            backup_info = self.create_backup()
            self.display_backup_status(backup_info)
            
            if backup_info['backup_status'] == 'success':
                print(f"\n[SUCCESS] Backup completed successfully!")
            else:
                print(f"\n[ERROR] Backup completed with errors")
                
        except Exception as e:
            print(f"\n[ERROR] Backup failed: {str(e)}")

if __name__ == "__main__":
    backup = QuantumBackup()
    backup.run()