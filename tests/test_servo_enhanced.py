"""
Unit Tests for ServoEnhanced

Tests for the enhanced servo control system including:
- Basic movement
- Health monitoring
- Calibration
- Error handling
- Data export

Run with: python -m pytest tests/test_servo_enhanced.py
Or: python tests/test_servo_enhanced.py
"""

import unittest
import time
import json
import tempfile
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.servo_control import ServoEnhanced


class TestServoEnhanced(unittest.TestCase):
    """Test cases for ServoEnhanced class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.servo = ServoEnhanced(
            channel=0,
            name="test_servo",
            min_angle=0,
            max_angle=180,
            default_speed=50
        )
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    # ========================================
    # Initialization Tests
    # ========================================
    
    def test_initialization(self):
        """Test servo initialization."""
        self.assertEqual(self.servo.channel, 0)
        self.assertEqual(self.servo.name, "test_servo")
        self.assertEqual(self.servo.min_angle, 0)
        self.assertEqual(self.servo.max_angle, 180)
        self.assertEqual(self.servo.current_angle, 90.0)
    
    def test_default_name(self):
        """Test default servo name generation."""
        servo = ServoEnhanced(channel=5)
        self.assertEqual(servo.name, "servo_5")
    
    # ========================================
    # Movement Tests
    # ========================================
    
    def test_move_to_valid_angle(self):
        """Test moving to valid angle."""
        result = self.servo.move_to(45)
        self.assertTrue(result)
        self.assertEqual(self.servo.current_angle, 45.0)
    
    def test_move_to_invalid_angle_low(self):
        """Test moving to angle below minimum."""
        result = self.servo.move_to(-10)
        self.assertFalse(result)
    
    def test_move_to_invalid_angle_high(self):
        """Test moving to angle above maximum."""
        result = self.servo.move_to(200)
        self.assertFalse(result)
    
    def test_move_with_duration(self):
        """Test movement with specified duration."""
        start_time = time.time()
        self.servo.move_to(90, duration=0.5, blocking=True)
        elapsed = time.time() - start_time
        
        # Should take approximately 0.5 seconds
        self.assertGreaterEqual(elapsed, 0.4)
        self.assertLessEqual(elapsed, 0.6)
    
    def test_move_with_speed(self):
        """Test movement with specified speed."""
        result = self.servo.move_to(90, speed=100)
        self.assertTrue(result)
    
    def test_movement_history(self):
        """Test movement history tracking."""
        initial_count = len(self.servo.movement_history)
        
        self.servo.move_to(45)
        self.servo.move_to(135)
        self.servo.move_to(90)
        
        self.assertEqual(len(self.servo.movement_history), initial_count + 3)
    
    # ========================================
    # Health Monitoring Tests
    # ========================================
    
    def test_get_health_status(self):
        """Test health status retrieval."""
        health = self.servo.get_health_status()
        
        self.assertIn('servo_name', health)
        self.assertIn('channel', health)
        self.assertIn('health', health)
        self.assertIn('status', health)
        
        self.assertEqual(health['servo_name'], 'test_servo')
        self.assertEqual(health['channel'], 0)
    
    def test_update_health_metrics(self):
        """Test updating health metrics."""
        self.servo.update_health_metrics(
            temperature=45.5,
            current=350.0,
            voltage=5.0
        )
        
        health = self.servo.get_health_status()
        self.assertEqual(health['health']['temperature'], 45.5)
        self.assertEqual(health['health']['current'], 350.0)
        self.assertEqual(health['health']['voltage'], 5.0)
    
    def test_temperature_warning(self):
        """Test temperature warning threshold."""
        self.servo.update_health_metrics(temperature=65.0)
        health = self.servo.get_health_status()
        
        self.assertEqual(health['status'], 'WARNING')
        self.assertGreater(health['health']['warning_count'], 0)
    
    def test_temperature_critical(self):
        """Test temperature critical threshold."""
        self.servo.update_health_metrics(temperature=80.0)
        health = self.servo.get_health_status()
        
        self.assertEqual(health['status'], 'CRITICAL')
        self.assertGreater(health['health']['error_count'], 0)
    
    def test_current_warning(self):
        """Test current warning threshold."""
        self.servo.update_health_metrics(current=850.0)
        health = self.servo.get_health_status()
        
        self.assertEqual(health['status'], 'WARNING')
    
    def test_current_critical(self):
        """Test current critical threshold."""
        self.servo.update_health_metrics(current=1100.0)
        health = self.servo.get_health_status()
        
        self.assertEqual(health['status'], 'CRITICAL')
    
    def test_reset_health_counters(self):
        """Test resetting health counters."""
        # Generate some errors
        self.servo.update_health_metrics(temperature=80.0)
        self.servo.update_health_metrics(current=1100.0)
        
        # Reset
        self.servo.reset_health_counters()
        
        health = self.servo.get_health_status()
        self.assertEqual(health['health']['error_count'], 0)
        self.assertEqual(health['health']['warning_count'], 0)
    
    # ========================================
    # Calibration Tests
    # ========================================
    
    def test_set_calibration(self):
        """Test setting calibration parameters."""
        self.servo.set_calibration(offset=5.0, scale=1.1, trim=0.5)
        
        self.assertEqual(self.servo.calibration['offset'], 5.0)
        self.assertEqual(self.servo.calibration['scale'], 1.1)
        self.assertEqual(self.servo.calibration['trim'], 0.5)
        self.assertIsNotNone(self.servo.calibration['last_calibrated'])
    
    def test_calibration_applied_to_movement(self):
        """Test that calibration is applied to movements."""
        self.servo.set_calibration(offset=10.0, scale=1.0, trim=0.0)
        self.servo.move_to(90)
        
        # With offset of 10, actual angle should be 100
        self.assertEqual(self.servo.current_angle, 100.0)
    
    # ========================================
    # Statistics Tests
    # ========================================
    
    def test_get_movement_stats(self):
        """Test movement statistics."""
        self.servo.move_to(45)
        self.servo.move_to(135)
        self.servo.move_to(90)
        
        stats = self.servo.get_movement_stats()
        
        self.assertIn('total_movements', stats)
        self.assertIn('total_distance', stats)
        self.assertIn('average_speed', stats)
        
        self.assertEqual(stats['total_movements'], 3)
        self.assertGreater(stats['total_distance'], 0)
    
    def test_movement_distance_calculation(self):
        """Test movement distance tracking."""
        self.servo.current_angle = 0
        self.servo.move_to(90)
        
        stats = self.servo.get_movement_stats()
        self.assertEqual(stats['total_distance'], 90.0)
    
    # ========================================
    # Data Export Tests
    # ========================================
    
    def test_export_data(self):
        """Test exporting servo data to JSON."""
        # Perform some operations
        self.servo.move_to(45)
        self.servo.move_to(135)
        self.servo.update_health_metrics(temperature=45.0, current=350.0)
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            result = self.servo.export_data(temp_file)
            self.assertTrue(result)
            
            # Verify file contents
            with open(temp_file, 'r') as f:
                data = json.load(f)
            
            self.assertIn('servo_info', data)
            self.assertIn('health_data', data)
            self.assertIn('movement_history', data)
            self.assertEqual(data['servo_info']['name'], 'test_servo')
        
        finally:
            # Clean up
            Path(temp_file).unlink(missing_ok=True)
    
    # ========================================
    # Error Handling Tests
    # ========================================
    
    def test_error_logging(self):
        """Test error logging."""
        # Trigger an error (invalid angle)
        self.servo.move_to(200)
        
        health = self.servo.get_health_status()
        self.assertGreater(len(health['errors']), 0)
    
    def test_warning_logging(self):
        """Test warning logging."""
        # Trigger a warning (high temperature)
        self.servo.update_health_metrics(temperature=65.0)
        
        health = self.servo.get_health_status()
        self.assertGreater(len(health['warnings']), 0)
    
    # ========================================
    # Thread Safety Tests
    # ========================================
    
    def test_concurrent_movements(self):
        """Test thread safety with concurrent operations."""
        import threading
        
        def move_servo():
            for _ in range(10):
                self.servo.move_to(45)
                self.servo.move_to(135)
        
        threads = [threading.Thread(target=move_servo) for _ in range(3)]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        # Should complete without errors
        health = self.servo.get_health_status()
        self.assertIsNotNone(health)
    
    # ========================================
    # String Representation Tests
    # ========================================
    
    def test_repr(self):
        """Test string representation."""
        repr_str = repr(self.servo)
        self.assertIn('test_servo', repr_str)
        self.assertIn('channel=0', repr_str)


class TestServoEnhancedIntegration(unittest.TestCase):
    """Integration tests for ServoEnhanced."""
    
    def test_full_workflow(self):
        """Test complete workflow: create, calibrate, move, monitor, export."""
        # Create servo
        servo = ServoEnhanced(channel=0, name="integration_test")
        
        # Set calibration
        servo.set_calibration(offset=5.0, scale=1.0, trim=0.0)
        
        # Perform movements
        servo.move_to(45, duration=0.5)
        servo.move_to(135, duration=0.5)
        servo.move_to(90, duration=0.5)
        
        # Update health
        servo.update_health_metrics(temperature=50.0, current=400.0)
        
        # Get health status
        health = servo.get_health_status()
        self.assertEqual(health['status'], 'HEALTHY')
        
        # Get statistics
        stats = servo.get_movement_stats()
        self.assertEqual(stats['total_movements'], 3)
        
        # Export data
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            result = servo.export_data(temp_file)
            self.assertTrue(result)
            self.assertTrue(Path(temp_file).exists())
        finally:
            Path(temp_file).unlink(missing_ok=True)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestServoEnhanced))
    suite.addTests(loader.loadTestsFromTestCase(TestServoEnhancedIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
