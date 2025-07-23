#!/usr/bin/env python3
"""
Script pour exécuter tous les tests du système de télémétrie
"""

import unittest
import sys
import os

# Ajouter le répertoire src au PATH Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_tests():
    # Découvrir et exécuter tous les tests
    loader = unittest.TestLoader()
    
    # Charger les tests unitaires
    unit_tests = loader.discover('tests/unit', pattern='test_*.py')
    
    # Charger les tests d'intégration
    integration_tests = loader.discover('tests/integration', pattern='test_*.py')
    
    # Créer une suite de tests complète
    test_suite = unittest.TestSuite([unit_tests, integration_tests])
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Retourner le code de sortie approprié
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)