"""
Communication Module

Network and IPC communication utilities for robot control and monitoring.

Features:
    - WebSocket communication
    - HTTP REST API
    - MQTT messaging
    - Serial communication
    - Inter-process communication (IPC)

Planned components:
    - WebSocketServer/Client
    - RESTAPIServer
    - MQTTClient
    - SerialInterface
    - IPCManager

Usage:
    from shared.communication import WebSocketServer
    
    server = WebSocketServer(host='0.0.0.0', port=8765)
    server.start()
"""

__version__ = '1.0.0'

# Placeholder for future communication implementations
__all__ = []

# Module-level configuration
DEFAULT_COMM_CONFIG = {
    'websocket_port': 8765,
    'rest_api_port': 5000,
    'mqtt_broker': 'localhost',
    'mqtt_port': 1883,
    'serial_baudrate': 115200,
    'timeout': 5.0,
    'max_retries': 3
}

def get_default_config():
    """Return default communication configuration"""
    return DEFAULT_COMM_CONFIG.copy()

# TODO: Import communication classes as they are implemented
# from .websocket import WebSocketServer, WebSocketClient
# from .rest_api import RESTAPIServer
# from .mqtt import MQTTClient
# from .serial_comm import SerialInterface

print("📡 Communication module loaded (placeholder)")
