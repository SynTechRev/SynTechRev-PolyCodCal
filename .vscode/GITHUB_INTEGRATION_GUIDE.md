# GitHub Integration Guide for VS Code

This guide helps you set up GitHub authentication in VS Code for the SynTechRev-PolyCodCal repository.

## Overview

To work effectively with GitHub PRs, commits, and branches in VS Code, you need to authenticate your GitHub account. This guide provides two methods to accomplish this.

---

## ✅ Option 1: GitHub Personal Access Token (PAT) - Recommended

This is the most reliable method and gives you full control over permissions.

### Step 1: Generate a Personal Access Token (PAT)

1. **Go to GitHub Settings**
   - Navigate to: [https://github.com/settings/tokens](https://github.com/settings/tokens)
   - Or: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token**
   - Click **"Generate new token"** → **"Generate new token (classic)"**
   - Give it a descriptive name: e.g., "VS Code - SynTechRev-PolyCodCal"

3. **Select Scopes (Minimum Required)**
   - ✅ `repo` - Full control of private repositories
   - ✅ `workflow` - Update GitHub Actions workflows (if working with CI/CD)
   - ✅ `write:packages` - Upload packages to GitHub Package Registry (optional)
   - ✅ `read:packages` - Download packages from GitHub Package Registry (optional)

4. **Generate and Copy Token**
   - Click **"Generate token"** at the bottom
   - ⚠️ **IMPORTANT**: Copy the token immediately - you won't see it again!
   - Store it securely (password manager recommended)

### Step 2: Configure VS Code with PAT

1. **Open Command Palette**
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Or press `F1`

2. **Sign in with Token**
   - Type: `GitHub: Sign in using a token`
   - Select the command
   - Paste your PAT when prompted
   - Press Enter

3. **Verify Authentication**
   - Look for GitHub icon in the Activity Bar (left sidebar)
   - Check status bar (bottom) for GitHub account name
   - Try accessing GitHub features (Pull Requests, Issues)

### Step 3: Verify Repository Sync

1. **Check Git Integration**
   - Open Source Control view (`Ctrl+Shift+G`)
   - Verify you can see current branch: `copilot/add-personal-access-token-support`
   - Check that remote is properly configured

2. **Verify Pull Request Access**
   - If GitHub Pull Requests extension is installed
   - Check Pull Requests view in Activity Bar
   - You should see active PRs for the repository

3. **Test Operations**
   ```bash
   # In VS Code integrated terminal (Ctrl+`)
   git fetch --all
   git status
   ```

---

## Option 2: GitHub OAuth (Browser-based Sign-in)

This method uses browser-based authentication.

### Steps:

1. **Open Command Palette**
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)

2. **Sign in to GitHub**
   - Type: `GitHub: Sign in`
   - Select the command

3. **Authorize in Browser**
   - Browser will open with GitHub authorization page
   - Click **"Authorize Visual-Studio-Code"**
   - May require 2FA if enabled

4. **Return to VS Code**
   - VS Code should now be authenticated
   - Check status bar for confirmation

### Note on OAuth Issues

If you encounter OAuth registration issues (e.g., "OAuth application not registered"), use **Option 1 (PAT)** instead, as it's more reliable and doesn't depend on dynamic OAuth registration.

---

## Verifying GitHub Integration Works

After authentication, verify these features work:

### ✅ Git Operations
- [ ] Can fetch from remote: `git fetch`
- [ ] Can pull changes: `git pull`
- [ ] Can push changes: `git push`
- [ ] Can see commit history
- [ ] Can create/switch branches

### ✅ GitHub Features (if extensions installed)
- [ ] Can view Pull Requests
- [ ] Can comment on PRs
- [ ] Can view Issues
- [ ] Can see GitHub Actions status
- [ ] Can view code reviews

### ✅ VS Code Integration
- [ ] GitHub account shown in status bar
- [ ] Source Control view shows repository
- [ ] Remote branches visible
- [ ] Commit history accessible

---

## Troubleshooting

### Problem: Token Authentication Failed

**Solution:**
1. Verify token has correct scopes (`repo`, `workflow`)
2. Check token hasn't expired
3. Try regenerating a new token
4. Ensure you copied the token correctly (no extra spaces)

### Problem: Can't See Pull Requests

**Solution:**
1. Install **GitHub Pull Requests and Issues** extension
2. Reload VS Code window (`Ctrl+Shift+P` → "Developer: Reload Window")
3. Verify token has `repo` scope
4. Check you're authenticated (status bar shows GitHub account)

### Problem: Git Operations Require Credentials

**Solution:**
1. Configure Git to use credential helper:
   ```bash
   git config --global credential.helper store
   ```
2. Or use SSH instead of HTTPS:
   ```bash
   git remote set-url origin git@github.com:SynTechRev/SynTechRev-PolyCodCal.git
   ```

### Problem: OAuth "Not Registered" Error

**Solution:**
- Use **Option 1 (PAT)** instead of OAuth
- PAT is more reliable and doesn't require OAuth app registration

---

## Security Best Practices

### ✅ DO:
- Store PAT in a secure password manager
- Use minimum required scopes
- Set expiration date for tokens
- Revoke tokens when no longer needed
- Use different tokens for different machines/projects

### ❌ DON'T:
- Share your PAT with anyone
- Commit PAT to version control
- Use tokens with more permissions than needed
- Leave tokens without expiration dates
- Reuse the same token across many applications

---

## Additional GitHub Extensions for VS Code

Enhance your GitHub workflow with these recommended extensions:

### Core Extensions (Recommended)
- **GitHub Pull Requests and Issues** (`GitHub.vscode-pull-request-github`)
  - View and manage PRs and Issues
  - Comment and review code
  - Create PRs directly from VS Code

- **GitLens** (`eamodio.gitlens`)
  - Enhanced Git integration
  - Inline blame annotations
  - Rich commit history
  - Branch comparison

### Optional Extensions
- **GitHub Actions** (`github.vscode-github-actions`)
  - View workflow runs
  - Monitor CI/CD status
  - Debug workflow files

- **GitHub Copilot** (`GitHub.copilot`) - If you have access
  - AI-powered code suggestions
  - Code completion
  - Documentation generation

---

## Workspace Configuration

This repository includes pre-configured VS Code settings in `.vscode/`:

### Files:
- `settings.json` - Workspace settings (Python, linters, formatters)
- `launch.json` - Debug configurations
- `tasks.json` - Build and test tasks
- `extensions.json` - Recommended extensions

### To Install All Recommended Extensions:
1. Open Command Palette (`Ctrl+Shift+P`)
2. Type: `Extensions: Show Recommended Extensions`
3. Click **"Install All"**

---

## Next Steps

After setting up GitHub authentication:

1. **Sync Repository**
   ```bash
   git fetch --all
   git pull
   ```

2. **Verify Development Environment**
   - Run tests: `pytest -v`
   - Run linters: `ruff check .`
   - Run formatter: `black src tests scripts`

3. **Review Documentation**
   - [QUICKSTART.md](../QUICKSTART.md) - 5-minute setup guide
   - [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
   - [.vscode/README.md](README.md) - VS Code specific guide

4. **Start Developing**
   - Create a feature branch
   - Make your changes
   - Run quality checks (`Ctrl+Shift+B`)
   - Commit and push
   - Create a Pull Request

---

## Support

### For GitHub Authentication Issues:
- [GitHub Personal Access Tokens Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [VS Code GitHub Extension Docs](https://code.visualstudio.com/docs/sourcecontrol/github)

### For Repository Issues:
- See [CONTRIBUTING.md](../CONTRIBUTING.md)
- Check [.vscode/README.md](README.md) for VS Code specific issues
- Open an issue on GitHub

---

## Summary Checklist

Use this checklist to verify your setup:

- [ ] Generated GitHub Personal Access Token with correct scopes
- [ ] Authenticated VS Code with GitHub (PAT or OAuth)
- [ ] GitHub account visible in VS Code status bar
- [ ] Can fetch/pull/push to repository
- [ ] Git operations work without credential prompts
- [ ] Can view repository branches and commits
- [ ] Recommended VS Code extensions installed
- [ ] Development environment verified (tests pass, linters work)
- [ ] Pre-commit hooks installed
- [ ] No outstanding merge conflicts
- [ ] Working directory clean (or only expected changes)

---

**Last Updated:** 2025-01-08  
**Repository:** SynTechRev/SynTechRev-PolyCodCal
