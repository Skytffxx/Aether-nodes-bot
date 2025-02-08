from argon2 import __name__
import discord
from discord.ext import commands
import os
import aiohttp
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_STATUS = os.getenv('BOT_STATUS', 'Online')  # Fallback status
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Check for required environment variables
if not TOKEN or not WEBHOOK_URL:
    raise ValueError("Missing required environment variables: DISCORD_TOKEN or WEBHOOK_URL")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# Create bot instance
bot = commands.Bot(command_prefix='/', intents=intents)

# Function to send error messages to the webhook
async def send_error_to_webhook(error_message):
    async with aiohttp.ClientSession() as session:
        data = {
            "content": error_message
        }
        try:
            async with session.post(WEBHOOK_URL, json=data) as response:
                if response.status != 204:
                    logger.error(f"Failed to send error message to webhook: {response.status}")
        except Exception as e:
            logger.error(f"Exception occurred while sending error message to webhook: {e}")

# Load cogs asynchronously
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Loaded cog: {filename[:-3]}')
            except Exception as e:
                logger.error(f'Failed to load cog {filename[:-3]}: {e}')

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name=BOT_STATUS))
    await load_cogs()  # Load cogs when the bot is ready
    await bot.tree.sync()  # Sync slash commands

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown. Try again in {error.retry_after:.2f} seconds.')
    else:
        error_message = f'Error in command {ctx.command}: {error}'
        await send_error_to_webhook(error_message)  # Send error to webhook
        await ctx.send('An error occurred. The developers have been notified.')

# Run the bot
bot.run(TOKEN)