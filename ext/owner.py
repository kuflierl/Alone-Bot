import discord, os
from discord.ext import commands
from datetime import datetime

class Owner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def cog_check(self, ctx):
    return await self.bot.is_owner(ctx.author)

  @commands.command()
  async def maintenance(self, ctx, *, reason="No reason provided."):
    if self.bot.maintenance is False:
      await ctx.message.add_reaction("\U00002705")
      self.bot.maintenance = True
      self.bot.maintenance = reason
      channel = self.bot.get_channel(int(os.getenv("maintenance_announcement_channel")))
      await channel.send("I am going on maintenance break, all commands will not work during the downtime.")
    else:
      await ctx.reply("Maintenance break is over.", mention_author=False)
      channel = self.bot.get_channel(int(os.getenv("maintenance_announcement_channel")))
      await channel.send("The maintenance break is over. You can use me again.")
      self.bot.maintenance = False
      self.bot.maintenance_reason = ""

  @commands.group(invoke_without_command=True)
  async def blacklist(self, ctx):
    for user in self.bot.userblacklist:
      reason = user["reason"]
      profile = "".join(f"{user}, {reason}\n")
    await ctx.reply(embed=self.bot.generate_embed("Blacklisted users", profile), mention_author=False)

  @blacklist.command()
  async def add(self, ctx, id: discord.Member, reason: str = "No reason provided"):
    # db here
    self.bot.userblacklist[id.id] = reason
    await ctx.message.add_reaction("\U00002705")

  @blacklist.command()
  async def remove(self, ctx, id: discord.Member):
    try:
      self.userblacklist.pop(id.id)
    except KeyError:
      await ctx.message.add_reaction("\U0000274c")
      return await ctx.reply("That user isn't blacklisted!", mention_author=False)
    await ctx.message.add_reaction("\U00002705")

  @commands.command()
  async def disable(self, ctx, command):
    command = self.bot.get_command(command)
    if not command.enabled:
      await ctx.message.add_reaction("<:redTick:596576672149667840>")
      return await ctx.reply("This command is already disabled!", mention_author=False)
    command.enabled = False
    await ctx.message.add_reaction("\U00002705")
    await ctx.reply(f"Disabled {command}.", mention_author=False)

  @commands.command()
  async def enable(self, ctx, command):
    command = self.bot.get_command(command)
    if command.enabled:
      await ctx.message.add_reaction("\U00002705")
      return await ctx.reply("This command is already enabled!", mention_author=False)
    command.enabled = True
    await ctx.message.add_reaction("\U00002705")
    await ctx.reply(f"Enabled {command}.", mention_author=False)

  @commands.command()
  async def print(self, ctx, *, arg=None):
    if not arg:
      await ctx.message.add_reaction("<:redTick:596576672149667840>")
      await ctx.reply("Why are you trying to print nothing? why?", mention_author=False)
    print(arg)
    await ctx.message.add_reaction("\U00002705")

  @commands.command()
  async def say(self, ctx, *, arg=None):
    if not arg:
      await ctx.message.add_reaction("<:redTick:596576672149667840>")
      return await ctx.reply("You have to give me something to say.", mention_author=False)
    await ctx.message.add_reaction("\U00002705")
    await ctx.reply(arg, mention_author=False)

  @commands.command(aliases=["d", "delete"])
  async def delmsg(self, ctx, id=None):
    if not id:
      await ctx.message.add_reaction("<:redTick:596576672149667840>")
      return await ctx.reply("You need to give me a message to delete.", delete_after=10, mention_author=False)
    msg = await ctx.channel.fetch_message(id)
    await msg.delete()
    await ctx.message.add_reaction("\U00002705")

  @commands.command()
  async def nick(self, ctx, *, name=None):
    if not name:
      await ctx.me.edit(nick=None)
      await ctx.message.add_reaction("\U00002705")
    await ctx.me.edit(nick=name)
    await ctx.message.add_reaction("\U00002705")

  @commands.command(aliases=["log", "die", "shutdown", "fuckoff"])
  async def logout(self, ctx):
    await ctx.message.add_reaction("\U00002705")
    await ctx.bot.close()

  @commands.command()
  async def leave(self, ctx, id=None):
    if not id:
      await ctx.message.add_reaction("\U00002705")
      await ctx.guild.leave()
    guild = await guild.fetch(id)
    await guild.leave()
    await ctx.message.add_reaction("\U00002705")

  @commands.command()
  async def reload(self, ctx):
    for cog in self.bot.extensions.copy():
      self.bot.reload_extension(cog)
      await ctx.message.add_reaction("\U00002705")

def setup(bot):
  bot.add_cog(Owner(bot))
