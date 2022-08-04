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

@app.route('/')
async def main():
    return await app.ipc.request("get_user_data", user_id=383946213629624322)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        app.ipc = loop.run_until_complete(IPC.start(loop=loop))
        app.run(loop=loop)
    finally:
        loop.run_until_complete(app.ipc.close())
        loop.close()