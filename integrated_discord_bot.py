#!/usr/bin/env python3
"""
Integrated Discord Bot for Trial Junkie
Integrates all components of the Trial Junkie system into a Discord bot interface
"""
import os
import sys
import json
import logging
import asyncio
import traceback
from datetime import datetime, timedelta
import random
import string
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("integrated_discord_bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("integrated_discord_bot")

# Initialize the Trial Junkie system
try:
    from trial_junkie_system import TrialJunkieSystem
    system = TrialJunkieSystem()
    SYSTEM_AVAILABLE = True
    logger.info("Trial Junkie system initialized successfully")
except ImportError:
    logger.error("Trial Junkie system module not available")
    SYSTEM_AVAILABLE = False
    system = None
except Exception as e:
    logger.error(f"Error initializing Trial Junkie system: {str(e)}")
    SYSTEM_AVAILABLE = False
    system = None

# Try to import Discord libraries
try:
    import discord
    from discord import app_commands
    from discord.ext import commands
    
    DISCORD_AVAILABLE = True
    logger.info("Discord libraries loaded successfully")
except ImportError:
    logger.error("Discord libraries not available")
    DISCORD_AVAILABLE = False

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logger.warning("dotenv module not available - environment variables may not be loaded")

# Discord bot configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    SIMULATION_MODE = True
    logger.info("Bot running in simulation mode (no actual Discord connection)")
else:
    SIMULATION_MODE = False

# Supported services
SUPPORTED_SERVICES = [
    "hulu",
    "netflix",
    "disney+",
    "spotify",
    "apple music",
    "youtube premium",
    "hbo max"
]

class IntegratedBot:
    """
    Integrated Discord bot for Trial Junkie
    """
    def __init__(self):
        """Initialize the bot"""
        self.system = system
        
        if not DISCORD_AVAILABLE:
            logger.error("Discord libraries not available - bot cannot be initialized")
            return
        
        # Initialize Discord bot
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        # Register event handlers
        self.bot.event(self.on_ready)
        
        # Register commands manually
        @self.bot.command(name="hit")
        async def hit(ctx, *, service_or_url: str = None):
            await self.hit_command(ctx, service_or_url=service_or_url)
            
        @self.bot.command(name="stash")
        async def stash(ctx):
            await self.stash_command(ctx)
            
        @self.bot.command(name="helpme")
        async def help_cmd(ctx):
            await self.help_command(ctx)
        
        logger.info("Integrated Discord bot initialized")
    
    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f"Logged in as {self.bot.user.name} (ID: {self.bot.user.id})")
        logger.info(f"Connected to {len(self.bot.guilds)} guilds")
        
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, 
                name="for !help commands"
            )
        )
        
        logger.info("Bot is ready")
    
    async def hit_command(self, ctx, *, service_or_url: str = None):
        """
        Generate a trial for a service
        
        Args:
            ctx: Command context
            service_or_url: Service name or URL to generate trial for
        """
        # Check if system is available
        if not SYSTEM_AVAILABLE or not self.system:
            await ctx.send("❌ Trial Junkie system is currently unavailable")
            return
        
        # Check service
        if not service_or_url:
            await ctx.send(
                f"Please specify a service. Example: `!hit hulu`\n"
                f"Supported services: {', '.join(SUPPORTED_SERVICES)}"
            )
            return
        
        service = service_or_url.lower()
        
        if service not in SUPPORTED_SERVICES and not service.startswith(('http://', 'https://')):
            await ctx.send(
                f"Sorry, {service} is not supported yet. Supported services: {', '.join(SUPPORTED_SERVICES)}"
            )
            return
        
        # Send acknowledegment
        await ctx.send(f"🧪 Generating your {service} trial... This may take a minute.")
        
        try:
            # Show typing indicator
            async with ctx.typing():
                # Generate trial
                result = self.system.generate_trial(
                    service=service,
                    discord_id=str(ctx.author.id)
                )
                
                if result.get("success", False):
                    trial_data = result.get("trial_data", {})
                    
                    # Format the message for Discord
                    embed = self._format_trial_embed(trial_data)
                    
                    # Send via DM
                    try:
                        await ctx.author.send(embed=embed)
                        await ctx.send(f"✅ Your {service} trial has been sent to your DMs!")
                    except discord.Forbidden:
                        await ctx.send(
                            "⚠️ I couldn't send you a DM. Please enable DMs from server members."
                        )
                        await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ Trial generation failed: {result.get('message')}")
        
        except Exception as e:
            logger.error(f"Error in hit command: {str(e)}")
            traceback.print_exc()
            await ctx.send(f"❌ An error occurred: {str(e)}")
    
    async def stash_command(self, ctx):
        """View user's generated trials"""
        # Check if system is available
        if not SYSTEM_AVAILABLE or not self.system:
            await ctx.send("❌ Trial Junkie system is currently unavailable")
            return
        
        try:
            # For demonstration purposes, we'll create a user if they don't exist
            user_result = self.system.create_user(
                discord_id=str(ctx.author.id),
                username=ctx.author.name
            )
            
            if user_result.get("success", False):
                user_id = user_result.get("user_id")
                
                # Get user trials
                trials_result = self.system.get_user_trials(user_id)
                
                if not trials_result.get("success", False):
                    await ctx.send(f"❌ Error retrieving trials: {trials_result.get('message')}")
                    return
                
                trials = trials_result.get("trials", [])
                
                if not trials:
                    await ctx.send("You don't have any trials yet. Use `!hit <service>` to generate one!")
                    return
                
                # Create an embed to display trials
                embed = discord.Embed(
                    title="Your Trial Stash",
                    description=f"You have {len(trials)} trials:",
                    color=0x9370DB
                )
                
                # Add each trial to the embed
                for i, trial in enumerate(trials[:10], 1):  # Limit to 10 trials
                    service = trial.get("service", "Unknown").title()
                    
                    # Determine if trial is active or expired
                    end_date_str = trial.get("end_date")
                    if end_date_str:
                        try:
                            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                            status = "Active" if end_date > datetime.now() else "Expired"
                        except ValueError:
                            status = "Unknown"
                    else:
                        status = "Unknown"
                    
                    # Add field for this trial
                    embed.add_field(
                        name=f"{i}. {service}",
                        value=(
                            f"**Email:** {trial.get('email', 'N/A')}\n"
                            f"**Expires:** {trial.get('end_date', 'Unknown')}\n"
                            f"**Status:** {status}"
                        ),
                        inline=True
                    )
                
                # Add a note if there are more than 10 trials
                if len(trials) > 10:
                    embed.set_footer(text=f"And {len(trials) - 10} more trials not shown.")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Error retrieving user: {user_result.get('message')}")
        
        except Exception as e:
            logger.error(f"Error in stash command: {str(e)}")
            traceback.print_exc()
            await ctx.send(f"❌ An error occurred: {str(e)}")
    
    async def help_command(self, ctx):
        """Show help information"""
        embed = discord.Embed(
            title="Trial Junkie Bot Help",
            description="Generate free trials with a single command",
            color=0x9370DB
        )
        
        embed.add_field(
            name="!hit <service>",
            value="Generate a trial for a specific service",
            inline=False
        )
        
        embed.add_field(
            name="!stash",
            value="View your generated trials",
            inline=False
        )
        
        embed.add_field(
            name="Supported Services",
            value=', '.join(SUPPORTED_SERVICES),
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    def _format_trial_embed(self, trial_data: Dict[str, Any]) -> discord.Embed:
        """Format trial data as a Discord embed"""
        service = trial_data.get("service", "Unknown").title()
        plan = trial_data.get("plan", "Basic")
        
        # Create embed
        embed = discord.Embed(
            title=f"{service} Trial Account",
            description=f"Your {service} trial is ready! Here are your login details:",
            color=0x9370DB
        )
        
        # Add basic fields
        embed.add_field(name="Service", value=service, inline=True)
        embed.add_field(name="Plan", value=plan, inline=True)
        
        # Add expiry date
        end_date = trial_data.get("end_date", "Unknown")
        embed.add_field(name="Valid Until", value=end_date, inline=True)
        
        # Add login information
        embed.add_field(
            name="Login Information",
            value=(
                f"**Email:** {trial_data.get('email', 'N/A')}\n"
                f"**Password:** {trial_data.get('password', 'N/A')}"
            ),
            inline=False
        )
        
        # Add personal information
        embed.add_field(
            name="Personal Info",
            value=(
                f"**Name:** {trial_data.get('first_name', 'N/A')} {trial_data.get('last_name', 'N/A')}\n"
                f"**Phone:** {trial_data.get('phone', 'N/A')}"
            ),
            inline=False
        )
        
        # Add payment information
        card_details = trial_data.get("card_details", {})
        if card_details:
            embed.add_field(
                name="Payment Method",
                value=(
                    f"**Card Type:** {card_details.get('type', 'N/A').upper()}\n"
                    f"**Last 4:** {card_details.get('last4', 'N/A')}"
                ),
                inline=False
            )
        
        # Add footer
        embed.set_footer(text="Remember to cancel before the trial ends to avoid charges.")
        
        return embed
    
    def run(self):
        """Run the bot"""
        if SIMULATION_MODE:
            logger.info("Bot is running in simulation mode (no actual Discord connection)")
            logger.info("Available commands: !hit, !stash, !help")
            
            # Simulate bot commands
            class SimulatedContext:
                def __init__(self, author_id="123456789", author_name="SimulatedUser"):
                    self.author = type('obj', (object,), {
                        'id': author_id,
                        'name': author_name,
                        'send': lambda embed=None, **kwargs: logger.info(f"DM sent to user: {embed}")
                    })
                
                async def send(self, content=None, embed=None, **kwargs):
                    if content:
                        logger.info(f"Message: {content}")
                    if embed:
                        logger.info(f"Embed: {embed.title}")
                
                async def typing(self):
                    class TypingContextManager:
                        async def __aenter__(self):
                            return None
                        
                        async def __aexit__(self, exc_type, exc_val, exc_tb):
                            return None
                    
                    return TypingContextManager()
            
            # Test hit command
            async def test_hit():
                ctx = SimulatedContext()
                await self.hit_command(ctx, service_or_url="hulu")
            
            # Test stash command
            async def test_stash():
                ctx = SimulatedContext()
                await self.stash_command(ctx)
            
            # Test help command
            async def test_help():
                ctx = SimulatedContext()
                await self.help_command(ctx)
            
            # Run test functions
            asyncio.run(test_hit())
            asyncio.run(test_stash())
            asyncio.run(test_help())
            
            return True
        elif DISCORD_AVAILABLE and DISCORD_BOT_TOKEN:
            logger.info("Starting Discord bot")
            self.bot.run(DISCORD_BOT_TOKEN)
            return True
        else:
            logger.error("Cannot start bot - missing required components")
            return False

# Create and run the bot if this file is executed directly
if __name__ == "__main__":
    bot = IntegratedBot()
    bot.run()