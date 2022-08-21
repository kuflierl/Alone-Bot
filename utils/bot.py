import discord, os, asyncpg, aiohttp
from discord.ext import commands
from datetime import datetime
from .context import AloneContext


class AloneBot(commands.AutoShardedBot):
    async def get_prefix(self, message):
        prefix = ["Alone", "alone"]
        custom_user_prefix = self.user_prefix.get(message.author.id)
        if message.guild:
            custom_guild_prefix = self.guild_prefix.get(message.guild.id)
            if custom_guild_prefix:
                prefix.append(custom_guild_prefix)
        if custom_user_prefix:
            prefix.extend(custom_user_prefix)
        if (
            not message.guild
            or message.author.id in self.no_prefix
            or await self.is_owner(message.author)
        ):
            prefix.append("")
        return commands.when_mentioned_or(*prefix)(self, message)

    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix,
            strip_after_prefix=True,
            case_insensitive=True,
            *args,
            **kwargs,
        )
        self.name = os.environ["name"]
        self.user_blacklist: dict[int, str] = {}
        self.guild_blacklist: list = []
        self.afk: dict[int, str] = {}
        self.todo: dict[int, dict[int, str]] = {}
        self.user_prefix: dict[int, list] = {34937972103561218: [":pensivewiggle"]}
        self.guild_prefix: dict[int, str] = {}
        self.no_prefix: list = []
        self.support_server: str = "https://discord.gg/cCvcQKxg6T"
        self.maintenance: bool = False
        self.maintenance_reason: str = ""
        # self.cooldown = commands.CooldownMapping.from_cooldown(
        #    1, 5, commands.BucketType.user
        # )
        self.owner_ids: list = [412734157819609090]
        self.helper_ids: list = []
        self.command_counter: int = 0
        self.launch_time: datetime.datetime = datetime.utcnow()
        self.session = aiohttp.ClientSession()

    async def get_context(self, message, *, cls=AloneContext):
        return await super().get_context(message, cls=cls)

    async def setup_hook(self):
        initial_extensions = [
            "ext.events",
            "ext.error",
            "ext.fun",
            "ext.help",
            "ext.ipc",
            "ext.moderation",
            "ext.owner",
            "ext.utility",
            "ext.permissions",
            "jishaku",
        ]
        for cog in initial_extensions:
            try:
                extension = await self.load_extension(cog)
                self.dispatch("cog_load", cog)
            except Exception as error:
                self.dispatch("cog_load_error", cog, error)

        # try:
        #    user_prefix_db = self.db.fetch("SELECT * FROM users WHERE prefix IS NOT NULL")
        #    for user in user_prefix_db:
        #        user_id = user[user_id]
        #        prefix = user[prefix]
        #        self.user_prefix[user_id] = prefix
        #    self.dispatch("user_prefix_ready")
        # except Exception as error:
        #    self.dispatch("prefix_error", error)

        # try:
        #    for guild in guild_prefix_db:
        #        guild_id = guild["guild_id"]
        #        prefix = guild[prefix]
        #        self.guild_prefix[guild_id] = prefix
        #    self.dispatch("guild_prefix_ready")
        # except Exception as error:
        #    self.dispatch("prefix_error", error)

    def is_blacklisted(self, member):
        return member in self.user_blacklist

    def add_owner(self, member):
        self.owner_ids.append(member)

    def remove_owner(self, member):
        if member == 412734157819609090:
            return False
        self.owner_ids.remove(member)

    def format_print(self, text):
        format = str(datetime.now().strftime("%x | %X") + f" | {text}")
        return format

class BlacklistedError(commands.CheckFailure):
    pass
class MaintenanceError(commands.CheckFailure):
    pass
