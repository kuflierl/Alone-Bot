from discord.ext import commands
import discord
from datetime import datetime


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        format = await self.bot.format_print("Alone Bot")
        print(f"{format} | Ready")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channel = self.bot.get_channel(906682479199531051)
        bots = sum(m.bot for m in guild.members)
        embed = discord.Embed(
            title="I joined a new guild!",
            description=f"Owner: {guild.owner}\nName: {guild.name}\nMembers: {guild.member_count}\nBots: {bots}\nNitro Tier: {guild.premium_tier}",
            color=0x5FAD68,
        )
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        channel = self.bot.get_channel(906682479199531051)
        await channel.send(f"I got kicked from {guild.name}.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content == f"<@{self.bot.user.id}>" and not message.author.bot:
            await message.reply("Hello, you just pinged me.")

    @commands.Cog.listener("on_message")
    async def is_afk_mention(self, message: discord.Message):
        for mention in message.mentions:
            for afk_id in self.bot.afk.copy():
                if mention.id == afk_id and not message.author.bot:
                    await message.reply(
                        f"I'm sorry, but <@{mention.id}> went afk for {self.bot.afk[mention.id]}."
                    )

    @commands.Cog.listener("on_message")
    async def is_afk(self, message: discord.Message):
        for member_id in self.bot.afk.copy():
            if member_id == message.author.id:
                self.bot.afk.pop(message.author.id)
                await message.reply(f"Welcome back <@{member_id}>!")

    @commands.Cog.listener()
    async def on_connect(self):
        format = await self.bot.format_print("Alone Bot")
        print(f"{format} | Connected")

    @commands.Cog.listener()
    async def on_disconnect(self):
        format = await self.bot.format_print("Alone Bot")
        print(f"{format} | Disconnected")

    @commands.Cog.listener()
    async def on_database_connect(self):
        format = await self.bot.format_print("AloneDB")
        print(f"{format} | Connected")

    @commands.Cog.listener()
    async def on_database_connect_error(self, error):
        format = await self.bot.format_print("AloneDB")
        print(f"{format} | Connection Errored!\n{error}")

    @commands.Cog.listener()
    async def on_message_edit(self, _, message):
        await self.bot.process_commands(message)
    
    @commands.Cog.listener()
    async def on_cog_load(self, cog):
        format = await self.bot.format_print(f"{cog}")
        print(f"{format} | Loaded")
    
    @commands.Cog.listener()
    async def on_cog_load_error(self, cog, error):
        format = await self.bot.format_print(f"{cog}")
        print(f"{format} | Loading Failed!\n{error}")
    

async def setup(bot):
    await bot.add_cog(Events(bot))
