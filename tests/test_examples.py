import pytest

from lightningrod import binary_example, continuous_example, multiple_choice_example


class TestMultipleChoiceExample:
    def test_good_example_int_label(self) -> None:
        result = multiple_choice_example(
            "What will the ECB decide at its April 10, 2025 meeting?",
            ["Rate increase", "No change", "Rate cut"],
            label=1,
        )
        assert result == (
            "Question: What will the ECB decide at its April 10, 2025 meeting?\n"
            "option_0: Rate increase\n"
            "option_1: No change\n"
            "option_2: Rate cut\n"
            "Label: No change"
        )

    def test_good_example_string_label(self) -> None:
        result = multiple_choice_example(
            "What will the ECB decide?",
            ["Rate increase", "No change", "Rate cut"],
            label="Rate cut",
        )
        assert result.endswith("Label: Rate cut")

    def test_good_example_first_option(self) -> None:
        result = multiple_choice_example("Q?", ["A", "B", "C"], label=0)
        assert "Label: A" in result

    def test_bad_example_comment(self) -> None:
        result = multiple_choice_example(
            "Which of the following will occur by December 31, 2025?",
            ["Japan raises interest rates", "Apple releases a foldable iPhone", "Brazil hosts a climate summit"],
            comment="Multiple unrelated events; violates single-event criterion.",
        )
        assert result == (
            "Question: Which of the following will occur by December 31, 2025?\n"
            "option_0: Japan raises interest rates\n"
            "option_1: Apple releases a foldable iPhone\n"
            "option_2: Brazil hosts a climate summit\n"
            "Comment: Multiple unrelated events; violates single-event criterion."
        )

    def test_no_label_no_comment(self) -> None:
        result = multiple_choice_example("Q?", ["A", "B", "C"])
        assert "Label:" not in result
        assert "Comment:" not in result
        assert result == "Question: Q?\noption_0: A\noption_1: B\noption_2: C"

    def test_options_auto_indexed(self) -> None:
        result = multiple_choice_example("Q?", ["A", "B", "C", "D", "E"])
        for i in range(5):
            assert f"option_{i}:" in result

    def test_label_and_comment_raises(self) -> None:
        with pytest.raises(ValueError, match="not both"):
            multiple_choice_example("Q?", ["A", "B"], label=0, comment="reason")

    def test_label_out_of_range_raises(self) -> None:
        with pytest.raises(ValueError, match="out of range"):
            multiple_choice_example("Q?", ["A", "B", "C"], label=5)

    def test_label_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="out of range"):
            multiple_choice_example("Q?", ["A", "B"], label=-1)

    def test_string_label_not_in_options_raises(self) -> None:
        with pytest.raises(ValueError, match="does not match any option"):
            multiple_choice_example("Q?", ["A", "B", "C"], label="D")


class TestBinaryExample:
    def test_good_example(self) -> None:
        result = binary_example("Will the Fed cut rates at its May 6, 2026 FOMC meeting?")
        assert result == "Question: Will the Fed cut rates at its May 6, 2026 FOMC meeting?"

    def test_bad_example_comment(self) -> None:
        result = binary_example(
            "Will inflation rise?",
            comment="No time frame, no specific metric, no resolution date.",
        )
        assert result == (
            "Question: Will inflation rise?\n"
            "Comment: No time frame, no specific metric, no resolution date."
        )

    def test_no_comment(self) -> None:
        result = binary_example("Will X happen?")
        assert "Comment:" not in result
        assert result == "Question: Will X happen?"


class TestContinuousExample:
    def test_good_example(self) -> None:
        result = continuous_example(
            "What will be the U.S. CPI year-over-year inflation rate for March 2026 "
            "as reported by the Bureau of Labor Statistics?"
        )
        assert result.startswith("Question: What will be the U.S. CPI")
        assert "Comment:" not in result

    def test_bad_example_comment(self) -> None:
        result = continuous_example(
            "How much will the economy grow soon?",
            comment="Vague timing, no country, no metric, no units.",
        )
        assert result == (
            "Question: How much will the economy grow soon?\n"
            "Comment: Vague timing, no country, no metric, no units."
        )

    def test_no_comment(self) -> None:
        result = continuous_example("What will GDP be?")
        assert "Comment:" not in result
        assert result == "Question: What will GDP be?"
