import sys
from typing import Optional
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QTabWidget, QStatusBar,
                             QGridLayout, QFrame, QSplitter, QSizePolicy)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

from .widgets.telemetry_display import TelemetryDisplayWidget
from .widgets.graph_widget import GraphWidget
from .widgets.control_panel import ControlPanelWidget
from .widgets.status_widget import StatusWidget
from ..core.telemetry_data import TelemetryReading
from ..sensors.mock_sensor import MockRocketSensor
from ..data.data_processor import TelemetryProcessor
from ..data.data_storage import DataStorage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Système de Télémétrie Fusée")
        self.setMinimumSize(800, 600)
        self.resize(1400, 900)
        self.showMaximized()
        
        # Composants principaux
        self.sensor = MockRocketSensor()
        self.data_processor = TelemetryProcessor()
        self.data_storage = DataStorage()
        
        # Timer pour la lecture des données
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.read_sensor_data)
        
        self.setup_ui()
        self.setup_connections()
        self.apply_dark_theme()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter principal
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Panel de gauche (contrôles et status)
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Panel principal (données et graphiques)
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # Ratio des panels (25% - 75%)
        main_splitter.setSizes([300, 1100])
        main_splitter.setCollapsible(0, False)
        main_splitter.setCollapsible(1, False)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt - Capteur déconnecté")
    
    def create_left_panel(self) -> QWidget:
        left_widget = QWidget()
        left_widget.setMinimumWidth(280)
        left_widget.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_widget)
        
        # Panel de contrôle
        self.control_panel = ControlPanelWidget()
        left_layout.addWidget(self.control_panel)
        
        # Widget de status
        self.status_widget = StatusWidget()
        left_layout.addWidget(self.status_widget)
        
        # Affichage des données en temps réel
        self.telemetry_display = TelemetryDisplayWidget()
        left_layout.addWidget(self.telemetry_display)
        
        left_layout.addStretch()
        
        return left_widget
    
    def create_right_panel(self) -> QWidget:
        right_widget = QWidget()
        right_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout = QVBoxLayout(right_widget)
        
        # Tabs pour différents graphiques
        tab_widget = QTabWidget()
        tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Tab altitude/vitesse
        self.altitude_graph = GraphWidget("Altitude (m)", "Temps (s)", "Altitude")
        tab_widget.addTab(self.altitude_graph, "Altitude")
        
        # Tab accélération
        self.acceleration_graph = GraphWidget("Accélération (m/s²)", "Temps (s)", "Accélération")
        tab_widget.addTab(self.acceleration_graph, "Accélération")
        
        # Tab température/pression
        self.env_graph = GraphWidget("Valeurs", "Temps (s)", "Environnement")
        tab_widget.addTab(self.env_graph, "Environnement")
        
        # Tab orientation
        self.orientation_graph = GraphWidget("Degrés", "Temps (s)", "Orientation")
        tab_widget.addTab(self.orientation_graph, "Orientation")
        
        right_layout.addWidget(tab_widget)
        
        return right_widget
    
    def setup_connections(self):
        # Connexions du panel de contrôle
        self.control_panel.connect_clicked.connect(self.connect_sensor)
        self.control_panel.start_clicked.connect(self.start_telemetry)
        self.control_panel.stop_clicked.connect(self.stop_telemetry)
        self.control_panel.save_clicked.connect(self.save_data)
        self.control_panel.clear_clicked.connect(self.clear_data)
        
        # Callback pour les nouvelles données
        self.data_processor.add_data_callback(self.update_displays)
    
    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        
        self.setPalette(dark_palette)
    
    def connect_sensor(self):
        if self.sensor.connect():
            self.status_bar.showMessage("Capteur connecté")
            self.status_widget.update_sensor_status(True)
        else:
            self.status_bar.showMessage("Erreur de connexion au capteur")
    
    def start_telemetry(self):
        if not self.sensor.is_connected:
            self.status_bar.showMessage("Connectez d'abord le capteur")
            return
        
        self.data_processor.start_processing()
        self.data_timer.start(int(1000 / self.sensor.sample_rate))
        self.status_bar.showMessage("Acquisition en cours...")
        self.status_widget.update_acquisition_status(True)
    
    def stop_telemetry(self):
        self.data_timer.stop()
        self.data_processor.stop_processing()
        self.status_bar.showMessage("Acquisition arrêtée")
        self.status_widget.update_acquisition_status(False)
    
    def read_sensor_data(self):
        reading = self.sensor.read_data()
        if reading:
            self.data_processor.add_reading(reading)
    
    def update_displays(self, reading: TelemetryReading):
        # Mettre à jour l'affichage des données
        self.telemetry_display.update_data(reading)
        
        # Mettre à jour les graphiques
        timestamp = reading.timestamp.timestamp()
        
        self.altitude_graph.add_data_point(timestamp, reading.altitude, "Altitude")
        self.altitude_graph.add_data_point(timestamp, reading.velocity, "Vitesse")
        
        self.acceleration_graph.add_data_point(timestamp, reading.acceleration['x'], "Acc X")
        self.acceleration_graph.add_data_point(timestamp, reading.acceleration['y'], "Acc Y")
        self.acceleration_graph.add_data_point(timestamp, reading.acceleration['z'], "Acc Z")
        
        self.env_graph.add_data_point(timestamp, reading.temperature, "Température")
        self.env_graph.add_data_point(timestamp, reading.pressure / 1000, "Pression (kPa)")
        
        self.orientation_graph.add_data_point(timestamp, reading.orientation['roll'], "Roll")
        self.orientation_graph.add_data_point(timestamp, reading.orientation['pitch'], "Pitch")
        self.orientation_graph.add_data_point(timestamp, reading.orientation['yaw'], "Yaw")
    
    def save_data(self):
        data = self.data_processor.get_all_data()
        if data:
            json_file = self.data_storage.save_to_json(data)
            csv_file = self.data_storage.save_to_csv(data)
            self.status_bar.showMessage(f"Données sauvegardées: {json_file}, {csv_file}")
        else:
            self.status_bar.showMessage("Aucune donnée à sauvegarder")
    
    def clear_data(self):
        self.data_processor.clear_data()
        self.altitude_graph.clear_data()
        self.acceleration_graph.clear_data()
        self.env_graph.clear_data()
        self.orientation_graph.clear_data()
        self.telemetry_display.clear_data()
        self.status_bar.showMessage("Données effacées")
    
    def closeEvent(self, event):
        self.stop_telemetry()
        self.sensor.disconnect()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Rocket Telemetry System")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())