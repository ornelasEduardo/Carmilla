from typing import Self
from .types import Title, Date, CoverImage, AiringSchedule, AiringScheduleNode, Media, Page, RootResponse
from typing import List

class AniList:
  @classmethod
  def parse_title(self, data: dict) -> Title:
    return Title(
        romaji_name=data.get("romaji"),
        english_name=data.get("english")
    )

  @classmethod
  def parse_date(self, data: dict) -> Date:
    return Date(
        year=data.get("year"),
        month=data.get("month"),
        day=data.get("day")
    )

  @classmethod
  def parse_cover_image(self, data: dict) -> CoverImage:
    return CoverImage(
        large=data.get("large")
    )

  @classmethod
  def parse_airing_schedule_nodes(self, nodes: list[dict]) -> List[AiringScheduleNode]:
    parsed_nodes: list[AiringScheduleNode] = []

    for node in nodes:
      parsed_nodes.append(AiringScheduleNode(
      airingAt=node.get("airingAt"),
      episode=node.get("episode")
    ))
      
    return parsed_nodes

  @classmethod
  def parse_airing_schedule(self, data: dict) -> AiringSchedule:
    return AiringSchedule(
      nodes=self.parse_airing_schedule_nodes(data["nodes"])
    )

  @classmethod
  def parse_media(self, data: dict) -> Media:
    return Media(
        title=self.parse_title(data["title"]),
        description=data.get("description"),
        episodes=data.get("episodes"),
        startDate=self.parse_date(data["startDate"]),
        endDate=self.parse_date(data["endDate"]),
        coverImage=self.parse_cover_image(data["coverImage"]),
        siteUrl=data.get("siteUrl"),
        genres=data.get("genres", []),
        status=data.get("status"),
        airingSchedule=self.parse_airing_schedule(data["airingSchedule"])
    )

  @classmethod
  def parse_page(self, data: dict) -> Page:
    media_list: list[Media] = [self.parse_media(media) for media in data["media"]]
    return Page(media=media_list)

  def parse_root_response(self, data: dict) -> RootResponse:
    return RootResponse(Page=self.parse_page(data["Page"]))