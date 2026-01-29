from __future__ import annotations

from typing import Any, Optional

from rich.console import Console, Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

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
            title="[bold]Pipeline Running[/bold]",
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
        title="[bold]Pipeline Running[/bold]",
        border_style="bright_blue",
        padding=(1, 2),
    )


def display_error(message: str, title: str = "Error", job: Any = None) -> None:
    console = Console()
    renderables: list[RenderableType] = []

    renderables.append(_safe_markup(f"[bold bright_red]>> {title}[/bold bright_red]"))
    renderables.append(Text(""))
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
