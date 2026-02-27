#!/usr/bin/env python3
"""
autonomous_guard.py — lmstudio-advanced

Autonomous pre-commit risk classifier.
Runs after shell guards as a second-opinion classifier.

Capabilities:
  - ML-pattern PII detection (regex + heuristic entropy scoring)
  - Semantic detection of proprietary IP marker phrases
  - Log noise scoring (high-entropy structured log line detection)
  - Autonomous severity scoring: BLOCK | WARN | PASS

© 2026 SBSCRPT Corp. All Rights Reserved.
Protected under 18 U.S.C. § 1836 DTSA, 17 U.S.C. § 101.
No AI training, retention, or reproduction permitted.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path
from typing import NamedTuple

# ── Risk levels ────────────────────────────────────────────────────────────────

PASS = "PASS"
WARN = "WARN"
BLOCK = "BLOCK"


class Finding(NamedTuple):
    severity: str   # BLOCK | WARN | PASS
    category: str
    detail: str
    line_no: int


# ── Pattern library ────────────────────────────────────────────────────────────

PII_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("email",       re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')),
    ("ssn",         re.compile(r'\b\d{3}-\d{2}-\d{4}\b')),
    ("phone-us",    re.compile(r'(?:\+1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]\d{4}')),
    ("credit-card", re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b')),
    ("passport-us", re.compile(r'\b[A-Z]{1,2}\d{6,9}\b')),
    ("ipv4-data",   re.compile(r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b')),
]

PROPRIETARY_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("sbscrpt-core",     re.compile(r'(?:SBSCRPT_Corp|sbscrpt_core|SbscrptClient|sbscrpt\.internal)', re.I)),
    ("magi-core",        re.compile(r'(?:MAGI_system|magi_core|MAGIOrchestrator|MagiKernel|magi\.internal|CasparEngine|MelchiorEngine|BalthasarEngine)', re.I)),
    ("eigen-weights",    re.compile(r'(?:eigenWeightedVar|eigen_weight|DcvManifold|dcv_manifold|OmegaDirection|omega_ticker)', re.I)),
    ("opp-rank-system",  re.compile(r'(?:UniversalOppRank|OpportunityScorer|UECS|UPLA|QCC)', re.I)),
]

LOG_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r'(?:ERROR|WARN(?:ING)?|DEBUG|TRACE|INFO)\s+\d{4}-\d{2}-\d{2}'),
    re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\s+(?:ERROR|WARN|DEBUG|INFO)'),
    re.compile(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]\s+(?:ERROR|WARN|DEBUG|INFO)'),
]

# Whitelisted files (mirrors .gitallowed)
ALLOWLIST: set[str] = {
    ".env.example",
    "tests/fixtures/dummy_token.txt",
    "tests/fixtures/fake_pii.json",
    ".hooks/guard_pii.sh",       # contains pattern strings, not real PII
    ".hooks/autonomous_guard.py",
    ".pre-commit-config.yaml",
}

# Private branch exemption
PRIVATE_BRANCH_PREFIXES = ("private/", "refs/heads/private/")


# ── Entropy helper ─────────────────────────────────────────────────────────────

def _shannon_entropy(text: str) -> float:
    """Shannon entropy of a string — high entropy = likely encoded secret."""
    if not text:
        return 0.0
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1
    n = len(text)
    return -sum((f / n) * math.log2(f / n) for f in freq.values())


HIGH_ENTROPY_PATTERN = re.compile(r'[A-Za-z0-9+/=_\-]{32,}')
ENTROPY_THRESHOLD = 4.5   # bits — typical random tokens exceed this


# ── Core scanner ───────────────────────────────────────────────────────────────

def scan_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []

    # Allowlist bypass
    for allowed in ALLOWLIST:
        if str(path).endswith(allowed) or path.name == Path(allowed).name:
            return []

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except (OSError, PermissionError) as exc:
        return [Finding(WARN, "io-error", str(exc), 0)]

    lines = content.splitlines()

    for lineno, line in enumerate(lines, start=1):
        # ── PII ──────────────────────────────────────────────────────────────
        for pii_name, pii_re in PII_PATTERNS:
            if pii_re.search(line):
                # Skip localhost/loopback for ipv4
                if pii_name == "ipv4-data" and re.search(r'127\.0\.0\.1|0\.0\.0\.0|localhost', line):
                    continue
                findings.append(Finding(BLOCK, f"pii:{pii_name}", f"Line {lineno}: {line.strip()[:80]}", lineno))

        # ── Proprietary IP ───────────────────────────────────────────────────
        for ip_name, ip_re in PROPRIETARY_PATTERNS:
            if ip_re.search(line):
                findings.append(Finding(BLOCK, f"ip:{ip_name}", f"Line {lineno}: {line.strip()[:80]}", lineno))

        # ── Log noise ────────────────────────────────────────────────────────
        for log_re in LOG_PATTERNS:
            if log_re.search(line):
                findings.append(Finding(BLOCK, "log:structured", f"Line {lineno}: {line.strip()[:80]}", lineno))
                break

        # ── High-entropy token detection (secrets) ───────────────────────────
        for token_match in HIGH_ENTROPY_PATTERN.finditer(line):
            token = token_match.group()
            if _shannon_entropy(token) >= ENTROPY_THRESHOLD:
                findings.append(Finding(BLOCK, "secret:high-entropy", f"Line {lineno}: token '{token[:20]}...' entropy={_shannon_entropy(token):.2f}", lineno))

    return findings


# ── Branch context ─────────────────────────────────────────────────────────────

def is_private_branch() -> bool:
    try:
        import subprocess
        result = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], capture_output=True, text=True, check=False)
        branch = result.stdout.strip()
        return branch.startswith("private/")
    except Exception:
        return False


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    files = [Path(f) for f in sys.argv[1:] if Path(f).is_file()]

    if is_private_branch():
        # On private branches, only enforce PII and logs — not IP guard
        skip_categories = {"ip:sbscrpt-core", "ip:magi-core", "ip:eigen-weights", "ip:opp-rank-system"}
    else:
        skip_categories: set[str] = set()

    all_findings: list[tuple[Path, Finding]] = []
    for file_path in files:
        for finding in scan_file(file_path):
            if finding.category not in skip_categories:
                all_findings.append((file_path, finding))

    if not all_findings:
        print("✅ [AUTONOMOUS GUARD] No issues detected.")
        sys.exit(0)

    blocks = [(p, f) for p, f in all_findings if f.severity == BLOCK]
    warns  = [(p, f) for p, f in all_findings if f.severity == WARN]

    for path, finding in warns:
        print(f"⚠️  [{finding.category}] {path}: {finding.detail}")

    for path, finding in blocks:
        print(f"❌ [{finding.category}] {path}: {finding.detail}")

    if blocks:
        print(f"\n❌ [AUTONOMOUS GUARD] Commit BLOCKED — {len(blocks)} issue(s) require resolution.")
        print("   Categories:", ", ".join(sorted({f.category for _, f in blocks})))
        print("   Add test files to .gitallowed if they contain intentional fixtures.")
        sys.exit(1)

    print(f"⚠️  [AUTONOMOUS GUARD] {len(warns)} warning(s). Commit proceeding — review recommended.")
    sys.exit(0)


if __name__ == "__main__":
    main()
