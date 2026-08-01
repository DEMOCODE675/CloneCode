"""Plugin protocol definitions."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from devsetup.core.models import (
    PluginAssessment,
    PluginExecutionContext,
    ProjectSnapshot,
)


@runtime_checkable
class PluginProtocol(Protocol):
    """Contract every DevSetup plugin must satisfy."""

    name: str

    def detect(self, snapshot: ProjectSnapshot) -> PluginAssessment:
        """Return a match assessment for the supplied project snapshot."""

    def validate(self, context: PluginExecutionContext) -> bool:
        """Return whether the plugin is ready to operate on the project."""

    def install(self, context: PluginExecutionContext) -> bool:
        """Install or bootstrap project dependencies."""

    def setup(self, context: PluginExecutionContext) -> bool:
        """Apply project-specific setup steps."""

    def doctor(self, context: PluginExecutionContext) -> bool:
        """Run project-specific health checks."""

    def run(self, context: PluginExecutionContext) -> bool:
        """Run the project using the conventional dev command."""
