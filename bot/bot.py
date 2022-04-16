import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import asyncpg
from bot.push_notification import main
from bot import __version__

load_dotenv()

#Environment Variables
TOKEN = os.getenv('DISCORD-BOT-TOKEN') # Discord Token
DB_NAME = os.getenv('DB_NAME') # Database name
DB_USER = os.getenv('DB_USER') # Database user
DB_PASSWORD = os.getenv('DB_PASSWORD') # Database user

class Bot(commands.Bot):
    def __init__(self, command_prefix = ".") -> None:#, help_command: Optional[HelpCommand] = ..., tree_cls: Type[app_commands.CommandTree[Any]] = ..., description: Optional[str] = None, **options) -> None:
        self.bot_intents = discord.Intents().default()
        self.bot_intents.message_content = True
        self.bot_intents.members = True
        super().__init__(command_prefix,intents = self.bot_intents)#, help_command, tree_cls, description, **options)
        self.db = None
        self.role = "Email Moderator"
        self.cog_extension = [
            "bot.cogs.general_commands",
            "bot.cogs.email_auth_cmnds",
            "bot.cogs.email_read_cmnds",
            "bot.cogs.email_send_cmnds"
        ]

    async def setup_hook(self) -> None: # This async function is auto called to further setup the bot
        print("Running Setup ...")
        await self.create_db_pool()
        for cogs in self.cog_extension:
            await self.load_extension(cogs)
        self.push_notification.start()
    
    async def create_db_pool(self) -> None: # Database Connection
        self.db = await asyncpg.create_pool(database = DB_NAME, user = DB_USER, password = DB_PASSWORD)
        print(F"Connection To Database:{DB_NAME} successful")

    @tasks.loop(seconds=1)
    async def push_notification(self):
        if PIPE_CONN.poll():
            data = PIPE_CONN.recv()
            await main(data,self)

    @push_notification.before_loop
    async def before_printer(self) -> None:
        await self.wait_until_ready()

    async def on_ready(self):
        print(f"Hexmail v{__version__} is online!")
        print(f"We have logged in as: {self.user}")

bot = Bot()

def run(conn) -> None:
    global PIPE_CONN 
    PIPE_CONN = conn # Connection to one side of Pipe
    bot.run(TOKEN) # run the bot

if __name__=="__main__":
    bot.run(TOKEN)