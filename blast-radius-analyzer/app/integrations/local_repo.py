from pathlib import Path


class LocalRepositoryProvider:
    """Provide file access for local repositories."""

    def __init__(self, root_path: Path):
        """Initialize the repository provider."""
        self.root_path = root_path

    def exists(self) -> bool:
        """Return whether the repository path exists."""
        return self.root_path.exists() and self.root_path.is_dir()

    def resolve(self, relative_path: str | Path) -> Path:
        """Return an absolute path inside the repository."""
        return (self.root_path / relative_path).resolve()

    def read_text(self, relative_path: str | Path) -> str:
        """Return text content from a repository file."""
        return self.resolve(relative_path).read_text(encoding="utf-8")

    def list_files(self) -> list[Path]:
        """Return all files in the repository."""
        return sorted(path for path in self.root_path.rglob("*") if path.is_file())
