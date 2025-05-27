from discord import app_commands, Interaction
from discord.ext import commands

class Feed(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="feed", description="Gets a feed of the requested category")
    async def feed(self, interaction: Interaction) -> None:
        await interaction.response.send_message("🚧 Under Construction 🚧")

# Required for dynamic loading via setup_hook
async def setup(bot) -> None:
    await bot.add_cog(Feed(bot))