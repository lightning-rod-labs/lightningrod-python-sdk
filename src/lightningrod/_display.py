from __future__ import annotations

from typing import Any, Optional

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from lightningrod._generated.types import Unset


def _is_set(value: Any) -> bool:
    return not isinstance(value, Unset) and value is not None


def _build_cost_summary(job: Any) -> Optional[str]:
    if not _is_set(job.usage):
        return None
    usage = job.usage
    parts = []
    if _is_set(usage.current_cost_dollars):
        parts.append(f"Cost: ${usage.current_cost_dollars:.4f}")
    if _is_set(usage.max_cost_dollars):
        parts.append(f"Max: ${usage.max_cost_dollars:.4f}")
    if _is_set(usage.estimated_cost_dollars):
        parts.append(f"Estimated: ${usage.estimated_cost_dollars:.4f}")
    return " | ".join(parts) if parts else None


def _build_usage_table(job: Any) -> Optional[Table]:
    from lightningrod._generated.models.job_usage_by_step_type_0 import JobUsageByStepType0
    from lightningrod._generated.models.usage_summary import UsageSummary

    if not _is_set(job.usage):
        return None

    usage = job.usage
    has_rows = False

    table = Table(title="Usage Breakdown", show_header=True, header_style="bold cyan")
    table.add_column("Step", style="dim")
    table.add_column("Cost ($)", justify="right")

    if _is_set(usage.by_step) and isinstance(usage.by_step, JobUsageByStepType0):
        for step_name, step_summary in usage.by_step.additional_properties.items():
            cost_val = step_summary.total_cost if not isinstance(step_summary.total_cost, Unset) else 0.0
            table.add_row(step_name, f"${cost_val:.4f}")
            has_rows = True

    if _is_set(usage.total) and isinstance(usage.total, UsageSummary):
        total_cost = usage.total.total_cost if not isinstance(usage.total.total_cost, Unset) else 0.0
        table.add_section()
        table.add_row("[bold]Total[/bold]", f"[bold]${total_cost:.4f}[/bold]")
        has_rows = True

    return table if has_rows else None


def display_error(message: str, title: str = "Error", job: Any = None) -> None:
    console = Console()
    renderables: list[Any] = []

    renderables.append(Text(message))

    if job is not None:
        cost_text = _build_cost_summary(job)
        if cost_text:
            renderables.append(Text(""))
            renderables.append(Text(cost_text, style="dim"))

        usage_table = _build_usage_table(job)
        if usage_table:
            renderables.append(Text(""))
            renderables.append(usage_table)

    console.print(Panel(Group(*renderables), title=title, border_style="bright_red"))


def display_warning(message: str, title: str = "Warning") -> None:
    console = Console()
    console.print(Panel(Text(message), title=title, border_style="yellow"))
