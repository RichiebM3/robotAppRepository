"""
Utilities Module

General utility functions and helper classes for robot applications.

Categories:
    - Math utilities (interpolation, kinematics, etc.)
    - Data processing (filtering, smoothing, etc.)
    - File I/O utilities
    - Logging utilities
    - Configuration management
    - Time/Date utilities

Usage:
    from shared.utils import interpolate, smooth_data, setup_logger
    
    values = interpolate(start=0, end=100, steps=10)
    smoothed = smooth_data(raw_data, window_size=5)
    logger = setup_logger('my_robot')
"""

__version__ = '1.0.0'

import math
import logging
from typing import List, Tuple, Union
from pathlib import Path


# ============================================================
# Math Utilities
# ============================================================

def interpolate(start: float, end: float, steps: int, 
                method: str = 'linear') -> List[float]:
    """
    Interpolate between start and end values.
    
    Args:
        start: Starting value
        end: Ending value
        steps: Number of interpolation steps
        method: Interpolation method ('linear', 'ease_in', 'ease_out', 'ease_in_out')
        
    Returns:
        list: Interpolated values
    """
    if steps <= 1:
        return [end]
    
    values = []
    
    for i in range(steps):
        t = i / (steps - 1)  # Normalized time [0, 1]
        
        if method == 'linear':
            value = start + (end - start) * t
        elif method == 'ease_in':
            value = start + (end - start) * (t ** 2)
        elif method == 'ease_out':
            value = start + (end - start) * (1 - (1 - t) ** 2)
        elif method == 'ease_in_out':
            if t < 0.5:
                value = start + (end - start) * (2 * t ** 2)
            else:
                value = start + (end - start) * (1 - 2 * (1 - t) ** 2)
        else:
            value = start + (end - start) * t
        
        values.append(value)
    
    return values


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp value between min and max.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        float: Clamped value
    """
    return max(min_val, min(max_val, value))


def map_range(value: float, in_min: float, in_max: float,
              out_min: float, out_max: float) -> float:
    """
    Map value from one range to another.
    
    Args:
        value: Input value
        in_min: Input range minimum
        in_max: Input range maximum
        out_min: Output range minimum
        out_max: Output range maximum
        
    Returns:
        float: Mapped value
    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def smooth_data(data: List[float], window_size: int = 5) -> List[float]:
    """
    Smooth data using moving average.
    
    Args:
        data: Input data
        window_size: Size of smoothing window
        
    Returns:
        list: Smoothed data
    """
    if len(data) < window_size:
        return data.copy()
    
    smoothed = []
    half_window = window_size // 2
    
    for i in range(len(data)):
        start = max(0, i - half_window)
        end = min(len(data), i + half_window + 1)
        window = data[start:end]
        smoothed.append(sum(window) / len(window))
    
    return smoothed


def degrees_to_radians(degrees: float) -> float:
    """Convert degrees to radians."""
    return degrees * math.pi / 180.0


def radians_to_degrees(radians: float) -> float:
    """Convert radians to degrees."""
    return radians * 180.0 / math.pi


# ============================================================
# Logging Utilities
# ============================================================

def setup_logger(name: str, log_file: str = None, 
                level: int = logging.INFO) -> logging.Logger:
    """
    Setup logger with console and optional file output.
    
    Args:
        name: Logger name
        log_file: Optional log file path
        level: Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(console_format)
        logger.addHandler(file_handler)
    
    return logger


# ============================================================
# File Utilities
# ============================================================

def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists, create if necessary.
    
    Args:
        path: Directory path
        
    Returns:
        Path: Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_project_root() -> Path:
    """
    Get project root directory.
    
    Returns:
        Path: Project root path
    """
    # Assuming this file is in shared/utils/
    return Path(__file__).parent.parent.parent


# ============================================================
# Configuration Utilities
# ============================================================

class ConfigManager:
    """Simple configuration manager for loading/saving configs."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.configs = {}
    
    def load(self, name: str) -> dict:
        """Load configuration from JSON file."""
        import json
        
        filepath = self.config_dir / f"{name}.json"
        
        if not filepath.exists():
            return {}
        
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
            
            self.configs[name] = config
            return config
        
        except Exception as e:
            print(f"❌ Failed to load config '{name}': {e}")
            return {}
    
    def save(self, name: str, config: dict) -> bool:
        """Save configuration to JSON file."""
        import json
        
        filepath = self.config_dir / f"{name}.json"
        
        try:
            with open(filepath, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.configs[name] = config
            return True
        
        except Exception as e:
            print(f"❌ Failed to save config '{name}': {e}")
            return False
    
    def get(self, name: str, key: str, default=None):
        """Get configuration value."""
        if name not in self.configs:
            self.load(name)
        
        return self.configs.get(name, {}).get(key, default)


# ============================================================
# Export
# ============================================================

__all__ = [
    # Math utilities
    'interpolate',
    'clamp',
    'map_range',
    'smooth_data',
    'degrees_to_radians',
    'radians_to_degrees',
    
    # Logging utilities
    'setup_logger',
    
    # File utilities
    'ensure_directory',
    'get_project_root',
    
    # Configuration
    'ConfigManager'
]


# Module info
print("🔧 Utils module loaded")
