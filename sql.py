from discord.ext import commands, tasks
import discord
import asyncpg
import asyncio
import datetime
from ext.useful import generate_embed

class PostgreSQL(commands.Cog):
  def __init__(self, bot):
   self.bot = bot
  
  @commands.command()
  @commands.is_owner()
  async def execute(self, ctx, *, arg):
   connection = self.bot.db
   response = await connection.execute(arg)
   await ctx.reply(embed=generate_embed("Done",f"If you didn't fuck something up,you did it.\nOh also:\n```fix\n{response}```\nThat's all I got for you", "Execute | Alone Bot", "5fc7a5"), mention_author=False)
   
  @commands.command()
  @commands.is_owner()
  async def sqlclose(self, ctx):
   self.bot.connection = self.bot.db
   await ctx.reply(embed=generate_embed("Closed","It's gone","SQL Close | Alone Bot"), mention_author=False)
   await connection.close()
  
  @commands.command()
  @commands.is_owner()
  async def sqlconnect(self, ctx):
   await ctx.reply(embed=generate_embed("Hacking into the mainframe","Connecting to the DB.","SQL Connect | Alone Bot"), mention_author=False)
  
def setup(bot):
  bot.add_cog(PostgreSQL(bot))