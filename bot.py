import discord
from discord.ext import commands
import discord.utils
from dotenv import load_dotenv
import os
import traceback
from webserver import keep_alive  # Import the keep_alive function

# Load environment variables from .env file
load_dotenv()

# Use the environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
ALLOWED_ROLE_ID_str = os.getenv('ALLOWED_ROLE_ID')
JOB_CHANNEL_ID_str = os.getenv('JOB_CHANNEL_ID')  # Channel ID for job postings
SERVICE_CHANNEL_ID_str = os.getenv('SERVICE_CHANNEL_ID')  # Channel ID for service postings

# Convert environment variables to integers
ALLOWED_ROLE_ID = int(ALLOWED_ROLE_ID_str) if ALLOWED_ROLE_ID_str else None
JOB_CHANNEL_ID = int(JOB_CHANNEL_ID_str) if JOB_CHANNEL_ID_str else None
SERVICE_CHANNEL_ID = int(SERVICE_CHANNEL_ID_str) if SERVICE_CHANNEL_ID_str else None

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command(name='postjob')
async def post_job(ctx, *, message: str):
    await post_to_channel(ctx, message, JOB_CHANNEL_ID, "New Job Posting")

@bot.command(name='postservices')
async def post_services(ctx, *, message: str):
    await post_to_channel(ctx, message, SERVICE_CHANNEL_ID, "New Service Offering")

@bot.command(name='post')
async def post(ctx, channel: discord.TextChannel, title: str, *, message: str):
    await post_to_any_channel(ctx, channel.id, title, message)

async def post_to_channel(ctx, message, channel_id, title):
    try:
        if channel_id is None:
            await ctx.send('Target channel not found.')
            return

        # Check if the author has the allowed role ID
        role = discord.utils.get(ctx.guild.roles, id=ALLOWED_ROLE_ID)
        if role in ctx.author.roles:
            channel = bot.get_channel(channel_id)
            if channel:
                embed = discord.Embed(
                    title=title,
                    description=message,
                    color=0xffd700  # Gold color for the embed border
                )
                # Add a footer to the embed
                embed.set_footer(text='- MoneyMotives Team')
                await channel.send(embed=embed)
                await ctx.message.delete()  # Delete the original command message
            else:
                await ctx.send('Target channel not found.')
        else:
            await ctx.send('You do not have the required role to use this command.')
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        await ctx.send('An error occurred while trying to execute the command.')

async def post_to_any_channel(ctx, channel_id, title, message):
    try:
        # Check if the author has the allowed role ID
        role = discord.utils.get(ctx.guild.roles, id=ALLOWED_ROLE_ID)
        if role in ctx.author.roles:
            channel = bot.get_channel(channel_id)
            if channel:
                embed = discord.Embed(
                    title=title,
                    description=message,
                    color=0xffd700  # Gold color for the embed border
                )
                # Add a footer to the embed
                embed.set_footer(text='- MoneyMotives Team')
                await channel.send(embed=embed)
                await ctx.message.delete()  # Delete the original command message
            else:
                await ctx.send('Target channel not found.')
        else:
            await ctx.send('You do not have the required role to use this command.')
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        await ctx.send('An error occurred while trying to execute the command.')

# Keep the web server alive
keep_alive()

if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN environment variable is not set.")
