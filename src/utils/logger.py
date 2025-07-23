import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from typing import Optional
import json


class TelemetryLogger:
    def __init__(self, log_dir: str = "logs", max_bytes: int = 10*1024*1024, backup_count: int = 5):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configuration du logger principal
        self.logger = logging.getLogger('rocket_telemetry')
        self.logger.setLevel(logging.DEBUG)
        
        # Éviter la duplication des handlers
        if not self.logger.handlers:
            self._setup_handlers(max_bytes, backup_count)
    
    def _setup_handlers(self, max_bytes: int, backup_count: int):
        # Handler pour fichier principal avec rotation
        main_file = self.log_dir / "telemetry.log"
        file_handler = logging.handlers.RotatingFileHandler(
            main_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Handler pour erreurs uniquement
        error_file = self.log_dir / "errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_file, maxBytes=max_bytes, backupCount=backup_count
        )
        error_handler.setLevel(logging.ERROR)
        
        # Handler pour console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Format des messages
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, extra_data: Optional[dict] = None):
        if extra_data:
            message = f"{message} | Data: {json.dumps(extra_data)}"
        self.logger.info(message)
    
    def warning(self, message: str, extra_data: Optional[dict] = None):
        if extra_data:
            message = f"{message} | Data: {json.dumps(extra_data)}"
        self.logger.warning(message)
    
    def error(self, message: str, extra_data: Optional[dict] = None):
        if extra_data:
            message = f"{message} | Data: {json.dumps(extra_data)}"
        self.logger.error(message)
    
    def debug(self, message: str, extra_data: Optional[dict] = None):
        if extra_data:
            message = f"{message} | Data: {json.dumps(extra_data)}"
        self.logger.debug(message)
    
    def log_telemetry_reading(self, reading_data: dict):
        self.debug("Telemetry reading received", reading_data)
    
    def log_sensor_event(self, event_type: str, sensor_name: str, details: Optional[dict] = None):
        message = f"Sensor {event_type}: {sensor_name}"
        self.info(message, details)
    
    def log_system_event(self, event_type: str, details: Optional[dict] = None):
        message = f"System event: {event_type}"
        self.info(message, details)
    
    def log_error_event(self, error_type: str, error_message: str, details: Optional[dict] = None):
        message = f"Error - {error_type}: {error_message}"
        self.error(message, details)


# Instance globale du logger
telemetry_logger = TelemetryLogger()


def get_logger():
    return telemetry_logger