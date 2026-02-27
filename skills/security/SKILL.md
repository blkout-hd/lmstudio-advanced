# Security Audit

> Skill for repository and code security auditing.
> Custom skill for lmstudio-advanced.

## When to Use

Use this skill when:
- Running pre-push security audits beyond pre-commit hooks
- Auditing dependencies for CVEs (npm audit, pip-audit)
- Scanning for hardcoded secrets missed by Gitleaks
- Reviewing plugin sandbox configurations for over-permissioned network access
- Generating SBOM (Software Bill of Materials) for releases

## Tools Used

- `gitleaks` — secret scanning
- `npm audit` / `pip-audit` — dependency CVEs
- `semgrep` — static analysis
- `.hooks/autonomous_guard.py` — PII + IP scanner
- `trivy` — container/image scanning
