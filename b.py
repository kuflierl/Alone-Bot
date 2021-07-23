import discord
from discord.ext import flags, commands, tasks
import os
from datetime import datetime
import time
import sys, traceback
from difflib import get_close_matches
import requests
import asyncio
import asyncpg
import typing
import json
import copy

save = "https://pastebin.com/VHzdr6Pf"
oid = [821703584789430282, 412734157819609090, 755055117773963476, 771424427605753907, 606648465065246750]

intents = discord.Intents.all()
intents.members = True
intents.presences = True
bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("•","!a"),owner_ids=oid, shard_count=10, strip_after_prefix=True, case_insensitive=True, activity=discord.Game("with my Owner's life | !ahelp"),intents=intents)

class Help(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            await destination.send(embed=generate_embed("You asked for help?", f"{page}".strip("help"), "Help | Alone Bot"))

ratelimitime = datetime.utcnow()
bot.commandcounter = 0
bot.help_command = Help()
bot.launch_time = datetime.utcnow()
bot.load_extension("jishaku")
initial_extensions = ["cogs.essential","cogs.owner"]
for cogs in initial_extensions:
 bot.load_extension(cogs)
 
def generate_embed(header, content, footer):
  embed = discord.Embed()
  embed.title = header
  embed.description = content
  embed.color = discord.Color(int("2F3136", 16))
  embed.set_footer(text=footer)
  return embed

def yes(reaction, user):
         return user == ctx.message.author and str(reaction.emoji) == "\U00002705"
def no(reaction, user):
         return user == ctx.message.author and str(reaction.emoji) == "\U0000274c"

@bot.event
async def on_message_edit(before, message):
 await bot.process_commands(message)

@tasks.loop(seconds=5)
async def ratelimitcheck():
 if bot.is_ws_ratelimited():
  print(f"At {ratelimitime}, I got ratelimited")
 else:
  return

@bot.event
async def on_ready():
 print("I'm alive")

@bot.after_invoke
async def aftercount(ctx):
 bot.commandcounter += 1

@bot.event
async def on_connect():
 print("I connected")
 
@bot.event
async def on_disconnnect():
 print("I disconnected...")

@bot.event
async def on_message(message):
 if message.content == "<@784545186612510811>" or message.content == "@Alone Bot#5952" or message.content == "!a" or message.content == "•" and not message.author.bot:
  await message.reply(embed=generate_embed("Roger that", "Hey you actually have to use a command ok thanks", "Alone Bot"), mention_author=False)
 await bot.process_commands(message)

ratelimitcheck.start()
bot.run("Nzg0NTQ1MTg2NjEyNTEwODEx.X8q2pA.Zbw5VIA3v-02yKF4hl68sFaw27Y")