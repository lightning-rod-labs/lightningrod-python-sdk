from enum import Enum


class RewardFunctionType(str, Enum):
    BINARY_BRIER = "binary_brier"
    BINARY_LOG_SCORE = "binary_log_score"
    BINARY_WEIGHTED_BRIER = "binary_weighted_brier"
    CONTINUOUS_CRPS = "continuous_crps"
    CONTINUOUS_LOG_SCORE = "continuous_log_score"
    CONTINUOUS_VALUE_ONLY_LINEAR_SCORE = "continuous_value_only_linear_score"
    CONTINUOUS_VALUE_ONLY_LOG_SCORE = "continuous_value_only_log_score"
    MULTI_CHOICE_BRIER = "multi_choice_brier"
    MULTI_CHOICE_LOG_SCORE = "multi_choice_log_score"
    RANKING_DELTA_NDCG = "ranking_delta_ndcg"

    def __str__(self) -> str:
        return str(self.value)
