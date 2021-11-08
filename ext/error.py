import discord
from discord.ext import commands

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
    await ctx.send(embed=errorembed)
    print(error)

def setup(bot):
  bot.add_cog(Error(bot))