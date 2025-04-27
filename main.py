"""
Main application for Trial Junkie
Handles both Discord bot and web interface
"""
import os
import logging
from flask import Flask, jsonify, request, render_template, redirect, url_for
from dotenv import load_dotenv
import subprocess
import atexit
import signal
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("trial_junkie")

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
           static_folder='static',
           template_folder='templates')

# Set secret key for sessions
app.secret_key = os.environ.get("SESSION_SECRET", os.urandom(24))

# Discord bot process reference
bot_process = None

@app.route('/')
def index():
    """Render the landing page"""
    return render_template('index.html')

@app.route('/login')
def login():
    """Render the login page"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Render the dashboard page"""
    return render_template('dashboard.html')

@app.route('/register')
def register():
    """Render the registration page"""
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Log the user out and redirect to the homepage"""
    # In a real implementation, this would clear the session
    return redirect(url_for('index'))

@app.route('/api/bot/status', methods=['GET'])
def bot_status():
    """Check if the Discord bot is running"""
    global bot_process
    
    if bot_process and bot_process.poll() is None:
        return jsonify({"status": "running"})
    else:
        return jsonify({"status": "stopped"})

@app.route('/api/bot/start', methods=['POST'])
def start_bot():
    """Start the Discord bot"""
    global bot_process
    
    if bot_process and bot_process.poll() is None:
        return jsonify({"status": "already_running", "message": "Bot is already running"})
    
    try:
        # Use the standalone version that doesn't depend on Flask
        bot_process = subprocess.Popen(["python", "discord_bot_standalone.py"],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      text=True)
        
        logger.info("Discord bot started")
        return jsonify({"status": "started", "message": "Bot started successfully"})
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    """Stop the Discord bot"""
    global bot_process
    
    if not bot_process or bot_process.poll() is not None:
        return jsonify({"status": "not_running", "message": "Bot is not running"})
    
    try:
        # Try to terminate gracefully first
        bot_process.terminate()
        
        # Wait for a short time to see if it terminates
        try:
            bot_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # If not, force kill
            bot_process.kill()
        
        logger.info("Discord bot stopped")
        return jsonify({"status": "stopped", "message": "Bot stopped successfully"})
    except Exception as e:
        logger.error(f"Error stopping bot: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/trials/<user_id>', methods=['GET'])
def get_user_trials(user_id):
    """Get trials for a user"""
    # This would normally query the database
    # For now, return a sample response
    return jsonify({
        "trials": [
            {
                "service": "netflix",
                "email": "user123@example.com",
                "password": "********",
                "expires": "2023-05-01"
            }
        ]
    })

def cleanup():
    """Clean up resources when the app exits"""
    global bot_process
    
    if bot_process and bot_process.poll() is None:
        logger.info("Shutting down Discord bot")
        try:
            bot_process.terminate()
            bot_process.wait(timeout=5)
        except:
            # Force kill if it doesn't terminate
            bot_process.kill()

# Register the cleanup function to be called when the app exits
atexit.register(cleanup)

if __name__ == '__main__':
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000)