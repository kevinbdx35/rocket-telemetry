import unittest
import time
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.core.telemetry_data import TelemetryReading
from src.data.data_processor import TelemetryProcessor


class TestTelemetryProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = TelemetryProcessor(buffer_size=100)
        self.sample_reading = TelemetryReading(
            timestamp=datetime.now(),
            altitude=1000.0,
            velocity=50.0,
            acceleration={'x': 1.0, 'y': 2.0, 'z': 9.8},
            temperature=20.0,
            pressure=101325.0,
            orientation={'roll': 0.0, 'pitch': 5.0, 'yaw': -2.0}
        )
    
    def tearDown(self):
        self.processor.stop_processing()
    
    def test_add_valid_reading(self):
        result = self.processor.add_reading(self.sample_reading)
        self.assertTrue(result)
    
    def test_add_invalid_reading(self):
        # Créer une lecture invalide
        invalid_reading = TelemetryReading(
            timestamp=datetime.now(),
            altitude=200000.0,  # Trop élevé
            velocity=50.0,
            acceleration={'x': 1.0, 'y': 2.0, 'z': 9.8},
            temperature=20.0,
            pressure=101325.0,
            orientation={'roll': 0.0, 'pitch': 5.0, 'yaw': -2.0}
        )
        result = self.processor.add_reading(invalid_reading)
        self.assertFalse(result)
    
    def test_start_stop_processing(self):
        self.processor.start_processing()
        self.assertTrue(self.processor._is_processing)
        
        self.processor.stop_processing()
        self.assertFalse(self.processor._is_processing)
    
    def test_data_processing(self):
        # Ajouter des données et démarrer le traitement
        self.processor.add_reading(self.sample_reading)
        self.processor.start_processing()
        
        # Attendre un peu pour que le traitement se fasse
        time.sleep(0.2)
        
        # Vérifier que les données ont été traitées
        processed_data = self.processor.get_all_data()
        self.assertEqual(len(processed_data), 1)
        self.assertEqual(processed_data[0].altitude, 1000.0)
    
    def test_get_recent_data(self):
        # Ajouter des données
        self.processor.add_reading(self.sample_reading)
        self.processor.start_processing()
        
        time.sleep(0.1)
        
        # Récupérer les données récentes
        recent_data = self.processor.get_recent_data(duration_seconds=60)
        self.assertEqual(len(recent_data), 1)
    
    def test_get_latest_reading(self):
        self.processor.add_reading(self.sample_reading)
        self.processor.start_processing()
        
        time.sleep(0.1)
        
        latest = self.processor.get_latest_reading()
        self.assertIsNotNone(latest)
        self.assertEqual(latest.altitude, 1000.0)
    
    def test_clear_data(self):
        self.processor.add_reading(self.sample_reading)
        self.processor.start_processing()
        
        time.sleep(0.1)
        
        self.processor.clear_data()
        all_data = self.processor.get_all_data()
        self.assertEqual(len(all_data), 0)
    
    def test_callback_mechanism(self):
        # Test du système de callback
        callback_called = False
        received_reading = None
        
        def test_callback(reading):
            nonlocal callback_called, received_reading
            callback_called = True
            received_reading = reading
        
        self.processor.add_data_callback(test_callback)
        self.processor.add_reading(self.sample_reading)
        self.processor.start_processing()
        
        time.sleep(0.2)
        
        self.assertTrue(callback_called)
        self.assertIsNotNone(received_reading)
        self.assertEqual(received_reading.altitude, 1000.0)


if __name__ == '__main__':
    unittest.main()