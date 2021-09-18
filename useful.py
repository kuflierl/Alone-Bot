import discord
from discord.ext import commands, flags, tasks

def generate_embed(header, content, footer, color=None):
  embed = discord.Embed()
  embed.title = header
  embed.description = content
  if color is None:
   embed.color = discord.Color(int("2F3136", 16))
  else:
   embed.color = discord.Color(int(color, 16))
  embed.set_footer(text=footer)
  return embed

def yes(reaction, user):
         return user == ctx.message.author and str(reaction.emoji) == "\U00002705"
def no(reaction, user):
         return user == ctx.message.author and str(reaction.emoji) == "\U0000274c"

class Help(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            helpembed = discord.Embed(title="You asked for help?", description=f"Hey my commands are:\n{page}".strip("help"), color=discord.Color(int("5960d8", 16)))
            helpembed.set_footer(text="Help | Alone Bot")
            helpembed.set_image(url="https://cdn.discordapp.com/attachments/685035292989718554/724301857157283910/ezgif-1-a2a2e7173d80.gif")
            await destination.send(embed=helpembed)

class Useful(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def embed(self, ctx, title, content, footer=None):
   if footer is None:
    await ctx.send(embed=generate_embed(title, content, "Embed | Alone Bot"))
   else:
     await ctx.send(embed=generate_embed(title, content, footer))
     
def setup(bot):
  bot.add_cog(Useful(bot))