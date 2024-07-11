import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
import asyncio
from datetime import datetime, timedelta
import pytz

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TIMEZONE = os.getenv('TIMEZONE')

drink = False

# Intents are necessary for some functionality
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# Event for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

# Command to respond to '!hello'
@bot.command()
async def water(ctx, member: discord.Member, time: str, country_code: str):
    # Validate and parse the time parameter
    try:
        reminder_time = datetime.strptime(time, '%H:%M').time()
    except ValueError:
        await ctx.send('Please provide a valid time in the format HH:MM.')
        return
    
    try:
        timezone = ' '.join(pytz.country_timezones[country_code])
    except:
        await ctx.send('Wrong country code, check your country code in ISO 3166 standard.')
        return
    
    # Get the current time and the target time for the reminder
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    target_time = tz.localize(datetime.combine(now.date(), reminder_time))

    # Calculate the difference in seconds
    wait_time = (target_time - now).total_seconds()

    # Send an initial message
    await ctx.send(f'Okay, I will remind at {time} of {timezone} time.')

    # Wait for the specified amount of time
    await asyncio.sleep(wait_time)

    await ctx.send(f'{member.mention} DON\'T FORGET TO DRINK WATER')

# Run the bot with your token
bot.run(TOKEN)
