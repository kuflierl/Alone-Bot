import sr_api
import discord
from discord.ext import flags, commands
import async_cleverbot as chatbot
from ext.useful import generate_embed
from datetime import datetime
import hmac
import string
import random
import asyncpraw
from waifuim import WaifuAioClient

reddit = asyncpraw.Reddit(
                       client_id="DW0OBpL8vJbwKT8Nhrhj3w",
                       client_secret="8Udwhvzmsv4vdwUnBkgAkhIRAsTxhA",
                       user_agent="NightSlasher35",
                       username="Alone Bot"
               )

client = sr_api.Client()
horiapi = WaifuAioClient(appname="Alone Bot")

class RandomAPIs(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def token(self, ctx):
   timestamp = datetime.utcnow().timestamp() + 1923840000
   time = "".join((random.choice(str("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")) for i in range(6)))
   enc = "".join((random.choice(str("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")) for i in range(27)))
   id = str(ctx.author.id)
   idenc = await client.encode_base64(id)
   await ctx.reply(embed=generate_embed("Your token is ready!", f"Hey,{ctx.author.name} your token is `{idenc}.{time}.{enc}`","Token | Alone Bot"), mention_author=False)
   
  @commands.command()
  async def joke(self, ctx):
   joke = await client.get_joke()
   await ctx.send(embed=generate_embed("I got a good one", joke, "Joke | Alone Bot"))
  
  @commands.command()
  async def pp(self, ctx, member: discord.Member=None):
   if member is None:
    ppsize = random.randint(1, 50)
    pp = "".join("="*ppsize)
    await ctx.reply(embed=generate_embed(f"{ctx.author.name}'s pp",f"8{pp}D\n({ppsize}cm)","PP | Alone Bot","ffcff1"), mention_author=False)
   else:
    ppsize = random.randint(1, 50)
    pp = "".join("="*ppsize)
    await ctx.reply(embed=generate_embed(f"{member}'s pp",f"8{pp}D\n({ppsize}cm)","PP | Alone Bot","ffcff1"), mention_author=False)
    
  @commands.command()
  @commands.cooldown(1, 1, commands.BucketType.user)
  async def meme(self, ctx):
   subreddit = await reddit.subreddit("dankmemes")
   async for submission in subreddit.hot(limit=1):
    embed = discord.Embed(color=discord.Color(int("2F3136", 16))).set_image(url=submission.url)
    await ctx.reply(embed=embed, mention_author=False)
  
  @commands.command()
  async def minecraft(self, ctx, username=None):
   if username is None:
    await ctx.reply(embed=generate_embed("Hey","You actually have to supply an account name","MC Lookup | Alone Bot"), mention_author=False)
   else:
    account = await client.mc_user(username)
    await ctx.reply(embed=generate_embed("I got the info", f"Current Name:{account.name}\nAccount Name History:\n{account.history}", "MC Lookup | Alone Bot"), mention_author=False)
    
  @commands.command()
  async def waifu(self, ctx):
   waifu_url = await horiapi.sfw('waifu')
   waifuembed = discord.Embed(title=f"Here is your waifu, {ctx.author.name}", description=f"Incase you're wondering, here's the link: {waifu_url}", color=discord.Color(int("2F3136", 16)))
   waifuembed.set_footer(text=f"Command ran by {ctx.author.name}")
   waifuembed.set_image(url=waifu_url)
   await ctx.send(embed=waifuembed)

def setup(bot):
  bot.add_cog(RandomAPIs(bot))
