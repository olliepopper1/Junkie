"""
Database module for Trial Junkie
Handles database connections and operations
"""
import os
import sqlite3
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path=None):
        """Initialize the database connection"""
        if db_path is None:
            db_path = os.getenv("DATABASE_PATH", "trial_junkie.db")
        
        self.db_path = db_path
        self._initialize_db()
    
    def _get_connection(self):
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def _initialize_db(self):
        """Initialize the database with necessary tables"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            created_at TEXT,
            last_active TEXT
        )
        ''')
        
        # Create credentials table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            command TEXT,
            parameters TEXT,
            executed_at TEXT,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Database initialized successfully")

    def user_exists(self, user_id):
        """Check if a user exists in the database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone() is not None
        
        conn.close()
        return result
    
    def create_user(self, user_id, username):
        """Create a new user in the database"""
        if self.user_exists(user_id):
            return self.update_user_activity(user_id)
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO users (user_id, username, created_at, last_active) VALUES (?, ?, ?, ?)",
            (user_id, username, now, now)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Created user: {username} ({user_id})")
        return True
    
    def update_user_activity(self, user_id):
        """Update a user's last active timestamp"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute(
            "UPDATE users SET last_active = ? WHERE user_id = ?",
            (now, user_id)
        )
        
        conn.commit()
        conn.close()
        return True
    
    def log_command(self, user_id, command, parameters, status="success"):
        """Log a command execution"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO commands (user_id, command, parameters, executed_at, status) VALUES (?, ?, ?, ?, ?)",
            (user_id, command, parameters, now, status)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Command logged - User: {user_id}, Command: {command}, Status: {status}")
        return True
    
    def save_credential(self, user_id, service, credential_type, credential_value):
        """Save a generated credential"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # Convert dictionary values to JSON if needed
        if isinstance(credential_value, dict):
            credential_value = json.dumps(credential_value)
        
        cursor.execute(
            "INSERT INTO credentials (user_id, service, credential_type, credential_value, created_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, service, credential_type, credential_value, now)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved credential - User: {user_id}, Service: {service}, Type: {credential_type}")
        return True
    
    def get_user_credentials(self, user_id, service=None):
        """Get a user's credentials, optionally filtered by service"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM credentials WHERE user_id = ?"
        params = [user_id]
        
        if service:
            query += " AND service = ?"
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
        cursor = conn.cursor()
        
        # Delete user credentials
        cursor.execute("DELETE FROM credentials WHERE user_id = ?", (user_id,))
        
        # Don't delete the user or command history, just credentials
        
        conn.commit()
        conn.close()
        
        logger.info(f"Cleared credentials for user: {user_id}")
        return True
    
    def get_user_stats(self, user_id):
        """Get statistics about a user's activity"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Get basic user info
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            stats['username'] = user['username']
            stats['created_at'] = user['created_at']
            stats['last_active'] = user['last_active']
        
        # Count credentials by type
        cursor.execute(
            "SELECT credential_type, COUNT(*) as count FROM credentials WHERE user_id = ? GROUP BY credential_type",
            (user_id,)
        )
        cred_counts = cursor.fetchall()
        stats['credentials'] = {row['credential_type']: row['count'] for row in cred_counts}
        
        # Count total credentials
        cursor.execute("SELECT COUNT(*) as count FROM credentials WHERE user_id = ?", (user_id,))
        stats['total_credentials'] = cursor.fetchone()['count']
        
        # Count commands
        cursor.execute(
            "SELECT command, COUNT(*) as count FROM commands WHERE user_id = ? GROUP BY command",
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
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # Check if payments table exists, create if not
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            reference TEXT UNIQUE,
            amount REAL,
            service_type TEXT,
            status TEXT,
            tx_signature TEXT,
            created_at TEXT,
            completed_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        cursor.execute(
            "INSERT INTO payments (user_id, reference, amount, service_type, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, reference, amount, service_type, 'pending', now)
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved payment request - User: {user_id}, Reference: {reference}, Amount: {amount}")
        return True
    
    def update_payment_status(self, reference, status, tx_signature=None):
        """Update a payment status"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        if status == 'completed' and tx_signature:
            cursor.execute(
                "UPDATE payments SET status = ?, tx_signature = ?, completed_at = ? WHERE reference = ?",
                (status, tx_signature, now, reference)
            )
        else:
            cursor.execute(
                "UPDATE payments SET status = ? WHERE reference = ?",
                (status, reference)
            )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Updated payment status - Reference: {reference}, Status: {status}")
        return True
    
    def get_payment_by_reference(self, reference):
        """Get a payment by reference"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM payments WHERE reference = ?", (reference,))
        payment = cursor.fetchone()
        
        conn.close()
        
        if not payment:
            return None
        
        return dict(payment)
    
    def get_user_payments(self, user_id, status=None):
        """Get payments for a user, optionally filtered by status"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM payments WHERE user_id = ?"
        params = [user_id]
        
        if status:
            query += " AND status = ?"
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
        cursor = conn.cursor()
        
        # Make sure users table has tier and membership_expires columns
        try:
            cursor.execute("SELECT tier FROM users LIMIT 1")
        except sqlite3.OperationalError:
            # Add tier column if it doesn't exist
            cursor.execute("ALTER TABLE users ADD COLUMN tier TEXT DEFAULT 'free'")
            cursor.execute("ALTER TABLE users ADD COLUMN membership_expires TEXT")
            conn.commit()
        
        if expires_at:
            cursor.execute(
                "UPDATE users SET tier = ?, membership_expires = ? WHERE user_id = ?",
                (tier, expires_at, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET tier = ? WHERE user_id = ?",
                (tier, user_id)
            )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Updated user tier - User: {user_id}, Tier: {tier}")
        return True
        
    def get_user_tier(self, user_id):
        """Get a user's membership tier"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT tier, membership_expires FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
        except sqlite3.OperationalError:
            # If tier column doesn't exist, add it
            cursor.execute("ALTER TABLE users ADD COLUMN tier TEXT DEFAULT 'free'")
            cursor.execute("ALTER TABLE users ADD COLUMN membership_expires TEXT")
            conn.commit()
            result = {'tier': 'free', 'membership_expires': None}
        
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
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Create table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_limits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            command TEXT,
            date TEXT,
            count INTEGER DEFAULT 0,
            UNIQUE(user_id, command, date)
        )
        ''')
        
        # Try to update existing record
        cursor.execute(
            "UPDATE usage_limits SET count = count + 1 WHERE user_id = ? AND command = ? AND date = ?",
            (user_id, command, today)
        )
        
        # If no record was updated, insert new record
        if cursor.rowcount == 0:
            cursor.execute(
                "INSERT INTO usage_limits (user_id, command, date, count) VALUES (?, ?, ?, 1)",
                (user_id, command, today)
            )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Tracked usage - User: {user_id}, Command: {command}, Date: {today}")
        return True
        
    def get_usage_count(self, user_id, command=None):
        """Get usage count for today"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Create table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_limits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            command TEXT,
            date TEXT,
            count INTEGER DEFAULT 0,
            UNIQUE(user_id, command, date)
        )
        ''')
        
        if command:
            cursor.execute(
                "SELECT count FROM usage_limits WHERE user_id = ? AND command = ? AND date = ?",
                (user_id, command, today)
            )
            result = cursor.fetchone()
            count = result['count'] if result else 0
        else:
            cursor.execute(
                "SELECT SUM(count) as total FROM usage_limits WHERE user_id = ? AND date = ?",
                (user_id, today)
            )
            result = cursor.fetchone()
            count = result['total'] if result and result['total'] else 0
        
        conn.close()
        return count
