from discord import Client, Intents, Message
from discord.ext import commands

class Carmilla(commands.Bot):
    def __init__(self) -> None:
        intents: Intents = Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="", intents=intents)

    async def on_ready(self) -> None:
        synced = await self.tree.sync()
        print('Carmilla is online', self.user)

    async def setup_hook(self) -> None:
      await self.load_extension("cogs.feed")
      await self.load_extension("cogs.anime")