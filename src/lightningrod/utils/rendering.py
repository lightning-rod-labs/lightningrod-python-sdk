"""Utilities for rendering Sample objects into prompt strings."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from lightningrod._generated.models.forward_looking_question import ForwardLookingQuestion
from lightningrod._generated.models.news_context import NewsContext
from lightningrod._generated.models.rag_context import RAGContext
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.types import Unset
from lightningrod._generated.models.binary_answer_type import BinaryAnswerType
from lightningrod._generated.models.continuous_answer_type import ContinuousAnswerType
from lightningrod._generated.models.multiple_choice_answer_type import MultipleChoiceAnswerType
from lightningrod._generated.models.free_response_answer_type import FreeResponseAnswerType

AnswerType = Union[BinaryAnswerType, ContinuousAnswerType, MultipleChoiceAnswerType, FreeResponseAnswerType]

# Headers and descriptions for each context type
_CONTEXT_TYPE_HEADERS: Dict[str, str] = {
    "NEWS_CONTEXT": "NEWS:",
    "RAG_CONTEXT": "DOCUMENTS:",
}

_CONTEXT_TYPE_DESCRIPTIONS: Dict[str, str] = {
    "NEWS_CONTEXT": "Recent news articles relevant to this question:",
    "RAG_CONTEXT": "Retrieved documents relevant to this question:",
}


def _get_context_type(ctx: Union[NewsContext, RAGContext]) -> str:
    """Get the context type string from a context object."""
    if isinstance(ctx, NewsContext):
        return "NEWS_CONTEXT"
    elif isinstance(ctx, RAGContext):
        return "RAG_CONTEXT"
    return "CONTEXT"


def _render_context(context: List[Union[NewsContext, RAGContext]]) -> str:
    """Render context objects grouped by type with headers."""
    if not context:
        return ""

    contexts_by_type: Dict[str, List[Union[NewsContext, RAGContext]]] = {}
    for ctx in context:
        ct = _get_context_type(ctx)
        if ct not in contexts_by_type:
            contexts_by_type[ct] = []
        contexts_by_type[ct].append(ctx)

    rendered_sections: List[str] = []
    for context_type, type_contexts in contexts_by_type.items():
        header = _CONTEXT_TYPE_HEADERS.get(context_type, "CONTEXT:")
        description = _CONTEXT_TYPE_DESCRIPTIONS.get(context_type, "")
        content = "\n\n".join(ctx.rendered_context for ctx in type_contexts)
        rendered_sections.append(f"{header}\n{description}\n\n{content}")

    return "\n\n".join(rendered_sections)


def render_sample(
    sample: Sample,
    template: Optional[str] = None,
    answer_type: Optional[AnswerType] = None,
) -> str:
    """Render a sample into a prompt string.

    Args:
        sample: The Sample to render.
        template: Optional template string with placeholders: {question_text},
            {context}, {answer_instructions}, {date_close}.
        answer_type: Optional AnswerType to include answer format instructions.

    Returns:
        The rendered prompt string.
    """
    template_values: Dict[str, Any] = {}

    # Question text
    question = sample.question if not isinstance(sample.question, Unset) else None
    question_text = question.question_text if question else ""
    template_values["question_text"] = question_text

    # Context
    context_list = sample.context if not isinstance(sample.context, Unset) else None
    rendered_context = _render_context(context_list) if context_list else ""
    template_values["context"] = rendered_context

    # Answer instructions
    answer_instructions = answer_type.answer_format_instruction if answer_type else ""
    if isinstance(answer_instructions, Unset) or answer_instructions is None:
        answer_instructions = ""
    template_values["answer_instructions"] = answer_instructions

    # Close date and other ForwardLookingQuestion fields
    date_close: Optional[str] = None
    todays_date: Optional[str] = None
    resolution_criteria: Optional[str] = None
    if question and isinstance(question, ForwardLookingQuestion):
        date_close = question.date_close.strftime("%Y-%m-%d")
        template_values["date_close"] = date_close
        todays_date = question.event_date.strftime("%Y-%m-%d")
        template_values["question_date"] = todays_date
        resolution_criteria = question.resolution_criteria
        template_values["resolution_criteria"] = resolution_criteria

    if not isinstance(sample.seed, Unset):
        template_values["seed"] = sample.seed
    if not isinstance(sample.question, Unset):
        template_values["question"] = sample.question
    if not isinstance(sample.label, Unset):
        template_values["label"] = sample.label
    if not isinstance(sample.meta, Unset):
        template_values["meta"] = sample.meta

    # Use provided template
    if template is not None:
        return template.format(**template_values)

    sections: List[str] = ["QUESTION:\n{question_text}"]
    if resolution_criteria:
        sections.append("RESOLUTION CRITERIA:\n{resolution_criteria}")
    if rendered_context.strip():
        sections.append("CONTEXT:\n{context}")
    if answer_instructions.strip():
        sections.append("ANSWER FORMAT:\n{answer_instructions}")
    if date_close:
        sections.append("CLOSE DATE:\n{date_close}")
    if todays_date:
        sections.append("TODAY'S DATE:\n{question_date}")

    return "\n\n".join(sections).format(**template_values)
