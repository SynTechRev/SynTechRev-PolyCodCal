#!/bin/bash
# Create a release tag with proper checks and cleanup
# Usage: ./scripts/create_release_tag.sh v0.1.0 "Optional release message"

set -e  # Exit on error

# Configuration
VERSION="${1:-}"
MESSAGE="${2:-Release $VERSION}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_error() {
    echo -e "${RED}Error: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_step() {
    echo -e "\n${BLUE}==> $1${NC}"
}

# Validate input
if [[ -z "$VERSION" ]]; then
    print_error "Version is required"
    echo "Usage: $0 <version> [message]"
    echo "Example: $0 v0.1.0 'Initial stable release'"
    exit 1
fi

# Validate version format (semantic versioning)
if [[ ! "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    print_error "Version must be in format vX.Y.Z (e.g., v0.1.0)"
    exit 1
fi

print_step "Creating release tag: $VERSION"
print_info "Message: $MESSAGE"

# Check if tag already exists locally
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    print_error "Tag $VERSION already exists locally"
    echo "To delete it: git tag -d $VERSION"
    exit 1
fi

# Check if tag exists remotely
if git ls-remote --tags origin | grep -q "refs/tags/$VERSION"; then
    print_error "Tag $VERSION already exists on remote"
    echo "Either:"
    echo "  1. Use a different version number"
    echo "  2. Delete remote tag: git push origin :refs/tags/$VERSION"
    exit 1
fi

# Check working directory status
print_step "Checking working directory status"
if [[ -n $(git status -s) ]]; then
    print_warning "Working directory has uncommitted changes:"
    git status -s
    echo
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Aborted by user"
        exit 1
    fi
else
    print_success "Working directory is clean"
fi

# Clean build artifacts
print_step "Cleaning build artifacts"
CLEANED=0

# Python cache
if find . -type d -name "__pycache__" 2>/dev/null | grep -q .; then
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    CLEANED=$((CLEANED + 1))
fi

# Egg info
if find . -type d -name "*.egg-info" 2>/dev/null | grep -q .; then
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    CLEANED=$((CLEANED + 1))
fi

# Test and coverage artifacts
for dir in .pytest_cache htmlcov .mypy_cache .ruff_cache; do
    if [[ -d "$dir" ]]; then
        rm -rf "$dir" 2>/dev/null || true
        CLEANED=$((CLEANED + 1))
    fi
done

# Coverage file
if [[ -f .coverage ]]; then
    rm -f .coverage 2>/dev/null || true
    CLEANED=$((CLEANED + 1))
fi

if [[ $CLEANED -gt 0 ]]; then
    print_success "Cleaned $CLEANED artifact type(s)"
else
    print_success "No artifacts to clean"
fi

# Verify git lock files don't exist
print_step "Checking for git lock files"
if [[ -f .git/index.lock ]]; then
    print_warning "Found .git/index.lock"
    read -p "Remove it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f .git/index.lock
        print_success "Removed .git/index.lock"
    else
        print_error "Cannot proceed with lock file present"
        exit 1
    fi
else
    print_success "No lock files found"
fi

# Check CHANGELOG.md for version entry
print_step "Verifying CHANGELOG.md"
if [[ -f CHANGELOG.md ]]; then
    # Remove 'v' prefix for CHANGELOG check
    VERSION_NO_V="${VERSION#v}"
    if grep -q "\[$VERSION_NO_V\]" CHANGELOG.md; then
        print_success "Found version $VERSION_NO_V in CHANGELOG.md"
    else
        print_warning "Version $VERSION_NO_V not found in CHANGELOG.md"
        echo "Consider updating CHANGELOG.md before tagging"
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Aborted by user"
            exit 1
        fi
    fi
else
    print_warning "CHANGELOG.md not found"
fi

# Get current branch/commit info
CURRENT_BRANCH=$(git branch --show-current || echo "detached HEAD")
CURRENT_COMMIT=$(git rev-parse --short HEAD)

print_step "Repository information"
echo "Branch: $CURRENT_BRANCH"
echo "Commit: $CURRENT_COMMIT"
echo "Commit message: $(git log -1 --pretty=%B | head -n 1)"

# Create the tag
print_step "Creating annotated tag"
if git tag -a "$VERSION" -m "$MESSAGE"; then
    print_success "Tag $VERSION created successfully"
else
    print_error "Failed to create tag"
    exit 1
fi

# Show the tag
echo
print_info "Tag details:"
git show "$VERSION" --quiet --format="%H%n%an <%ae>%n%ad%n%n%s%n%b"

# Ask to push
echo
read -p "Push tag to origin? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Pushing tag to remote"
    if git push origin "$VERSION"; then
        print_success "Tag pushed successfully!"
        echo
        print_info "Next steps:"
        echo "1. Create GitHub release at:"
        echo "   https://github.com/SynTechRev/SynTechRev-PolyCodCal/releases/new?tag=$VERSION"
        echo "2. Update ROADMAP.md if this completes a phase"
        echo "3. Announce the release to your team"
    else
        print_error "Failed to push tag"
        echo "The tag exists locally. To push later:"
        echo "  git push origin $VERSION"
        exit 1
    fi
else
    print_warning "Tag created locally but not pushed"
    echo "To push later: git push origin $VERSION"
    echo "To delete: git tag -d $VERSION"
fi

print_success "Done!"
