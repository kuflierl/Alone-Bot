from discord.ext import commands
import discord
from datetime import datetime
import asyncio

class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
 
  @commands.Cog.listener()
  async def on_ready(self):
    print("Connected")

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    channel = self.bot.get_channel(906682479199531051)
    bots = sum(m.bot for m in guild.members)
    joinembed = discord.Embed(title="I joined a new guild!", description=f"Owner: {guild.owner}\nName: {guild.name}\nMembers: {guild.member_count}\nBots: {bots}\nNitro Tier: {guild.premium_tier}", color=discord.Color(int("5fad68", 16)))
    joinembed.set_footer(text="Alone Bot", icon_url=guild.icon_url)
    await channel.send(embed=joinembed)

  @commands.Cog.listener()
  async def on_guild_leave(self, guild):
    channel = self.bot.get_channel(906682479199531051)
    await channel.send(f"I got kicked from {guild.name}.")
  
  @commands.Cog.listener()
  async def on_command(self, ctx):
    channel = self.bot.get_channel(906682526456774697)
    await channel.send(f"{ctx.command} was used by {ctx.author} in {ctx.guild}.")

  @commands.Cog.listener()
  async def on_message(self, ctx):
    if ctx.content == f"<@{self.bot.user.id}>" and not ctx.author.bot:
      await ctx.channel.send("Hi, you just pinged me.")

  @commands.Cog.listener("on_message")
  async def is_afk_mention(self, ctx):
    for id in ctx.raw_mentions:
      for afkid in self.bot.afk.copy():
        if id == afkid and not ctx.author.bot:
          await ctx.channel.send(f"I'm sorry, but <@{id}> went afk for {self.bot.afk[id]}.")

  @commands.Cog.listener("on_message")
  async def is_afk(self, ctx):
    for id in self.bot.afk.copy():
      if id == ctx.author.id:
        self.bot.afk.pop(ctx.author.id)
        await ctx.channel.send(f"Welcome back <@{id}>!")

  @commands.Cog.listener()
  async def on_message_edit(self, before, message):
    await self.bot.process_commands(message)

def setup(bot):
  bot.add_cog(Events(bot))
