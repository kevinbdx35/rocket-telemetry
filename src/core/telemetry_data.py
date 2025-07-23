from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class TelemetryReading:
    timestamp: datetime
    altitude: float
    velocity: float
    acceleration: Dict[str, float]  # x, y, z
    temperature: float
    pressure: float
    orientation: Dict[str, float]  # roll, pitch, yaw
    gps_coordinates: Optional[Dict[str, float]] = None  # lat, lon
    battery_voltage: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'altitude': self.altitude,
            'velocity': self.velocity,
            'acceleration': self.acceleration,
            'temperature': self.temperature,
            'pressure': self.pressure,
            'orientation': self.orientation,
            'gps_coordinates': self.gps_coordinates,
            'battery_voltage': self.battery_voltage
        }


@dataclass
class FlightPhase:
    PRE_LAUNCH = "pre_launch"
    POWERED_FLIGHT = "powered_flight"
    COASTING = "coasting"
    APOGEE = "apogee"
    DESCENT = "descent"
    RECOVERY = "recovery"
    LANDED = "landed"


class TelemetryDataValidator:
    @staticmethod
    def validate_reading(reading: TelemetryReading) -> bool:
        if reading.altitude < -1000 or reading.altitude > 100000:
            return False
        if abs(reading.velocity) > 1000:
            return False
        if reading.temperature < -100 or reading.temperature > 100:
            return False
        if reading.pressure < 0 or reading.pressure > 120000:
            return False
        return True