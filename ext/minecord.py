from discord.ext import commands
from datetime import datetime
import asyncpg
from ext.useful import generate_embed
import random

class Minecord(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def nuke(self, ctx):
   await self.bot.db.execute("DROP TABLE minecord")
   await self.bot.db.execute("CREATE TABLE minecord ( user_id BIGINT PRIMARY KEY, wood BIGINT, stone BIGINT, obsidian BIGINT, coal BIGINT, iron BIGINT, gold BIGINT, redstone BIGINT, lapis BIGINT, diamond BIGINT, emerald BIGINT, quartz BIGINT, coins BIGINT, pickaxe BIGINT NOT NULL, axe BIGINT NOT NULL, pet BIGINT )")
   await ctx.reply("I nuked the database and deleted everyone's info in minecord.", mention_author=False)
 
  @commands.command()
  async def mine(self, ctx):
   table = await self.bot.db.fetchrow("SELECT * FROM minecord WHERE user_id = $1", ctx.author.id)
   if not table:
       await self.bot.db.execute("INSERT INTO minecord (user_id, wood, stone, obsidian, coal, iron, gold, redstone, lapis, diamond, emerald, quartz, coins, pickaxe, axe, pet) VALUES ($1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0, 0)", ctx.author.id)
       return await ctx.reply("I made a profile for you due to you not having one, if you did please contact my developer about it. Anyways welcome to Minecord!", mention_author=False)
   pickaxe = table["pickaxe"]
   stone = table["stone"]
   coal = table["coal"]
   iron =  table["iron"]
   ironn = random.randint(0 + pickaxe, 0 + pickaxe)
   ironnn = iron + ironn
   coall = random.randint(5 + pickaxe, 25 + pickaxe)
   coalll = coal + coall
   stonee = random.randint(10 + pickaxe, 30 + pickaxe)
   stoneee = stonee + stone
   await self.bot.db.execute(f"UPDATE minecord SET stone = $1", stoneee)
   await self.bot.db.execute(f"UPDATE minecord SET iron = $1", ironnn)
   await self.bot.db.execute(f"UPDATE minecord SET coal = $1", coalll)
   await ctx.reply(f"You mined {stonee} stone, {ironn} iron and {coalll} coal! Now you have {stoneee} stone, {coalll} coal and {ironnn} iron!", mention_author=False)
  
  @commands.command(aliases=["inv"])
  async def inventory(self, ctx):
    table = await self.bot.db.fetchrow("SELECT * FROM minecord WHERE user_id = $1", ctx.author.id)
    if not table:
        await self.bot.db.execute("INSERT INTO minecord (user_id, wood, stone, obsidian, coal, iron, gold, redstone, lapis, diamond, emerald, quartz, coins, pickaxe, axe, pet) VALUES ($1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0, 0)", ctx.author.id)
        return await ctx.reply("I made a profile for you due to you not having one, if you did please contact my developer about it. Anyways welcome to Minecord!", mention_author=False)
    wood = table["wood"]
    stone = table["stone"]
    obsidian = table["obsidian"]
    coal = table["coal"]
    iron = table["iron"]
    gold = table["gold"]
    redstone = table["redstone"]
    lapis = table["lapis"]
    diamond = table["diamond"]
    emerald = table["emerald"]
    quartz = table["quartz"]
    coins = table["coins"]
    pickaxe = table["pickaxe"]
    axe = table["axe"]
    pet = table["pet"]
    await ctx.reply(embed=generate_embed("Here's your inventory:",f"{coins} coins\n{wood} wood\n{stone} stone\n{obsidian} obsidian\n{coal} coal\n{iron} iron\n{gold} gold\n{redstone} redstone\n{lapis} lapis\n{diamond} diamond\n{emerald} emerald\n{quartz} quartz.", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)

  @commands.command()
  async def reset(self, ctx):
   table = await self.bot.db.fetchrow("SELECT * FROM minecord WHERE user_id = $1", ctx.author.id)
   if not table:
       await self.bot.db.execute("INSERT INTO minecord (user_id, wood, stone, obsidian, coal, iron, gold, redstone, lapis, diamond, emerald, quartz, coins, pickaxe, axe, pet) VALUES ($1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0, 0)", ctx.author.id)
       return await ctx.send("You don't have a profile! ....I made you one")
   await ctx.reply("Ok,I deleted your profile.", mention_author=False)
   await self.bot.db.execute("DELETE FROM minecord WHERE user_id = $1", ctx.author.id)

def setup(bot):
  bot.add_cog(Minecord(bot))