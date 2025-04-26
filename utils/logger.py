"""
Logging utilities
Handles logging and command tracking
"""
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class CommandLogger:
    """Class to log command usage"""
    
    def __init__(self):
        """Initialize the command logger"""
        self.commands = []
        self.start_time = time.time()
        logger.info("Command logger initialized")
    
    def log_command(self, user_id, username, command, parameters):
        """Log a command execution"""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "user_id": user_id,
            "username": username,
            "command": command,
            "parameters": parameters,
            "timestamp": timestamp
        }
        
        self.commands.append(log_entry)
        
        # Log to the application logger as well
        logger.info(f"Command executed - User: {username} ({user_id}), Command: {command}, Params: {parameters}")
        
        return log_entry
    
    def get_command_history(self, user_id=None, limit=10):
        """Get command history, optionally filtered by user"""
        if user_id:
            # Filter by user ID
            history = [cmd for cmd in self.commands if cmd["user_id"] == user_id]
        else:
            # All commands
            history = self.commands.copy()
        
        # Return the most recent commands up to the limit
        return sorted(history, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_popular_commands(self, limit=5):
        """Get the most popular commands"""
        command_counts = {}
        
        for cmd in self.commands:
            command = cmd["command"]
            if command not in command_counts:
                command_counts[command] = 0
            command_counts[command] += 1
        
        # Sort by count and return top commands
        sorted_commands = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_commands[:limit]
    
    def get_active_users(self, limit=5):
        """Get the most active users"""
        user_counts = {}
        
        for cmd in self.commands:
            user_id = cmd["user_id"]
            username = cmd["username"]
            
            if user_id not in user_counts:
                user_counts[user_id] = {"username": username, "count": 0}
            
            user_counts[user_id]["count"] += 1
        
        # Sort by count and return top users
        sorted_users = sorted(user_counts.values(), key=lambda x: x["count"], reverse=True)
        return sorted_users[:limit]
    
    def get_stats(self):
        """Get usage statistics"""
        uptime = time.time() - self.start_time
        uptime_hours = uptime / 3600
        
        total_commands = len(self.commands)
        unique_users = len(set(cmd["user_id"] for cmd in self.commands))
        
        # Commands per hour rate
        commands_per_hour = total_commands / uptime_hours if uptime_hours > 0 else 0
        
        return {
            "uptime_seconds": uptime,
            "uptime_hours": uptime_hours,
            "total_commands": total_commands,
            "unique_users": unique_users,
            "commands_per_hour": commands_per_hour,
            "popular_commands": self.get_popular_commands(),
            "active_users": self.get_active_users()
        }
