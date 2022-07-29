import discord
from discord.ext import commands

class DeleteView(discord.ui.View):
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
