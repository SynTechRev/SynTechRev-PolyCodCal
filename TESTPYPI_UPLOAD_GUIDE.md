# TestPyPI Upload Guide - Version 0.2.1

**Quick Reference for TestPyPI Publication**

---

## Pre-Upload Verification ✅

All quality gates PASS:
- ✅ Package builds: `syntechrev-polycodcal-0.2.1.tar.gz` + wheel
- ✅ Tests: 51/51 passing
- ✅ Linting: Ruff passed
- ✅ Formatting: Black passed
- ✅ Type checking: mypy passed
- ✅ Metadata: twine check passed

---

## Upload Methods

### Method 1: Automated (Tag-Based) ⭐ RECOMMENDED

**Prerequisites:**
- `TEST_PYPI_API_TOKEN` secret configured in repository settings

**Steps:**
```bash
# 1. Checkout main and pull latest
git checkout main
git pull origin main

# 2. Create annotated tag
git tag -a v0.2.1 -m "Release version 0.2.1 - Phase 7 complete

✅ All Phase 7 objectives achieved
✅ Package metadata PEP 621 compliant
✅ Console scripts configured (3 entry points)
✅ Release workflow with version guard
✅ Documentation builds successfully
✅ All quality checks passing (51/51 tests)

Ready for TestPyPI publication and Phase 8."

# 3. Push tag (triggers release workflow)
git push origin v0.2.1

# 4. Monitor workflow
# Go to: https://github.com/SynTechRev/SynTechRev-PolyCodCal/actions
# Watch: Release workflow execution
```

**What the Workflow Does:**
1. ✅ Validates version matches tag (v0.2.1 → 0.2.1)
2. ✅ Cleans previous build artifacts
3. ✅ Builds sdist and wheel with `--no-isolation`
4. ✅ Uploads to TestPyPI with `--skip-existing`
5. ✅ Verifies installation in clean environment
6. ✅ Tests console script entry points

---

### Method 2: Manual Workflow Trigger

**When to Use:** Testing workflow without creating a tag

**Prerequisites:**
- Tag must exist (create tag first, don't push)
- Or use existing tag

**Steps:**
1. Go to: GitHub → Actions → Release workflow
2. Click "Run workflow" dropdown
3. Select branch: Choose tag `v0.2.1`
4. Click green "Run workflow" button
5. Monitor execution in Actions tab

**Note:** Jobs are gated to tags starting with `v`, so this must be run on a tag reference.

---

### Method 3: Manual Upload (Local)

**When to Use:** Direct upload from local machine for testing

**Prerequisites:**
- TestPyPI account: https://test.pypi.org/account/register/
- API token: https://test.pypi.org/manage/account/token/

**Steps:**
```bash
# 1. Clean previous builds
rm -rf dist/ build/ *.egg-info

# 2. Build package
python -m build --no-isolation

# 3. Check package
python -m twine check dist/*

# 4. Upload to TestPyPI
python -m twine upload \
  --repository-url https://test.pypi.org/legacy/ \
  --skip-existing \
  --verbose \
  -u __token__ \
  -p <your-test-pypi-token> \
  dist/*
```

**Expected Output:**
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading syntechrev_polycodcal-0.2.1-py3-none-any.whl
Uploading syntechrev-polycodcal-0.2.1.tar.gz
View at:
https://test.pypi.org/project/syntechrev-polycodcal/0.2.1/
```

---

## Post-Upload Verification

### 1. Check TestPyPI Page

**URL:** https://test.pypi.org/project/syntechrev-polycodcal/

**Verify:**
- ✅ Version 0.2.1 appears
- ✅ Description renders correctly (from README.md)
- ✅ Metadata shows correct dependencies
- ✅ Console scripts listed in Project details
- ✅ Download files available (wheel + sdist)

### 2. Test Installation

**Create Clean Environment:**
```bash
# Use Python 3.12 (recommended for Windows due to NumPy 3.13 issue)
python3.12 -m venv testpypi-verify
source testpypi-verify/bin/activate  # Windows: testpypi-verify\Scripts\activate
```

**Install from TestPyPI:**
```bash
# Install with fallback to PyPI for dependencies
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    syntechrev-polycodcal==0.2.1
```

**Expected Output:**
```
Collecting syntechrev-polycodcal==0.2.1
  Downloading https://test-files.pythonhosted.org/...
Collecting certifi>=2025.10.5
  Using cached https://files.pythonhosted.org/...
[... other dependencies ...]
Successfully installed syntechrev-polycodcal-0.2.1 [... dependencies ...]
```

### 3. Verify Console Scripts

**Test Each Entry Point:**
```bash
# Test syntech-monitor
syntech-monitor --help
# Expected: Help text for feedback monitor CLI

# Test genesis-gateway
genesis-gateway --help
# Expected: Help text for genesis gateway CLI

# Test legal-generator
legal-generator --help
# Expected: Help text for legal generator CLI
```

### 4. Verify Package Import

**Test Python Import:**
```bash
python -c "import syntechrev_polycodcal; print('✅ Import successful')"
python -c "from syntechrev_polycodcal import FeedbackMonitor; print('✅ FeedbackMonitor import successful')"
```

### 5. Run Smoke Tests

**Test Basic Functionality:**
```bash
# Create test events file
cat > /tmp/test_events.jsonl << 'EOF'
{"timestamp": "2024-01-01T10:00:00Z", "outcome": "success"}
{"timestamp": "2024-01-01T10:00:01Z", "outcome": "success"}
{"timestamp": "2024-01-01T10:00:02Z", "outcome": "failure"}
{"timestamp": "2024-01-01T10:00:03Z", "outcome": "success"}
{"timestamp": "2024-01-01T10:00:04Z", "outcome": "failure"}
EOF

# Run syntech-monitor
syntech-monitor /tmp/test_events.jsonl
# Expected: Processes events, may generate alerts depending on thresholds
```

**Cleanup:**
```bash
deactivate
rm -rf testpypi-verify
```

---

## Troubleshooting

### Issue: Version Already Exists

**Error:** `File already exists`

**Cause:** Version 0.2.1 already uploaded to TestPyPI

**Solutions:**
1. Use `--skip-existing` flag (already in workflow)
2. Bump version to 0.2.2 if you need to re-upload
3. Delete from TestPyPI (if you have permissions)

---

### Issue: Dependencies Not Found

**Error:** `Could not find a version that satisfies the requirement`

**Cause:** TestPyPI doesn't have all dependencies

**Solution:** Use `--extra-index-url`:
```bash
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    syntechrev-polycodcal==0.2.1
```

---

### Issue: NumPy DLL Error (Windows Python 3.13)

**Error:** `DLL load failed while importing _multiarray_umath`

**Cause:** Known NumPy 2.3.3+ issue on Windows Python 3.13

**Solution:** Use Python 3.12:
```bash
py -3.12 -m venv testpypi-verify
testpypi-verify\Scripts\activate
pip install ...
```

---

### Issue: Console Scripts Not Found

**Error:** `syntech-monitor: command not found`

**Cause:** Scripts not in PATH or installation incomplete

**Solutions:**
1. Check installation: `pip show syntechrev-polycodcal`
2. Verify entry points: `pip show -f syntechrev-polycodcal | grep console_scripts`
3. Use full path: `python -m syntechrev_polycodcal.feedback_monitor`
4. Reinstall: `pip install --force-reinstall syntechrev-polycodcal==0.2.1`

---

## Success Criteria

Upload is successful when:
- ✅ Package appears at https://test.pypi.org/project/syntechrev-polycodcal/0.2.1/
- ✅ Installation completes without errors
- ✅ All 3 console scripts run and show help text
- ✅ Python imports work (`import syntechrev_polycodcal`)
- ✅ Basic smoke test passes (process events file)

---

## Next Steps After Successful Upload

1. **Document Success**
   - Update CHANGELOG.md with TestPyPI link
   - Add TestPyPI badge to README.md
   - Take screenshots of TestPyPI page

2. **Monitor Early Usage**
   - Watch for installation issues
   - Check TestPyPI download stats
   - Respond to any user reports

3. **Plan PyPI Upload**
   - After TestPyPI validation (1-2 days)
   - Same process with PyPI token
   - Tag: v0.2.1 (or create new stable release)

4. **Begin Phase 8**
   - Security documentation (SECURITY.md)
   - Community guidelines (CODE_OF_CONDUCT.md)
   - Issue/PR templates
   - Dependabot configuration
   - CodeQL scanning

---

## Reference Links

- **TestPyPI Project:** https://test.pypi.org/project/syntechrev-polycodcal/
- **PyPI Packaging Guide:** https://packaging.python.org/en/latest/tutorials/packaging-projects/
- **PEP 440 (Versioning):** https://peps.python.org/pep-0440/
- **Twine Documentation:** https://twine.readthedocs.io/
- **GitHub Release Workflow:** `.github/workflows/release.yml`

---

## Quick Command Reference

```bash
# Build package
python -m build --no-isolation

# Check package
python -m twine check dist/*

# Upload to TestPyPI
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    syntechrev-polycodcal==0.2.1

# Test console scripts
syntech-monitor --help
genesis-gateway --help
legal-generator --help

# Test import
python -c "import syntechrev_polycodcal; print('Success')"
```

---

**Last Updated:** 2025-10-18  
**Version:** 0.2.1  
**Status:** Ready for Upload ✅
