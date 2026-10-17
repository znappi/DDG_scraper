from dataclasses import dataclass

@dataclass
class SearchResult:
    title: str
    url: str
    body: str

@dataclass
class ImageResult:
    title: str
    image: str
    url: str
    source: str
