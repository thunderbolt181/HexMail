import os
import discord
import json
from discord.ext import commands
from gmail.gmail_cmnds import service
from gmail.gmail_auth import get_authorization_url,get_credentials
from extra_functions import check_user
from database_functions import delete_user_token, fetch_users_from_discord_id

class Authorization(commands.Cog):
    """
        This Cog containg the commands for user authorization and setup.
        Commands:
            .new_authorization(.new_auth) :
                Fetches Authorization like from [get_authorization_url()] and send it to user
            
            .token <TOKEN> :
                Takes the token provided by user, authorize it and fetches user credential from gmail
                [get_credentials()] and saves it to database and create and set up a category for discord
                user [user_setup()]
    """

    def __init__(self,bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.command(aliases=['new_auth'])
    async def new_authorization(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name=self.bot.role)
        if role in ctx.message.author.roles:
            user = await fetch_users_from_discord_id(self.bot,ctx.message.author)
            if await check_user(ctx,user,new_auth=True):
                url = get_authorization_url()
                url_embed = discord.Embed(
                    title = "Click to go to verification page",
                    url=f"{url}",
                    description = 'To authorize type => .token <YOUR_TOKEN>  here only .\n Warning do not share your auth token.',
                    color=0xFF5733
                )
                await ctx.channel.send(embed=url_embed)
        else:
            await ctx.channel.send(f"Sorry {ctx.message.author}. You do Not have required permissions")

    @commands.command()
    async def token(self, ctx,token):
        user = await fetch_users_from_discord_id(self.bot,ctx.message.author)
        if await check_user(ctx,user,new_auth=True):
            await ctx.channel.send(f"Your authorization token is processing.")
            cred=get_credentials(authorization_code=token)
            if cred != None:
                token = json.loads(cred.to_json())
                email = await self.get_email(token)
                category_id = await self.user_setup(ctx,email)
                details = await self.bot.db.fetchrow("SELECT * FROM user_token WHERE email = $1",email)
                if details is not None:
                    await ctx.channel.send(f"Sorry {email} is already authorized")
                else:
                    try:
                        await self.bot.db.execute("""
                        INSERT INTO user_token (email,token,category_id,fk_user) VALUES
                        ($1,$2,$3,(SELECT discord_id FROM users WHERE discord_id = $4))
                        """,email,str(token),str(category_id),str(ctx.message.author.id))
                        success=True
                    except Exception as e:
                        success=False
                    if success:
                        await ctx.channel.send(f"Congratulations {ctx.message.author},You have verified successfully. Type '.more' for more help")
                    else:
                        await ctx.channel.send(f"Sorry something went wrong.")
            else:
                await ctx.channel.send("There is something wrong with your token. Please check again")
        await ctx.message.delete()

    @commands.command(aliases=['d'])
    async def deauthorize(self,ctx,email):
        role = discord.utils.get(ctx.guild.roles, name=self.bot.role)
        if role in ctx.message.author.roles:
            user = await fetch_users_from_discord_id(self.bot,ctx.message.author)
            if await check_user(ctx,user,deauth=True):
                delete = await delete_user_token(self.bot,email)
                if delete:await ctx.channel.send(f"Email:{email} is deauthorized.")
                else:await ctx.channel.send(f"Failed.\nEmail:{email} was not authorized.")
        else:
            await ctx.channel.send(f"Sorry {ctx.message.author}. You do Not have required permissions")

    async def get_email(self,token):
        service_obj = service(token)
        profile = service_obj.get_profile(for_user_token=True)
        return profile['emailAddress']

    async def user_setup(self,ctx,email):
        """GENERAL,INBOX,SENT,STARRED,SPAM"""
        guild = ctx.message.guild
        gmail_tabs = ["COMPOSE","CATEGORY_PERSONAL","CATEGORY_SOCIAL","CATEGORY_PROMOTIONS","SENT","SPAM"]
        category_id = None
        role = discord.utils.get(ctx.guild.roles, name=self.bot.role)
        member = ctx.message.author
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True),
            member: discord.PermissionOverwrite(read_messages=True,  send_messages = True, attach_files = True)
        }
        email_category = discord.utils.get(guild.categories, name = email)
        if email_category is None:
            email_category = await guild.create_category(email)
            email_category = email_category
            category_id=email_category.id
        else:
            category_id = email_category.id
        await email_category.edit(overwrites=overwrites)
        for text_channel in email_category.channels:
            if text_channel.name.upper() in gmail_tabs:gmail_tabs.remove(text_channel.name.upper())
        for tab in gmail_tabs:
            await guild.create_text_channel(tab, category=email_category)
        return category_id

async def setup(bot):
    await bot.add_cog(Authorization(bot))