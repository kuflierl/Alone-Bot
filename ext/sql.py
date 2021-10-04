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
   await ctx.reply(embed=generate_embed("Done",f"If you didn't fuck something up,you did it.\nOh also:\n```fix\n{response}```\nThat's all I got for you", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url, "5fc7a5"), mention_author=False)
  
  @commands.command()
  @commands.is_owner()
  async def sqlclose(self, ctx):
   self.bot.connection = self.bot.db
   await ctx.reply(embed=generate_embed("Closed","It's gone", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
   await connection.close()
  
def setup(bot):
  bot.add_cog(PostgreSQL(bot))