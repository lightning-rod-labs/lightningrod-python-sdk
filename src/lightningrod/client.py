from lightningrod.utils import config
from lightningrod.prediction import (
    DEFAULT_MODEL,
    AnswerType,
    BinaryPrediction,
    ContinuousPrediction,
    FreeResponsePrediction,
    MultiChoicePrediction,
    PredictionResult,
    ReasoningEffort,
    Source,
    Usage,
    _parse_prediction,
)


def _build_usage(usage: dict) -> Usage:
    return Usage(
        prompt_tokens=usage.get("prompt_tokens", 0),
        completion_tokens=usage.get("completion_tokens", 0),
        total_tokens=usage.get("total_tokens", 0),
        research_cost_usd=usage.get("research_cost_usd"),
        classification_cost_usd=usage.get("classification_cost_usd"),
        inference_cost_usd=usage.get("inference_cost_usd"),
        cost_usd=usage.get("cost_usd"),
    )


class LightningRod:
    """
    Python SDK for the Lightning Rod API.

    Args:
        api_key: Your Lightning Rod API key
        base_url: Base URL for the API (defaults to production)

    Example:
        >>> lr = LightningRod(api_key="your-api-key")
        >>> result = lr.predict("Will the Fed cut rates by 25bp in March 2026?", answer_type="binary")
        >>> print(result.binary.probability)
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.lightningrod.ai/v1"
    ):
        # Resolve credentials lazily (at instantiation, not at import time) so a
        # missing key doesn't blow up `import lightningrod`.
        if api_key is None:
            api_key = config.get_config_value("LIGHTNINGROD_API_KEY")

        base_url = config.get_config_value("LIGHTNINGROD_BASE_URL", base_url)

        self.api_key: str = api_key
        self.base_url: str = base_url.rstrip("/")

    def predict(
        self,
        prompt: str,
        *,
        model: str | None = None,
        research: bool | list[str] | None = None,
        answer_type: AnswerType | str | None = None,
        reasoning_effort: ReasoningEffort | str = ReasoningEffort.MEDIUM,
        system_prompt: str | None = None,
        **kwargs,
    ) -> PredictionResult:
        """Run a single prediction against a Lightning Rod model.

        Args:
            prompt: The question or prompt text.
            model: The model to query. Accepts the same IDs as the
                OpenAI-compatible endpoint, in either short form
                (``"foresight-v4"``) or full provider form
                (``"LightningRodLabs/foresight-v4"``), as well as a trained
                checkpoint ID. Defaults to the latest hosted forecasting model
                (:data:`~lightningrod.prediction.DEFAULT_MODEL`).
            research: Enable web research. ``True`` uses all available sources;
                a list such as ``["perplexity", "google_news"]`` restricts to specific
                sources; ``False``/``None`` disables research.
            answer_type: Requested structured-answer format. Accepts an
                :class:`AnswerType` or its string value. ``None`` omits answer
                formatting and returns prose only.
            reasoning_effort: ``"low"``, ``"medium"`` or ``"high"`` (default
                medium). Accepts a :class:`ReasoningEffort` or its string value.
            system_prompt: Optional system message prepended to the request.
            **kwargs: Forwarded to ``openai.chat.completions.create`` for any
                additional parameters.

        Returns:
            A :class:`PredictionResult` with the full content, reasoning,
            sources, usage and the typed prediction matching ``answer_type``.

        .. note::
            **Breaking change:** ``prompt`` is now the first positional
            argument and the model moved to an optional ``model`` keyword
            argument (was the required first positional ``model_id``).
            ``predict()`` also now returns a structured
            :class:`PredictionResult` rather than the raw content string; the
            raw string is available as ``result.content``. The ``research``,
            ``answer_type`` and ``reasoning_effort`` parameters are first-class
            keyword arguments rather than ``extra_body`` passthroughs.
        """
        _at = answer_type.value if isinstance(answer_type, AnswerType) else answer_type
        if _at == "auto":
            raise ValueError(
                "answer_type='auto' is not supported by predict(). "
                "Use a specific answer_type ('binary', 'continuous', 'multiple_choice', "
                "or 'free_response'), or omit it for unstructured prose."
            )

        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Run `pip install openai` to use lr.predict().")
        client = OpenAI(api_key=self.api_key, base_url=f"{self.base_url}/openai")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Lightning Rod-specific params travel in the request body alongside the
        # standard OpenAI fields via extra_body.
        extra_body: dict = dict(kwargs.pop("extra_body", {}) or {})
        extra_body["reasoning_effort"] = (
            reasoning_effort.value
            if isinstance(reasoning_effort, ReasoningEffort)
            else reasoning_effort
        )
        if research is True:
            extra_body["research"] = True
        elif isinstance(research, list):
            extra_body["research"] = {"sources": research}
        # research False/None: omit
        if answer_type is not None:
            extra_body["answer_type"] = (
                answer_type.value if isinstance(answer_type, AnswerType) else answer_type
            )

        response = client.chat.completions.create(
            model=model or DEFAULT_MODEL,
            messages=messages,
            extra_body=extra_body,
            **kwargs,
        )

        return self._build_prediction_result(response, answer_type)

    @staticmethod
    def _build_prediction_result(response, answer_type) -> PredictionResult:
        data = response.model_dump()
        message = data["choices"][0]["message"]
        content = message.get("content") or ""

        prediction = _parse_prediction(content, answer_type)
        result = PredictionResult(
            content=content,
            thinking=message.get("thinking"),
            sources=[
                Source(
                    url=ann["url_citation"]["url"],
                    title=ann["url_citation"].get("title", ""),
                )
                for ann in (message.get("annotations") or [])
                if ann.get("type") == "url_citation"
            ],
            usage=_build_usage(data.get("usage") or {}),
            model=data.get("model", ""),
            id=data.get("id", ""),
        )

        if isinstance(prediction, BinaryPrediction):
            result.binary = prediction
        elif isinstance(prediction, ContinuousPrediction):
            result.continuous = prediction
        elif isinstance(prediction, MultiChoicePrediction):
            result.multiple_choice = prediction
        elif isinstance(prediction, FreeResponsePrediction):
            result.free_response = prediction

        return result
