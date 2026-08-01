"""Repository cloning utilities."""

from __future__ import annotations

from pathlib import Path

from git import Repo


class RepositoryCloner:
    """Clone Git repositories using GitPython."""

    def clone(
        self,
        url: str,
        destination: Path,
        *,
        branch: str | None = None,
        depth: int | None = 1,
    ) -> Path:
        """Clone a repository into the given destination."""

        destination.parent.mkdir(parents=True, exist_ok=True)
        if branch is not None and depth is not None and depth > 0:
            Repo.clone_from(url, to_path=str(destination), branch=branch, depth=depth)
        elif branch is not None:
            Repo.clone_from(url, to_path=str(destination), branch=branch)
        elif depth is not None and depth > 0:
            Repo.clone_from(url, to_path=str(destination), depth=depth)
        else:
            Repo.clone_from(url, to_path=str(destination))
        return destination
