import discord
from discord.ext import commands
import requests
from ext.useful import generate_embed

API = 38c24dfff7f974d4b65b1a13390e97617479b9a69844b5df5368a61a9e683ef5
Board = 60ae7dd9115e2035804ecd35
Key = 5a9571e9bad1ec23d8b226037211f618
Cards = GET /1/lists/60ae7dd9115e2035804ecd35/cards
getboard1 = requests.get("https://api.trello.com/1/boards/SZfyiwcJ?key=5a9571e9bad1ec23d8b226037211f618&token=38c24dfff7f974d4b65b1a13390e97617479b9a69844b5df5368a61a9e683ef5")
Webhook make = requests.post(/1/webhooks)

class Dashboard(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

def setup(bot):
  bot.add_cog(Dashboard(bot))