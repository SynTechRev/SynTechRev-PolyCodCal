# VS Code Tagging Quick Reference

This guide addresses common issues when creating release tags from VS Code terminal.

## Quick Start (Recommended)

If you're in VS Code and want to tag a release, use the automated script:

```bash
./scripts/create_release_tag.sh v0.1.0 "Release v0.1.0 - Initial stable release"
```

This handles all the edge cases automatically.

## Common VS Code Issues and Solutions

### Issue 1: `git stash push -u -m "message"` fails

**Error:**
```
No local changes to save
```

**Why it happens:**
- Your working directory is already clean
- `git stash` only works when there are uncommitted changes
- This is actually a good thing - you're ready to tag!

**Solution:**
```bash
# Check if you have changes first
git status -s

# Only stash if the output is not empty
if [[ -n $(git status -s) ]]; then
    git stash push -u -m "pre-tag cleanup"
else
    echo "No changes to stash - proceeding to tag"
fi

# Or just skip stashing if working tree is clean
```

### Issue 2: `git pull --ff-only` fails

**Error:**
```
fatal: couldn't find remote ref main
# or
Authentication failed
```

**Why it happens:**
1. **Branch doesn't exist:** The `main` branch might not exist locally or remotely
2. **Authentication:** VS Code needs credentials configured for HTTPS, or SSH keys for SSH URLs
3. **Detached HEAD:** You might be on a specific commit, not a branch

**Solutions:**

#### Solution A: Check what branches exist
```bash
# See all branches
git branch -a

# Check current branch/commit
git branch --show-current
git log --oneline -1
```

#### Solution B: Skip pulling if on feature branch
If you're on a feature branch like `copilot/cleanup-and-tag-phase-5`, you can tag directly:

```bash
# You don't need to switch to main
# Just tag where you are
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

#### Solution C: Fix authentication
For HTTPS (requires token or credentials):
```bash
# Check remote URL
git remote -v

# If using HTTPS, you may need to configure credentials
# In VS Code, this is usually handled by the Git extension
# Make sure you're signed into GitHub in VS Code
```

For SSH (requires SSH keys):
```bash
# Check if SSH keys are set up
ssh -T git@github.com

# If not, switch remote to SSH
git remote set-url origin git@github.com:SynTechRev/SynTechRev-PolyCodCal.git
```

### Issue 3: `git clean -xdf` too aggressive

**Problem:**
This command removes ALL untracked files, including:
- Local configuration files
- IDE settings you want to keep
- Downloaded data files
- Anything not in `.gitignore` and not committed

**Solution:**
Use the safer cleanup script instead:

```bash
# Safe cleanup - only removes build artifacts
./scripts/cleanup_repo.sh
```

Or clean specific types manually:
```bash
# Python cache only
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Test artifacts only  
rm -rf .pytest_cache htmlcov .coverage

# Linter cache only
rm -rf .mypy_cache .ruff_cache
```

### Issue 4: `.git/index.lock` file exists

**Error:**
```
fatal: Unable to create '.git/index.lock': File exists
```

**Why it happens:**
- A previous git operation was interrupted
- Another git process is running
- VS Code Git extension might be refreshing

**Solution:**
```bash
# Make sure no git operations are running
ps aux | grep git

# Remove the lock file (ONLY if no git processes are running!)
rm -f .git/index.lock

# Now try your git command again
```

## Recommended VS Code Workflow

### Method 1: Using the Automation Script (Easiest)

```bash
# 1. Open integrated terminal in VS Code (Ctrl+`)
cd /home/runner/work/SynTechRev-PolyCodCal/SynTechRev-PolyCodCal

# 2. Run the tag script
./scripts/create_release_tag.sh v0.1.0 "Release v0.1.0"

# 3. Follow the prompts
# - Script checks for issues
# - Cleans artifacts
# - Creates tag
# - Offers to push
```

### Method 2: Manual Steps (More Control)

```bash
# 1. Check current state
git status
git log --oneline -5

# 2. Clean artifacts (safe)
./scripts/cleanup_repo.sh

# 3. Create tag
git tag -a v0.1.0 -m "Release v0.1.0

- Comprehensive documentation
- Code repair strategy
- VS Code integration
- 100% test coverage
"

# 4. Verify tag
git tag -l
git show v0.1.0

# 5. Push tag
git push origin v0.1.0
```

## VS Code Git Integration

### Using VS Code Source Control Panel

1. **Create Tag:**
   - Click Source Control icon (Ctrl+Shift+G)
   - Click "..." menu → "Tags" → "Create Tag"
   - Enter tag name: `v0.1.0`
   - Enter message
   - Note: VS Code creates lightweight tags by default, use terminal for annotated tags

2. **Push Tag:**
   - After creating tag via Source Control
   - Open terminal and run: `git push origin v0.1.0`
   - Or use Command Palette (Ctrl+Shift+P) → "Git: Push Tags"

3. **View Tags:**
   - Source Control "..." menu → "Tags" → "View Tags"

### Authentication in VS Code

VS Code uses different authentication methods:

1. **GitHub Authentication:**
   - Click Account icon (bottom left)
   - Sign in with GitHub
   - Grants access to repos

2. **Git Credential Manager:**
   - Handles HTTPS authentication
   - Prompts when needed
   - Stores credentials securely

3. **SSH Keys:**
   - VS Code uses your system SSH keys
   - Set up SSH keys: [GitHub SSH docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

## Troubleshooting Checklist

Before tagging, verify:

- [ ] Working directory is clean: `git status`
- [ ] You're on the right commit: `git log -1`
- [ ] CHANGELOG.md is updated with the version
- [ ] All tests pass (if you can run them)
- [ ] No `.git/index.lock` file exists
- [ ] You're authenticated to GitHub in VS Code

## When to Tag from Feature Branch vs Main

### Tag from Feature Branch When:
- You're in CI/CD environment
- Main branch doesn't exist locally
- You're completing a specific phase of work
- The feature branch IS ready for release

### Tag from Main Branch When:
- Main branch exists and is up to date
- Following traditional release workflow
- Multiple features are being released together

**For this project:** Since you're on `copilot/cleanup-and-tag-phase-5` and it represents the state you want to release, it's fine to tag directly from this branch. After tagging, merge the branch to main (or make main point to this commit).

## Example: Complete VS Code Tagging Session

```bash
# Step 1: Check where you are
git status
# Output: On branch copilot/cleanup-and-tag-phase-5
# Output: nothing to commit, working tree clean
# ✓ Good - working tree is clean, no need to stash

# Step 2: Check branches
git branch -a
# Output: * copilot/cleanup-and-tag-phase-5
# Note: Main branch doesn't exist locally, that's OK

# Step 3: Clean artifacts
./scripts/cleanup_repo.sh
# ✓ Removes build files safely

# Step 4: Create tag
git tag -a v0.1.0 -m "Release v0.1.0 - Phase 1 complete"
# ✓ Tag created

# Step 5: Verify
git show v0.1.0
# Shows tag details

# Step 6: Push
git push origin v0.1.0
# ✓ Tag pushed to GitHub

# Step 7: Create GitHub Release
# Go to: https://github.com/SynTechRev/SynTechRev-PolyCodCal/releases/new
# Select tag: v0.1.0
# Add release notes from CHANGELOG.md
# Publish!
```

## What NOT to Do

❌ Don't use `git clean -xdf` without understanding what it removes
❌ Don't force-stash when working tree is clean
❌ Don't delete `.git/index.lock` while git operations are running  
❌ Don't create tags with secrets or credentials in commit history
❌ Don't tag without updating CHANGELOG.md
❌ Don't delete remote tags that others might be using

## Getting Help

If you encounter issues:

1. Check the full [TAGGING_GUIDE.md](../TAGGING_GUIDE.md) for detailed explanations
2. Run `./scripts/create_release_tag.sh` for automated handling
3. Verify authentication: `git remote -v` and sign in to GitHub in VS Code
4. Check for lock files: `ls -la .git/ | grep lock`
5. Review git status: `git status -vv`

## Summary

The commands that gave you trouble:

```bash
# ❌ This fails if working tree is clean (good state!)
git stash push -u -m "pre-tag cleanup before switching to main"

# ❌ This fails if main branch doesn't exist or auth issues
git pull --ff-only

# ❌ This is too aggressive and removes everything untracked
git clean -xdf
```

**Instead, use:**

```bash
# ✅ Simple and works from any branch
./scripts/create_release_tag.sh v0.1.0 "Release v0.1.0"

# Or manually:
./scripts/cleanup_repo.sh              # Safe cleanup
git tag -a v0.1.0 -m "Release v0.1.0"  # Create tag
git push origin v0.1.0                  # Push tag
```

That's it! No need to switch branches, stash changes, or pull from remote.
