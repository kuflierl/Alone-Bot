import discord
from discord.ext import commands
from utils.help import Help


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._original_help_command = bot.help_command
        bot.help_command = HelpMe()
        bot.help_command_cog = self


class HelpMe(commands.HelpCommand):
    async def get_command_signature(self, command):
        return f"{command.qualified_name}"

  async def send_bot_help(self, mapping):
    embed = discord.Embed(title="Help", description="Use help (command) or help (category) for more information\n <> is a required argument | [] is an optional argument", color=discord.Color.blurple())
    embed.set_footer(text=f"Command ran by {self.context.author.display_name}", icon_url=self.context.author.avatar_url)
    embed.timestamp = datetime.utcnow()
    for cog, command in mapping.items():
      filtered = await self.filter_commands(command, sort=True)
      command_signatures = [await self.get_command_signature(c) for c in filtered]
      if command_signatures:
        cog_name = getattr(cog, "qualified_name", "No Category")
        embed.add_field(name=cog_name, value=" ".join(command_signatures), inline=False)
    await self.context.reply(embed=embed, mention_author=False)

  async def send_command_help(self, command):
    embed = discord.Embed(title=self.get_command_signature(command))
    embed.add_field(name="Description of the command", value=command.help)
    alias = command.aliases
    if alias:
      embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
    await self.context.reply(embed=embed, mention_author=False)

    async def send_command_help(self, command):
        command_name = await self.get_command_signature(command)
        embed = discord.Embed(title=command_name, color=discord.Color.blurple())
        embed.add_field(name="Description of the command", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        await self.context.reply(embed=embed)

    async def send_error_message(self, error: Exception):
        embed = discord.Embed(title="Error", description=error, color=0xF02E2E)
        await self.context.add_reaction(self.context.emoji.x)
        await self.context.reply(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group, color=discord.Color.blurple())
        embed.add_field(
            name="Subcommands",
            value=", ".join([command.name for command in group.walk_commands()]),
        )
        await self.context.reply(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=cog.qualified_name,
            description=cog.description,
            color=discord.Color.blurple(),
        )
        embed.add_field(
            name="Commands",
            value="\n".join([command.name for command in cog.get_commands()]),
        )
        await self.context.reply(embed=embed)


async def cog_unload(self):
    self.bot.help_command = Help()


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
