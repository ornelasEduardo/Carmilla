from datetime import datetime, timezone
import time
from requests import post, Response

class AniList:
  def __init__(self, page: int = 1, per_page: int = 5) -> None:
    self.page = page
    self.per_page = per_page
    
  def getUrl(self) -> str:
    return "https://graphql.anilist.co"

  def getAnimeSeason(self, season: str, season_year: int) -> dict:
    lower_cased_season: str = season.lower()
    valid_seasons: list[str] = ["fall", "winter", "spring", "summer"]

    if not lower_cased_season in valid_seasons:
      raise ValueError("season is not valid, choose from 'Spring', 'Summer', 'Autumn', or 'Winter'.")
    
    query = '''
      query ($season: MediaSeason, $seasonYear: Int, $page: Int, $perPage: Int) {
        Page(page: $page, perPage: $perPage) {
          media(season: $season, seasonYear: $seasonYear, type: ANIME, sort: POPULARITY_DESC) {
            title {
              romaji
              english
            }
            description(asHtml: false)
            episodes
            startDate { year month day }
            endDate { year month day }
            coverImage { large }
            siteUrl
            genres
            status
            airingSchedule(notYetAired: true, perPage: 1) {
              nodes {
                airingAt
                episode
              }
            }
          }
        }
      }
    '''

    variables: dict[str, int|str] = {
      "season": season.upper(),
      "seasonYear": season_year,
      "page": self.page,
      "perPage": self.per_page
    }

    res: Response = post(self.getUrl(), json={'query': query, 'variables': variables})

    return res.json()

