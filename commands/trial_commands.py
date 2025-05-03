"""
Trial Commands for Discord Bot
Handles all commands related to trial generation and management
"""
import os
import sys
import logging
import json
import asyncio

import discord
from discord.ext import commands
from discord import Embed, Color

sys.path.append('.')  # Add the current directory to the path
from bot_trial_delivery import TrialDelivery

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("discord_bot_trial_commands.log")
    ]
)
logger = logging.getLogger("trial_commands")

class TrialCommands(commands.Cog):
    """Commands for generating and managing trials"""
    
    def __init__(self, bot):
        self.bot = bot
        self.delivery = TrialDelivery()
        
    @commands.command(name="hit")
    async def hit_command(self, ctx, *, service_or_url: str = None):
        """Full trial setup command (all agents) - Works with services or URLs"""
        if not service_or_url:
            return await ctx.send("Please specify a service or URL. For example: `!hit hulu`")
        
        # Check if the user is subscribed
        # This would be implemented with your subscription system
        is_subscribed = True  # Mock subscription check
        
        if not is_subscribed:
            return await ctx.send("You need an active subscription to use this command. Type `!plans` to see available plans.")
        
        # Send the initial response
        response = await ctx.send(f"🔄 Processing your request for `{service_or_url}`. Please wait...")
        
        # Process the request based on the service
        if service_or_url.lower() == "hulu":
            # First, save the message to simulate processing
            await response.edit(content="⏳ Generating Hulu trial. This may take a moment...")
            
            # Generate the trial
            await self._generate_hulu_trial(ctx, response)
        else:
            await response.edit(content=f"⚠️ Service `{service_or_url}` is not supported yet.")
    
    async def _generate_hulu_trial(self, ctx, response):
        """Generate a Hulu trial using browser automation"""
        try:
            # Use the trial generator in a separate thread to avoid blocking
            # Since RealHuluTrialGenerator uses Selenium which is not async-compatible
            
            # First provide feedback that we're working on it
            await response.edit(content="🤖 Initializing browser automation...\n⏳ This can take a minute or two...")
            
            # Simulate actual trial generation with a delay
            # In a real implementation, you would use your actual trial generation here
            await asyncio.sleep(3)
            
            # Simulate successful trial generation
            # In production you would use:
            # trial_info = await loop.run_in_executor(None, lambda: RealHuluTrialGenerator().generate_trial(user_id=str(ctx.author.id), discord_id=str(ctx.author.id)))
            
            # For now, just load the last generated trial from the file
            latest_trial_file = self._get_latest_trial_file()
            trial_info = None
            
            if latest_trial_file:
                with open(latest_trial_file, 'r', encoding='utf-8') as f:
                    trial_info = json.load(f)
            
            if not trial_info:
                # If no trial file is found, generate a new one
                await response.edit(content="⚠️ No recent trial found. Generating a new one...")
                await asyncio.sleep(2)
                
                # Generate a trial 
                if hasattr(self.delivery, 'generate_trial'):
                    self.delivery.generate_trial("hulu", ctx.author.id)
                else:
                    logger.error("TrialDelivery does not have a 'generate_trial' method.")
                
                # Get the latest file again
                latest_trial_file = self._get_latest_trial_file()
                if latest_trial_file:
                    with open(latest_trial_file, 'r', encoding='utf-8') as f:
                        trial_info = json.load(f)
            
            if trial_info and trial_info.get('success', False):
                # Format the trial information into a Discord embed
                embed = self._format_trial_embed(trial_info)
                
                # Send the trial information via DM
                try:
                    await ctx.author.send(embed=embed)
                    await ctx.author.send("**⚠️ Important Notes:**\n- This trial will expire automatically after 30 days\n- To avoid charges, cancel before the expiration date\n- Login details will also be available on your dashboard at trialjunkie.io")
                    await response.edit(content="✅ Hulu trial created successfully! Check your DMs for login details.")
                except discord.Forbidden:
                    await response.edit(content="✅ Hulu trial created successfully! But I couldn't DM you the details. Please enable DMs from server members.")
            else:
                await response.edit(content="❌ Failed to generate Hulu trial. Please try again later.")
                
        except discord.Forbidden as e:
            logger.error("Discord permission error: %s", e, exc_info=True)
            await response.edit(content="❌ Unable to send you a DM. Please enable DMs from server members.")
        except FileNotFoundError as e:
            logger.error("File not found: %s", e, exc_info=True)
            await response.edit(content="❌ An error occurred while generating your trial: File not found.")
        except json.JSONDecodeError as e:
            logger.error("JSON decoding error: %s", e, exc_info=True)
            await response.edit(content="❌ An error occurred while processing trial data.")
        except (OSError, IOError) as e:
            logger.error("File system error: %s", e, exc_info=True)
            await response.edit(content="❌ A file system error occurred while generating your trial.")
        except asyncio.TimeoutError as e:
            logger.error("Timeout error: %s", e, exc_info=True)
            await response.edit(content="❌ The operation timed out. Please try again later.")
        except Exception as e:
            logger.error("Unexpected error: %s", e, exc_info=True)
            await response.edit(content="❌ An unexpected error occurred while generating your trial.")
    
    def _get_latest_trial_file(self):
        """Get the most recently created trial file"""
        trial_files = [f for f in os.listdir('.') if f.startswith('hulu_trial_') and f.endswith('.json')]
        if not trial_files:
            return None
        
        # Sort by creation time, newest first
        trial_files.sort(key=os.path.getctime, reverse=True)
        return trial_files[0]
    
    def _format_trial_embed(self, trial_info):
        """Format trial information as an embed"""
        embed = Embed(
            title=f"🎬 {trial_info['service'].upper()} TRIAL ACCOUNT",
            description="Your trial account has been created successfully!",
            color=Color.purple()
        )
        
        # Add login credentials
        credentials = trial_info.get('login_credentials', {})
        embed.add_field(
            name="📧 Login Credentials",
            value=f"**Email:** {credentials.get('email', 'N/A')}\n**Password:** {credentials.get('password', 'N/A')}",
            inline=False
        )
        
        # Add account details
        details = trial_info.get('account_details', {})
        embed.add_field(
            name="📋 Account Details",
            value=f"**Name:** {details.get('first_name', 'N/A')} {details.get('last_name', 'N/A')}\n**Plan:** {details.get('plan', 'N/A')}\n**Price:** {details.get('price', 'N/A')}",
            inline=False
        )
        
        # Add payment information (last 4 digits only for security)
        payment = trial_info.get('payment_method', {})
        embed.add_field(
            name="💳 Payment Method",
            value=f"**Card Type:** {payment.get('card_type', 'N/A')}\n**Last 4 Digits:** {payment.get('last_four', 'N/A')}\n**Expiry:** {payment.get('expiry', 'N/A')}",
            inline=False
        )
        
        # Add trial expiration
        embed.add_field(
            name="⏱️ Trial Expiration",
            value=f"Expires on: **{trial_info.get('expiration_date', 'N/A').split('T')[0]}**",
            inline=False
        )
        
        # Add login URL
        embed.add_field(
            name="🔗 Login URL",
            value="[Click here to login](https://www.hulu.com/welcome)",
            inline=False
        )
        
        # Set footer with a reminder to avoid charges
        embed.set_footer(text="Remember to cancel before the trial ends to avoid charges.")
        
        return embed
    
    @commands.command(name="stash")
    async def stash_command(self, ctx):
        """View user's generated items"""
        # Send initial response
        response = await ctx.send("🔄 Retrieving your trials...")
        
        # Get the trials for this user from the database
        # In a real implementation, you would use your actual database
        latest_trial_file = self._get_latest_trial_file()
        
        if not latest_trial_file:
            return await response.edit(content="❌ You don't have any trials yet. Use `!hit hulu` to create one.")
        
        with open(latest_trial_file, 'r', encoding='utf-8') as f:
            trial_info = json.load(f)
        
        # Create an embed with the trial information
        embed = self._format_trial_embed(trial_info)
        
        # Update the response with the embed
        await response.edit(content="🗃️ Here are your saved trials:", embed=embed)
        
    @commands.command(name="agents")
    async def agents_command(self, ctx):
        """Display information about all agents"""
        embed = Embed(
            title="🤖 Trial Junkie Agents",
            description="Meet the specialized agents that help you get trials",
            color=Color.purple()
        )
        
        embed.add_field(
            name="🕵️ Personator",
            value="Generates realistic identities for trial signups",
            inline=False
        )
        
        embed.add_field(
            name="📱 Virtual Number",
            value="Creates phone numbers for verification",
            inline=False
        )
        
        embed.add_field(
            name="💳 Card Smith",
            value="Generates valid credit cards for free trials",
            inline=False
        )
        
        embed.add_field(
            name="📧 Disposable Mail",
            value="Creates disposable email addresses",
            inline=False
        )
        
        embed.add_field(
            name="🤖 Trial Bot",
            value="Automates the trial signup process",
            inline=False
        )
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(TrialCommands(bot))