"""
Test suite for Discord bot commands
Tests all command functionality with mocked contexts
"""
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from discord.ext import commands

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from discord_bot_standalone import hit_command, dose_command, stash_command, agents_command
from database import Database

class MockContext:
    """Mock Discord context for testing"""
    def __init__(self, user_id="123456789012345678", username="TestUser"):
        self.author = MagicMock()
        self.author.id = user_id
        self.author.name = username
        self.send = AsyncMock()
        self.reply = AsyncMock()
        self.message = MagicMock()
        self.message.add_reaction = AsyncMock()
        self.bot = MagicMock()
        self.bot.get_channel = MagicMock(return_value=MagicMock())
        self.channel = MagicMock()
        self.channel.send = AsyncMock()

class BotCommandTests(unittest.TestCase):
    """Tests for bot commands"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock the database
        self.db_patcher = patch('discord_bot_standalone.Database')
        self.mock_db_class = self.db_patcher.start()
        self.mock_db = self.mock_db_class.return_value
        self.mock_db.user_exists.return_value = True
        self.mock_db.get_user_credentials.return_value = []
        self.mock_db.get_user_stats.return_value = {"commands": 10, "trials": 5, "first_seen": "2025-01-01"}
        
        # Create context
        self.ctx = MockContext()
        
    def tearDown(self):
        """Clean up after tests"""
        self.db_patcher.stop()
    
    async def test_hit_command(self):
        """Test the hit command"""
        await hit_command(self.ctx, service_or_url="netflix")
        self.ctx.send.assert_called_once()
        
    async def test_dose_command(self):
        """Test the dose command"""
        await dose_command(self.ctx, agent_type="identity", platform="any")
        self.ctx.send.assert_called_once()
        
    async def test_stash_command(self):
        """Test the stash command"""
        await stash_command(self.ctx)
        self.ctx.send.assert_called_once()
        
    async def test_agents_command(self):
        """Test the agents command"""
        await agents_command(self.ctx)
        self.ctx.send.assert_called_once()
        
if __name__ == "__main__":
    unittest.main()