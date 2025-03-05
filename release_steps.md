# Release Creation Guide for Botwell

This document outlines the steps to create a new release of the Botwell package based on the CHANGELOG.md file.

## 1. Update Version Numbers

### ✅ Update setup.py 

The version number in `setup.py` has been updated from 1.0.0 to 1.2.0.

### ✅ Update CHANGELOG.md

The Unreleased section in CHANGELOG.md has been moved to a 1.2.0 release with today's date (2025-03-05).

## 2. Create a Git Tag

```bash
# Commit the changes first
git add setup.py docs/CHANGELOG.md
git commit -m "Bump version to 1.2.0"

# Create a tag for the new version
git tag -a v1.2.0 -m "Version 1.2.0 - University Grade Scale and N/A Handling"

# Push the tag to the remote repository
git push origin v1.2.0
```

## 3. Build Distribution Packages

```bash
# Make sure you have the latest build tools
pip install --upgrade build twine

# Build the distribution packages
python -m build

# This will create both source distribution (.tar.gz) and 
# wheel distribution (.whl) in the dist/ directory
```

## 4. Upload to PyPI (if applicable)

```bash
# Upload to PyPI using twine
twine upload dist/*
```

## 5. Create GitHub Release (if using GitHub)

1. Go to the GitHub repository
2. Click on "Releases"
3. Click "Draft a new release"
4. Select the tag "v1.2.0"
5. Set the title to "Version 1.2.0"
6. Copy the relevant section from CHANGELOG.md into the description
7. Attach the distribution files from the dist/ directory
8. Click "Publish release"

## 6. Prepare for Next Release

Create a new Unreleased section in CHANGELOG.md for future changes:

```markdown
## [Unreleased]

### Added
- 

### Changed
- 

### Fixed
- 
```

## 7. Update Documentation (if necessary)

- Update the version number in documentation
- Update API reference documentation if there were API changes
- Update user guides for any new features

## Version Numbering (Semantic Versioning)

- MAJOR: Breaking changes (not backward compatible)
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

This release is version 1.2.0, which indicates new features without breaking changes.