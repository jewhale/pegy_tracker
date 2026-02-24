# Issue Draft: Add a Comprehensive Testing Suite

## Summary
The project has pytest and tooling configured but lacks a committed test suite covering core business logic and pipeline persistence.

## Proposed Work
- Add unit tests for:
  - calculation helpers (`cagr`, `eps_cagr_from_annual`)
  - validation helpers (`validate_positive`, `cap_outliers`)
  - PEGY calculator behavior and failure flags
- Add an integration-style test for the daily snapshot pipeline against in-memory SQLite.

## Acceptance Criteria
- `pytest` runs successfully in CI/local and validates core logic paths.
- Tests cover both happy paths and input-validation edge cases.
- Pipeline test confirms snapshots are persisted.

## Notes
This file is an issue draft because this local environment is not connected to a GitHub remote with issue-creation credentials.
