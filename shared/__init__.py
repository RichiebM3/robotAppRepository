"""
Shared utilities for all robot platforms in ROBOTAPPREPOSITORY

This package contains reusable modules that can be shared across
different robot platforms (Freenove Hexapod, Spider Robot, etc.)

Modules:
    - servo_control: Enhanced servo control with health monitoring
    - sensors: Sensor interfaces and data processing
    - communication: Network and IPC communication utilities
    - utils: General utility functions
"""

__version__ = '1.0.0'
__author__ = 'Robot App Repository Team'

# Import submodules for easier access
from . import servo_control
from . import sensors
from . import communication
from . import utils

__all__ = [
    'servo_control',
    'sensors', 
    'communication',
    'utils'
]

# Package-level configuration
DEFAULT_CONFIG = {
    'debug_mode': False,
    'log_level': 'INFO',
    'data_directory': 'data/'
}

def get_version():
    """Return the current package version"""
    return __version__

def get_config():
    """Return the default configuration"""
    return DEFAULT_CONFIG.copy()
