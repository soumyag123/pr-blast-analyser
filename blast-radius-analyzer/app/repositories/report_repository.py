from datetime import UTC, datetime
from pathlib import Path

from app.core.config import get_settings
from app.domain.report import AnalysisReport


def save_report(report: AnalysisReport) -> Path:
    """Save a markdown report to local storage."""
    settings = get_settings()
    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    filename = f"{report.service_name}-{timestamp}.md"
    path = settings.reports_dir / filename
    path.write_text(report.markdown, encoding="utf-8")
    return path
