Feature: Step Management
  As a developer
  I want to add and manage steps in tours
  So that I can guide users through the codebase

  Background:
    Given a tour directory ".tours"
    And a tour file exists at ".tours/steps-tour.tour" with title "Steps Tour"

  Scenario: Add a step with pattern regex
    When I insert a step at ".tours/steps-tour.tour" with:
      | file         | src/main.py           |
      | pattern      | def main\\(\\):      |
      | description  | Main entry point      |
      | title        | Main Function         |
    Then the tour should have 1 steps
    And step 0 should have file "src/main.py"
    And step 0 should have pattern "def main\\(\\):"
    And step 0 should have description "Main entry point"
    And step 0 should have title "Main Function"

  Scenario: Add a step with directory
    When I insert a directory step at ".tours/steps-tour.tour" with:
      | file        | README.md              |
      | directory   | .                      |
      | description | Project documentation  |
    Then the tour should have 1 steps
    And step 0 should have file "README.md"
    And step 0 should have directory "."

  Scenario: Insert a step at specific position
    Given the tour at ".tours/steps-tour.tour" has steps:
      | file        | step1.py | step2.py |
      | description | Step 1   | Step 2   |
    When I insert a step at ".tours/steps-tour.tour" at index 1 with:
      | file        | middle.py          |
      | pattern     | class Middle       |
      | description | Middle step        |
    Then the tour should have 3 steps
    And step 0 should have file "step1.py"
    And step 1 should have file "middle.py"
    And step 2 should have file "step2.py"

  Scenario: Update a step description
    Given the tour at ".tours/steps-tour.tour" has a step with:
      | file        | test.py              |
      | pattern     | def test             |
      | description | Old description      |
    When I update step 0 at ".tours/steps-tour.tour" with description "Updated description"
    Then step 0 should have description "Updated description"

  Scenario: Update a step title
    Given the tour at ".tours/steps-tour.tour" has a step with:
      | file        | test.py       |
      | pattern     | def test      |
      | description | Test function |
      | title       | Old Title     |
    When I update step 0 at ".tours/steps-tour.tour" with title "New Title"
    Then step 0 should have title "New Title"

  Scenario: Remove a step
    Given the tour at ".tours/steps-tour.tour" has steps:
      | file        | step1.py | step2.py | step3.py |
      | description | Step 1   | Step 2   | Step 3   |
    When I remove step 1 from ".tours/steps-tour.tour"
    Then the tour should have 2 steps
    And step 0 should have file "step1.py"
    And step 1 should have file "step3.py"

  Scenario: List all steps
    Given the tour at ".tours/steps-tour.tour" has steps:
      | file        | file1.py | file2.py |
      | description | First    | Second   |
    When I list steps in ".tours/steps-tour.tour"
    Then I should get 2 steps
    And step 0 in the list should have file "file1.py"
    And step 1 in the list should have file "file2.py"

  Scenario: Get a specific step
    Given the tour at ".tours/steps-tour.tour" has steps:
      | file        | file1.py | file2.py |
      | description | First    | Second   |
    When I get step 1 from ".tours/steps-tour.tour"
    Then I should get a step with file "file2.py"
    And I should get a step with description "Second"
