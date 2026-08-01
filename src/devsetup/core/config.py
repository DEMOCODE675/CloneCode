"""Central configuration for DevSetup."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from platformdirs import user_cache_dir, user_config_dir, user_state_dir
from pydantic import BaseModel, ConfigDict, Field


class CloneSettings(BaseModel):
    """Repository cloning configuration."""

    model_config = ConfigDict(frozen=True)

    branch: str | None = None
    depth: int = 1
    destination: Path | None = None


class ScanSettings(BaseModel):
    """Filesystem scanning configuration."""

    model_config = ConfigDict(frozen=True)

    max_depth: int | None = None
    ignore_directories: tuple[str, ...] = (
        ".git",
        ".hg",
        ".svn",
        "node_modules",
        "dist",
        "build",
        "target",
        "vendor",
        ".venv",
        "venv",
        ".mypy_cache",
        ".pytest_cache",
        "__pycache__",
    )


class InstallSettings(BaseModel):
    """Dependency installation configuration."""

    model_config = ConfigDict(frozen=True)

    install_missing_sdks: bool = False
    install_dependencies: bool = True
    dry_run: bool = False


class CacheSettings(BaseModel):
    """Cache and state directory configuration."""

    model_config = ConfigDict(frozen=True)

    root: Path = Field(default_factory=lambda: Path(user_cache_dir("devsetup")))
    state: Path = Field(default_factory=lambda: Path(user_state_dir("devsetup")))
    config: Path = Field(default_factory=lambda: Path(user_config_dir("devsetup")))


class AppConfig(BaseModel):
    """Top-level application configuration."""

    model_config = ConfigDict(frozen=True)

    clone: CloneSettings = Field(default_factory=CloneSettings)
    scan: ScanSettings = Field(default_factory=ScanSettings)
    install: InstallSettings = Field(default_factory=InstallSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)
    plugin_search_paths: tuple[Path, ...] = ()
    plugin_entrypoint_group: str = "devsetup.plugins"

    @classmethod
    def load(cls, path: Path | None = None) -> AppConfig:
        """Load configuration from YAML if present, otherwise return defaults."""

        if path is None or not path.exists():
            return cls()

        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            return cls()

        return cls.model_validate(_normalize_paths(raw))

    def dump(self, path: Path) -> None:
        """Write the configuration to disk as YAML."""

        path.parent.mkdir(parents=True, exist_ok=True)
        payload = self.model_dump(mode="python")
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _normalize_paths(value: Any) -> Any:
    """Recursively normalize YAML values that represent paths."""

    if isinstance(value, dict):
        return {key: _normalize_paths(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_paths(item) for item in value]
    if isinstance(value, str) and ("/" in value or "\\" in value):
        return Path(value)
    return value
