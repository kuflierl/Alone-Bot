import sr_api
import discord
from discord.ext import flags, commands
import async_cleverbot as chatbot

client = sr_api.Client()

def generate_embed(header, content, footer):
  embed = discord.Embed()
  embed.title = header
  embed.description = content
  embed.color = discord.Color(int("2F3136", 16))
  embed.set_footer(text=footer)
  return embed

class RandomAPIs(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def token(self, ctx):
   token = await client.bot_token()
   await ctx.reply(embed=generate_embed("Your token is ready!", f"Hey,{ctx.author.name} your token is {token}.","Alone Bot"), mention_author=False)
   
  @commands.command()
  @commands.max_concurrency(1, commands.BucketType.member)
  async def chatbot(self, ctx):
   await ctx.reply(embed=generate_embed("Done!","I started a Chatbot session for you,to cancel just say \"stop fucking talking\" or \"Cancel\"!","Chatbot | Alone Bot"), mention_author=False)
   chatbot = chatbot.cleverbot(self.bot.config["CLEVERBOT"])
   while True:
    try:
     msg = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel, timeout=60)
    except asyncio.TimeoutError:
       await msg.reply(embed=generate_embed("Chatbot cancelled.","I cancelled your Chatbot session due to you being either afk or typing too slow","Chatbot | Alone Bot"), mention_author=False)
    break
   else:
    if msg.content.lower() is ["stop fucking talking", "Cancel", "cancel"]:
     await msg.reply(embed=generate_embed("Chatbot cancelled.","Ok,I stopped the Chatbot session.","Chatbot | Alone Bot"), mention_author=False)
    break
   finally:
    async with ctx.typing():
     mesg = await chatbot.ask(msg.content, msg.author.id)
     await msg.reply(embed=generate_embed("Here's the response:",f"{mesg.text}", "Chatbot | **Alone Bot**"), mention_author=False, allowed_mentions=discord.AllowedMentions.none())
   
def setup(bot):
  bot.add_cog(RandomAPIs(bot))