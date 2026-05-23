Feature: E2E Testcase
  As a user
  I want to complete the full 99acres flow
  So that I can reach the property details page

  Scenario: Complete login, search, filter, and property details flow
    Given the user launches the 99acres website
    When the user opens the login panel
    And the user selects the Login/Register option
    And the user enters mobile number "9629705329"
    And the user clicks the Continue button
    And the system waits for manual OTP entry
    And the user completes OTP login
    And the user searches for properties
    And the user applies property filters
    And the user opens the property details page
    Then the property details page should load successfully
