import discord, logging
import os
from discord.ext import commands
from utils.bot import AloneBot, BlacklistedError, MaintenanceError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)

bot = AloneBot(intents=discord.Intents.all())


@bot.after_invoke
async def aftercount(ctx: commands.Context):
    bot.command_counter += 1


@bot.check_once
async def blacklist(ctx: commands.Context):
    if ctx.author.id not in bot.user_blacklist:
        return True
    if ctx.author.id in bot.owner_ids:
        return True
    raise BlacklistedError


@bot.check_once
async def maintenance(ctx: commands.Context):
    if bot.maintenance is False or ctx.author.id in bot.owner_ids:
        return True
    raise MaintenanceError


if __name__ == "__main__":
    bot.run(os.getenv("token"), log_handler=handler)