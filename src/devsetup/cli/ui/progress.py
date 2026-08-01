"""Progress helpers for long-running CLI actions."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)


@contextmanager
def progress_session(label: str) -> Iterator[Progress]:
    """Create a consistent progress session."""

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        task_id = progress.add_task(label, total=100)
        yield progress
        progress.update(task_id, completed=100)