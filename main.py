"""
Trial Junkie - Main Application Entry Point
Runs both the web application and the Discord bot
"""
from app import app

# This is a simple import of the Flask app from app.py
# The actual application logic is in app.py
# This file is needed for Gunicorn to find the Flask app object

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)