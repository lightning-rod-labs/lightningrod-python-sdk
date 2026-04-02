def multiple_choice_example(
    question: str,
    options: list[str],
    label: int | str | None = None,
    comment: str | None = None,
) -> str:
    """Build a formatted multiple-choice example string.

    Args:
        question: The question text.
        options: Answer option texts. Auto-labeled option_0, option_1, …
        label: Correct option for good examples. Accepts an int (1 → options[1])
            or the option text directly ("No change"). Mutually exclusive with comment.
        comment: Explanation for bad examples (e.g. "Only two options given").
            Mutually exclusive with label.

    Examples:
        # good example
        multiple_choice_example(
            "What will the ECB decide at its April 10, 2025 meeting?",
            ["Rate increase", "No change", "Rate cut"],
            label=1,
        )

        # bad example
        multiple_choice_example(
            "Which of the following will occur by December 31, 2025?",
            ["Japan raises interest rates", "Apple releases a foldable iPhone"],
            comment="Multiple unrelated events; violates single-event criterion.",
        )
    """
    if label is not None and comment is not None:
        raise ValueError("Provide either label (good example) or comment (bad example), not both.")

    if isinstance(label, int):
        if label < 0 or label >= len(options):
            raise ValueError(f"label index {label} is out of range for {len(options)} options.")
        label = options[label]
    elif isinstance(label, str) and label not in options:
        raise ValueError(f"label {label!r} does not match any option.")

    lines = [f"Question: {question}"]
    for i, option in enumerate(options):
        lines.append(f"option_{i}: {option}")
    if label is not None:
        lines.append(f"Label: {label}")
    if comment is not None:
        lines.append(f"Comment: {comment}")
    return "\n".join(lines)


def binary_example(question: str, comment: str | None = None) -> str:
    """Build a formatted binary example string.

    Args:
        question: The question text.
        comment: Explanation for bad examples (e.g. "No resolution date given").

    Examples:
        # good example
        binary_example("Will the Fed cut rates at its May 6, 2026 FOMC meeting?")

        # bad example
        binary_example(
            "Will inflation rise?",
            comment="No time frame, no specific metric, no resolution date.",
        )
    """
    lines = [f"Question: {question}"]
    if comment is not None:
        lines.append(f"Comment: {comment}")
    return "\n".join(lines)


def continuous_example(question: str, comment: str | None = None) -> str:
    """Build a formatted continuous example string.

    Args:
        question: The question text.
        comment: Explanation for bad examples (e.g. "Averaging period not complete").

    Examples:
        # good example
        continuous_example(
            "What will be the U.S. CPI year-over-year inflation rate for March 2026 "
            "as reported by the Bureau of Labor Statistics?"
        )

        # bad example
        continuous_example(
            "How much will the economy grow soon?",
            comment="Vague timing, no country, no metric, no units.",
        )
    """
    lines = [f"Question: {question}"]
    if comment is not None:
        lines.append(f"Comment: {comment}")
    return "\n".join(lines)
