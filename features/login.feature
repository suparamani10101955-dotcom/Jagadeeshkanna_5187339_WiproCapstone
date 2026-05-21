Feature: 99acres login functionality
  As a user
  I want to start login with my mobile number
  So that I can proceed to OTP verification

  Scenario: Login flow until manual OTP entry
    Given the user launches the 99acres website
    When the user opens the login panel
    And the user selects the Login/Register option
    And the user enters mobile number "9629705329"
    And the user clicks the Continue button
    Then the system waits for manual OTP entry
