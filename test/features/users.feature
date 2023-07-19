Feature: Handle creating, retrieving user details
 As a Holy Grail API user
 I want to be able to create users
 So that I can add and retrieve top user quotes to have a focused good laugh

Scenario: Create user
    Given Server is responding with health status '200' at "http://localhost:8080/health"
     And create user endpoint POST "http://localhost:8080/users" is triggered
    When user enters new user name 'Hase02'
     And user enters new user password '2'
    Then '200' response is returned
     And the following details are returned:
     | id         |
     | <"auto-incremeneted user id">|

Scenario: Get user's id
    Given Server is responding with health status '200' at "http://localhost:8080/health"
     And create user endpoint POST "http://localhost:8080/users" is triggered

Scenario: Get user's top quotes
Scenario: Add a quote to user's top quotes