Feature: 99acres property search functionality
  As a user
  I want to navigate to property search results
  So that I can start exploring listings

  Scenario: Navigate to property search results after login
    Given the user launches the 99acres website
    When the user opens the login panel
    And the user selects the Login/Register option
    And the user enters mobile number "9629705329"
    And the user clicks the Continue button
    And the system waits for manual OTP entry
    Then the user searches for properties
