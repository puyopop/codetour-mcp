"""Core functionality for managing CodeTour files."""

import json
from pathlib import Path
from typing import Any


def load_tour(tour_path: str) -> dict[str, Any]:
    """Load a tour file from the given path."""
    path = Path(tour_path)
    if not path.exists():
        raise FileNotFoundError(f"Tour file not found: {tour_path}")

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_tour(tour_path: str, tour_data: dict[str, Any]) -> None:
    """Save a tour file to the given path."""
    path = Path(tour_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(tour_data, f, indent=2, ensure_ascii=False)
        f.write("\n")
