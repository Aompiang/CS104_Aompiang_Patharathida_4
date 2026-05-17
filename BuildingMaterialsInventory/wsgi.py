"""
WSGI entry point for PythonAnywhere deployment
"""
import sys
import os

# Add the project directory to sys.path
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.append(project_home)

# Import the Flask app
from app import app as application

# Ensure debug mode is OFF for production
application.config['DEBUG'] = False
