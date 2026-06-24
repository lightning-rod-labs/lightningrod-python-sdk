from enum import Enum


class ResearchOptionsSourcesItem(str, Enum):
    GOOGLE_SEARCH = "google_search"
    GOOGLE_NEWS = "google_news"
    PERPLEXITY = "perplexity"

    def __str__(self) -> str:
        return str(self.value)
