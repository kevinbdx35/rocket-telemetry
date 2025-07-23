from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..core.telemetry_data import TelemetryReading


class BaseSensor(ABC):
    def __init__(self, name: str, sample_rate: float = 10.0):
        self.name = name
        self.sample_rate = sample_rate
        self._is_connected = False
        self._last_reading: Optional[TelemetryReading] = None
    
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        pass
    
    @abstractmethod
    def read_data(self) -> Optional[TelemetryReading]:
        pass
    
    @property
    def is_connected(self) -> bool:
        return self._is_connected
    
    @property
    def last_reading(self) -> Optional[TelemetryReading]:
        return self._last_reading
    
    def get_status(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'connected': self._is_connected,
            'sample_rate': self.sample_rate,
            'last_reading_time': self._last_reading.timestamp.isoformat() if self._last_reading else None
        }