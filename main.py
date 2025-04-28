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
import json
from functools import wraps
from urllib.parse import urlencode
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from requests_oauthlib import OAuth2Session
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

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define models
class WebUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)  # Nullable for Discord login
    discord_id = db.Column(db.String(64), unique=True, nullable=True)
    discord_username = db.Column(db.String(80), nullable=True)
    discord_discriminator = db.Column(db.String(10), nullable=True)
    discord_avatar = db.Column(db.String(256), nullable=True)
    discord_access_token = db.Column(db.String(256), nullable=True)
    discord_refresh_token = db.Column(db.String(256), nullable=True)
    discord_token_expires_at = db.Column(db.DateTime, nullable=True)
    referral_code = db.Column(db.String(20), unique=True, nullable=True)
    referred_by_id = db.Column(db.Integer, db.ForeignKey('web_user.id'), nullable=True)
    referral_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Self-referential relationship for referrals
    referred_by = db.relationship('WebUser', remote_side=[id], backref=db.backref('referrals', lazy='dynamic'))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return self.password_hash and check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return WebUser.query.get(int(user_id))

# In newer Flask versions, we use this pattern instead of before_first_request
with app.app_context():
    db.create_all()

# Discord OAuth2 Configuration
DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID", "")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET", "")
DISCORD_REDIRECT_URI = os.environ.get("DISCORD_REDIRECT_URI", "http://localhost:5000/discord-callback")
DISCORD_API_BASE_URL = "https://discord.com/api"
DISCORD_AUTHORIZATION_BASE_URL = DISCORD_API_BASE_URL + "/oauth2/authorize"
DISCORD_TOKEN_URL = DISCORD_API_BASE_URL + "/oauth2/token"

def get_discord_oauth():
    return OAuth2Session(
        client_id=DISCORD_CLIENT_ID,
        redirect_uri=DISCORD_REDIRECT_URI,
        scope=["identify", "email"]
    )

# Web routes for static pages
@app.route('/')
def index():
    # Read index.html content
    with open(os.path.join('static', 'index.html'), 'r') as file:
        content = file.read()
    
    # Replace the Discord client ID placeholder
    client_id = os.environ.get('DISCORD_CLIENT_ID', '')
    content = content.replace('CLIENT_ID_PLACEHOLDER', client_id)
    
    return content

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
    return render_template('404.html'), 404

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
        
        # Log the user in
        login_user(user)
        session['user_id'] = user.id
        session['username'] = user.username
        
        return redirect('/dashboard')
    
    return send_from_directory('static', 'register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        logger.info(f"Login attempt for username: {username}")
        
        user = WebUser.query.filter_by(username=username).first()
        
        if not user:
            logger.warning(f"Login failed: User {username} not found")
            return redirect('/login?error=invalid_credentials')
            
        if not user.check_password(password):
            logger.warning(f"Login failed: Invalid password for {username}")
            return redirect('/login?error=invalid_credentials')
            
        # Valid credentials
        logger.info(f"User {username} logged in successfully")
        login_user(user)
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect('/dashboard')
    else:
        # Show any error messages
        error = request.args.get('error')
        if error:
            logger.info(f"Login page displayed with error: {error}")
        return send_from_directory('static', 'login.html')
    
    return send_from_directory('static', 'login.html')

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('/')

# Discord OAuth2 Routes
@app.route('/login-with-discord')
def login_with_discord():
    """Initiate the Discord OAuth2 flow"""
    if not DISCORD_CLIENT_ID or not DISCORD_CLIENT_SECRET:
        flash('Discord login is not configured', 'danger')
        return redirect('/login')
    
    discord = get_discord_oauth()
    authorization_url, state = discord.authorization_url(DISCORD_AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)

@app.route('/discord-callback')
def discord_callback():
    """Handle the Discord OAuth2 callback"""
    if 'oauth2_state' not in session:
        return redirect('/login')
    
    if not DISCORD_CLIENT_ID or not DISCORD_CLIENT_SECRET:
        flash('Discord login is not configured', 'danger')
        return redirect('/login')
    
    try:
        # Get the authorization code
        discord = get_discord_oauth()
        token = discord.fetch_token(
            DISCORD_TOKEN_URL,
            client_secret=DISCORD_CLIENT_SECRET,
            authorization_response=request.url
        )
        
        # Get the user info
        discord = OAuth2Session(DISCORD_CLIENT_ID, token=token)
        user_data = discord.get(f"{DISCORD_API_BASE_URL}/users/@me").json()
        
        # Check if we already have a user with this Discord ID
        discord_id = user_data.get('id')
        user = WebUser.query.filter_by(discord_id=discord_id).first()
        
        if not user:
            # Check if there's a user with this email
            discord_email = user_data.get('email')
            if discord_email:
                user = WebUser.query.filter_by(email=discord_email).first()
                
            if not user:
                # Create a new user
                username = f"{user_data.get('username')}#{user_data.get('discriminator', '')}"
                email = discord_email or f"{discord_id}@example.com"  # Fallback email if none provided
                
                # Make sure username is unique
                base_username = username
                counter = 1
                while WebUser.query.filter_by(username=username).first():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = WebUser(
                    username=username,
                    email=email,
                    discord_id=discord_id,
                    discord_username=user_data.get('username'),
                    discord_discriminator=user_data.get('discriminator', ''),
                    discord_avatar=user_data.get('avatar'),
                    discord_access_token=token.get('access_token'),
                    discord_refresh_token=token.get('refresh_token'),
                )
                db.session.add(user)
                db.session.commit()
            else:
                # Update the existing user with Discord info
                user.discord_id = discord_id
                user.discord_username = user_data.get('username')
                user.discord_discriminator = user_data.get('discriminator', '')
                user.discord_avatar = user_data.get('avatar')
                user.discord_access_token = token.get('access_token')
                user.discord_refresh_token = token.get('refresh_token')
                db.session.commit()
        else:
            # Update token info
            user.discord_access_token = token.get('access_token')
            user.discord_refresh_token = token.get('refresh_token')
            db.session.commit()
        
        # Log the user in
        login_user(user)
        session['user_id'] = user.id
        session['username'] = user.username
        
        # Redirect to dashboard
        return redirect('/dashboard')
        
    except Exception as e:
        logger.error(f"Discord login error: {str(e)}")
        flash('An error occurred during Discord login', 'danger')
        return redirect('/login')

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
    """Get referral statistics for the current user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Get the user
        user_id = session['user_id']
        user = WebUser.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Generate a referral code if they don't have one
        if not user.referral_code:
            import uuid
            import base64
            # Generate a unique code based on user ID and random values
            code_base = f"{user_id}-{uuid.uuid4()}"
            # Create a URL-safe base64 encoded string and truncate to 12 chars
            user.referral_code = base64.urlsafe_b64encode(code_base.encode()).decode()[:12].upper()
            db.session.commit()
        
        # Get referral stats
        referrals = user.referrals.all()
        
        # Format the response
        return jsonify({
            'success': True,
            'referral_code': user.referral_code,
            'referral_count': len(referrals),
            'referrals': [
                {
                    'username': ref.username,
                    'joined_at': ref.created_at.isoformat() if ref.created_at else None
                }
                for ref in referrals
            ]
        })
    except Exception as e:
        logger.error(f"Error fetching referral stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/register-referral', methods=['POST'])
def register_referral():
    """Register a referral code for the current user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    referral_code = data.get('referral_code')
    
    if not referral_code:
        return jsonify({'error': 'Referral code is required'}), 400
    
    try:
        # Get the current user
        user_id = session['user_id']
        user = WebUser.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if they're already referred
        if user.referred_by_id:
            return jsonify({'error': 'You are already referred by someone else'}), 400
        
        # Find the referring user
        referring_user = WebUser.query.filter_by(referral_code=referral_code).first()
        
        if not referring_user:
            return jsonify({'error': 'Invalid referral code'}), 400
        
        # Can't refer yourself
        if referring_user.id == user.id:
            return jsonify({'error': 'You cannot refer yourself'}), 400
        
        # Set the referral relationship
        user.referred_by_id = referring_user.id
        referring_user.referral_count += 1
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'You are now referred by {referring_user.username}',
            'referrer': {
                'username': referring_user.username,
                'id': referring_user.id
            }
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
        
@app.route('/api/discord-client-id', methods=['GET'])
def discord_client_id():
    """Return the Discord client ID for use in frontend templates"""
    client_id = os.environ.get('DISCORD_CLIENT_ID', '')
    return jsonify({'client_id': client_id})

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Always run the web app only (Discord bot runs separately)
    app.run(host='0.0.0.0', port=5000)
