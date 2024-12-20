Feature: Test Scenarios for Amazon Home Page using xpath locators

  Scenario Outline: User can navigate to Home Page
    Given Open Amazon Home page
    When Click on Search Bar
    And Input <Text> into Amazon Search Box
    And Click on Amazon search icon
    Then Verify that the results for <Text> are shown
    Then Verify that <Nth Element> of the search result == <Text>

    Examples:
      | Text |    Nth Element |
      |  Shorts |      14        |
      |  Shoes  |      11        |
      | Russian Vodka   |      10        |