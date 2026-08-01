"""Filesystem scanning and manifest parsing."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import yaml

from devsetup.core.config import ScanSettings
from devsetup.core.models import FileSignal, ManifestData, ProjectSnapshot

_MANIFEST_NAMES = {
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "composer.json",
    "Gemfile",
    "pubspec.yaml",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
}

_LOCK_FILES = {
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lockb",
    "poetry.lock",
    "uv.lock",
    "Cargo.lock",
    "composer.lock",
    "Gemfile.lock",
    "pubspec.lock",
}


class ProjectScanner:
    """Scan a project tree for manifests, lock files, and signals."""

    def __init__(self, settings: ScanSettings | None = None) -> None:
        self._settings = settings or ScanSettings()

    def scan(self, root: Path) -> ProjectSnapshot:
        """Return a snapshot of the project rooted at ``root``."""

        files: list[Path] = []
        signals: list[FileSignal] = []
        manifests: dict[str, ManifestData] = {}
        for path in self._iter_files(root):
            relative = path.relative_to(root)
            files.append(relative)
            if path.name in _MANIFEST_NAMES:
                parsed = self._parse_manifest(path)
                if parsed is not None:
                    manifests[path.name] = ManifestData(path=relative, data=parsed)
                signals.append(FileSignal(path=relative, reason="manifest"))
            elif path.name in _LOCK_FILES:
                signals.append(FileSignal(path=relative, reason="lock-file"))
        return ProjectSnapshot(root=root, files=tuple(files), manifests=manifests, signals=tuple(signals))

    def _iter_files(self, root: Path) -> list[Path]:
        """Yield files below ``root`` while honoring ignore settings."""

        discovered: list[Path] = []
        ignore_directories = set(self._settings.ignore_directories)
        max_depth = self._settings.max_depth
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(root)
            if any(part in ignore_directories for part in relative.parts):
                continue
            if max_depth is not None and len(relative.parts) > max_depth:
                continue
            discovered.append(path)
        return discovered

    def _parse_manifest(self, path: Path) -> dict[str, Any] | None:
        """Parse supported manifest file formats into a dictionary."""

        try:
            if path.suffix == ".json":
                return self._coerce_manifest(json.loads(path.read_text(encoding="utf-8")))
            if path.suffix in {".toml", ".lock"} or path.name == "pyproject.toml":
                return self._coerce_manifest(tomllib.loads(path.read_text(encoding="utf-8")))
            if path.suffix in {".yaml", ".yml"}:
                payload = yaml.safe_load(path.read_text(encoding="utf-8"))
                return self._coerce_manifest(payload)
            if path.suffix in {".xml"}:
                return self._xml_to_dict(ET.fromstring(path.read_text(encoding="utf-8")))
            if path.name == "Gemfile":
                return {"source": path.read_text(encoding="utf-8")}
        except Exception:
            return None
        return None

    def _coerce_manifest(self, payload: object) -> dict[str, Any]:
        """Coerce a parsed manifest payload into a dictionary shape."""

        if isinstance(payload, dict):
            return payload
        return {"value": payload}

    def _xml_to_dict(self, element: ET.Element) -> dict[str, Any]:
        """Convert a small XML tree into a nested dictionary."""

        children = list(element)
        if not children:
            return {element.tag: element.text or ""}
        return {element.tag: [self._xml_to_dict(child) for child in children]}
