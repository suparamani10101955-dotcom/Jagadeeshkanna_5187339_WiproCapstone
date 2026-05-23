Feature: Positive Testcase
  As a user
  I want to search for a Mumbai property and apply filters
  So that I can validate the search results workflow

  Scenario: Search Mumbai properties and apply a filter
    Given the user launches the 99acres homepage for positive search
    When the user clicks the property search field
    And the user enters "Mumbai" in the property search field
    And the user selects the "Mumbai" search suggestion
    And the user clicks the property search button
    Then the Mumbai property search results should load successfully
    When the user applies the primary property filter
    Then the property filter should be applied successfully
