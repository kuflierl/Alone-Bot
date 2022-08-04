import sys, os
import discord
from dotenv import load_dotenv

load_dotenv()


from discord.ext import commands, ipc
from discord.ext.ipc.server import route
from discord.ext.ipc.errors import IPCError

class IPC(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if not hasattr(bot, "ipc"):
            format = self.bot.format_print("IPC")
            try:
                bot.ipc = ipc.Server(self.bot, host="127.0.0.1", port=2300, secret_key=os.getenv("ipc_key"))
                bot.ipc.start(self)
                print(f"{format} | Connected")
            except Exception as error:
                print(f"{format} | Errored!\n{error}")
    
    @route()
    async def get_user_data(self, data):
        user = self.bot.get_user(data.user_id)
        return user._to_minimal_user_json()
    
    async def cog_unload(bot):
        format = self.bot.format_print("IPC")
        bot.ipc_online = True if bot.ipc else False
        if bot.ipc:
            bot.ipc = None
            print(f"{format} | Disconnected")
        print("{format} | Unloaded")
    
    async def cog_load(bot):
        if not hasattr(bot, "ipc"):
            bot.ipc = ipc.Server(self.bot, host="127.0.0.1", port=2300, secret_key=os.getenv("ipc_key"))
            if not bot.ipc_online:
                bot.ipc.start(self)

async def setup(bot):
    await bot.add_cog(IPC(bot))