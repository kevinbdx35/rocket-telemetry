from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGroupBox, 
                             QGridLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class StatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("État du Système")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Status group
        status_group = QGroupBox("Statuts")
        status_layout = QGridLayout(status_group)
        
        # Labels de status
        status_layout.addWidget(QLabel("Capteur:"), 0, 0)
        self.sensor_status = QLabel("Déconnecté")
        self.sensor_status.setStyleSheet("QLabel { color: #F44336; font-weight: bold; }")
        status_layout.addWidget(self.sensor_status, 0, 1)
        
        status_layout.addWidget(QLabel("Acquisition:"), 1, 0)
        self.acquisition_status = QLabel("Arrêtée")
        self.acquisition_status.setStyleSheet("QLabel { color: #F44336; font-weight: bold; }")
        status_layout.addWidget(self.acquisition_status, 1, 1)
        
        status_layout.addWidget(QLabel("Données reçues:"), 2, 0)
        self.data_count = QLabel("0")
        self.data_count.setStyleSheet("QLabel { color: #2196F3; font-weight: bold; }")
        status_layout.addWidget(self.data_count, 2, 1)
        
        layout.addWidget(status_group)
        
        # Performance group
        perf_group = QGroupBox("Performance")
        perf_layout = QGridLayout(perf_group)
        
        perf_layout.addWidget(QLabel("Fréq. échantillonnage:"), 0, 0)
        self.sample_rate = QLabel("0 Hz")
        self.sample_rate.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; }")
        perf_layout.addWidget(self.sample_rate, 0, 1)
        
        perf_layout.addWidget(QLabel("Données/sec:"), 1, 0)
        self.data_rate = QLabel("0")
        self.data_rate.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; }")
        perf_layout.addWidget(self.data_rate, 1, 1)
        
        layout.addWidget(perf_group)
        
        layout.addStretch()
        
        # Compteurs internes
        self._data_count = 0
    
    def update_sensor_status(self, connected: bool):
        if connected:
            self.sensor_status.setText("Connecté")
            self.sensor_status.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; }")
            self.sample_rate.setText("10 Hz")
        else:
            self.sensor_status.setText("Déconnecté")
            self.sensor_status.setStyleSheet("QLabel { color: #F44336; font-weight: bold; }")
            self.sample_rate.setText("0 Hz")
    
    def update_acquisition_status(self, running: bool):
        if running:
            self.acquisition_status.setText("Active")
            self.acquisition_status.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; }")
        else:
            self.acquisition_status.setText("Arrêtée")
            self.acquisition_status.setStyleSheet("QLabel { color: #F44336; font-weight: bold; }")
            self.data_rate.setText("0")
    
    def increment_data_count(self):
        self._data_count += 1
        self.data_count.setText(str(self._data_count))
        
        # Calculer approximativement le taux de données
        if self._data_count > 0:
            # Simulation simple - dans une vraie application, on calculerait le vrai taux
            self.data_rate.setText("10")
    
    def reset_counters(self):
        self._data_count = 0
        self.data_count.setText("0")
        self.data_rate.setText("0")