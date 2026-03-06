from __future__ import annotations

from typing import Any, Callable, Optional

from rich.console import Console, Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from lightningrod._generated.models import EvalJob
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


def _build_cost_lines(job: Any) -> list[RenderableType]:
    """Build cost info lines from job.usage. Returns empty list if no data."""
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
    metrics: Any = None,
    job: Any = None,
) -> RenderableType:
    """Build the live display renderable for the polling loop."""
    renderables: list[RenderableType] = []

    renderables.append(_safe_markup("[bold bright_blue]>> Pipeline Running[/bold bright_blue]"))
    renderables.append(Text(""))

    # Cost summary from job.usage
    if job is not None:
        cost_lines = _build_cost_lines(job)
        if cost_lines:
            renderables.extend(cost_lines)
            renderables.append(Text(""))

    if metrics is None:
        renderables.append(Text("Waiting for metrics...", style="dim italic"))
        return Panel(
            Group(*renderables),
            border_style="bright_blue",
            padding=(1, 2),
        )

    # Per-step table
    table = Table(show_header=True, header_style="bold cyan", expand=True)
    table.add_column("Step", style="bold", no_wrap=True)
    table.add_column("Progress", width=20)
    table.add_column("In", justify="right")
    table.add_column("Out", justify="right")
    table.add_column("Rejected", justify="right")
    table.add_column("Errors", justify="right")
    table.add_column("Duration", justify="right")

    for step in sorted(metrics.steps, key=lambda s: s.step_index):
        if step.progress >= 1.0:
            status = Text("Complete", style="bold bright_green")
        elif step.progress > 0:
            status = Text("In progress", style="bold bright_yellow")
        else:
            status = Text("Pending", style="dim")

        rejected_style = "bright_red" if step.rejected_count > 0 else "dim"
        error_style = "bold bright_red" if step.error_count > 0 else "dim"

        table.add_row(
            step.transform_name,
            status,
            str(step.input_rows),
            str(step.output_rows),
            Text(str(step.rejected_count), style=rejected_style),
            Text(str(step.error_count), style=error_style),
            _format_duration(step.duration_seconds),
        )

    renderables.append(table)

    return Panel(
        Group(*renderables),
        border_style="bright_blue",
        padding=(1, 2),
    )


def _make_progress_bar(pct: float, width: int = 24) -> str:
    filled = int(width * (pct / 100))
    return "█" * filled + "░" * (width - filled)


def build_training_live_display(job: Any) -> RenderableType:
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
        renderables.append(_safe_markup(f"  [bold]Model:[/bold] {job.model_id}"))
        renderables.append(_safe_markup(f"  [bold]Dataset:[/bold] {job.dataset_hf_repo}"))
        renderables.append(Text(""))
        if _is_set(job.metrics) and job.metrics and job.metrics.additional_properties:
            for k, v in job.metrics.additional_properties.items():
                renderables.append(_safe_markup(f"  [bold]{k}:[/bold] {v}"))
            renderables.append(Text(""))
        if job.status == TrainingJobStatus.FAILED and _is_set(job.error_message):
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
        renderables.append(_safe_markup(f"  [bold]Model:[/bold] {job.model_id}"))
        dataset = None
        if _is_set(job.dataset_hf_repo):
            dataset = str(job.dataset_hf_repo)
        elif _is_set(job.test_dataset_id):
            dataset = str(job.test_dataset_id)
        if dataset:
            renderables.append(_safe_markup(f"  [bold]Dataset:[/bold] {dataset}"))
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
        if job.status == TrainingJobStatus.FAILED and _is_set(job.error_message):
            renderables.append(_safe_markup(f"  [bold]Error:[/bold] {job.error_message}"))
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
        while job.status in (TrainingJobStatus.RUNNING, TrainingJobStatus.STARTING):
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
            while job.status in (TrainingJobStatus.RUNNING, TrainingJobStatus.STARTING):
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
    poll_callback: Any,
    poll_interval: float = 15,
    warning_message: Optional[str] = None,
) -> None:
    """Run a live-updating display that polls for metrics.

    Args:
        poll_callback: A callable that returns (metrics, job, is_running) each cycle.
            - metrics: PipelineMetricsResponse or None
            - job: TransformJob with current status/usage
            - is_running: bool, False to stop the loop
        poll_interval: Seconds between polls.
        warning_message: Optional warning to persist above the live display.
    """
    import time
    console = Console()

    if _is_notebook():
        from IPython.display import clear_output
        metrics, job, is_running = poll_callback()
        while is_running:
            clear_output(wait=True)
            if warning_message:
                display_warning(warning_message)
            console.print(build_live_display(metrics=metrics, job=job))
            time.sleep(poll_interval)
            metrics, job, is_running = poll_callback()
    else:
        from rich.live import Live
        with Live(
            build_live_display(metrics=None, job=None),
            console=console,
            refresh_per_second=1,
            transient=True,
        ) as live:
            metrics, job, is_running = poll_callback()
            while is_running:
                live.update(build_live_display(metrics=metrics, job=job))
                time.sleep(poll_interval)
                metrics, job, is_running = poll_callback()
            # Final update
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
    renderables.append(_safe_markup("  • Adjust and retry the transform pipeline (e.g., lower confidence thresholds, relax filter criteria)"))
    renderables.append(_safe_markup("  • If the problem persists, contact support or open a GitHub issue: [link=https://github.com/lightning-rod-labs/lightningrod-python-sdk/issues]https://github.com/lightning-rod-labs/lightningrod-python-sdk/issues[/link]"))
    
    return Group(*renderables)


def display_error(message: str, title: str = "Error", job: Any = None) -> None:
    console = Console()
    renderables: list[RenderableType] = []

    renderables.append(_safe_markup(f"[bold bright_red]>> {title}[/bold bright_red]"))
    renderables.append(Text(""))

    if "Job completed with 0 valid rows" in message:
        renderables.append(_build_invalid_samples_error_message(message))
    else:
        renderables.append(_safe_markup(f"[bold]{message}[/bold]"))

    if job is not None:
        cost_lines = _build_cost_lines(job)
        if cost_lines:
            renderables.append(Text(""))
            renderables.extend(cost_lines)

    console.print(Panel(Group(*renderables), border_style="bright_red", padding=(1, 2)))


def display_warning(message: str, title: str = "Warning", job: Any = None) -> None:
    console = Console()
    renderables: list[RenderableType] = []

    renderables.append(_safe_markup(f"[bold yellow]>> {title}[/bold yellow]"))
    renderables.append(Text(""))
    renderables.append(_safe_markup(message))

    if job is not None:
        cost_lines = _build_cost_lines(job)
        if cost_lines:
            renderables.append(Text(""))
            renderables.extend(cost_lines)

    console.print(Panel(Group(*renderables), border_style="yellow", padding=(1, 2)))
