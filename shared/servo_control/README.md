# Servo Control Module

Enhanced servo control system with health monitoring, calibration, and performance tracking capabilities for robotics applications.

## 📋 Overview

This module provides three main components:

1. **ServoEnhanced** - Enhanced servo class with health monitoring
2. **ServoCalibration** - Calibration utilities and tools
3. **ServoHealthMonitor** - Centralized health monitoring system

## 🚀 Quick Start

### Basic Usage

```python
from shared.servo_control import ServoEnhanced

# Create enhanced servo
servo = ServoEnhanced(
    channel=0,
    name="leg_1_hip",
    min_angle=0,
    max_angle=180
)

# Move servo
servo.move_to(90, duration=1.0)

# Check health
health = servo.get_health_status()
print(f"Status: {health['status']}")
print(f"Temperature: {health['health']['temperature']}°C")
```

### With Calibration

```python
from shared.servo_control import ServoEnhanced, ServoCalibration

# Load calibration
cal = ServoCalibration()
cal.load_calibration("my_robot_profile")

# Create servo and apply calibration
servo = ServoEnhanced(channel=0, name="leg_1_hip")
cal.apply_to_servo("leg_1_hip", servo)

# Servo now uses calibrated values
servo.move_to(90)
```

### Health Monitoring

```python
from shared.servo_control import ServoEnhanced, ServoHealthMonitor

# Create servos
servos = [
    ServoEnhanced(channel=i, name=f"servo_{i}")
    for i in range(4)
]

# Create monitor
monitor = ServoHealthMonitor()

# Register servos
for servo in servos:
    monitor.register_servo(servo)

# Start monitoring
monitor.start_monitoring()

# View dashboard
print(monitor.generate_dashboard())

# Export report
monitor.export_health_report()
```

## 📚 Components

### ServoEnhanced

Enhanced servo control with:
- ✅ Health monitoring (temperature, current, position)
- ✅ Movement history tracking
- ✅ Smooth interpolated movements
- ✅ Automatic error detection
- ✅ Calibration support
- ✅ Performance metrics

**Key Methods:**
- `move_to(angle, duration, speed, blocking)` - Move to target angle
- `move_smooth(angle, duration, interpolation)` - Smooth movement
- `get_health_status()` - Get current health metrics
- `update_health_metrics(temp, current, voltage)` - Update health data
- `set_calibration(offset, scale, trim)` - Apply calibration
- `export_data(filepath)` - Export servo data to JSON

### ServoCalibration

Calibration utilities including:
- ✅ Interactive calibration wizard
- ✅ Automated calibration routines
- ✅ Save/load calibration profiles
- ✅ Bulk calibration for multiple servos
- ✅ Calibration reports

**Key Methods:**
- `calibrate_servo_interactive(servo_name)` - Interactive calibration
- `calibrate_servo_auto(servo_name, servo_obj)` - Automated calibration
- `save_calibration(profile_name)` - Save calibration profile
- `load_calibration(profile_name)` - Load calibration profile
- `apply_to_servo(servo_name, servo_obj)` - Apply calibration
- `generate_report()` - Generate calibration report

### ServoHealthMonitor

Centralized monitoring system:
- ✅ Monitor multiple servos simultaneously
- ✅ Configurable alert thresholds
- ✅ Health trend analysis
- ✅ Real-time dashboard
- ✅ Export health reports

**Key Methods:**
- `register_servo(servo_obj, thresholds)` - Register servo for monitoring
- `start_monitoring()` - Start continuous monitoring
- `stop_monitoring()` - Stop monitoring
- `get_health_summary()` - Get system health summary
- `generate_dashboard()` - Generate console dashboard
- `export_health_report(filename)` - Export comprehensive report

## 🔧 Configuration

### Default Thresholds

```python
DEFAULT_THRESHOLDS = {
    'temp_warning': 60.0,      # °C
    'temp_critical': 75.0,     # °C
    'current_warning': 800.0,  # mA
    'current_critical': 1000.0, # mA
    'position_error': 5.0      # degrees
}
```

### Calibration Parameters

```python
calibration = {
    'offset': 0.0,    # Angle offset in degrees
    'scale': 1.0,     # Scaling factor
    'trim': 0.0       # Fine-tuning trim
}
```

## 📊 Data Storage

### Directory Structure

```
data/
├── calibrations/          # Calibration profiles (.json)
├── health/               # Health monitoring data (.json)
└── reports/              # Generated reports (.txt, .json)
```

### Calibration File Format

```json
{
  "profile_name": "my_robot",
  "created_at": "2024-01-15T10:30:00",
  "servo_count": 12,
  "servos": {
    "leg_1_hip": {
      "offset": 5.0,
      "scale": 1.0,
      "trim": 0.5,
      "min_angle": 0,
      "max_angle": 180,
      "calibrated_at": "2024-01-15T10:30:00"
    }
  }
}
```

## 🛠️ Command-Line Tools

### Calibration Tool

```bash
python shared/servo_control/servo_calibration.py
```

Interactive menu for:
- Calibrating servos
- Managing calibration profiles
- Generating reports

### Health Monitor Test

```bash
python shared/servo_control/servo_health_monitor.py
```

Runs test monitoring with mock servos.

## 🔌 Integration Examples

### With Freenove Hexapod

```python
from Freenove_Robot_Servo import Servo
from shared.servo_control import ServoEnhanced

# Create base servo
base_servo = Servo()

# Create enhanced servo
servo = ServoEnhanced(
    channel=0,
    name="leg_1_hip",
    base_servo=base_servo
)

# Use enhanced features
servo.move_to(90, duration=1.0)
health = servo.get_health_status()
```

### With Custom Robot

```python
from shared.servo_control import ServoEnhanced, ServoHealthMonitor

# Create servos for your robot
servos = {
    'shoulder': ServoEnhanced(channel=0, name='shoulder'),
    'elbow': ServoEnhanced(channel=1, name='elbow'),
    'wrist': ServoEnhanced(channel=2, name='wrist')
}

# Setup monitoring
monitor = ServoHealthMonitor()
for servo in servos.values():
    monitor.register_servo(servo)

monitor.start_monitoring()

# Use servos
servos['shoulder'].move_to(45)
servos['elbow'].move_to(90)

# Check health
print(monitor.generate_dashboard())
```

## 📈 Performance Metrics

Each servo tracks:
- Total movements
- Total distance traveled (degrees)
- Average speed
- Error count
- Warning count
- Uptime

Access via:
```python
stats = servo.get_movement_stats()
```

## ⚠️ Error Handling

The module includes comprehensive error handling:

```python
# Errors are logged and accessible
health = servo.get_health_status()
print(health['errors'])    # Recent errors
print(health['warnings'])  # Recent warnings

# Reset counters
servo.reset_health_counters()
```

## 🧪 Testing

Run tests with:

```bash
python tests/test_servo_enhanced.py
```

## 📝 License

Part of the Robot App Repository project.

## 👥 Contributing

Contributions welcome! Please follow the project's coding standards.

## 📞 Support

For issues or questions, please refer to the main repository documentation.
