Feature: Tour Management
  As a developer
  I want to create and manage CodeTour files
  So that I can provide interactive code tours

  Scenario: Create a new tour
    Given a tour directory ".tours"
    When I create a tour with path ".tours/test-tour.tour" and title "Test Tour"
    Then the tour file should exist at ".tours/test-tour.tour"
    And the tour should have title "Test Tour"
    And the tour should have 0 steps

  Scenario: Create a tour with description
    Given a tour directory ".tours"
    When I create a tour with path ".tours/described-tour.tour" and title "Described Tour" and description "A tour with description"
    Then the tour file should exist at ".tours/described-tour.tour"
    And the tour should have title "Described Tour"
    And the tour should have description "A tour with description"

  Scenario: Read an existing tour
    Given a tour file exists at ".tours/existing-tour.tour" with title "Existing Tour"
    When I read the tour at ".tours/existing-tour.tour"
    Then I should get a tour object with title "Existing Tour"

  Scenario: List tours in directory
    Given a tour directory ".tours"
    And a tour file exists at ".tours/tour1.tour" with title "Tour 1"
    And a tour file exists at ".tours/tour2.tour" with title "Tour 2"
    When I list tours in ".tours"
    Then I should get 2 tours
    And the tour list should contain ".tours/tour1.tour"
    And the tour list should contain ".tours/tour2.tour"
