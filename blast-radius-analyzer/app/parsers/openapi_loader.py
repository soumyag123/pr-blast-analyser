import json
from pathlib import Path

import yaml


def load_openapi_document(path: Path) -> dict:
    """Load an OpenAPI document from YAML or JSON."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)
