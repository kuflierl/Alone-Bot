import discord, logging
import os, asyncio, asyncpg
from discord.ext import commands, ipc
from utils.bot import AloneBot, BlacklistedError, MaintenanceError
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()


  async def send_bot_help(self, mapping):
    embed = discord.Embed(title="Help", description="Use help (command) or help (category) for more information\n <> is a required argument | [] is an optional argument", color=discord.Color.blurple())
    embed.set_footer(text=f"Command ran by {self.context.author.display_name}", icon_url=self.context.author.avatar_url)
    embed.timestamp = datetime.utcnow()
    for cog, command in mapping.items():
      filtered = await self.filter_commands(command, sort=True)
      command_signatures = [self.get_command_signature(c) for c in filtered]
      if command_signatures:
        cog_name = getattr(cog, "qualified_name", "No Category")
        embed.add_field(name=cog_name, value=" ".join(command_signatures), inline=False)
    await self.context.send(embed=embed)

bot = AloneBot(intents=discord.Intents.all())


    async def send_group_help(self, group):
      await self.context.send("This is help group")

    async def send_cog_help(self, cog):
      embed = discord.Embed(title=cog.qualified_name, description=cog.description)
      embed.add_field(name="Commands", value="\n".join(cog.get_commands()))

#class DeleteButton(discord.Button):
#  def __init__(self):
#    self.style = discord.ButtonStyle.red()
#    self.label = "Delete"

class AloneBot(commands.AutoShardedBot):
  def __init__(self, *args, **kwargs):
    super().__init__(command_prefix=(os.getenv("prefix")), *args, **kwargs)
    self.token = os.getenv("token")
    self.userblacklist: dict[int, str] = {}
    self.afk: dict[int, str] = {}
    self.maintenance = False
    self.maintenance_reason = ""
    self.db = 0
    self.activity = discord.Game(os.getenv("discord_activity"))
    self.owner_ids = [int(i) for i in os.getenv("owners").split(",")]
    self.name = os.getenv("bot_name")
    self.command_counter = 0
    self.launch_time = datetime.utcnow()
    self.support_server = os.getenv("support_server")
    self.strip_after_prefix = True
    self.case_insensitive = True

  def generate_embed(self, ctx: commands.Context, title: str, content: str, color: Optional[int] = None):
    embed = discord.Embed()
    embed.title = title
    embed.description = content
    if color is None:
      embed.color = discord.Color.random()
    else:
      embed.color = int(color, 16)
    embed.set_footer(text=f"Command ran by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    embed.timestamp = datetime.utcnow()
    return embed

  def botmsgs(self, msg):
    return msg.author == self.user

class BlacklistedError(commands.CheckFailure):
  pass

class MaintenanceError(commands.CheckFailure):
  pass

def main():
  os.environ["JISHAKU_HIDE"] = "true"
  os.environ["JISHAKU_RETAIN"] = "true"
  os.environ["JISHAKU_NO_UNDERSCORE"] = "true"
  os.environ["JISHAKU_FORCE_PAGINATOR"] = "true"
  os.environ["JISHAKU_NO_DM_TRACEBACK"] = "true"

  bot = AloneBot(intents=discord.Intents.all())

  bot.load_extension("jishaku")
  initial_extensions = [
        "ext.error",
        "ext.events",
        "ext.fun",
        "ext.help",
        "ext.moderation",
        "ext.owner",
        "ext.utility",
  ]
  for cog in initial_extensions:
    bot.load_extension(cog)

  @bot.after_invoke
  async def aftercount(ctx):
    bot.command_counter += 1

  @bot.check
  def blacklist(ctx):
    if ctx.author.id not in bot.userblacklist:
      return True
    else:
      raise BlacklistedError

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
    async with asyncpg.create_pool(os.environ["database"]) as bot.db:
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
