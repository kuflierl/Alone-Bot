import discord
from discord.ext import commands

class DeleteView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(
        emoji="\U0001f5d1", style=discord.ButtonStyle.danger, label="Delete", custom_id="delete"
    )
    async def delete(self, interaction, button):
        if interaction.user.id == self.ctx.author.id:
            return await interaction.message.delete()
        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't delete it!",
            ephemeral=True,
        )

class JoinSupportView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.remove_item(self.delete_button)
        self.add_item(discord.ui.Button(label="Support", url=self.ctx.bot.support_server))
        self.add_item(self.delete_button)
    
    @discord.ui.button(
        emoji="\U0001f5d1", custom_id="delete_short", style=discord.ButtonStyle.danger
    )
    async def delete_button(self, interaction, button):
        if interaction.user.id == self.ctx.author.id:
            return await interaction.message.delete()
        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't delete it!",
            ephemeral=True,
        )