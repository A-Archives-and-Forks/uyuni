# Copyright (c) 2015 SUSE LLC
# Licensed under the terms of the MIT license.

@setup
Feature: Create a new user

  Scenario: Create a new user
    Given I am on the Users page
    When I follow "Create User"
    And I enter "user1" as "login"
    And I enter "user1" as "desiredpassword"
    And I enter "user1" as "desiredpasswordConfirm"
    And I select "Mr." from "prefix"
    And I enter "Test" as "firstNames"
    And I enter "User" as "lastName"
    And I enter "galaxy-noise@suse.de" as "email"
    And I click on "Create Login"
    Then I should see a "Account user1 created, login information sent to galaxy-noise@suse.de" text
    And I should see a "user1" link
    And I should see a "normal user" text

  Scenario: Login as user1
    Given I am authorized as "user1" with password "user1"
    Then I should see a "user1" link
