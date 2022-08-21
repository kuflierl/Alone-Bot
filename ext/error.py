import discord, os
from discord.ext import commands
from utils.bot import BlacklistedError, MaintenanceError
from utils.logger import logger


class Error(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      return
    elif isinstance(error, BlacklistedError):
      reason = self.bot.blacklist.get(ctx.author.id)
      await ctx.message.add_reaction(os.getenv("emoji_redTick"))
      await ctx.reply(f"You have been blacklisted for {reason}. you may not appeal this blacklist. There still exists a chance I'll unban you, but it's not likely.", mention_author=False, delete_after=20)
    elif isinstance(error, commands.CheckFailure):
      await ctx.message.add_reaction(os.getenv("emoji_redTick"))
      await ctx.reply(embed=self.bot.generate_embed(ctx, "Error", "You do not have permission to run this command!", "ea132c"), mention_author=False)
    elif isinstance(error, MaintenanceError):
      await ctx.message.add_reaction(os.getenv("emoji_redTick"))
      await ctx.reply(f"The bot is currently in maintenance mode for {self.bot.maintenance_reason}, please wait. If you have any issues, you can join my support server for help.", mention_author=False, delete_after=20)
    else:
      errorembed = discord.Embed(title=f"Ignoring exception in {ctx.command}:", description=f"```py\n{error}```", color=discord.Color(int("FF2E2E", 16)))
      errorembed.timestamp = datetime.utcnow()
      channel = self.bot.get_channel(int(os.getenv("error_logs_channel")))
      await channel.send(f"This error came from {ctx.author} using {ctx.command} in {ctx.guild}.", embed=errorembed)
      await ctx.message.add_reaction(os.getenv("emoji_redTick"))
      await ctx.reply(embed=errorembed, mention_author=False, delete_after=120)


async def setup(bot: commands.Bot):
    await bot.add_cog(Error(bot))
