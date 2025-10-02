"""BDD step definitions for step management."""

import json
from pathlib import Path

from pytest_bdd import given, when, then, scenario, parsers

from codetour_mcp.core import save_tour, load_tour
from conftest import create_tour_file, load_tour_file


# Scenarios
@scenario("features/step_management.feature", "Add a step with pattern regex")
def test_add_a_step_with_pattern_regex():
    """Test adding a step with pattern regex."""
    pass


@scenario("features/step_management.feature", "Add a step with directory")
def test_add_a_step_with_directory():
    """Test adding a step with directory."""
    pass


@scenario("features/step_management.feature", "Insert a step at specific position")
def test_insert_a_step_at_specific_position():
    """Test inserting a step at specific position."""
    pass


@scenario("features/step_management.feature", "Update a step description")
def test_update_a_step_description():
    """Test updating a step description."""
    pass


@scenario("features/step_management.feature", "Update a step title")
def test_update_a_step_title():
    """Test updating a step title."""
    pass


@scenario("features/step_management.feature", "Remove a step")
def test_remove_a_step():
    """Test removing a step."""
    pass


@scenario("features/step_management.feature", "List all steps")
def test_list_all_steps():
    """Test listing all steps."""
    pass


@scenario("features/step_management.feature", "Get a specific step")
def test_get_a_specific_step():
    """Test getting a specific step."""
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


@given(parsers.parse('a tour file exists at "{path}" with title "{title}"'))
def existing_tour(tour_directory, path, title):
    """Create an existing tour file."""
    full_path = tour_directory.parent / path
    create_tour_file(str(full_path), title)
    return str(full_path)


@given("the tour at \".tours/steps-tour.tour\" has steps:", target_fixture="tour_with_steps")
def tour_with_steps(tour_directory, datatable):
    """Create a tour with multiple steps from a table."""
    full_path = tour_directory.parent / ".tours/steps-tour.tour"

    files = datatable[0][1:]  # First row, skip "file" header
    descriptions = datatable[1][1:]  # Second row, skip "description" header

    steps = []
    for file, desc in zip(files, descriptions):
        steps.append({
            "file": file,
            "pattern": f"pattern_{file}",
            "description": desc
        })

    tour_data = {"title": "Steps Tour", "steps": steps}
    save_tour(str(full_path), tour_data)
    return str(full_path)


@given(parsers.parse('the tour at "{path}" has a step with:'))
def tour_with_single_step(tour_directory, path, datatable):
    """Create a tour with a single step from a table."""
    full_path = tour_directory.parent / path

    step = {}
    for row in datatable:
        key = row[0]
        value = row[1]
        if key == "file":
            step["file"] = value
        elif key == "pattern":
            step["pattern"] = value
        elif key == "description":
            step["description"] = value
        elif key == "title":
            step["title"] = value

    tour_data = {"title": "Steps Tour", "steps": [step]}
    save_tour(str(full_path), tour_data)
    return str(full_path)


# When steps
@when(parsers.parse('I insert a step at "{path}" with:'))
def insert_step_with_pattern(tour_directory, tour_context, path, datatable):
    """Insert a step with pattern regex."""
    full_path = tour_directory.parent / path
    tour_data = load_tour(str(full_path))

    step = {}
    for row in datatable:
        key = row[0]
        value = row[1]
        if key == "file":
            step["file"] = value
        elif key == "pattern":
            step["pattern"] = value
        elif key == "description":
            step["description"] = value
        elif key == "title":
            step["title"] = value

    tour_data["steps"].append(step)
    save_tour(str(full_path), tour_data)
    tour_context["tour_path"] = str(full_path)


@when(parsers.parse('I insert a directory step at "{path}" with:'))
def insert_step_with_directory(tour_directory, tour_context, path, datatable):
    """Insert a step with directory."""
    full_path = tour_directory.parent / path
    tour_data = load_tour(str(full_path))

    step = {}
    for row in datatable:
        key = row[0]
        value = row[1]
        if key == "file":
            step["file"] = value
        elif key == "directory":
            step["directory"] = value
        elif key == "description":
            step["description"] = value

    tour_data["steps"].append(step)
    save_tour(str(full_path), tour_data)
    tour_context["tour_path"] = str(full_path)


@when(parsers.parse('I insert a step at "{path}" at index {index:d} with:'))
def insert_step_at_index(tour_directory, tour_context, path, index, datatable):
    """Insert a step at specific index."""
    full_path = tour_directory.parent / path
    tour_data = load_tour(str(full_path))

    step = {}
    for row in datatable:
        key = row[0]
        value = row[1]
        if key == "file":
            step["file"] = value
        elif key == "pattern":
            step["pattern"] = value
        elif key == "description":
            step["description"] = value

    tour_data["steps"].insert(index, step)
    save_tour(str(full_path), tour_data)
    tour_context["tour_path"] = str(full_path)


@when(parsers.parse('I update step {index:d} at "{path}" with description "{description}"'))
def update_step_description(tour_directory, tour_context, index, path, description):
    """Update a step's description."""
    full_path = tour_directory.parent / path
    tour_data = load_tour(str(full_path))
    tour_data["steps"][index]["description"] = description
    save_tour(str(full_path), tour_data)
    tour_context["tour_path"] = str(full_path)


@when(parsers.parse('I update step {index:d} at "{path}" with title "{title}"'))
def update_step_title(tour_directory, tour_context, index, path, title):
    """Update a step's title."""
    full_path = tour_directory.parent / path
    tour_data = load_tour(str(full_path))
    tour_data["steps"][index]["title"] = title
    save_tour(str(full_path), tour_data)
    tour_context["tour_path"] = str(full_path)


@when(parsers.parse('I remove step {index:d} from "{path}"'))
def remove_step(tour_directory, tour_context, index, path):
    """Remove a step from tour."""
    full_path = tour_directory.parent / path
    tour_data = load_tour(str(full_path))
    tour_data["steps"].pop(index)
    save_tour(str(full_path), tour_data)
    tour_context["tour_path"] = str(full_path)


@when(parsers.parse('I list steps in "{path}"'))
def list_steps(tour_directory, tour_context, path):
    """List all steps in a tour."""
    full_path = tour_directory.parent / path
    tour_data = load_tour(str(full_path))
    steps = tour_data.get("steps", [])

    step_list = []
    for i, step in enumerate(steps):
        step_info = {"index": i}
        step_info.update(step)
        step_list.append(step_info)

    tour_context["step_list"] = step_list


@when(parsers.parse('I get step {index:d} from "{path}"'))
def get_step(tour_directory, tour_context, index, path):
    """Get a specific step."""
    full_path = tour_directory.parent / path
    tour_data = load_tour(str(full_path))
    tour_context["step_data"] = tour_data["steps"][index]


# Then steps
@then(parsers.parse('the tour should have {count:d} steps'))
def tour_has_step_count(tour_directory, tour_context, count):
    """Verify tour has the expected number of steps."""
    tour_data = load_tour(tour_context["tour_path"])
    assert len(tour_data.get("steps", [])) == count


@then(parsers.parse('step {index:d} should have file "{file}"'))
def step_has_file(tour_directory, tour_context, index, file):
    """Verify step has the expected file."""
    tour_data = load_tour(tour_context["tour_path"])
    assert tour_data["steps"][index]["file"] == file


@then(parsers.parse('step {index:d} should have pattern "{pattern}"'))
def step_has_pattern(tour_directory, tour_context, index, pattern):
    """Verify step has the expected pattern."""
    tour_data = load_tour(tour_context["tour_path"])
    assert tour_data["steps"][index]["pattern"] == pattern


@then(parsers.parse('step {index:d} should have description "{description}"'))
def step_has_description(tour_directory, tour_context, index, description):
    """Verify step has the expected description."""
    tour_data = load_tour(tour_context["tour_path"])
    assert tour_data["steps"][index]["description"] == description


@then(parsers.parse('step {index:d} should have title "{title}"'))
def step_has_title(tour_directory, tour_context, index, title):
    """Verify step has the expected title."""
    tour_data = load_tour(tour_context["tour_path"])
    assert tour_data["steps"][index]["title"] == title


@then(parsers.parse('step {index:d} should have directory "{directory}"'))
def step_has_directory(tour_directory, tour_context, index, directory):
    """Verify step has the expected directory."""
    tour_data = load_tour(tour_context["tour_path"])
    assert tour_data["steps"][index]["directory"] == directory


@then(parsers.parse('I should get {count:d} steps'))
def step_list_has_count(tour_context, count):
    """Verify step list has the expected count."""
    assert len(tour_context["step_list"]) == count


@then(parsers.parse('step {index:d} in the list should have file "{file}"'))
def step_in_list_has_file(tour_context, index, file):
    """Verify step in list has the expected file."""
    assert tour_context["step_list"][index]["file"] == file


@then(parsers.parse('I should get a step with file "{file}"'))
def step_data_has_file(tour_context, file):
    """Verify step data has the expected file."""
    assert tour_context["step_data"]["file"] == file


@then(parsers.parse('I should get a step with description "{description}"'))
def step_data_has_description(tour_context, description):
    """Verify step data has the expected description."""
    assert tour_context["step_data"]["description"] == description
