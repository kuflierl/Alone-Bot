import discord, psutil, asyncio, typing, random
from datetime import datetime
from discord.ext import commands
import time
import inspect

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        timestamp = int(self.bot.launch_time.timestamp())
        await ctx.reply(
            embed=discord.Embed(
                title="Current Uptime",
                description=f"Uptime: {days}d, {hours}h, {minutes}m, {seconds}s\n\nStartup Time: <t:{timestamp}:F>",
                color=0x88FF44,
            )
        )

    @commands.group(invoke_without_command=True)
    async def prefix(self, ctx: commands.Context):
        prefixes = ""
        for prefix in await self.bot.get_prefix(ctx.message):
            if prefix == "":
                prefixes += "No prefix enabled!"
            prefixes += f"{prefix}\n"
        await ctx.reply(
            embed=discord.Embed(title="Your prefixes", description=prefixes)
        )

    @prefix.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def guild(self, ctx: commands.Context, *, prefix: str):
        if prefix == "remove":
            self.bot.guild_prefix.pop(ctx.guild.id)
            await ctx.message.add_reaction(ctx.emoji.check)
            return await ctx.reply("Custom prefix for this guild has been cleared.")
        self.bot.guild_prefix[ctx.guild.id] = prefix
        await ctx.message.add_reaction(ctx.emoji.check)

    @prefix.command(aliases=["noprefix"])
    async def no_prefix(self, ctx: commands.Context):
        if ctx.author.id in self.bot.no_prefix:
            self.bot.no_prefix.remove(ctx.author.id)
            return await ctx.reply("No prefix has been disabled.")
        self.bot.no_prefix.append(ctx.author.id)
        await ctx.message.add_reaction(ctx.emoji.check)

    @prefix.command()
    async def add(self, ctx: commands.Context, *, prefix: str):
        if len(prefix) >= 15:
            return await ctx.reply(
                "Your prefix can't be longer than 15 characters, sorry!"
            )
        if self.bot.user_prefix.get(ctx.author.id):
            prefix_list = self.bot.user_prefix.get(ctx.author.id)
        else:
            prefix_list = []
            prefix_list.append(prefix)
            self.bot.user_prefix[ctx.author.id] = prefix_list
        await ctx.message.add_reaction(ctx.emoji.check) #todo

    @prefix.command()
    async def remove(self, ctx: commands.Context, prefix: str = None):
        if not prefix:
            try:
                self.bot.user_prefix.pop(ctx.author.id)
                await ctx.message.add_reaction(ctx.emoji.check)
            except KeyError:
                await ctx.reply("You don't have any custom prefixes!")
        else:
            if self.bot.user_prefix.get(ctx.author.id):
                try:
                    prefix_list = self.bot.user_prefix.get(ctx.author.id)
                    prefix_list.remove(prefix)
                    await ctx.message.add_reaction(ctx.emoji.check)
                except ValueError:
                    await ctx.message.add_reaction(ctx.emoji.x)
                    await ctx.reply("That prefix isn't in the list!")
            else:
                await ctx.reply("You don't have any custom prefixes!")

    @commands.command()
    async def source(self, ctx, command_name: str = None):
        if not command_name:
            return await ctx.reply("https://github.com/Alone-Bot/Alone-Bot")
        command = self.bot.get_command(command_name)
        if not command:
            return await ctx.reply("That's not a valid command!")
        source = inspect.getsource(command.callback)
        await ctx.reply(f"```py\n{source}```")

    @commands.group(invoke_without_command=True)
    async def todo(self, ctx: commands.Context):
        task_list = ""
        _todo = self.bot.todo.get(ctx.author.id)
        if not _todo:
            return await ctx.reply("You don't have a todo list!")
        for task_number in _todo:
            task = _todo.get(task_number)
            task_list += f"{task_number}: {task}\n"
        await ctx.reply(embed=discord.Embed(title="Todo", description=task_list))
    
    @todo.command()
    async def add(self, ctx: commands.Context, *, task: str):
        _todo = self.bot.todo.get(ctx.author.id)
        task_number = len(self.bot.todo.get(ctx.author.id)) + 1
        self.bot.todo[ctx.author.id][task_number] = task
        await ctx.message.add_reaction(ctx.emoji.x)
    
    @todo.command(aliases=["delete", "erase"])
    async def remove(self, ctx: commands.Context, task_number: int):
        _todo = self.bot.todo.get(ctx.author.id)
        try:
            _todo.pop(task_number)
            await ctx.message.add_reaction(ctx.emoji.x)
        except Exception as error:
            await ctx.reply("That isn't a valid task!")

    @commands.command()
    async def invite(self, ctx: commands.Context):
        normal_perms = discord.utils.oauth_url(
            self.bot.user.id,
            discord.Permissions(27494536309),
            scopes=("bot", "applications.commands"),
        )
        moderation_perms = discord.utils.oauth_url(
            self.bot.user.id,
            discord.Permissions(274945363015),
            scopes=("bot", "applications.commands"),
        )
        await ctx.reply(
            embed=discord.Embed(
                title="Invite me using these links!",
                description=f"[Normal Permissions]({normal_perms})\n\n[Moderation Permissions]({moderation_perms})\n(Enables Moderation commands)",
                color=0x28E8ED,
            )
        )

    @commands.command()
    async def quote(self, ctx: commands.Context, message: discord.Message = None):
        if not message:
            if not ctx.message.reference:
                return await ctx.reply("You need to give me a message to quote.")
            message = ctx.message.reference.resolved
        await ctx.reply(
            embed=discord.Embed(
                title=f"{message.author} sent:",
                description=f"> {message.content}\n- {message.author.mention}",
            )
        )

    @commands.command()
    async def ping(self, ctx: commands.Context):
        websocket = self.bot.latency * 1000
        startwrite = time.perf_counter()
        msg = await ctx.reply("Pong!")
        endwrite = time.perf_counter()
        duration = (endwrite - startwrite) * 100
        embed = discord.Embed(title="Pong!", color=discord.Colour.blue())
        embed.add_field(
            name="<a:typing:990387851940229120> | Typing",
            value=f"```py\n{duration:.2f}ms```",
        )
        embed.add_field(
            name="<a:loading2:990387928213631046> | Websocket",
            value=f"```py\n{websocket:.2f}ms```",
        )
        embed.set_footer(
            text=f"Command ran by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar,
        )
        embed.timestamp = discord.utils.utcnow()
        await msg.edit(embed=embed)

    @commands.command()
    async def battery(self, ctx: commands.Context):
        battery = psutil.sensors_battery()
        await ctx.reply(
            embed=discord.Embed(
                title="Battery",
                description=f"{battery.percent}%\n{'Plugged In' if battery.power_plugged else 'Not Plugged In'}",
                color=0x88FF44 if battery.power_plugged else 0xFF2E2E,
            )
        )

    @commands.command()
    async def counter(self, ctx: commands.Context):
        counter = self.bot.command_counter
        await ctx.reply(
            embed=discord.Embed(
                title="Command Counter",
                description=f"Commands used since last restart: {counter}",
                color=0x1F84C5,
            )
        )

    @commands.command(aliases=["av"])
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            member = ctx.author
        embed = discord.Embed(title=f"{member}'s avatar")
        embed.set_image(url=member.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["ui", "user_info", "user info"])
    async def userinfo(self, ctx: commands.Context, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        jointime = int(member.joined_at.timestamp())
        createdtime = int(member.created_at.timestamp())
        status = member.status
        embed = discord.Embed(
            title="Userinfo",
            description=f"Name: {member.name}\nNickname: {member.nick}\nJoined at: <t:{jointime}:F>\nreated at: <t:{createdtime}:F>\nAvatar: [Click Here]({member.avatar.url})\nStatus: {status}\n{'Banner:' if member.banner else ''}",
            color=0x53BDCE,
        )
        if member.banner:
            embed.set_image(url=member.banner)
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["server_info", "server info", "si", "guildinfo"])
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context, guild: discord.Guild = None):
        if not guild:
            guild = ctx.guild
        members = len([members for members in guild.members])
        bots = sum(m.bot for m in guild.members)
        embed = discord.Embed(
            title="Server Info",
            description=f"Owner: {guild.owner}\nID: {guild.id}\nName: {guild.name}\nMembers: {guild.member_count}\nBots: {bots}\nNitro Tier: Level {guild.premium_tier}",
            color=0x184EF3,
        )
        embed.set_thumbnail(url=guild.icon.url)
        await ctx.reply(embed=embed)

    @commands.command()
    async def support(self, ctx: commands.Context):
        await ctx.reply(
            embed=discord.Embed(
                title="Support",
                description="Join my [support server]({self.bot.support_server})!",
            )
        )

    @commands.command()
    async def suggest(self, ctx: commands.Context, *, suggestion: str = None):
        if not suggestion:
            return await ctx.reply("You need to give me a suggestion!")
        channel = self.bot.get_channel(868117548087005224)
        message = await channel.send(
            embed=discord.Embed(
                title=f"Suggestion by {ctx.author.name}",
                description=f"`{arg}`",
                color=0xFFFFFF,
            )
        )
        await message.add_reaction(ctx.emoji.x)
        await message.add_reaction(ctx.emoji.check)
        await ctx.message.add_reaction(ctx.emoji.check)
        await ctx.reply("Suggestion sent.")

    @commands.command(aliases=["cf", "flip_coin"])
    async def coinflip(self, ctx):
        message = await ctx.reply("Choosing a side..", mention_author=False)
        coin = ["heads", "tails"]
        choice = random.choice(coin)
        await message.edit(
            content=f"It's {choice}!", allowed_mentions=discord.AllowedMentions.none()
        )

    @commands.command()
    async def choose(
        self, ctx: commands.Context, choices: commands.Greedy[typing.Union[str, int]]
    ):
        choice = random.choice(choices)
        await ctx.reply(choice)

    @commands.command()
    async def cleanup(self, ctx: commands.Context, limit: int = 50):
        async for message in ctx.channel.history(limit=limit):
            if message.author == ctx.me:
                await message.delete()
        await ctx.message.add_reaction(ctx.emoji.check)

    @commands.command()
    async def afk(self, ctx: commands.Context, *, reason: str = "no reason"):
        if self.bot.afk.get(id):
            return await ctx.reply("You are already afk!")
        await ctx.message.add_reaction(ctx.emoji.check)
        await ctx.reply(f"**AFK**\nYou are now afk for {reason}.")
        await asyncio.sleep(0.1)
        self.bot.afk[ctx.author.id] = reason


async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))
