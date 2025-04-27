"""
Discord Token Tester for Trial Junkie
Checks if the Discord token is valid
"""
import os
import sys
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands

# Load environment variables
load_dotenv()

# Get Discord bot token from environment variable
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    print("ERROR: DISCORD_BOT_TOKEN not found in environment variables!")
    print("Please make sure you have set the DISCORD_BOT_TOKEN environment variable.")
    sys.exit(1)

# Setup Discord bot with command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord"""
    print(f"Success! Discord bot token is valid.")
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print(f"Connected to {len(bot.guilds)} guilds")
    
    # Print the invite link
    app_info = await bot.application_info()
    invite_link = discord.utils.oauth_url(
        app_info.id,
        permissions=discord.Permissions(administrator=True),
        scopes=("bot", "applications.commands")
    )
    print(f"\nInvite link: {invite_link}")
    
    # Exit after verification is complete
    await bot.close()

@bot.event
async def on_error(event, *args, **kwargs):
    """Handle errors during bot operation"""
    print(f"Error in event {event}: {sys.exc_info()[1]}")
    await bot.close()

def main():
    """Main function to run the token test"""
    print("Testing Discord bot token...")
    try:
        bot.run(DISCORD_BOT_TOKEN, reconnect=False)
        print("Bot closed cleanly.")
    except discord.errors.LoginFailure:
        print("ERROR: Invalid Discord bot token. Please check your DISCORD_BOT_TOKEN environment variable.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        sys.exit(1)
    else:
        print("Discord token test completed successfully.")

if __name__ == "__main__":
    main()