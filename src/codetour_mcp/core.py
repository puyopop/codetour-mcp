"""Core functionality for managing CodeTour files."""

import json
from pathlib import Path
from typing import Any


def load_tour(tour_path: str) -> dict[str, Any]:
    """
    Load a tour file from the given path.

    Args:
        tour_path: Path to the tour file

    Returns:
        Dictionary containing tour data

    Raises:
        FileNotFoundError: If the tour file doesn't exist

    >>> import tempfile
    >>> import os
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = os.path.join(tmpdir, "test.tour")
    ...     with open(path, "w") as f:
    ...         _ = f.write('{"title": "Test", "steps": []}')
    ...     tour = load_tour(path)
    ...     tour["title"]
    'Test'
    >>> load_tour("/nonexistent/path.tour")
    Traceback (most recent call last):
        ...
    FileNotFoundError: Tour file not found: /nonexistent/path.tour
    """
    path = Path(tour_path)
    if not path.exists():
        raise FileNotFoundError(f"Tour file not found: {tour_path}")

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_tour(tour_path: str, tour_data: dict[str, Any]) -> None:
    """
    Save a tour file to the given path.

    Args:
        tour_path: Path where the tour file will be saved
        tour_data: Dictionary containing tour data

    >>> import tempfile
    >>> import os
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = os.path.join(tmpdir, "subdir", "test.tour")
    ...     save_tour(path, {"title": "Test", "steps": []})
    ...     os.path.exists(path)
    True
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = os.path.join(tmpdir, "test.tour")
    ...     save_tour(path, {"title": "Test", "steps": []})
    ...     with open(path) as f:
    ...         "Test" in f.read()
    True
    """
    path = Path(tour_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(tour_data, f, indent=2, ensure_ascii=False)
        f.write("\n")
