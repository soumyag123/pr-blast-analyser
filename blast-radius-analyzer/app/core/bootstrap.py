import sqlite3

from app.core.config import get_settings


def ensure_directories() -> None:
    """Create required local storage directories."""
    settings = get_settings()
    settings.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    settings.reports_dir.mkdir(parents=True, exist_ok=True)
    settings.chroma_dir.mkdir(parents=True, exist_ok=True)


def initialize_sqlite() -> None:
    """Initialize the local SQLite database."""
    settings = get_settings()
    with sqlite3.connect(settings.sqlite_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS app_state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        connection.commit()


def bootstrap_app() -> None:
    """Prepare local resources required by the app."""
    ensure_directories()
    initialize_sqlite()
