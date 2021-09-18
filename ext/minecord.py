from discord.ext import commands, flags, tasks
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
   await ctx.send("I nuked the database and deleted everyone's info in minecord.")
 
  @commands.command()
  async def mine(self, ctx):
   table = await self.bot.db.fetchrow("SELECT * FROM minecord WHERE user_id = $1", ctx.author.id)
   if not table:
       await self.bot.db.execute("INSERT INTO minecord (user_id, wood, stone, obsidian, coal, iron, gold, redstone, lapis, diamond, emerald, quartz, coins, pickaxe, axe, pet) VALUES ($1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0, 0)", ctx.author.id)
       return await ctx.send("I made a profile for you due to you not having one, if you did please contact my developer about it. Anyways welcome to Minecord!")
   pickaxe = table["pickaxe"]
   stone = table["stone"]
   stonee = random.randint(1 + pickaxe, 25 + pickaxe)
   stoneee = stonee + stone
   await self.bot.db.execute(f"UPDATE minecord SET stone = $1", stone + stonee)
   await ctx.send(f"You mined {stonee} stone! Now you have {stoneee} stone!")
  
  @commands.command(aliases=["inv"])
  async def inventory(self, ctx):
    table = await self.bot.db.fetchrow("SELECT * FROM minecord WHERE user_id = $1", ctx.author.id)
    if not table:
        await self.bot.db.execute("INSERT INTO minecord (user_id, wood, stone, obsidian, coal, iron, gold, redstone, lapis, diamond, emerald, quartz, coins, pickaxe, axe, pet) VALUES ($1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0, 0)", ctx.author.id)
        return await ctx.send("I made a profile for you due to you not having one, if you did please contact my developer about it. Anyways welcome to Minecord!")
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
    await ctx.reply(embed=generate_embed("Here's your inventory:",f"{coins} coins\n{wood} wood\n{stone} stone\n{obsidian} obsidian\n{coal} coal\n{iron} iron\n{gold} gold\n{redstone} redstone\n{lapis} lapis\n{diamond} diamond\n{emerald} emerald\n{quartz} quartz.", "Minecord | Alone Bot"), mention_author=False)

  @commands.command()
  async def reset(self, ctx):
   table = await self.bot.db.fetchrow("SELECT * FROM minecord WHERE user_id = $1", ctx.author.id)
   if not table:
       await self.bot.db.execute("INSERT INTO minecord (user_id, wood, stone, obsidian, coal, iron, gold, redstone, lapis, diamond, emerald, quartz, coins, pickaxe, axe, pet) VALUES ($1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 0, 0, 0)", ctx.author.id)
       return await ctx.send("You don't have a profile! ....I made you one")
   await ctx.send("Ok,I deleted your profile.")
   await self.bot.db.execute("DELETE FROM minecord WHERE user_id = $1", ctx.author.id)

def setup(bot):
  bot.add_cog(Minecord(bot))
