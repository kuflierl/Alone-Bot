from quart import Quart
from discord.ext.ipc import Client

app = Quart(__name__)
IPC = Client(
    host="127.0.0.1", 
    port=2300, 
    secret_key="discordbot"
)