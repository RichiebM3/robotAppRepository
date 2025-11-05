"""
Servo Health Monitoring System

Centralized health monitoring for multiple servos with:
- Real-time health tracking
- Alert system for warnings/errors
- Performance analytics
- Health history logging
- Dashboard generation

Features:
    - Monitor multiple servos simultaneously
    - Configurable alert thresholds
    - Health trend analysis
    - Export health reports
    - Real-time dashboard (console-based)

Author: Robot App Repository Team
Version: 1.0.0
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict, deque
from pathlib import Path
import threading


class ServoHealthMonitor:
    """
    Centralized health monitoring system for multiple servos.
    
    Monitors temperature, current, position errors, and other metrics
    across multiple servos. Provides alerts and health reports.
    
    Attributes:
        servos (dict): Dictionary of monitored servos
        health_history (dict): Historical health data
        alerts (deque): Recent alerts
    """
    
    def __init__(self, 
                 update_interval: float = 1.0,
                 history_size: int = 1000,
                 data_dir: str = "data/health"):
        """
        Initialize health monitoring system.
        
        Args:
            update_interval: Seconds between health checks
            history_size: Number of historical records to keep
            data_dir: Directory for health data storage
        """
        self.servos = {}
        self.update_interval = update_interval
        self.history_size = history_size
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Health history for each servo
        self.health_history = defaultdict(lambda: deque(maxlen=history_size))
        
        # Alerts and warnings
        self.alerts = deque(maxlen=100)
        
        # Statistics
        self.stats = {
            'total_alerts': 0,
            'critical_alerts': 0,
            'warnings': 0,
            'monitoring_start': datetime.now(),
            'uptime': 0
        }
        
        # Monitoring thread
        self.monitoring = False
        self.monitor_thread = None
        
        # Thresholds (can be customized per servo)
        self.default_thresholds = {
            'temp_warning': 60.0,
            'temp_critical': 75.0,
            'current_warning': 800.0,
            'current_critical': 1000.0,
            'position_error_warning': 5.0,
            'position_error_critical': 10.0
        }
        
        print("✅ ServoHealthMonitor initialized")
        print(f"📁 Data directory: {self.data_dir}")
    
    def register_servo(self, servo_obj, thresholds: Dict = None):
        """
        Register a servo for monitoring.
        
        Args:
            servo_obj: Servo object to monitor (must have get_health_status method)
            thresholds: Custom thresholds for this servo (optional)
        """
        if not hasattr(servo_obj, 'get_health_status'):
            print(f"⚠️  Servo doesn't support health monitoring")
            return False
        
        servo_name = getattr(servo_obj, 'name', f'servo_{len(self.servos)}')
        
        self.servos[servo_name] = {
            'object': servo_obj,
            'thresholds': thresholds or self.default_thresholds.copy(),
            'registered_at': datetime.now(),
            'last_check': None,
            'status': 'UNKNOWN'
        }
        
        print(f"✅ Registered servo for monitoring: {servo_name}")
        return True
    
    def unregister_servo(self, servo_name: str):
        """Remove servo from monitoring."""
        if servo_name in self.servos:
            del self.servos[servo_name]
            print(f"✅ Unregistered servo: {servo_name}")
            return True
        return False
    
    def start_monitoring(self):
        """Start continuous health monitoring in background thread."""
        if self.monitoring:
            print("⚠️  Monitoring already running")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        print("✅ Health monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous health monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        
        print("✅ Health monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop (runs in background thread)."""
        while self.monitoring:
            self.check_all_servos()
            time.sleep(self.update_interval)
    
    def check_all_servos(self):
        """Check health of all registered servos."""
        for servo_name, servo_info in self.servos.items():
            self.check_servo(servo_name)
    
    def check_servo(self, servo_name: str) -> Dict:
        """
        Check health of specific servo.
        
        Args:
            servo_name: Name of servo to check
            
        Returns:
            dict: Health status
        """
        if servo_name not in self.servos:
            return None
        
        servo_info = self.servos[servo_name]
        servo_obj = servo_info['object']
        thresholds = servo_info['thresholds']
        
        try:
            # Get health status from servo
            health = servo_obj.get_health_status()
            
            # Record in history
            health_record = {
                'timestamp': datetime.now().isoformat(),
                'temperature': health['health']['temperature'],
                'current': health['health']['current'],
                'voltage': health['health']['voltage'],
                'angle': health['current_angle'],
                'status': health['status']
            }
            
            self.health_history[servo_name].append(health_record)
            
            # Check thresholds and generate alerts
            self._check_thresholds(servo_name, health, thresholds)
            
            # Update servo info
            servo_info['last_check'] = datetime.now()
            servo_info['status'] = health['status']
            
            return health
        
        except Exception as e:
            self._create_alert(servo_name, 'ERROR', f"Health check failed: {e}")
            return None
    
    def _check_thresholds(self, servo_name: str, health: Dict, thresholds: Dict):
        """Check if health metrics exceed thresholds."""
        temp = health['health']['temperature']
        current = health['health']['current']
        
        # Temperature checks
        if temp >= thresholds['temp_critical']:
            self._create_alert(
                servo_name, 
                'CRITICAL', 
                f"Temperature critical: {temp}°C (threshold: {thresholds['temp_critical']}°C)"
            )
        elif temp >= thresholds['temp_warning']:
            self._create_alert(
                servo_name,
                'WARNING',
                f"Temperature high: {temp}°C (threshold: {thresholds['temp_warning']}°C)"
            )
        
        # Current checks
        if current >= thresholds['current_critical']:
            self._create_alert(
                servo_name,
                'CRITICAL',
                f"Current critical: {current}mA (threshold: {thresholds['current_critical']}mA)"
            )
        elif current >= thresholds['current_warning']:
            self._create_alert(
                servo_name,
                'WARNING',
                f"Current high: {current}mA (threshold: {thresholds['current_warning']}mA)"
            )
    
    def _create_alert(self, servo_name: str, level: str, message: str):
        """Create and log an alert."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'servo': servo_name,
            'level': level,
            'message': message
        }
        
        self.alerts.append(alert)
        
        # Update statistics
        self.stats['total_alerts'] += 1
        if level == 'CRITICAL':
            self.stats['critical_alerts'] += 1
        elif level == 'WARNING':
            self.stats['warnings'] += 1
        
        # Print alert
        icon = '🔴' if level == 'CRITICAL' else '⚠️' if level == 'WARNING' else 'ℹ️'
        print(f"{icon} [{level}] {servo_name}: {message}")
    
    def get_servo_health(self, servo_name: str) -> Optional[Dict]:
        """Get current health status for specific servo."""
        if servo_name not in self.servos:
            return None
        
        return self.check_servo(servo_name)
    
    def get_all_health(self) -> Dict:
        """Get health status for all servos."""
        health_data = {}
        
        for servo_name in self.servos:
            health_data[servo_name] = self.check_servo(servo_name)
        
        return health_data
    
    def get_health_summary(self) -> Dict:
        """Get summary of overall system health."""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_servos': len(self.servos),
            'servos_by_status': defaultdict(int),
            'recent_alerts': list(self.alerts)[-10:],
            'statistics': self.stats.copy()
        }
        
        # Count servos by status
        for servo_info in self.servos.values():
            status = servo_info.get('status', 'UNKNOWN')
            summary['servos_by_status'][status] += 1
        
        # Calculate uptime
        summary['statistics']['uptime'] = (
            datetime.now() - self.stats['monitoring_start']
        ).total_seconds()
        
        return summary
    
    def get_health_trends(self, servo_name: str, 
                         metric: str = 'temperature',
                         duration: int = 60) -> List[Dict]:
        """
        Get health trends for specific metric.
        
        Args:
            servo_name: Name of servo
            metric: Metric to analyze ('temperature', 'current', 'voltage')
            duration: Duration in seconds to analyze
            
        Returns:
            list: Historical data points
        """
        if servo_name not in self.health_history:
            return []
        
        cutoff_time = datetime.now() - timedelta(seconds=duration)
        
        trends = []
        for record in self.health_history[servo_name]:
            record_time = datetime.fromisoformat(record['timestamp'])
            if record_time >= cutoff_time:
                trends.append({
                    'timestamp': record['timestamp'],
                    'value': record.get(metric, 0)
                })
        
        return trends
    
    def generate_dashboard(self) -> str:
        """Generate console-based health dashboard."""
        lines = []
        
        lines.append("=" * 80)
        lines.append("🏥 SERVO HEALTH MONITORING DASHBOARD")
        lines.append("=" * 80)
        lines.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Monitoring: {len(self.servos)} servos")
        lines.append("")
        
        # Summary statistics
        summary = self.get_health_summary()
        lines.append("📊 SYSTEM STATUS:")
        for status, count in summary['servos_by_status'].items():
            icon = {'HEALTHY': '✅', 'WARNING': '⚠️', 'CRITICAL': '🔴', 'ERROR': '❌'}.get(status, '❓')
            lines.append(f"  {icon} {status}: {count}")
        
        lines.append("")
        lines.append(f"📈 STATISTICS:")
        lines.append(f"  Total Alerts: {self.stats['total_alerts']}")
        lines.append(f"  Critical: {self.stats['critical_alerts']}")
        lines.append(f"  Warnings: {self.stats['warnings']}")
        lines.append(f"  Uptime: {summary['statistics']['uptime']:.1f}s")
        
        lines.append("")
        lines.append("🤖 SERVO DETAILS:")
        lines.append("-" * 80)
        
        # Individual servo status
        for servo_name, servo_info in self.servos.items():
            health = self.check_servo(servo_name)
            if health:
                status_icon = {
                    'HEALTHY': '✅',
                    'WARNING': '⚠️',
                    'CRITICAL': '🔴',
                    'ERROR': '❌'
                }.get(health['status'], '❓')
                
                lines.append(f"{status_icon} {servo_name}")
                lines.append(f"   Temp: {health['health']['temperature']:.1f}°C  "
                           f"Current: {health['health']['current']:.0f}mA  "
                           f"Angle: {health['current_angle']:.1f}°")
                lines.append(f"   Movements: {health['health']['total_movements']}  "
                           f"Errors: {health['health']['error_count']}")
                lines.append("-" * 80)
        
        # Recent alerts
        if self.alerts:
            lines.append("")
            lines.append("🚨 RECENT ALERTS (Last 5):")
            for alert in list(self.alerts)[-5:]:
                icon = '🔴' if alert['level'] == 'CRITICAL' else '⚠️'
                lines.append(f"  {icon} [{alert['timestamp']}] {alert['servo']}: {alert['message']}")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def export_health_report(self, filename: str = None) -> str:
        """
        Export comprehensive health report to JSON.
        
        Args:
            filename: Output filename (default: auto-generated)
            
        Returns:
            str: Path to exported file
        """
        if filename is None:
            filename = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.data_dir / filename
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': self.get_health_summary(),
            'servos': {},
            'alerts': list(self.alerts)
        }
        
        # Add detailed servo data
        for servo_name in self.servos:
            report['servos'][servo_name] = {
                'current_health': self.get_servo_health(servo_name),
                'history': list(self.health_history[servo_name])[-100:]  # Last 100 records
            }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"✅ Health report exported: {filepath}")
            return str(filepath)
        
        except Exception as e:
            print(f"❌ Failed to export report: {e}")
            return None
    
    def clear_alerts(self):
        """Clear all alerts."""
        self.alerts.clear()
        print("✅ Alerts cleared")
    
    def reset_statistics(self):
        """Reset monitoring statistics."""
        self.stats = {
            'total_alerts': 0,
            'critical_alerts': 0,
            'warnings': 0,
            'monitoring_start': datetime.now(),
            'uptime': 0
        }
        print("✅ Statistics reset")


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("ServoHealthMonitor - Test Mode")
    print("=" * 80)
    
    # Create monitor
    monitor = ServoHealthMonitor(update_interval=2.0)
    
    # Simulate servo registration (would use real servo objects)
    class MockServo:
        def __init__(self, name):
            self.name = name
            self.angle = 90
        
        def get_health_status(self):
            import random
            return {
                'servo_name': self.name,
                'current_angle': self.angle,
                'status': 'HEALTHY',
                'health': {
                    'temperature': random.uniform(20, 70),
                    'current': random.uniform(100, 900),
                    'voltage': 5.0,
                    'total_movements': random.randint(0, 100),
                    'error_count': 0
                }
            }
    
    # Register mock servos
    for i in range(3):
        servo = MockServo(f"test_servo_{i}")
        monitor.register_servo(servo)
    
    # Start monitoring
    monitor.start_monitoring()
    
    # Run for a bit
    print("\n🔄 Monitoring for 10 seconds...")
    for i in range(5):
        time.sleep(2)
        print(monitor.generate_dashboard())
    
    # Stop monitoring
    monitor.stop_monitoring()
    
    # Export report
    monitor.export_health_report()
    
    print("\n✅ Test completed!")
