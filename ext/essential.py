import discord
from discord.ext import commands
from datetime import datetime
import time
import sys
import psutil
from ext.useful import generate_embed

class Essential(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def uptime(self, ctx):
    delta_uptime = datetime.utcnow() - self.bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.reply(embed=generate_embed("Uptime!",f"{days}d, {hours}h, {minutes}m, {seconds}s", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)

  @commands.command()
  async def here(self, ctx):
   await ctx.reply(embed=generate_embed("Here","yup I'm here", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False, delete_after=10)
   
  @commands.command()
  async def invite(self, ctx):
   await ctx.reply(embed=generate_embed("Invite","Invite me [here!](https://discord.com/api/oauth2/authorize?client_id=784545186612510811&permissions=8&scope=bot)", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
   
  @commands.command(aliases=["ui"])
  async def userinfo(self, ctx, *, member: discord.Member=None):
   if member is None:
    member = ctx.author
   user = await self.bot.fetch_user(member.id)
   memberjoinedyear = member.joined_at.strftime("%x")
   memberjoinedtime = member.joined_at.strftime("%X")
   membercreatedyear = member.created_at.strftime("%x")
   membercreatedtime = member.created_at.strftime("%X") # thanks to fahad for help with strftime
   status = member.status
   if user.banner:
    userinfoembed = discord.Embed(description=f"Nickname: {member.nick}\nFull Name:{member}\nJoined at: {memberjoinedtime} {memberjoinedyear}\nCreated at: {membercreatedtime} {membercreatedyear}\nAvatar: [click here]({user.avatar.url})\nStatus:\n{status}\nBanner:", timestamp=discord.utils.utcnow(), title="Userinfo", color=discord.Color(int("53bdce", 16)))
    userinfoembed.set_image(url=user.banner)
   else:
    userinfoembed = discord.Embed(description=f"Nickname: {member.nick}\nFull Name:{member}\nJoined at: {memberjoinedtime} {memberjoinedyear}\nCreated at: {membercreatedtime} {membercreatedyear}\nAvatar: [click here]({user.avatar.url})\nStatus:\n{status}\nBanner: None", title="Userinfo", timestamp=discord.utils.utcnow(), color=discord.Color(int("53bdce", 16)))
   memberpfp = f"{member.avatar.url}"
   userinfoembed.set_footer(text=f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
   userinfoembed.set_thumbnail(url=memberpfp)
   await ctx.reply(embed=userinfoembed, mention_author=False, delete_after=120)
   
  @commands.command()
  async def quote(self, ctx, message):
   msg = await ctx.channel.fetch_message(message)
   await ctx.reply(embed=generate_embed(f"{msg.author} sent this:", f"> {msg.content}\n{msg.author.mention}", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
  
  @commands.command()
  async def ping(self, ctx):
    connection = self.bot.db
    websock = self.bot.latency * 1000
    startype = time.perf_counter()
    message = await ctx.reply(embed=generate_embed("Ping!", "Wait a second...", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
    endtype = time.perf_counter()
    await connection.execute("SELECT 1")
    startdb = time.perf_counter()
    await connection.execute("SELECT 1")
    enddb = time.perf_counter()
    databas = (enddb - startdb) * 1000
    duration = (endtype - startype) * 1000
    await message.edit(embed=generate_embed("Pong!", f"<a:typing:597589448607399949> Typing\n`{duration:.2f}ms`\n<a:loading:747680523459231834> Websocket\n`{websock:.2f}ms`\n<:postgresql:875853638751359027> Database\n`{databas:.2f}ms`", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url, "101c6b"))
   
  @commands.command()
  async def battery(self, ctx):
   battery = psutil.sensors_battery()  
   await ctx.reply(embed=generate_embed("I am alive", f"{battery.percent}% | {'Plugged In' if battery.power_plugged else 'Not Plugged In'}", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url, "7f797b"), mention_author=False)

  @commands.command()
  async def counter(self, ctx):
   counter = self.bot.commandcounter
   msg = await ctx.reply(embed=generate_embed(":0 wow",f"Commands used since last restart: {counter}", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False)
   
  @commands.command(aliases=["about","developer"])
  async def credits(self, ctx):
   version = discord.__version__
   await ctx.reply(embed=generate_embed("About me",f"Hi, my name is Alone Bot. \n My developer is <@412734157819609090> and my helpers are <@606648465065246750> and <@771424427605753907>. \nMy discord.py version is {version}. <:dpy:596577034537402378>\nMy Python version is 3.8.0 <:python:596577462335307777>", f"Command ran by {ctx.author.name}#{ctx.author.discriminator}", ctx.author.avatar.url), mention_author=False, delete_after=150)

def setup(bot):
  bot.add_cog(Essential(bot))
