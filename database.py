"""
Database module for Trial Junkie
Handles database connections and operations
"""
import os
import json
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_url=None):
        """Initialize the database connection"""
        if db_url is None:
            db_url = os.getenv("DATABASE_URL")
        
        self.db_url = db_url
        self._initialize_db()
    
    def _get_connection(self):
        """Get a database connection"""
        conn = psycopg2.connect(self.db_url)
        return conn
    
    def _get_cursor(self, conn):
        """Get a database cursor that returns dictionaries"""
        return conn.cursor(cursor_factory=RealDictCursor)
    
    def _initialize_db(self):
        """Initialize the database with necessary tables"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            created_at TEXT,
            last_active TEXT,
            tier TEXT DEFAULT 'free',
            membership_expires TEXT
        )
        ''')
        
        # Create credentials table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id SERIAL PRIMARY KEY,
            user_id TEXT,
            service TEXT,
            credential_type TEXT,
            credential_value TEXT,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        # Create commands table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS commands (
            id SERIAL PRIMARY KEY,
            user_id TEXT,
            command TEXT,
            parameters TEXT,
            executed_at TEXT,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        # Create payments table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id SERIAL PRIMARY KEY,
            user_id TEXT,
            reference TEXT UNIQUE,
            amount REAL,
            service_type TEXT,
            status TEXT DEFAULT 'pending',
            tx_signature TEXT,
            created_at TEXT,
            completed_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        # Create usage_limits table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_limits (
            id SERIAL PRIMARY KEY,
            user_id TEXT,
            command TEXT,
            date TEXT,
            count INTEGER DEFAULT 0,
            UNIQUE(user_id, command, date),
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        # Create referrals table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            id SERIAL PRIMARY KEY,
            referrer_id TEXT,
            referred_id TEXT,
            referral_code TEXT UNIQUE,
            status TEXT DEFAULT 'pending',
            created_at TEXT,
            confirmed_at TEXT,
            FOREIGN KEY (referrer_id) REFERENCES users (user_id),
            FOREIGN KEY (referred_id) REFERENCES users (user_id)
        )
        ''')
        
        # Create commissions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS commissions (
            id SERIAL PRIMARY KEY,
            referrer_id TEXT,
            referred_id TEXT,
            payment_id INTEGER,
            amount REAL,
            percentage REAL,
            status TEXT DEFAULT 'pending',
            created_at TEXT,
            paid_at TEXT,
            FOREIGN KEY (referrer_id) REFERENCES users (user_id),
            FOREIGN KEY (referred_id) REFERENCES users (user_id),
            FOREIGN KEY (payment_id) REFERENCES payments (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Database initialized successfully")

    def user_exists(self, user_id):
        """Check if a user exists in the database"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        cursor.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone() is not None
        
        conn.close()
        return result
    
    def create_user(self, user_id, username):
        """Create a new user in the database"""
        if self.user_exists(user_id):
            return self.update_user_activity(user_id)
        
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        now = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO users (user_id, username, created_at, last_active) VALUES (%s, %s, %s, %s)",
            (user_id, username, now, now)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Created user: {username} ({user_id})")
        return True
    
    def update_user_activity(self, user_id):
        """Update a user's last active timestamp"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        now = datetime.now().isoformat()
        cursor.execute(
            "UPDATE users SET last_active = %s WHERE user_id = %s",
            (now, user_id)
        )
        
        conn.commit()
        conn.close()
        return True
    
    def log_command(self, user_id, command, parameters, status="success"):
        """Log a command execution"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        now = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO commands (user_id, command, parameters, executed_at, status) VALUES (%s, %s, %s, %s, %s)",
            (user_id, command, parameters, now, status)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Command logged - User: {user_id}, Command: {command}, Status: {status}")
        return True
    
    def save_credential(self, user_id, service, credential_type, credential_value):
        """Save a generated credential"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        now = datetime.now().isoformat()
        
        # Convert dictionary values to JSON if needed
        if isinstance(credential_value, dict):
            credential_value = json.dumps(credential_value)
        
        cursor.execute(
            "INSERT INTO credentials (user_id, service, credential_type, credential_value, created_at) VALUES (%s, %s, %s, %s, %s)",
            (user_id, service, credential_type, credential_value, now)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved credential - User: {user_id}, Service: {service}, Type: {credential_type}")
        return True
    
    def get_user_credentials(self, user_id, service=None):
        """Get a user's credentials, optionally filtered by service"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        query = "SELECT * FROM credentials WHERE user_id = %s"
        params = [user_id]
        
        if service:
            query += " AND service = %s"
            params.append(service)
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            cred_value = row['credential_value']
            # Try to parse JSON values
            try:
                cred_value = json.loads(cred_value)
            except (json.JSONDecodeError, TypeError):
                pass
                
            result.append({
                'id': row['id'],
                'service': row['service'],
                'type': row['credential_type'],
                'value': cred_value,
                'created_at': row['created_at']
            })
        
        conn.close()
        return result
    
    def clear_user_data(self, user_id):
        """Clear all user data (for rehab command)"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        # Delete user credentials
        cursor.execute("DELETE FROM credentials WHERE user_id = %s", (user_id,))
        
        # Don't delete the user or command history, just credentials
        
        conn.commit()
        conn.close()
        
        logger.info(f"Cleared credentials for user: {user_id}")
        return True
    
    def get_user_stats(self, user_id):
        """Get statistics about a user's activity"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        stats = {}
        
        # Get basic user info
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            stats['username'] = user['username']
            stats['created_at'] = user['created_at']
            stats['last_active'] = user['last_active']
        
        # Count credentials by type
        cursor.execute(
            "SELECT credential_type, COUNT(*) as count FROM credentials WHERE user_id = %s GROUP BY credential_type",
            (user_id,)
        )
        cred_counts = cursor.fetchall()
        stats['credentials'] = {row['credential_type']: row['count'] for row in cred_counts}
        
        # Count total credentials
        cursor.execute("SELECT COUNT(*) as count FROM credentials WHERE user_id = %s", (user_id,))
        stats['total_credentials'] = cursor.fetchone()['count'] if cursor.fetchone() else 0
        
        # Count commands
        cursor.execute(
            "SELECT command, COUNT(*) as count FROM commands WHERE user_id = %s GROUP BY command",
            (user_id,)
        )
        cmd_counts = cursor.fetchall()
        stats['commands'] = {row['command']: row['count'] for row in cmd_counts}
        
        # Get hit, dose, and trip counts
        stats['hit_count'] = stats['commands'].get('hit', 0)
        stats['dose_count'] = stats['commands'].get('dose', 0)
        stats['trip_count'] = stats['commands'].get('trip', 0)
        
        conn.close()
        return stats
        
    def save_payment_request(self, user_id, amount, reference, service_type):
        """Save a payment request"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        now = datetime.now().isoformat()
        
        cursor.execute(
            "INSERT INTO payments (user_id, reference, amount, service_type, status, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, reference, amount, service_type, 'pending', now)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved payment request - User: {user_id}, Reference: {reference}, Amount: {amount}")
        return True
    
    def update_payment_status(self, reference, status, tx_signature=None):
        """Update a payment status"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        now = datetime.now().isoformat()
        
        if status == 'completed' and tx_signature:
            cursor.execute(
                "UPDATE payments SET status = %s, tx_signature = %s, completed_at = %s WHERE reference = %s",
                (status, tx_signature, now, reference)
            )
        else:
            cursor.execute(
                "UPDATE payments SET status = %s WHERE reference = %s",
                (status, reference)
            )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Updated payment status - Reference: {reference}, Status: {status}")
        return True
    
    def get_payment_by_reference(self, reference):
        """Get a payment by reference"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        cursor.execute("SELECT * FROM payments WHERE reference = %s", (reference,))
        payment = cursor.fetchone()
        
        conn.close()
        
        if not payment:
            return None
        
        return dict(payment)
    
    def get_user_payments(self, user_id, status=None):
        """Get payments for a user, optionally filtered by status"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        query = "SELECT * FROM payments WHERE user_id = %s"
        params = [user_id]
        
        if status:
            query += " AND status = %s"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        result = [dict(row) for row in rows]
        
        conn.close()
        return result
        
    def update_user_tier(self, user_id, tier, expires_at=None):
        """Update a user's membership tier"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        if expires_at:
            cursor.execute(
                "UPDATE users SET tier = %s, membership_expires = %s WHERE user_id = %s",
                (tier, expires_at, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET tier = %s WHERE user_id = %s",
                (tier, user_id)
            )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Updated user tier - User: {user_id}, Tier: {tier}")
        return True
        
    def get_user_tier(self, user_id):
        """Get a user's membership tier"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        cursor.execute("SELECT tier, membership_expires FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if not result:
            return {'tier': 'free', 'membership_expires': None}
        
        tier_info = dict(result)
        
        # Check if premium membership has expired
        if tier_info['tier'] == 'premium' and tier_info['membership_expires']:
            try:
                expires = datetime.fromisoformat(tier_info['membership_expires'])
                if expires < datetime.now():
                    # Membership has expired, update in database
                    self.update_user_tier(user_id, 'free')
                    return {'tier': 'free', 'membership_expires': None}
            except (ValueError, TypeError):
                pass
        
        return tier_info
        
    def track_usage(self, user_id, command):
        """Track command usage for daily limits"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Try to update existing record
            cursor.execute(
                "UPDATE usage_limits SET count = count + 1 WHERE user_id = %s AND command = %s AND date = %s",
                (user_id, command, today)
            )
            
            # If no record was updated, insert new record
            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO usage_limits (user_id, command, date, count) VALUES (%s, %s, %s, 1)",
                    (user_id, command, today)
                )
        except Exception as e:
            # Handle the case where the table might not exist yet
            logger.error(f"Error tracking usage: {e}")
            conn.rollback()
        
        conn.commit()
        conn.close()
        
        logger.info(f"Tracked usage - User: {user_id}, Command: {command}, Date: {today}")
        return True
        
    def get_usage_count(self, user_id, command=None):
        """Get usage count for today"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        try:
            if command:
                cursor.execute(
                    "SELECT count FROM usage_limits WHERE user_id = %s AND command = %s AND date = %s",
                    (user_id, command, today)
                )
                result = cursor.fetchone()
                count = result['count'] if result else 0
            else:
                cursor.execute(
                    "SELECT SUM(count) as total FROM usage_limits WHERE user_id = %s AND date = %s",
                    (user_id, today)
                )
                result = cursor.fetchone()
                count = result['total'] if result and result['total'] else 0
        except Exception as e:
            # Handle the case where the table might not exist yet
            logger.error(f"Error getting usage count: {e}")
            count = 0
        
        conn.close()
        return count
        
    # Referral system methods
    def create_referral_code(self, user_id):
        """Create a unique referral code for a user"""
        import uuid
        import base64
        
        # Generate a short, unique referral code based on the user ID and a random component
        unique_id = str(uuid.uuid4())[:8]  # First 8 chars of UUID
        code_base = f"{user_id}-{unique_id}"
        
        # Create a URL-safe code
        referral_code = base64.urlsafe_b64encode(code_base.encode()).decode()[:12]
        
        # Store the referral code
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        now = datetime.now().isoformat()
        
        try:
            # Check if user already has a referral code
            cursor.execute(
                "SELECT referral_code FROM referrals WHERE referrer_id = %s AND referred_id IS NULL",
                (user_id,)
            )
            existing_code = cursor.fetchone()
            
            if existing_code:
                # Return existing code
                conn.close()
                return existing_code['referral_code']
            
            # Create new referral code entry
            cursor.execute(
                "INSERT INTO referrals (referrer_id, referral_code, created_at) VALUES (%s, %s, %s)",
                (user_id, referral_code, now)
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"Created referral code - User: {user_id}, Code: {referral_code}")
            return referral_code
        except Exception as e:
            logger.error(f"Error creating referral code: {e}")
            conn.rollback()
            conn.close()
            return None
    
    def get_referral_code(self, user_id):
        """Get a user's referral code, generating one if needed"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        try:
            cursor.execute(
                "SELECT referral_code FROM referrals WHERE referrer_id = %s AND referred_id IS NULL",
                (user_id,)
            )
            code = cursor.fetchone()
            
            conn.close()
            
            if code:
                return code['referral_code']
            else:
                # No code exists, generate one
                return self.create_referral_code(user_id)
        except Exception as e:
            logger.error(f"Error getting referral code: {e}")
            conn.close()
            return self.create_referral_code(user_id)
    
    def register_referral(self, referred_id, referral_code):
        """Register a user as referred by another user via referral code"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        try:
            # First verify the code exists and is unused
            cursor.execute(
                "SELECT id, referrer_id FROM referrals WHERE referral_code = %s AND referred_id IS NULL",
                (referral_code,)
            )
            referral = cursor.fetchone()
            
            if not referral:
                conn.close()
                return False, "Invalid or already used referral code"
            
            # Make sure user isn't referring themselves
            if referral['referrer_id'] == referred_id:
                conn.close()
                return False, "You can't refer yourself"
            
            # Check if user is already referred
            cursor.execute(
                "SELECT 1 FROM referrals WHERE referred_id = %s AND status = 'active'",
                (referred_id,)
            )
            if cursor.fetchone():
                conn.close()
                return False, "User is already referred by someone else"
            
            # Create a new referral entry linking to the code's owner
            now = datetime.now().isoformat()
            
            cursor.execute(
                "UPDATE referrals SET referred_id = %s, status = 'active', confirmed_at = %s WHERE id = %s",
                (referred_id, now, referral['id'])
            )
            
            # Create a new empty code for the referred user to be able to refer others
            self.create_referral_code(referred_id)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Registered referral - Referrer: {referral['referrer_id']}, Referred: {referred_id}")
            return True, f"Successfully registered with referral code. Welcome to Trial Junkie!"
        except Exception as e:
            logger.error(f"Error registering referral: {e}")
            conn.rollback()
            conn.close()
            return False, f"Error processing referral: {str(e)}"
    
    def record_commission(self, payment_id, amount):
        """Record a commission when a referred user makes a payment"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        try:
            # Get payment details
            cursor.execute("SELECT user_id, amount, service_type FROM payments WHERE id = %s", (payment_id,))
            payment = cursor.fetchone()
            
            if not payment:
                conn.close()
                return False, "Payment not found"
            
            # Find the referrer (if any)
            cursor.execute(
                "SELECT referrer_id FROM referrals WHERE referred_id = %s AND status = 'active'",
                (payment['user_id'],)
            )
            referral = cursor.fetchone()
            
            if not referral:
                # No referrer found, no commission to record
                conn.close()
                return False, "No active referrer found for this user"
            
            # Calculate commission (10% of payment amount)
            commission_amount = round(float(amount) * 0.1, 4)  # 10% commission, rounded to 4 decimal places
            
            # Record the commission
            now = datetime.now().isoformat()
            
            cursor.execute(
                """
                INSERT INTO commissions 
                (referrer_id, referred_id, payment_id, amount, percentage, status, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (referral['referrer_id'], payment['user_id'], payment_id, commission_amount, 10.0, 'pending', now)
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"Recorded commission - Referrer: {referral['referrer_id']}, Amount: {commission_amount}")
            return True, f"Commission of {commission_amount} SOL recorded for payment"
        except Exception as e:
            logger.error(f"Error recording commission: {e}")
            conn.rollback()
            conn.close()
            return False, f"Error recording commission: {str(e)}"
    
    def get_user_referrals(self, user_id):
        """Get all users referred by a given user"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        try:
            cursor.execute(
                """
                SELECT r.referred_id, u.username, r.confirmed_at, r.status 
                FROM referrals r
                JOIN users u ON r.referred_id = u.user_id
                WHERE r.referrer_id = %s AND r.referred_id IS NOT NULL
                ORDER BY r.confirmed_at DESC
                """,
                (user_id,)
            )
            referrals = cursor.fetchall()
            
            conn.close()
            return [dict(r) for r in referrals]
        except Exception as e:
            logger.error(f"Error getting user referrals: {e}")
            conn.close()
            return []
    
    def get_user_commissions(self, user_id, status=None):
        """Get all commissions for a user, optionally filtered by status"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        try:
            query = """
                SELECT c.*, u.username as referred_username
                FROM commissions c
                JOIN users u ON c.referred_id = u.user_id
                WHERE c.referrer_id = %s
            """
            params = [user_id]
            
            if status:
                query += " AND c.status = %s"
                params.append(status)
            
            query += " ORDER BY c.created_at DESC"
            
            cursor.execute(query, params)
            commissions = cursor.fetchall()
            
            conn.close()
            return [dict(c) for c in commissions]
        except Exception as e:
            logger.error(f"Error getting user commissions: {e}")
            conn.close()
            return []
    
    def get_total_commission(self, user_id):
        """Get the total commission amount for a user"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        try:
            cursor.execute(
                "SELECT SUM(amount) as total FROM commissions WHERE referrer_id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            
            conn.close()
            return result['total'] if result and result['total'] else 0.0
        except Exception as e:
            logger.error(f"Error getting total commission: {e}")
            conn.close()
            return 0.0
    
    def update_commission_status(self, commission_id, status, paid_at=None):
        """Update the status of a commission (e.g., mark as paid)"""
        conn = self._get_connection()
        cursor = self._get_cursor(conn)
        
        try:
            now = datetime.now().isoformat() if paid_at is None else paid_at
            
            if status == 'paid':
                cursor.execute(
                    "UPDATE commissions SET status = %s, paid_at = %s WHERE id = %s",
                    (status, now, commission_id)
                )
            else:
                cursor.execute(
                    "UPDATE commissions SET status = %s WHERE id = %s",
                    (status, commission_id)
                )
            
            conn.commit()
            conn.close()
            
            logger.info(f"Updated commission status - ID: {commission_id}, Status: {status}")
            return True
        except Exception as e:
            logger.error(f"Error updating commission status: {e}")
            conn.rollback()
            conn.close()
            return False
