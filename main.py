import discord, logging
import os
from discord.ext import commands
from utils.bot import AloneBot, BlacklistedError, MaintenanceError
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()


handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.add_handler(handler)

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

async def main():
    async with bot:
        if not hasattr(bot, "ipc"):
            format = self.bot.format_print("IPC")
            try:
                bot.ipc = ipc.Server(self.bot, host="127.0.0.1", port=2300, secret_key=os.getenv("ipc_key"))
                bot.ipc.start(self)
                print(f"{format} | Connected")
            except Exception as error:
                print(f"{format} | Errored!\n{error}")
        bot.start(os.getenv("token"))

if __name__ == "__main__":
    asyncio.run(main())