from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGroupBox, 
                             QGridLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from typing import Optional
from ...core.telemetry_data import TelemetryReading


class TelemetryDisplayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("Données Temps Réel")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Group altitude/vitesse
        flight_group = QGroupBox("Vol")
        flight_layout = QGridLayout(flight_group)
        
        # Altitude
        flight_layout.addWidget(QLabel("Altitude:"), 0, 0)
        self.altitude_label = QLabel("0.0 m")
        self.altitude_label.setStyleSheet("QLabel { color: #2196F3; font-weight: bold; font-size: 14px; }")
        flight_layout.addWidget(self.altitude_label, 0, 1)
        
        # Vitesse
        flight_layout.addWidget(QLabel("Vitesse:"), 1, 0)
        self.velocity_label = QLabel("0.0 m/s")
        self.velocity_label.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; font-size: 14px; }")
        flight_layout.addWidget(self.velocity_label, 1, 1)
        
        layout.addWidget(flight_group)
        
        # Group accélération
        accel_group = QGroupBox("Accélération")
        accel_layout = QGridLayout(accel_group)
        
        accel_layout.addWidget(QLabel("X:"), 0, 0)
        self.accel_x_label = QLabel("0.0 m/s²")
        self.accel_x_label.setStyleSheet("QLabel { color: #FF5722; font-weight: bold; }")
        accel_layout.addWidget(self.accel_x_label, 0, 1)
        
        accel_layout.addWidget(QLabel("Y:"), 1, 0)
        self.accel_y_label = QLabel("0.0 m/s²")
        self.accel_y_label.setStyleSheet("QLabel { color: #FF5722; font-weight: bold; }")
        accel_layout.addWidget(self.accel_y_label, 1, 1)
        
        accel_layout.addWidget(QLabel("Z:"), 2, 0)
        self.accel_z_label = QLabel("0.0 m/s²")
        self.accel_z_label.setStyleSheet("QLabel { color: #FF5722; font-weight: bold; }")
        accel_layout.addWidget(self.accel_z_label, 2, 1)
        
        layout.addWidget(accel_group)
        
        # Group environnement
        env_group = QGroupBox("Environnement")
        env_layout = QGridLayout(env_group)
        
        env_layout.addWidget(QLabel("Température:"), 0, 0)
        self.temp_label = QLabel("0.0 °C")
        self.temp_label.setStyleSheet("QLabel { color: #FF9800; font-weight: bold; }")
        env_layout.addWidget(self.temp_label, 0, 1)
        
        env_layout.addWidget(QLabel("Pression:"), 1, 0)
        self.pressure_label = QLabel("0.0 hPa")
        self.pressure_label.setStyleSheet("QLabel { color: #9C27B0; font-weight: bold; }")
        env_layout.addWidget(self.pressure_label, 1, 1)
        
        layout.addWidget(env_group)
        
        # Group orientation
        orient_group = QGroupBox("Orientation")
        orient_layout = QGridLayout(orient_group)
        
        orient_layout.addWidget(QLabel("Roll:"), 0, 0)
        self.roll_label = QLabel("0.0°")
        self.roll_label.setStyleSheet("QLabel { color: #607D8B; font-weight: bold; }")
        orient_layout.addWidget(self.roll_label, 0, 1)
        
        orient_layout.addWidget(QLabel("Pitch:"), 1, 0)
        self.pitch_label = QLabel("0.0°")
        self.pitch_label.setStyleSheet("QLabel { color: #607D8B; font-weight: bold; }")
        orient_layout.addWidget(self.pitch_label, 1, 1)
        
        orient_layout.addWidget(QLabel("Yaw:"), 2, 0)
        self.yaw_label = QLabel("0.0°")
        self.yaw_label.setStyleSheet("QLabel { color: #607D8B; font-weight: bold; }")
        orient_layout.addWidget(self.yaw_label, 2, 1)
        
        layout.addWidget(orient_group)
        
        # Group GPS/Batterie
        misc_group = QGroupBox("Système")
        misc_layout = QGridLayout(misc_group)
        
        misc_layout.addWidget(QLabel("Latitude:"), 0, 0)
        self.lat_label = QLabel("0.0°")
        self.lat_label.setStyleSheet("QLabel { color: #795548; font-weight: bold; }")
        misc_layout.addWidget(self.lat_label, 0, 1)
        
        misc_layout.addWidget(QLabel("Longitude:"), 1, 0)
        self.lon_label = QLabel("0.0°")
        self.lon_label.setStyleSheet("QLabel { color: #795548; font-weight: bold; }")
        misc_layout.addWidget(self.lon_label, 1, 1)
        
        misc_layout.addWidget(QLabel("Batterie:"), 2, 0)
        self.battery_label = QLabel("0.0 V")
        self.battery_label.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; }")
        misc_layout.addWidget(self.battery_label, 2, 1)
        
        layout.addWidget(misc_group)
        
        layout.addStretch()
    
    def update_data(self, reading: TelemetryReading):
        # Mettre à jour tous les labels avec les nouvelles données
        self.altitude_label.setText(f"{reading.altitude:.1f} m")
        self.velocity_label.setText(f"{reading.velocity:.1f} m/s")
        
        self.accel_x_label.setText(f"{reading.acceleration['x']:.1f} m/s²")
        self.accel_y_label.setText(f"{reading.acceleration['y']:.1f} m/s²")
        self.accel_z_label.setText(f"{reading.acceleration['z']:.1f} m/s²")
        
        self.temp_label.setText(f"{reading.temperature:.1f} °C")
        self.pressure_label.setText(f"{reading.pressure/100:.1f} hPa")
        
        self.roll_label.setText(f"{reading.orientation['roll']:.1f}°")
        self.pitch_label.setText(f"{reading.orientation['pitch']:.1f}°")
        self.yaw_label.setText(f"{reading.orientation['yaw']:.1f}°")
        
        if reading.gps_coordinates:
            self.lat_label.setText(f"{reading.gps_coordinates['lat']:.6f}°")
            self.lon_label.setText(f"{reading.gps_coordinates['lon']:.6f}°")
        
        if reading.battery_voltage:
            self.battery_label.setText(f"{reading.battery_voltage:.1f} V")
            
            # Changer la couleur selon le niveau de batterie
            if reading.battery_voltage > 11.0:
                self.battery_label.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; }")
            elif reading.battery_voltage > 10.0:
                self.battery_label.setStyleSheet("QLabel { color: #FF9800; font-weight: bold; }")
            else:
                self.battery_label.setStyleSheet("QLabel { color: #F44336; font-weight: bold; }")
    
    def clear_data(self):
        # Remettre toutes les valeurs à zéro
        self.altitude_label.setText("0.0 m")
        self.velocity_label.setText("0.0 m/s")
        self.accel_x_label.setText("0.0 m/s²")
        self.accel_y_label.setText("0.0 m/s²")
        self.accel_z_label.setText("0.0 m/s²")
        self.temp_label.setText("0.0 °C")
        self.pressure_label.setText("0.0 hPa")
        self.roll_label.setText("0.0°")
        self.pitch_label.setText("0.0°")
        self.yaw_label.setText("0.0°")
        self.lat_label.setText("0.0°")
        self.lon_label.setText("0.0°")
        self.battery_label.setText("0.0 V")
        self.battery_label.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; }")