#!/usr/bin/env python3
"""
Simple CRM System - Run Script
This script starts the Flask CRM application.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the app - this will trigger the initialization in app.py
from app import app

if __name__ == '__main__':
    print("🚀 Starting Simple CRM System via run.py...")
    print("📱 Access the application at: http://localhost:5000")
    print("👤 Login credentials: admin / admin123")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 CRM System stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting the application: {e}")
        sys.exit(1) 