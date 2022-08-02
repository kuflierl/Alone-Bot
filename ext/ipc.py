import sys
import discord

from discord.ext import commands, ipc
from discord.ext.ipc.server import route
from discord.ext.ipc.errors import IPCError

class IPC(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if not hasattr(bot, "ipc"):
            bot.ipc = ipc.Server(self.bot, host="127.0.0.1", port=2300, secret_key=os.getenv("ipc_key"))
            bot.ipc.start(self)

    @commands.Cog.listener()
    async def on_ipc_ready(self):
        format = self.bot.format_print("IPC")
        print(f"{format} | Connected")

    
    @commands.Cog.listener()
    async def on_ipc_error(self, endpoint: str, error: IPCError):
        logging.error(f"An error has occurred in the ipc", exc_info=error)
    
    @route()
    async def get_user_data(self, data):
        user = self.bot.get_user(data.user_id)
        return user._to_minimal_user_json()

async def cog_unload(bot):
    bot.ipc = None
    format = self.bot.format_print("IPC")
    print(f"{format} | Disconnected")

async def cog_load(bot):
    if not hasattr(bot, "ipc"):
        bot.ipc = ipc.Server(self.bot, host="127.0.0.1", port=2300, secret_key=os.getenv("ipc_key"))
        bot.ipc.start(self)

async def setup(bot):
    await bot.add_cog(IPC(bot))