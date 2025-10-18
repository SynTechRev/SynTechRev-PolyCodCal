```markdown
# Security Policy — SynTechRev-PolyCodCal

## Reporting Vulnerabilities
If you discover a vulnerability, please do NOT open a public issue. Instead report privately using one of these options:

- Email: security@syntechrev.org (PGP available — see below)
- GitHub: Create a private GitHub Security Advisory in this repository (recommended)
- If you need to send encrypted details, use our PGP key: <paste-or-link-your-armor-here>

When reporting, please include:
- A short summary of the issue and potential impact
- Steps to reproduce (fully automated PoC if available)
- Affected versions and environment details (Python, OS, dependency versions)
- Any PoC code or test data necessary to reproduce

## Response and Remediation Timeline
- Acknowledgement: within 72 hours of receipt.
- Initial triage and severity classification: within 7 days.
- Target remediation: within 14 days for high/critical issues where feasible, with regular updates for longer fixes.
- If a CVE should be requested, we will coordinate assignment and disclosure timing.

## Coordinated Disclosure
We follow coordinated disclosure to allow time to prepare fixes before public disclosure. We will:
- Work with the reporter to agree disclosure timing.
- Notify affected users via release notes and security advisories.
- Provide attribution in an ACKNOWLEDGMENTS file unless the reporter requests anonymity.

## Supported Versions
| Version | Supported |
|--------:|:---------:|
| 0.2.x   | ✅        |
| < 0.2.0 | ❌        |

If you report an issue on an unsupported version, we may ask you to reproduce on a supported release.

## Security Tooling & Practices
- Code scanning: GitHub CodeQL (scheduled + PR scans)
- Dependency monitoring: Dependabot (automated PRs for dependency updates)
- CI signature & verification: release artifacts validated in CI
- License & dependency compliance checks via pip-licenses in CI

## How we handle sensitive data
Do not include secrets, passwords, or private keys in reports. If you need to share sensitive data, use encrypted email (PGP) or the private GitHub Security Advisory.

## Contact & Acknowledgements
- Email: security@syntechrev.org
- For legal or escalation matters: governance@syntechrev.org

We acknowledge security researchers who responsibly disclose issues. See ACKNOWLEDGMENTS.md for names (if provided).

```
