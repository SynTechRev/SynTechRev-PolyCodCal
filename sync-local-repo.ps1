# Sync Local VS Code Repository with Remote Main Branch
# This script helps sync your local repository with the GitHub main branch
# which already includes all changes from PR #5

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  VS Code Repository Sync Script" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path ".git")) {
    Write-Host "ERROR: Not in a git repository!" -ForegroundColor Red
    Write-Host "Please navigate to: C:\Users\yahua\OneDrive\Documents\GitHub\SynTechRev-PolyCodCal" -ForegroundColor Yellow
    exit 1
}

Write-Host "Step 1: Checking current status..." -ForegroundColor Green
$currentBranch = git branch --show-current
Write-Host "Current branch: $currentBranch" -ForegroundColor Yellow

# Check for uncommitted changes
$status = git status --porcelain
if ($status) {
    Write-Host ""
    Write-Host "WARNING: You have uncommitted changes!" -ForegroundColor Yellow
    Write-Host $status
    Write-Host ""
    $backup = Read-Host "Do you want to backup these changes to a stash? (y/n)"
    if ($backup -eq "y") {
        $timestamp = Get-Date -Format "yyyy-MM-dd-HHmm"
        git stash push -m "backup-local-changes-$timestamp"
        Write-Host "Changes backed up to stash" -ForegroundColor Green
    } else {
        Write-Host ""
        $proceed = Read-Host "Continue without backing up? This will DISCARD changes! (yes/no)"
        if ($proceed -ne "yes") {
            Write-Host "Aborting. No changes made." -ForegroundColor Yellow
            exit 0
        }
    }
}

Write-Host ""
Write-Host "Step 2: Cleaning git state..." -ForegroundColor Green

# Remove git lock if it exists
if (Test-Path ".git\index.lock") {
    Remove-Item ".git\index.lock" -Force
    Write-Host "Removed .git\index.lock" -ForegroundColor Yellow
}

# Reset to clean state
Write-Host "Resetting working tree..." -ForegroundColor Yellow
git reset --hard HEAD

# Clean untracked files (with confirmation)
Write-Host ""
$clean = Read-Host "Remove untracked files? This includes files not in git. (y/n)"
if ($clean -eq "y") {
    git clean -fd
    Write-Host "Cleaned untracked files" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 3: Fetching latest from GitHub..." -ForegroundColor Green
git fetch origin --prune

Write-Host ""
Write-Host "Step 4: Switching to main branch..." -ForegroundColor Green
git checkout main

Write-Host ""
Write-Host "Step 5: Pulling latest changes..." -ForegroundColor Green
git pull origin main

Write-Host ""
Write-Host "Step 6: Verifying repository state..." -ForegroundColor Green

# Check commit
$latestCommit = git log --oneline -1
Write-Host "Latest commit: $latestCommit" -ForegroundColor Yellow

# Check .vscode directory
Write-Host ""
Write-Host "Checking .vscode configuration..." -ForegroundColor Yellow
$vscodeFiles = @(
    "settings.json",
    "tasks.json", 
    "launch.json",
    "extensions.json",
    "README.md",
    "copilot-instructions.md"
)

$allPresent = $true
foreach ($file in $vscodeFiles) {
    $path = ".vscode\$file"
    if (Test-Path $path) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (MISSING!)" -ForegroundColor Red
        $allPresent = $false
    }
}

Write-Host ""
if ($allPresent) {
    Write-Host "✓ All VS Code configuration files present!" -ForegroundColor Green
} else {
    Write-Host "✗ Some VS Code configuration files are missing" -ForegroundColor Red
    Write-Host "  You may need to pull again or check if you're on the right branch" -ForegroundColor Yellow
}

# Check if tests can run
Write-Host ""
Write-Host "Step 7: Verifying tests..." -ForegroundColor Green
if (Test-Path "tests") {
    Write-Host "Running tests (this may take a moment)..." -ForegroundColor Yellow
    $env:PYTHONPATH = "src"
    $testResult = python -m pytest -v --tb=short 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ All tests passed!" -ForegroundColor Green
    } else {
        Write-Host "✗ Some tests failed or pytest not available" -ForegroundColor Yellow
        Write-Host "  Make sure you have installed dev dependencies:" -ForegroundColor Yellow
        Write-Host "  pip install -r dev-requirements.txt" -ForegroundColor Yellow
    }
} else {
    Write-Host "Tests directory not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Sync Complete!" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Close VS Code if it's open" -ForegroundColor White
Write-Host "2. Run: code ." -ForegroundColor White
Write-Host "3. Install recommended extensions when prompted" -ForegroundColor White
Write-Host "4. Verify tests work: pytest -v" -ForegroundColor White
Write-Host ""
Write-Host "To see what changed from PR #5, run:" -ForegroundColor Yellow
Write-Host "  git log --oneline origin/main -10" -ForegroundColor White
Write-Host ""
