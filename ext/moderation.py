import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            return False
        return True

    @commands.group(invoke_without_command=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_guild_permissions(manage_channels=True)
    async def channel(self, ctx: commands.Context):
        await ctx.reply(
            f"Channel Name: {ctx.channel.name}\nID: {ctx.channel.id}\nCategory: {ctx.channel.category}"
        )

    @channel.command()
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_guild_permissions(manage_channels=True)
    async def slowmode(self, ctx: commands.Context, time: int = 0):
        await ctx.channel.edit(slowmode_delay=time)
        await ctx.message.add_reaction(ctx.emoji.check)

    @channel.command()
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_guild_permissions(manage_channels=True)
    async def name(self, ctx: commands.Context, *, name: str = None):
        if not name:
            return await ctx.reply("You need to supply a channel name!")
        await ctx.channel.edit(name=name)
        await ctx.message.add_reaction(ctx.emoji.check)

    @channel.command()
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_guild_permissions(manage_channels=True)
    async def topic(self, ctx: commands.Context, *, topic: str = None):
        await ctx.channel.edit(topic=topic)
        await ctx.message.add_reaction(ctx.emoji.check)

    @commands.command()
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "No reason provided.",
    ):
        if member == None:
            return await ctx.reply(
                embed=discord.Embed(
                    title="An error occured",
                    description="You need to provide a member to ban.",
                )
            )
        await member.ban(reason=reason)
        await ctx.reply(f"Banned {member} for {reason}.")

    @commands.command()
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.has_guild_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "No reason provided.",
    ):
        if member == None:
            return await ctx.reply(
                embed=discord.Embed(
                    title="An error occured",
                    description="You need to provide a member to ban.",
                )
            )
        await member.kick(reason=reason)
        await ctx.reply(f"Kicked {member} for {reason}.")

    @commands.command()
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, limit: int = 20):
        messages = await ctx.channel.purge(limit=limit)
        await ctx.send(f"{len(messages)} messages deleted.")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
