import os
import re
import datetime
from typing import List, Dict
import json

class QuantumAutoSave:
    def __init__(self):
        self.config = self.load_config()
        self.base_path = self.config["auto_save"]["base_path"]
        self.current_time = datetime.datetime.utcnow().strftime(
            self.config["auto_save"]["timestamp_format"]
        )

    def load_config(self) -> dict:
        """Load configuration from config file."""
        config_path = os.path.join(
            "C:\\Users\\Ma2tA\\Documents\\GitHub\\Ma2tA\\.quantum",
            "automation",
            "config.json"
        )
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def extract_code_blocks(self, message: str) -> List[Dict[str, str]]:
        """Extract code blocks with their filenames from messages."""
        pattern = r"```(\w+)\s+name=([\w./\\-]+)\n(.*?)```"
        matches = re.finditer(pattern, message, re.DOTALL)
        return [
            {
                "language": match.group(1),
                "filename": match.group(2),
                "content": match.group(3)
            }
            for match in matches
        ]

    def save_file(self, file_info: Dict[str, str]) -> bool:
        """Save a single file to the appropriate directory."""
        try:
            full_path = os.path.join(self.base_path, file_info["filename"])
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, "w", encoding=self.config["auto_save"]["file_encoding"]) as f:
                f.write(file_info["content"])
            
            return True
        except Exception as e:
            print(f"Error saving {file_info['filename']}: {str(e)}")
            return False

    def process_message(self, message: str) -> None:
        """Process a message and save all code blocks."""
        code_blocks = self.extract_code_blocks(message)
        markers = self.config["auto_save"]["markers"]
        
        for block in code_blocks:
            if self.save_file(block):
                print(f"{markers['complete']} Saved: {block['filename']}")