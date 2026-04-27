from __future__ import annotations

from datetime import datetime, timezone

from rich.console import Console

from lightningrod import display_lint_overview, display_lint_detailed
from lightningrod._generated.models import (
    DatasetLinterRunResponse,
    LinterIssue,
    LinterIssueMeta,
    RuleResult,
    RuleResultStats,
    RunSummary,
    RunSummaryByRule,
    RunSummaryBySeverity,
    Severity,
)


def _render_text(renderable: object) -> str:
    console = Console(record=True, width=240)
    console.print(renderable)
    return console.export_text()


def _render_text_at_width(renderable: object, width: int) -> str:
    console = Console(record=True, width=width)
    console.print(renderable)
    return console.export_text()


def _run() -> DatasetLinterRunResponse:
    by_rule = RunSummaryByRule()
    by_rule.additional_properties = {"base_rate": 0, "prediction_date_distribution": 1}

    by_severity = RunSummaryBySeverity()
    by_severity.additional_properties = {"error": 1}

    stats = RuleResultStats()
    stats.additional_properties = {"valid_rows": 375, "span_days": 515}

    meta = LinterIssueMeta()
    meta.additional_properties = {"count": 7}

    return DatasetLinterRunResponse(
        id="run-1",
        dataset_id="dataset-1",
        status="COMPLETED",
        rules_requested=["base_rate", "prediction_date_distribution"],
        sample_size=50,
        created_at=datetime(2026, 4, 27, tzinfo=timezone.utc),
        updated_at=datetime(2026, 4, 27, 0, 1, tzinfo=timezone.utc),
        summary=RunSummary(total_issues=1, by_rule=by_rule, by_severity=by_severity),
        rules=[
            RuleResult(name="base_rate", issues=[], duration_ms=62),
            RuleResult(
                name="prediction_date_distribution",
                stats=stats,
                issues=[
                    LinterIssue(
                        rule="prediction_date_distribution",
                        severity=Severity.ERROR,
                        message="7 row(s) have prediction_date >= resolution_date.",
                        tip="Temporal leakage.",
                        affected_sample_ids=["sample-1", "sample-2"],
                        meta=meta,
                    )
                ],
                duration_ms=25,
            ),
        ],
    )


def test_dataset_linter_overview_display_includes_summary() -> None:
    text = _render_text(display_lint_overview(_run()))

    assert "Dataset Linter: COMPLETED" in text
    assert "run-1" in text
    assert "dataset-1" in text
    assert "Issues:" in text
    assert "prediction_date_distribution" in text
    assert "error: 1" in text


def test_dataset_linter_display_helpers_are_importable_from_top_level(capsys) -> None:
    run = _run()

    display_lint_overview(run)
    display_lint_detailed(run)

    captured = capsys.readouterr()
    assert "Dataset Linter: COMPLETED" in captured.out
    assert "Dataset Linter Details" in captured.out


def test_dataset_linter_details_display_includes_issue_details() -> None:
    text = _render_text(display_lint_detailed(_run(), max_sample_ids=1))

    assert "Dataset Linter Details" in text
    assert "span_days" in text
    assert "7 row(s) have prediction_date >= resolution_date." in text
    assert "sample-1" in text
    assert "+1 more" in text
    assert '{"count": 7}' in text


def test_dataset_linter_details_orders_rules_by_issue_priority_then_count() -> None:
    run = _run()
    run.rules = [
        RuleResult(
            name="warning_rule",
            issues=[
                LinterIssue(rule="warning_rule", severity=Severity.WARNING, message="warning one"),
                LinterIssue(rule="warning_rule", severity=Severity.WARNING, message="warning two"),
            ],
        ),
        RuleResult(
            name="info_rule",
            issues=[
                LinterIssue(rule="info_rule", severity=Severity.INFO, message="info one"),
            ],
        ),
        RuleResult(
            name="error_rule",
            issues=[
                LinterIssue(rule="error_rule", severity=Severity.ERROR, message="error one"),
            ],
        ),
        RuleResult(name="clean_rule", issues=[]),
    ]

    text = _render_text(display_lint_detailed(run))

    assert text.index("error_rule") < text.index("warning_rule")
    assert text.index("warning_rule") < text.index("info_rule")
    assert text.index("info_rule") < text.index("clean_rule")


def test_dataset_linter_details_orders_issues_by_severity_then_affected_count() -> None:
    run = _run()
    run.rules = [
        RuleResult(
            name="mixed_rule",
            issues=[
                LinterIssue(
                    rule="mixed_rule",
                    severity=Severity.WARNING,
                    message="warning many",
                    affected_sample_ids=["a", "b", "c"],
                ),
                LinterIssue(
                    rule="mixed_rule",
                    severity=Severity.ERROR,
                    message="error few",
                    affected_sample_ids=["a"],
                ),
                LinterIssue(
                    rule="mixed_rule",
                    severity=Severity.ERROR,
                    message="error many",
                    affected_sample_ids=["a", "b"],
                ),
            ],
        ),
    ]

    text = _render_text(display_lint_detailed(run))

    assert text.index("error many") < text.index("error few")
    assert text.index("error few") < text.index("warning many")


def test_dataset_linter_details_does_not_truncate_long_issue_messages() -> None:
    run = _run()
    message = (
        "Context relevance score 0.20: the context contains several clauses, "
        "citations, caveats, and counterclaims that make this warning span well "
        "past a normal terminal width while still ending with UNIQUE_FINAL_TOKEN."
    )
    run.rules = [
        RuleResult(
            name="long_message_rule",
            issues=[LinterIssue(rule="long_message_rule", severity=Severity.WARNING, message=message)],
        )
    ]

    text = _render_text_at_width(display_lint_detailed(run), width=80)

    assert "UNIQUE_FINAL_TOKEN" in text
