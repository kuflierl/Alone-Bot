import discord
from discord.ext import commands
import traceback
import aiohttp
from ext.useful import generate_embed

class Error(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
   if isinstance(error, commands.CommandNotFound):
    return
   else:
    await ctx.send(embed=generate_embed(f"Ignoring exception in command {ctx.command}:", f"`{error}`","That's all I got for you | Alone Bot","FF2E2E"))

def setup(bot):
  bot.add_cog(Error(bot))
