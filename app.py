"""
Trial Junkie - Web Application
Flask web app for the Trial Junkie platform
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
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Load environment variables
load_dotenv()

# Define SQLAlchemy base class for models
class Base(DeclarativeBase):
    pass

# Initialize database with the base class
db = SQLAlchemy(model_class=Base)

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key_replace_in_production")

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize the app with the extension
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Wallet session storage for Phantom Wallet integration
wallet_sessions = {}

# Import models (must be imported after db is initialized)
from models import WebUser, Trial, Payment, Referral, Commission, UserTier

@login_manager.user_loader
def load_user(user_id):
    return WebUser.query.get(int(user_id))
    
# Helper function to check subscription status
def check_subscription_status(user_id):
    """Check if a user has an active subscription
    
    Args:
        user_id: The user ID to check
        
    Returns:
        dict: Subscription status information
    """
    user = WebUser.query.get(user_id)
    if not user:
        return {
            'active': False,
            'tier': None,
            'error': 'User not found'
        }
        
    from datetime import datetime
    now = datetime.utcnow()
    
    # Check if subscription is active
    active = bool(user.subscription_tier and user.subscription_expires_at and user.subscription_expires_at > now)
    
    # Calculate days remaining if active
    days_remaining = 0
    if active and user.subscription_expires_at:
        days_remaining = (user.subscription_expires_at - now).days
        
    # Check if subscription is expiring soon (5 days or less)
    expiring_soon = active and days_remaining <= 5
    
    return {
        'active': active,
        'tier': user.subscription_tier if active else None,
        'expires_at': user.subscription_expires_at.isoformat() if active and user.subscription_expires_at else None,
        'days_remaining': days_remaining,
        'expiring_soon': expiring_soon,
        'last_payment_date': user.last_payment_date.isoformat() if user.last_payment_date else None,
        'last_payment_amount': user.last_payment_amount
    }
    
# Helper function to check trial usage limits
def check_trial_usage_limits(user_id, subscription_tier, db_conn=None):
    """Check if a user has reached their daily trial generation limit
    
    Args:
        user_id: The user ID to check
        subscription_tier: The user's subscription tier
        db_conn: A Database connection (optional)
        
    Returns:
        dict: Usage limit information including whether generation is allowed
    """
    # Define tier limits
    tier_limits = {
        'standard': 10,
        'premium': 25,
        'dealers_choice': 50,
        'free': 3  # Free tier has the lowest limit
    }
    
    # Get limit based on user's tier (default to free tier limit)
    tier_limit = tier_limits.get(subscription_tier, tier_limits['free'])
    
    # Create database connection if not provided
    if not db_conn:
        from database import Database
        db_conn = Database()
    
    # Get current usage count for today
    daily_usage = db_conn.get_usage_count(user_id, 'generate_trial')
    
    # Check if user is below the limit
    allowed = daily_usage < tier_limit
    
    # Generate appropriate message
    if allowed:
        message = f"You have used {daily_usage}/{tier_limit} trial generations today"
    else:
        message = f"You have reached your daily limit of {tier_limit} trial generations for your {subscription_tier} tier"
    
    return {
        'allowed': allowed,
        'current_usage': daily_usage,
        'limit': tier_limit,
        'tier': subscription_tier,
        'message': message
    }

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

# Decorator for authentication requirement
def authenticated_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

# Decorator for subscription requirement
def subscription_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
            
        user_id = session['user_id']
        user = WebUser.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Check if user has an active subscription
        from datetime import datetime
        now = datetime.utcnow()
        
        if not user.subscription_tier or not user.subscription_expires_at or user.subscription_expires_at < now:
            return jsonify({
                'error': 'Subscription required',
                'message': 'You need an active subscription to use this feature',
                'redirect': '/subscriptions'
            }), 403
            
        return f(*args, **kwargs)
    return decorated

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
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/login')
        
    # Check if the user has wallet connected
    user_id = session['user_id']
    user = WebUser.query.get(user_id)
    
    if not user:
        logout_user()
        session.clear()
        return redirect('/login?error=user_not_found')
    
    # Check subscription status
    from datetime import datetime
    now = datetime.utcnow()
    subscription_active = user.subscription_tier and user.subscription_expires_at and user.subscription_expires_at > now
    
    # Get subscription days remaining if active
    days_remaining = 0
    if subscription_active and user.subscription_expires_at:
        days_remaining = (user.subscription_expires_at - now).days
    
    # If subscription is expiring soon (5 days or less), set a notification flag for frontend
    subscription_expiring_soon = subscription_active and days_remaining <= 5
    
    # Set session variables for frontend access
    session['subscription_active'] = subscription_active
    session['subscription_tier'] = user.subscription_tier if subscription_active else None
    session['subscription_expiring_soon'] = subscription_expiring_soon
    session['subscription_days_remaining'] = days_remaining
    
    # Serve the dashboard HTML
    return send_from_directory('static', 'dashboard.html')

@app.route('/agents')
def agents():
    return send_from_directory('static', 'agents.html')

@app.route('/referrals')
def referrals():
    # No login required for referrals page
    return send_from_directory('static', 'referrals.html')

@app.route('/referrals/<referral_code>')
def referral_landing(referral_code):
    # Landing page for referral links
    # Store referral code in session for later use during registration
    session['referral_code'] = referral_code
    return send_from_directory('static', 'referrals.html')

@app.route('/roadmap')
def roadmap():
    return send_from_directory('static', 'roadmap.html')

@app.route('/bot-guide')
def bot_guide():
    return render_template('bot_guide.html')

@app.route('/subscriptions')
def subscriptions():
    """Show the subscriptions page"""
    return send_from_directory('static', 'subscriptions.html')

@app.route('/trials')
def trials():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/login')
        
    # Check subscription status - trials page is only for active subscribers
    user_id = session['user_id']
    user = WebUser.query.get(user_id)
    
    if not user:
        logout_user()
        session.clear()
        return redirect('/login?error=user_not_found')
    
    # Check for active subscription
    from datetime import datetime
    now = datetime.utcnow()
    subscription_active = user.subscription_tier and user.subscription_expires_at and user.subscription_expires_at > now
    
    # If no active subscription, redirect to subscriptions page
    if not subscription_active:
        # Add a flash message or query parameter to indicate why they're being redirected
        return redirect('/subscriptions?error=subscription_required')
    
    # User has active subscription, show trials page
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
    return send_from_directory('static/css', filename)

@app.route('/js/<path:filename>')
def js_files(filename):
    return send_from_directory('static/js', filename)

@app.route('/img/<path:filename>')
def img_files(filename):
    return send_from_directory('static/img', filename)

# Password reset routes
@app.route('/forgot-password')
def forgot_password():
    """Show forgot password page"""
    return send_from_directory('static', 'forgot-password.html')

@app.route('/reset-password')
def reset_password_page():
    """Show reset password page"""
    # Check if token is provided
    token = request.args.get('token')
    if not token:
        return redirect('/forgot-password?error=no_token')
    
    return send_from_directory('static', 'reset-password.html')

@app.route('/api/forgot-password', methods=['POST'])
def api_forgot_password():
    """Handle forgot password request"""
    if not request.is_json:
        return jsonify({"success": False, "message": "Invalid request format"})
    
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"success": False, "message": "Email is required"})
    
    # Find user by email
    user = WebUser.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"success": False, "message": "Email not found"})
    
    # Generate reset token
    token = user.generate_reset_token()
    db.session.commit()
    
    # In a real application, we would send an email with the reset link
    # For now, we'll just log it
    reset_link = f"{request.host_url}reset-password?token={token}"
    logger.info(f"Password reset link for {email}: {reset_link}")
    
    # For demo purposes, we'll return the token in the response
    # In production, you would NOT do this - you would only send it via email
    return jsonify({
        "success": True,
        "message": "Password reset instructions sent to your email. Please check your inbox.",
        "_debug_link": reset_link  # For development only, remove in production
    })

@app.route('/api/reset-password', methods=['POST'])
def api_reset_password():
    """Handle password reset"""
    if not request.is_json:
        return jsonify({"success": False, "message": "Invalid request format"})
    
    data = request.get_json()
    token = data.get('token')
    password = data.get('password')
    
    if not token or not password:
        return jsonify({"success": False, "message": "Token and password are required"})
    
    # Find user by reset token
    user = WebUser.query.filter_by(reset_password_token=token).first()
    
    if not user:
        return jsonify({"success": False, "message": "Invalid or expired token"})
    
    # Verify token is valid
    if not user.verify_reset_token(token):
        return jsonify({"success": False, "message": "Token has expired. Please request a new password reset."})
    
    # Check password strength
    if len(password) < 8:
        return jsonify({"success": False, "message": "Password must be at least 8 characters long"})
    
    # Update password and clear token
    user.set_password(password)
    user.clear_reset_token()
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Password has been reset successfully. You can now log in with your new password."
    })

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        discord_id = request.form.get('discord_id')
        
        # Get referral code from form or session
        referral_code = request.form.get('referral_code')
        if not referral_code and 'referral_code' in session:
            referral_code = session.get('referral_code')
        
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
        
        # Process referral if provided
        if referral_code:
            try:
                # Link user to referrer in database
                from database import Database
                db_conn = Database()
                db_conn.register_referral(user.id, referral_code)
                logger.info(f"User {username} registered with referral code: {referral_code}")
            except Exception as e:
                logger.error(f"Error processing referral: {str(e)}")
        
        # Log the user in
        login_user(user)
        session['user_id'] = user.id
        session['username'] = user.username
        
        # Clear referral code from session after use
        if 'referral_code' in session:
            session.pop('referral_code')
        
        return redirect('/dashboard')
    
    # Pass referral code to template if available in session
    referral_code = session.get('referral_code', None)
    if referral_code:
        # In a real implementation, we would pass this to the template
        # But for now, we'll just show it in the logs
        logger.info(f"Registration page loaded with referral code: {referral_code}")
    
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
    try:
        # Get user ID before clearing session to cleanup wallet sessions
        user_id = session.get('user_id')
        
        # Clear Flask-Login
        logout_user()
        
        # Remove from wallet session tracking if it exists
        if user_id and user_id in wallet_sessions:
            del wallet_sessions[user_id]
        
        # Clear all session data
        session.clear()
        
        logger.info(f"User logged out successfully: {user_id}")
        return redirect('/')
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        # Even if there's an error, try to clear session and redirect
        session.clear()
        return redirect('/?error=logout_error')

# Discord OAuth2 Routes
# Wallet Authentication routes
@app.route('/api/login-with-wallet', methods=['POST'])
@app.route('/login-with-wallet', methods=['POST'])
def login_with_wallet():
    """Login with Phantom wallet"""
    if not request.is_json:
        return jsonify({"success": False, "message": "Invalid request format"})
    
    data = request.get_json()
    wallet_address = data.get('wallet_address')
    
    if not wallet_address:
        return jsonify({"success": False, "message": "Wallet address is required"})
    
    # Check if user exists with this wallet address
    user = WebUser.query.filter_by(wallet_address=wallet_address).first()
    
    if not user:
        # No existing user with this wallet
        return jsonify({
            "success": False, 
            "message": "No account found for this wallet. Please register first."
        })
    
    # User found, log them in
    login_user(user)
    session['user_id'] = user.id
    session['username'] = user.username
    
    # Return success
    return jsonify({
        "success": True,
        "message": "Login successful",
        "redirect": "/dashboard"
    })

@app.route('/api/register-with-wallet', methods=['POST'])
@app.route('/register-with-wallet', methods=['POST'])
def register_with_wallet():
    """Register with Phantom wallet"""
    if not request.is_json:
        return jsonify({"success": False, "message": "Invalid request format"})
    
    data = request.get_json()
    wallet_address = data.get('wallet_address')
    username = data.get('username')
    email = data.get('email')
    
    if not wallet_address:
        return jsonify({"success": False, "message": "Wallet address is required"})
    
    if not username or not email:
        return jsonify({"success": False, "message": "Username and email are required"})
    
    # Check if user already exists with this wallet
    existing_wallet_user = WebUser.query.filter_by(wallet_address=wallet_address).first()
    
    if existing_wallet_user:
        return jsonify({"success": False, "message": "This wallet is already registered"})
    
    # Check if username or email already exists
    existing_user = WebUser.query.filter((WebUser.username == username) | (WebUser.email == email)).first()
    
    if existing_user:
        return jsonify({"success": False, "message": "Username or email already exists"})
    
    # Create new user with wallet address
    user = WebUser(
        username=username,
        email=email,
        wallet_address=wallet_address
    )
    
    # Generate a random secure password for wallet users
    import secrets
    import string
    password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(20))
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    # Process referral if provided
    referral_code = session.get('referral_code')
    if referral_code:
        try:
            from database import Database
            db_conn = Database()
            db_conn.register_referral(user.id, referral_code)
            logger.info(f"Wallet user {username} registered with referral code: {referral_code}")
            # Clear referral code from session after use
            session.pop('referral_code')
        except Exception as e:
            logger.error(f"Error processing referral: {str(e)}")
    
    # Log the user in
    login_user(user)
    session['user_id'] = user.id
    session['username'] = user.username
    
    # Return success
    return jsonify({
        "success": True,
        "message": "Registration successful",
        "redirect": "/dashboard"
    })
    
# Deprecated Discord OAuth routes - keeping for backward compatibility
@app.route('/login-with-discord')
def login_with_discord():
    """Initiate the Discord OAuth2 flow - Deprecated"""
    flash('Discord login is being phased out. Please use Phantom Wallet login instead.', 'warning')
    return redirect('/login')

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
                
                # Process referral if provided in session
                referral_code = session.get('referral_code')
                if referral_code:
                    try:
                        # Link user to referrer in database
                        from database import Database
                        db_conn = Database()
                        db_conn.register_referral(user.id, referral_code)
                        logger.info(f"Discord user {username} registered with referral code: {referral_code}")
                        # Clear referral code from session after use
                        session.pop('referral_code')
                    except Exception as e:
                        logger.error(f"Error processing referral for Discord user: {str(e)}")
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

# Import bot_integration for API integration
from bot_integration import BotIntegration
bot_integration = BotIntegration()

# API bridge to Discord bot
@app.route('/api/bot/trials/<int:user_id>', methods=['GET'])
def get_user_trials_from_bot(user_id):
    # Check if the user is logged in and authorized
    if 'user_id' not in session or int(session['user_id']) != user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        trials = bot_integration.get_user_trials(user_id)
        return jsonify({'trials': trials})
    except Exception as e:
        logger.error(f"Error getting trials from bot: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/payments/<int:user_id>', methods=['GET'])
def get_user_payments_from_bot(user_id):
    # Check if the user is logged in and authorized
    if 'user_id' not in session or int(session['user_id']) != user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        payments = bot_integration.get_user_payments(user_id)
        return jsonify({'payments': payments})
    except Exception as e:
        logger.error(f"Error getting payments from bot: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/tier/<int:user_id>', methods=['GET'])
def get_user_tier_from_bot(user_id):
    # Check if the user is logged in and authorized
    if 'user_id' not in session or int(session['user_id']) != user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        tier = bot_integration.get_user_tier(user_id)
        return jsonify({'tier': tier})
    except Exception as e:
        logger.error(f"Error getting tier from bot: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/referrals/<int:user_id>', methods=['GET'])
def get_referral_stats_from_bot(user_id):
    # Check if the user is logged in and authorized
    if 'user_id' not in session or int(session['user_id']) != user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        stats = bot_integration.get_referral_stats(user_id)
        return jsonify({'referral_stats': stats})
    except Exception as e:
        logger.error(f"Error getting referral stats from bot: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-trial', methods=['POST'])
@subscription_required
def generate_trial():
    """Generate a trial for a service - requires active subscription"""
    data = request.get_json()
    service = data.get('service')
    trial_type = data.get('type', 'hit')
    automate = data.get('automate', False)
    
    if not service:
        return jsonify({'error': 'Service is required'}), 400
    
    try:
        # Get user info from session
        user_id = session['user_id']
        user = WebUser.query.get(user_id)
        
        # Get user's subscription tier for limits check
        from datetime import datetime
        now = datetime.utcnow()
        
        # Double-check subscription is active (belt and suspenders approach)
        if not user.subscription_tier or not user.subscription_expires_at or user.subscription_expires_at < now:
            return jsonify({
                'error': 'Subscription required',
                'message': 'You need an active subscription to generate trials',
                'redirect': '/subscriptions'
            }), 403
        
        # Check trial usage limits based on subscription tier
        # Import the database accessor
        from database import Database
        bot_db = Database()
        
        # Check if user has reached their daily limit
        usage_result = check_trial_usage_limits(user_id, user.subscription_tier, bot_db)
        if not usage_result['allowed']:
            return jsonify({
                'error': 'Daily limit reached',
                'message': usage_result['message'],
                'upgrade_url': '/subscriptions',
                'current_usage': usage_result['current_usage'],
                'limit': usage_result['limit']
            }), 429  # 429 Too Many Requests
        
        # Import the trial generator
        from utils.trial_generator import TrialGenerator
        generator = TrialGenerator()
        
        # Generate trial based on the service
        trial_info = asyncio.run(generator.generate_trial(service))
        
        # Track this usage in the database
        bot_db.track_usage(user_id, 'generate_trial')
        
        # Save the trial to the database
        try:
            # Create a new trial record
            trial = Trial(
                user_id=user_id,
                service=service,
                trial_type=trial_type,
                email=trial_info['user_info']['email'],
                password=trial_info['user_info']['password'],
                created_at=datetime.utcnow(),
                expires_at=datetime.fromisoformat(trial_info['trial_end_date']) if 'trial_end_date' in trial_info else None
            )
            db.session.add(trial)
            db.session.commit()
            logger.info(f"Trial saved to database: {trial.id} for user {user_id}")
        except Exception as e:
            logger.error(f"Error saving trial to database: {str(e)}")
            # Continue anyway since we have the trial info to return
        
        # Generate a random trial ID as fallback
        trial_id = random.randint(1000, 9999)
        
        # This variable will be defined if database save was successful
        saved_trial = locals().get('trial')
        
        # If we have a saved trial with an ID, use that instead
        if saved_trial is not None:
            try:
                if hasattr(saved_trial, 'id') and saved_trial.id:
                    trial_id = saved_trial.id
            except Exception as e:
                logger.debug(f"Using random trial ID due to error: {e}")
        
        return jsonify({
            'success': True,
            'trial': {
                'id': trial_id,
                'service': service,
                'type': trial_type,
                'automated': automate,
                'email': trial_info['user_info']['email'],
                'password': trial_info['user_info']['password'],
                'created_at': trial_info['generated_at'],
                'expires_at': trial_info['trial_end_date'],
                'subscription_tier': user.subscription_tier,
                'usage_count': usage_result['current_usage'] + 1,
                'daily_limit': usage_result['limit']
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
    signature = data.get('signature')
    
    if not reference:
        return jsonify({'error': 'Payment reference is required'}), 400
    
    try:
        # Import the payment processor
        from utils.payment_processor import PaymentProcessor
        
        # Verify the payment
        processor = PaymentProcessor()
        result = asyncio.run(processor.verify_payment(reference, signature))
        
        if result['status'] == 'confirmed':
            # Update the user's subscription tier
            user_id = session['user_id']
            user = WebUser.query.get(user_id)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
                
            # Get payment details to determine plan
            payment = result.get('payment', {})
            plan_id = payment.get('plan_id')
            
            # Set subscription dates - 30 days from now for expiration
            from datetime import datetime, timedelta
            now = datetime.utcnow()
            expiration_date = now + timedelta(days=30)
            
            # Update the user's subscription in the database
            user.subscription_tier = plan_id
            user.subscription_starts_at = now
            user.subscription_expires_at = expiration_date
            
            # Store the payment information
            user.last_payment_amount = payment.get('amount')
            user.last_payment_date = now
            user.last_payment_reference = reference
            
            db.session.commit()
            
            # Also update in the bot database if needed
            try:
                from database import Database
                bot_db = Database()
                bot_db.update_user_tier(user_id, plan_id, expiration_date.isoformat())
                logger.info(f"Updated subscription tier in bot database: {user_id} -> {plan_id}")
            except Exception as e:
                logger.error(f"Error updating tier in bot database: {str(e)}")
            
            # Return success with subscription details
            return jsonify({
                'success': True,
                'message': 'Payment verified successfully',
                'status': 'confirmed',
                'subscription': {
                    'tier': plan_id,
                    'starts_at': now.isoformat(),
                    'expires_at': expiration_date.isoformat()
                }
            })
        else:
            return jsonify({
                'success': False,
                'status': result['status'],
                'message': result['message']
            })
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Phantom Wallet API Endpoints
@app.route('/api/wallet/connect', methods=['POST'])
@app.route('/connect-wallet', methods=['POST'])
def connect_wallet():
    """Connect a Phantom wallet"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.json
        wallet_address = data.get('address')
        
        if not wallet_address:
            return jsonify({'error': 'Wallet address is required'}), 400
        
        # Store wallet connection in session
        user_id = session['user_id']
        wallet_sessions[user_id] = {
            'wallet_address': wallet_address,
            'connected_at': time.time()
        }
        
        # Update user record in database if we want to persist this
        user = WebUser.query.get(user_id)
        if user:
            user.wallet_address = wallet_address
            db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Wallet connected successfully',
            'address': wallet_address
        })
    except Exception as e:
        logger.error(f"Error connecting wallet: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/wallet/disconnect', methods=['POST'])
@app.route('/disconnect-wallet', methods=['POST'])
def disconnect_wallet():
    """Disconnect a Phantom wallet"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        user_id = session['user_id']
        
        # Remove wallet connection from session
        if user_id in wallet_sessions:
            del wallet_sessions[user_id]
        
        # Update user record in database if needed
        user = WebUser.query.get(user_id)
        if user and hasattr(user, 'wallet_address') and user.wallet_address:
            user.wallet_address = None
            db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Wallet disconnected successfully'
        })
    except Exception as e:
        logger.error(f"Error disconnecting wallet: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/wallet/status', methods=['GET'])
@app.route('/wallet-status', methods=['GET'])
def wallet_status():
    """Get wallet connection status"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        user_id = session['user_id']
        
        # Check if wallet is connected in session
        wallet_info = wallet_sessions.get(user_id)
        
        # If not in session, check database
        if not wallet_info:
            user = WebUser.query.get(user_id)
            if user and hasattr(user, 'wallet_address') and user.wallet_address:
                wallet_info = {
                    'wallet_address': user.wallet_address,
                    'connected_at': None  # We don't have this info from DB
                }
        
        if wallet_info:
            return jsonify({
                'status': 'success',
                'connected': True,
                'address': wallet_info['wallet_address']
            })
        else:
            return jsonify({
                'status': 'success',
                'connected': False
            })
    except Exception as e:
        logger.error(f"Error getting wallet status: {str(e)}")
        return jsonify({'error': str(e)}), 500
        
@app.route('/api/subscription/status', methods=['GET'])
def subscription_status():
    """Get subscription status for the current user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        user_id = session['user_id']
        status = check_subscription_status(user_id)
        
        return jsonify({
            'status': 'success',
            'subscription': status
        })
    except Exception as e:
        logger.error(f"Error getting subscription status: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Trial Junkie Web Application...")
    # Use the environment variable for PORT if available
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)