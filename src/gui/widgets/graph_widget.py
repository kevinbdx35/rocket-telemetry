from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np
from collections import deque
from typing import Dict, List, Tuple
import time


class GraphWidget(QWidget):
    def __init__(self, y_label: str, x_label: str, title: str, max_points: int = 500):
        super().__init__()
        self.y_label = y_label
        self.x_label = x_label
        self.title = title
        self.max_points = max_points
        
        # Données pour les différentes séries
        self.data_series: Dict[str, deque] = {}
        self.time_series: Dict[str, deque] = {}
        self.colors = ['#2196F3', '#4CAF50', '#FF5722', '#FF9800', '#9C27B0', '#607D8B']
        self.color_index = 0
        
        self.setup_ui()
        self.start_time = time.time()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Configuration matplotlib pour thème sombre
        plt.style.use('dark_background')
        
        # Créer la figure
        self.figure = Figure(figsize=(12, 6), facecolor='#353535')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Créer l'axe
        self.ax = self.figure.add_subplot(111, facecolor='#2d2d2d')
        self.ax.set_xlabel(self.x_label, color='white')
        self.ax.set_ylabel(self.y_label, color='white')
        self.ax.set_title(self.title, color='white', fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        self.ax.tick_params(colors='white')
        
        # Dict pour stocker les lignes de plot
        self.lines: Dict[str, plt.Line2D] = {}
        
        # Configuration des limites initiales
        self.ax.set_xlim(0, 60)  # 60 secondes par défaut
        self.ax.set_ylim(-10, 10)  # Limites par défaut
        
        self.canvas.draw()
    
    def add_data_point(self, timestamp: float, value: float, series_name: str):
        # Convertir timestamp en temps relatif
        relative_time = timestamp - self.start_time if hasattr(self, 'start_time') else 0
        
        # Initialiser la série si elle n'existe pas
        if series_name not in self.data_series:
            self.data_series[series_name] = deque(maxlen=self.max_points)
            self.time_series[series_name] = deque(maxlen=self.max_points)
            
            # Créer une nouvelle ligne
            color = self.colors[self.color_index % len(self.colors)]
            line, = self.ax.plot([], [], label=series_name, color=color, linewidth=2)
            self.lines[series_name] = line
            self.color_index += 1
            
            # Mettre à jour la légende
            self.ax.legend(loc='upper left', fancybox=True, framealpha=0.8)
        
        # Ajouter les nouvelles données
        self.data_series[series_name].append(value)
        self.time_series[series_name].append(relative_time)
        
        # Mettre à jour la ligne
        self.lines[series_name].set_data(list(self.time_series[series_name]), 
                                        list(self.data_series[series_name]))
        
        # Ajuster les limites
        self._update_limits()
        
        # Redessiner
        self.canvas.draw_idle()
    
    def _update_limits(self):
        if not self.data_series:
            return
        
        # Calculer les limites temporelles
        all_times = []
        all_values = []
        
        for series_name in self.data_series:
            if self.time_series[series_name]:
                all_times.extend(list(self.time_series[series_name]))
                all_values.extend(list(self.data_series[series_name]))
        
        if all_times and all_values:
            time_min, time_max = min(all_times), max(all_times)
            value_min, value_max = min(all_values), max(all_values)
            
            # Limites temporelles avec un peu de marge
            time_range = max(60, time_max - time_min + 10)
            self.ax.set_xlim(max(0, time_max - time_range), time_max + 5)
            
            # Limites de valeurs avec marge
            if value_max != value_min:
                value_range = value_max - value_min
                margin = value_range * 0.1
                self.ax.set_ylim(value_min - margin, value_max + margin)
            else:
                # Si toutes les valeurs sont identiques
                self.ax.set_ylim(value_min - 1, value_max + 1)
    
    def clear_data(self):
        # Effacer toutes les données
        self.data_series.clear()
        self.time_series.clear()
        
        # Effacer toutes les lignes
        for line in self.lines.values():
            line.remove()
        self.lines.clear()
        
        # Réinitialiser les paramètres
        self.color_index = 0
        self.start_time = time.time()
        
        # Remettre les limites par défaut
        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(-10, 10)
        self.ax.legend().remove() if self.ax.get_legend() else None
        
        # Redessiner
        self.canvas.draw()
    
    def export_plot(self, filename: str):
        self.figure.savefig(filename, dpi=300, bbox_inches='tight', 
                          facecolor='#353535', edgecolor='none')
    
    def set_y_limits(self, min_val: float, max_val: float):
        self.ax.set_ylim(min_val, max_val)
        self.canvas.draw()