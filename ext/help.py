import discord
from discord.ext import commands
from datetime import datetime
from main import Help

class Help(commands.Cog):
 def __init__(self, bot):
  self._original_help_command = bot.help_command
  bot.help_command = HelpMe()
  bot.help_command_cog = self

class HelpMe(commands.HelpCommand):
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

def cog_unload(self):
    self.bot.help_command = Help()

def setup(bot):
    bot.add_cog(Help(bot))
