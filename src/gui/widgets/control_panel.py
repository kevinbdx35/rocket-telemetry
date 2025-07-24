from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QGroupBox, 
                             QLabel, QSpinBox, QHBoxLayout, QSizePolicy)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class ControlPanelWidget(QWidget):
    connect_clicked = pyqtSignal()
    start_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    save_clicked = pyqtSignal()
    clear_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("Contrôle de Mission")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Group box connexion
        connection_group = QGroupBox("Connexion Capteur")
        connection_layout = QVBoxLayout(connection_group)
        
        self.connect_btn = QPushButton("Connecter Capteur")
        self.connect_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.connect_btn.setMinimumHeight(35)
        self.connect_btn.clicked.connect(self.connect_clicked.emit)
        connection_layout.addWidget(self.connect_btn)
        
        layout.addWidget(connection_group)
        
        # Group box acquisition
        acquisition_group = QGroupBox("Acquisition Données")
        acquisition_layout = QVBoxLayout(acquisition_group)
        
        # Boutons start/stop
        self.start_btn = QPushButton("Démarrer Acquisition")
        self.start_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.start_btn.setMinimumHeight(35)
        self.start_btn.setStyleSheet("QPushButton { background-color: #2E7D32; }")
        self.start_btn.clicked.connect(self.start_clicked.emit)
        acquisition_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Arrêter Acquisition")
        self.stop_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.stop_btn.setMinimumHeight(35)
        self.stop_btn.setStyleSheet("QPushButton { background-color: #C62828; }")
        self.stop_btn.clicked.connect(self.stop_clicked.emit)
        acquisition_layout.addWidget(self.stop_btn)
        
        layout.addWidget(acquisition_group)
        
        # Group box données
        data_group = QGroupBox("Gestion Données")
        data_layout = QVBoxLayout(data_group)
        
        self.save_btn = QPushButton("Sauvegarder Données")
        self.save_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.save_btn.setMinimumHeight(30)
        self.save_btn.clicked.connect(self.save_clicked.emit)
        data_layout.addWidget(self.save_btn)
        
        self.clear_btn = QPushButton("Effacer Données")
        self.clear_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.clear_btn.setMinimumHeight(30)
        self.clear_btn.setStyleSheet("QPushButton { background-color: #FF8F00; }")
        self.clear_btn.clicked.connect(self.clear_clicked.emit)
        data_layout.addWidget(self.clear_btn)
        
        layout.addWidget(data_group)
        
        layout.addStretch()