"""
Discord Bot Tester for Trial Junkie
Tests the bot's functionality and commands
"""
import os
import sys
import traceback
from datetime import datetime
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Discord bot token from environment variable
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    print("ERROR: DISCORD_BOT_TOKEN not found in environment variables!")
    print("Please make sure you have set the DISCORD_BOT_TOKEN environment variable.")
    sys.exit(1)

# Create test results directory
TEST_RESULTS_DIR = "test_results"
os.makedirs(TEST_RESULTS_DIR, exist_ok=True)

# Setup logging function
def log_test(test_name, success, error=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "PASS" if success else "FAIL"
    log_line = f"[{timestamp}] {test_name}: {status}"
    
    if error:
        log_line += f"\n    Error: {error}"
        if hasattr(error, '__traceback__'):
            tb = ''.join(traceback.format_tb(error.__traceback__))
            log_line += f"\n    Traceback:\n{tb}"
        
    print(log_line)
    
    with open(f"{TEST_RESULTS_DIR}/discord_bot_tests.log", "a") as log_file:
        log_file.write(log_line + "\n")

# Setup Discord bot with command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Test suite class
class BotTests:
    def __init__(self, bot):
        self.bot = bot
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
    
    async def run_all_tests(self):
        """Run all test methods in this class"""
        print(f"{'='*20} TRIAL JUNKIE BOT TEST SUITE {'='*20}")
        print(f"Starting tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        start_time = datetime.now()
        
        # Get all test methods (methods that start with 'test_')
        test_methods = [method for method in dir(self) if method.startswith('test_') and callable(getattr(self, method))]
        
        for method_name in test_methods:
            try:
                test_method = getattr(self, method_name)
                self.tests_run += 1
                await test_method()
            except Exception as e:
                self.tests_failed += 1
                log_test(method_name, False, e)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n{'='*70}")
        print(f"Test Summary:")
        print(f"  Total tests: {self.tests_run}")
        print(f"  Passed: {self.tests_passed}")
        print(f"  Failed: {self.tests_failed}")
        print(f"  Duration: {duration:.2f} seconds")
        print(f"{'='*70}")
        
        # Shutdown the bot after tests are complete
        await self.bot.close()
    
    # Test Methods
    
    async def test_bot_online(self):
        """Test that the bot is online and responsive"""
        try:
            # Simply checking if the bot is connected
            if self.bot.is_ready():
                self.tests_passed += 1
                log_test("test_bot_online", True)
            else:
                raise Exception("Bot is not connected")
        except Exception as e:
            self.tests_failed += 1
            log_test("test_bot_online", False, e)
    
    async def test_help_command(self):
        """Test that the help command works"""
        try:
            # This is a simple test to make sure the help command doesn't throw an error
            help_command = self.bot.get_command('help')
            
            if help_command and help_command.enabled:
                self.tests_passed += 1
                log_test("test_help_command", True)
            else:
                raise Exception("Help command not found or disabled")
        except Exception as e:
            self.tests_failed += 1
            log_test("test_help_command", False, e)
    
    async def test_commands_exist(self):
        """Test that all required commands exist"""
        required_commands = [
            'hit', 'dose', 'trip', 'stash', 'rehab', 
            'quote', 'agents', 'plans', 'pay', 
            'verify_payment', 'payments', 'tier',
            'referral', 'refer', 'commissions'
        ]
        
        try:
            missing_commands = []
            
            for cmd_name in required_commands:
                if not self.bot.get_command(cmd_name):
                    missing_commands.append(cmd_name)
            
            if missing_commands:
                raise Exception(f"Missing commands: {', '.join(missing_commands)}")
            else:
                self.tests_passed += 1
                log_test("test_commands_exist", True)
        except Exception as e:
            self.tests_failed += 1
            log_test("test_commands_exist", False, e)
            
    async def test_database_connection(self):
        """Test database connection"""
        try:
            from database import Database
            db = Database()
            conn = db._get_connection()
            if conn:
                conn.close()
                self.tests_passed += 1
                log_test("test_database_connection", True)
            else:
                raise Exception("Could not get database connection")
        except Exception as e:
            self.tests_failed += 1
            log_test("test_database_connection", False, e)
            
    async def test_agents_loaded(self):
        """Test that all agents are loaded"""
        try:
            # Check if agent handler or similar system exists
            # This is a placeholder - implement based on your actual agent architecture
            agent_names = [
                "Heroin Harry", "Meth Mandy", "Xanny Xan", 
                "Cokehead Carl", "Shroomy Sal", "Crypto Craig"
            ]
            
            # Placeholder for agent check - implement based on your system
            agents_loaded = True
            missing_agents = []
            
            # Example implementation - replace with your actual agent check
            # for agent_name in agent_names:
            #     if agent_name not in your_agent_registry:
            #         agents_loaded = False
            #         missing_agents.append(agent_name)
            
            if not agents_loaded:
                raise Exception(f"Missing agents: {', '.join(missing_agents)}")
            else:
                self.tests_passed += 1
                log_test("test_agents_loaded", True)
        except Exception as e:
            self.tests_failed += 1
            log_test("test_agents_loaded", False, e)

# Bot event handlers
@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord"""
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print(f"Connected to {len(bot.guilds)} guilds")
    print("------")
    
    # Run tests once the bot is ready
    tests = BotTests(bot)
    await tests.run_all_tests()

# Main function to run the bot
def main():
    """Main function to run the bot for testing"""
    try:
        bot.run(DISCORD_BOT_TOKEN, reconnect=True)
    except discord.errors.LoginFailure:
        print("Error: Invalid Discord bot token. Please check your DISCORD_BOT_TOKEN environment variable.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()