from datetime import datetime, timezone
import time
import requests

URL = "https://graphql.anilist.co"

class AniList:
  def get_season_start_epoch(self, year: int, season: str) -> tuple:
    lower_cased_season: str = season.lower()

    """
    Returns the epoch timestamp (seconds since the Unix epoch) for the start of a given season and year.
    Seasons are defined as:
    - Spring: March 20
    - Summer: June 21
    - Fall: September 22
    - Winter: December 21
    """
    season_starts: dict[str, tuple[int, int, str]] = {
        "spring": (3, 20, "summer"),
        "summer": (6, 21, "fall"),
        "fall": (9, 22, "winter"),
        "winter": (12, 21, "spring")
    }

    if lower_cased_season not in season_starts:
        raise ValueError("Invalid season name. Choose from 'Spring', 'Summer', 'Autumn', or 'Winter'.")

    month, day, next_season = season_starts[season]
    month_next, day_next, _ = season_starts[next_season]

    if season == "winter":
      year_next = year+1
    else:
      year_next = year
    
    # Construct datetime object
    dt_object: datetime = datetime(year, month, day, 0, 0, 0, tzinfo=timezone.utc)
    dt_object_next: datetime = datetime(year_next, month_next, day_next, 0, 0, 0, tzinfo=timezone.utc)

    # Get epoch timestamp
    epoch_time: int = int(dt_object.timestamp())
    epoch_time_next: int = int(dt_object_next.timestamp())

    return (epoch_time, epoch_time_next)

  def getAnimeSchedule(self, season: str) -> dict:
    lower_cased_season: str = season.lower()
    valid_seasons: list[str] = ["fall", "winter", "spring", "summer"]
    current_year: int = datetime.now().year

    if not lower_cased_season in valid_seasons:
      raise ValueError("season is not valid, choose from 'Spring', 'Summer', 'Autumn', or 'Winter'.")

    season_start_epoch, season_end_epoch = self.get_season_start_epoch(current_year, lower_cased_season)
    
    query = '''
        query (
          $airingAt_greater: Int
          $airingAt_lesser: Int
        ) {
          Page(perPage: 5) {
              pageInfo {
                  total
                  perPage
                  currentPage
                  lastPage
                  hasNextPage
              }
              airingSchedules(
                airingAt_greater: $airingAt_greater
                airingAt_lesser: $airingAt_lesser
                sort: TIME
                episode_greater: 1
              ) {
                  id
                  airingAt
                  timeUntilAiring
                  episode
                  mediaId
                  media {
                      title {
                          english
                          romaji
                      }
                      status
                      description
                      startDate {
                          year
                          month
                          day
                      }
                      endDate {
                          year
                          month
                          day
                      }
                      season
                      episodes
                      siteUrl
                  }
              }
          }
      }
    '''

    variables: dict[str, int] = {
      'airingAt_greater': season_start_epoch,
      'airingAt_lesser': season_end_epoch
    }

    res = requests.post(URL, json={'query': query, 'variables': variables})

    return res.json()

