import json
import sys
from pathlib import Path

from app.services.replay_service import load_replay_event


def main() -> int:
    """Load and print a replay pull request event."""
    event_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/sample_events/pr_opened.json")
    event = load_replay_event(event_path)
    print(json.dumps(event.model_dump(mode="json"), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
