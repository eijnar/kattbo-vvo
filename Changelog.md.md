---
share: "true"
---


# Common Changelog

This document provides a detailed record of changes, improvements and fixes for the common package, a critical part of the Kättbo VVO homepage.

---

## [0.5.3] - 2023-12-15

### Changed
- **Transitioned from `setup.py` to `pyproject.toml`**:
    - Removed the `setup.py` file.
    - Introduced `pyproject.toml` as the new packaging and build configuration file.

#### Details
- **Files Modified**:
  - Removed: `setup.py`
  - Added: `pyproject.toml`
- **Rationale**: 
  - The change to `pyproject.toml` aligns with modern Python packaging standards and provides a more standardized approach to manage project metadata, dependencies, and build requirements.

#### Impact
- This change simplifies the build and packaging process of the common package.
- It might require updates in the build and release pipeline to accommodate the new configuration format.
- Developers should update their local development setup to align with this change.

#### Migration Notes
- Ensure that your environment is compatible with `pyproject.toml`.
- Update any build scripts or CI/CD pipelines that previously relied on `setup.py`.
- Refer to the new `pyproject.toml` for updated dependencies and build instructions.

#### Additional Resources
- [Link to `pyproject.toml` documentation]
- [Migration guide or relevant discussion thread]

---
## [0.5.2] - 2023-12-15

### Changed
- **Updated `EventDay` Model**: Added a new column `sequence` to the `EventDay` class in the database model.
#### Details
- **File Modified**: `models/events/__init__.py`
- **Class Modified**: `EventDay`
- **New Column Added**:
  - `sequence`: A new column of type `Integer` with a default value of `1`. This column is used track changes to the `EventDay`
#### Impact
- This addition introduces a new field that allows for the iCal to let the subscribers of the calendar to know that an update is needed
- Existing queries and operations involving the `EventDay` model may need to be updated to accommodate this new field.
#### Migration
- A database migration is required to add the `sequence` column to existing tables.

---
