Feature: Negative Testcase
  As a user
  I want invalid search input to be blocked
  So that the website prevents empty and whitespace-only searches

  Scenario: Search with Empty Input
    Given the user launches the 99acres homepage for negative search
    When the user keeps the search box empty
    And the user clicks the negative search button
    Then a validation message should appear or the search should not be performed

  Scenario: Enter Only Spaces in Search Field
    Given the user launches the 99acres homepage for negative search
    When the user enters only spaces in the search field
    And the user clicks the negative search button
    Then a validation message should appear or the search should be blocked
