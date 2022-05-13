import discord
from discord.ext import commands

class Moderation(commands.Cog):
  def __init__(self, bot):
  	self.bot = bot

  async def cog_check(self, ctx):
   if not ctx.guild:
   	return False
   return True

  @commands.command()
  @commands.bot_has_guild_permissions(ban_members=True)
  @commands.has_guild_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member = None, *, reason: str = None):
   if member == None:
   	await ctx.reply(embed=generate_embed("An error occured", "You need to provide a member to ban."))
   elif reason == None:
   	await member.ban(reason="No reason provided.")
   	await ctx.reply(f"Banned {member} for no reason.")
   else:
   	await member.ban(reason=reason)
   	await ctx.reply(f"Banned {member} for {reason}.")

  @commands.command()
  @commands.bot_has_guild_permissions(kick_members=True)
  @commands.has_guild_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member = None, *, reason: str = None):
   if member == None:
   	await ctx.reply(embed=generate_embed("An error occured", "You need to provide a member to kick."))
   elif reason == None:
   	await member.kick(reason="No reason provided.")
   	await ctx.reply(f"Kicked {member} for no reason.")
   else:
   	await member.kick(reason=reason)
   	await ctx.reply(f"Kicked {member} for {reason}.")

  @commands.command()
  @commands.bot_has_guild_permissions(manage_messages=True)
  @commands.has_guild_permissions(manage_messages=True)
  async def purge(self, ctx, limit: int=None):
   if not limit:
   	limit = 20
   messages = await ctx.channel.purge(limit=limit)
   await ctx.send(f"{len(messages)} messages deleted.", delete_after=15)

def setup(bot):
	bot.add_cog(Moderation(bot))