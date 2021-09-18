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
    await ctx.reply(embed=generate_embed("Uptime!",f"{days}d, {hours}h, {minutes}m, {seconds}s","Uptime | Alone Bot"), mention_author=False, delete_after=15)

  @commands.command()
  async def here(self, ctx):
   await ctx.reply(embed=generate_embed("Here","yup I'm here","Here | Alone Bot"), mention_author=False, delete_after=10)
   
  @commands.command()
  async def invite(self, ctx):
   await ctx.reply(embed=generate_embed("Invite","Invite me [here!](https://discord.com/api/oauth2/authorize?client_id=784545186612510811&permissions=8&scope=bot) (Link doesn't work now,bot is privated with no ETA","Thanks! | Alone Bot"), mention_author=False)
   
  @commands.command(aliases=["ui"])
  async def userinfo(self, ctx, member: discord.Member=None):
   if member is None:
            member = ctx.author
   await ctx.reply(embed=generate_embed("Userinfo",f"Full Name:{member}\nJoined at: {member.joined_at}","Userinfo | Alone Bot"), mention_author=False, delete_after=120)
   
  @commands.command()
  async def ping(self, ctx):
    connection = self.bot.db
    websock = self.bot.latency * 1000
    startype = time.perf_counter()
    message = await ctx.reply(embed=generate_embed("Ping!", "Wait a second...","Ping | Alone Bot"), mention_author=False)
    endtype = time.perf_counter()
    await connection.execute("SELECT 1")
    startdb = time.perf_counter()
    await connection.execute("SELECT 1")
    enddb = time.perf_counter()
    databas = (enddb - startdb) * 1000
    duration = (endtype - startype) * 1000
    await message.edit(embed=generate_embed("Pong!", f"<a:typing:597589448607399949> Typing\n`{duration:.2f}ms`\n<a:loading:747680523459231834> Websocket\n`{websock:.2f}ms`\n<:postgresql:875853638751359027> Database\n`{databas:.2f}ms`", "Ping | Alone Bot","101c6b"))
   
  @commands.command()
  async def battery(self, ctx):
   battery = psutil.sensors_battery()  
   await ctx.send(embed=generate_embed("I am alive", f"{battery.percent}% | {'Plugged In' if battery.power_plugged else 'Not Plugged In'}", "Battery | Alone Bot","7f797b"))

  @commands.command()
  async def counter(self, ctx):
   counter = self.bot.commandcounter
   msg = await ctx.reply(embed=generate_embed(":0 wow",f"Commands used since last restart: {counter}","Alone Bot"))

  @commands.command(hidden=True)
  @commands.is_owner()
  async def vc(self, ctx):
   await ctx.send("<@&858793244861923348> fuckheads join vc")
   
  @commands.command(aliases=["about","developer"])
  async def credits(self, ctx):
   version = discord.__version__
   await ctx.reply(embed=generate_embed("About me",f"Hi, my name is Alone Bot. \n My developer is <@412734157819609090> and my helpers are <@606648465065246750> and <@771424427605753907>. \nMy discord.py version is {version}. <:dpy:596577034537402378>\nMy Python version is 3.8.0 <:python:596577462335307777>","Made with Python | Alone Bot"), mention_author=False, delete_after=150)

def setup(bot):
  bot.add_cog(Essential(bot))