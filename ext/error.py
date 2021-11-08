
import discord
from b import BlackListedError, MaintenanceError
from discord.ext import commands


class Error(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
   if isinstance(error, commands.CommandNotFound):
    return
   elif isinstance(error, BlackListedError):
    reason = self.bot.blacklist.get(ctx.author.id)
    if reason:
     await ctx.send(f"Hi welcome. You got blacklisted. Now this is simple, you got blacklisted for {reason}, and you may not appeal, nor ask for an unban. If you got banned, it's for a reason. I will occasionally check who is banned and see if its worth unbanning or not.")
   elif isinstance(error, MaintenanceError):
    await ctx.send(f"The bot is currently in maintenance mode, please wait. The reason for this is {self.bot.maintenance_reason}")
   else:
    errorembed = discord.Embed(color=discord.Color(int("FF2E2E", 16)), title=f"Ignoring Exception in {ctx.command}:", description=f"```py\n{error}```")
    errorembed.timestamp = discord.utils.utcnow()
    channel = self.bot.get_channel(906683175571435550)
    await channel.send(embed=errorembed)
    await channel.send(f"This error came from {ctx.author} in {ctx.guild}.")
    await ctx.send(embed=errorembed)

def setup(bot):
  bot.add_cog(Error(bot))