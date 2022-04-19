import os
import discord
from discord.ext import commands
from database_functions import fetch_users_from_discord_id
from bot.modal import ComposeEmailModel
from discord.ui import button,Button, View
from discord import Interaction
from extra_functions import check_user

class ComposeEmailView(View):
    def __init__(self,user):
        self.user = user
        super().__init__(timeout=None)

    @button(label = 'Compose Mail', custom_id=os.urandom(16).hex(),style=discord.ButtonStyle.gray)
    async def compose_email(self,interaction : Button, button: Interaction):#something suspesious in declaring data type of parameters(they are cross related)
        await interaction.response.send_modal(ComposeEmailModel(self.user))

class SendEmails(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.command()
    async def sendmail(self,ctx):
        user = await fetch_users_from_discord_id(self.bot,ctx.message.author)
        if await check_user(ctx,user):
            if ctx.channel.name=="compose":
                await ctx.channel.send(view=ComposeEmailView(user))
            else:
                await ctx.message.delete()
                await ctx.channel.send("This channel is not for composing emails.\nPlease use #Compose channel.",delete_after=10)

async def setup(bot) -> None:
    await bot.add_cog(SendEmails(bot))