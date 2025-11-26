from enum import Enum


class TransformType(str, Enum):
    NEWS_SEED_GENERATOR = "NEWS_SEED_GENERATOR"
    PIPELINE = "PIPELINE"
    QUESTION_GENERATOR = "QUESTION_GENERATOR"
    QUESTION_PIPELINE = "QUESTION_PIPELINE"
    SCULPT = "SCULPT"
    WEB_SEARCH_LABELER = "WEB_SEARCH_LABELER"

    def __str__(self) -> str:
        return str(self.value)
