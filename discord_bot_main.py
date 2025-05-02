#!/usr/bin/env python3
"""
Discord Bot for Trial Junkie

Main entry point for the Discord bot
"""
import os
import logging
import asyncio
import json
from datetime import datetime
import traceback

import discord
from discord.ext import commands

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("discord_bot.log")
    ]
)
logger = logging.getLogger("discord_bot")

# Set intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord"""
    logger.info(f"Bot is ready! Logged in as {bot.user.name} ({bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} guilds")
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="!help for commands"
        )
    )

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}. Use !help [command] for more info.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Invalid argument: {error}")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send(f"An error occurred: {str(error)}")

@bot.command(name="help")
async def help_command(ctx, command_name=None):
    """Display help information"""
    embed = discord.Embed(
        title="Trial Junkie Bot Help",
        description="Generate and manage trial accounts. Below are the available commands:",
        color=0x9b59b6  # Purple color
    )
    
    if command_name:
        # Get specific command help
        command = bot.get_command(command_name)
        if command:
            embed.add_field(name=f"!{command.name}", value=command.help or "No description available", inline=False)
        else:
            embed.add_field(name="Error", value=f"Command '{command_name}' not found", inline=False)
    else:
        # Get all commands
        embed.add_field(name="!hit [service/url]", value="Generate a trial for a specific service or URL", inline=False)
        embed.add_field(name="!stash", value="View your generated trials", inline=False)
        embed.add_field(name="!agents", value="Show information about the available agents", inline=False)
        embed.add_field(name="!plans", value="Show subscription plan information", inline=False)
        embed.add_field(name="!tier", value="Check your current subscription tier", inline=False)
        embed.add_field(name="!help [command]", value="Show this help message or get help for a specific command", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="agents")
async def agents_command(ctx):
    """Display information about all agents"""
    embed = discord.Embed(
        title="🤖 Trial Junkie Agents",
        description="Meet the specialized agents that power Trial Junkie:",
        color=0x9b59b6  # Purple color
    )
    
    embed.add_field(
        name="Personator 🧠",
        value="Generates realistic identities with names, addresses, and personal information.",
        inline=False
    )
    
    embed.add_field(
        name="Virtual Number 📱",
        value="Creates working phone numbers for verification steps.",
        inline=False
    )
    
    embed.add_field(
        name="Card Shark 💳",
        value="Produces valid credit card numbers that pass verification checks.",
        inline=False
    )
    
    embed.add_field(
        name="InboxForger 📧",
        value="Creates disposable email addresses for account registration.",
        inline=False
    )
    
    embed.add_field(
        name="ScraperNinja 🕸️",
        value="Extracts data from websites to find subscription details.",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name="plans")
async def plans_command(ctx):
    """Display subscription plans"""
    embed = discord.Embed(
        title="💰 Subscription Plans",
        description="Choose the plan that fits your needs:",
        color=0x9b59b6  # Purple color
    )
    
    embed.add_field(
        name="Basic Tier - $9.99/month",
        value="• Up to 2 trials per day\n• Access to basic services\n• Email support",
        inline=False
    )
    
    embed.add_field(
        name="Pro Tier - $19.99/month",
        value="• Up to 5 trials per day\n• Access to all popular services\n• Priority email support\n• Early access to new features",
        inline=False
    )
    
    embed.add_field(
        name="Premium Tier - $39.99/month",
        value="• Unlimited trials (up to 10 per day)\n• Access to all services, including premium ones\n• Priority 24/7 support\n• Custom trial generation\n• API access",
        inline=False
    )
    
    embed.set_footer(text="Visit trialjunkie.app/subscribe to upgrade your subscription")
    
    await ctx.send(embed=embed)

@bot.command(name="tier")
async def tier_command(ctx):
    """Display user's current subscription tier"""
    # For demonstration purposes, we'll use a hardcoded premium tier
    # In a real implementation, this would check the database
    
    embed = discord.Embed(
        title="🏆 Your Subscription",
        description="Here's your current subscription information:",
        color=0x9b59b6  # Purple color
    )
    
    embed.add_field(
        name="Current Tier",
        value="Premium",
        inline=True
    )
    
    embed.add_field(
        name="Status",
        value="Active",
        inline=True
    )
    
    embed.add_field(
        name="Next Billing Date",
        value="June 1, 2025",
        inline=True
    )
    
    embed.add_field(
        name="Daily Trial Limit",
        value="10/10 remaining",
        inline=True
    )
    
    embed.add_field(
        name="Member Since",
        value="May 1, 2025",
        inline=True
    )
    
    embed.set_footer(text="Visit trialjunkie.app/account to manage your subscription")
    
    await ctx.send(embed=embed)

def load_cogs():
    """Load all cogs"""
    # Make sure the commands directory exists
    os.makedirs("commands", exist_ok=True)
    
    try:
        # Load trial commands
        bot.load_extension("commands.trial_commands")
        logger.info("Loaded trial commands")
    except Exception as e:
        logger.error(f"Error loading trial commands: {e}")

def main():
    """Main function"""
    logger.info("Starting Discord bot")
    
    # Load Discord token from environment
    token = os.environ.get("DISCORD_BOT_TOKEN")
    
    if not token:
        logger.error("No Discord bot token found in environment variables")
        logger.info("For testing purposes, the bot will run with a dummy token")
        token = "dummy_token_for_testing"
        logger.info("Bot is running in simulation mode - no connection to Discord")
        load_cogs()
        
        # Print some simulated events
        logger.info("Simulating bot startup...")
        logger.info("Discord bot simulated and ready")
        logger.info("Commands available: !hit, !stash, !agents, !plans, !tier, !help")
        
        # Simulate some trial generation
        logger.info("You can test trial generation and stash commands via the Python API")
        return 0
    
    # Load cogs if we have a real token
    load_cogs()
    
    # Run the bot
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        logger.error("Invalid Discord bot token")
        return 1
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())