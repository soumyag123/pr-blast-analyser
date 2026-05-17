from pathlib import Path

from app.domain.contracts import ContractChange
from app.domain.dependencies import CodeEvidence


def collect_snippet(lines: list[str], start_index: int, end_index: int, radius: int = 2) -> tuple[int, int, str]:
    """Collect a nearby code snippet around matched lines."""
    start = max(start_index - radius, 0)
    end = min(end_index + radius + 1, len(lines))
    snippet = "".join(lines[start:end]).strip()
    return start + 1, end, snippet


def build_field_patterns(field_path: str) -> list[str]:
    """Build likely code patterns for a field reference."""
    return [
        f'"{field_path}"',
        f"'{field_path}'",
        f'["{field_path}"]',
        f"['{field_path}']",
        f".{field_path}",
    ]


def scan_service_for_change(service_root: Path, service_name: str, change: ContractChange) -> list[CodeEvidence]:
    """Scan a downstream service for evidence related to a contract change."""
    evidence: list[CodeEvidence] = []
    field_patterns = build_field_patterns(change.field_path)

    for path in sorted(service_root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".py", ".md", ".txt", ".json", ".yaml", ".yml"}:
            continue

        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        endpoint_lines = [index for index, line in enumerate(lines) if change.endpoint in line]
        field_lines = [
            index for index, line in enumerate(lines) if any(pattern in line for pattern in field_patterns)
        ]

        if not endpoint_lines or not field_lines:
            continue

        if path.suffix.lower() == ".py":
            start_index = min(endpoint_lines + field_lines)
            end_index = max(endpoint_lines + field_lines)
            line_start, line_end, snippet = collect_snippet(lines, start_index, end_index, radius=1)
            evidence.append(
                CodeEvidence(
                    service_name=service_name,
                    file_path=path.as_posix(),
                    line_start=line_start,
                    line_end=line_end,
                    snippet=snippet,
                    matched_terms=[change.endpoint, change.field_path],
                )
            )
            continue

        for endpoint_index in endpoint_lines:
            nearest_field_index = min(field_lines, key=lambda idx: abs(idx - endpoint_index))
            start_index = min(endpoint_index, nearest_field_index)
            end_index = max(endpoint_index, nearest_field_index)
            line_start, line_end, snippet = collect_snippet(lines, start_index, end_index, radius=1)
            evidence.append(
                CodeEvidence(
                    service_name=service_name,
                    file_path=path.as_posix(),
                    line_start=line_start,
                    line_end=line_end,
                    snippet=snippet,
                    matched_terms=[change.endpoint, change.field_path],
                )
            )

    deduped: dict[tuple[str, int, int], CodeEvidence] = {}
    for item in evidence:
        key = (item.file_path, item.line_start, item.line_end)
        deduped[key] = item

    return sorted(
        deduped.values(),
        key=lambda item: (0 if item.file_path.endswith(".py") else 1, item.file_path, item.line_start),
    )
