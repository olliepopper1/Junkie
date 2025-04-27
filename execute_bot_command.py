#!/usr/bin/env python
"""
Execute Bot Command
Bridge script to execute Discord bot commands from the web API
"""
import os
import sys
import json
import argparse
import logging
from bot import setup_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("execute_bot_command.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MockContext:
    """Mock Discord context for executing commands"""
    def __init__(self, user_id, username, command, args):
        self.author = MockUser(user_id, username)
        self.command = command
        self.args = args
        self.message = MockMessage(user_id, username, command, args)
        self.bot = None
        self.sent_messages = []
    
    async def send(self, content=None, embed=None, file=None):
        """Mock send method to capture responses"""
        self.sent_messages.append({
            "content": content,
            "embed": embed.to_dict() if embed else None,
        })
        return MockMessage(None, "bot", content, "")
    
    async def reply(self, content=None, embed=None, file=None):
        """Mock reply method"""
        return await self.send(content, embed, file)

class MockUser:
    """Mock Discord user"""
    def __init__(self, user_id, username):
        self.id = user_id
        self.name = username
        self.display_name = username
        self.bot = False
        self.discriminator = "0000"

class MockMessage:
    """Mock Discord message"""
    def __init__(self, user_id, username, content, args):
        self.author = MockUser(user_id, username)
        self.content = content
        self.args = args
        self.channel = MockChannel()
        
    async def add_reaction(self, emoji):
        """Mock add_reaction method"""
        return True

class MockChannel:
    """Mock Discord channel"""
    def __init__(self):
        self.id = 123456789
        self.name = "web-command"
        
    async def send(self, content=None, embed=None, file=None):
        """Mock send method"""
        return MockMessage(None, "bot", content, "")

async def execute_command(user_id, username, command_name, args):
    """Execute a bot command with the given arguments"""
    try:
        # Set up the bot
        bot = setup_bot()
        
        # Find the command
        command = bot.get_command(command_name)
        if not command:
            return {
                "success": False,
                "error": f"Command '{command_name}' not found"
            }
        
        # Create a mock context
        ctx = MockContext(user_id, username, command_name, args)
        ctx.bot = bot
        
        # Execute the command
        await command(ctx, *args)
        
        # Return the command output
        return {
            "success": True,
            "responses": ctx.sent_messages
        }
    except Exception as e:
        logger.error(f"Error executing command: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Execute a bot command')
    parser.add_argument('--user_id', required=True, help='User ID')
    parser.add_argument('--username', required=True, help='Username')
    parser.add_argument('--command', required=True, help='Command name')
    parser.add_argument('--args', required=False, default="[]", help='Command arguments (JSON array)')
    
    args = parser.parse_args()
    
    # Parse the command arguments
    try:
        command_args = json.loads(args.args)
    except json.JSONDecodeError:
        command_args = []
    
    # Execute the command and handle asyncio
    import asyncio
    result = asyncio.run(execute_command(args.user_id, args.username, args.command, command_args))
    
    # Output as JSON
    print(json.dumps(result))
    return 0

if __name__ == "__main__":
    sys.exit(main())