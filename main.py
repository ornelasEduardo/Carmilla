import os
from dotenv import load_dotenv
from Carmilla import *

load_dotenv()

DISCORD_BOT_TOKEN: str|None = os.getenv("DISCORD_BOT_TOKEN")

if __name__ == "__main__":
  if (DISCORD_BOT_TOKEN == None):
      raise RuntimeError("Discord bot token not found")

  bot: Carmilla = Carmilla()
  bot.run(DISCORD_BOT_TOKEN)
