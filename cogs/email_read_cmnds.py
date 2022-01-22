import discord
from discord.ext import commands
from request_gmail import get_emails, get_message, get_profile
from extra_functions import send_embed, save_or_check_user_info

class ReadEmails(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.command()
    async def summery(self, ctx):
        user = save_or_check_user_info(ctx.message.author)
        if str(ctx.message.author) != str(ctx.channel).split()[-1] or user != False:
            try:
                summery=get_profile(user['token'],ctx.message.author.id)
                summery_embed = discord.Embed(
                    title = "Your account summery",
                    description = summery,
                    color = discord.Color.blue()
                )
                await send_embed(ctx,embed=summery_embed)
            except Exception as error:
                print(error)
                if str(error).strip("'") == 'token':
                    await ctx.author.send("You are currently not authorized.\nType '.new_auth' to start authorization process.")
                else:
                    await ctx.author.send("Sorry We are having a bit of a problem")
        else:
            await ctx.channel.send("Please send '.Hello' in general chat in bot server to start the process of authonitcation.")

    @commands.command()
    async def recent(self, ctx):
        user = save_or_check_user_info(ctx.message.author)
        if str(ctx.message.author) != str(ctx.channel).split()[-1] or user != False:
            try:
                mail = get_emails(user['token'],ctx.message.author.id)
                for i in mail:
                    mail_content = str(get_message(i['id'],user['token'],ctx.message.author.id))
                    # await ctx.author.send('processing')
                    await ctx.author.send(mail_content)
            except Exception as error:
                print(error)
                if str(error).strip("'") == 'token':
                    await ctx.author.send("You are currently not authorized.\nType '.new_auth' to start authorization process.")
                else:
                    await ctx.author.send("Sorry We are having a bit of a problem")
        else:
            await ctx.channel.send("Please send '.Hello' in general chat in bot server to start the process of authonitcation.")

def setup(bot):
    bot.add_cog(ReadEmails(bot))