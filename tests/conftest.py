"""Pytest configuration and shared fixtures for BDD tests."""

import json
import shutil
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def temp_tour_dir(tmp_path: Path):
    """Create a temporary tour directory for testing."""
    tour_dir = tmp_path / ".tours"
    tour_dir.mkdir(parents=True, exist_ok=True)
    yield tour_dir
    # Cleanup
    if tour_dir.exists():
        shutil.rmtree(tour_dir)


@pytest.fixture
def tour_context():
    """Shared context for tour operations in BDD tests."""
    return {
        "tour_data": None,
        "tour_list": None,
        "step_list": None,
        "step_data": None,
        "last_result": None,
    }


def create_tour_file(path: str, title: str, description: str = "", steps: list[dict[str, Any]] | None = None):
    """Helper function to create a tour file."""
    tour_data = {"title": title, "steps": steps or []}
    if description:
        tour_data["description"] = description

    tour_path = Path(path)
    tour_path.parent.mkdir(parents=True, exist_ok=True)

    with open(tour_path, "w", encoding="utf-8") as f:
        json.dump(tour_data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def load_tour_file(path: str) -> dict[str, Any]:
    """Helper function to load a tour file."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)
