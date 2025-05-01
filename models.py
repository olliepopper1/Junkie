"""
Trial Junkie - Database Models
Models for the Trial Junkie platform
"""
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

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
    wallet_address = db.Column(db.String(256), nullable=True)  # Phantom wallet address
    referral_code = db.Column(db.String(20), unique=True, nullable=True)
    referred_by_id = db.Column(db.Integer, db.ForeignKey('web_user.id'), nullable=True)
    referral_count = db.Column(db.Integer, default=0)
    reset_password_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_password_expires = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Self-referential relationship for referrals
    referred_by = db.relationship('WebUser', remote_side=[id], backref=db.backref('referrals', lazy='dynamic'))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return self.password_hash and check_password_hash(self.password_hash, password)
        
    def generate_reset_token(self):
        """Generate a secure token for password reset"""
        import secrets
        import string
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))
        self.reset_password_token = token
        # Token expires after 24 hours
        self.reset_password_expires = datetime.utcnow() + timedelta(hours=24)
        return token
    
    def verify_reset_token(self, token):
        """Verify if a reset token is valid"""
        if self.reset_password_token != token:
            return False
        if datetime.utcnow() > self.reset_password_expires:
            return False
        return True
        
    def clear_reset_token(self):
        """Clear the reset token after use"""
        self.reset_password_token = None
        self.reset_password_expires = None

class Trial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('web_user.id'), nullable=False)
    service = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    card_number = db.Column(db.String(20), nullable=True)
    card_expiry = db.Column(db.String(10), nullable=True)
    card_cvv = db.Column(db.String(5), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='active')
    
    # Relationship with user
    user = db.relationship('WebUser', backref=db.backref('trials', lazy='dynamic'))

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('web_user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    service_type = db.Column(db.String(50), nullable=False)
    reference = db.Column(db.String(100), unique=True, nullable=False)
    tx_signature = db.Column(db.String(100), unique=True, nullable=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with user
    user = db.relationship('WebUser', backref=db.backref('payments', lazy='dynamic'))

class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('web_user.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('web_user.id'), nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    referrer = db.relationship('WebUser', foreign_keys=[referrer_id], backref=db.backref('referrals_made', lazy='dynamic'))
    referred = db.relationship('WebUser', foreign_keys=[referred_id], backref=db.backref('referral_source', uselist=False))

class Commission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('web_user.id'), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    referrer = db.relationship('WebUser', backref=db.backref('commissions', lazy='dynamic'))
    payment = db.relationship('Payment', backref=db.backref('commissions', lazy='dynamic'))

class UserTier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('web_user.id'), nullable=False, unique=True)
    tier = db.Column(db.String(20), default='free')
    starts_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    # Relationship with user
    user = db.relationship('WebUser', backref=db.backref('tier', uselist=False))