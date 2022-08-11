import sys, os
import discord


from discord.ext import commands, ipc
from discord.ext.ipc.server import route
from discord.ext.ipc.errors import IPCError


class IPC(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @route()
    async def get_user_data(self, data):
        user = self.bot.get_user(data.user_id)
        return user._to_minimal_user_json()


async def setup(bot):
    await bot.add_cog(IPC(bot))
