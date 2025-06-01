from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Title:
  romaji_name: Optional[str]
  english_name: Optional[str]

@dataclass
class Date:
  year: Optional[int]
  month: Optional[int]
  day: Optional[int]

@dataclass
class CoverImage:
  large: Optional[str]
  
@dataclass
class AiringScheduleNode:
  airingAt: Optional[float]  # Epoch time
  episode: Optional[int]

@dataclass
class AiringSchedule:
  nodes: List[AiringScheduleNode]

@dataclass
class Media:
  title: Title
  description: Optional[str]
  episodes: Optional[int]
  startDate: Date
  endDate: Date
  coverImage: CoverImage
  siteUrl: Optional[str]
  genres: List[str]
  status: Optional[str]
  airingSchedule: Optional[AiringSchedule]

@dataclass
class Page:
  media: List[Media]

@dataclass
class RootResponse:
  Page: Page
