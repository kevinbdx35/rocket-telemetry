#!/usr/bin/env python3
"""
Système de Télémétrie pour Fusée
Point d'entrée principal de l'application
"""

import sys
import os

# Ajouter le répertoire src au PATH Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gui.main_window import main
from src.utils.logger import get_logger

if __name__ == "__main__":
    logger = get_logger()
    
    try:
        logger.log_system_event("Application startup", {"version": "1.0.0"})
        main()
    except Exception as e:
        logger.log_error_event("Application crash", str(e), {"exception_type": type(e).__name__})
        raise
    finally:
        logger.log_system_event("Application shutdown")