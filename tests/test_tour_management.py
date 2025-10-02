"""BDD step definitions for tour management."""

import json
from pathlib import Path

from pytest_bdd import given, when, then, scenario, parsers

from codetour_mcp.core import save_tour, load_tour
from conftest import create_tour_file, load_tour_file


# Scenarios
@scenario("features/tour_management.feature", "Create a new tour")
def test_create_a_new_tour():
    """Test creating a new tour."""
    pass


@scenario("features/tour_management.feature", "Create a tour with description")
def test_create_a_tour_with_description():
    """Test creating a tour with description."""
    pass


@scenario("features/tour_management.feature", "Read an existing tour")
def test_read_an_existing_tour():
    """Test reading an existing tour."""
    pass


@scenario("features/tour_management.feature", "List tours in directory")
def test_list_tours_in_directory():
    """Test listing tours in directory."""
    pass


# Given steps
@given(parsers.parse('a tour directory "{tour_dir}"'), target_fixture="tour_directory")
def tour_directory(temp_tour_dir, tour_dir):
    """Create a tour directory."""
    if tour_dir != ".tours":
        tour_path = temp_tour_dir.parent / tour_dir
        tour_path.mkdir(parents=True, exist_ok=True)
        return tour_path
    return temp_tour_dir


@given(parsers.parse('a tour file exists at "{path}" with title "{title}"'), target_fixture="existing_tour_path")
def existing_tour(temp_tour_dir, path, title):
    """Create an existing tour file."""
    full_path = temp_tour_dir.parent / path
    create_tour_file(str(full_path), title)
    return str(full_path)


# When steps
@when(parsers.parse('I create a tour with path "{path}" and title "{title}"'))
def create_tour(tour_directory, tour_context, path, title):
    """Create a tour with path and title."""
    full_path = tour_directory.parent / path
    tour_data = {"title": title, "steps": []}
    save_tour(str(full_path), tour_data)
    tour_context["tour_path"] = str(full_path)


@when(parsers.parse('I create a tour with path "{path}" and title "{title}" and description "{description}"'))
def create_tour_with_description(tour_directory, tour_context, path, title, description):
    """Create a tour with path, title, and description."""
    full_path = tour_directory.parent / path
    tour_data = {"title": title, "description": description, "steps": []}
    save_tour(str(full_path), tour_data)
    tour_context["tour_path"] = str(full_path)


@when(parsers.parse('I read the tour at "{path}"'))
def read_tour(temp_tour_dir, tour_context, path):
    """Read a tour file."""
    full_path = temp_tour_dir.parent / path
    tour_context["tour_data"] = load_tour(str(full_path))


@when(parsers.parse('I list tours in "{dir}"'))
def list_tours(tour_directory, tour_context, dir):
    """List tours in a directory."""
    dir_path = tour_directory.parent / dir
    tours = []
    for tour_file in dir_path.glob("*.tour"):
        tour_data = load_tour(str(tour_file))
        tours.append({
            "path": str(tour_file),
            "title": tour_data.get("title", ""),
            "description": tour_data.get("description", ""),
            "stepCount": len(tour_data.get("steps", []))
        })
    tour_context["tour_list"] = tours


# Then steps
@then(parsers.parse('the tour file should exist at "{path}"'))
def tour_file_exists(tour_directory, path):
    """Verify tour file exists."""
    full_path = tour_directory.parent / path
    assert Path(full_path).exists()


@then(parsers.parse('the tour should have title "{title}"'))
def tour_has_title(tour_directory, tour_context, title):
    """Verify tour has the expected title."""
    if "tour_path" in tour_context:
        tour_data = load_tour(tour_context["tour_path"])
    else:
        tour_data = tour_context["tour_data"]
    assert tour_data["title"] == title


@then(parsers.parse('the tour should have description "{description}"'))
def tour_has_description(tour_directory, tour_context, description):
    """Verify tour has the expected description."""
    if "tour_path" in tour_context:
        tour_data = load_tour(tour_context["tour_path"])
    else:
        tour_data = tour_context["tour_data"]
    assert tour_data.get("description") == description


@then(parsers.parse('the tour should have {count:d} steps'))
def tour_has_step_count(tour_directory, tour_context, count):
    """Verify tour has the expected number of steps."""
    if "tour_path" in tour_context:
        tour_data = load_tour(tour_context["tour_path"])
    else:
        tour_data = tour_context["tour_data"]
    assert len(tour_data.get("steps", [])) == count


@then(parsers.parse('I should get a tour object with title "{title}"'))
def tour_object_has_title(tour_context, title):
    """Verify tour object has the expected title."""
    assert tour_context["tour_data"]["title"] == title


@then(parsers.parse('I should get {count:d} tours'))
def tour_list_has_count(tour_context, count):
    """Verify tour list has the expected count."""
    assert len(tour_context["tour_list"]) == count


@then(parsers.parse('the tour list should contain "{path}"'))
def tour_list_contains_path(tour_directory, tour_context, path):
    """Verify tour list contains the expected path."""
    full_path = str(tour_directory.parent / path)
    paths = [tour["path"] for tour in tour_context["tour_list"]]
    assert full_path in paths
