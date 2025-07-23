import unittest
import time
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.sensors.mock_sensor import MockRocketSensor
from src.data.data_processor import TelemetryProcessor
from src.data.data_storage import DataStorage


class TestSensorIntegration(unittest.TestCase):
    def setUp(self):
        self.sensor = MockRocketSensor()
        self.processor = TelemetryProcessor()
        self.storage = DataStorage("test_logs")
    
    def tearDown(self):
        self.processor.stop_processing()
        self.sensor.disconnect()
        
        # Nettoyer les fichiers de test
        import shutil
        if os.path.exists("test_logs"):
            shutil.rmtree("test_logs")
    
    def test_full_data_pipeline(self):
        # Test de l'intégration complète: Capteur -> Processeur -> Stockage
        
        # 1. Connecter le capteur
        self.assertTrue(self.sensor.connect())
        self.assertTrue(self.sensor.is_connected)
        
        # 2. Démarrer le traitement
        self.processor.start_processing()
        
        # 3. Lire plusieurs échantillons
        readings = []
        for _ in range(5):
            reading = self.sensor.read_data()
            self.assertIsNotNone(reading)
            success = self.processor.add_reading(reading)
            self.assertTrue(success)
            readings.append(reading)
            time.sleep(0.1)  # Petite pause entre les lectures
        
        # 4. Attendre que le traitement soit fait
        time.sleep(0.3)
        
        # 5. Vérifier que toutes les données ont été traitées
        processed_data = self.processor.get_all_data()
        self.assertEqual(len(processed_data), 5)
        
        # 6. Sauvegarder les données
        json_file = self.storage.save_to_json(processed_data, "test_data.json")
        csv_file = self.storage.save_to_csv(processed_data, "test_data.csv")
        
        # 7. Vérifier que les fichiers ont été créés
        self.assertTrue(os.path.exists(json_file))
        self.assertTrue(os.path.exists(csv_file))
        
        # 8. Recharger les données depuis JSON et vérifier
        loaded_data = self.storage.load_from_json("test_data.json")
        self.assertEqual(len(loaded_data), 5)
        
        # Vérifier que les données chargées correspondent aux originales
        for original, loaded in zip(processed_data, loaded_data):
            self.assertEqual(original.altitude, loaded.altitude)
            self.assertEqual(original.velocity, loaded.velocity)
            self.assertEqual(original.temperature, loaded.temperature)
    
    def test_sensor_data_validation(self):
        # Test que le capteur génère des données valides
        self.sensor.connect()
        
        for _ in range(10):
            reading = self.sensor.read_data()
            self.assertIsNotNone(reading)
            
            # Vérifier les types de données
            self.assertIsInstance(reading.altitude, float)
            self.assertIsInstance(reading.velocity, float)
            self.assertIsInstance(reading.temperature, float)
            self.assertIsInstance(reading.pressure, float)
            self.assertIsInstance(reading.acceleration, dict)
            self.assertIsInstance(reading.orientation, dict)
            
            # Vérifier que les dictionnaires ont les bonnes clés
            self.assertIn('x', reading.acceleration)
            self.assertIn('y', reading.acceleration)
            self.assertIn('z', reading.acceleration)
            self.assertIn('roll', reading.orientation)
            self.assertIn('pitch', reading.orientation)
            self.assertIn('yaw', reading.orientation)
            
            # Vérifier que le timestamp est récent
            time_diff = (datetime.now() - reading.timestamp).total_seconds()
            self.assertLess(time_diff, 1.0)  # Moins d'1 seconde de différence
    
    def test_real_time_processing(self):
        # Test du traitement en temps réel
        data_received = []
        
        def callback(reading):
            data_received.append(reading)
        
        # Configuration
        self.processor.add_data_callback(callback)
        self.processor.start_processing()
        self.sensor.connect()
        
        # Générer des données en continu
        for i in range(3):
            reading = self.sensor.read_data()
            self.processor.add_reading(reading)
            time.sleep(0.1)
        
        # Attendre que tous les callbacks soient exécutés
        time.sleep(0.3)
        
        # Vérifier que tous les callbacks ont été appelés
        self.assertEqual(len(data_received), 3)
        
        # Vérifier que les données sont dans l'ordre chronologique
        for i in range(1, len(data_received)):
            self.assertGreaterEqual(data_received[i].timestamp, 
                                  data_received[i-1].timestamp)


if __name__ == '__main__':
    unittest.main()