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
        
        conn.close()
        return stats
