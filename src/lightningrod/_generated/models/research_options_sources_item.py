from enum import Enum


class ResearchOptionsSourcesItem(str, Enum):
    GOOGLE_SEARCH = "google_search"
    NEWS = "news"
    PERPLEXITY = "perplexity"

    def __str__(self) -> str:
        return str(self.value)
