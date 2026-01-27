#!/usr/bin/env python3
"""
Script to start the web-based task management chatbot
"""

import subprocess
import sys
import os
import time

def install_dependencies():
    """Install required dependencies"""
    print("Installing required dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "web_requirements.txt"])

def start_web_chatbot():
    """Start the web chatbot"""
    print("Starting web-based task management chatbot...")
    print("Visit http://localhost:5001 in your browser to use the chatbot")

    # Import and run the web chatbot
    from web_chatbot import app
    app.run(host='0.0.0.0', port=5001, debug=False)

if __name__ == "__main__":
    # Change to the current directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        # Install dependencies if not already installed
        try:
            import flask
        except ImportError:
            install_dependencies()

        start_web_chatbot()
    except KeyboardInterrupt:
        print("\nShutting down the chatbot...")
    except Exception as e:
        print(f"Error starting the chatbot: {e}")
        sys.exit(1)