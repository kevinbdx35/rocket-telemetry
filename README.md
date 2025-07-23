# Rocket Telemetry System

A modern and modular telemetry system for rockets, developed in Python with a real-time dashboard GUI.

## Features

- **Modern GUI**: Professional PyQt5 dashboard with dark theme
- **Real-time Visualization**: Integrated matplotlib charts for all data
- **Modular Architecture**: Follows SOLID, DRY, and Clean Code principles
- **Sensor System**: Abstract interface for different sensor types
- **Data Validation**: Automatic validation with safety limits
- **Multi-format Storage**: JSON and CSV export capabilities
- **Advanced Logging**: Log system with automatic rotation
- **Complete Testing**: Unit and integration test coverage

## Project Structure

```
rocket_telemetry/
├── src/
│   ├── core/                 # Core data models
│   ├── sensors/              # Sensor interface and implementations
│   ├── data/                 # Data processing and storage
│   ├── gui/                  # Graphical user interface
│   │   └── widgets/          # Reusable UI components
│   └── utils/                # Utilities (logging, etc.)
├── tests/
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── config/                   # Configuration files
├── logs/                     # Log files
├── main.py                   # Main entry point
├── run_tests.py              # Test runner script
└── requirements.txt          # Python dependencies
```

## Installation

1. **Navigate to project** :
   ```bash
   cd rocket_telemetry
   ```

2. **Install dependencies** :
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Launch Application

```bash
python main.py
```

### Dashboard Interface

The interface is divided into several sections:

- **Control Panel**: Sensor connection, start/stop acquisition, data saving
- **Real-time Data**: Digital display of current values
- **Charts**: Real-time visualization by tabs (Altitude, Acceleration, Environment, Orientation)
- **System Status**: Component state and statistics

### Main Features

1. **Connect Sensor**: Click "Connect Sensor"
2. **Start Acquisition**: Click "Start Acquisition" button (green)
3. **Visualize Data**: Watch real-time chart updates
4. **Save Data**: Click "Save Data" button to export
5. **Stop**: Click "Stop Acquisition" button (red)

## Telemetry Data

The system collects and displays:

- **Flight**: Altitude (m), Velocity (m/s)
- **Acceleration**: X, Y, Z axes (m/s²)
- **Environment**: Temperature (°C), Pressure (hPa)
- **Orientation**: Roll, Pitch, Yaw (degrees)
- **System**: GPS (lat/lon), Battery voltage (V)

## Testing

Run all tests:

```bash
python run_tests.py
```

Unit tests only:
```bash
python -m unittest discover tests/unit
```

Integration tests only:
```bash
python -m unittest discover tests/integration
```

## Technical Architecture

### Design Principles

- **KISS**: Simple interface, readable code
- **DRY**: Reusable components, no duplication
- **SOLID**: Separation of concerns, extensibility
- **Clean Code**: Explicit naming, clear structure
- **Testability**: Complete test coverage

### Main Components

1. **TelemetryReading**: Immutable data model
2. **BaseSensor**: Abstract interface for sensors
3. **TelemetryProcessor**: Thread-safe real-time processing
4. **DataStorage**: Multi-format persistence
5. **MainWindow**: Modular graphical interface

### Observer Pattern

The system uses an Observer pattern for communication:
- Sensors produce data
- Processor validates and processes
- UI widgets are notified via callbacks
- Complete decoupling between components

## Extensibility

### Add New Sensor

1. Inherit from `BaseSensor`
2. Implement `connect()`, `disconnect()`, `read_data()`
3. Replace `MockRocketSensor` in `MainWindow`

### Add New Widget

1. Create in `src/gui/widgets/`
2. Inherit from `QWidget`
3. Implement `update_data()` method
4. Add to main layout

### New Export Format

1. Add method in `DataStorage`
2. Implement serialization
3. Add button in `ControlPanelWidget`

## Security

- Strict input data validation
- Safety limits on all parameters
- Robust error handling
- Detailed logs for audit trail

## Performance

- Threading to avoid UI blocking
- Circular buffers for limited memory
- Optimized chart updates
- Automatic log rotation