import discord
from discord import PartialEmoji as get_emoji
from discord.ext import commands


class View(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(
        emoji="\U0001f5d1", style=discord.ButtonStyle.danger, label="Delete"
    )
    async def delete(self, interaction, button):
        if interaction.user.id == self.ctx.author.id:
            return await interaction.message.delete()
        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't delete it!",
            ephemeral=True,
        )


class AloneContext(commands.Context):
    async def send(self, *args, button: bool = True, **kwargs):
        embed = kwargs.get("embed")
        if embed:
            if not embed.color:
                embed.color = discord.Color.random()
            if not embed.footer:
                embed.set_footer(
                    text=f"Command ran by {self.author.display_name}",
                    icon_url=self.author.display_avatar,
                )
            if not embed.timestamp:
                embed.timestamp = discord.utils.utcnow()

        if button:
          kwargs["view"] = View(self)

        return await super().send(*args, **kwargs)

    async def reply(self, *args, **kwargs):
        if not kwargs.get("mention_author"):
            kwargs["mention_author"] = False

        return await super().reply(*args, **kwargs)
    
    class Emoji:
      x = get_emoji(name="redTick", id="895688440568508518")
      check = get_emoji(name="greenTick", id="895688440690147370")
      slash = get_emoji(name="greyTick", id="895688440690114560")
    
    emoji = Emoji()