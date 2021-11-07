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
    errorembed = discord.Embed(color=discord.Color(int("FF2E2E", 16)), title=f"Ignoring Exception in {ctx.command}:", description=f"```py\n{error}```")
    errorembed.timestamp = discord.utils.utcnow()
    channel = self.bot.get_channel(906683175571435550)
    await channel.send(embed=errorembed)
    await channel.send(f"This error came from {ctx.author} in {ctx.guild}.")
    await ctx.send(embed=errorembed)

def setup(bot):
  bot.add_cog(Error(bot))