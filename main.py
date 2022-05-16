import asyncpg, discord, os
from dotenv import load_dotenv
from discord.ext import commands, tasks
from datetime import datetime
from typing import Optional

load_dotenv()

class Help(commands.HelpCommand):
  def get_command_signature(self, command):
    return "%s %s" % (command.qualified_name, command.signature)

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

    async def send_command_help(self, command):
      embed = discord.Embed(title=self.get_command_signature(command))
      embed.add_field(name="Description of the command", value=command.help)
      alias = command.aliases
      if alias:
        embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

    async def send_error_message(self, error):
      embed = discord.Embed(title="Error", description=error)
      await self.context.send(embed=embed)

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

  @bot.check
  def maintenance(ctx):
    if bot.maintenance is False:
      return True
    else:
      if ctx.author.id in bot.ownerids:
        return True
      else:
        raise MaintenanceError

  bot.run(bot.token)

if __name__ == "__main__":
  main()
