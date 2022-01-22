import discord
import json
from discord.ext import commands
from gmail_auth import get_authorization_url,get_credentials
from extra_functions import save_or_check_user_info, send_embed, save_user

class Authorization(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.command(aliases=['new_auth'])
    async def new_authorization(self, ctx):
        user = save_or_check_user_info(ctx.message.author)
        if str(ctx.message.author) != str(ctx.channel).split()[-1] or user != False:
            if 'token' not in user.keys():
                url = get_authorization_url()
                url_embed = discord.Embed(
                    title = "Click to go to verification page",
                    url=f"{url}",
                    description = 'To authorize type => .token <YOUR_TOKEN>  here only .\n Warning do not share your auth token.',
                    color=0xFF5733
                )
                await send_embed(ctx,embed=url_embed)
            else:
                await ctx.author.send('You are already authorized from our app. type ".more" for more help')
        else:
            await ctx.channel.send("Please send '.Hello' in general chat in bot server to start the process of authonitcation.")

    @commands.command()
    async def token(self, ctx):
        token = ctx.message.content.split('.token')[-1].strip()
        user = save_or_check_user_info(ctx.message.author)
        if str(ctx.message.author) != str(ctx.channel).split()[-1] or user != False:
            if str(ctx.message.author) == str(ctx.channel).split()[-1]:
                if 'token' not in user.keys():
                    await ctx.author.send(f"Your authorization token is processing.")
                    cred=get_credentials(authorization_code=token)
                    user['token']=json.loads(cred.to_json())
                    if save_user(user,ctx.message.author.id):
                        await ctx.author.send(f"Congratulations {ctx.message.author},You have verified successfully. Type '.more' for more help")
                    else:
                        await ctx.author.send("There is something wrong")
                else:
                    await ctx.author.send(f'You are already authorized from our app. type ".more" for more help')
            else:
                await ctx.message.delete()
                await ctx.author.send("Please do not send token in server as it is confedential Informaiton.Please Send token in your personal chat.\n We have deleted your token from public chat as a safty precaution.")
        else:
            await ctx.channel.send("Please send '.Hello' in general chat in bot server to start the process of authonitcation.")

def setup(bot):
    bot.add_cog(Authorization(bot))