import discord, asyncpg, random, aiohttp, sr_api, asyncpraw, base64, os
from discord.ext import commands
from waifuim import WaifuAioClient
from datetime import datetime

srapi = sr_api.Client()
hori = WaifuAioClient(session=aiohttp.ClientSession(), appname="Alone Bot")

reddit = asyncpraw.Reddit(
  client_id=os.getenv("client_id"),
  client_secret=os.getenv("client_secret"),
  user_agent=os.getenv("user_agent"),
  username=os.getenv("username"),
)

class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def token(self, ctx):
    time = await srapi.encode_base64(str(int(datetime.utcnow().timestamp()) + 1923840000))
    id = await srapi.encode_base64(str(ctx.author.id))
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    enc = "".join((random.choice(alphabet) for i in range(27)))
    await ctx.reply(embed=self.bot.generate_embed(ctx, "Here's your token!", f"Hey {ctx.author.mention}, here's your randomly generated token!\n`{id}.{time}.{enc}`"), mention_author=False)

    @commands.command()
    async def pp(self, ctx, member: discord.Member = None):
      if member is None:
        member = ctx.author
      ppsize = random.randint(1, 50)
      pp = "".join("=" * ppsize)
      await ctx.reply(embed=self.bot.generate_embed(ctx, f"{member}'s pp", f"8{pp}D\n({ppsize}cm)"), mention_author=False)

    @commands.command()
    async def meme(self, ctx):
      subreddit = await reddit.subreddit("dankmemes")
      meme = random.choice([post async for post in subreddit.new(limit=250)])
      embed = discord.Embed().set_image(url=meme.url)
      await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def joke(self, ctx):
      joke = await srapi.get_joke()
      await ctx.reply(embed=self.bot.generate_embed(ctx, "Joke", joke), mention_author=False)

    @commands.command()
    async def waifu(self, ctx):
      waifu_url = await hori.random(is_nsfw=["False"], selected_tags=["waifu"])
      embed = discord.Embed(title=f"Here's your waifu, {ctx.author.name}", description=f"[Here's the link]({waifu_url})")
      embed.set_footer(text=f"Command ran by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
      embed.set_image(url=waifu_url)
      await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
  bot.add_cog(Fun(bot))
