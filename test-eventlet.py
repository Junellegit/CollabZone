#!/usr/bin/env python
"""Test eventlet installation and compatibility"""

import sys

def test_eventlet():
    try:
        import eventlet
        print("✓ eventlet imported successfully")
        print(f"  Version: {eventlet.__version__}")
        
        # Test monkey patching
        eventlet.monkey_patch()
        print("✓ eventlet monkey patching successful")
        
        return True
    except ImportError:
        print("✗ eventlet not installed")
        print("  Run: pip install eventlet")
        return False
    except Exception as e:
        print(f"✗ eventlet error: {e}")
        return False

def test_socketio_eventlet():
    try:
        from flask import Flask
        from flask_socketio import SocketIO
        
        app = Flask(__name__)
        socketio = SocketIO(app, async_mode='eventlet')
        print("✓ Flask-SocketIO with eventlet mode initialized")
        return True
    except Exception as e:
        print(f"✗ Flask-SocketIO eventlet error: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing eventlet compatibility ===\n")
    
    result1 = test_eventlet()
    result2 = test_socketio_eventlet()
    
    if result1 and result2:
        print("\n✓ All tests passed! eventlet is ready to use.")
    else:
        print("\n✗ Some tests failed. Check the errors above.")
        sys.exit(1)