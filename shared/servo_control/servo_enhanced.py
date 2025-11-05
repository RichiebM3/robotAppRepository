"""
Enhanced Servo Control Module

Provides advanced servo control with health monitoring, calibration,
and performance tracking capabilities.

Features:
    - Health monitoring (temperature, current, voltage)
    - Movement history and analytics
    - Calibration support (offset, scale, trim)
    - Error detection and logging
    - Performance metrics
    - Data export capabilities

Author: Robot App Repository
Version: 1.0.0
"""

import time
import json
from datetime import datetime
from collections import deque
from typing import Optional, Dict, List, Tuple
import threading


class ServoEnhanced:
    """
    Enhanced servo controller with health monitoring and calibration.
    
    This class wraps a basic servo controller and adds:
    - Real-time health monitoring
    - Movement history tracking
    - Calibration management
    - Performance metrics
    - Error detection and logging
    
    Attributes:
        channel (int): Servo channel number
        name (str): Human-readable servo name
        min_angle (float): Minimum safe angle
        max_angle (float): Maximum safe angle
        current_angle (float): Current servo angle
        target_angle (float): Target servo angle
        is_moving (bool): Whether servo is currently moving
        
    Example:
        >>> servo = ServoEnhanced(channel=0, name="leg_1_hip")
        >>> servo.move_to(90, duration=1.0)
        >>> health = servo.get_health_status()
        >>> print(f"Temperature: {health['health']['temperature']}°C")
    """
    
    def __init__(self,
                 channel: int,
                 name: str = None,
                 min_angle: float = 0,
                 max_angle: float = 180,
                 default_speed: float = 50,
                 base_servo=None):
        """
        Initialize enhanced servo controller.
        
        Args:
            channel: Servo channel number (0-15 typically)
            name: Human-readable name for the servo
            min_angle: Minimum safe angle in degrees
            max_angle: Maximum safe angle in degrees
            default_speed: Default movement speed in degrees/second
            base_servo: Optional underlying servo object for hardware control
        """
        self.channel = channel
        self.name = name or f"servo_{channel}"
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.default_speed = default_speed
        self.base_servo = base_servo
        
        # Current state
        self.current_angle = (min_angle + max_angle) / 2  # Start at center
        self.target_angle = self.current_angle
        self.is_moving = False
        self.last_move_time = time.time()
        
        # Health monitoring
        self.health_data = {
            'temperature': 0.0,      # Celsius
            'current': 0.0,          # mA
            'voltage': 0.0,          # V
            'error_count': 0,
            'warning_count': 0,
            'total_movements': 0,
            'total_distance': 0.0,   # Total degrees moved
        }
        
        # Movement history (limited to last 100 movements)
        self.movement_history = deque(maxlen=100)
        
        # Calibration data
        self.calibration = {
            'offset': 0.0,           # Angle offset in degrees
            'scale': 1.0,            # Scaling factor
            'trim': 0.0,             # Fine-tuning trim
            'last_calibrated': None
        }
        
        # Error/warning logs
        self.errors = deque(maxlen=100)
        self.warnings = deque(maxlen=100)
        
        # Thresholds for health monitoring
        self.thresholds = {
            'temp_warning': 60.0,    # °C
            'temp_critical': 75.0,   # °C
            'current_warning': 800.0,  # mA
            'current_critical': 1000.0,  # mA
            'position_error': 5.0    # degrees
        }
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Initialization time
        self.init_time = time.time()
        
        print(f"✅ ServoEnhanced initialized: {self.name} (channel {self.channel})")
    
    def move_to(self, 
                angle: float, 
                duration: float = None,
                speed: float = None,
                blocking: bool = False) -> bool:
        """
        Move servo to target angle with optional duration or speed control.
        
        Args:
            angle: Target angle in degrees
            duration: Time to complete movement in seconds (optional)
            speed: Movement speed in degrees/second (optional)
            blocking: If True, wait for movement to complete
            
        Returns:
            bool: True if movement initiated successfully
            
        Example:
            >>> servo.move_to(90, duration=2.0, blocking=True)
            >>> servo.move_to(45, speed=30)
        """
        with self.lock:
            # Validate angle
            if not self._validate_angle(angle):
                self._log_error(f"Invalid angle: {angle}° (range: {self.min_angle}-{self.max_angle})")
                return False
            
            # Apply calibration
            calibrated_angle = self._apply_calibration(angle)
            
            # Calculate movement parameters
            distance = abs(calibrated_angle - self.current_angle)
            
            # Determine actual duration and speed
            # FIXED: Preserve the original duration/speed parameters
            if duration is not None:
                # Duration specified: use it directly
                actual_duration = duration
                actual_speed = distance / duration if duration > 0 else self.default_speed
            elif speed is not None:
                # Speed specified: calculate duration from it
                actual_speed = speed
                actual_duration = distance / speed if speed > 0 else 0
            else:
                # Neither specified: use default speed
                actual_speed = self.default_speed
                actual_duration = distance / self.default_speed if self.default_speed > 0 else 0
            
            # Record movement (use actual_duration, not recalculated)
            movement_record = {
                'timestamp': datetime.now().isoformat(),
                'from_angle': self.current_angle,
                'to_angle': calibrated_angle,
                'distance': distance,
                'speed': actual_speed,
                'duration': actual_duration  # ✅ FIXED: Use preserved duration
            }
            self.movement_history.append(movement_record)
            
            # Update state
            self.target_angle = calibrated_angle
            self.is_moving = True
            self.last_move_time = time.time()
            
            # Update health data
            self.health_data['total_movements'] += 1
            self.health_data['total_distance'] += distance
            
            # Execute movement (if base servo is available)
            if self.base_servo:
                try:
                    self.base_servo.setServoAngle(self.channel, calibrated_angle)
                except Exception as e:
                    self._log_error(f"Servo movement failed: {e}")
                    return False
            
            # Handle movement completion
            if blocking:
                # Wait for movement to complete
                time.sleep(actual_duration)  # ✅ FIXED: Use actual_duration
                self.current_angle = calibrated_angle
                self.is_moving = False
            else:
                # Non-blocking: update immediately
                # In real implementation with hardware, this would be handled by feedback
                self.current_angle = calibrated_angle
                self.is_moving = False
            
            return True
    
    def move_smooth(self,
                    angle: float,
                    duration: float = 1.0,
                    interpolation: str = 'linear') -> bool:
        """
        Move servo smoothly to target angle with interpolation.
        
        Args:
            angle: Target angle in degrees
            duration: Time to complete movement in seconds
            interpolation: Interpolation method ('linear', 'ease_in', 'ease_out', 'ease_in_out')
            
        Returns:
            bool: True if movement initiated successfully
            
        Example:
            >>> servo.move_smooth(90, duration=2.0, interpolation='ease_in_out')
        """
        # For now, just use move_to with duration
        # In a real implementation, this would use interpolation for smoother movement
        return self.move_to(angle, duration=duration, blocking=False)
    
    def _validate_angle(self, angle: float) -> bool:
        """
        Validate that angle is within safe range.
        
        Args:
            angle: Angle to validate
            
        Returns:
            bool: True if angle is valid
        """
        return self.min_angle <= angle <= self.max_angle
    
    def _apply_calibration(self, angle: float) -> float:
        """
        Apply calibration parameters to angle.
        
        Args:
            angle: Raw angle
            
        Returns:
            float: Calibrated angle
        """
        # Apply scale, offset, and trim
        calibrated = (angle * self.calibration['scale']) + \
                     self.calibration['offset'] + \
                     self.calibration['trim']
        
        # Ensure calibrated angle is still within bounds
        return max(self.min_angle, min(self.max_angle, calibrated))
    
    def set_calibration(self,
                       offset: float = 0.0,
                       scale: float = 1.0,
                       trim: float = 0.0) -> None:
        """
        Set calibration parameters for the servo.
        
        Args:
            offset: Angle offset in degrees
            scale: Scaling factor (1.0 = no scaling)
            trim: Fine-tuning trim in degrees
            
        Example:
            >>> servo.set_calibration(offset=5.0, scale=1.0, trim=0.5)
        """
        with self.lock:
            self.calibration['offset'] = offset
            self.calibration['scale'] = scale
            self.calibration['trim'] = trim
            self.calibration['last_calibrated'] = datetime.now().isoformat()
            
            print(f"✅ Calibration updated for {self.name}")
    
    def update_health_metrics(self,
                             temperature: float = None,
                             current: float = None,
                             voltage: float = None) -> None:
        """
        Update health monitoring metrics.
        
        Args:
            temperature: Temperature in Celsius
            current: Current draw in mA
            voltage: Voltage in V
            
        Example:
            >>> servo.update_health_metrics(temperature=45.5, current=350.0, voltage=5.0)
        """
        with self.lock:
            if temperature is not None:
                self.health_data['temperature'] = temperature
                
                # Check temperature thresholds
                if temperature >= self.thresholds['temp_critical']:
                    self._log_error(f"CRITICAL: Temperature {temperature}°C")
                elif temperature >= self.thresholds['temp_warning']:
                    self._log_warning(f"High temperature: {temperature}°C")
            
            if current is not None:
                self.health_data['current'] = current
                
                # Check current thresholds
                if current >= self.thresholds['current_critical']:
                    self._log_error(f"CRITICAL: Current {current}mA")
                elif current >= self.thresholds['current_warning']:
                    self._log_warning(f"High current: {current}mA")
            
            if voltage is not None:
                self.health_data['voltage'] = voltage
    
    def get_health_status(self) -> Dict:
        """
        Get comprehensive health status.
        
        Returns:
            dict: Health status including all metrics, warnings, and errors
            
        Example:
            >>> health = servo.get_health_status()
            >>> print(f"Status: {health['status']}")
            >>> print(f"Temperature: {health['health']['temperature']}°C")
        """
        with self.lock:
            # Determine overall status
            if self.health_data['error_count'] > 0:
                status = 'ERROR'
            elif (self.health_data['temperature'] >= self.thresholds['temp_critical'] or
                  self.health_data['current'] >= self.thresholds['current_critical']):
                status = 'CRITICAL'
            elif (self.health_data['temperature'] >= self.thresholds['temp_warning'] or
                  self.health_data['current'] >= self.thresholds['current_warning']):
                status = 'WARNING'
            else:
                status = 'HEALTHY'
            
            # Calculate uptime
            uptime = time.time() - self.init_time
            
            return {
                'servo_name': self.name,
                'channel': self.channel,
                'current_angle': self.current_angle,
                'target_angle': self.target_angle,
                'is_moving': self.is_moving,
                'health': {
                    **self.health_data,
                    'uptime': uptime
                },
                'status': status,
                'warnings': list(self.warnings),
                'errors': list(self.errors),
                'last_movement': self.movement_history[-1] if self.movement_history else None
            }
    
    def get_movement_stats(self) -> Dict:
        """
        Get movement statistics.
        
        Returns:
            dict: Movement statistics including total movements, distance, etc.
            
        Example:
            >>> stats = servo.get_movement_stats()
            >>> print(f"Total movements: {stats['total_movements']}")
            >>> print(f"Average speed: {stats['average_speed']}°/s")
        """
        with self.lock:
            total_movements = self.health_data['total_movements']
            total_distance = self.health_data['total_distance']
            
            # Calculate average speed
            if self.movement_history:
                speeds = [m['speed'] for m in self.movement_history if m['speed'] > 0]
                avg_speed = sum(speeds) / len(speeds) if speeds else 0
            else:
                avg_speed = 0
            
            return {
                'total_movements': total_movements,
                'total_distance': total_distance,
                'average_speed': avg_speed,
                'last_movement': self.movement_history[-1] if self.movement_history else None,
                'uptime': time.time() - self.init_time
            }
    
    def reset_health_counters(self) -> None:
        """
        Reset health error and warning counters.
        
        Example:
            >>> servo.reset_health_counters()
        """
        with self.lock:
            self.health_data['error_count'] = 0
            self.health_data['warning_count'] = 0
            self.errors.clear()
            self.warnings.clear()
            
            print(f"✅ Health counters reset for {self.name}")
    
    def export_data(self, filename: str) -> bool:
        """
        Export servo data to JSON file.
        
        Args:
            filename: Output filename
            
        Returns:
            bool: True if export successful
            
        Example:
            >>> servo.export_data("servo_data.json")
        """
        try:
            data = {
                'servo_info': {
                    'name': self.name,
                    'channel': self.channel,
                    'min_angle': self.min_angle,
                    'max_angle': self.max_angle,
                    'default_speed': self.default_speed
                },
                'current_state': {
                    'current_angle': self.current_angle,
                    'target_angle': self.target_angle,
                    'is_moving': self.is_moving
                },
                'health_data': self.health_data.copy(),
                'calibration': self.calibration.copy(),
                'movement_history': list(self.movement_history),
                'errors': list(self.errors),
                'warnings': list(self.warnings),
                'export_timestamp': datetime.now().isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Data exported to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def _log_error(self, message: str) -> None:
        """Log an error message."""
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'message': message
        }
        self.errors.append(error_record)
        self.health_data['error_count'] += 1
        print(f"❌ ERROR [{self.name}]: {message}")
    
    def _log_warning(self, message: str) -> None:
        """Log a warning message."""
        warning_record = {
            'timestamp': datetime.now().isoformat(),
            'message': message
        }
        self.warnings.append(warning_record)
        self.health_data['warning_count'] += 1
        print(f"⚠️  WARNING [{self.name}]: {message}")
    
    def __repr__(self) -> str:
        """String representation of servo."""
        return (f"ServoEnhanced(name='{self.name}', channel={self.channel}, "
                f"angle={self.current_angle:.1f}°, status='{self._get_status()}')")
    
    def _get_status(self) -> str:
        """Get simple status string."""
        health = self.get_health_status()
        return health['status']


# ============================================================
# Module Testing
# ============================================================

def _test_servo_enhanced():
    """Test ServoEnhanced functionality."""
    print("=" * 60)
    print("ServoEnhanced - Test Mode")
    print("=" * 60)
    
    # Create test servo
    servo = ServoEnhanced(
        channel=0,
        name="test_servo",
        min_angle=0,
        max_angle=180,
        default_speed=50
    )
    
    print("\n🔧 Testing movements...")
    
    # Test basic movement
    servo.move_to(45, duration=0.5)
    time.sleep(0.6)
    
    servo.move_to(135, duration=0.5)
    time.sleep(0.6)
    
    servo.move_to(90, duration=0.5)
    time.sleep(0.6)
    
    print("\n🏥 Simulating health data...")
    
    # Update health metrics
    servo.update_health_metrics(
        temperature=45.5,
        current=350.0,
        voltage=5.0
    )
    
    # Get health status
    print("\n📊 Health Status:")
    health = servo.get_health_status()
    print(json.dumps(health, indent=2))
    
    # Get movement stats
    print("\n📈 Movement Statistics:")
    stats = servo.get_movement_stats()
    print(json.dumps(stats, indent=2))
    
    # Test calibration
    print("\n🎯 Testing calibration...")
    servo.set_calibration(offset=5.0, scale=1.0, trim=0.5)
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    _test_servo_enhanced()
