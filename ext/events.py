from discord.ext import commands
from ext.useful import generate_embed as gen_embed

class Events(commands.Cog):
  def __init__(self, bot):
   self.bot = bot
  
  @commands.Cog.listener()
  async def on_message_edit(self, before, message):
   await self.bot.process_commands(message)

  @commands.Cog.listener()
  async def on_message(self, message):
   if message.content == "<@784545186612510811>" or message.content == "@Alone Bot#5952" and not message.author.bot:
    await message.reply(embed=gen_embed("Roger that", "Hey you actually have to use a command ok thanks", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)

def setup(bot):
  bot.add_cog(Events(bot))
