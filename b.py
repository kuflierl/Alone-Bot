import discord
from discord.ext import commands
import asyncpg
from datetime import datetime
import random
from ext.useful import generate_embed
import os

oid = [821703584789430282, 412734157819609090, 755055117773963476, 771424427605753907, 606648465065246750, 631821494774923264]

class AloneBot(commands.AutoShardedBot):
 def __init__(self, *args, **kwargs):
  super().__init__(*args, **kwargs)
  self.maintenance = False

intents = discord.Intents.all()
bot = AloneBot(command_prefix=commands.when_mentioned_or("!a","•"), owner_ids=oid, strip_after_prefix=True, case_insensitive=True, activity=discord.Game("Thank you Danny, o7."),intents=intents)

class Help(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            helpembed = discord.Embed(title="Help", description=page, color=discord.Color(int("5960d8", 16)))
            helpembed.timestamp = discord.utils.utcnow()
            await destination.send(embed=helpembed)

bot.db = bot.loop.run_until_complete(asyncpg.create_pool(host="127.0.0.1", port="5432", user="hadock", password="discordbot", database="alonedb"))
bot.commandcounter = 0
bot.launch_time = datetime.utcnow()
bot.load_extension("jishaku")

os.environ["JISHAKU_HIDE"] = "true"
os.environ["JISHAKU_RETAIN"] = "true"
os.environ["JISHAKU_NO_UNDERSCORE"] = "true"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "true"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "true"

initial_extensions = ["ext.essential","ext.owner","ext.moderation","ext.error","ext.sql", "ext.events","ext.minecord","ext.random", "ext.help"]
for cogs in initial_extensions:
 bot.load_extension(cogs)

@bot.listen()
async def on_ready():
 print("I'm alive")

@bot.before_invoke
async def blacklist(ctx):
 table = await bot.db.fetchrow("SELECT * FROM blacklist WHERE user_id = $1", ctx.author.id)
 if table:
  reason = table["reason"]
  return await ctx.send(f"You've been blacklisted, the reason was {reason}, and you cannot appeal. Goodbye.")
  
 return

@bot.after_invoke
async def aftercount(ctx):
 bot.commandcounter += 1
 
@bot.listen("on_message")
async def prefixcheck(message):
 if message.content == "!a" or message.content == "•" and not message.author.bot:
  embed = discord.Embed(title="Roger that", description="Hey you actually have to use a command ok thanks", color = discord.Color(int("2F3136", 16)))
  embed.set_footer(text="Alone Bot")
  await message.reply(embed=embed,mention_author=False)

@bot.command(hidden=True)
@commands.is_owner()
async def cogsave(ctx):
 bot.load_extension(cogs)
 bot.load_extension("jishaku")
 await ctx.send("done")

@bot.command(hidden=True)
@commands.is_owner()
async def devkill(ctx):
 await ctx.send("cya")
 await ctx.bot.close()
 
bot.add_listener(prefixcheck)
bot.run("Nzg0NTQ1MTg2NjEyNTEwODEx.X8q2pA.qex5ifbezQvQnLcTzKeaLtzfE5w")