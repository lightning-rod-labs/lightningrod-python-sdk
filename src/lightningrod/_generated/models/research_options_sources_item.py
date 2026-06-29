from enum import Enum


class ResearchOptionsSourcesItem(str, Enum):
    GOOGLE_NEWS = "google_news"
    PERPLEXITY = "perplexity"

    def __str__(self) -> str:
        return str(self.value)
