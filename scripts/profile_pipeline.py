"""Profile a Quadrant (QuestionPipeline) transform run with LogFire.

The LightningRod transform runs server-side: ``TransformsClient.run`` submits a
job and then polls ``/transform_jobs/{id}/metrics`` every 15s. The server reports
per-step ``duration_seconds``, ``input_rows``, ``output_rows``, ``rejected_count``
and ``error_count`` for every transform in the pipeline (seed generator,
question generator, context generator(s), labeler, deduplication, renderer,
rollout generator, scorer).

This script mirrors that control flow but wraps it with logfire spans so each
step shows up as its own timed interval in LogFire, and prints a plain-text
bottleneck summary at the end.

Usage:

    pip install "lightningrod-ai[profiling]"
    export LIGHTNINGROD_API_KEY=...
    export LOGFIRE_TOKEN=...            # optional; falls back to local output
    python scripts/profile_pipeline.py --max-questions 50

Run with ``--help`` for all options.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

try:
    import logfire
except ImportError:
    print(
        "logfire is not installed. Install with:\n"
        "    pip install 'lightningrod-ai[profiling]'\n"
        "or:\n"
        "    pip install logfire",
        file=sys.stderr,
    )
    raise

from lightningrod import (
    BinaryAnswerType,
    ForwardLookingQuestionGenerator,
    LightningRod,
    NewsSeedGenerator,
    QuestionPipeline,
    WebSearchLabeler,
)
from lightningrod._generated.models.transform_job_status import TransformJobStatus
from lightningrod._generated.types import Unset
from lightningrod.utils import config


POLL_INTERVAL_SECONDS = 15


@dataclass
class StepTiming:
    """Local bookkeeping for an active logfire span per pipeline step."""

    transform_name: str
    step_index: int
    span_cm: object = None
    span: object = None
    first_seen_monotonic: float = 0.0
    last_duration_seconds: float = 0.0
    last_progress: float = 0.0
    last_input_rows: int = 0
    last_output_rows: int = 0
    last_rejected: int = 0
    last_errors: int = 0
    closed: bool = False
    history: list[dict] = field(default_factory=list)


def _build_default_pipeline() -> QuestionPipeline:
    """A simple news-based pipeline matching notebooks/00_quickstart.ipynb."""
    answer_type = BinaryAnswerType()
    return QuestionPipeline(
        seed_generator=NewsSeedGenerator(
            start_date=datetime(2025, 10, 1),
            end_date=datetime(2025, 11, 1),
            search_query="technology announcements",
        ),
        question_generator=ForwardLookingQuestionGenerator(
            instructions="Generate forward-looking questions about technology announcements.",
            answer_type=answer_type,
        ),
        labeler=WebSearchLabeler(answer_type=answer_type),
    )


def _unwrap(value):
    """Return None for Unset/None attrs fields, the value otherwise."""
    if isinstance(value, Unset) or value is None:
        return None
    return value


def _step_attrs(step) -> dict:
    return {
        "step_index": step.step_index,
        "transform_name": step.transform_name,
        "input_rows": step.input_rows,
        "output_rows": step.output_rows,
        "rejected_count": step.rejected_count,
        "error_count": step.error_count,
        "progress": step.progress,
        "server_duration_seconds": step.duration_seconds,
    }


def profile_pipeline(
    lr: LightningRod,
    pipeline: QuestionPipeline,
    max_questions: Optional[int],
    name: str,
) -> None:
    transforms = lr.transforms
    jobs = transforms.jobs

    with logfire.span(
        "quadrant_pipeline",
        max_questions=max_questions,
        job_name=name,
        pipeline_config_type=type(pipeline).__name__,
    ) as pipeline_span:
        # ---- submit ----
        with logfire.span("submit_job") as submit_span:
            t0 = time.monotonic()
            job = transforms.submit(
                config=pipeline,
                max_questions=max_questions,
                name=name,
            )
            submit_span.set_attribute("job_id", job.id)
            submit_span.set_attribute("client_elapsed_seconds", time.monotonic() - t0)

        pipeline_span.set_attribute("job_id", job.id)
        logfire.info("job_submitted", job_id=job.id, name=name)

        # ---- poll loop ----
        step_timings: dict[int, StepTiming] = {}
        final_metrics = None
        poll_count = 0

        while True:
            poll_count += 1
            with logfire.span("poll_cycle", poll_count=poll_count) as poll_span:
                poll_t0 = time.monotonic()
                job = jobs.get(job.id)
                metrics = jobs.get_metrics(job.id)
                poll_span.set_attribute("server_call_seconds", time.monotonic() - poll_t0)
                poll_span.set_attribute("job_status", str(job.status))

                if metrics is not None:
                    final_metrics = metrics
                    poll_span.set_attribute("total_input_rows", metrics.total_input_rows)
                    poll_span.set_attribute("total_output_rows", metrics.total_output_rows)
                    poll_span.set_attribute(
                        "total_duration_seconds", metrics.total_duration_seconds
                    )

                    for step in sorted(metrics.steps, key=lambda s: s.step_index):
                        timing = step_timings.get(step.step_index)
                        if timing is None:
                            timing = StepTiming(
                                transform_name=step.transform_name,
                                step_index=step.step_index,
                            )
                            step_timings[step.step_index] = timing

                        # Open a span the first time a step shows any activity.
                        if timing.span_cm is None and (
                            step.progress > 0
                            or step.input_rows > 0
                            or step.output_rows > 0
                        ):
                            span_cm = logfire.span(
                                "pipeline_step",
                                step_index=step.step_index,
                                transform_name=step.transform_name,
                            )
                            span = span_cm.__enter__()
                            timing.span_cm = span_cm
                            timing.span = span
                            timing.first_seen_monotonic = time.monotonic()

                        timing.last_progress = step.progress
                        timing.last_duration_seconds = step.duration_seconds
                        timing.last_input_rows = step.input_rows
                        timing.last_output_rows = step.output_rows
                        timing.last_rejected = step.rejected_count
                        timing.last_errors = step.error_count
                        timing.history.append(_step_attrs(step))

                        # Per-poll event so throughput over time is visible.
                        logfire.info(
                            "step_progress",
                            **_step_attrs(step),
                        )

                        # Close the span once the server reports the step done.
                        if (
                            timing.span_cm is not None
                            and not timing.closed
                            and step.progress >= 1.0
                        ):
                            timing.span.set_attribute(
                                "final_input_rows", step.input_rows
                            )
                            timing.span.set_attribute(
                                "final_output_rows", step.output_rows
                            )
                            timing.span.set_attribute(
                                "final_rejected_count", step.rejected_count
                            )
                            timing.span.set_attribute(
                                "final_error_count", step.error_count
                            )
                            timing.span.set_attribute(
                                "server_duration_seconds", step.duration_seconds
                            )
                            timing.span_cm.__exit__(None, None, None)
                            timing.closed = True

            if job.status != TransformJobStatus.RUNNING:
                break
            time.sleep(POLL_INTERVAL_SECONDS)

        # Close any step spans still open (e.g. on failure / cancel).
        for timing in step_timings.values():
            if timing.span_cm is not None and not timing.closed:
                timing.span.set_attribute(
                    "server_duration_seconds", timing.last_duration_seconds
                )
                timing.span_cm.__exit__(None, None, None)
                timing.closed = True

        pipeline_span.set_attribute("final_status", str(job.status))
        pipeline_span.set_attribute("poll_count", poll_count)
        if final_metrics is not None:
            pipeline_span.set_attribute(
                "total_duration_seconds", final_metrics.total_duration_seconds
            )
            pipeline_span.set_attribute(
                "total_input_rows", final_metrics.total_input_rows
            )
            pipeline_span.set_attribute(
                "total_output_rows", final_metrics.total_output_rows
            )

        usage = _unwrap(job.usage)
        if usage is not None:
            cost = _unwrap(usage.current_cost_dollars)
            if cost is not None:
                pipeline_span.set_attribute("cost_dollars", cost)

    # ---- stdout summary (after spans close) ----
    print()
    print("=" * 72)
    print(f"Quadrant pipeline profile: job {job.id}  status={job.status}")
    print("=" * 72)
    if final_metrics is None:
        print("No metrics were returned.")
        return

    total = final_metrics.total_duration_seconds or 0.0
    print(f"Total server-reported duration: {total:.1f}s")
    print(f"Total input rows:  {final_metrics.total_input_rows}")
    print(f"Total output rows: {final_metrics.total_output_rows}")
    print()
    print(f"{'Step':<36}{'Duration':>10}{'Share':>8}{'In':>8}{'Out':>8}{'Rej':>6}{'Err':>6}")
    print("-" * 82)
    ranked = sorted(
        final_metrics.steps, key=lambda s: s.duration_seconds, reverse=True
    )
    for step in ranked:
        share = (step.duration_seconds / total * 100.0) if total > 0 else 0.0
        print(
            f"{step.transform_name[:34]:<36}"
            f"{step.duration_seconds:>9.1f}s"
            f"{share:>7.1f}%"
            f"{step.input_rows:>8}"
            f"{step.output_rows:>8}"
            f"{step.rejected_count:>6}"
            f"{step.error_count:>6}"
        )

    if ranked:
        worst = ranked[0]
        worst_share = (worst.duration_seconds / total * 100.0) if total > 0 else 0.0
        print()
        print(
            f"Likely bottleneck: {worst.transform_name} "
            f"({worst.duration_seconds:.1f}s, {worst_share:.1f}% of total)"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-questions",
        type=int,
        default=50,
        help="Cap the number of questions generated (keeps the run short).",
    )
    parser.add_argument(
        "--name",
        default=f"profile-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        help="Name for the transform job.",
    )
    parser.add_argument(
        "--service-name",
        default="lightningrod-sdk-profile",
        help="Service name reported to LogFire.",
    )
    args = parser.parse_args()

    # LogFire reads LOGFIRE_TOKEN from the environment. Without a token it still
    # runs but only emits locally, which is fine for ad-hoc profiling.
    logfire.configure(
        service_name=args.service_name,
        send_to_logfire="if-token-present",
    )
    # Trace outbound HTTP so we can also see the raw API latency per request.
    try:
        logfire.instrument_httpx()
    except Exception:
        pass

    api_key = config.get_config_value("LIGHTNINGROD_API_KEY")
    if not api_key:
        print("LIGHTNINGROD_API_KEY is not set.", file=sys.stderr)
        return 2

    lr = LightningRod(api_key=api_key)
    pipeline = _build_default_pipeline()

    profile_pipeline(
        lr=lr,
        pipeline=pipeline,
        max_questions=args.max_questions,
        name=args.name,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
