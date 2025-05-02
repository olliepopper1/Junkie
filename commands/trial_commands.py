"""
Trial Commands Module for Discord Bot

Handles commands related to generating and delivering trials
"""
import os
import logging
import json
from datetime import datetime, timedelta
import asyncio

import discord
from discord.ext import commands
from discord import app_commands

from trial_delivery_service import TrialDeliveryService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("trial_commands.log")
    ]
)
logger = logging.getLogger("trial_commands")

class TrialCommands(commands.Cog):
    """Commands for generating and delivering trials"""

    def __init__(self, bot):
        """Initialize TrialCommands cog"""
        self.bot = bot
        self.trial_service = TrialDeliveryService()
        logger.info("Trial commands initialized")
    
    @commands.command(name="hit")
    async def hit_command(self, ctx, *, service_or_url: str = None):
        """
        Generate a trial for a service or URL
        
        Args:
            service_or_url: The service name (hulu, netflix, etc.) or URL to generate a trial for
        """
        logger.info(f"Hit command received from {ctx.author.id} for {service_or_url}")
        
        # Check if a service was specified
        if not service_or_url:
            await ctx.send("Please specify a service (e.g. !hit hulu) or URL to generate a trial for.")
            return
        
        # Start typing indicator to show the bot is working
        async with ctx.typing():
            # Check user's subscription status
            user_status = self._check_user_subscription(ctx.author.id)
            
            if not user_status.get("has_subscription", False):
                await ctx.send("You need an active subscription to generate trials. Use !plans to see subscription options.")
                return
            
            # Check if the user has reached their daily limit
            usage_limit = self._check_trial_usage_limits(ctx.author.id, user_status.get("tier", "basic"))
            
            if not usage_limit.get("can_generate", False):
                await ctx.send(f"You've reached your daily trial generation limit ({usage_limit.get('current_count', 0)}/{usage_limit.get('max_count', 0)}). Try again tomorrow or upgrade your subscription.")
                return
            
            # Determine the service name from the input
            service = self._determine_service(service_or_url)
            
            # Send the initial message
            await ctx.send(f"🧪 Generating your {service} trial... This might take a minute...")
            
            try:
                # Generate and deliver the trial
                result = self.trial_service.generate_and_deliver(
                    service, 
                    str(ctx.author.id),  # Use the Discord ID as the user ID for dashboard
                    str(ctx.author.id)   # Also deliver via Discord
                )
                
                if result.get("success", False):
                    login_credentials = result.get("login_credentials", {})
                    account_details = result.get("account_details", {})
                    expiration_date = result.get("expiration_date", "unknown")
                    
                    # Format the expiration date for better readability
                    try:
                        expiration_date_obj = datetime.fromisoformat(expiration_date)
                        formatted_expiration = expiration_date_obj.strftime("%B %d, %Y")
                    except (ValueError, TypeError):
                        formatted_expiration = expiration_date
                    
                    # Send the confirmation message
                    embed = discord.Embed(
                        title=f"✅ {service.title()} Trial Generated",
                        description=f"Your trial has been generated and saved to your dashboard. Check your DMs for login details.",
                        color=0x00ff00  # Green color
                    )
                    embed.add_field(name="Plan", value=account_details.get("plan", "Standard"), inline=True)
                    embed.add_field(name="Expires", value=formatted_expiration, inline=True)
                    
                    await ctx.send(embed=embed)
                    
                    # Update usage tracking in database
                    self._track_trial_usage(ctx.author.id, service)
                    
                else:
                    error_message = result.get("error", "Unknown error")
                    await ctx.send(f"⚠️ Could not generate trial: {error_message}")
                    logger.error(f"Trial generation failed for user {ctx.author.id}: {error_message}")
            
            except Exception as e:
                logger.error(f"Error generating trial: {e}")
                await ctx.send(f"⚠️ An error occurred while generating your trial: {str(e)}")
    
    @commands.command(name="stash")
    async def stash_command(self, ctx):
        """View your generated trials"""
        logger.info(f"Stash command received from {ctx.author.id}")
        
        # Start typing indicator
        async with ctx.typing():
            try:
                # Get the user's trials from database
                if hasattr(self.trial_service, 'db_connection') and self.trial_service.db_connection:
                    trials = self.trial_service.db_connection.get_user_trials(str(ctx.author.id))
                else:
                    from database import Database
                    db = Database()
                    trials = db.get_user_trials(str(ctx.author.id))
                    db.close()
                
                if not trials:
                    await ctx.send("You don't have any trials yet. Use !hit to generate one.")
                    return
                
                # Create an embed for the trials
                embed = discord.Embed(
                    title="🧪 Your Trial Stash",
                    description=f"You have {len(trials)} trials in your stash.",
                    color=0x9b59b6  # Purple color
                )
                
                # Add the most recent 5 trials to the embed
                for i, trial in enumerate(trials[:5]):
                    service = trial.get("service", "unknown").title()
                    creation_date = trial.get("creation_date", "unknown")
                    expiration_date = trial.get("expiration_date", "unknown")
                    
                    # Format the dates for better readability
                    try:
                        creation_date_obj = datetime.fromisoformat(creation_date)
                        formatted_creation = creation_date_obj.strftime("%B %d, %Y")
                    except (ValueError, TypeError):
                        formatted_creation = creation_date
                        
                    try:
                        expiration_date_obj = datetime.fromisoformat(expiration_date)
                        formatted_expiration = expiration_date_obj.strftime("%B %d, %Y")
                    except (ValueError, TypeError):
                        formatted_expiration = expiration_date
                    
                    embed.add_field(
                        name=f"{i+1}. {service}",
                        value=f"Created: {formatted_creation}\nExpires: {formatted_expiration}",
                        inline=False
                    )
                
                if len(trials) > 5:
                    embed.set_footer(text=f"Showing 5 most recent trials of {len(trials)} total. Check your dashboard to see all.")
                
                await ctx.send(embed=embed)
                
            except Exception as e:
                logger.error(f"Error getting trials: {e}")
                await ctx.send(f"⚠️ An error occurred while retrieving your trials: {str(e)}")
    
    def _check_user_subscription(self, user_id):
        """
        Check a user's subscription status
        
        Args:
            user_id: The Discord user ID
            
        Returns:
            dict: Subscription status information
        """
        # For demonstration purposes, we'll assume all users have a basic subscription
        # In a real implementation, this would check the database
        return {
            "has_subscription": True,
            "tier": "premium",
            "subscribed_since": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(days=30)).isoformat()
        }
    
    def _check_trial_usage_limits(self, user_id, subscription_tier):
        """
        Check if a user has reached their daily trial generation limit
        
        Args:
            user_id: The Discord user ID
            subscription_tier: The user's subscription tier
            
        Returns:
            dict: Usage limit information including whether generation is allowed
        """
        # For demonstration purposes, we'll assume all users have not reached their limit
        # In a real implementation, this would check the database
        
        # Determine max trials based on tier
        if subscription_tier == "premium":
            max_trials = 10
        elif subscription_tier == "pro":
            max_trials = 5
        else:  # basic tier
            max_trials = 2
        
        # For demo, assume user has used 0 trials today
        return {
            "can_generate": True,
            "current_count": 0,
            "max_count": max_trials,
            "reset_time": (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0).isoformat()
        }
    
    def _track_trial_usage(self, user_id, service):
        """
        Track a trial generation for usage limits
        
        Args:
            user_id: The Discord user ID
            service: The service name
            
        Returns:
            bool: True if tracking was successful
        """
        # For demonstration purposes, we'll just log it
        logger.info(f"Tracking trial usage for user {user_id} for service {service}")
        return True
    
    def _determine_service(self, service_or_url):
        """
        Determine the service name from the input
        
        Args:
            service_or_url: The service name or URL
            
        Returns:
            str: The service name
        """
        # Convert to lowercase for easier comparison
        input_lower = service_or_url.lower()
        
        # Check if it's a known service
        known_services = ["hulu", "netflix", "disney", "spotify", "youtube"]
        
        for service in known_services:
            if service in input_lower:
                return service
        
        # If it's a URL, extract the domain
        if input_lower.startswith("http"):
            try:
                from urllib.parse import urlparse
                domain = urlparse(input_lower).netloc
                
                # Extract the main domain name (e.g., "hulu.com" -> "hulu")
                domain_parts = domain.split(".")
                if len(domain_parts) >= 2:
                    return domain_parts[-2]
                else:
                    return domain
            except:
                pass
        
        # If we can't determine the service, just return the input
        return service_or_url

# Setup function for loading the cog
def setup(bot):
    """Load the TrialCommands cog"""
    bot.add_cog(TrialCommands(bot))
    logger.info("TrialCommands cog loaded")