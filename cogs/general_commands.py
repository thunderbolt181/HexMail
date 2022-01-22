import discord
from discord.ext import commands
from extra_functions import save_or_check_user_info, send_embed

CHANNEL_HELP = """```1. .ping : Bot tells you its latency in ms.
2. .new_auth : Bot sends you a authorization link in your DM.
4. .summery : Bot send general info about your account if it's authorized.
5. .recent : Bot sends most recent email in your DM.```"""

class GeneralCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()
    
    @commands.command()
    async def ping(self,ctx):
        await ctx.channel.send(f'Bot ping is *{round(self.bot.latency)*1000}ms*')

    @commands.command()
    async def more(self,ctx):
        user = save_or_check_user_info(ctx.message.author)
        if str(ctx.message.author) != str(ctx.channel).split()[-1] or user != False:
            await ctx.send(CHANNEL_HELP)
        else:
            await ctx.author.send("Please send '.Hello' in general chat in bot server to start the process of authonitcation.")

    @commands.command()
    async def hello(self,ctx):
        if str(ctx.message.author) != str(ctx.channel).split()[-1]:
            save_or_check_user_info(ctx.message.author)
            embed = discord.Embed(
                title = "Taking first step to save you time",
                description="We will get you latest emails to you without any hassel.\n Type '.new_auth' to start authontication process",
                color = 0xFF5733
            )
            await send_embed(ctx,embed=embed)
        else:
            await ctx.channel.send("Please send '.Hello' in general chat in bot server to start the process of authonitcation.")

def setup(bot):
    bot.add_cog(GeneralCommands(bot))