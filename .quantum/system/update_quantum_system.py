import os
import json
from datetime import datetime
import re
from pathlib import Path
from typing import Dict, List, Union

class QuantumSystemUpdater:
    def __init__(self):
        self.current_time2025-03-10 06:20:56=2025-03-10 06:20:56"2025-03-102025-03-10 06:20:5606:20:56"
        self.old_username = "artgalleryma2ta"
        self.new_username = input("Enter new username (press Enter to keep current): ").strip()
        self.quantum_path = Path(".quantum")
        self.file_patterns = {
            ".py": r"(timestamp|current_time)\s*=\s*[\"'][\d\-\s\:]+[\"']",
            ".js": r"(timestamp|current_time)\s*=\s*[\"'][\d\-\s\:]+[\"']",
            ".ts": r"(current_moment|timestamp)\s*:\s*[\"'][\d\-\s\:]+[\"']",
            ".go": r"LastSync\s*:\s*[\"'][\d\-\s\:]+[\"']",
            ".json": r"\"(timestamp|current_time)\"\s*:\s*\"[\d\-\s\:]+\"",
            ".yml": r"(timestamp|current_time)\s*:\s*['\"]([\d\-\s\:]+)['\"]"
        }
        
    def update_file_content(self, content: str, file_ext: str) -> str:
        """Update timestamps and username in file content"""
        if not self.new_username:
            self.new_username = self.old_username

        # Update timestamps
        pattern = self.file_patterns.get(file_ext)
        if pattern:
            # Handle different date formats
            content = re.sub(
                pattern,
                lambda m: m.group(0).replace(
                    re.search(r"[\d\-\s\:]+", m.group(0)).group(0),
                    self.current_time
                ),
                content
            )

        # Update username
        content = content.replace(self.old_username, self.new_username)
        return content

    def update_yml_file(self, file_path: Path) -> None:
        """Update YAML files without using PyYAML"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple pattern matching for YAML files
            content = re.sub(
                r'(timestamp|current_time)\s*:\s*[\'"]([\d\-\s\:]+)[\'"]',
                f'\g<1>: "{self.current_time}"',
                content
            )
            content = content.replace(self.old_username, self.new_username)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Updated YAML: {file_path}")
        except Exception as e:
            print(f"❌ Error processing YAML {file_path}: {str(e)}")

    def process_file(self, file_path: Path) -> None:
        """Process a single file"""
        if not file_path.is_file():
            return

        try:
            # Special handling for YAML files
            if file_path.suffix == '.yml':
                self.update_yml_file(file_path)
                return

            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update content
            updated_content = self.update_file_content(content, file_path.suffix)

            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            print(f"✅ Updated: {file_path}")

        except Exception as e:
            print(f"❌ Error processing {file_path}: {str(e)}")

    def update_system(self):
        """Update entire quantum system"""
        print("\n💫 Quantum System Update")
        print(f"⏰ Current Time: {self.current_time}")
        print(f"👤 Username: {self.new_username or self.old_username}")
        print("─" * 50)

        # Process all files recursively
        for file_path in self.quantum_path.rglob("*"):
            if file_path.suffix in self.file_patterns:
                self.process_file(file_path)

        # Update permissions
        if os.name != 'nt':  # Skip on Windows
            self.update_permissions()

        print("\n✨ System Update Complete!")
        print(f"⏰ System time synchronized to: {self.current_time}")
        print(f"👤 Username updated to: {self.new_username or self.old_username}")

    def update_permissions(self):
        """Update file permissions"""
        try:
            # Set directory permissions
            for dir_path in self.quantum_path.rglob("*/"):
                os.chmod(dir_path, 0o750)
            
            # Set file permissions
            for file_path in self.quantum_path.rglob("*"):
                if file_path.is_file():
                    if file_path.suffix in ['.yml', '.json']:
                        os.chmod(file_path, 0o640)
                    else:
                        os.chmod(file_path, 0o750)

            print("✅ Permissions updated successfully")
        except Exception as e:
            print(f"❌ Error updating permissions: {str(e)}")

def main():
    updater = QuantumSystemUpdater()
    updater.update_system()

if __name__ == "__main__":
    main()