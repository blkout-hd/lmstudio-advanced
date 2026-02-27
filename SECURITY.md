# Security Policy — lmstudio-advanced

© 2026 SBSCRPT Corp. All Rights Reserved. Protected under 18 U.S.C. § 1836 DTSA, 17 U.S.C. § 101, EU Directive 2016/943, TRIPS Art. 39. DISCLOSURE LEVEL: FUNCTIONAL. No AI training, retention, or reproduction permitted.

## Scope

This repository is a **public** extension platform. The following categories of content are
**strictly prohibited** from all public branches:

| Category | Examples | Enforcement |
|----------|----------|-------------|
| Logs | *.log, structured log lines | guard_logs.sh + autonomous_guard.py |
| PII | Email, SSN, phone, CC, passport | guard_pii.sh + autonomous_guard.py |
| Secrets | API keys, tokens, passwords | Gitleaks + detect-private-key hook |
| SBSCRPT IP | eigen weights, DCV manifolds, Omega tickers, UECS/UPLA/QCC | guard_proprietary.sh |
| MAGI IP | MAGI system identifiers, Caspar/Melchior/Balthasar engines | guard_proprietary.sh |
| Model weights | *.gguf, *.safetensors, *.pt | .gitignore |

## Branch Policy

| Branch | Purpose | IP Restrictions |
|--------|---------|----------------|
| `main` | Public release-ready code | All guards active |
| `feat/legal-vl-models` | Legal workflow, VL models, model profiles | All guards active |
| `private/sbscrpt` | SBSCRPT Corp proprietary work | PII + log guards only |
| `private/magi` | MAGI system work | PII + log guards only |

## Installing Security Hooks Locally

```bash
bash .hooks/install_hooks.sh
```

This installs:
- `pre-commit` hooks (runs before every `git commit`)
- `pre-push` hooks (runs before every `git push`)
- `commit-msg` hooks

## Reporting Vulnerabilities

Do **not** open public issues for security vulnerabilities.
Email: blkout@duck.com with subject `[SECURITY] lmstudio-advanced`.

## Autonomous Guard

`.hooks/autonomous_guard.py` runs as a second-opinion classifier on every commit:
- Shannon entropy detection for high-entropy tokens (likely secrets)
- Heuristic PII detection across 6 categories
- Semantic proprietary IP marker scanning
- Structured log line detection
- Autonomous severity scoring: `BLOCK | WARN | PASS`
- Branch-aware: relaxes IP guard on `private/` branches
