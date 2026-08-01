"""Shared typed models used across DevSetup."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any


class Language(StrEnum):
    """Supported project languages."""

    UNKNOWN = "unknown"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    PYTHON = "python"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    DART = "dart"
    PHP = "php"
    RUBY = "ruby"


class Framework(StrEnum):
    """Supported frameworks and platform families."""

    UNKNOWN = "unknown"
    REACT = "react"
    NEXTJS = "nextjs"
    VUE = "vue"
    ANGULAR = "angular"
    SVELTE = "svelte"
    ASTRO = "astro"
    REMIX = "remix"
    EXPRESS = "express"
    NESTJS = "nestjs"
    FASTAPI = "fastapi"
    FLASK = "flask"
    DJANGO = "django"
    SPRING = "spring"
    LARAVEL = "laravel"
    RAILS = "rails"
    FLUTTER = "flutter"


class PackageManager(StrEnum):
    """Supported package and build managers."""

    UNKNOWN = "unknown"
    NPM = "npm"
    PNPM = "pnpm"
    YARN = "yarn"
    BUN = "bun"
    PIP = "pip"
    UV = "uv"
    POETRY = "poetry"
    CARGO = "cargo"
    GO = "go"
    MAVEN = "maven"
    GRADLE = "gradle"
    COMPOSER = "composer"
    GEM = "gem"
    FLUTTER = "flutter"


@dataclass(slots=True, frozen=True)
class FileSignal:
    """A discovered file that helps identify a project."""

    path: Path
    reason: str


@dataclass(slots=True, frozen=True)
class ManifestData:
    """Parsed data for a manifest file."""

    path: Path
    data: dict[str, Any]


@dataclass(slots=True)
class ProjectSnapshot:
    """Immutable project view produced by the scanner."""

    root: Path
    files: tuple[Path, ...]
    manifests: dict[str, ManifestData] = field(default_factory=dict)
    signals: tuple[FileSignal, ...] = field(default_factory=tuple)

    def has_file(self, relative_path: str) -> bool:
        """Return whether a relative path exists in the scan result."""

        candidate = Path(relative_path)
        return any(file_path == candidate for file_path in self.files)

    def has_any_file(self, candidates: tuple[str, ...] | list[str]) -> bool:
        """Return whether any candidate file exists in the scan result."""

        return any(self.has_file(candidate) for candidate in candidates)


@dataclass(slots=True, frozen=True)
class PluginAssessment:
    """Result of asking a plugin whether it matches a project."""

    plugin_name: str
    language: Language
    framework: Framework
    package_manager: PackageManager
    score: float
    matched: bool
    reasons: tuple[str, ...]


@dataclass(slots=True, frozen=True)
class DetectedProject:
    """Best matching plugin and its detected metadata."""

    plugin_name: str
    language: Language
    framework: Framework
    package_manager: PackageManager
    reasons: tuple[str, ...]
    snapshot: ProjectSnapshot


@dataclass(slots=True, frozen=True)
class PluginExecutionContext:
    """Context passed into plugin operations."""

    snapshot: ProjectSnapshot
    config: Any
    runner: Any
    console: Any


@dataclass(slots=True, frozen=True)
class HealthCheckResult:
    """Outcome of a health check step."""

    name: str
    success: bool
    message: str


@dataclass(slots=True, frozen=True)
class CommandResult:
    """Captured command execution result."""

    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
