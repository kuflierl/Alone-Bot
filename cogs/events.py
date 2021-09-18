from discord.ext import commands
from ext.useful import generate_embed

class Events(commands.Cog):
  def __init__(self, bot):
   self.bot = bot
   
  @commands.Cog.listener()
  async def on_message_edit(self, before, message):
   await self.bot.process_commands(message)
   
  @commands.Cog.listener()
  async def on_message(self, message):
   if message.content == "<@784545186612510811>" or message.content == "@Alone Bot#5952" and not message.author.bot:
    await message.reply(embed=generate_embed("Roger that", "Hey you actually have to use a command ok thanks", "Alone Bot"), mention_author=False)

   if message.content == "!a" or message.content == "•" and not message.author.bot:
    await message.reply(embed=generate_embed("Roger that", "Hey you actually have to use a command ok thanks", "Alone Bot"), mention_author=False)

def setup(bot):
  bot.add_cog(Events(bot))
