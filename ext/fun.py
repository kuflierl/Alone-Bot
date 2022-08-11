import discord, random, sr_api, asyncpraw, os, aiohttp
from discord.ext import commands
from waifuim import WaifuAioClient
from datetime import datetime


async def urban(word: str):
    async with bot.session as session:
        async with session.get(
            f"https://api.urbandictionary.com/v0/define?term={word}"
        ) as word:
            response = await word.json()
    return response


srapi = sr_api.Client()
hori = WaifuAioClient(session=aiohttp.ClientSession(), appname="Alone Bot")

reddit = asyncpraw.Reddit(
    client_id=os.environ["client_id"],
    client_secret=os.environ["client_secret"],
    user_agent=os.environ["user_agent"],
    username=os.environ["username"],
)


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["define"])
    async def urban(self, ctx: commands.Context, *, word: str):
        urbanapi = await urban(word)
        definition = urbanapi["list"][0]["definition"]
        name = urbanapi["list"][0]["word"]
        await ctx.reply(embed=discord.Embed(title=name, description=definition))

    @commands.command()
    async def token(self, ctx: commands.Context):
        time = await srapi.encode_base64(
            str(int(datetime.utcnow().timestamp()) + 1923840000)
        )
        encoded_id = await srapi.encode_base64(str(ctx.author.id))
        keys = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        enc = "".join((random.choice(keys) for i in range(27)))
        await ctx.reply(
            embed=discord.Embed(
                title="Here's your token!",
                description=f"Hey {ctx.author.mention}, here's your randomly generated token!\n`{encoded_id}.{time}.{enc}`",
            )
        )

    @commands.command()
    async def pp(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        ppsize = random.randint(1, 50)
        pp = "".join("=" * ppsize)
        await ctx.reply(
            embed=discord.Embed(
                title="{member}'s pp", description=f"8{pp}D\n({ppsize}cm)"
            )
        )

    @commands.command()
    async def meme(self, ctx: commands.Context):
        subreddit = await reddit.subreddit("dankmemes")
        meme = random.choice([post async for post in subreddit.new(limit=250)])
        embed = discord.Embed().set_image(url=meme.url)
        await ctx.reply(embed=embed)

    @commands.command()
    async def joke(self, ctx: commands.Context):
        joke = await srapi.get_joke()
        await ctx.reply(embed=discord.Embed(title="Joke", description=joke))

    @commands.command()
    async def waifu(self, ctx: commands.Context):
        waifu_url = await hori.random(is_nsfw=["False"], selected_tags=["waifu"])
        embed = discord.Embed(
            title=f"Here's your waifu, {ctx.author.name}",
            description=f"[Here's the link]({waifu_url})",
        )
        embed.set_image(url=waifu_url)
        await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
