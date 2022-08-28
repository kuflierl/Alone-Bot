import discord
from discord.ext import commands
from utils.bot import BlacklistedError, MaintenanceError
from utils.logger import logger


class Error(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, BlacklistedError):
            await ctx.message.add_reaction(ctx.emoji.x)
            reason = self.bot.user_blacklist.get(ctx.author.id)
            await ctx.reply(
                f"You have been blacklisted for {reason}. you may not appeal this blacklist. There still exists a chance I'll unban you, but it's not likely."
            )
        elif isinstance(error, MaintenanceError):
            await ctx.message.add_reaction(ctx.emoji.x)
            await ctx.reply(
                f"The bot is currently in maintenance mode for {self.bot.maintenance_reason}, please wait. If you have any issues, you can join my support server for help."
            )
        elif isinstance(error, commands.CheckFailure):
            await ctx.message.add_reaction(ctx.emoji.x)
            await ctx.reply(
                embed=discord.Embed(
                    title="Error",
                    description="You do not have permission to run this command!",
                    color=0xF02E2E,
                )
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction(ctx.emoji.x)
            await ctx.reply(
                f"You are on cooldown. Try again in {error.retry_after:.2f}s"
            )
        else:
            await ctx.message.add_reaction(ctx.emoji.x)
            logger.error("An error occurred", exc_info=error)
            embed = discord.Embed(
                title=f"Ignoring exception in {ctx.command}:",
                description=f"```py\n{error}```",
                color=0xF02E2E,
            )
            channel = self.bot.get_channel(906683175571435550)
            await channel.send(
                f"This error came from {ctx.author} using {ctx.command} in {ctx.guild}.",
                embed=embed,
            )
            await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Error(bot))
