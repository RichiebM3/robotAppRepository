# Servo Enhancement Guide

Complete guide to using the enhanced servo control system with health monitoring, calibration, and performance tracking.

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Basic Usage](#basic-usage)
4. [Health Monitoring](#health-monitoring)
5. [Calibration](#calibration)
6. [Advanced Features](#advanced-features)
7. [Integration Examples](#integration-examples)
8. [Troubleshooting](#troubleshooting)

## 🎯 Introduction

The servo enhancement system provides three main components:

- **ServoEnhanced** - Individual servo with health monitoring
- **ServoCalibration** - Calibration tools and management
- **ServoHealthMonitor** - System-wide health monitoring

### Key Features

✅ Real-time health monitoring (temperature, current, voltage)  
✅ Movement history and analytics  
✅ Automatic error detection  
✅ Calibration management  
✅ Performance metrics  
✅ Data export capabilities  

## 🚀 Quick Start

### Installation

```bash
# Navigate to project root
cd robotAppRepository

# Ensure shared module is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Basic Example

```python
from shared.servo_control import ServoEnhanced

# Create servo
servo = ServoEnhanced(
    channel=0,
    name="my_servo",
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

## 📖 Basic Usage

### Creating a Servo

```python
from shared.servo_control import ServoEnhanced

servo = ServoEnhanced(
    channel=0,              # Servo channel (0-15 typically)
    name="leg_1_hip",       # Human-readable name
    min_angle=0,            # Minimum safe angle
    max_angle=180,          # Maximum safe angle
    default_speed=50,       # Default speed (degrees/second)
    base_servo=None         # Optional: underlying servo object
)
```

### Moving the Servo

#### Simple Movement

```python
# Move to angle (non-blocking)
servo.move_to(90)

# Move with duration
servo.move_to(90, duration=2.0)

# Move with speed
servo.move_to(90, speed=30)  # 30 degrees/second

# Move and wait (blocking)
servo.move_to(90, duration=1.0, blocking=True)
```

#### Smooth Movement

```python
# Smooth movement with interpolation
servo.move_smooth(90, duration=2.0, interpolation='ease_in_out')

# Interpolation options:
# - 'linear'       : Constant speed
# - 'ease_in'      : Slow start, fast end
# - 'ease_out'     : Fast start, slow end
# - 'ease_in_out'  : Slow start and end
```

### Getting Servo State

```python
# Current angle
print(f"Current angle: {servo.current_angle}°")

# Target angle
print(f"Target angle: {servo.target_angle}°")

# Is moving?
print(f"Moving: {servo.is_moving}")
```

## 🏥 Health Monitoring

### Checking Health Status

```python
health = servo.get_health_status()

print(f"Servo: {health['servo_name']}")
print(f"Status: {health['status']}")  # HEALTHY, WARNING, CRITICAL, ERROR
print(f"Temperature: {health['health']['temperature']}°C")
print(f"Current: {health['health']['current']}mA")
print(f"Voltage: {health['health']['voltage']}V")
print(f"Total Movements: {health['health']['total_movements']}")
print(f"Errors: {health['health']['error_count']}")
```

### Updating Health Metrics

```python
# Update from sensor readings
servo.update_health_metrics(
    temperature=45.5,  # Celsius
    current=350.0,     # mA
    voltage=5.0        # V
)
```

### Health Status Levels

| Status | Description | Conditions |
|--------|-------------|------------|
| **HEALTHY** | Normal operation | All metrics within safe ranges |
| **WARNING** | Attention needed | Temperature 60-75°C or Current 800-1000mA |
| **CRITICAL** | Immediate action required | Temperature >75°C or Current >1000mA |
| **ERROR** | Malfunction detected | Movement failures or other errors |

### Configuring Thresholds

```python
# Customize warning/critical thresholds
servo.thresholds = {
    'temp_warning': 55.0,      # °C
    'temp_critical': 70.0,     # °C
    'current_warning': 750.0,  # mA
    'current_critical': 950.0, # mA
    'position_error': 5.0      # degrees
}
```

### Movement Statistics

```python
stats = servo.get_movement_stats()

print(f"Total Movements: {stats['total_movements']}")
print(f"Total Distance: {stats['total_distance']}°")
print(f"Average Speed: {stats['average_speed']}°/s")
print(f"Uptime: {stats['uptime']}s")
```

### Resetting Health Data

```python
# Reset error/warning counters
servo.reset_health_counters()
```

## 🎯 Calibration

### Interactive Calibration

```python
from shared.servo_control import ServoCalibration

# Create calibration tool
cal = ServoCalibration()

# Run interactive calibration wizard
calibration_data = cal.calibrate_servo_interactive("leg_1_hip")

# Save calibration profile
cal.save_calibration("my_robot_v1")
```

### Automated Calibration

```python
# Automated calibration (requires position feedback)
calibration_data = cal.calibrate_servo_auto(
    servo_name="leg_1_hip",
    servo_obj=servo,
    test_angles=[0, 45, 90, 135, 180]
)
```

### Loading Calibration

```python
# Load existing calibration profile
cal.load_calibration("my_robot_v1")

# Apply to servo
cal.apply_to_servo("leg_1_hip", servo)
```

### Manual Calibration

```python
# Set calibration parameters directly
servo.set_calibration(
    offset=5.0,   # Angle offset in degrees
    scale=1.0,    # Scaling factor
    trim=0.5      # Fine-tuning trim
)
```

### Calibration Parameters Explained

#### Offset
Corrects systematic angle errors.
- **Example**: If servo is at 85° when commanded 90°, set offset to 5.0

#### Scale
Corrects range compression/expansion.
- **Example**: If servo only moves 160° when commanded 180°, set scale to 0.89

#### Trim
Fine-tunes center position.
- **Example**: Small adjustments (±2°) to perfect center position

### Calibration Reports

```python
# Generate calibration report
report = cal.generate_report()
print(report)

# Export to file
cal.export_report("calibration_report_2024.txt")
```

## 🔍 Advanced Features

### System-Wide Health Monitoring

```python
from shared.servo_control import ServoHealthMonitor

# Create monitor
monitor = ServoHealthMonitor(
    update_interval=1.0,    # Check every 1 second
    history_size=1000,      # Keep 1000 historical records
    data_dir="data/health"  # Data storage directory
)

# Register servos
servos = [servo1, servo2, servo3, servo4]
for servo in servos:
    monitor.register_servo(servo)

# Start continuous monitoring
monitor.start_monitoring()

# View dashboard
print(monitor.generate_dashboard())

# Get health summary
summary = monitor.get_health_summary()

# Export health report
monitor.export_health_report("health_report_2024.json")

# Stop monitoring
monitor.stop_monitoring()
```

### Custom Alert Thresholds

```python
# Register servo with custom thresholds
custom_thresholds = {
    'temp_warning': 55.0,
    'temp_critical': 70.0,
    'current_warning': 750.0,
    'current_critical': 950.0
}

monitor.register_servo(servo, thresholds=custom_thresholds)
```

### Health Trends Analysis

```python
# Get temperature trends for last 60 seconds
trends = monitor.get_health_trends(
    servo_name="leg_1_hip",
    metric="temperature",
    duration=60
)

# Plot trends (requires matplotlib)
import matplotlib.pyplot as plt

times = [t['timestamp'] for t in trends]
values = [t['value'] for t in trends]

plt.plot(times, values)
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.title('Servo Temperature Trend')
plt.show()
```

### Data Export

```python
# Export servo data to JSON
servo.export_data("servo_data_2024.json")

# Exported data includes:
# - Servo configuration
# - Current state
# - Health metrics
# - Calibration data
# - Movement history
# - Errors and warnings
```

## 🔌 Integration Examples

### Example 1: Hexapod Leg Control

```python
from shared.servo_control import ServoEnhanced, ServoHealthMonitor

class HexapodLeg:
    def __init__(self, leg_id):
        self.leg_id = leg_id
        
        # Create servos for hip, knee, ankle
        self.hip = ServoEnhanced(
            channel=leg_id * 3 + 0,
            name=f"leg_{leg_id}_hip",
            min_angle=0,
            max_angle=180
        )
        
        self.knee = ServoEnhanced(
            channel=leg_id * 3 + 1,
            name=f"leg_{leg_id}_knee",
            min_angle=0,
            max_angle=180
        )
        
        self.ankle = ServoEnhanced(
            channel=leg_id * 3 + 2,
            name=f"leg_{leg_id}_ankle",
            min_angle=0,
            max_angle=180
        )
    
    def move_to_position(self, hip_angle, knee_angle, ankle_angle, duration=1.0):
        """Move leg to position."""
        self.hip.move_to(hip_angle, duration=duration)
        self.knee.move_to(knee_angle, duration=duration)
        self.ankle.move_to(ankle_angle, duration=duration)
    
    def get_health(self):
        """Get health status of all servos."""
        return {
            'hip': self.hip.get_health_status(),
            'knee': self.knee.get_health_status(),
            'ankle': self.ankle.get_health_status()
        }

# Create hexapod with 6 legs
hexapod_legs = [HexapodLeg(i) for i in range(6)]

# Setup health monitoring
monitor = ServoHealthMonitor()
for leg in hexapod_legs:
    monitor.register_servo(leg.hip)
    monitor.register_servo(leg.knee)
    monitor.register_servo(leg.ankle)

monitor.start_monitoring()

# Move legs
hexapod_legs[0].move_to_position(90, 90, 90, duration=2.0)

# Check health
print(monitor.generate_dashboard())
```

### Example 2: Calibration Workflow

```python
from shared.servo_control import ServoEnhanced, ServoCalibration

# Create servos
servos = {
    'leg_1_hip': ServoEnhanced(channel=0, name='leg_1_hip'),
    'leg_1_knee': ServoEnhanced(channel=1, name='leg_1_knee'),
    'leg_1_ankle': ServoEnhanced(channel=2, name='leg_1_ankle'),
}

# Create calibration tool
cal = ServoCalibration()

# Calibrate each servo
for name, servo in servos.items():
    print(f"\nCalibrating {name}...")
    cal.calibrate_servo_interactive(name, servo)

# Save calibration profile
cal.save_calibration("hexapod_leg_1")

# Later: Load and apply calibration
cal.load_calibration("hexapod_leg_1")
for name, servo in servos.items():
    cal.apply_to_servo(name, servo)

# Generate report
print(cal.generate_report())
```

### Example 3: Real-time Monitoring Dashboard

```python
import time
from shared.servo_control import ServoEnhanced, ServoHealthMonitor

# Create servos
servos = [
    ServoEnhanced(channel=i, name=f"servo_{i}")
    for i in range(4)
]

# Setup monitoring
monitor = ServoHealthMonitor(update_interval=0.5)
for servo in servos:
    monitor.register_servo(servo)

monitor.start_monitoring()

# Simulate robot operation
try:
    while True:
        # Move servos
        for servo in servos:
            import random
            angle = random.randint(0, 180)
            servo.move_to(angle, duration=0.5)
        
        # Update health (simulate sensor readings)
        for servo in servos:
            temp = random.uniform(30, 60)
            current = random.uniform(200, 800)
            servo.update_health_metrics(temperature=temp, current=current)
        
        # Display dashboard
        print("\033[2J\033[H")  # Clear screen
        print(monitor.generate_dashboard())
        
        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping...")
    monitor.stop_monitoring()
    monitor.export_health_report()
```

## 🔧 Troubleshooting

### Common Issues

#### Issue: Servo not moving

**Possible causes:**
- Angle out of range
- Hardware not connected
- Base servo not configured

**Solution:**
```python
# Check angle validity
if not servo._validate_angle(angle):
    print(f"Angle {angle} out of range [{servo.min_angle}, {servo.max_angle}]")

# Check if base servo is configured
if servo.base_servo is None:
    print("Base servo not configured")
```

#### Issue: High temperature warnings

**Possible causes:**
- Excessive load
- Poor ventilation
- Continuous operation

**Solution:**
```python
# Reduce movement speed
servo.default_speed = 30  # Slower movement

# Add delays between movements
servo.move_to(90, duration=2.0, blocking=True)
time.sleep(1.0)  # Cool-down period

# Check load
health = servo.get_health_status()
if health['health']['current'] > 600:
    print("High current draw - check mechanical load")
```

#### Issue: Position errors

**Possible causes:**
- Calibration needed
- Mechanical obstruction
- Servo wear

**Solution:**
```python
# Recalibrate servo
from shared.servo_control import ServoCalibration

cal = ServoCalibration()
cal.calibrate_servo_interactive("my_servo", servo)
cal.apply_to_servo("my_servo", servo)

# Check for mechanical issues
servo.move_to(90, speed=10)  # Slow movement to detect obstruction
```

### Debug Mode

```python
# Enable verbose logging
import logging
from shared.utils import setup_logger

logger = setup_logger('servo_debug', level=logging.DEBUG)

# Monitor servo operations
servo.move_to(90)
health = servo.get_health_status()
logger.debug(f"Health: {health}")
```

### Performance Optimization

```python
# Reduce history size for memory-constrained systems
servo.movement_history = deque(maxlen=50)  # Instead of 100

# Reduce health check frequency
monitor = ServoHealthMonitor(update_interval=2.0)  # Instead of 1.0

# Disable features if not needed
# (Modify ServoEnhanced class to make features optional)
```

## 📚 API Reference

See [Servo Control README](../shared/servo_control/README.md) for complete API documentation.

## 🤝 Contributing

Contributions welcome! Please:
1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Submit pull request

## 📝 Version History

- **v1.0.0** - Initial release
  - Basic servo control
  - Health monitoring
  - Calibration system

---

*Last updated: 2024-01-15*
