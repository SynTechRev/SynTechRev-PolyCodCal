#!/bin/bash
# Script to push ops/release-robustness branch and create PR
# This script should be run by a maintainer with GitHub push access

set -e  # Exit on error

echo "============================================"
echo "Release Workflow Enhancement - Push and PR"
echo "============================================"
echo ""

# Check if we're in the right repository
if [ ! -d ".github/workflows" ]; then
    echo "ERROR: Must be run from repository root"
    exit 1
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Switch to ops/release-robustness if not already there
if [ "$CURRENT_BRANCH" != "ops/release-robustness" ]; then
    echo "Switching to ops/release-robustness branch..."
    git checkout ops/release-robustness
fi

# Show the changes
echo ""
echo "=========================================="
echo "Changes in ops/release-robustness branch:"
echo "=========================================="
git log --oneline main..ops/release-robustness 2>/dev/null || git log --oneline 0c5244e..ops/release-robustness
echo ""

# Show files changed
echo "Files modified:"
git diff --name-status main..ops/release-robustness 2>/dev/null || git diff --name-status 0c5244e..ops/release-robustness
echo ""

# Ask for confirmation
read -p "Push ops/release-robustness branch to GitHub? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted. No changes pushed."
    exit 0
fi

# Push the branch
echo "Pushing ops/release-robustness to origin..."
git push -u origin ops/release-robustness

echo ""
echo "✅ Branch pushed successfully!"
echo ""

# Create PR using gh CLI if available
if command -v gh &> /dev/null; then
    echo "=========================================="
    echo "Creating Pull Request"
    echo "=========================================="
    echo ""
    
    # Read PR body from file
    if [ -f "PR_BODY_FOR_RELEASE_WORKFLOW.md" ]; then
        PR_BODY=$(cat PR_BODY_FOR_RELEASE_WORKFLOW.md)
    else
        PR_BODY="See RELEASE_WORKFLOW_CHANGES.md for details.

**Refs:** #31, #32

### ⚠️ Maintainer Action Required

Ensure repository secrets are configured:
- [ ] TEST_PYPI_API_TOKEN
- [ ] PYPI_API_TOKEN

### Changes
- Pre-build cleanup
- Version verification guard
- Robust twine uploads (--skip-existing --verbose)
- Post-publish verification job
- Enhanced logging"
    fi
    
    read -p "Create pull request now? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gh pr create \
            --title "Enhance release workflow with robustness improvements" \
            --body "$PR_BODY" \
            --base main \
            --head ops/release-robustness
        
        echo ""
        echo "✅ Pull request created successfully!"
        echo ""
        echo "View PR: $(gh pr view --web ops/release-robustness 2>&1 || echo 'Open GitHub to see PR')"
    else
        echo ""
        echo "PR not created. You can create it manually:"
        echo "  gh pr create --base main --head ops/release-robustness"
        echo "  or visit: https://github.com/SynTechRev/SynTechRev-PolyCodCal/compare/main...ops/release-robustness"
    fi
else
    echo "=========================================="
    echo "Next Steps (gh CLI not available)"
    echo "=========================================="
    echo ""
    echo "1. Go to GitHub repository"
    echo "2. Click 'Pull requests' → 'New pull request'"
    echo "3. Set base: main, compare: ops/release-robustness"
    echo "4. Title: 'Enhance release workflow with robustness improvements'"
    echo "5. Copy body from: PR_BODY_FOR_RELEASE_WORKFLOW.md"
    echo "6. Reference issues #31 and PR #32"
    echo "7. Add maintainer checklist for secrets"
    echo ""
    echo "Or use this URL:"
    echo "https://github.com/SynTechRev/SynTechRev-PolyCodCal/compare/main...ops/release-robustness"
fi

echo ""
echo "=========================================="
echo "Documentation Files"
echo "=========================================="
echo "- RELEASE_WORKFLOW_CHANGES.md - Implementation details"
echo "- PR_BODY_FOR_RELEASE_WORKFLOW.md - Complete PR description"
echo "- /tmp/patches/ - Git patch files (if needed)"
echo ""
echo "✅ Done!"
