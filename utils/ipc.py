from quart import Quart
from discord.ext.ipc import Client
import os
from dotenv import load_dotenv

load_dotenv()


app = Quart(__name__)
IPC = Client(
    host="127.0.0.1", 
    port=2300, 
    secret_key=os.getenv("ipc_key"),
)