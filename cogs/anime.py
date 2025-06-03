from discord import app_commands, Interaction, Embed, Color
from discord.ext import commands
from queries.AniList import AniList as AniListQuery
from datetime import datetime
from html2text import html2text
from models.AniList.AniList import AniList
from models.AniList.types import RootResponse, Media

class AnimeCog(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot
  
  def parseAnime(self, anime: Media) -> list:
    english_name: str | None = anime.title.english_name
    romaji_name: str | None = anime.title.romaji_name
    name_to_use: str | None = english_name or romaji_name
    name_to_use = f"✨ **{name_to_use}** ✨"

    description_markdown: str = f"\n\n{html2text(anime.description)}\n" if anime.description else "\n"
    short_desc: str = (description_markdown[:400] + "...") if len(description_markdown) > 400 else description_markdown
    short_desc = short_desc.strip().replace("\n", "")
    
    if anime.startDate and anime.startDate.year and anime.startDate.month and anime.startDate.day:
      start_date_string: str = datetime(
        anime.startDate.year,
        anime.startDate.month,
        anime.startDate.day
      ).strftime("%b %d, %Y")
    else:
      start_date_string = ""
      
    if anime.endDate and anime.endDate.year and anime.endDate.month and anime.endDate.day:
      end_date_string: str|None = datetime(
        anime.endDate.year,
        anime.endDate.month,
        anime.endDate.day
      ).strftime("%b %d, %Y")
    else:
      end_date_string: str|None = None
    
    if anime.airingSchedule and anime.airingSchedule.nodes:
      epoch_time: float | None = anime.airingSchedule.nodes[0].airingAt if anime.airingSchedule.nodes[0].airingAt else None
      airing_day: str|None = datetime.fromtimestamp(epoch_time).strftime("%A") if epoch_time else None
      episodes: int|None = len(anime.airingSchedule.nodes)
    else:
      airing_day = None
      episodes = None
    
    genres: list[str] = anime.genres
    status: str | None = anime.status
    
    return [name_to_use, short_desc, airing_day, episodes, genres, status, start_date_string, end_date_string]

  def generateFieldValue(self, airing_day, episodes, genres: list[str], status, start_date, end_date, description, site_url) -> str:
    airing_str: str = f"🗓️ **Airs:** {airing_day if airing_day else ''}"
    episodes_str: str = f"🎬 **Episodes:** {episodes if episodes else ''}"
    genres_str: str = f"🎭 **Genres:** {','.join(genres)}"
    status_str: str = f"📝 **Status:** {status}"
    airing_from_str: str = f"📅 **From:** {start_date} {f"→ {end_date}" if end_date else ''}"
    description_str: str = f"🧾 **Description:** {description}"
    site_url_str: str = f"🔗 [See more]({site_url})"
    
    return '\n\n'.join([airing_str, episodes_str, genres_str, status_str, airing_from_str, description_str, site_url_str])

  @app_commands.command(name="anime", description="Gets a feed of the requested category")
  @app_commands.describe(season="Which season do you want? (fall, winter...)")
  async def anime(self, interaction: Interaction, season: str = "fall") -> None:
    sentence_case_season = season[0].upper() + season[1:].lower()
    current_year: int = datetime.now().year
    data: dict = AniListQuery().getAnimeSeason(season, current_year)

    embed: Embed = Embed(
        title=f"{sentence_case_season} {current_year} Anime Season",
        color=Color.red()
    )

    parsed: RootResponse = AniList().parse_root_response(data["data"])
    media: list[Media] = parsed.Page.media

    for index, anime in enumerate(media):
      [
        name_to_use,
        short_desc,
        airing_day,
        episodes,
        genres,
        status,
        start_date_string,
        end_date_string
      ] = self.parseAnime(anime)
      
      field_value: str = self.generateFieldValue(
        airing_day,
        episodes,
        anime.genres,
        anime.status,
        start_date_string,
        end_date_string,
        short_desc,
        anime.siteUrl
      )
      
      if index != len(media) - 1:
        field_value += "\n\n~~▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬~~"

      embed.add_field(
        name=name_to_use,
        value=field_value,
        inline=False
      )

    await interaction.response.send_message(embed=embed)

# Required for dynamic loading via setup_hook
async def setup(bot) -> None:
  await bot.add_cog(AnimeCog(bot))