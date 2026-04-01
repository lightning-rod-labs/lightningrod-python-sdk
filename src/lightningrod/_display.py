from __future__ import annotations

from typing import Any, Callable, Optional

from rich.console import Console, Group, RenderableType
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
                reasons_str = ", ".join(f"{k} ({v})" for k, v in sorted(ps.rejection_reasons.additional_properties.items(), key=lambda x: -x[1]))
                row_cells.append(Text(reasons_str, style="dim"))
            else:
                row_cells.append(Text("-", style="dim"))
        row_cells.append(_format_duration(step.duration_seconds))
        table.add_row(*row_cells)

    renderables.append(table)

    return Panel(
        Group(*renderables),
        border_style=border,
        padding=(1, 2),
    )


def _make_progress_bar(pct: float, width: int = 24) -> str:
    filled = int(width * (pct / 100))
    return "█" * filled + "░" * (width - filled)


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
            renderables.append(_safe_markup(f"  [bold]Job:[/bold] {job.name}"))
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

        if _is_set(job.reward_history) and job.reward_history:
            latest = job.reward_history[-1]
            count = len(job.reward_history)
            avg = sum(job.reward_history) / count
            reward_line = f"  [bold]Reward:[/bold] latest {latest:.4f}  avg {avg:.4f}  ({count} steps)  [dim](higher is better)[/dim]"
            renderables.append(_safe_markup(reward_line))
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
        renderables.append(_safe_markup(f"  [bold]Model:[/bold] {job.config.model_id}"))
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
    """Print a prettified eval job summary. Use with evals.run() or evals.get()."""
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
        renderables.append(_safe_markup(f"  [bold]ID:[/bold] {job.id}"))
        renderables.append(_safe_markup(f"  [bold]Model:[/bold] {job.config.model_id}"))
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


def _build_invalid_samples_error_message(original_message: str) -> Group:
    """Build enhanced error message for invalid samples error using Rich formatting."""
    renderables: list[RenderableType] = []
    
    renderables.append(_safe_markup(f"[bold]{original_message}[/bold]"))
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


def display_error(message: str, title: str = "Error", job: Any = None, response_body: str | None = None) -> None:
    console = Console()
    renderables: list[RenderableType] = []

    renderables.append(_safe_markup(f"[bold bright_red]>> {title}[/bold bright_red]"))
    renderables.append(Text(""))

    if "Job completed with 0 valid rows" in message:
        renderables.append(_build_invalid_samples_error_message(message))
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
