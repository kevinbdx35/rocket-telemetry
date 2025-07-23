import random
import time
from datetime import datetime
from typing import Optional
from .base_sensor import BaseSensor
from ..core.telemetry_data import TelemetryReading


class MockRocketSensor(BaseSensor):
    def __init__(self, name: str = "Mock Rocket Sensor", sample_rate: float = 10.0):
        super().__init__(name, sample_rate)
        self._flight_time = 0.0
        self._phase = "pre_launch"
    
    def connect(self) -> bool:
        self._is_connected = True
        return True
    
    def disconnect(self) -> None:
        self._is_connected = False
    
    def read_data(self) -> Optional[TelemetryReading]:
        if not self._is_connected:
            return None
        
        self._flight_time += 1.0 / self.sample_rate
        
        # Simuler différentes phases de vol
        altitude = self._simulate_altitude()
        velocity = self._simulate_velocity()
        
        reading = TelemetryReading(
            timestamp=datetime.now(),
            altitude=altitude,
            velocity=velocity,
            acceleration={
                'x': random.uniform(-10, 10),
                'y': random.uniform(-10, 10),
                'z': random.uniform(-20, 50) if self._phase == "powered_flight" else random.uniform(-10, 10)
            },
            temperature=random.uniform(15, 25) + altitude * -0.006,  # Température diminue avec l'altitude
            pressure=101325 * (1 - 0.0065 * altitude / 288.15) ** 5.257,  # Formule barométrique
            orientation={
                'roll': random.uniform(-5, 5),
                'pitch': random.uniform(-10, 10),
                'yaw': random.uniform(-5, 5)
            },
            gps_coordinates={
                'lat': 45.5017 + random.uniform(-0.001, 0.001),
                'lon': -73.5673 + random.uniform(-0.001, 0.001)
            },
            battery_voltage=12.0 - self._flight_time * 0.01
        )
        
        self._last_reading = reading
        return reading
    
    def _simulate_altitude(self) -> float:
        if self._flight_time < 5:  # Phase de lancement
            self._phase = "powered_flight"
            return (self._flight_time ** 2) * 20
        elif self._flight_time < 15:  # Phase de montée libre
            self._phase = "coasting"
            t_coast = self._flight_time - 5
            initial_velocity = 200
            return 500 + initial_velocity * t_coast - 4.9 * (t_coast ** 2)
        elif self._flight_time < 30:  # Descente
            self._phase = "descent"
            max_alt = 1500
            t_descent = self._flight_time - 15
            return max_alt - 15 * t_descent
        else:  # Au sol
            self._phase = "landed"
            return 0
    
    def _simulate_velocity(self) -> float:
        if self._flight_time < 5:
            return self._flight_time * 40
        elif self._flight_time < 15:
            t_coast = self._flight_time - 5
            return 200 - 9.8 * t_coast
        elif self._flight_time < 30:
            return -15
        else:
            return 0