import os
import discord
from discord.ext import commands
# from discord import user, Member
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD-BOT-TOKEN')

#Create a bot
bot = commands.Bot(command_prefix='.')
# bot Event
@bot.event
async def on_ready(): #Runs after the bots becomes online
    print(f"We have logged in as {bot.user}")

# Loading Cogs from other Modules present in Cogs folder
bot.load_extension('cogs.general_commands') # Contains general commands Ex. Ping, hello etc
bot.load_extension('cogs.email_auth_cmnds') # Contains Commands for email authorization Ex. new_auth, token etc
bot.load_extension('cogs.email_read_cmnds') # Contains Commands for reading emails Ex. recent, summery etc

bot.run(TOKEN)