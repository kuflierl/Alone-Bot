import discord
from discord.ext import commands


class Permissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)

    @commands.group(invoke_without_command=True)
    async def helper(self, ctx: commands.Context):
        helper_list = ""
        for helper_id in self.bot.helper_ids:
            member = self.bot.get_user(helper_id)
            helper_list += f"{helper_id}, {member.name}, {member.mention}\n"
        await ctx.reply(
            embed=discord.Embed(title="Helper List", description=helper_list)
        )

    @helper.command()
    async def add(self, ctx, *, member: discord.Member):
        self.bot.helper_ids.append(member.id)
        await ctx.message.add_reaction(ctx.emoji.check)

    @helper.command()
    async def remove(self, ctx, *, member: discord.Member):
        try:
            self.bot.helper_ids.remove(member.id)
        except KeyError as error:
            return await ctx.reply("That person isn't a helper!")
        await ctx.message.add_reaction(ctx.emoji.check)


async def setup(bot):
    await bot.add_cog(Permissions(bot))
