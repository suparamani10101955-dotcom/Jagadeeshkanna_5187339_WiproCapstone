Feature: 99acres filter functionality
  As a user
  I want to apply listing filters
  So that I can narrow down property results

  Scenario: Apply owner, dropdown, and checkbox filters
    Given the user launches the 99acres website
    When the user opens the login panel
    And the user selects the Login/Register option
    And the user enters mobile number "9629705329"
    And the user clicks the Continue button
    And the system waits for manual OTP entry
    And the user searches for properties
    Then the user applies property filters
