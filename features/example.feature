@smoke @regression
Feature: Example Test Suite
  As a tester
  I want to demonstrate the framework capabilities
  So that I can understand how to write tests

  Background:
    Given I navigate to "https://example.com"

  @TC-001 @high-priority
  Scenario: Verify page title
    Then the page title should contain "Example"
    And I should see "h1"
    When I take a screenshot named "homepage"

  @TC-002
  Scenario: Verify navigation
    When I click on "a[href='/about']"
    Then the page URL should contain "/about"
    And I should see "About"

  @TC-003 @data-driven
  Scenario Outline: Search functionality
    When I enter "<search_term>" in "input[name='search']"
    And I click "button[type='submit']"
    Then I should see "<expected_result>" in ".results"

    Examples:
      | search_term | expected_result |
      | playwright  | Playwright      |
      | automation  | Automation      |
      | testing     | Testing         |

  @TC-004 @form-test
  Scenario: Form submission
    When I enter "John Doe" in "input[name='name']"
    And I enter "john@example.com" in "input[name='email']"
    And I select "Option 1" from "select[name='option']"
    And I check "input[name='subscribe']"
    And I click "button[type='submit']"
    Then I should see "Thank you" in ".success-message"
    And I wait for 2 seconds

  @TC-005 @authentication
  Scenario: User login
    When I navigate to "https://example.com/login"
    And I enter "testuser" in "#username"
    And I enter "password123" in "#password"
    And I click "button#login"
    Then I should be on "https://example.com/dashboard"
    And I should see ".user-profile"