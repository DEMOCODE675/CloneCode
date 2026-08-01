"""Command execution helpers."""

from __future__ import annotations

import subprocess
from collections.abc import Mapping
from pathlib import Path
from shutil import which

from devsetup.core.models import CommandResult


class CommandRunner:
    """Execute external commands in a platform-safe way."""

    def run(
        self,
        command: list[str] | tuple[str, ...],
        *,
        cwd: Path | None = None,
        env: Mapping[str, str] | None = None,
        check: bool = True,
    ) -> CommandResult:
        """Run a command and capture its output."""

        completed = subprocess.run(
            list(command),
            cwd=cwd,
            env=dict(env) if env is not None else None,
            capture_output=True,
            text=True,
            check=False,
        )
        result = CommandResult(
            command=tuple(command),
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
        if check and completed.returncode != 0:
            raise subprocess.CalledProcessError(
                completed.returncode,
                list(command),
                output=completed.stdout,
                stderr=completed.stderr,
            )
        return result

    def exists(self, executable: str) -> bool:
        """Return whether an executable is available on PATH."""

        return which(executable) is not None
