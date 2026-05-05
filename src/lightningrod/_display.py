from __future__ import annotations

import json
import math
from typing import Any, Callable, Optional

from rich.console import Console, Group, RenderableType
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from lightningrod._generated.models import EvalJob, PipelineMetricsResponse, TransformJob
from lightningrod._generated.models.transform_job_status import TransformJobStatus
from lightningrod._generated.models.eval_job_status import EvalJobStatus
from lightningrod._generated.models.training_job import TrainingJob
from lightningrod._generated.models.training_job_status import TrainingJobStatus
from lightningrod._generated.types import Unset


def _is_set(value: Any) -> bool:
    return not isinstance(value, Unset) and value is not None


def _safe_markup(text: Optional[str]) -> Text:
    """Parse text as rich markup, falling back to plain text if parsing fails."""
    if text is None:
        return Text("")
    try:
        return Text.from_markup(text)
    except Exception:
        return Text(text)


def _format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.0f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def _format_linter_duration(milliseconds: Any) -> str:
    if not _is_set(milliseconds):
        return "-"
    if milliseconds < 1000:
        return f"{milliseconds}ms"
    return f"{milliseconds / 1000:.1f}s"


def _format_linter_datetime(value: Any) -> str:
    if not _is_set(value):
        return "-"
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


def _linter_status_style(status: str) -> str:
    return {
        "COMPLETED": "bold bright_green",
        "FAILED": "bold bright_red",
        "RUNNING": "bold bright_blue",
        "PENDING": "bold yellow",
    }.get(status.upper(), "bold")


def _linter_severity_style(severity: str) -> str:
    return {
        "error": "bold bright_red",
        "warning": "bold yellow",
        "info": "bright_blue",
    }.get(severity.lower(), "dim")


def _linter_severity_order(item: tuple[str, int]) -> tuple[int, str]:
    return ({"error": 0, "warning": 1, "info": 2}.get(item[0].lower(), 99), item[0])


def _linter_severity_rank(severity: str) -> int:
    return {"error": 0, "warning": 1, "info": 2}.get(severity.lower(), 99)


def _linter_count_map(value: Any) -> dict[str, int]:
    if not _is_set(value):
        return {}
    if hasattr(value, "additional_properties"):
        return dict(value.additional_properties)
    if isinstance(value, dict):
        return value
    return {}


def _linter_rule_issue_count(rule: Any) -> int:
    return len(rule.issues) if _is_set(rule.issues) else 0


def _linter_rule_severity_counts(rule: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not _is_set(rule.issues):
        return counts
    for issue in rule.issues:
        severity = getattr(issue.severity, "value", issue.severity)
        severity = str(severity)
        counts[severity] = counts.get(severity, 0) + 1
    return counts


def _linter_rule_sort_key(rule: Any) -> tuple[int, int, str]:
    counts = _linter_rule_severity_counts(rule)
    highest_severity = min((_linter_severity_rank(severity) for severity in counts), default=99)
    return (highest_severity, -_linter_rule_issue_count(rule), rule.name)


def _linter_issue_sort_key(issue: Any) -> tuple[int, int, str]:
    severity = str(getattr(issue.severity, "value", issue.severity))
    affected_count = len(issue.affected_sample_ids) if _is_set(issue.affected_sample_ids) else 0
    return (_linter_severity_rank(severity), -affected_count, issue.message)


def _format_linter_counts(counts: dict[str, int]) -> Text:
    if not counts:
        return Text("0", style="dim")
    text = Text()
    for index, (name, count) in enumerate(sorted(counts.items(), key=_linter_severity_order)):
        if index:
            text.append(", ")
        text.append(f"{name}: {count}", style=_linter_severity_style(name))
    return text


def _format_linter_value(value: Any, max_length: int = 120) -> str:
    if not _is_set(value):
        return "-"
    if hasattr(value, "to_dict"):
        value = value.to_dict()
    if isinstance(value, (dict, list)):
        formatted = json.dumps(value, default=str, sort_keys=True)
    else:
        formatted = str(value)
    return formatted if len(formatted) <= max_length else formatted[: max_length - 3] + "..."


def _build_cost_lines(job: TrainingJob | EvalJob) -> list[RenderableType]:
    """Build cost info lines from job.usage. Returns empty list if no data."""
    lines: list[RenderableType] = []

    if _is_set(job.cost_dollars) and job.cost_dollars is not None:
        lines.append(_safe_markup(f"  [bold]Cost:[/bold]  ${job.cost_dollars:.2f}"))
    return lines

def _build_transform_cost_lines(job: TransformJob) -> list[RenderableType]:
    if not _is_set(job.usage):
        return []
    usage = job.usage
    lines: list[RenderableType] = []

    # Total cost
    if _is_set(usage.current_cost_dollars):
        lines.append(_safe_markup(f"  [bold]Total cost:[/bold] [bright_green]${usage.current_cost_dollars:.2f}[/bright_green]"))
    if _is_set(usage.max_cost_dollars):
        lines.append(_safe_markup(f"  [bold]Budget:[/bold]     ${usage.max_cost_dollars:.2f}"))
    if _is_set(usage.estimated_cost_dollars):
        lines.append(_safe_markup(f"  [bold]Estimated:[/bold]  ${usage.estimated_cost_dollars:.2f}"))

    return lines


def build_live_display(
    metrics: Optional[PipelineMetricsResponse] = None,
    job: Optional[TransformJob] = None,
) -> RenderableType:
    """Build the live display renderable for the polling loop."""
    renderables: list[RenderableType] = []

    status_label = {
        TransformJobStatus.RUNNING: ("[bold bright_blue]>> Pipeline Running[/bold bright_blue]", "bright_blue"),
        TransformJobStatus.COMPLETED: ("[bold bright_green]>> Pipeline Completed[/bold bright_green]", "bright_green"),
        TransformJobStatus.FAILED: ("[bold bright_red]>> Pipeline Failed[/bold bright_red]", "bright_red"),
        TransformJobStatus.CANCELLED: ("[bold yellow]>> Pipeline Cancelled[/bold yellow]", "yellow"),
    }
    status = job.status if job is not None else TransformJobStatus.RUNNING
    label, border = status_label.get(status, ("[bold bright_blue]>> Pipeline[/bold bright_blue]", "bright_blue"))
    renderables.append(_safe_markup(label))
    renderables.append(Text(""))

    if job is not None:
        renderables.append(_safe_markup(f"  [bold]Job ID:[/bold]           {job.id}"))
        if job.input_dataset_id is not None:
            renderables.append(_safe_markup(f"  [bold]Input dataset:[/bold]    {job.input_dataset_id}"))
        renderables.append(Text(""))

    # Cost summary from job.usage
    if job is not None:
        cost_lines = _build_transform_cost_lines(job)
        if cost_lines:
            renderables.extend(cost_lines)
            renderables.append(Text(""))

    if metrics is None:
        renderables.append(Text("Waiting for metrics...", style="dim italic"))
        return Panel(
            Group(*renderables),
            border_style=border,
            padding=(1, 2),
        )

    pipeline_summary_by_index: dict[int, Any] = {}
    has_rejection_reasons = False
    if job is not None and not isinstance(job.usage, Unset) and job.usage is not None:
        summary = job.usage.pipeline_summary
        if not isinstance(summary, Unset) and summary is not None:
            for ps in summary:
                pipeline_summary_by_index[ps.step_index] = ps
                if not isinstance(ps.rejection_reasons, Unset) and ps.rejection_reasons is not None and ps.rejection_reasons.additional_properties:
                    has_rejection_reasons = True

    table = Table(show_header=True, header_style="bold cyan", expand=True)
    table.add_column("Step", style="bold")
    table.add_column("Progress", width=20)
    table.add_column("In", justify="right")
    table.add_column("Out", justify="right")
    table.add_column("Rejected", justify="right")
    table.add_column("Errors", justify="right")
    if has_rejection_reasons:
        table.add_column("Rejection Reasons")
    table.add_column("Duration", justify="right")

    for step in sorted(metrics.steps, key=lambda s: s.step_index):
        if step.progress >= 1.0:
            step_status = Text("Complete", style="bold bright_green")
        elif step.progress > 0:
            step_status = Text("In progress", style="bold bright_yellow")
        else:
            step_status = Text("Pending", style="dim")

        rejected_style = "bright_red" if step.rejected_count > 0 else "dim"
        error_style = "bold bright_red" if step.error_count > 0 else "dim"

        row_cells: list[Any] = [
            step.transform_name,
            step_status,
            str(step.input_rows),
            str(step.output_rows),
            Text(str(step.rejected_count), style=rejected_style),
            Text(str(step.error_count), style=error_style),
        ]
        if has_rejection_reasons:
            ps = pipeline_summary_by_index.get(step.step_index)
            if ps and not isinstance(ps.rejection_reasons, Unset) and ps.rejection_reasons is not None and ps.rejection_reasons.additional_properties:
                sorted_reasons = sorted(ps.rejection_reasons.additional_properties.items(), key=lambda x: -x[1])
                parts = [f"{k[:40]}{'...' if len(k) > 40 else ''} ({v})" for k, v in sorted_reasons[:2]]
                if len(sorted_reasons) > 2:
                    parts.append(f"+{len(sorted_reasons) - 2} more")
                row_cells.append(Text("\n".join(parts), style="dim"))
            else:
                row_cells.append(Text("-", style="dim"))
        row_cells.append(_format_duration(step.duration_seconds))
        table.add_row(*row_cells)

    renderables.append(table)

    if job is not None and job.output_dataset_id:
        url = f"https://dashboard.lightningrod.ai/?redirect=/datasets/{job.output_dataset_id}"
        renderables.append(Text(""))
        renderables.append(_safe_markup(f"  [dim]View full details: [link={url}]{url}[/link][/dim]"))

    return Panel(
        Group(*renderables),
        border_style=border,
        padding=(1, 2),
    )


def _make_progress_bar(pct: float, width: int = 24) -> str:
    filled = int(width * (pct / 100))
    return "█" * filled + "░" * (width - filled)


def _training_metric_history_covers_reward(job: TrainingJob) -> bool:
    if not _is_set(job.metric_history) or not job.metric_history:
        return False
    for series in job.metric_history:
        if series.name.lower() == "reward" and series.values:
            return True
    return False


_SPARKLINE_BLOCKS = "▁▂▃▄▅▆▇█"


def _finite_floats(values: list[float]) -> list[float]:
    out: list[float] = []
    for v in values:
        if isinstance(v, (int, float)) and math.isfinite(float(v)):
            out.append(float(v))
    return out


def _subsample_for_sparkline(values: list[float], max_width: int) -> list[float]:
    n = len(values)
    if n <= max_width:
        return list(values)
    return [values[int(i * (n - 1) / (max_width - 1))] for i in range(max_width)]


def _metric_sparkline(values: list[float], max_width: int = 32) -> str:
    finite = _finite_floats(values)
    if not finite:
        return ""
    sampled = _subsample_for_sparkline(finite, max_width)
    if len(sampled) == 1:
        return _SPARKLINE_BLOCKS[3]
    vmin, vmax = min(sampled), max(sampled)
    if vmin == vmax:
        return _SPARKLINE_BLOCKS[3] * len(sampled)
    parts: list[str] = []
    for v in sampled:
        t = (v - vmin) / (vmax - vmin)
        idx = min(7, max(0, int(t * 7 + 0.5)))
        parts.append(_SPARKLINE_BLOCKS[idx])
    return "".join(parts)


def _format_training_metric_line(
    name: str, values: list[float], hint: str | None = None, sparkline_width: int = 32
) -> RenderableType:
    latest = values[-1]
    count = len(values)
    avg = sum(values) / count
    safe_name = escape(name)
    hint_part = f"  [dim]{escape(hint)}[/dim]" if hint else ""
    header = _safe_markup(
        f"  [bold]{safe_name}:[/bold] latest {latest:.4f}  avg {avg:.4f}  ({count} steps){hint_part}"
    )
    spark = _metric_sparkline(values, max_width=sparkline_width)
    if not spark:
        return header
    return Group(
        header,
        Text(f"      {spark}", style="dim cyan"),
    )


def build_training_live_display(job: TrainingJob) -> RenderableType:
    renderables: list[RenderableType] = []
    status = str(job.status) if job is not None else ""
    header_style = {
        "COMPLETED": "bright_green",
        "FAILED": "bright_red",
        "RUNNING": "bright_blue",
        "STARTING": "bright_blue",
    }.get(status, "bright_blue") if status else "bright_blue"
    header = f">> Training {status}" if status else ">> Training"
    renderables.append(_safe_markup(f"[bold {header_style}]{header}[/bold {header_style}]"))
    renderables.append(Text(""))
    if job is not None:
        if _is_set(job.name) and job.name:
            renderables.append(_safe_markup(f"  [bold]Job ID:[/bold] {job.id}"))
            renderables.append(Text(""))
        if _is_set(job.model_id) and job.model_id:
            renderables.append(_safe_markup(f"  [bold]Model:[/bold] {job.model_id}"))
            renderables.append(Text(""))

        if job.status == TrainingJobStatus.RUNNING:
            current = job.current_step or 0
            total = job.total_steps or None
            if total is not None:
                pct = min(100, int(100 * current / total))
            else:
                pct = 0
            step_progress = f"{current}/{total} ({pct}%)" if total is not None else "(0%)"
            bar = _make_progress_bar(pct)
            renderables.append(_safe_markup(f"  [bold]Progress:[/bold] [{bar}] {step_progress}"))
            renderables.append(Text(""))

        if _is_set(job.metric_history) and job.metric_history:
            for series in job.metric_history:
                if not series.values:
                    continue

                hint = None
                if series.name.lower() == "loss":
                    hint = "(lower is better)"
                elif series.name.lower() == "reward":
                    hint = "(higher is better)"
                renderables.append(_format_training_metric_line(series.name, series.values, hint))
            if any(s.values for s in job.metric_history):
                renderables.append(Text(""))

        if (
            _is_set(job.reward_history)
            and job.reward_history
            and not _training_metric_history_covers_reward(job)
        ):
            renderables.append(
                _format_training_metric_line(
                    "Reward", job.reward_history, "(higher is better)"
                )
            )
            renderables.append(Text(""))

        if job.status == TrainingJobStatus.FAILED:
            renderables.append(_safe_markup(f"  [bold]Error:[/bold] {job.error_message}"))
            renderables.append(Text(""))
        if job.status == TrainingJobStatus.COMPLETED:
            cost_lines = _build_cost_lines(job)
            if cost_lines:
                renderables.extend(cost_lines)
                renderables.append(Text(""))

    return Panel(
        Group(*renderables),
        border_style="bright_blue",
        padding=(1, 2),
    )


def run_training_live_display(
    poll_callback: Callable[[], TrainingJob],
    poll_interval: float = 15,
    initial_job: Any = None,
) -> None:
    import time
    console = Console()
    if _is_notebook():
        from IPython.display import clear_output
        console.print(build_training_live_display(initial_job))
        job = poll_callback()
        while job.status in (TrainingJobStatus.RUNNING, TrainingJobStatus.STARTING):
            clear_output(wait=True)
            console.print(build_training_live_display(job))
            time.sleep(poll_interval)
            job = poll_callback()
        clear_output(wait=True)
        console.print(build_training_live_display(job))
    else:
        from rich.live import Live
        with Live(
            build_training_live_display(initial_job),
            console=console,
            refresh_per_second=1,
            transient=True,
        ) as live:
            job = poll_callback()
            while job.status in (TrainingJobStatus.RUNNING, TrainingJobStatus.STARTING):
                live.update(build_training_live_display(job))
                time.sleep(poll_interval)
                job = poll_callback()
            live.update(build_training_live_display(job))


def build_eval_live_display(job: EvalJob) -> RenderableType:
    renderables: list[RenderableType] = []
    status = str(job.status) if job is not None else ""
    header_style = {
        "COMPLETED": "bright_green",
        "FAILED": "bright_red",
        "RUNNING": "bright_blue",
        "STARTING": "bright_blue",
    }.get(status, "bright_blue") if status else "bright_blue"
    header = f">> Eval {status}" if status else ">> Eval"
    renderables.append(_safe_markup(f"[bold {header_style}]{header}[/bold {header_style}]"))
    renderables.append(Text(""))
    if job is not None:
        renderables.append(_safe_markup(f"  [bold]Job ID:[/bold] {job.id}"))
        renderables.append(_safe_markup(f"  [bold]Dataset:[/bold] {job.config.dataset.id}"))
        renderables.append(Text(""))
        if job.status in (EvalJobStatus.RUNNING, EvalJobStatus.STARTING):
            current = job.current_step or 0
            total = job.total_steps or None
            if total is not None:
                pct = min(100, int(100 * current / total))
            else:
                pct = 0
            step_progress = f"{current}/{total} ({pct}%)" if total is not None else "(0%)"
            bar = _make_progress_bar(pct)
            renderables.append(_safe_markup(f"  [bold]Progress:[/bold] [{bar}] {step_progress}"))
            renderables.append(Text(""))
        if _is_set(job.metrics) and job.metrics and job.metrics.additional_properties:
            for k, v in job.metrics.additional_properties.items():
                renderables.append(_safe_markup(f"  [bold]{k}:[/bold] {v}"))
            renderables.append(Text(""))
        if job.status == EvalJobStatus.FAILED and _is_set(job.error_message):
            renderables.append(_safe_markup(f"  [bold]Error:[/bold] {job.error_message}"))
            renderables.append(Text(""))
    return Panel(
        Group(*renderables),
        border_style="bright_blue",
        padding=(1, 2),
    )


def print_eval(job: EvalJob) -> None:
    """Print a prettified eval job summary. Use with evals.run(), run_from_training_job(), or evals.get()."""
    console = Console()
    renderables: list[RenderableType] = []
    status = str(job.status) if job is not None else ""
    header_style = {
        "COMPLETED": "bright_green",
        "FAILED": "bright_red",
        "RUNNING": "bright_blue",
        "STARTING": "bright_blue",
    }.get(status, "bright_blue") if status else "bright_blue"
    header = f">> Eval {status}" if status else ">> Eval"
    renderables.append(_safe_markup(f"[bold {header_style}]{header}[/bold {header_style}]"))
    renderables.append(Text(""))
    if job is not None:
        renderables.append(_safe_markup(f"  [bold]Job ID:[/bold] {job.id}"))
        renderables.append(_safe_markup(f"  [bold]Dataset:[/bold] {job.config.dataset.id}"))
        renderables.append(Text(""))
        if _is_set(job.metrics) and job.metrics and job.metrics.additional_properties:
            props = job.metrics.additional_properties
            if all(isinstance(v, dict) for v in props.values()):
                # Compute all unique metric keys
                metric_keys = set()
                for data in props.values():
                    metric_keys.update(data.keys())
                metric_keys = sorted(metric_keys)
                table = Table(show_header=True, header_style="bold cyan")
                table.add_column("Metric", style="dim")
                for name in props:
                    table.add_column(name, justify="right")
                for key in metric_keys:
                    row = [key]
                    for name, data in props.items():
                        val = data.get(key)
                        if val is None:
                            row.append("—")
                        elif isinstance(val, float):
                            row.append(f"{val:.4f}")
                        else:
                            row.append(str(val))
                    table.add_row(*row)
                renderables.append(table)
            else:
                for k, v in props.items():
                    renderables.append(_safe_markup(f"  [bold]{k}:[/bold] {v}"))
            renderables.append(Text(""))
        if job.status == EvalJobStatus.FAILED and _is_set(job.error_message):
            renderables.append(_safe_markup(f"  [bold]Error:[/bold] {job.error_message}"))
            renderables.append(Text(""))
        cost_lines = _build_cost_lines(job)
        if cost_lines:
            renderables.extend(cost_lines)
            renderables.append(Text(""))
    console.print(Panel(Group(*renderables), border_style="bright_blue", padding=(1, 2)))


def run_eval_live_display(
    poll_callback: Callable[[], Any],
    poll_interval: float = 15,
    initial_job: Any = None,
) -> None:
    import time
    console = Console()
    if _is_notebook():
        from IPython.display import clear_output
        console.print(build_eval_live_display(initial_job))
        job = poll_callback()
        while job.status in (EvalJobStatus.RUNNING, EvalJobStatus.STARTING):
            clear_output(wait=True)
            console.print(build_eval_live_display(job))
            time.sleep(poll_interval)
            job = poll_callback()
        clear_output(wait=True)
        print_eval(job)
    else:
        from rich.live import Live
        with Live(
            build_eval_live_display(initial_job),
            console=console,
            refresh_per_second=1,
            transient=True,
        ) as live:
            job = poll_callback()
            while job.status in (EvalJobStatus.RUNNING, EvalJobStatus.STARTING):
                live.update(build_eval_live_display(job))
                time.sleep(poll_interval)
                job = poll_callback()
            live.stop()
            print_eval(job)


def _is_notebook() -> bool:
    """Check if we're running inside a Jupyter or Colab notebook."""
    try:
        from IPython import get_ipython
        shell = get_ipython()
        if shell is None:
            return False  # Not running in IPython at all
        # Jupyter notebook or qtconsole
        if "IPKernelApp" in shell.config:
            return True
        else:
            return False
    except Exception:
        return False

def _is_colab_notebook() -> bool:
    """Check if we're running inside a Jupyter or Colab notebook."""
    try:
        import google.colab.userdata
    except ImportError as e:
        return False
    else:
        return True


def run_live_display(
    poll_callback: Callable[[], tuple[PipelineMetricsResponse, TransformJob]],
    poll_interval: float = 15,
    warning_message: Optional[str] = None,
) -> None:
    """Run a live-updating display that polls for metrics.

    Args:
        poll_callback: Returns ``(metrics, job)`` on each call; ``metrics`` may be None until available.
        poll_interval: Seconds between polls.
        warning_message: Optional warning to persist above the live display.
    """
    import time
    console = Console()

    if _is_notebook():
        from IPython.display import clear_output
        metrics, job = poll_callback()
        while job.status == TransformJobStatus.RUNNING:
            clear_output(wait=True)
            if warning_message:
                display_warning(warning_message)
            console.print(build_live_display(metrics=metrics, job=job))
            time.sleep(poll_interval)
            metrics, job = poll_callback()
        clear_output(wait=True)
        if warning_message:
            display_warning(warning_message)
        console.print(build_live_display(metrics=metrics, job=job))
    else:
        from rich.live import Live
        metrics, job = poll_callback()
        with Live(
            build_live_display(metrics=metrics, job=job),
            console=console,
            refresh_per_second=1,
            transient=False,
        ) as live:
            while job.status == TransformJobStatus.RUNNING:
                live.update(build_live_display(metrics=metrics, job=job))
                time.sleep(poll_interval)
                metrics, job = poll_callback()
            live.update(build_live_display(metrics=metrics, job=job))


def _build_invalid_samples_error_message(
    original_message: str,
    error_details: Optional[list[str]] = None,
) -> Group:
    """Build enhanced error message for invalid samples error using Rich formatting."""
    renderables: list[RenderableType] = []

    renderables.append(_safe_markup(f"[bold]{original_message}[/bold]"))
    renderables.append(Text(""))

    if error_details:
        renderables.append(_safe_markup("[bold]Error details:[/bold]"))
        for detail in error_details[:5]:
            truncated = detail[:500] + "..." if len(detail) > 500 else detail
            renderables.append(Text(f"  • {truncated}", style="dim"))
        if len(error_details) > 5:
            renderables.append(Text(f"  • ... and {len(error_details) - 5} more", style="dim italic"))
        renderables.append(Text(""))

    renderables.append(_safe_markup("[bold]This typically happens when:[/bold]"))
    renderables.append(_safe_markup("  • Filter criteria is too strict"))
    renderables.append(_safe_markup("  • Labeling failed (e.g., questions couldn't be answered or had low confidence)"))
    renderables.append(_safe_markup("  • Seed generation found no suitable content"))
    renderables.append(Text(""))

    renderables.append(_safe_markup("[bold]Next steps:[/bold]"))
    renderables.append(_safe_markup("  • Check the dataset samples to see specific failure reasons in the 'meta.filter_reason' field"))
    renderables.append(_safe_markup("  • Adjust and retry the transform pipeline (e.g., try a wider date range)"))
    renderables.append(_safe_markup("  • If the problem persists, contact support or open a GitHub issue: [link=https://github.com/lightning-rod-labs/lightningrod-python-sdk/issues]https://github.com/lightning-rod-labs/lightningrod-python-sdk/issues[/link]"))

    return Group(*renderables)


def display_error(
    message: str,
    title: str = "Error",
    job: Any = None,
    response_body: str | None = None,
    error_details: Optional[list[str]] = None,
) -> None:
    console = Console()
    renderables: list[RenderableType] = []

    renderables.append(_safe_markup(f"[bold bright_red]>> {title}[/bold bright_red]"))
    renderables.append(Text(""))

    if "Job completed with 0 valid rows" in message:
        renderables.append(_build_invalid_samples_error_message(message, error_details=error_details))
    elif error_details:
        renderables.append(_safe_markup(f"[bold]{message}[/bold]"))
        renderables.append(Text(""))
        renderables.append(_safe_markup("[bold]Error details:[/bold]"))
        for detail in error_details[:5]:
            truncated = detail[:500] + "..." if len(detail) > 500 else detail
            renderables.append(Text(f"  • {truncated}", style="dim"))
        if len(error_details) > 5:
            renderables.append(Text(f"  • ... and {len(error_details) - 5} more", style="dim italic"))
    else:
        renderables.append(_safe_markup(f"[bold]{message}[/bold]"))

    if response_body is not None and response_body.strip():
        renderables.append(Text(""))
        renderables.append(_safe_markup("[bold]Response body:[/bold]"))
        renderables.append(Text(response_body.strip()[:2000], style="dim"))

    if job is not None:
        cost_lines = _build_transform_cost_lines(job) if isinstance(job, TransformJob) else _build_cost_lines(job)
        if cost_lines:
            renderables.append(Text(""))
            renderables.extend(cost_lines)

    console.print(Panel(Group(*renderables), border_style="bright_red", padding=(1, 2)))


def display_prepare_report(report: Any, verbose: bool = True) -> None:
    """Render a PrepareReport as a Rich panel. Used inside Jupyter notebooks."""
    from lightningrod.training.samples import PrepareReport
    assert isinstance(report, PrepareReport)
    stats = report.stats
    console = Console()
    renderables: list[RenderableType] = []

    border = "bright_green" if report.is_healthy else "yellow"
    header_style = "bold bright_green" if report.is_healthy else "bold yellow"
    renderables.append(_safe_markup(f"[{header_style}]>> prepare_for_training[/{header_style}]"))
    renderables.append(Text(""))

    if verbose or not report.is_healthy:
        renderables.append(_safe_markup(f"  [dim]Starting with {stats.total} samples[/dim]"))
        renderables.append(Text(""))

        parts = []
        if stats.filter_invalid:
            parts.append(f"{stats.filter_invalid} invalid")
        if stats.filter_horizon:
            part = f"{stats.filter_horizon} horizon"
            if stats.filter_missing_resolution_date or stats.filter_missing_prediction_date:
                sub = []
                if stats.filter_missing_resolution_date:
                    sub.append(f"{stats.filter_missing_resolution_date} missing resolution date")
                if stats.filter_missing_prediction_date:
                    sub.append(f"{stats.filter_missing_prediction_date} missing prediction date")
                part += f" ({', '.join(sub)})"
            parts.append(part)
        if stats.filter_context:
            parts.append(f"{stats.filter_context} missing context")
        if stats.filter_missing_or_invalid_label:
            parts.append(f"{stats.filter_missing_or_invalid_label} missing/bad label")
        filter_line = (
            f"  [bold]Filter:[/bold]  Dropped {', '.join(parts)} → {stats.filter_kept} remain"
            if parts else
            f"  [bold]Filter:[/bold]  {stats.filter_kept} remain (0 dropped)"
        )
        renderables.append(_safe_markup(filter_line))

        if stats.dedup_removed > 0:
            renderables.append(_safe_markup(
                f"  [bold]Dedup:[/bold]   Removed {stats.dedup_removed} duplicates "
                f"({stats.dedup_kept + stats.dedup_removed} → {stats.dedup_kept})"
            ))
            for k, c in stats.dedup_top_collisions:
                q = repr(k[0])[:60] + ("..." if len(repr(k[0])) > 60 else "")
                renderables.append(Text(f"    ({q}, {k[1]}): {c} samples → 1", style="dim"))
        else:
            renderables.append(_safe_markup(f"  [bold]Dedup:[/bold]   {stats.dedup_kept} remain (0 duplicates)"))

        split_detail = f"Splits: {stats.split_train_after} train | {stats.split_test_after} test ({stats.split_no_sort_key} dropped, no prediction_date)"
        renderables.append(_safe_markup(f"  [bold]Split:[/bold]   {split_detail}"))
        n_leaked = stats.split_train_before - stats.split_train_after
        if n_leaked:
            renderables.append(_safe_markup(
                f"           [yellow]{n_leaked} train samples removed for leakage[/yellow]"
            ))

    if not report.is_healthy:
        renderables.append(Text(""))
        renderables.append(_safe_markup("[bold yellow]⚠ Unhealthy dataset[/bold yellow]"))
        for issue in report.issues:
            renderables.append(Text(""))
            renderables.append(Text(issue.message, style="bold"))
            if issue.tips:
                renderables.append(Text(""))
                renderables.append(_safe_markup("  [dim]Tips:[/dim]"))
                for tip in issue.tips:
                    renderables.append(Text(f"    • {tip}"))

    console.print(Panel(Group(*renderables), border_style=border, padding=(1, 2)))


def build_dataset_linter_run_overview(run: Any) -> RenderableType:
    status = str(run.status)
    total_issues = 0
    severity_counts: dict[str, int] = {}
    rule_counts: dict[str, int] = {}

    if _is_set(run.summary):
        total_issues = run.summary.total_issues
        severity_counts = _linter_count_map(run.summary.by_severity)
        rule_counts = _linter_count_map(run.summary.by_rule)
    elif _is_set(run.rules):
        for rule in run.rules:
            count = _linter_rule_issue_count(rule)
            total_issues += count
            rule_counts[rule.name] = count
            for severity, severity_count in _linter_rule_severity_counts(rule).items():
                severity_counts[severity] = severity_counts.get(severity, 0) + severity_count

    border = "bright_green" if status.upper() == "COMPLETED" and total_issues == 0 else "yellow"
    if status.upper() == "FAILED" or _is_set(run.error_message):
        border = "bright_red"

    renderables: list[RenderableType] = [
        _safe_markup(f"[{_linter_status_style(status)}]>> Dataset Linter: {escape(status)}[/{_linter_status_style(status)}]"),
        Text(""),
        _safe_markup(f"  [bold]Run ID:[/bold]      {escape(run.id)}"),
        _safe_markup(f"  [bold]Dataset:[/bold]     {escape(run.dataset_id)}"),
        _safe_markup(f"  [bold]Created:[/bold]     {_format_linter_datetime(run.created_at)}"),
        _safe_markup(f"  [bold]Updated:[/bold]     {_format_linter_datetime(run.updated_at)}"),
        _safe_markup(f"  [bold]Sample size:[/bold] {run.sample_size if run.sample_size is not None else 'default'}"),
        Text(""),
        _safe_markup(f"  [bold]Issues:[/bold]      {total_issues}"),
    ]

    if severity_counts:
        renderables.append(Text("  Severity:    ") + _format_linter_counts(severity_counts))

    if _is_set(run.error_message):
        renderables.append(Text(""))
        renderables.append(Text(str(run.error_message), style="bold bright_red"))

    if rule_counts or _is_set(run.rules):
        table = Table(show_header=True, header_style="bold cyan", expand=True)
        table.add_column("Rule", style="bold")
        table.add_column("Issues", justify="right")
        table.add_column("Severity")
        table.add_column("Duration", justify="right")

        rules_by_name = {rule.name: rule for rule in run.rules} if _is_set(run.rules) else {}
        names = list(rule_counts.keys()) or list(rules_by_name.keys())
        for name in sorted(names, key=lambda item: (-rule_counts.get(item, 0), item)):
            rule = rules_by_name.get(name)
            count = rule_counts.get(name, _linter_rule_issue_count(rule) if rule is not None else 0)
            counts = _linter_rule_severity_counts(rule) if rule is not None else {}
            table.add_row(
                name,
                Text(str(count), style="bold bright_red" if count else "dim"),
                _format_linter_counts(counts),
                _format_linter_duration(rule.duration_ms) if rule is not None else "-",
            )
        renderables.append(Text(""))
        renderables.append(table)

    return Panel(Group(*renderables), border_style=border, padding=(1, 2))


def build_dataset_linter_run_details(run: Any, max_sample_ids: int = 10) -> RenderableType:
    renderables: list[RenderableType] = [
        _safe_markup(f"[{_linter_status_style(str(run.status))}]>> Dataset Linter Details[/{_linter_status_style(str(run.status))}]"),
        Text(""),
        _safe_markup(f"  [bold]Run ID:[/bold]  {escape(run.id)}"),
        _safe_markup(f"  [bold]Dataset:[/bold] {escape(run.dataset_id)}"),
    ]

    if not _is_set(run.rules):
        renderables.append(Text(""))
        renderables.append(Text("No per-rule results were returned for this run.", style="dim italic"))
        return Panel(Group(*renderables), border_style="yellow", padding=(1, 2))

    for rule in sorted(run.rules, key=_linter_rule_sort_key):
        issue_count = _linter_rule_issue_count(rule)
        renderables.append(Text(""))
        renderables.append(_safe_markup(
            f"[bold cyan]{escape(rule.name)}[/bold cyan] "
            f"[dim]({_format_linter_duration(rule.duration_ms)}, {issue_count} issue{'s' if issue_count != 1 else ''})[/dim]"
        ))

        if _is_set(rule.stats) and rule.stats.additional_properties:
            stats_table = Table(show_header=False, expand=True, box=None, padding=(0, 1))
            stats_table.add_column("Metric", style="dim")
            stats_table.add_column("Value")
            for key, value in sorted(rule.stats.additional_properties.items()):
                stats_table.add_row(str(key), _format_linter_value(value))
            renderables.append(stats_table)

        if not _is_set(rule.issues) or not rule.issues:
            renderables.append(Text("  No issues.", style="dim"))
            continue

        for index, issue in enumerate(sorted(rule.issues, key=_linter_issue_sort_key), start=1):
            severity = str(getattr(issue.severity, "value", issue.severity))
            affected_count = len(issue.affected_sample_ids) if _is_set(issue.affected_sample_ids) else 0
            if affected_count:
                sample_ids = issue.affected_sample_ids[:max_sample_ids]
                affected = "\n".join(sample_ids)
                if affected_count > max_sample_ids:
                    affected += f"\n+{affected_count - max_sample_ids} more"
            else:
                affected = "-"

            renderables.append(Text(""))
            header = Text(f"  Issue {index}: ", style="bold")
            header.append(severity, style=_linter_severity_style(severity))
            renderables.append(header)
            renderables.append(Text(f"    Message: {issue.message}", overflow="fold", no_wrap=False))
            renderables.append(Text(f"    Affected samples: {affected}"))
            if _is_set(issue.meta):
                renderables.append(Text(f"    Meta: {_format_linter_value(issue.meta, max_length=500)}"))
            if _is_set(issue.tip):
                renderables.append(Text(f"    Tip: {issue.tip}"))

    return Panel(Group(*renderables), border_style="cyan", padding=(1, 2))


def display_lint_overview(run: Any) -> None:
    Console().print(build_dataset_linter_run_overview(run))


def display_lint_detailed(run: Any, max_sample_ids: int = 10) -> None:
    Console().print(build_dataset_linter_run_details(run, max_sample_ids=max_sample_ids))


def run_dataset_linter_live_display(
    poll_callback: Callable[[], Any],
    poll_interval: float = 15,
    initial_run: Any = None,
) -> None:
    import time

    console = Console()
    active_statuses = {"PENDING", "QUEUED", "STARTING", "RUNNING", "IN_PROGRESS"}

    if _is_notebook():
        from IPython.display import clear_output
        if initial_run is not None:
            console.print(build_dataset_linter_run_overview(initial_run))
        run = poll_callback()
        while str(run.status).upper() in active_statuses:
            clear_output(wait=True)
            console.print(build_dataset_linter_run_overview(run))
            time.sleep(poll_interval)
            run = poll_callback()
        clear_output(wait=True)
        console.print(build_dataset_linter_run_overview(run))
    else:
        from rich.live import Live
        with Live(
            build_dataset_linter_run_overview(initial_run),
            console=console,
            refresh_per_second=1,
            transient=True,
        ) as live:
            run = poll_callback()
            while str(run.status).upper() in active_statuses:
                live.update(build_dataset_linter_run_overview(run))
                time.sleep(poll_interval)
                run = poll_callback()
            live.update(build_dataset_linter_run_overview(run))


def display_warning(message: str, title: str = "Warning", job: Any = None) -> None:
    console = Console()
    renderables: list[RenderableType] = []

    renderables.append(_safe_markup(f"[bold yellow]>> {title}[/bold yellow]"))
    renderables.append(Text(""))
    renderables.append(_safe_markup(message))

    if job is not None:
        cost_lines = _build_transform_cost_lines(job) if isinstance(job, TransformJob) else _build_cost_lines(job)
        if cost_lines:
            renderables.append(Text(""))
            renderables.extend(cost_lines)

    console.print(Panel(Group(*renderables), border_style="yellow", padding=(1, 2)))
