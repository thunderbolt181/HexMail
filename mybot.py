from logging import error
import os
from turtle import color
import discord
from discord.ext import commands
from discord import user, Member
from discord.utils import get
from dotenv import load_dotenv
import json
from gmail_auth import get_authorization_url,get_credentials
from request_gmail import get_emails, get_message, get_profile
from discord.errors import Forbidden

load_dotenv()

TOKEN = os.getenv('DISCORD-BOT-TOKEN')
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready(): #Turns the bot online
    print(f"We have logged in as {bot.user}")

class ping_cog(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.group(name='ping', invoke_without_command=True)
    async def ping(self,ctx):
        await ctx.channel.send(f'Bot ping is *{round(bot.latency)*1000}ms*')

    @ping.command(name='cmd')
    async def cmd_ping(self,ctx):
        await ctx.channel.send(f'Bot ping is *{round(bot.latency)*1000}ms* via commands')
    
def setup(bot):
    bot.add_cog(ping_cog(bot))

setup(bot)
bot.run(TOKEN)