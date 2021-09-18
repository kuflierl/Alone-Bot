import discord
from discord.ext import flags, commands, tasks
from ext.useful import generate_embed

class Moderation(commands.Cog):
  def __init__(self, bot):
   self.bot = bot

  @commands.command()
  @commands.guild_only()
  @commands.bot_has_guild_permissions(ban_members=True)
  @commands. has_guild_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member = None, *, reason: str = None):
   if member == None:
    await ctx.send(embed=generate_embed("An error occurred","You need to provide a member.","Alone Bot"))
   elif reason == None:
    await member.ban(reason="No reason provided.")
    await ctx.send(embed=generate_embed("Snapped",f"Banned {member} but no reason was provided.","Alone Bot"))
   else:
    await member.ban(reason=reason)
    await ctx.send(embed=generate_embed("Snapped",f"Banned {member} for {reason}.","Alone Bot"))
  
  @commands.command()
  @commands.guild_only()
  @commands.is_owner()
  async def leave(self, ctx):
   if id is None:
    await ctx.reply(embed=generate_embed("You need more IQ","You need to provide a guild id","Alone Bot"), mention_author=False)
   else:
    guild = client.get_guild(int(id))
    await ctx.send("Leaving {guild}...", delete_after=3)
    guild.leave()
    await ctx.send("Done", delete_after=3)
  
  @commands.command()
  @commands.guild_only()
  @commands.bot_has_guild_permissions(kick_members=True)
  @commands. has_guild_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member = None, *, reason: str = None):
   if member == None:
    await ctx.send(embed=generate_embed("An error occurred","You need to provide a member.","Alone Bot"))
   elif reason == None:
    await member.kick(reason=f"{ctx.author.id} {ctx.author}: No reason provided.")
    await ctx.send(embed=generate_embed("Snapped",f"Kicked {member} but no reason was provided like normal. ¯\_(ツ)_/¯","Alone Bot"))
   else:
    await member.kick(reason=reason)
    await ctx.send(embed=generate_embed("Snapped",f"Kicked {member} for {reason}.","Alone Bot"))

def setup(bot):
  bot.add_cog(Moderation(bot))