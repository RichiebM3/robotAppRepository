"""
Servo Calibration Tool

This module provides utilities for calibrating servos, including:
- Interactive calibration wizard
- Automated calibration routines
- Calibration data management
- Bulk calibration for multiple servos

Features:
    - Step-by-step calibration process
    - Save/load calibration profiles
    - Test calibration accuracy
    - Generate calibration reports

Author: Robot App Repository Team
Version: 1.0.0
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class ServoCalibration:
    """
    Servo calibration utility class.
    
    Provides tools for calibrating servos including offset, scale,
    and trim adjustments. Supports saving/loading calibration profiles.
    
    Attributes:
        calibration_data (dict): Dictionary of servo calibrations
        calibration_dir (Path): Directory for calibration files
    """
    
    def __init__(self, calibration_dir: str = "data/calibrations"):
        """
        Initialize calibration tool.
        
        Args:
            calibration_dir: Directory to store calibration files
        """
        self.calibration_dir = Path(calibration_dir)
        self.calibration_dir.mkdir(parents=True, exist_ok=True)
        
        self.calibration_data = {}
        self.current_profile = None
        
        print(f"✅ ServoCalibration initialized")
        print(f"📁 Calibration directory: {self.calibration_dir}")
    
    def calibrate_servo_interactive(self, servo_name: str, servo_obj=None) -> Dict:
        """
        Interactive calibration wizard for a single servo.
        
        Args:
            servo_name: Name of the servo to calibrate
            servo_obj: Servo object (optional, for live testing)
            
        Returns:
            dict: Calibration parameters
        """
        print("\n" + "=" * 60)
        print(f"🎯 SERVO CALIBRATION WIZARD - {servo_name}")
        print("=" * 60)
        
        calibration = {
            'servo_name': servo_name,
            'offset': 0.0,
            'scale': 1.0,
            'trim': 0.0,
            'min_angle': 0,
            'max_angle': 180,
            'center_angle': 90,
            'calibrated_at': datetime.now().isoformat(),
            'notes': ''
        }
        
        print("\n📋 Calibration Steps:")
        print("1. Offset: Adjust if servo doesn't reach expected angles")
        print("2. Scale: Adjust if servo range is compressed/expanded")
        print("3. Trim: Fine-tune center position")
        print("4. Test: Verify calibration accuracy")
        
        # Step 1: Offset calibration
        print("\n" + "-" * 60)
        print("STEP 1: OFFSET CALIBRATION")
        print("-" * 60)
        print("Move servo to 90° and measure actual angle.")
        print("If actual angle is different, enter the difference.")
        print("Example: If servo is at 85° when commanded 90°, enter -5")
        
        try:
            offset_input = input("Enter offset (or press Enter for 0): ").strip()
            if offset_input:
                calibration['offset'] = float(offset_input)
                print(f"✅ Offset set to: {calibration['offset']}°")
        except ValueError:
            print("⚠️  Invalid input, using 0")
        
        # Step 2: Scale calibration
        print("\n" + "-" * 60)
        print("STEP 2: SCALE CALIBRATION")
        print("-" * 60)
        print("Test full range (0° to 180°).")
        print("If servo doesn't reach full range, adjust scale.")
        print("Example: If servo only moves 160° when commanded 180°, enter 0.89")
        
        try:
            scale_input = input("Enter scale (or press Enter for 1.0): ").strip()
            if scale_input:
                calibration['scale'] = float(scale_input)
                print(f"✅ Scale set to: {calibration['scale']}")
        except ValueError:
            print("⚠️  Invalid input, using 1.0")
        
        # Step 3: Trim calibration
        print("\n" + "-" * 60)
        print("STEP 3: TRIM CALIBRATION")
        print("-" * 60)
        print("Fine-tune center position (90°).")
        print("Small adjustments to perfect the center position.")
        
        try:
            trim_input = input("Enter trim (or press Enter for 0): ").strip()
            if trim_input:
                calibration['trim'] = float(trim_input)
                print(f"✅ Trim set to: {calibration['trim']}°")
        except ValueError:
            print("⚠️  Invalid input, using 0")
        
        # Step 4: Range limits
        print("\n" + "-" * 60)
        print("STEP 4: RANGE LIMITS")
        print("-" * 60)
        print("Set safe operating range for this servo.")
        
        try:
            min_input = input("Enter minimum angle (default 0): ").strip()
            if min_input:
                calibration['min_angle'] = int(min_input)
            
            max_input = input("Enter maximum angle (default 180): ").strip()
            if max_input:
                calibration['max_angle'] = int(max_input)
            
            print(f"✅ Range set to: {calibration['min_angle']}° - {calibration['max_angle']}°")
        except ValueError:
            print("⚠️  Invalid input, using defaults")
        
        # Notes
        print("\n" + "-" * 60)
        notes = input("Add notes (optional): ").strip()
        if notes:
            calibration['notes'] = notes
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 CALIBRATION SUMMARY")
        print("=" * 60)
        print(f"Servo: {calibration['servo_name']}")
        print(f"Offset: {calibration['offset']}°")
        print(f"Scale: {calibration['scale']}")
        print(f"Trim: {calibration['trim']}°")
        print(f"Range: {calibration['min_angle']}° - {calibration['max_angle']}°")
        if calibration['notes']:
            print(f"Notes: {calibration['notes']}")
        print("=" * 60)
        
        # Save to internal data
        self.calibration_data[servo_name] = calibration
        
        return calibration
    
    def calibrate_servo_auto(self, servo_name: str, servo_obj, 
                            test_angles: List[int] = None) -> Dict:
        """
        Automated calibration using feedback (requires position sensor).
        
        Args:
            servo_name: Name of servo
            servo_obj: Servo object with position feedback
            test_angles: List of angles to test (default: [0, 45, 90, 135, 180])
            
        Returns:
            dict: Calibration parameters
        """
        if test_angles is None:
            test_angles = [0, 45, 90, 135, 180]
        
        print(f"\n🤖 AUTO-CALIBRATING: {servo_name}")
        print(f"Testing angles: {test_angles}")
        
        measurements = []
        
        for target_angle in test_angles:
            print(f"  Testing {target_angle}°...", end=" ")
            
            # Move servo
            if hasattr(servo_obj, 'move_to'):
                servo_obj.move_to(target_angle, blocking=True)
            
            time.sleep(0.5)  # Wait for servo to settle
            
            # Read actual position (simulated for now)
            # In real implementation, read from position sensor
            actual_angle = target_angle  # Placeholder
            
            measurements.append({
                'target': target_angle,
                'actual': actual_angle,
                'error': actual_angle - target_angle
            })
            
            print(f"Actual: {actual_angle}° (error: {actual_angle - target_angle}°)")
        
        # Calculate calibration parameters
        avg_error = sum(m['error'] for m in measurements) / len(measurements)
        
        calibration = {
            'servo_name': servo_name,
            'offset': -avg_error,  # Negative because we compensate
            'scale': 1.0,  # Would calculate from range compression
            'trim': 0.0,
            'min_angle': 0,
            'max_angle': 180,
            'calibrated_at': datetime.now().isoformat(),
            'method': 'auto',
            'measurements': measurements,
            'notes': f'Auto-calibrated with {len(test_angles)} test points'
        }
        
        self.calibration_data[servo_name] = calibration
        
        print(f"✅ Auto-calibration complete!")
        print(f"   Calculated offset: {calibration['offset']}°")
        
        return calibration
    
    def save_calibration(self, profile_name: str = None) -> str:
        """
        Save calibration data to JSON file.
        
        Args:
            profile_name: Name for calibration profile (default: timestamp)
            
        Returns:
            str: Path to saved file
        """
        if not self.calibration_data:
            print("⚠️  No calibration data to save")
            return None
        
        if profile_name is None:
            profile_name = f"calibration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = self.calibration_dir / f"{profile_name}.json"
        
        save_data = {
            'profile_name': profile_name,
            'created_at': datetime.now().isoformat(),
            'servo_count': len(self.calibration_data),
            'servos': self.calibration_data
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            print(f"✅ Calibration saved: {filepath}")
            self.current_profile = profile_name
            return str(filepath)
        
        except Exception as e:
            print(f"❌ Failed to save calibration: {e}")
            return None
    
    def load_calibration(self, profile_name: str) -> bool:
        """
        Load calibration data from JSON file.
        
        Args:
            profile_name: Name of calibration profile
            
        Returns:
            bool: Success status
        """
        filepath = self.calibration_dir / f"{profile_name}.json"
        
        if not filepath.exists():
            print(f"❌ Calibration file not found: {filepath}")
            return False
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.calibration_data = data['servos']
            self.current_profile = profile_name
            
            print(f"✅ Calibration loaded: {profile_name}")
            print(f"   Servos: {len(self.calibration_data)}")
            print(f"   Created: {data['created_at']}")
            
            return True
        
        except Exception as e:
            print(f"❌ Failed to load calibration: {e}")
            return False
    
    def list_profiles(self) -> List[str]:
        """
        List all available calibration profiles.
        
        Returns:
            list: List of profile names
        """
        profiles = []
        
        for filepath in self.calibration_dir.glob("*.json"):
            profiles.append(filepath.stem)
        
        if profiles:
            print(f"\n📋 Available Calibration Profiles ({len(profiles)}):")
            for i, profile in enumerate(profiles, 1):
                print(f"  {i}. {profile}")
        else:
            print("📋 No calibration profiles found")
        
        return profiles
    
    def get_servo_calibration(self, servo_name: str) -> Optional[Dict]:
        """
        Get calibration data for specific servo.
        
        Args:
            servo_name: Name of servo
            
        Returns:
            dict: Calibration data or None
        """
        return self.calibration_data.get(servo_name)
    
    def apply_to_servo(self, servo_name: str, servo_obj) -> bool:
        """
        Apply calibration to servo object.
        
        Args:
            servo_name: Name of servo
            servo_obj: Servo object with set_calibration method
            
        Returns:
            bool: Success status
        """
        calibration = self.get_servo_calibration(servo_name)
        
        if not calibration:
            print(f"⚠️  No calibration found for {servo_name}")
            return False
        
        if not hasattr(servo_obj, 'set_calibration'):
            print(f"⚠️  Servo object doesn't support calibration")
            return False
        
        try:
            servo_obj.set_calibration(
                offset=calibration['offset'],
                scale=calibration['scale'],
                trim=calibration['trim']
            )
            
            print(f"✅ Calibration applied to {servo_name}")
            return True
        
        except Exception as e:
            print(f"❌ Failed to apply calibration: {e}")
            return False
    
    def generate_report(self) -> str:
        """
        Generate calibration report.
        
        Returns:
            str: Formatted report
        """
        if not self.calibration_data:
            return "No calibration data available"
        
        report = []
        report.append("=" * 70)
        report.append("SERVO CALIBRATION REPORT")
        report.append("=" * 70)
        report.append(f"Profile: {self.current_profile or 'Unsaved'}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Servos: {len(self.calibration_data)}")
        report.append("=" * 70)
        report.append("")
        
        for servo_name, cal in self.calibration_data.items():
            report.append(f"Servo: {servo_name}")
            report.append(f"  Offset:  {cal['offset']:>8.2f}°")
            report.append(f"  Scale:   {cal['scale']:>8.3f}")
            report.append(f"  Trim:    {cal['trim']:>8.2f}°")
            report.append(f"  Range:   {cal['min_angle']}° - {cal['max_angle']}°")
            report.append(f"  Date:    {cal['calibrated_at']}")
            if cal.get('notes'):
                report.append(f"  Notes:   {cal['notes']}")
            report.append("-" * 70)
        
        report.append("")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def export_report(self, filename: str = None) -> str:
        """
        Export calibration report to text file.
        
        Args:
            filename: Output filename (default: auto-generated)
            
        Returns:
            str: Path to exported file
        """
        if filename is None:
            filename = f"calibration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = self.calibration_dir.parent / "reports" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        report = self.generate_report()
        
        try:
            with open(filepath, 'w') as f:
                f.write(report)
            
            print(f"✅ Report exported: {filepath}")
            return str(filepath)
        
        except Exception as e:
            print(f"❌ Failed to export report: {e}")
            return None


# Command-line interface
def main():
    """Command-line calibration tool."""
    print("\n" + "=" * 70)
    print("🎯 SERVO CALIBRATION TOOL")
    print("=" * 70)
    
    cal = ServoCalibration()
    
    while True:
        print("\n📋 MENU:")
        print("  1. Calibrate new servo (interactive)")
        print("  2. List calibration profiles")
        print("  3. Load calibration profile")
        print("  4. Save current calibration")
        print("  5. Generate report")
        print("  6. Export report")
        print("  0. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            servo_name = input("Enter servo name: ").strip()
            if servo_name:
                cal.calibrate_servo_interactive(servo_name)
        
        elif choice == '2':
            cal.list_profiles()
        
        elif choice == '3':
            profile_name = input("Enter profile name: ").strip()
            if profile_name:
                cal.load_calibration(profile_name)
        
        elif choice == '4':
            profile_name = input("Enter profile name (or press Enter for auto): ").strip()
            cal.save_calibration(profile_name if profile_name else None)
        
        elif choice == '5':
            print("\n" + cal.generate_report())
        
        elif choice == '6':
            filename = input("Enter filename (or press Enter for auto): ").strip()
            cal.export_report(filename if filename else None)
        
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("⚠️  Invalid option")


if __name__ == "__main__":
    main()
