import discord
from discord.ext import commands
from ext.useful import generate_embed

class Events(commands.Cog):
  def __init__(self, bot):
   self.bot = bot
  
  @commands.Cog.listener()
  async def on_guild_join(self, guild):
   channel = self.bot.get_channel(906682479199531051)
   bots = sum(m.bot for m in guild.members)
   await channel.send(embed=generate_embed("I joined a new guild!", f"Name: {guild.name}\nMembers: {guild.member_count}\nBots: {bots}\nNitro Tier: {guild.premium_tier}", "Alone Bot", guild.icon, "5fad68"))

  @commands.Cog.listener()
  async def on_guild_leave(self, guild):
   channel = self.bot.get_channel(906682479199531051)
   await channel.send(f"I got kicked from {guild.name}....")
  
  @commands.Cog.listener()
  async def on_command(self, ctx):
   channel = self.bot.get_channel(906682526456774697)
   await channel.send(f"{ctx.command} was used by {ctx.author} in {ctx.guild}.")

  @commands.Cog.listener()
  async def on_message_edit(self, before, message):
   await self.bot.process_commands(message)

  @commands.Cog.listener()
  async def on_message(self, ctx):
   if ctx.content == "<@784545186612510811>" or ctx.content == "@Alone Bot#5952" and not ctx.author.bot:
    await ctx.reply(embed=generate_embed("Roger that", "Hey you actually have to use a command ok thanks", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)

def setup(bot):
  bot.add_cog(Events(bot))
