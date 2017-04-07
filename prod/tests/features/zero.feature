Feature: Data Loader
  Tet the data loader

  Scenario: Init database
    Given I connect to the database
    Then The connection is valid

  Scenario: Load fake data
    Given I run load data
    Then The database wont be empty

