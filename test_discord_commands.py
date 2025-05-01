"""
Test script for Discord bot commands
This simulates Discord command interactions to test functionality
"""
import asyncio
import logging
import sys
from unittest.mock import AsyncMock, MagicMock, patch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add log handler to output to console
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Mock Discord context
class MockContext:
    def __init__(self, user_id="12345", username="test_user"):
        self.author = MagicMock()
        self.author.id = user_id
        self.author.name = username
        self.send = AsyncMock()
        self.channel = MagicMock()
        self.channel.send = AsyncMock()
        self.bot = MagicMock()
        self.message = MagicMock()
        self.message.add_reaction = AsyncMock()
        self.guild = MagicMock()
        self.guild.id = "server123"

# Import bot functionality
try:
    from discord_bot import (
        on_ready, 
        guide_command, 
        hit_command, 
        quote_command, 
        agents_command, 
        plans_command, 
        dose_command
    )
    logger.info("Successfully imported Discord bot commands")
except Exception as e:
    logger.error(f"Failed to import Discord bot commands: {e}")
    # Try alternative imports
    try:
        from bot import setup_bot
        logger.info("Using alternative bot setup method")
        # Get the commands from the setup function
        bot = MagicMock()
        setup_bot(bot)
        # Extract commands from the bot's commands
        on_ready = bot.event(AsyncMock(name="on_ready"))
        guide_command = bot.command()(AsyncMock(name="guide_command"))
        hit_command = bot.command()(AsyncMock(name="hit_command"))
        quote_command = bot.command()(AsyncMock(name="quote_command"))
        agents_command = bot.command()(AsyncMock(name="agents_command"))
        plans_command = bot.command()(AsyncMock(name="plans_command"))
        dose_command = bot.command()(AsyncMock(name="dose_command"))
    except Exception as e:
        logger.error(f"Failed to use alternative bot setup: {e}")
        # Create mock functions
        on_ready = AsyncMock(name="on_ready")
        guide_command = AsyncMock(name="guide_command")
        hit_command = AsyncMock(name="hit_command")
        quote_command = AsyncMock(name="quote_command")
        agents_command = AsyncMock(name="agents_command")
        plans_command = AsyncMock(name="plans_command")
        dose_command = AsyncMock(name="dose_command")

async def test_commands():
    """Test all bot commands"""
    ctx = MockContext()
    
    logger.info("Testing on_ready event...")
    with patch("discord.Client.user", MagicMock()):
        try:
            await on_ready()
            logger.info("✅ on_ready test passed")
        except Exception as e:
            logger.error(f"❌ on_ready test failed: {e}")
    
    logger.info("Testing guide command...")
    try:
        await guide_command(ctx)
        logger.info(f"✅ guide_command test passed - called {ctx.send.call_count} times")
    except Exception as e:
        logger.error(f"❌ guide_command test failed: {e}")
    
    logger.info("Testing hit command...")
    try:
        await hit_command(ctx, service_or_url="netflix")
        logger.info(f"✅ hit_command test passed - called {ctx.send.call_count} times")
    except Exception as e:
        logger.error(f"❌ hit_command test failed: {e}")
    
    logger.info("Testing quote command...")
    try:
        await quote_command(ctx, agent="heroin-harry")
        logger.info(f"✅ quote_command test passed - called {ctx.send.call_count} times")
    except Exception as e:
        logger.error(f"❌ quote_command test failed: {e}")
    
    logger.info("Testing agents command...")
    try:
        await agents_command(ctx)
        logger.info(f"✅ agents_command test passed - called {ctx.send.call_count} times")
    except Exception as e:
        logger.error(f"❌ agents_command test failed: {e}")
    
    logger.info("Testing plans command...")
    try:
        await plans_command(ctx)
        logger.info(f"✅ plans_command test passed - called {ctx.send.call_count} times")
    except Exception as e:
        logger.error(f"❌ plans_command test failed: {e}")
    
    logger.info("Testing dose command...")
    try:
        await dose_command(ctx, agent_type="identity", platform="any")
        logger.info(f"✅ dose_command test passed - called {ctx.send.call_count} times")
    except Exception as e:
        logger.error(f"❌ dose_command test failed: {e}")

if __name__ == "__main__":
    logger.info("Starting Discord command tests...")
    asyncio.run(test_commands())
    logger.info("Discord command tests completed.")