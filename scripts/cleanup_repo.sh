#!/bin/bash
# Clean up Python build artifacts and caches
# Safe to run anytime - only removes generated files, never source code

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

echo -e "${BLUE}==> Cleaning Python artifacts${NC}"

# Count artifacts before cleanup
BEFORE_COUNT=0

# Python bytecode cache
PYCACHE_COUNT=$(find . -type d -name "__pycache__" 2>/dev/null | wc -l)
if [[ $PYCACHE_COUNT -gt 0 ]]; then
    print_info "Removing $PYCACHE_COUNT __pycache__ directories"
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + PYCACHE_COUNT))
fi

# .pyc files
PYC_COUNT=$(find . -type f -name "*.pyc" 2>/dev/null | wc -l)
if [[ $PYC_COUNT -gt 0 ]]; then
    print_info "Removing $PYC_COUNT .pyc files"
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + PYC_COUNT))
fi

# .pyo files
PYO_COUNT=$(find . -type f -name "*.pyo" 2>/dev/null | wc -l)
if [[ $PYO_COUNT -gt 0 ]]; then
    print_info "Removing $PYO_COUNT .pyo files"
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + PYO_COUNT))
fi

# Egg info
EGGINFO_COUNT=$(find . -type d -name "*.egg-info" 2>/dev/null | wc -l)
if [[ $EGGINFO_COUNT -gt 0 ]]; then
    print_info "Removing $EGGINFO_COUNT .egg-info directories"
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + EGGINFO_COUNT))
fi

# Build directory
if [[ -d build ]]; then
    print_info "Removing build/ directory"
    rm -rf build 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + 1))
fi

# Dist directory
if [[ -d dist ]]; then
    print_info "Removing dist/ directory"
    rm -rf dist 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + 1))
fi

echo -e "\n${BLUE}==> Cleaning test artifacts${NC}"

# Pytest cache
if [[ -d .pytest_cache ]]; then
    print_info "Removing .pytest_cache/"
    rm -rf .pytest_cache 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + 1))
fi

# Coverage files
if [[ -f .coverage ]]; then
    print_info "Removing .coverage"
    rm -f .coverage 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + 1))
fi

if [[ -d htmlcov ]]; then
    print_info "Removing htmlcov/"
    rm -rf htmlcov 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + 1))
fi

if [[ -f coverage.xml ]]; then
    print_info "Removing coverage.xml"
    rm -f coverage.xml 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + 1))
fi

echo -e "\n${BLUE}==> Cleaning linter caches${NC}"

# Mypy cache
if [[ -d .mypy_cache ]]; then
    print_info "Removing .mypy_cache/"
    rm -rf .mypy_cache 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + 1))
fi

# Ruff cache
if [[ -d .ruff_cache ]]; then
    print_info "Removing .ruff_cache/"
    rm -rf .ruff_cache 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + 1))
fi

# Pre-commit cache (optional, uncomment if you want to clean it)
# if [[ -d .pre-commit ]]; then
#     print_info "Removing .pre-commit/"
#     rm -rf .pre-commit 2>/dev/null || true
#     BEFORE_COUNT=$((BEFORE_COUNT + 1))
# fi

echo -e "\n${BLUE}==> Cleaning editor files${NC}"

# .DS_Store (macOS)
DSSTORE_COUNT=$(find . -type f -name ".DS_Store" 2>/dev/null | wc -l)
if [[ $DSSTORE_COUNT -gt 0 ]]; then
    print_info "Removing $DSSTORE_COUNT .DS_Store files"
    find . -type f -name ".DS_Store" -delete 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + DSSTORE_COUNT))
fi

# Thumbs.db (Windows)
THUMBS_COUNT=$(find . -type f -name "Thumbs.db" 2>/dev/null | wc -l)
if [[ $THUMBS_COUNT -gt 0 ]]; then
    print_info "Removing $THUMBS_COUNT Thumbs.db files"
    find . -type f -name "Thumbs.db" -delete 2>/dev/null || true
    BEFORE_COUNT=$((BEFORE_COUNT + THUMBS_COUNT))
fi

echo
if [[ $BEFORE_COUNT -gt 0 ]]; then
    print_success "Cleanup complete! Removed $BEFORE_COUNT item(s)"
else
    print_success "Repository is already clean!"
fi

# Show current status
echo -e "\n${BLUE}==> Git status${NC}"
git status --short

echo
print_info "Safe to commit and push!"
