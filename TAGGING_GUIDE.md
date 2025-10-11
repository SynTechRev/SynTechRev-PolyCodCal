# Repository Tagging and Release Guide

This guide provides step-by-step instructions for cleaning up the repository and creating release tags, with special considerations for different environments (local VS Code, CI/CD, etc.).

## Overview

Creating a release tag involves:
1. Ensuring the repository is in a clean state
2. Verifying all tests pass and quality checks are green
3. Creating an annotated Git tag
4. Pushing the tag to GitHub
5. (Optional) Creating a GitHub release

## Prerequisites

Before tagging a release:

- [ ] All tests pass (`pytest -v`)
- [ ] Code quality checks pass (`black --check .`, `ruff check .`, `mypy src`)
- [ ] CHANGELOG.md is updated with the release version and date
- [ ] All intended changes are committed and pushed
- [ ] CI/CD pipeline is green

## Method 1: Simple Tagging (Recommended for CI/CD)

This method works best in CI/CD environments or when you have a clean working directory.

### Step 1: Verify Clean State

```bash
# Check current status
git status

# Should show "nothing to commit, working tree clean"
```

### Step 2: Ensure You're on the Right Branch

```bash
# Check current branch
git branch --show-current

# If you're on a feature branch and want to tag from main:
# Note: In CI/CD, main branch may not exist locally
git log --oneline -5  # Verify you're on the right commit
```

### Step 3: Create the Tag

```bash
# Create an annotated tag (preferred for releases)
git tag -a v0.1.0 -m "Release version 0.1.0

- Comprehensive documentation
- Code repair strategy implementation
- VS Code integration
- 100% test coverage
"

# Verify the tag was created
git tag -l
git show v0.1.0
```

### Step 4: Push the Tag

```bash
# Push the tag to GitHub
git push origin v0.1.0

# Or push all tags
git push origin --tags
```

## Method 2: Cleanup and Tag (For Local Development)

Use this method when working locally in VS Code with potential uncommitted changes.

### Step 1: Save Work in Progress (If Needed)

```bash
# Check if there are uncommitted changes
git status -s

# If there are changes you want to keep:
git stash push -u -m "WIP: before tagging v0.1.0"

# If status shows nothing, skip the stash step
# (attempting to stash with no changes will fail)
```

### Step 2: Clean Build Artifacts

```bash
# Remove Python cache and build artifacts (safe)
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name ".coverage" -delete 2>/dev/null || true
rm -rf htmlcov/ .mypy_cache/ .ruff_cache/ 2>/dev/null || true

# Or use git clean for more aggressive cleanup
# WARNING: This removes ALL untracked files!
# git clean -xdf  # Use with caution!
```

### Step 3: Sync with Remote (If Available)

```bash
# Fetch latest from origin
git fetch origin 2>/dev/null || echo "Fetch failed, continuing with local state"

# Try to pull if on a branch that tracks remote
git pull --ff-only origin $(git branch --show-current) 2>/dev/null || echo "Pull not needed or branch doesn't track remote"

# Alternative: If you want to ensure you're on main
# git checkout main 2>/dev/null && git pull --ff-only origin main || echo "Main branch not available locally"
```

### Step 4: Create and Push Tag

Follow Steps 3-4 from Method 1 above.

### Step 5: Restore Work in Progress (If Stashed)

```bash
# List stashes
git stash list

# Restore the most recent stash
git stash pop

# Or restore a specific stash
# git stash pop stash@{0}
```

## Method 3: Full Repository Reset and Tag

Use this for a completely clean slate (rarely needed).

### Step 1: Backup Current Work

```bash
# Save any uncommitted changes as a patch
git diff > /tmp/my-changes-$(date +%Y%m%d-%H%M%S).patch

# Or commit everything to a backup branch
git checkout -b backup-before-tag-$(date +%Y%m%d-%H%M%S)
git add .
git commit -m "Backup before tagging"
git checkout -  # Return to previous branch
```

### Step 2: Hard Reset to Remote

```bash
# Fetch all changes
git fetch origin

# Reset to match remote branch exactly
git reset --hard origin/$(git branch --show-current)

# Clean all untracked files
git clean -xdf
```

### Step 3: Create and Push Tag

Follow Steps 3-4 from Method 1 above.

## Troubleshooting

### Issue: "git stash push" fails

**Symptom:** `No local changes to save`

**Solution:** This is normal when working tree is clean. Skip the stash step and proceed to tagging.

```bash
# Only stash if there are changes
if [[ -n $(git status -s) ]]; then
    git stash push -u -m "pre-tag cleanup"
else
    echo "No changes to stash, proceeding..."
fi
```

### Issue: "git pull --ff-only" fails

**Symptom:** `Authentication failed` or `fatal: couldn't find remote ref`

**Solutions:**

1. **Authentication Issue:** Configure credentials or use SSH instead of HTTPS
   ```bash
   # Check remote URL
   git remote -v
   
   # Switch to SSH if needed
   git remote set-url origin git@github.com:SynTechRev/SynTechRev-PolyCodCal.git
   ```

2. **Branch doesn't exist remotely:** Create it or tag from current branch
   ```bash
   # Check available remote branches
   git branch -r
   
   # Tag from current branch instead
   git tag -a v0.1.0 -m "Release v0.1.0"
   ```

3. **In CI/CD environment:** You may not need to pull at all
   ```bash
   # CI/CD often checks out specific commits, not branches
   # Just create and push the tag
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

### Issue: "git clean -xdf" removes important files

**Symptom:** Accidentally deleted configuration or local files

**Prevention:** 
1. Always ensure important files are tracked in Git
2. Use `.gitignore` to protect local config files
3. Use more targeted cleanup commands first

**Recovery:**
```bash
# If files were committed, restore them
git checkout HEAD -- <filename>

# If files were never committed, check backups
```

### Issue: Tag already exists

**Symptom:** `fatal: tag 'v0.1.0' already exists`

**Solutions:**

1. **Check existing tags:**
   ```bash
   git tag -l
   git show v0.1.0  # See what's in the existing tag
   ```

2. **Delete and recreate (if tag is only local):**
   ```bash
   git tag -d v0.1.0
   git tag -a v0.1.0 -m "Release v0.1.0"
   ```

3. **Delete remote tag (use with caution!):**
   ```bash
   # Delete local tag
   git tag -d v0.1.0
   
   # Delete remote tag
   git push origin :refs/tags/v0.1.0
   
   # Create new tag
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

4. **Use a different version number:**
   ```bash
   # If v0.1.0 is already released, use v0.1.1 or v0.2.0
   git tag -a v0.1.1 -m "Release v0.1.1"
   ```

### Issue: Permission denied or lock file errors

**Symptom:** `.git/index.lock` or permission errors

**Solution:**
```bash
# Remove lock file (only if no git operations are running!)
rm -f .git/index.lock

# Fix permissions if needed
chmod -R u+w .git/
```

## Best Practices

### 1. Use Semantic Versioning

- **Major (X.0.0):** Breaking changes
- **Minor (0.X.0):** New features, backwards compatible
- **Patch (0.0.X):** Bug fixes, backwards compatible

### 2. Create Annotated Tags

```bash
# Good: Annotated tag with message
git tag -a v0.1.0 -m "Release v0.1.0 - Initial stable release"

# Avoid: Lightweight tag (no metadata)
git tag v0.1.0
```

### 3. Keep CHANGELOG Updated

Ensure `CHANGELOG.md` has an entry for the version you're tagging:

```markdown
## [0.1.0] - 2025-10-11

### Added
- Feature A
- Feature B

### Fixed
- Bug fix C
```

### 4. Verify Before Pushing

```bash
# Check the tag locally before pushing
git show v0.1.0

# Review the commit history
git log --oneline -10

# Ensure CI/CD passed on the commit you're tagging
```

### 5. Create GitHub Release

After pushing the tag, create a GitHub release:

1. Go to: `https://github.com/SynTechRev/SynTechRev-PolyCodCal/releases/new`
2. Select the tag: `v0.1.0`
3. Fill in release title: `Release v0.1.0`
4. Copy content from CHANGELOG.md for the release notes
5. Attach any release artifacts if needed
6. Publish release

## Automation Script

Save this as `scripts/create_release_tag.sh`:

```bash
#!/bin/bash
# Create a release tag with proper checks

set -e  # Exit on error

# Configuration
VERSION="${1:-}"
MESSAGE="${2:-Release $VERSION}"

# Validate input
if [[ -z "$VERSION" ]]; then
    echo "Usage: $0 <version> [message]"
    echo "Example: $0 v0.1.0 'Initial stable release'"
    exit 1
fi

# Validate version format
if [[ ! "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format vX.Y.Z (e.g., v0.1.0)"
    exit 1
fi

echo "Creating release tag: $VERSION"
echo "Message: $MESSAGE"
echo

# Check if tag already exists
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo "Error: Tag $VERSION already exists"
    echo "Use: git tag -d $VERSION  # to delete local tag"
    exit 1
fi

# Check working directory is clean
if [[ -n $(git status -s) ]]; then
    echo "Warning: Working directory has uncommitted changes"
    git status -s
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Clean build artifacts
echo "Cleaning build artifacts..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
rm -rf .pytest_cache htmlcov .coverage .mypy_cache .ruff_cache 2>/dev/null || true

# Create the tag
echo "Creating annotated tag..."
git tag -a "$VERSION" -m "$MESSAGE"

# Show the tag
echo
echo "Tag created successfully:"
git show "$VERSION" --quiet

# Ask to push
echo
read -p "Push tag to origin? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin "$VERSION"
    echo
    echo "Tag pushed successfully!"
    echo "Create GitHub release at:"
    echo "https://github.com/SynTechRev/SynTechRev-PolyCodCal/releases/new?tag=$VERSION"
else
    echo "Tag created locally but not pushed."
    echo "To push later: git push origin $VERSION"
fi
```

Make it executable:
```bash
chmod +x scripts/create_release_tag.sh
```

Usage:
```bash
# Create and push v0.1.0 tag
./scripts/create_release_tag.sh v0.1.0 "Initial stable release with comprehensive documentation"
```

## Quick Reference

### Common Commands

```bash
# List all tags
git tag -l

# Show tag details
git show v0.1.0

# Create annotated tag
git tag -a v0.1.0 -m "Release v0.1.0"

# Push specific tag
git push origin v0.1.0

# Push all tags
git push origin --tags

# Delete local tag
git tag -d v0.1.0

# Delete remote tag
git push origin :refs/tags/v0.1.0

# Check out specific tag
git checkout v0.1.0

# Create branch from tag
git checkout -b hotfix-v0.1.1 v0.1.0
```

### For VS Code Users

In VS Code terminal, use the safest approach:

```bash
# 1. Check status
git status

# 2. Clean artifacts only (safe)
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# 3. Create tag
git tag -a v0.1.0 -m "Release v0.1.0"

# 4. Push tag (may require authentication setup in VS Code)
git push origin v0.1.0
```

## Summary

The key to successful tagging is:

1. **Verify clean state** - No uncommitted changes (or stash them)
2. **Clean artifacts** - Remove build files, not source files
3. **Create annotated tag** - Include version and description
4. **Push to remote** - Share with team and trigger CI/CD
5. **Create GitHub release** - Official release with notes

For most cases, especially in CI/CD, you only need:
```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

The complicated steps are only needed when dealing with local changes, authentication issues, or repository cleanup needs.
