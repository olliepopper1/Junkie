"""
Discord Bot Implementation for Trial Junkie
Handles all Discord interactions and commands
"""
import os
import discord
from discord.ext import commands
import logging
from agents.pusher import Pusher
from utils.logger import CommandLogger
from utils.cooldown import Cooldown
from database import Database

logger = logging.getLogger(__name__)

def setup_bot():
    # Set up intents
    intents = discord.Intents.default()
    intents.message_content = True
    
    # Create the bot
    bot = commands.Bot(command_prefix='!', intents=intents)
    
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
        await bot.change_presence(activity=discord.Game(name="!hit | !dose | !trip | !rehab"))
        
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
    
    return bot
