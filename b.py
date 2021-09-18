import discord
from discord.ext import commands, tasks
import asyncpg
from datetime import datetime
import random
from ext.useful import generate_embed, Help

oid = [821703584789430282, 412734157819609090, 755055117773963476, 771424427605753907, 606648465065246750, 631821494774923264]

intents = discord.Intents.all()
intents.members = True
intents.presences = True
bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("!a","•"), owner_ids=oid, strip_after_prefix=True, case_insensitive=True, activity=discord.Game("Thank you Danny, o7."),intents=intents)

ratelimitime = datetime.utcnow()
bot.db = bot.loop.run_until_complete(asyncpg.create_pool(host="127.0.0.1", port="5432", user="hadock", password="discordbot", database="alonedb"))
bot.commandcounter = 0
bot.help_command = Help()
bot.launch_time = datetime.utcnow()
bot.load_extension("jishaku")
initial_extensions = ["ext.essential","ext.owner","ext.moderation","ext.error","ext.sql"]
for cogs in initial_extensions:
 bot.load_extension(cogs)

@bot.listen()
async def on_message_edit(before, message):
 await bot.process_commands(message)

@tasks.loop(seconds=5)
async def ratelimitcheck():
 if bot.is_ws_ratelimited():
  print(f"At {ratelimitime}, I got ratelimited")
 else:
  return

@bot.listen()
async def on_ready():
 print("I'm alive")

@bot.after_invoke
async def aftercount(ctx):
 bot.commandcounter += 1

@bot.listen("on_message")
async def prefixcheck(message):
 if message.content == "!a" or message.content == "•" and not message.author.bot:
  await message.reply(embed=generate_embed("Roger that", "Hey you actually have to use a command ok thanks", "Alone Bot"), mention_author=False)
 
@bot.listen()
async def on_message(message):
 if message.content == "<@784545186612510811>" or message.content == "@Alone Bot#5952" and not message.author.bot:
  await message.reply(embed=generate_embed("Roger that", "Hey you actually have to use a command ok thanks", "Alone Bot"), mention_author=False)
  
@bot.command(hidden=True)
@commands.is_owner()
async def devkill(ctx):
 await ctx.send("cya")
 await bot.close()
 
@bot.command(hidden=True)
@commands.is_owner()
async def cogsave(ctx):
 await bot.load_extension(cogs)
 await ctx.send("done")

bot.add_listener(prefixcheck)
ratelimitcheck.start()
bot.run("Nzg0NTQ1MTg2NjEyNTEwODEx.X8q2pA.Zbw5VIA3v-02yKF4hl68sFaw27Y")