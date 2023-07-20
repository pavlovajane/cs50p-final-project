@fixture.server
Feature: Handle creating, retrieving user details
    As a Holy Grail API user
    I want to be able to create users
    So that I can add and retrieve top user quotes to have a focused good laugh

    Background:
        Given I set Holy Grail API url

    Scenario: Create user
        Given Holy Grail API url health responds with '200'
        When user send create new user POST '/users'
        | username | password |
        | Jane Doe | pass     |
        Then '200' response is returned
        And the following details are returned:
        | id         |
        | <"auto-incremeneted user id">|

    # Future scenarios
    # Scenario: Get user's id
    # Scenario: Get user's top quotes
    # Scenario: Add a quote to user's top quotes
