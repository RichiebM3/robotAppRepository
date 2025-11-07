# 🕷️ SpiderPi - Enhanced Servo Control System

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![Tests](https://img.shields.io/badge/tests-25%20passed-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-red.svg)

**Advanced servo control system for Freenove hexapod robot with comprehensive health monitoring, calibration, and analytics.**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Testing](#-testing) • [Contributing](#-contributing)

</div>

---

## 📖 **Table of Contents**

- [Overview](#overview)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Usage Examples](#-usage-examples)
- [Health Monitoring](#-health-monitoring)
- [Calibration](#-calibration)
- [Testing](#-testing)
- [API Reference](#-api-reference)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## **Overview**

SpiderPi is an enhanced servo control system designed for the Freenove hexapod robot platform. It extends basic servo functionality with enterprise-grade features including real-time health monitoring, precise calibration, movement analytics, and comprehensive error handling.

### **Why SpiderPi?**

- 🎯 **Precision Control**: Accurate angle positioning with duration and speed control
- 🏥 **Health Monitoring**: Real-time tracking of temperature, current, and voltage
- 📊 **Analytics**: Complete movement history and performance statistics
- 🔧 **Calibration**: Per-servo offset, scale, and trim adjustments
- ⚡ **Performance**: Thread-safe, non-blocking operations
- 🧪 **Tested**: 100% test coverage with 25 comprehensive tests

---

## ✨ **Features**

### **Core Functionality**
- ✅ Enhanced servo control with precise angle positioning
- ✅ Duration-based movement (smooth transitions)
- ✅ Speed control (degrees per second)
- ✅ Blocking and non-blocking operation modes
- ✅ Thread-safe multi-servo coordination

### **Health & Monitoring**
- 🏥 Real-time temperature monitoring
- ⚡ Current consumption tracking
- 🔋 Voltage level monitoring
- ⚠️ Automatic warning and critical alerts
- 📈 Health status reporting

### **Analytics & History**
- 📊 Complete movement history
- 📉 Movement statistics and patterns
- 🎯 Position tracking
- ⏱️ Timing analysis
- 💾 JSON data export

### **Calibration System**
- 🔧 Angle offset adjustment
- 📏 Scaling factor configuration
- ⚙️ Fine-tuning trim settings
- 💾 Calibration profile save/load
- 🎯 Per-servo customization

### **Error Handling**
- 🚨 Automatic error detection
- ⚠️ Warning system (temperature, current)
- 🔴 Critical alert system
- 📝 Error logging and tracking
- 🛡️ Safe failure modes

---

## 📦 **Installation**

### **Prerequisites**

- Python 3.7 or higher
- Raspberry Pi (for hardware control)
- Freenove Hexapod Robot Kit (optional for full functionality)

### **Clone Repository**

```bash
git clone https://github.com/RichiebM3/robotAppRepository.git
cd robotAppRepository
```

### **Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Verify Installation**

```bash
python tests/test_servo_enhanced.py
```

You should see:
```
✅ All 25 tests passed!
```

---

## 🚀 **Quick Start**

### **Basic Usage**

```python
from shared.servo_control.servo_enhanced import ServoEnhanced

# Create a servo instance
servo = ServoEnhanced(channel=0, name="leg_1_hip")

# Move to 90 degrees over 1 second
servo.move_to(90, duration=1.0, blocking=True)

# Check current position
print(f"Current angle: {servo.get_current_angle()}°")

# Get health status
health = servo.get_health_status()
print(f"Status: {health['status']}")
print(f"Temperature: {health['health']['temperature']}°C")
```

### **Advanced Example**

```python
# Create servo with calibration
servo = ServoEnhanced(
    channel=0, 
    name="leg_1_hip",
    min_angle=0,
    max_angle=180
)

# Set calibration parameters
servo.set_calibration(offset=5.0, scale=1.0, trim=0.5)

# Update health metrics
servo.update_health_metrics(
    temperature=45.5,
    current=350.0,
    voltage=5.0
)

# Move with speed control
servo.move_to(135, speed=45.0, blocking=False)

# Get movement statistics
stats = servo.get_movement_stats()
print(f"Total movements: {stats['total_movements']}")
print(f"Average duration: {stats['avg_duration']:.2f}s")

# Export data
servo.export_data("servo_data.json")
```

---

## 📁 **Project Structure**

```
SpiderPi/
│
├── shared/                          # Shared modules
│   ├── servo_control/              # Servo control system
│   │   ├── __init__.py
│   │   ├── servo_enhanced.py       # Enhanced servo controller ⭐
│   │   └── servo_calibration.py    # Calibration utilities
│   │
│   ├── sensors/                    # Sensor interfaces
│   ├── communication/              # Communication protocols
│   └── utils/                      # Utility functions
│
├── tests/                          # Test suite
│   ├── __init__.py
│   └── test_servo_enhanced.py      # Comprehensive tests (25 tests) ✅
│
├── data/                           # Data storage
│   ├── calibrations/               # Calibration profiles
│   └── logs/                       # Log files
│
├── examples/                       # Usage examples
│   ├── basic_movement.py
│   ├── health_monitoring.py
│   └── multi_servo_demo.py
│
├── docs/                           # Documentation
│   ├── API.md                      # API reference
│   ├── CALIBRATION.md             # Calibration guide
│   └── TROUBLESHOOTING.md         # Common issues
│
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── LICENSE                         # MIT License
└── .gitignore                     # Git ignore rules
```

---

## 💡 **Usage Examples**

### **Example 1: Single Servo Control**

```python
from shared.servo_control.servo_enhanced import ServoEnhanced
import time

# Initialize servo
servo = ServoEnhanced(channel=0, name="test_servo")

# Smooth movement sequence
angles = [0, 45, 90, 135, 180, 90]
for angle in angles:
    servo.move_to(angle, duration=0.5, blocking=True)
    time.sleep(0.1)

# Get statistics
stats = servo.get_movement_stats()
print(f"Completed {stats['total_movements']} movements")
```

### **Example 2: Health Monitoring**

```python
from shared.servo_control.servo_enhanced import ServoEnhanced
import time

servo = ServoEnhanced(channel=0, name="monitored_servo")

# Simulate operation with monitoring
for i in range(10):
    # Move servo
    servo.move_to(90 + (i * 10), duration=0.5)
    
    # Update health metrics (in real scenario, read from sensors)
    servo.update_health_metrics(
        temperature=40 + i,
        current=300 + (i * 10),
        voltage=5.0
    )
    
    # Check health
    health = servo.get_health_status()
    print(f"Cycle {i}: {health['status']} - Temp: {health['health']['temperature']}°C")
    
    time.sleep(0.5)
```

### **Example 3: Multi-Servo Coordination**

```python
from shared.servo_control.servo_enhanced import ServoEnhanced
import threading

# Create multiple servos
servos = [
    ServoEnhanced(channel=i, name=f"servo_{i}")
    for i in range(6)
]

# Coordinated movement (non-blocking)
def move_all_servos(target_angle):
    threads = []
    for servo in servos:
        thread = threading.Thread(
            target=servo.move_to,
            args=(target_angle,),
            kwargs={'duration': 1.0, 'blocking': True}
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all to complete
    for thread in threads:
        thread.join()

# Execute coordinated movement
move_all_servos(90)
print("All servos moved to 90°")
```

### **Example 4: Calibration**

```python
from shared.servo_control.servo_enhanced import ServoEnhanced

servo = ServoEnhanced(channel=0, name="calibrated_servo")

# Set calibration (e.g., servo is 5° off)
servo.set_calibration(
    offset=5.0,    # Compensate for 5° offset
    scale=1.0,     # No scaling needed
    trim=0.0       # No fine-tuning needed
)

# Move to 90° (actually moves to 95° to compensate)
servo.move_to(90)

# Get calibration info
cal = servo.get_calibration()
print(f"Calibration: {cal}")
```

### **Example 5: Data Export & Analysis**

```python
from shared.servo_control.servo_enhanced import ServoEnhanced
import json

servo = ServoEnhanced(channel=0, name="data_servo")

# Perform movements
for angle in range(0, 181, 30):
    servo.move_to(angle, duration=0.5, blocking=True)
    servo.update_health_metrics(
        temperature=40 + (angle / 10),
        current=300 + angle,
        voltage=5.0
    )

# Export all data
servo.export_data("servo_analysis.json")

# Load and analyze
with open("servo_analysis.json", 'r') as f:
    data = json.load(f)
    
print(f"Servo: {data['servo_info']['name']}")
print(f"Total movements: {len(data['movement_history'])}")
print(f"Health status: {data['health_status']['status']}")
```

---

## 🏥 **Health Monitoring**

### **Health Metrics**

The system tracks three key health metrics:

| Metric | Normal Range | Warning | Critical |
|--------|-------------|---------|----------|
| **Temperature** | < 60°C | 60-80°C | > 80°C |
| **Current** | < 500mA | 500-800mA | > 800mA |
| **Voltage** | 4.5-5.5V | 4.0-4.5V or 5.5-6.0V | < 4.0V or > 6.0V |

### **Health Status Levels**

- 🟢 **HEALTHY**: All metrics within normal range
- 🟡 **WARNING**: One or more metrics in warning range
- 🔴 **CRITICAL**: One or more metrics in critical range

### **Usage**

```python
# Update health metrics
servo.update_health_metrics(
    temperature=45.5,  # °C
    current=350.0,     # mA
    voltage=5.0        # V
)

# Get comprehensive health report
health = servo.get_health_status()

print(f"Status: {health['status']}")
print(f"Temperature: {health['health']['temperature']}°C")
print(f"Current: {health['health']['current']}mA")
print(f"Voltage: {health['health']['voltage']}V")
print(f"Warnings: {health['warnings']}")
print(f"Critical Issues: {health['critical_issues']}")
```

---

## 🔧 **Calibration**

### **Why Calibrate?**

Servo motors may have slight variations due to:
- Manufacturing tolerances
- Mechanical wear
- Mounting position
- Load differences

### **Calibration Parameters**

1. **Offset**: Compensates for angular misalignment
   - Example: Servo reads 5° when it should be 0°
   - Set `offset=5.0` to compensate

2. **Scale**: Adjusts for range compression/expansion
   - Example: Servo only moves 170° instead of 180°
   - Set `scale=180/170` to compensate

3. **Trim**: Fine-tuning adjustment
   - Small corrections after offset and scale
   - Typically ±2°

### **Calibration Process**

```python
# Step 1: Create servo
servo = ServoEnhanced(channel=0, name="leg_1_hip")

# Step 2: Test without calibration
servo.move_to(0)    # Observe actual position
servo.move_to(90)   # Observe actual position
servo.move_to(180)  # Observe actual position

# Step 3: Calculate corrections
# If 0° shows as 5°, offset = -5
# If 90° shows as 88°, adjust scale or trim

# Step 4: Apply calibration
servo.set_calibration(
    offset=-5.0,
    scale=1.0,
    trim=0.0
)

# Step 5: Test again
servo.move_to(0)    # Should now be accurate
servo.move_to(90)   # Should now be accurate
servo.move_to(180)  # Should now be accurate

# Step 6: Save calibration
cal_data = servo.get_calibration()
# Save to file for future use
```

---

## 🧪 **Testing**

### **Run All Tests**

```bash
python tests/test_servo_enhanced.py
```

### **Test Coverage**

The test suite includes **25 comprehensive tests**:

#### **Basic Functionality** (5 tests)
- ✅ Servo initialization
- ✅ Basic movement
- ✅ Angle limits enforcement
- ✅ Position tracking
- ✅ Reset functionality

#### **Movement Control** (5 tests)
- ✅ Duration-based movement
- ✅ Speed-based movement
- ✅ Blocking operations
- ✅ Non-blocking operations
- ✅ Movement history tracking

#### **Health Monitoring** (5 tests)
- ✅ Health metric updates
- ✅ Warning detection
- ✅ Critical alert detection
- ✅ Health status reporting
- ✅ Multi-metric monitoring

#### **Calibration** (5 tests)
- ✅ Offset calibration
- ✅ Scale calibration
- ✅ Trim calibration
- ✅ Combined calibration
- ✅ Calibration persistence

#### **Advanced Features** (5 tests)
- ✅ Movement statistics
- ✅ Data export
- ✅ Thread safety
- ✅ Error handling
- ✅ Edge cases

### **Expected Output**

```
Running SpiderPi Enhanced Servo Tests...
==========================================

Test 1: Basic Servo Initialization... ✅ PASSED
Test 2: Basic Movement... ✅ PASSED
Test 3: Angle Limits... ✅ PASSED
...
Test 25: Edge Cases... ✅ PASSED

==========================================
✅ All 25 tests passed!
Total time: 2.34 seconds
```

---

## 📚 **API Reference**

### **ServoEnhanced Class**

#### **Constructor**

```python
ServoEnhanced(
    channel: int,
    name: str = None,
    min_angle: float = 0,
    max_angle: float = 180,
    default_duration: float = 0.5
)
```

**Parameters:**
- `channel`: Servo channel number (0-15)
- `name`: Optional servo identifier
- `min_angle`: Minimum allowed angle (default: 0)
- `max_angle`: Maximum allowed angle (default: 180)
- `default_duration`: Default movement duration in seconds (default: 0.5)

#### **Movement Methods**

```python
move_to(angle: float, duration: float = None, speed: float = None, blocking: bool = False) -> bool
```
Move servo to target angle.

```python
get_current_angle() -> float
```
Get current servo angle.

```python
reset() -> None
```
Reset servo to default position (90°).

#### **Health Methods**

```python
update_health_metrics(temperature: float = None, current: float = None, voltage: float = None) -> None
```
Update health monitoring metrics.

```python
get_health_status() -> dict
```
Get comprehensive health status report.

#### **Calibration Methods**

```python
set_calibration(offset: float = 0, scale: float = 1.0, trim: float = 0) -> None
```
Set calibration parameters.

```python
get_calibration() -> dict
```
Get current calibration settings.

#### **Analytics Methods**

```python
get_movement_history() -> list
```
Get complete movement history.

```python
get_movement_stats() -> dict
```
Get movement statistics.

```python
export_data(filename: str) -> bool
```
Export all data to JSON file.

---

## 🗺️ **Roadmap**

### **Version 1.0** (Current)
- ✅ Enhanced servo control
- ✅ Health monitoring
- ✅ Calibration system
- ✅ Movement analytics
- ✅ Comprehensive testing

### **Version 1.1** (Planned)
- 🔲 Hexapod integration class
- 🔲 Coordinated leg movements
- 🔲 Gait pattern library
- 🔲 Real-time monitoring dashboard

### **Version 1.2** (Future)
- 🔲 Web-based control interface
- 🔲 Mobile app integration
- 🔲 Machine learning movement optimization
- 🔲 Computer vision integration

### **Version 2.0** (Vision)
- 🔲 Multi-robot coordination
- 🔲 Autonomous navigation
- 🔲 Advanced AI behaviors
- 🔲 Cloud data analytics

---

## 🤝 **Contributing**

Contributions are welcome! Here's how you can help:

### **Ways to Contribute**

1. 🐛 **Report Bugs**: Open an issue with details
2. 💡 **Suggest Features**: Share your ideas
3. 📝 **Improve Documentation**: Fix typos, add examples
4. 🔧 **Submit Code**: Create pull requests

### **Development Setup**

```bash
# Fork and clone the repository
git clone https://github.com/RichiebM3/robotAppRepository
cd robotAppRepository

```

### **Code Standards**

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation as needed

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 SpiderPi Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 **Acknowledgments**

- **Freenove** - For the excellent hexapod robot platform
- **Raspberry Pi Foundation** - For the amazing Raspberry Pi
- **Python Community** - For the incredible ecosystem
- **Contributors** - Azure 
---

## 📧 **Contact & Support**

- **Issues**: [GitHub Issues](https://github.com/RichiebM3/robotAppRepository/issues)
- **Discussions**: [GitHub Discussions](https://github.com/RichiebM3/robotAppRepository/discussions)
- **Email**: Rbruce85@uw.edu

---

## 🌟 **Show Your Support**

If you find this project useful, please consider:

- ⭐ **Starring** the repository
- 🐛 **Reporting** bugs
- 💡 **Suggesting** features
- 📢 **Sharing** with others
- 🤝 **Contributing** code

---

## 📊 **Project Stats**

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/SpiderPi?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/SpiderPi?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/YOUR_USERNAME/SpiderPi?style=social)

---

<div align="center">

**Built with ❤️ for robotics enthusiasts**

[⬆ Back to Top](#️-spiderpi---enhanced-servo-control-system)

</div>
