import discord
from discord.ext import commands
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
    await ctx.reply(embed=generate_embed("An error occurred","You need to provide a member.", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
   elif reason == None:
    await member.ban(reason="No reason provided.")
    await ctx.reply(embed=generate_embed("Snapped",f"Banned {member} but no reason was provided.", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
   else:
    await member.ban(reason=reason)
    await ctx.reply(embed=generate_embed("Snapped",f"Banned {member} for {reason}.", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
  
  @commands.command()
  @commands.guild_only()
  @commands.is_owner()
  async def leave(self, ctx, id=None):
   if id is None:
    await ctx.reply("Leaving this guild because no argument was supplied.", mention_author=False)
    await guild.leave()
   else:
    guildleave = await guild.fetch(id)
    message = await ctx.reply(f"Leaving {guild.name}....", mention_author=False)
    await guildleave.leave()
    await message.edit("Done")

  @commands.command()
  @commands.guild_only()
  @commands.bot_has_guild_permissions(kick_members=True)
  @commands. has_guild_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member = None, *, reason: str = None):
   if member == None:
    await ctx.reply(embed=generate_embed("An error occurred","You need to provide a member.", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
   elif reason == None:
    await member.kick(reason=f"{ctx.author.id} {ctx.author}: No reason provided.")
    await ctx.reply(embed=generate_embed("Snapped",f"Kicked {member} but no reason was provided like normal. ¯\_(ツ)_/¯", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
   else:
    await member.kick(reason=reason)
    await ctx.reply(embed=generate_embed("Snapped",f"Kicked {member} for {reason}.", "Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)

def setup(bot):
  bot.add_cog(Moderation(bot))