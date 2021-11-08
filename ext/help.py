from discord.ext import commands
import discord

class Help(commands.Cog):
 def __init__(self, bot):
  self._original_help_command = bot.help_command
  bot.help_command = HelpMe()
  bot.help_command.cog = self

class HelpMe(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_command_signature(c) for c in filtered]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)


def cog_unload(self):
 self.bot.help_command = None

def setup(bot):
  bot.add_cog(Help(bot))