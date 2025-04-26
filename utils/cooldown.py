"""
Cooldown Management
Handles user cooldown periods
"""
import time
import logging
from config import COOLDOWNS

logger = logging.getLogger(__name__)

class Cooldown:
    """Class to manage user cooldowns"""
    
    def __init__(self):
        """Initialize the cooldown manager"""
        self.cooldowns = {}
        logger.info("Cooldown manager initialized")
    
    def set_cooldown(self, user_id, command, duration=None):
        """Set a cooldown for a user and command"""
        if duration is None:
            # Use default cooldown from config
            duration = COOLDOWNS.get(command, 60)
        
        end_time = time.time() + duration
        
        if user_id not in self.cooldowns:
            self.cooldowns[user_id] = {}
        
        self.cooldowns[user_id][command] = end_time
        logger.debug(f"Set cooldown for user {user_id}, command {command} for {duration} seconds")
    
    def is_on_cooldown(self, user_id, command):
        """Check if a user is on cooldown for a command"""
        if user_id not in self.cooldowns or command not in self.cooldowns[user_id]:
            return False
        
        end_time = self.cooldowns[user_id][command]
        is_cooling = time.time() < end_time
        
        if not is_cooling:
            # Cooldown has expired, remove it
            del self.cooldowns[user_id][command]
            if not self.cooldowns[user_id]:
                del self.cooldowns[user_id]
        
        return is_cooling
    
    def get_remaining_time(self, user_id, command):
        """Get the remaining cooldown time in seconds"""
        if not self.is_on_cooldown(user_id, command):
            return 0
        
        end_time = self.cooldowns[user_id][command]
        remaining = int(end_time - time.time())
        return max(0, remaining)
    
    def clear_cooldown(self, user_id, command=None):
        """Clear a cooldown for a user, optionally for a specific command"""
        if user_id not in self.cooldowns:
            return
        
        if command is None:
            # Clear all cooldowns for this user
            del self.cooldowns[user_id]
            logger.debug(f"Cleared all cooldowns for user {user_id}")
        elif command in self.cooldowns[user_id]:
            # Clear specific command cooldown
            del self.cooldowns[user_id][command]
            if not self.cooldowns[user_id]:
                del self.cooldowns[user_id]
            logger.debug(f"Cleared cooldown for user {user_id}, command {command}")
    
    def clear_all_cooldowns(self):
        """Clear all cooldowns for all users"""
        self.cooldowns = {}
        logger.debug("Cleared all cooldowns")
