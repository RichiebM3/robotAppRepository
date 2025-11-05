# Robot App Repository - Architecture

## 📋 Overview

This document describes the architecture of the Robot App Repository, a unified codebase for managing multiple robot platforms with shared utilities and platform-specific implementations.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Robot App Repository                      │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│   Shared     │      │  Freenove    │     │   Spider     │
│   Modules    │      │   Hexapod    │     │    Robot     │
└──────────────┘      └──────────────┘     └──────────────┘
        │                     │                     │
        │                     │                     │
        ├─ servo_control      ├─ Client             ├─ Client
        ├─ sensors            ├─ Server             ├─ Server
        ├─ communication      └─ Data               └─ Data
        └─ utils
```

## 📦 Module Structure

### Shared Modules (`shared/`)

Reusable components that can be used across all robot platforms.

#### **servo_control/**
Enhanced servo control with health monitoring and calibration.

**Components:**
- `ServoEnhanced` - Main servo class with health monitoring
- `ServoCalibration` - Calibration utilities
- `ServoHealthMonitor` - Multi-servo health monitoring

**Features:**
- Real-time health monitoring
- Movement history tracking
- Calibration management
- Performance metrics
- Alert system

#### **sensors/**
Sensor interfaces and data processing (planned).

**Planned Components:**
- Ultrasonic distance sensors
- IMU (Inertial Measurement Unit)
- Camera/Vision processing
- Touch/Pressure sensors

#### **communication/**
Network and IPC communication utilities (planned).

**Planned Components:**
- WebSocket server/client
- REST API
- MQTT messaging
- Serial communication

#### **utils/**
General utility functions.

**Components:**
- Math utilities (interpolation, mapping, etc.)
- Data processing (filtering, smoothing)
- Logging utilities
- Configuration management
- File I/O helpers

### Platform-Specific Modules

#### **freenove_base/**
Freenove Big Hexapod robot implementation.

**Structure:**
```
freenove_base/
├── Freenove_Big_Hexapod/
│   ├── Client/              # Web interface
│   ├── Server/              # Robot control server
│   ├── data/
│   │   ├── recordings/      # Movement recordings
│   │   ├── calibrations/    # Servo calibrations
│   │   └── reports/         # Health reports
│   └── tests/               # Platform tests
```

#### **spider_client/** & **spider_server/**
Spider robot implementation (similar structure).

### Configuration (`config/`)

Centralized configuration management.

**Structure:**
```
config/
├── robot_configs/           # Robot-specific configs
│   ├── hexapod.json
│   └── spider.json
└── ai_configs/              # AI module configs
    ├── vision.json
    └── navigation.json
```

### AI Modules (`ai_modules/`)

AI and machine learning components (planned).

**Planned Components:**
- Computer vision
- Path planning
- Behavior learning
- Autonomous navigation

## 🔄 Data Flow

### Servo Control Flow

```
┌─────────────┐
│   Command   │ (move_to, move_smooth, etc.)
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ ServoEnhanced   │ - Validate angle
│                 │ - Apply calibration
│                 │ - Record movement
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Base Servo     │ - Execute movement
│  Controller     │ - Hardware interface
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Health Monitor  │ - Track metrics
│                 │ - Generate alerts
│                 │ - Log history
└─────────────────┘
```

### Health Monitoring Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Servo 1    │────▶│    Health    │────▶│   Alerts &   │
│   Servo 2    │────▶│   Monitor    │────▶│   Reports    │
│   Servo N    │────▶│              │────▶│              │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Dashboard   │
                     │  & Logging   │
                     └──────────────┘
```

## 🔌 Integration Points

### 1. Servo Control Integration

```python
from shared.servo_control import ServoEnhanced
from Freenove_Robot_Servo import Servo

# Create base servo
base_servo = Servo()

# Wrap with enhanced features
enhanced_servo = ServoEnhanced(
    channel=0,
    name="leg_1_hip",
    base_servo=base_servo
)

# Use enhanced features
enhanced_servo.move_to(90, duration=1.0)
health = enhanced_servo.get_health_status()
```

### 2. Health Monitoring Integration

```python
from shared.servo_control import ServoHealthMonitor

# Create monitor
monitor = ServoHealthMonitor()

# Register servos
for servo in robot.servos:
    monitor.register_servo(servo)

# Start monitoring
monitor.start_monitoring()

# Access health data
dashboard = monitor.generate_dashboard()
```

### 3. Configuration Integration

```python
from shared.utils import ConfigManager

# Load configuration
config_mgr = ConfigManager()
robot_config = config_mgr.load('hexapod')

# Use configuration
servo_config = robot_config['servos']['leg_1_hip']
```

## 📊 Data Storage

### Directory Structure

```
robotAppRepository/
├── data/                    # Runtime data (gitignored)
│   ├── recordings/          # Movement recordings
│   ├── calibrations/        # Servo calibrations
│   ├── health/              # Health monitoring data
│   └── logs/                # Application logs
│
├── config/                  # Configuration files
│   ├── robot_configs/       # Robot configurations
│   └── ai_configs/          # AI configurations
│
└── freenove_base/
    └── Freenove_Big_Hexapod/
        └── data/            # Platform-specific data
```

### Data Formats

#### Calibration Data (JSON)
```json
{
  "profile_name": "hexapod_2024",
  "servos": {
    "leg_1_hip": {
      "offset": 5.0,
      "scale": 1.0,
      "trim": 0.5,
      "min_angle": 0,
      "max_angle": 180
    }
  }
}
```

#### Health Report (JSON)
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "servos": {
    "leg_1_hip": {
      "temperature": 45.5,
      "current": 350.0,
      "status": "HEALTHY",
      "movements": 1234
    }
  }
}
```

## 🔐 Security Considerations

### Network Communication
- Use authentication for WebSocket/REST API
- Encrypt sensitive data
- Validate all inputs

### File System
- Restrict file permissions
- Validate file paths
- Sanitize user inputs

### Hardware Control
- Implement emergency stop
- Validate movement ranges
- Monitor for anomalies

## 🚀 Deployment

### Development Environment
```bash
# Clone repository
git clone <repository-url>

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### Production Environment
```bash
# On Raspberry Pi or robot controller
cd robotAppRepository

# Activate environment
source venv/bin/activate

# Start robot server
python freenove_base/Freenove_Big_Hexapod/Server/server.py
```

## 📈 Performance Considerations

### Servo Control
- Update rate: 50-100 Hz typical
- Movement smoothing: Linear/ease interpolation
- Health checks: 1-10 Hz (configurable)

### Memory Usage
- Movement history: Limited to last 100 movements per servo
- Health history: Limited to last 1000 records per servo
- Alert history: Limited to last 100 alerts

### CPU Usage
- Background monitoring: Low priority thread
- Main control loop: High priority
- Data logging: Asynchronous when possible

## 🔧 Extensibility

### Adding New Robot Platforms

1. Create platform directory:
```
new_robot/
├── client/
├── server/
├── data/
└── tests/
```

2. Use shared modules:
```python
from shared.servo_control import ServoEnhanced
from shared.utils import setup_logger
```

3. Implement platform-specific code:
```python
class NewRobotController:
    def __init__(self):
        self.servos = [
            ServoEnhanced(channel=i, name=f"servo_{i}")
            for i in range(12)
        ]
```

### Adding New Sensors

1. Create sensor module in `shared/sensors/`
2. Implement standard interface
3. Add to `shared/sensors/__init__.py`

### Adding New Communication Protocols

1. Create protocol module in `shared/communication/`
2. Implement standard interface
3. Add to `shared/communication/__init__.py`

## 📚 Related Documentation

- [Servo Enhancement Guide](servo_enhancement_guide.md)
- [Servo Control README](../shared/servo_control/README.md)
- [API Documentation](api_reference.md) (planned)

## 🤝 Contributing

See main repository README for contribution guidelines.

## 📝 Version History

- **v1.0.0** (2024-01) - Initial architecture
  - Servo control module
  - Health monitoring
  - Calibration system
  - Basic utilities

---

*Last updated: 2024-01-15*
