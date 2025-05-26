import os
from dotenv import load_dotenv
import discord

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

class Carmilla(discord.Client):
    async def on_ready(self):
        print('Carmilla is online', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents.default()
intents.message_content = True
client = Carmilla(intents=intents)
client.run(DISCORD_BOT_TOKEN)