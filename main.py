"""
Trial Junkie - Main Entry Point
A drug-themed Discord bot for generating trial credentials and automation
Also includes a web dashboard for account management
"""
import os
import logging
import random
import time
import asyncio
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from bot import setup_bot

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = os.environ.get("SESSION_SECRET", os.urandom(24))

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize database
db = SQLAlchemy(app)

# Define models
class WebUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    discord_id = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# In newer Flask versions, we use this pattern instead of before_first_request
with app.app_context():
    db.create_all()

# Web routes for static pages
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return send_from_directory('static', 'dashboard.html')

@app.route('/agents')
def agents():
    return send_from_directory('static', 'agents.html')

@app.route('/referrals')
def referrals():
    return send_from_directory('static', 'referrals.html')

@app.route('/roadmap')
def roadmap():
    return send_from_directory('static', 'roadmap.html')

@app.route('/trials')
def trials():
    if 'user_id' not in session:
        return redirect('/login')
    return send_from_directory('static', 'trials.html')

# Catch-all route for any dashboard pages that don't exist yet
@app.route('/<path:path>')
def catch_all(path):
    # Check if file exists in static folder first
    static_file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(static_file_path):
        return send_from_directory(app.static_folder, path)
    
    # If it's an HTML page in our known pages, try to serve it
    if path.endswith('.html'):
        try:
            return send_from_directory('static', path)
        except:
            pass

    # If it's likely a frontend route, serve the main index
    probable_routes = ['dashboard', 'login', 'register', 'profile', 'settings', 'agents', 'trials', 'referrals', 'roadmap']
    for route in probable_routes:
        if path.startswith(route):
            return send_from_directory('static', 'index.html')
    
    # Otherwise, return a custom 404 page
    return render_404()

# Static assets routes
@app.route('/css/<path:filename>')
def css_files(filename):
    return send_from_directory('src/public/css', filename)

@app.route('/js/<path:filename>')
def js_files(filename):
    return send_from_directory('src/public/js', filename)

@app.route('/img/<path:filename>')
def img_files(filename):
    return send_from_directory('src/public/img', filename)

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        discord_id = request.form.get('discord_id')
        
        # Check if user already exists
        existing_user = WebUser.query.filter((WebUser.username == username) | (WebUser.email == email)).first()
        if existing_user:
            flash('Username or email already exists', 'danger')
            return send_from_directory('static', 'register.html')
        
        # Create new user
        user = WebUser(username=username, email=email, discord_id=discord_id)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return redirect('/login')
    
    return send_from_directory('static', 'register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = WebUser.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect('/dashboard')
        else:
            return redirect('/login?error=invalid_credentials')
    
    return send_from_directory('static', 'login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# API routes
@app.route('/api/trials', methods=['GET'])
def get_trials():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Here we would fetch the user's trials from our database
    # For now, return a sample response
    return jsonify({
        'trials': [
            {
                'id': 1,
                'service': 'netflix',
                'email': 'user123@example.com',
                'created_at': '2025-04-26T12:00:00Z',
                'expires_at': '2025-05-26T12:00:00Z'
            },
            {
                'id': 2,
                'service': 'hulu',
                'email': 'user456@example.com',
                'created_at': '2025-04-25T14:30:00Z',
                'expires_at': '2025-05-25T14:30:00Z'
            }
        ]
    })

@app.route('/api/generate-trial', methods=['POST'])
def generate_trial():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    service = data.get('service')
    trial_type = data.get('type', 'hit')
    automate = data.get('automate', False)
    
    if not service:
        return jsonify({'error': 'Service is required'}), 400
    
    try:
        # Get user's subscription tier
        user_id = session['user_id']
        user = WebUser.query.get(user_id)
        
        # Import the trial generator
        from utils.trial_generator import TrialGenerator
        generator = TrialGenerator()
        
        # Generate trial based on the service
        trial_info = asyncio.run(generator.generate_trial(service))
        
        # Save the trial to the database (implementation would go here)
        # ...
        
        # Return the trial info
        return jsonify({
            'success': True,
            'trial': {
                'id': random.randint(1000, 9999),
                'service': service,
                'type': trial_type,
                'automated': automate,
                'email': trial_info['user_info']['email'],
                'password': trial_info['user_info']['password'],
                'created_at': trial_info['generated_at'],
                'expires_at': trial_info['trial_end_date']
            }
        })
    except Exception as e:
        logger.error(f"Error generating trial: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/create-payment', methods=['POST'])
def create_payment():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    plan_id = data.get('plan_id')
    
    if not plan_id:
        return jsonify({'error': 'Plan ID is required'}), 400
    
    try:
        # Import the payment processor
        from utils.payment_processor import PaymentProcessor, SUBSCRIPTION_TIERS
        
        # Get pricing from subscription tiers
        if plan_id not in SUBSCRIPTION_TIERS:
            return jsonify({'error': 'Invalid plan ID'}), 400
            
        amount = SUBSCRIPTION_TIERS[plan_id]['price']
        
        # Create payment request
        processor = PaymentProcessor()
        payment = asyncio.run(processor.create_payment_request(session['user_id'], plan_id, amount))
        
        return jsonify({
            'success': True,
            'amount': amount,
            'reference': payment['reference'],
            'wallet_address': payment['wallet_address'],
            'created_at': payment['created_at']
        })
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    reference = data.get('reference')
    tx_signature = data.get('tx_signature')
    
    if not reference:
        return jsonify({'error': 'Payment reference is required'}), 400
    
    try:
        # Import the payment processor
        from utils.payment_processor import PaymentProcessor
        
        # Verify payment
        processor = PaymentProcessor()
        result = asyncio.run(processor.verify_payment(reference, tx_signature))
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Payment verified successfully',
                'tier': result.get('service_type')
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            })
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/payments', methods=['GET'])
def get_payments():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    status = request.args.get('status')
    
    try:
        # Import the payment processor
        from utils.payment_processor import PaymentProcessor
        
        # Get user payments
        processor = PaymentProcessor()
        payments = asyncio.run(processor.get_user_payments(session['user_id'], status))
        
        return jsonify({
            'success': True,
            'payments': payments
        })
    except Exception as e:
        logger.error(f"Error fetching payments: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/user-tier', methods=['GET'])
def get_user_tier():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Import the payment processor
        from utils.payment_processor import PaymentProcessor
        
        # Get user tier
        processor = PaymentProcessor()
        tier_info = asyncio.run(processor.get_user_tier(session['user_id']))
        
        return jsonify({
            'success': True,
            'tier': tier_info
        })
    except Exception as e:
        logger.error(f"Error fetching user tier: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/referral-stats', methods=['GET'])
def get_referral_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Import the referral system
        from utils.referral_system import ReferralSystem
        
        # Get referral stats
        referral_system = ReferralSystem()
        stats = asyncio.run(referral_system.get_referral_stats(session['user_id']))
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        logger.error(f"Error fetching referral stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/register-referral', methods=['POST'])
def register_referral():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    referral_code = data.get('referral_code')
    
    if not referral_code:
        return jsonify({'error': 'Referral code is required'}), 400
    
    try:
        # Import the referral system
        from utils.referral_system import ReferralSystem
        
        # Register referral
        referral_system = ReferralSystem()
        result = asyncio.run(referral_system.register_referral(session['user_id'], referral_code))
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message'],
                'referrer': result.get('referrer')
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            })
    except Exception as e:
        logger.error(f"Error registering referral: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/withdraw-commission', methods=['POST'])
def withdraw_commission():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    amount = data.get('amount')
    wallet_address = data.get('wallet_address')
    
    if not amount or not wallet_address:
        return jsonify({'error': 'Amount and wallet address are required'}), 400
    
    try:
        # In a real implementation, this would process the withdrawal
        # and transfer SOL to the user's wallet
        
        # For now, just return success response
        return jsonify({
            'success': True,
            'message': f'Successfully requested withdrawal of {amount} SOL to {wallet_address}',
            'transaction_id': f'withdrawal_{int(time.time())}'
        })
    except Exception as e:
        logger.error(f"Error processing withdrawal: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check if we're running the Discord bot
    if os.environ.get("RUN_DISCORD_BOT", "0") == "1":
        # Check if Discord token is available
        token = os.getenv("DISCORD_BOT_TOKEN")
        if not token:
            logger.error("DISCORD_BOT_TOKEN not found in environment variables")
            logger.info("Please set DISCORD_BOT_TOKEN in the .env file")
            exit(1)
        
        # Run the bot
        logger.info("Starting Trial Junkie Discord Bot...")
        bot = setup_bot()
        bot.run(token)
    else:
        # Run the web app
        app.run(host='0.0.0.0', port=5000)
