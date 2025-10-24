# License Compliance

## Project License

SynTechRev-PolyCodCal is licensed under the **MIT License**, an OSI-approved open source license.

The full license text is available in the [LICENSE](LICENSE) file in the repository root.

### MIT License Summary

The MIT License is a permissive license that allows:

- ✅ **Commercial use**: Use the software for commercial purposes
- ✅ **Modification**: Modify the software
- ✅ **Distribution**: Distribute the software
- ✅ **Private use**: Use the software privately

**Requirements**:
- Include the original license and copyright notice in distributions
- No warranty is provided

**Limitations**:
- The software is provided "as is" without warranty
- Authors are not liable for any damages

## Dependency Licenses

All dependencies used by SynTechRev-PolyCodCal must be compatible with the MIT License and approved by the Open Source Initiative (OSI).

### Checking Dependency Licenses

We use `pip-licenses` to audit and verify dependency licenses:

```bash
# Install pip-licenses
pip install pip-licenses

# List all dependency licenses
pip-licenses

# Check for GPL or other restricted licenses
pip-licenses --format=markdown --with-urls

# Generate a detailed license report
pip-licenses --format=json --with-urls --output-file=licenses.json
```

### Approved License Types

The following OSI-approved licenses are compatible with MIT and allowed for dependencies:

- **MIT License**: Permissive, simple, widely used
- **Apache License 2.0**: Permissive with patent grants
- **BSD Licenses (2-Clause, 3-Clause)**: Permissive, simple
- **ISC License**: Functionally equivalent to MIT
- **Python Software Foundation License**: For Python standard library
- **Mozilla Public License 2.0 (MPL-2.0)**: Weak copyleft, file-level

### Restricted Licenses

The following licenses are **NOT allowed** for dependencies without special approval:

- ❌ **GPL (v2, v3)**: Strong copyleft, requires derivative works to be GPL
- ❌ **AGPL**: Strong copyleft with network use trigger
- ❌ **LGPL**: Weak copyleft, complicates distribution
- ⚠️ **Creative Commons Non-Commercial**: Restricts commercial use
- ⚠️ **Proprietary/Custom licenses**: Require case-by-case review

If a dependency with a restricted license is necessary, open an issue for discussion.

## Current Dependencies

As of version 0.2.1, our main dependencies and their licenses are:

| Package | License | OSI Approved |
|---------|---------|--------------|
| certifi | MPL-2.0 | ✅ |
| charset-normalizer | MIT | ✅ |
| idna | BSD-3-Clause | ✅ |
| numpy | BSD-3-Clause | ✅ |
| pandas | BSD-3-Clause | ✅ |
| python-dateutil | Apache-2.0, BSD | ✅ |
| pytz | MIT | ✅ |
| requests | Apache-2.0 | ✅ |
| six | MIT | ✅ |
| tzdata | Apache-2.0 | ✅ |
| urllib3 | MIT | ✅ |

All dependencies use OSI-approved licenses compatible with MIT.

## Adding New Dependencies

Before adding a new dependency, maintainers must:

1. **Check the License**:
   ```bash
   # After adding to pyproject.toml or requirements.txt
   pip install <package>
   pip-licenses | grep <package>
   ```

2. **Verify OSI Approval**:
   - Check [opensource.org/licenses](https://opensource.org/licenses) for OSI approval
   - Ensure compatibility with MIT License

3. **Document the Decision**:
   - Update this file if adding a new license type
   - Document in PR description why the dependency is necessary
   - Note any license-related considerations

4. **Automated Checks**:
   - Dependabot will monitor for license changes in dependencies
   - CodeQL and other security tools help identify licensing issues

## License Headers

Source files in this project do not require license headers. The LICENSE file in the repository root applies to all source code unless otherwise noted.

For clarity, you may add a header to new files:

```python
# This file is part of SynTechRev-PolyCodCal
# Licensed under the MIT License
# See LICENSE file in the project root
```

## Third-Party Code

If you incorporate third-party code:

1. **Ensure License Compatibility**: The code must use an MIT-compatible license
2. **Preserve Attribution**: Keep original copyright and license notices
3. **Document Clearly**: Note the source and license in comments
4. **Update This Document**: Add an entry below if substantial

### Third-Party Components

*None currently. Any third-party code incorporated will be listed here.*

## Contributor Agreement

By contributing to SynTechRev-PolyCodCal, you agree that:

1. Your contributions are your original work or properly attributed
2. You have the right to submit the work under the MIT License
3. You grant the project maintainers a perpetual, worldwide, non-exclusive, royalty-free license to use, modify, and distribute your contributions under the MIT License

No formal Contributor License Agreement (CLA) is required beyond the terms of the MIT License.

## License Compliance Workflow

Our automated workflows help maintain license compliance:

1. **Dependabot**: Monitors dependency updates and alerts on license changes
2. **CodeQL**: Scans for security and licensing issues
3. **Pre-commit Hooks**: Ensure code quality and catch obvious issues

## Questions and Concerns

If you have questions about licensing or discover a licensing issue:

- **General Questions**: Open a [GitHub Discussion](https://github.com/SynTechRev/SynTechRev-PolyCodCal/discussions)
- **License Violations**: Report privately via email to `you@example.com`
- **New Dependency Review**: Open an issue tagged with `dependencies` and `licensing`

## Resources

- [MIT License Full Text](LICENSE)
- [Open Source Initiative (OSI)](https://opensource.org/)
- [OSI Approved Licenses](https://opensource.org/licenses)
- [Choose a License](https://choosealicense.com/)
- [pip-licenses Documentation](https://github.com/raimon49/pip-licenses)
- [SPDX License List](https://spdx.org/licenses/)

---

**Last Updated**: 2025-10-18
