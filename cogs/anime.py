from discord import app_commands, Interaction, Embed, Color
from discord.ext import commands
from queries.AniList import AniList
from datetime import datetime
from html2text import html2text

class AnimeCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="anime", description="Gets a feed of the requested category")
    @app_commands.describe(season="Which season do you want? (fall, winter...)")
    async def anime(self, interaction: Interaction, season: str = "fall") -> None:
        sentence_case_season = season[0].upper() + season[1:].lower()
        data: dict = AniList().getAnimeSchedule(season)
        airing_schedules: list = data["data"]["Page"]["airingSchedules"]

        embed: Embed = Embed(
            title=f"{sentence_case_season} 2025 Anime Season",
            description="Here are some airing anime:",
            color=Color.red()
        )


        for anime in airing_schedules:
          anime_media: dict = anime["media"]
          english_name: str = anime_media["title"]["english"]
          romaji_name: str = anime_media["title"]["romaji"]
          name_to_use: str = english_name or romaji_name

          description_markdown = f"\n\n{html2text(anime_media["description"])}\n" if anime_media["description"] else "\n"
          short_desc = (description_markdown[:400] + "...") if len(description_markdown) > 400 else description_markdown

          start_date_string = datetime.fromtimestamp(anime["airingAt"]).strftime("%b %d, %Y")

          try:
            end_date_string = datetime(**anime_media["endDate"]).strftime("%b %d, %Y")
          except:
            end_date_string = "Ongoing"

          field_value: str = (
              f"{short_desc.strip()}\n"
              f"**Start:** {start_date_string} • **End:** {end_date_string}\n"
              f"[More Info]({anime_media['siteUrl']})"
          )

          embed.add_field(
            name=name_to_use,
            value=field_value,
            inline=False
          )

        await interaction.response.send_message(embed=embed)




# Required for dynamic loading via setup_hook
async def setup(bot) -> None:
    await bot.add_cog(AnimeCog(bot))