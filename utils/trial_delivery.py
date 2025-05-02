"""
Trial Delivery Utility
Handles delivery of generated trials to users via different methods
(Discord DM, website dashboard, email, etc.)
"""
import os
import json
import logging
import asyncio
import discord
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrialDelivery:
    """
    Handles delivery of generated trials to users
    Supports multiple delivery methods (Discord DM, website dashboard)
    """
    def __init__(self, bot=None):
        """
        Initialize trial delivery module
        
        Args:
            bot (discord.Bot, optional): Discord bot instance for DM delivery
        """
        self.bot = bot
        
    async def deliver_trial(self, user_id, trial_data, delivery_methods=None):
        """
        Deliver trial data to a user using multiple methods
        
        Args:
            user_id (str): The user ID to deliver the trial to
            trial_data (dict): The trial data to deliver
            delivery_methods (list, optional): List of delivery methods
                If None, defaults to ['dashboard', 'discord'] if bot is available,
                otherwise just ['dashboard']
        
        Returns:
            dict: Delivery results for each method
        """
        if delivery_methods is None:
            delivery_methods = ['dashboard']
            if self.bot is not None:
                delivery_methods.append('discord')
        
        results = {}
        
        for method in delivery_methods:
            if method == 'discord':
                if self.bot is not None:
                    results['discord'] = await self.deliver_to_discord(user_id, trial_data)
                else:
                    results['discord'] = {'success': False, 'message': 'Discord bot not available'}
            
            elif method == 'dashboard':
                results['dashboard'] = await self.save_to_dashboard(user_id, trial_data)
            
            elif method == 'email':
                # Future: implement email delivery if needed
                results['email'] = {'success': False, 'message': 'Email delivery not implemented yet'}
        
        return results
    
    async def deliver_to_discord(self, user_id, trial_data):
        """
        Deliver trial data to a user via Discord DM
        
        Args:
            user_id (str): The Discord user ID to DM
            trial_data (dict): The trial data to deliver
            
        Returns:
            dict: Delivery result
        """
        try:
            # Try to get the user
            user = await self.bot.fetch_user(int(user_id))
            
            if not user:
                logger.error(f"User not found for Discord ID: {user_id}")
                return {
                    'success': False,
                    'message': f"User with ID {user_id} not found"
                }
            
            # Create embedded message for trial data
            embed = self._create_trial_embed(trial_data)
            
            # Send DM to user
            await user.send(
                content="🎉 Your trial is ready! Here are the login details:",
                embed=embed
            )
            
            logger.info(f"Trial delivered via Discord DM to user: {user_id}")
            
            return {
                'success': True,
                'message': f"Trial delivered to Discord user {user.name}#{user.discriminator}",
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error delivering trial to Discord: {str(e)}")
            return {
                'success': False,
                'message': f"Error delivering trial to Discord: {str(e)}"
            }
    
    async def save_to_dashboard(self, user_id, trial_data):
        """
        Save trial data to user's dashboard
        
        Args:
            user_id (str): The user ID
            trial_data (dict): The trial data to save
            
        Returns:
            dict: Save result
        """
        from database import Database
        try:
            # Connect to database
            db = Database()
            
            # Create trial entry
            service = trial_data.get('service', 'unknown')
            trial_type = 'generated'  # or 'automated', etc.
            
            # Extract user info
            user_info = trial_data.get('user_info', {})
            email = user_info.get('email', 'unknown')
            password = user_info.get('password', 'unknown')
            
            # Get trial end date
            end_date = trial_data.get('trial_end_date')
            if end_date:
                # If it's a string, convert to datetime
                if isinstance(end_date, str):
                    try:
                        expires_at = datetime.fromisoformat(end_date)
                    except ValueError:
                        expires_at = None
                else:
                    expires_at = end_date
            else:
                expires_at = None
            
            # Additional details as JSON
            details = json.dumps(trial_data)
            
            # Save to database
            # For database.py implementation, we'll use the save_credential method
            # This could be expanded in the future if a dedicated trial table is created
            db.save_credential(
                user_id=user_id,
                service=service,
                credential_type='trial',
                credential_value=json.dumps({
                    'email': email,
                    'password': password,
                    'expires_at': expires_at.isoformat() if expires_at else None,
                    'details': details
                })
            )
            
            logger.info(f"Trial saved to dashboard for user: {user_id}")
            
            return {
                'success': True,
                'message': f"Trial saved to dashboard for user {user_id}",
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error saving trial to dashboard: {str(e)}")
            return {
                'success': False,
                'message': f"Error saving trial to dashboard: {str(e)}"
            }
    
    def _create_trial_embed(self, trial_data):
        """
        Create a Discord embed for trial data
        
        Args:
            trial_data (dict): The trial data
            
        Returns:
            discord.Embed: Formatted embed
        """
        # Get service and capitalize for title
        service = trial_data.get('service', 'unknown').capitalize()
        
        # Create embed
        embed = discord.Embed(
            title=f"{service} Trial Account",
            description="Here are your trial account details. Use these to log in.",
            color=0x6f42c1  # Purple color
        )
        
        # Add login details
        user_info = trial_data.get('user_info', {})
        embed.add_field(
            name="Login Details",
            value=f"Email: `{user_info.get('email', 'N/A')}`\nPassword: `{user_info.get('password', 'N/A')}`",
            inline=False
        )
        
        # Add payment information (obscured)
        payment_info = trial_data.get('payment_info', {})
        card_number = payment_info.get('card_number', '')
        if card_number:
            # Only show last 4 digits
            last_four = card_number[-4:] if len(card_number) >= 4 else card_number
            obscured = f"{'*' * (len(card_number) - 4)}{last_four}"
        else:
            obscured = "N/A"
            
        embed.add_field(
            name="Payment Method",
            value=f"Card: `{obscured}`\nExpiry: `{payment_info.get('expiry', 'N/A')}`",
            inline=True
        )
        
        # Add service details
        service_details = trial_data.get('service_details', {})
        plan = service_details.get('plan', 'Standard')
        
        embed.add_field(
            name="Plan Details",
            value=f"Plan: `{plan}`",
            inline=True
        )
        
        # Add expiry information
        trial_end = trial_data.get('trial_end_date')
        if trial_end:
            try:
                # Parse ISO format date
                end_date = datetime.fromisoformat(trial_end)
                # Format as readable date
                formatted_date = end_date.strftime("%B %d, %Y")
            except (ValueError, TypeError):
                formatted_date = trial_end
        else:
            formatted_date = "Unknown"
            
        embed.add_field(
            name="Trial Expiry",
            value=f"Expires on: `{formatted_date}`",
            inline=False
        )
        
        # Add footer
        embed.set_footer(text="Generated by Trial Junkie | Remember to cancel before the trial ends to avoid charges!")
        
        return embed

# For testing
if __name__ == "__main__":
    async def test_delivery():
        # Create mock trial data
        mock_trial = {
            'service': 'netflix',
            'user_info': {
                'email': 'test@example.com',
                'password': 'ComplexPassword123!'
            },
            'payment_info': {
                'card_number': '4242424242424242',
                'expiry': '12/25',
                'cvv': '123'
            },
            'service_details': {
                'plan': 'Standard'
            },
            'trial_end_date': (datetime.now().replace(month=datetime.now().month + 1)).isoformat()
        }
        
        # Create delivery instance (without bot for testing)
        delivery = TrialDelivery()
        
        # Test dashboard delivery
        result = await delivery.save_to_dashboard('test_user_123', mock_trial)
        print(f"Dashboard delivery result: {result}")
    
    # Run the test
    asyncio.run(test_delivery())