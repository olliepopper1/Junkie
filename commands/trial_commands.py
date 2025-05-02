"""
Trial Commands for Discord Bot
Handles commands related to trial generation and management
"""
import asyncio
import logging
import sys
import os
import json
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from database import Database
from utils.trial_generator import TrialGenerator
from simplified_hulu_trial import SimpleTrialGenerator
from bot_trial_delivery import TrialDelivery

# Configure logging
logger = logging.getLogger(__name__)

class TrialCommands(commands.Cog):
    """Commands for generating and managing trials"""
    
    def __init__(self, bot, db):
        """
        Initialize the trial commands
        
        Args:
            bot: The Discord bot
            db: Database instance
        """
        self.bot = bot
        self.db = db
        self.trial_generator = TrialGenerator(db)
        
    @commands.command(name="trial")
    async def trial_command(self, ctx, service=None):
        """
        Generate trial information for a service
        
        Usage: !trial [service]
        
        Args:
            service: The service to generate a trial for (hulu, netflix, youtube, etc.)
        """
        if not service:
            await ctx.send("Please specify a service (e.g., !trial hulu)")
            return
            
        await ctx.send(f"Generating trial information for {service.upper()}... 🔄")
        
        try:
            # Generate trial information
            trial_info = await self.trial_generator.generate_trial(service)
            
            # Extract user info
            user_info = trial_info["user_info"]
            
            # Create a Discord embed
            embed = discord.Embed(
                title=f"✅ {service.upper()} Trial Information",
                description=f"Successfully generated trial information for {service.upper()}",
                color=0x2ecc71
            )
            
            # Add account fields
            embed.add_field(
                name="📧 Account Info",
                value=f"**Email:** {user_info['email']}\n**Password:** {user_info['password']}",
                inline=False
            )
            
            # Add personal info fields
            embed.add_field(
                name="👤 Identity",
                value=f"**Name:** {user_info['first_name']} {user_info['last_name']}\n"
                      f"**Address:** {user_info['address']}, {user_info['city']}, {user_info['state']} {user_info['zipcode']}\n"
                      f"**Phone:** {user_info['phone']}",
                inline=False
            )
            
            # Add payment fields (masked)
            embed.add_field(
                name="💳 Payment Info",
                value=f"**Card Type:** {user_info['card_type'].capitalize()}\n"
                      f"**Card Number:** **** **** **** {user_info['card_number'][-4:]}\n"
                      f"**Expiry:** {user_info['card_expiry']}\n"
                      f"**CVV:** {user_info['card_cvv']}\n"
                      f"**Cardholder:** {user_info['card_holder']}",
                inline=False
            )
            
            # Add subscription info
            embed.add_field(
                name="📺 Subscription Details",
                value=f"**Plan:** {trial_info['plan']}\n"
                      f"**Monthly Cost:** {trial_info['monthly_price']}\n"
                      f"**Trial Period:** {trial_info['trial_days']} days\n"
                      f"**Trial Ends:** {trial_info['trial_end_date'].split('T')[0]}\n"
                      f"**Cancellation URL:** {trial_info.get('cancellation_url', 'Not available')}",
                inline=False
            )
            
            # Add footer
            embed.set_footer(text=f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Trial Junkie")
            
            # Send the embed
            await ctx.send(embed=embed)
            
            # Save to database
            try:
                # Save the credentials to the database
                self.db.save_credential(ctx.author.id, service, "email", user_info["email"])
                self.db.save_credential(ctx.author.id, service, "password", user_info["password"])
                self.db.save_credential(ctx.author.id, service, "profile", json.dumps(trial_info))
                
                logger.info(f"Saved {service} trial credentials for user {ctx.author.id}")
            except Exception as e:
                logger.error(f"Error saving trial credentials to database: {str(e)}")
                
        except Exception as e:
            logger.error(f"Error generating trial information: {str(e)}")
            await ctx.send(f"❌ Error generating trial information: {str(e)}")
    
    @commands.command(name="trials")
    async def trials_command(self, ctx):
        """
        List available trial services
        
        Usage: !trials
        """
        # Create a Discord embed
        embed = discord.Embed(
            title="🔥 Available Trial Services",
            description="Use `!trial <service>` to generate trial information for any of these services",
            color=0x3498db
        )
        
        # Add services
        embed.add_field(
            name="Streaming Services",
            value="• **hulu** - Hulu (No Ads)\n"
                  "• **netflix** - Netflix Standard\n"
                  "• **disney** - Disney+ Premium\n"
                  "• **youtube** - YouTube Premium\n"
                  "• **amazon** - Amazon Prime\n"
                  "• **spotify** - Spotify Premium\n"
                  "• **paramount** - Paramount+\n"
                  "• **hbomax** - HBO Max",
            inline=False
        )
        
        embed.add_field(
            name="Coming Soon",
            value="• **apple** - Apple TV+\n"
                  "• **peacock** - Peacock Premium\n"
                  "• **discovery** - Discovery+\n"
                  "• **crunchyroll** - Crunchyroll Premium",
            inline=False
        )
        
        # Add footer
        embed.set_footer(text="Trial Junkie | Get lit with free trials 🔥")
        
        # Send the embed
        await ctx.send(embed=embed)
        
def setup(bot, db):
    """Set up the trial commands for the bot"""
    bot.add_cog(TrialCommands(bot, db))
    logger.info("Trial commands loaded")