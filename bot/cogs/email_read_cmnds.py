import discord
from discord.ext import commands
from gmail.gmail_cmnds import service
from extra_functions import longer_msg, send_embed,check_user
from database_functions import fetch_users_from_discord_id
import json

class ReadEmails(commands.Cog):
    """
        This Cog is for reading email from autorized user
        Commands:
            .summary :
                returns a basic summary of users gmail account
            
            .recent :
                returns latest email to the user

            .recent last <AMOUNT>:
                returns last <AMOUNT> of email to the user

            .search <KEYWORD> :
                returns the result of the search.

            .call_watch :
                returns historyId and watchExpiration for push Notification.
    """
    def __init__(self,bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.command()
    async def summary(self,ctx):
        user = await fetch_users_from_discord_id(self.bot,ctx.message.author)
        if await check_user(ctx,user):
            token = json.loads(user['token'].replace("'",'"'))
            service_obj = service(token)
            summary=service_obj.get_profile()
            summery_embed = discord.Embed(
                title = "Your account summary",
                description = summary,
                color = discord.Color.blue()
            )
            await send_embed(ctx,embed=summery_embed)

    @commands.group(name='recent', invoke_without_command=True)
    async def recent(self, ctx):
        user = await fetch_users_from_discord_id(self.bot,ctx.message.author)
        if await check_user(ctx,user):
            token = json.loads(user['token'].replace("'",'"'))
            service_obj = service(token)
            mail = service_obj.get_emails()
            for i in mail:
                mail_content = service_obj.get_message(i['id'],True)
                message=''
                try:
                    for i in mail_content.keys():
                        if 'body'==i:
                            continue
                        message+=f"\n[{i}]: {mail_content[i]}"
                    await ctx.channel.send(f"```ini\n{message}```")
                    if "body" in mail_content.keys():
                        if len(mail_content['body'])<2000:
                            await ctx.channel.send(f"{mail_content['body']}")
                        else:await longer_msg(ctx,mail_content['body'])
                except Exception as e:
                    print(e)

    @recent.command(name='last')
    async def last(self,ctx,amount=1):
        user = await fetch_users_from_discord_id(self.bot,ctx.message.author)
        if await check_user(ctx,user):
            token = json.loads(user['token'].replace("'",'"'))
            service_obj = service(token)
            mail = service_obj.get_emails(amount)
            for i in mail:
                mail_content = service_obj.get_message(i['id'])
                message=''
                for i in mail_content.keys():
                    message+=f"\n[{i}]: {mail_content[i]}"
                await ctx.channel.send(f"```ini\n{message}```")
        
    @commands.command()
    async def search(self,ctx,*search_string):
        user = await fetch_users_from_discord_id(self.bot,ctx.message.author)
        if await check_user(ctx,user):
            token = json.loads(user['token'].replace("'",'"'))
            service_obj = service(token)
            mail = service_obj.search_email(' '.join(search_string))
            if mail['resultSizeEstimate']!=0:
                for i in mail['messages']:
                    mail_content = service_obj.get_message(i['id'],False)
                    message=''
                    for i in mail_content.keys():
                        message+=f"\n[{i}]: {mail_content[i]}"
                    await ctx.channel.send(f"```ini\n{message}```")
            else:
                await ctx.channel.send("Sorry No Results Found")

    @commands.command()
    async def call_watch(self,ctx):
        user = await fetch_users_from_discord_id(self.bot,ctx.message.author)
        if await check_user(ctx,user):
            token = json.loads(user['token'].replace("'",'"'))
            service_obj = service(token)
            result = service_obj.call_watch()
            if 'historyId' in result.keys():
                await self.bot.db.execute("""
                UPDATE user_token
                SET history_id = $1,
                watch_exp = $2
                WHERE email = $3;
                """,int(result['historyId']),str(result['expiration']),user['email'])
                await ctx.channel.send(f"Push Notification Emabled for: {str(ctx.message.author)}")
            else:
                await ctx.channel.send('Some error occured while emabling push notificaitons for your email')

async def setup(bot):
    await bot.add_cog(ReadEmails(bot))