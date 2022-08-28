import discord, logging
import os, asyncio, asyncpg
from discord.ext import commands, ipc
from utils.bot import AloneBot, BlacklistedError, MaintenanceError
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()


handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

bot = AloneBot(intents=discord.Intents.all())


@bot.after_invoke
async def aftercount(ctx: commands.Context):
    bot.command_counter += 1


@bot.check_once
async def blacklist(ctx: commands.Context):
    if not bot.is_blacklisted(ctx.author.id):
        return True
    if ctx.author.id in bot.owner_ids:
        return True
    raise BlacklistedError


@bot.check_once
async def maintenance(ctx: commands.Context):
    if bot.maintenance is False or ctx.author.id in bot.owner_ids:
        return True
    raise MaintenanceError


async def main():
    async with bot:
        if not hasattr(bot, "ipc"):
            format = bot.format_print("IPC")
            try:
                bot.ipc = ipc.Server(
                    bot, host="127.0.0.1", secret_key=os.getenv("ipc_key")
                )
                bot.ipc.start()
                print(f"{format} | Connected")
                bot.dispatch("ipc_connect")
            except Exception as error:
                print(f"{format} | Errored!\n{error}")
        await bot.start(os.getenv("token"))

if __name__ == "__main__":
    asyncio.run(main())
