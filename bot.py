"""
Discord Bot Implementation for Trial Junkie
Handles all Discord interactions and commands
"""
import os
import discord
from discord.ext import commands
import logging
import asyncio
import random
from datetime import datetime
from agents.pusher import Pusher
from utils.logger import CommandLogger
from utils.cooldown import Cooldown
from utils.response_templates import get_agent_quote, random_drug_emoji
from database import Database
from config import AGENT_NAMES, COLORS

logger = logging.getLogger(__name__)

def setup_bot():
    # Set up intents
    intents = discord.Intents.default()
    intents.message_content = True
    
    # Create the bot
    bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
    
    # Create database connection
    db = Database()
    
    # Create the main pusher agent
    pusher = Pusher(db)
    
    # Create cooldown manager
    cooldown = Cooldown()
    
    # Create command logger
    cmd_logger = CommandLogger()
    
    @bot.event
    async def on_ready():
        """Called when the bot is ready and connected to Discord"""
        logger.info(f"Trial Junkie online as {bot.user}")
        await bot.change_presence(activity=discord.Game(name="!hit | !dose | !stash | !help"))
    
    @bot.event
    async def on_command_error(ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Unknown command. Use `!help` to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param}")
        else:
            logger.error(f"Command error: {str(error)}")
            await ctx.send(f"Error: {str(error)}")
    
    @bot.command(name="help")
    async def help_command(ctx):
        """Display help information"""
        embed = discord.Embed(
            title="🧪 Trial Junkie Help",
            description="Your friendly neighborhood dealer for free trials",
            color=COLORS["info"],
            timestamp=datetime.now()
        )
        
        # Main commands
        embed.add_field(
            name="🎯 Hit (Full Trial)",
            value="`!hit <service>` - Generate all credentials for a trial\nExample: `!hit Netflix`",
            inline=False
        )
        
        embed.add_field(
            name="💊 Dose (Single Resource)",
            value="`!dose <agent> <service>` - Generate a specific credential\nAgents: harry (identity), mandy (card), xan (email), carl (phone)\nExample: `!dose harry Spotify`",
            inline=False
        )
        
        embed.add_field(
            name="🍄 Trip (Automation)",
            value="`!trip <script>` - Run an automation script\nExample: `!trip netflix_signup`\nUse `!trip help` for available scripts",
            inline=False
        )
        
        embed.add_field(
            name="🧪 Stash",
            value="`!stash` - View your saved credentials",
            inline=True
        )
        
        embed.add_field(
            name="🏥 Rehab",
            value="`!rehab` - Clear all your data",
            inline=True
        )
        
        # Fun commands
        embed.add_field(
            name="😜 Fun Commands",
            value="`!quote <agent>` - Get a quote from an agent\n`!agents` - Meet the agents\n`!stats` - View usage statistics",
            inline=False
        )
        
        embed.set_footer(text="Trial Junkie | The Last Free Trial You'll Ever Need")
        
        await ctx.send(embed=embed)
        
    @bot.command(name="hit")
    async def hit_command(ctx, service: str = None):
        """Full trial setup command (all agents)"""
        user_id = ctx.author.id
        username = ctx.author.name
        
        # Check cooldown
        if cooldown.is_on_cooldown(user_id, "hit"):
            remaining = cooldown.get_remaining_time(user_id, "hit")
            await ctx.send(f"🔒 **Need to sober up first.** Try again in {remaining} seconds.")
            return
            
        # Check if service was provided
        if not service:
            await ctx.send("❌ **Missing service name**. Use `!hit <service>` to start a trial.")
            return
            
        # Log command usage
        cmd_logger.log_command(user_id, username, "hit", service)
        
        # Send initial response
        await ctx.send(f"💉 **The Pusher** is preparing your `{service}` trial... Hold tight.")
        
        # Set cooldown
        cooldown.set_cooldown(user_id, "hit", 300)  # 5 minute cooldown
        
        # Process the request through the pusher
        try:
            result = await pusher.process_hit(user_id, username, service)
            await ctx.send(embed=result)
        except Exception as e:
            logger.error(f"Error processing hit command: {e}")
            await ctx.send(f"❌ **Bad batch!** Something went wrong: {str(e)}")
            
    @bot.command(name="dose")
    async def dose_command(ctx, agent_type: str = None, platform: str = None):
        """Partial account generation (single agent)"""
        user_id = ctx.author.id
        username = ctx.author.name
        
        # Check cooldown
        if cooldown.is_on_cooldown(user_id, "dose"):
            remaining = cooldown.get_remaining_time(user_id, "dose")
            await ctx.send(f"🔒 **Too soon for another hit.** Try again in {remaining} seconds.")
            return
        
        # Check if required params were provided
        if not agent_type or not platform:
            await ctx.send("❌ **Missing parameters**. Use `!dose <agent> <platform>` to get specific credentials.")
            await ctx.send("Available agents: `harry` (identity), `mandy` (card), `xan` (email), `phone` (SMS)")
            return
        
        # Log command usage
        cmd_logger.log_command(user_id, username, "dose", f"{agent_type} {platform}")
        
        # Set cooldown (shorter than full hit)
        cooldown.set_cooldown(user_id, "dose", 60)  # 1 minute cooldown
        
        # Process the dose request
        try:
            result = await pusher.process_dose(user_id, username, agent_type, platform)
            await ctx.send(embed=result)
        except Exception as e:
            logger.error(f"Error processing dose command: {e}")
            await ctx.send(f"❌ **Bad trip!** Something went wrong: {str(e)}")
    
    @bot.command(name="trip")
    async def trip_command(ctx, script: str = None):
        """Run automation scripts"""
        user_id = ctx.author.id
        username = ctx.author.name
        
        # Check cooldown
        if cooldown.is_on_cooldown(user_id, "trip"):
            remaining = cooldown.get_remaining_time(user_id, "trip")
            await ctx.send(f"🔒 **You're still tripping.** Try again in {remaining} seconds.")
            return
        
        # Check if script was provided
        if not script:
            await ctx.send("❌ **Missing script name**. Use `!trip <script>` to run an automation.")
            await ctx.send("Available scripts: `signup`, `verify`, `cancel`")
            return
        
        # Log command usage
        cmd_logger.log_command(user_id, username, "trip", script)
        
        # Send initial response
        await ctx.send(f"🍄 **Shroomy Sal** is taking you on a `{script}` trip... Enjoy the ride.")
        
        # Set cooldown
        cooldown.set_cooldown(user_id, "trip", 600)  # 10 minute cooldown
        
        # Process the trip request
        try:
            result = await pusher.process_trip(user_id, username, script)
            await ctx.send(embed=result)
        except Exception as e:
            logger.error(f"Error processing trip command: {e}")
            await ctx.send(f"❌ **Bad trip!** Something went wrong: {str(e)}")
    
    @bot.command(name="stash")
    async def stash_command(ctx):
        """View user's generated items"""
        user_id = ctx.author.id
        username = ctx.author.name
        
        # Log command usage
        cmd_logger.log_command(user_id, username, "stash", "")
        
        # Process the stash request
        try:
            result = await pusher.process_stash(user_id, username)
            await ctx.send(embed=result)
        except Exception as e:
            logger.error(f"Error processing stash command: {e}")
            await ctx.send(f"❌ **Stash is empty!** Something went wrong: {str(e)}")
    
    @bot.command(name="rehab")
    async def rehab_command(ctx):
        """Clear user data"""
        user_id = ctx.author.id
        username = ctx.author.name
        
        # Check cooldown
        if cooldown.is_on_cooldown(user_id, "rehab"):
            remaining = cooldown.get_remaining_time(user_id, "rehab")
            await ctx.send(f"🔒 **Rehab still in progress.** Try again in {remaining} seconds.")
            return
        
        # Log command usage
        cmd_logger.log_command(user_id, username, "rehab", "")
        
        # Set cooldown
        cooldown.set_cooldown(user_id, "rehab", 3600)  # 1 hour cooldown
        
        # Send confirmation message
        confirm_msg = await ctx.send(f"⚠️ **Checking into rehab will clear all your data.** React with ✅ to confirm.")
        await confirm_msg.add_reaction("✅")
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == confirm_msg.id
        
        try:
            # Wait for confirmation (30 seconds timeout)
            reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
            
            # Process the rehab request
            result = await pusher.process_rehab(user_id, username)
            await ctx.send(embed=result)
            
        except TimeoutError:
            await ctx.send("❌ **Rehab canceled** - You changed your mind. Your data is still intact.")
        except Exception as e:
            logger.error(f"Error processing rehab command: {e}")
            await ctx.send(f"❌ **Rehab failed!** Something went wrong: {str(e)}")
    
    @bot.command(name="quote")
    async def quote_command(ctx, agent: str = None):
        """Get a random quote from an agent"""
        if not agent:
            await ctx.send("Please specify an agent. Example: `!quote harry` or use `!agents` to see all agents.")
            return
        
        # Standardize agent name
        agent_aliases = {
            "harry": "harry",
            "h": "harry",
            "heroin": "harry",
            "mandy": "mandy",
            "m": "mandy",
            "meth": "mandy",
            "xan": "xan",
            "x": "xan",
            "xanny": "xan",
            "carl": "carl",
            "c": "carl",
            "coke": "carl",
            "sal": "sal",
            "s": "sal",
            "shroom": "sal",
            "shroomy": "sal",
            "pusher": "pusher",
            "p": "pusher"
        }
        
        std_agent = agent_aliases.get(agent.lower())
        if not std_agent:
            await ctx.send(f"Unknown agent '{agent}'. Use `!agents` to see all agents.")
            return
        
        # Generate quote about random topic
        topics = ["free trials", "subscriptions", "streaming", "credit cards", "online accounts", 
                  "passwords", "identities", "emails", "phone numbers", "verification",
                  "automation", "bots", "discord", "signing up", "getting high on trials"]
        
        topic = random.choice(topics)
        quote = get_agent_quote(std_agent, topic)
        
        # Format with agent emoji
        agent_emoji = {
            "harry": "💉",
            "mandy": "💊",
            "xan": "💊",
            "carl": "⚗️",
            "sal": "🍄",
            "pusher": "🎯"
        }
        emoji = agent_emoji.get(std_agent, "🧪")
        agent_name = AGENT_NAMES.get(std_agent, agent)
        
        await ctx.send(f"{emoji} **{agent_name}**: {quote}")
    
    @bot.command(name="agents")
    async def agents_command(ctx):
        """Display information about all agents"""
        embed = discord.Embed(
            title="🧪 Meet the Agents",
            description="The crew that makes Trial Junkie possible",
            color=COLORS["info"],
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="💉 Heroin Harry",
            value="Identity generation specialist. Need a new you for every trial.",
            inline=False
        )
        
        embed.add_field(
            name="💊 Meth Mandy",
            value="Card generator extraordinaire. Pure, uncut credit cards that always work.",
            inline=False
        )
        
        embed.add_field(
            name="💊 Xanny Xan",
            value="Email address creator. Helping you chill out with disposable addresses.",
            inline=False
        )
        
        embed.add_field(
            name="⚗️ Cokehead Carl",
            value="Phone number specialist. The fastest numbers in the West.",
            inline=False
        )
        
        embed.add_field(
            name="🍄 Shroomy Sal",
            value="Automation wizard. Let Sal guide you through the sign-up trip.",
            inline=False
        )
        
        embed.add_field(
            name="🎯 The Pusher",
            value="Main dealer. Controls all agents and delivers the goods.",
            inline=False
        )
        
        embed.set_footer(text="Use !quote <agent> to hear from your favorite agent")
        
        await ctx.send(embed=embed)
    
    return bot
