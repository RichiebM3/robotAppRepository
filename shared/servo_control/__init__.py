"""
Servo Control Module

Enhanced servo control system with health monitoring, calibration,
and performance tracking capabilities.

Classes:
    - ServoEnhanced: Main enhanced servo class with health monitoring
    - ServoCalibration: Calibration utilities for servo tuning
    - ServoHealthMonitor: Standalone health monitoring system

Usage:
    from shared.servo_control import ServoEnhanced
    
    servo = ServoEnhanced(channel=0, name="leg_1_hip")
    servo.move_to(90, duration=1.0)
    health = servo.get_health_status()
"""

__version__ = '1.0.0'

# Import main classes (will be available after we create the files)
try:
    from .servo_enhanced import ServoEnhanced
    from .servo_calibration import ServoCalibration
    from .servo_health_monitor import ServoHealthMonitor
    
    __all__ = [
        'ServoEnhanced',
        'ServoCalibration', 
        'ServoHealthMonitor'
    ]
except ImportError as e:
    # Graceful handling if modules aren't ready yet
    print(f"Warning: Some servo_control modules not yet available: {e}")
    __all__ = []

# Module-level constants
DEFAULT_SERVO_CONFIG = {
    'min_angle': 0,
    'max_angle': 180,
    'default_speed': 50,  # degrees per second
    'health_check_interval': 10,  # seconds
    'temperature_warning': 60,  # Celsius
    'temperature_critical': 75,  # Celsius
    'current_warning': 800,  # mA
    'current_critical': 1000,  # mA
}

def get_default_config():
    """Return default servo configuration"""
    return DEFAULT_SERVO_CONFIG.copy()
