# Copyright (c) 2018-2019 SUSE LLC
# Licensed under the terms of the MIT license.
#
# The scenarios in this feature are skipped:
# * if there is no proxy ($proxy is nil)
# * if there is no private network ($private_net is nil)
#
# Last scenarios (the real bootstrap) are skipped:
# * if there is no PXE boot minion ($pxeboot_mac is nil)

Feature: Mass import Retail terminals
  In order to use SUSE Manager for Retail solution
  As the system administrator
  I want perform a mass import of several virtual terminals and one real minion

@proxy
@private_net
@pxeboot_minion
  Scenario: Install or update PXE formulas on the server
    When I manually install the "tftpd" formula on the server
    And I manually install the "saltboot" formula on the server
    And I manually install the "pxe" formula on the server

@proxy
@private_net
  Scenario: Enable the formulas needed for mass import on the branch server
    Given I am on the Systems overview page of this "proxy"
    When I follow "Formulas" in the content area
    And I check the "pxe" formula
    And I check the "saltboot" formula
    And I check the "tftpd" formula
    And I check the "vsftpd" formula
    And I click on "Save"
    Then the "pxe" formula should be checked
    And the "saltboot" formula should be checked
    And the "tftpd" formula should be checked
    And the "vsftpd" formula should be checked

@proxy
@private_net
@retail_massive_import
  Scenario: Mass import of terminals
    When I copy the retail configuration file "massive-import-terminals.yml" on server
    And I import the retail configuration using retail_yaml command
    And I am on the Systems page
    Then I should see the terminals imported from the configuration file

@proxy
@private_net
@pxeboot_minion
  Scenario: Cheat with missing avahi domain
    #   (Avahi does not cross networks, so we need to cheat by serving tf.local)
    Given I am on the Systems overview page of this "proxy"
    When I follow "Formulas" in the content area
    And I follow first "Bind" in the content area
    And I press "Add Item" in configured zones section
    And I enter "tf.local" in third configured zone name field
    And I press "Add Item" in available zones section
    And I enter "tf.local" in third available zone name field
    And I enter "master/db.tf.local" in third file name field
    And I enter the hostname of "proxy" in third name server field
    And I enter "admin@tf.local." in third contact field
    And I press "Add Item" in third A section
    And I enter the hostname of "proxy" in fifth A name field
    And I enter the IP address of "proxy" in fifth A address field
    And I press "Add Item" in third NS section
    And I enter the hostname of "proxy" in third NS field
    And I click on "Save Formula"
    Then I should see a "Formula saved" text

@proxy
@private_net
@pxeboot_minion
  Scenario: Apply the highstate to take into account the imported formulas
    Given I am on the Systems overview page of this "proxy"
    When I follow "States" in the content area
    And I enable repositories before installing branch server
    And I click on "Apply Highstate"
    And I wait until event "Apply highstate scheduled by admin" is completed
    And I disable repositories after installing branch server

@proxy
@private_net
@pxeboot_minion
@retail_massive_import
  Scenario: Bootstrap the PXE boot minion
    And I am authorized
    And I stop and disable avahi on the PXE boot minion
    And I create bootstrap script and set the activation key "1-SUSE-DEV-x86_64" in the bootstrap script on the proxy
    And I bootstrap pxeboot minion via bootstrap script on the proxy
    And I wait at most 180 seconds until Salt master sees "pxeboot-minion" as "unaccepted"
    And I accept key of pxeboot minion in the Salt master
    Then I navigate to "rhn/systems/Overview.do" page
    And I wait until I see the name of "pxeboot-minion", refreshing the page


@proxy
@private_net
@pxeboot_minion
@retail_massive_import
  Scenario: Check connection from bootstrapped terminal to proxy
    Given I am on the Systems page
    And I follow "pxeboot" terminal
    When I follow "Details" in the content area
    And I follow "Connection" in the content area
    Then I should see "proxy" hostname

@proxy
@private_net
@pxeboot_minion
@retail_massive_import
  Scenario: Install a package on the bootstrapped terminal
    Given I am on the Systems page
    When I follow "pxeboot" terminal
    And I follow "Software" in the content area
    And I follow "Install"
    And I check "virgo-dummy-2.0-1.1" in the list
    And I click on "Install Selected Packages"
    And I click on "Confirm"
    Then I should see a "1 package install has been scheduled" text
    When I wait until event "Package Install/Upgrade scheduled by admin" is completed

@proxy
@private_net
@pxeboot_minion
@retail_massive_import
  Scenario: Cleanup: remove a package on the bootstrapped terminal
    Given I am on the Systems page
    When I follow "pxeboot" terminal
    And I follow "Software" in the content area
    And I follow "List / Remove"
    And I enter "virgo" in the css "input[placeholder='Filter by Package Name: ']"
    And I click on the css "button.spacewalk-button-filter"
    And I check "virgo-dummy-2.0-1.1" in the list
    And I click on "Remove Packages"
    And I click on "Confirm"
    Then I should see a "1 package removal has been scheduled" text
    When I wait until event "Package Removal scheduled by admin" is completed

@proxy
@private_net
@retail_massive_import
  Scenario: Cleanup: delete all imported Retail terminals
    Given I am on the Systems page
    When I delete all the terminals imported
    Then I should not see any terminals imported from the configuration file

@proxy
@private_net
  Scenario: Cleanup: make sure salt-minion is stopped after mass import
    When I stop salt-minion on the PXE boot minion

@proxy
@private_net
  Scenario: Cleanup: delete the terminal groups generated by retail_yaml command
    Given I am on the groups page
    When I follow "HWTYPE:Intel-Genuine" in the content area
    And I follow "Delete Group" in the content area
    And I click on "Confirm Deletion"
    Then I should see a "deleted" text
    When I follow "example.org" in the content area
    And I follow "Delete Group" in the content area
    And I click on "Confirm Deletion"
    Then I should see a "deleted" text
    When I follow "TERMINALS" in the content area
    And I follow "Delete Group" in the content area
    And I click on "Confirm Deletion"
    Then I should see a "deleted" text
    When I follow "SERVERS" in the content area
    And I follow "Delete Group" in the content area
    And I click on "Confirm Deletion"
    Then I should see a "deleted" text

@proxy
@private_net
  Scenario: Cleanup: Disable the formulas needed for mass import
    Given I am on the Systems overview page of this "proxy"
    When I follow "Formulas" in the content area
    And I uncheck the "pxe" formula
    And I uncheck the "saltboot" formula
    And I uncheck the "tftpd" formula
    And I uncheck the "vsftpd" formula
    And I click on "Save"
    Then the "pxe" formula should be unchecked
    And the "saltboot" formula should be unchecked
    And the "tftpd" formula should be unchecked
    And the "vsftpd" formula should be unchecked

@proxy
@private_net
  Scenario: Cleanup: apply the highstate after the mass import cleanup changes
    Given I am on the Systems overview page of this "proxy"
    When I follow "States" in the content area
    And I click on "Apply Highstate"
    And I wait until event "Apply highstate scheduled by admin" is completed
