import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author):
            return True
        elif self.bot.is_helper(ctx.author.id):
            return True
        return False

    @commands.command()
    async def botinfo(self, ctx: commands.Context):
        await ctx.reply(
            embed=discord.Embed(
                title="Bot Info",
                description=f"`{len(self.bot.guilds)}` guilds\n`{len(self.bot.users)}` users",
            )
        )

    @commands.command()
    async def maintenance(self, ctx: commands.Context, *, reason="No reason provided."):
        if not self.bot.maintenance:
            await ctx.message.add_reaction(ctx.emoji.check)
            self.bot.maintenance = True
            self.bot.maintenance_reason = reason
            channel = self.bot.get_channel(907363405466333274)
            return await channel.send(
                "I am going on maintenance break, all commands will not work during the downtime."
            )
        await ctx.reply("Maintenance mode is now off.")
        self.bot.maintenance = False
        self.bot.maintenance_reason = ""
        channel = self.bot.get_channel(907363405466333274)
        await channel.send(
            "The maintenance break is over. All commands should be up now."
        )

    @commands.group(invoke_without_command=True)
    async def blacklist(self, ctx: commands.Context):
        profile = ""
        for user_id, reason in self.bot.user_blacklist.items():
            name = await self.bot.fetch_user(user_id)
            profile += f"\n{name}, {user_id}, {reason}"
        await ctx.reply(
            embed=discord.Embed(title="Blacklisted users", description=profile)
        )

    @blacklist.command()
    async def add(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "No reason provided",
    ):
        self.bot.user_blacklist[member.id] = reason
        await ctx.message.add_reaction(ctx.emoji.check)

    @blacklist.command()
    async def remove(self, ctx: commands.Context, *, member: discord.Member):
        try:
            self.bot.user_blacklist.pop(member.id)
        except KeyError:
            await ctx.message.add_reaction(bot.default_emoji("no"))
            return await ctx.reply("That user isn't blacklisted!")
        await ctx.message.add_reaction(ctx.emoji.check)

    @commands.command()
    async def disable(self, ctx: commands.Context, command_name: str):
        command = self.bot.get_command(command_name)
        if not command.enabled:
            await ctx.message.add_reaction(ctx.emoji.x)
            return await ctx.reply("This command is already disabled!")
        command.enabled = False
        await ctx.reply(f"Disabled {command_name}.")

    @commands.command()
    async def enable(self, ctx: commands.Context, command_name: str):
        command = self.bot.get_command(command_name)
        if command.enabled:
            await ctx.message.add_reaction(ctx.emoji.x)
            return await ctx.reply("This command is already enabled!")
        command.enabled = True
        await ctx.reply(f"Enabled {command_name}.")

    @commands.command()
    async def print(self, ctx: commands.Context, *, arg=""):
        print(arg)
        await ctx.message.add_reaction(ctx.emoji.check)

    @commands.command()
    async def say(self, ctx: commands.Context, *, arg=None):
        if not arg:
            await ctx.message.add_reaction(ctx.emoji.x)
            return await ctx.reply("You have to give me something to say.")
        await ctx.reply(arg)

    @commands.command(aliases=["d", "delete"])
    async def delmsg(self, ctx: commands.Context, message: discord.Message = None):
        if not message:
            if not ctx.message.reference:
                return await ctx.reply("You need to give me a message to delete.")
            message = ctx.message.reference.resolved
        await message.delete()
        await ctx.message.add_reaction(ctx.emoji.check)

    @commands.command()
    async def nick(self, ctx: commands.Context, *, name: str = None):
        await ctx.me.edit(nick=name)
        await ctx.message.add_reaction(ctx.emoji.check)

    @commands.command(aliases=["die", "shutdown", "fuckoff", "quit"])
    async def logout(self, ctx: commands.Context):
        await ctx.message.add_reaction(ctx.emoji.check)
        await ctx.bot.close()

    @commands.command(hidden=True)
    async def guild_leave(self, ctx: commands.Context, guild: discord.Guild = None):
        important_guilds = [774561547930304536, 867919029447295006, 336642139381301249]
        if guild:
            if guild.id in important_guilds:
                return await ctx.message.add_reaction(ctx.emoji.x)
        if ctx.guild.id in important_guilds:
            return await ctx.message.add_reaction(ctx.emoji.x)
        if not guild:
            await ctx.message.add_reaction(ctx.emoji.check)
            return await ctx.guild.leave()
        await ctx.message.add_reaction(ctx.emoji.check)
        await guild.leave()

    @commands.group(invoke_without_command=True)
    async def status(self, ctx: commands.Context):
        await ctx.reply(f"The current bot's status is {self.bot.activity}.")

    @status.command()
    async def set(self, ctx: commands.Context, type: str, *, activity: str):
        if type == "playing":
            type = discord.Game(activity)
        elif type == "watching":
            type = discord.Activity(type=discord.ActivityType.watching, name=activity)
        elif type == "streaming":
            type = discord.Streaming(name=activity, url="https://twitch.tv/AloneBot")
        elif type == "listening":
            type = discord.Activity(type=discord.ActivityType.listening, name=activity)
        await self.bot.change_presence(activity=type, status=discord.Status.online)
        await ctx.message.add_reaction(ctx.emoji.check)

    @commands.command()
    async def load(self, ctx: commands.Context, cog: str):
        try:
            await self.bot.load_extension(cog)
            message = "Loaded!"
        except Exception as error:
            message = f"Error! {error}"
        await ctx.reply(message)

    @commands.command()
    async def unload(self, ctx: commands.Context, cog: str):
        try:
            await self.bot.unload_extension(cog)
            message = "Unloaded!"
        except Exception as error:
            message = f"Error! {error}"
        await ctx.reply(message)

    @commands.command()
    async def reload(self, ctx: commands.Context):
        cog_status = ""
        for cog_name in self.bot.cogs.copy():
            if cog_name == "Jishaku":
              continue
            cog = self.bot.get_cog(cog_name)
            try:
                await self.bot.reload_extension(cog.__module__)
                cog_status += f"\U0001f504 {cog_name} Reloaded!\n\n"
            except commands.ExtensionNotLoaded:
                try:
                    await self.bot.load_extension(cog.__module__)
                    cog_status += f"\U00002705 {cog_name} Loaded!\n\n"
                except Exception as error:
                    cog_status += (
                        f"\U0000274c {cog_name} Errored!\n```py\n{error}```\n\n"
                    )
        await ctx.reply(embed=discord.Embed(title="Cogs", description=cog_status))
        await ctx.message.add_reaction(ctx.emoji.check)


async def setup(bot: commands.Bot):
    await bot.add_cog(Owner(bot))
