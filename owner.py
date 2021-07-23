import discord
from discord.ext import commands

cogs = ["cogs.essential","cogs.owner"]
for cogs in cogs:

 def generate_embed(header, content, footer):
  embed = discord.Embed()

  embed.title = header
  embed.description = content
  embed.color = discord.Color(int("2F3136", 16))

  embed.set_footer(text=footer)

  return embed

class Owner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def disable(self, ctx, command):
    command = self.bot.get_command(command)
    if not command.enabled:
      return await ctx.reply(embed=generate_embed("Disable", "This command is already disabled.","Disable | Alone Bot"), mention_author=False, delete_after=5)
    command.enabled = False
    await ctx.reply(embed=generate_embed("Disable",f"Disabled {command.name} command.","Disable | Alone Bot"), mention_author=False, delete_after=5)

  @commands.command()
  @commands.is_owner()
  async def enable(self, ctx, command):
    command = self.bot.get_command(command)
    if command.enabled:
      return await ctx.reply(embed=generate_embed("Enable", "This command is already enabled.","Enable | Alone Bot"), mention_author=False, delete_after=5)
    command.enabled = True
    await ctx.reply(embed=generate_embed("Enable",f"Enabled {command.name} command.","Enable | Alone Bot"), mention_author=False, delete_after=5)

  @commands.command(aliases=["r"])
  @commands.is_owner()
  async def reload(self, ctx):
   await ctx.reply(embed=generate_embed("Reloaded all Cogs!","Reloaded all cogs!","Cogs | Alone Bot"), mention_author=False, delete_after=5)
   self.bot.reload_extension(cogs)
    
  @commands.command(aliases=["log","die","shutdown","fuckoff","dios"])
  @commands.is_owner()
  async def logout(self, ctx):
   await ctx.reply(embed=generate_embed("Logout","Logging out now...","Logout | Alone Bot"), mention_author=False, delete_after=5)
   await ctx.bot.close()

def setup(bot):
  bot.add_cog(Owner(bot))