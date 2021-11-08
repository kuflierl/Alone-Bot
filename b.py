import discord
from discord.ext import commands, tasks
import asyncpg
from datetime import datetime
import os

oid = [821703584789430282, 412734157819609090, 755055117773963476, 771424427605753907, 606648465065246750, 631821494774923264]

class BlackListedError(commands.CheckFailure):
 pass
class MaintenanceError(commands.CheckFailure):
 pass

class AloneBot(commands.AutoShardedBot):
 def __init__(self, *args, **kwargs):
  super().__init__(*args, **kwargs)
  self.maintenance = False
  self.maintenance_reason = ""
  self.blacklist: dict[int, str] = {}
  self.db = self.loop.run_until_complete(asyncpg.create_pool(host="127.0.0.1", port="5432", user="hadock", password="discordbot", database="alonedb"))
  self.commandcounter = 0
  self.launch_time = datetime.utcnow()
  self.intents = discord.Intents.all()

bot = AloneBot(command_prefix=commands.when_mentioned_or("!a","•"), owner_ids=oid, strip_after_prefix=True, case_insensitive=True, activity=discord.Game("Thank you Danny, o7."),intents=AloneBot().intents)

class Help(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            helpembed = discord.Embed(title="Help", description=page, color=discord.Color(int("5960d8", 16)))
            helpembed.timestamp = discord.utils.utcnow()
            await destination.send(embed=helpembed)

bot.load_extension("jishaku")

os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_RETAIN"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

initial_extensions = ["ext.essential","ext.owner","ext.moderation","ext.error","ext.sql", "ext.events","ext.minecord","ext.random", "ext.help"]
for cogs in initial_extensions:
 bot.load_extension(cogs)

@bot.listen()
async def on_ready():
 print("I'm alive")

@bot.check
def blacklist(ctx: commands.Context):
 if bot.blacklist.get(ctx.author.id) == None:
  return True
 else:
  raise BlackListedError

@bot.check
def maintenance(ctx: commands.Context):
 if bot.maintenance == True:
  if ctx.author.id == id:
   return True
  else:
   raise MaintenanceError
 else:
  return True

async def run_once_when_ready():
 await bot.wait_until_ready()
 data = await bot.db.fetch("SELECT user_id, reason FROM blacklist")
 for users in data:
  bot.blacklist.update({users["user_id"]: users["reason"]})
  print("Done inserting blacklisted users into cache!")

@bot.after_invoke
async def aftercount(ctx):
 bot.commandcounter += 1
 
@bot.listen("on_message")
async def prefixcheck(message):
 if message.content == "!a" or message.content == "•" and not message.author.bot:
  embed = discord.Embed(title="Roger that", description="Hey you actually have to use a command ok thanks", color = discord.Color(int("2F3136", 16)))
  embed.set_footer(text="Alone Bot")
  await message.reply(embed=embed,mention_author=False)

bot.add_listener(prefixcheck)
bot.loop.create_task(run_once_when_ready())
bot.run("Nzg0NTQ1MTg2NjEyNTEwODEx.X8q2pA.qex5ifbezQvQnLcTzKeaLtzfE5w")