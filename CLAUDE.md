# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Run Application
```bash
python main.py
```

### Testing
```bash
# Run all tests
python run_tests.py

# Unit tests only
python -m unittest discover tests/unit

# Integration tests only
python -m unittest discover tests/integration
```

### Dependencies
```bash
pip install -r requirements.txt
```

## Architecture Overview

This is a modular rocket telemetry system built with Python and PyQt5 following the Observer pattern and SOLID principles.

### Core Components

- **TelemetryReading** (`src/core/telemetry_data.py`): Immutable dataclass containing flight data (altitude, velocity, acceleration, temperature, pressure, orientation, GPS, battery)
- **TelemetryDataValidator**: Validates readings with safety limits
- **BaseSensor** (`src/sensors/base_sensor.py`): Abstract interface for all sensor implementations
- **TelemetryProcessor** (`src/data/data_processor.py`): Thread-safe data processing with callback system
- **DataStorage** (`src/data/data_storage.py`): Multi-format persistence (JSON, CSV)
- **MainWindow** (`src/gui/main_window.py`): Main PyQt5 interface with modular widgets

### Data Flow

1. Sensors produce `TelemetryReading` objects
2. `TelemetryProcessor` validates and buffers data in separate thread
3. Observer callbacks notify GUI widgets for real-time updates
4. `DataStorage` handles persistence in multiple formats

### Key Patterns

- **Observer Pattern**: Components communicate via callbacks, enabling loose coupling
- **Abstract Factory**: `BaseSensor` provides interface for different sensor types
- **Threading**: Non-blocking UI with background data processing
- **Validation**: All telemetry data validated against safety limits

### GUI Structure

- Uses PyQt5 with dark theme
- Modular widget system in `src/gui/widgets/`
- Real-time matplotlib charts with tabs for different data types
- Control panel for sensor management and data export

### Extension Points

- **New Sensors**: Inherit from `BaseSensor`, implement `connect()`, `disconnect()`, `read_data()`
- **New Widgets**: Create in `src/gui/widgets/`, implement `update_data()` method
- **Export Formats**: Add methods to `DataStorage` class

### French Comments

Note: The codebase contains French comments and docstrings (`Système de Télémétrie pour Fusée`). This is the original language used by the developers.