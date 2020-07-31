# Copyright (c) 2015 SUSE LLC
# Licensed under the terms of the MIT license.

@sle15sp1_client
Feature: Bootstrap a SLES 15 SP1 traditional client
  In order to register a traditional client to the SUSE Manager server
  As the root user
  I want to call rhnreg_ks

  Scenario: Register a SLES 15 SP1 traditional client
    When I register "sle15sp1_client" as traditional client with activation key "1-sle15sp1_client_key"
    And I run "mgr-actions-control --enable-all" on "sle15sp1_client"
    Then I should see "sle15sp1_client" via spacecmd

  Scenario: The onboarding of SLES 15 SP1 traditional client is completed
    Given I am authorized
    Then I wait until onboarding is completed for "sle15sp1_client"

  Scenario: Check registration values of SLES 15 SP1 traditional
    Given I update the profile of "sle15sp1_client"
    When I am on the Systems overview page of this "sle15sp1_client"
    And I wait until I see "Software Updates Available" text or "System is up to date" text
    Then I should see a "System Status" text
    And I should see a "Edit These Properties" link
    And I should see a "[Management]" text
    And I should see a "Add to SSM" link
    And I should see a "Delete System" link
    And I should see a "Initial Registration Parameters:" text
    And I should see a "OS: sles-release" text

@proxy
  Scenario: Check connection from SLES 15 SP1 traditional to proxy
    Given I am on the Systems overview page of this "sle15sp1_client"
    When I follow "Details" in the content area
    And I follow "Connection" in the content area
    Then I should see "proxy" hostname

@proxy
  Scenario: Check registration on proxy of SLES 15 SP1 traditional
    Given I am on the Systems overview page of this "proxy"
    When I follow "Details" in the content area
    And I follow "Proxy" in the content area
    Then I should see "sle15sp1_client" hostname

  Scenario: Check tab links "Software" => "Patches" for SLES 15 SP1 traditional
    Given I am on the Systems overview page of this "sle15sp1_client"
    When I follow "Software" in the content area
    And I follow "Patches" in the content area
    Then I should see a "Relevant Patches" text
    And I should see a "Show" button
