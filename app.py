"""
Trial Junkie - Web API Entry Point
A simple web API for the Trial Junkie service
"""
from flask import Flask, jsonify
import logging
import os
from database import Database
from agents.pusher import Pusher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "trial_junkie_secret_key")

# Initialize database
db = Database()

# Initialize pusher with agents
try:
    pusher = Pusher(db)
    logger.info("Pusher agent initialized successfully")
except Exception as e:
    logger.error(f"Error initializing pusher agent: {str(e)}")
    pusher = None

@app.route('/')
def index():
    """Home route"""
    return jsonify({
        "name": "Trial Junkie API",
        "version": "1.0.0",
        "description": "API for Trial Junkie - A drug-themed service for generating trial credentials",
        "endpoints": [
            "/api/status"
        ]
    })

@app.route('/api/status')
def status():
    """Status route"""
    api_status = {
        "server": "operational",
        "database": "operational",
        "rapidapi": os.environ.get("RAPIDAPI_KEY") is not None,
        "discord_bot": os.environ.get("DISCORD_BOT_TOKEN") is not None
    }
    
    return jsonify({
        "status": "operational",
        "message": "Trial Junkie API is running",
        "components": api_status
    })

if __name__ == "__main__":
    # Run the Flask app in the main thread
    logger.info("Starting Trial Junkie Web API...")
    app.run(host='0.0.0.0', port=5000)