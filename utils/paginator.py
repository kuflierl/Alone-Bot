import discord
from discord.ext import commands, menus

class Paginator(ui.View, menus.MenuPages):
    def __init__(self, source):
        super().__init__(timeout=240)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None

    async def start(self, ctx, *, channel=None, wait=False):
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        value = await super()._get_kwargs_from_page(page)
        if "view" not in value:
            value.update({"view": self})
        return value

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @ui.button(emoji="\U000023ee", style=discord.ButtonStyle.blurple)
    async def first_page(self, button, interaction):
        await self.show_page(0)

    @ui.button(emoji="\U00002b05", style=discord.ButtonStyle.blurple)
    async def before_page(self, button, interaction):
        await self.show_checked_page(self.current_page - 1)

    @ui.button(emoji="\U000023f9", style=discord.ButtonStyle.blurple)
    async def stop_page(self, button, interaction):
        self.stop()

    @ui.button(emoji="\U000027a1", style=discord.ButtonStyle.blurple)
    async def next_page(self, button, interaction):
        await self.show_checked_page(self.current_page + 1)

    @ui.button(emoji="\U0000fe0f", style=discord.ButtonStyle.blurple)
    async def last_page(self, button, interaction):
        await self.show_page(self._source.get_max_pages() - 1)