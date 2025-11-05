"""
Sensors Module

Sensor interfaces and data processing utilities for various robot sensors.

Planned sensors:
    - Ultrasonic distance sensors
    - IMU (Inertial Measurement Unit)
    - Camera/Vision sensors
    - Touch/Pressure sensors
    - Temperature sensors
    - Current sensors

Usage:
    from shared.sensors import UltrasonicSensor
    
    sensor = UltrasonicSensor(trigger_pin=23, echo_pin=24)
    distance = sensor.read_distance()
"""

__version__ = '1.0.0'

# Placeholder for future sensor implementations
__all__ = []

# Module-level configuration
DEFAULT_SENSOR_CONFIG = {
    'update_rate': 10,  # Hz
    'timeout': 1.0,     # seconds
    'retry_count': 3,
    'filter_enabled': True
}

def get_default_config():
    """Return default sensor configuration"""
    return DEFAULT_SENSOR_CONFIG.copy()

# TODO: Import sensor classes as they are implemented
# from .ultrasonic import UltrasonicSensor
# from .imu import IMUSensor
# from .camera import CameraSensor

print("📡 Sensors module loaded (placeholder)")
