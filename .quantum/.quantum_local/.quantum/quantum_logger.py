import logging
import os
import sys
from datetime import datetime

class QuantumLogger:
    def __init__(self, name="quantum_system"):
        self.timestamp = "2025-03-10 08:19:50"
        self.log_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "monitoring",
            "logs"
        )
        os.makedirs(self.log_path, exist_ok=True)
        
        # تنظیم لاگر
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # فایل لاگ
        log_file = os.path.join(
            self.log_path,
            f"quantum_system_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # لاگ کنسول
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)
    
    def _safe_log(self, level, message):
        try:
            if level == 'INFO':
                self.logger.info(message)
            elif level == 'WARNING':
                self.logger.warning(message)
            elif level == 'ERROR':
                self.logger.error(message)
            elif level == 'DEBUG':
                self.logger.debug(message)
        except UnicodeEncodeError:
            clean_message = ''.join(c for c in message if ord(c) < 0x10000)
            if level == 'INFO':
                self.logger.info(clean_message)
            elif level == 'WARNING':
                self.logger.warning(clean_message)
            elif level == 'ERROR':
                self.logger.error(clean_message)
            elif level == 'DEBUG':
                self.logger.debug(clean_message)
    
    def info(self, message):
        self._safe_log('INFO', message)
    
    def warning(self, message):
        self._safe_log('WARNING', message)
    
    def error(self, message):
        self._safe_log('ERROR', message)
    
    def debug(self, message):
        self._safe_log('DEBUG', message)