"""Utilities for rendering Sample objects into prompt strings."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from lightningrod._generated.models.answer_type import AnswerType
from lightningrod._generated.models.answer_type_enum import AnswerTypeEnum
from lightningrod._generated.models.forward_looking_question import ForwardLookingQuestion
from lightningrod._generated.models.news_context import NewsContext
from lightningrod._generated.models.rag_context import RAGContext
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.types import Unset


# Default answer format instructions for each answer type
_DEFAULT_ANSWER_FORMATS: Dict[AnswerTypeEnum, str] = {
    AnswerTypeEnum.BINARY: (
        "This is a binary yes/no question. You are estimating the probability that the answer is 'Yes'. "
        "Provide your confidence as a value between 0 (definitely No) and 1 (definitely Yes). "
        "Provide your probability estimate for Yes as a decimal between 0 and 1. "
        r"Format your answer as: \boxed{0.75}"
    ),
    AnswerTypeEnum.MULTIPLE_CHOICE: (
        "This is a multiple choice question with answer options labeled with letters starting from A. "
        "The list of options will be provided in the question. "
        "You are estimating the probability for each option being the correct answer. "
        "Provide your confidence for each option as a value between 0 and 1, where the probabilities must sum to 1. "
        "Provide your probability estimate for each option as a decimal between 0 and 1. "
        r"Format your answer as: \boxed{A: 0.3, B: 0.4, C: 0.2, D: 0.1}"
    ),
    AnswerTypeEnum.CONTINUOUS: (
        "This question expects a numeric value as the answer. "
        "Provide your best estimate as a single number. Include units if specified in the question. "
        r"Provide your final answer wrapped in \boxed{}. Example: \boxed{42.5}"
    ),
    AnswerTypeEnum.FREE_RESPONSE: (
        "This question expects a free-form text response. "
        "Provide an answer that directly addresses what the question is asking. "
        r"Provide your final answer wrapped in \boxed{}. Example: \boxed{The company announced a new product line.}"
    ),
}

# Headers and descriptions for each context type
_CONTEXT_TYPE_HEADERS: Dict[str, str] = {
    "NEWS_CONTEXT": "NEWS:",
    "RAG_CONTEXT": "DOCUMENTS:",
}

_CONTEXT_TYPE_DESCRIPTIONS: Dict[str, str] = {
    "NEWS_CONTEXT": "Recent news articles relevant to this question:",
    "RAG_CONTEXT": "Retrieved documents relevant to this question:",
}


def _get_answer_format_instruction(answer_type: AnswerType) -> str:
    """Get the answer format instruction, falling back to defaults."""
    if not isinstance(answer_type.answer_format_instruction, Unset) and answer_type.answer_format_instruction is not None:
        return answer_type.answer_format_instruction
    return _DEFAULT_ANSWER_FORMATS.get(answer_type.answer_type, "")


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
    rendered_answer_instructions = _get_answer_format_instruction(answer_type) if answer_type else ""
    template_values["answer_instructions"] = rendered_answer_instructions

    # Close date (only for ForwardLookingQuestion)
    date_close: Optional[str] = None
    if question and isinstance(question, ForwardLookingQuestion):
        date_close = question.date_close.strftime("%Y-%m-%d")
        template_values["date_close"] = date_close

    # Use provided template
    if template is not None:
        return template.format(**template_values)

    # Dynamic template building
    sections: List[str] = ["QUESTION:\n{question_text}"]
    if rendered_context.strip():
        sections.append("CONTEXT:\n{context}")
    if rendered_answer_instructions.strip():
        sections.append("ANSWER FORMAT:\n{answer_instructions}")
    if date_close:
        sections.append("CLOSE DATE:\n{date_close}")

    return "\n\n".join(sections).format(**template_values)
