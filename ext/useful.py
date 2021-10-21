import discord
from discord.ext import commands, flags, tasks

class Useful(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

def generate_embed(header, content, footer, icon, color=None):
  embed = discord.Embed()
  embed.title = header
  embed.description = content
  if color is None:
   embed.color = discord.Color(int("2F3136", 16))
  else:
   embed.color = discord.Color(int(color, 16))
  embed.set_footer(text=footer, icon_url=icon)
  embed.timestamp = discord.utils.utcnow()
  # embed.set_footer(text=f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", icon_url=member.avatar.url)
  return embed
     
def setup(bot):
  bot.add_cog(Useful(bot))