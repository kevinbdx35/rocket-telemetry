import unittest
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.core.telemetry_data import TelemetryReading, TelemetryDataValidator


class TestTelemetryReading(unittest.TestCase):
    def setUp(self):
        self.sample_reading = TelemetryReading(
            timestamp=datetime.now(),
            altitude=1000.0,
            velocity=50.0,
            acceleration={'x': 1.0, 'y': 2.0, 'z': 9.8},
            temperature=20.0,
            pressure=101325.0,
            orientation={'roll': 0.0, 'pitch': 5.0, 'yaw': -2.0},
            gps_coordinates={'lat': 45.5017, 'lon': -73.5673},
            battery_voltage=12.0
        )
    
    def test_to_dict(self):
        data_dict = self.sample_reading.to_dict()
        
        self.assertIn('timestamp', data_dict)
        self.assertEqual(data_dict['altitude'], 1000.0)
        self.assertEqual(data_dict['velocity'], 50.0)
        self.assertEqual(data_dict['acceleration']['x'], 1.0)
        self.assertEqual(data_dict['temperature'], 20.0)
        self.assertEqual(data_dict['pressure'], 101325.0)
        self.assertEqual(data_dict['orientation']['roll'], 0.0)
        self.assertEqual(data_dict['gps_coordinates']['lat'], 45.5017)
        self.assertEqual(data_dict['battery_voltage'], 12.0)
    
    def test_required_fields(self):
        # Test que tous les champs requis sont présents
        self.assertIsNotNone(self.sample_reading.timestamp)
        self.assertIsInstance(self.sample_reading.altitude, float)
        self.assertIsInstance(self.sample_reading.velocity, float)
        self.assertIsInstance(self.sample_reading.acceleration, dict)
        self.assertIsInstance(self.sample_reading.temperature, float)
        self.assertIsInstance(self.sample_reading.pressure, float)
        self.assertIsInstance(self.sample_reading.orientation, dict)


class TestTelemetryDataValidator(unittest.TestCase):
    def setUp(self):
        self.validator = TelemetryDataValidator()
        self.valid_reading = TelemetryReading(
            timestamp=datetime.now(),
            altitude=1000.0,
            velocity=50.0,
            acceleration={'x': 1.0, 'y': 2.0, 'z': 9.8},
            temperature=20.0,
            pressure=101325.0,
            orientation={'roll': 0.0, 'pitch': 5.0, 'yaw': -2.0}
        )
    
    def test_valid_reading(self):
        self.assertTrue(self.validator.validate_reading(self.valid_reading))
    
    def test_invalid_altitude_too_low(self):
        self.valid_reading.altitude = -2000.0
        self.assertFalse(self.validator.validate_reading(self.valid_reading))
    
    def test_invalid_altitude_too_high(self):
        self.valid_reading.altitude = 200000.0
        self.assertFalse(self.validator.validate_reading(self.valid_reading))
    
    def test_invalid_velocity_too_high(self):
        self.valid_reading.velocity = 2000.0
        self.assertFalse(self.validator.validate_reading(self.valid_reading))
    
    def test_invalid_temperature_too_low(self):
        self.valid_reading.temperature = -150.0
        self.assertFalse(self.validator.validate_reading(self.valid_reading))
    
    def test_invalid_temperature_too_high(self):
        self.valid_reading.temperature = 150.0
        self.assertFalse(self.validator.validate_reading(self.valid_reading))
    
    def test_invalid_pressure_negative(self):
        self.valid_reading.pressure = -100.0
        self.assertFalse(self.validator.validate_reading(self.valid_reading))
    
    def test_invalid_pressure_too_high(self):
        self.valid_reading.pressure = 200000.0
        self.assertFalse(self.validator.validate_reading(self.valid_reading))


if __name__ == '__main__':
    unittest.main()