from discord.ext import commands 
from ext.useful import generate_embed
from datetime import datetime

class Owner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def revealtoken(self, ctx):
   await ctx.send("Are you sure you want to make my token invalid? If so, use the secret command 'tokenreveal'")
  
  @commands.command()
  @commands.is_owner()
  async def maintenance(self, ctx, *, reason="No reason provided"):
   if self.bot.maintenance is True:
    await ctx.send("Ok, maintenance mode is over.")
    self.bot.maintenance = False
    self.bot.maintenance_reason = ""
   else:
    await ctx.send("Maintenance time? oh boi what did you fuck up.")
    self.bot.maintenance = True
    self.bot.maintenance_reason = reason
  
  @commands.command(aliases=["unbl", "ubl"])
  @commands.is_owner()
  async def unblacklist(self, ctx, id: discord.Member):
   await self.bot.db.execute("delete from blacklist where user_id = $1", id.id)
   try:
    self.bot.blacklist.pop(id.id)
    await ctx.send("I unblacklisted that person.")
   except KeyError:
    await ctx.send("That person isn't blacklisted!")

  @commands.command(aliases=["bl"])
  @commands.is_owner()
  async def blacklist(self, ctx, id: discord.Member, *, reason=None):
   if reason is None:
    reason = "No reason provided."
   await self.bot.db.execute("INSERT INTO blacklist ( user_id, reason, time) VALUES ($1, $2, $3)", id, reason, discord.utils.utcnow().timestamp())
   self.bot.blacklist.update({id.id: reason})
  
  @commands.command(hidden=True)
  @commands.is_owner()
  async def tokenreveal(self, ctx):
   await ctx.send("Ok, goodbye for now i guess.")
   channel = await self.bot.fetch_channel(381963689470984203)
   await channel.send(self.bot.http.token)
   await ctx.bot.logout()

  @commands.command()
  @commands.is_owner()
  async def disable(self, ctx, command):
    command = self.bot.get_command(command)
    if not command.enabled:
      return await ctx.reply(embed=generate_embed("Disable", "This command is already disabled.", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False, delete_after=5)
    command.enabled = False
    await ctx.reply(embed=generate_embed("Disable",f"Disabled {command.name} command.", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False, delete_after=5)
  
  @commands.command(aliases=["terminalclear"])
  @commands.is_owner()
  async def clear_terminal(self, ctx):
   print("[H[2J[3J")
  
  @commands.command()
  @commands.is_owner()
  async def print(self, ctx, *, arg):
   print(arg)
  
  @commands.command()
  @commands.is_owner()
  async def say(self, ctx, *, arg=None):
   if arg is None:
    await ctx.reply(embed=generate_embed("You know what went wrong","You need to give me a message", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
   else:
     await ctx.reply(embed=generate_embed("", arg, f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
  
  @commands.command()
  @commands.is_owner()
  async def enable(self, ctx, command):
    command = self.bot.get_command(command)
    if command.enabled:
      return await ctx.reply(embed=generate_embed("Enable", "This command is already enabled.", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False, delete_after=5)
    command.enabled = True
    await ctx.reply(embed=generate_embed("Enable",f"Enabled {command.name} command.", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False, delete_after=5)

  @commands.command(aliases=["r"])
  @commands.is_owner()
  async def reload(self, ctx):
   cogs = ["ext.essential","ext.owner","ext.moderation","ext.error","ext.sql","ext.events","ext.minecord","ext.random"]
   for cogs in cogs:
    self.bot.reload_extension(cogs)
   await ctx.reply(embed=generate_embed("Reloaded all Cogs!","Reloaded all cogs!", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url, "0C9027"), mention_author=False, delete_after=5)
  
  @commands.command(aliases=["delete", "msgdel"])
  @commands.is_owner()
  async def delmsg(self, ctx, msgid=None):
   if msgid is None:
    await ctx.reply("You need to give me an id.", mention_author=False)
   else:
    channel = ctx.channel
    msg = await channel.fetch_message(msgid)
    await msg.delete()
    await ctx.reply("Done", mention_author=False, delete_after=3)
  
  @commands.command()
  @commands.is_owner()
  async def nick(self, ctx, *, name=None):
   if name == None:
    await ctx.me.edit(nick=None)
    await ctx.reply(embed=generate_embed("Roger", "My nickname has been reset.", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
   else:
    await ctx.me.edit(nick=name)
    await ctx.reply(embed=generate_embed("I have changed my identity", f"My new nick is \"{name}\".", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
  
  @commands.command(aliases=["log","die","shutdown","fuckoff","dios"])
  @commands.is_owner()
  async def logout(self, ctx):
   await ctx.reply(embed=generate_embed("Logout","Logging out now...", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False, delete_after=5)
   await ctx.bot.close()

def setup(bot):
  bot.add_cog(Owner(bot))