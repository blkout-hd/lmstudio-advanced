#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# guard_proprietary.sh — Block proprietary SBSCRPT/MAGI IP
# from being committed to public-facing branches.
#
# Scans for:
#   - SBSCRPT internal API patterns
#   - MAGI-specific identifiers and class names
#   - Eigen-weighted variable patterns (UECS, DCV, Omega)
#   - SBSCRPT Corp copyright with non-functional disclosure
# ─────────────────────────────────────────────────────────
set -euo pipefail

# Determine current branch
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "detached")

# Only enforce on public-facing branches
PUBLIC_BRANCHES=("main" "feat/legal-vl-models" "develop" "release")
IS_PUBLIC=0
for branch in "${PUBLIC_BRANCHES[@]}"; do
  [[ "$CURRENT_BRANCH" == "$branch" ]] && { IS_PUBLIC=1; break; }
done

# Private branches bypass this guard (they're allowed to have proprietary code)
if [[ $IS_PUBLIC -eq 0 ]]; then
  exit 0
fi

FAILED=0

for file in "$@"; do
  if ! file "$file" | grep -qE '(text|ASCII|UTF)'; then
    continue
  fi

  MATCH=""

  # SBSCRPT core IP patterns
  if grep -qiP '(?:SBSCRPT(?:_| )Corp|sbscrpt_core|SbscrptClient|sbscrpt\.internal|eigen_weight|dcv_manifold|omega_ticker|UECS|UPLA|QCC)' "$file" 2>/dev/null; then
    MATCH="SBSCRPT proprietary identifier"
  fi

  # MAGI system patterns
  if grep -qiP '(?:MAGI(?:_| )system|magi_core|MAGIOrchestrator|MagiKernel|magi\.internal|CasparEngine|MelchiorEngine|BalthasarEngine)' "$file" 2>/dev/null; then
    MATCH="MAGI proprietary identifier"
  fi

  # Universal Opportunity Ranking / SBSCRPT algorithmic IP
  if grep -qiP '(?:UniversalOppRank|OpportunityScorer|eigenWeightedVar|DcvManifold|OmegaDirection)' "$file" 2>/dev/null; then
    MATCH="SBSCRPT algorithmic IP (opportunity ranking system)"
  fi

  if [[ -n "$MATCH" ]]; then
    echo "❌ [IP GUARD] $MATCH detected in: $file"
    echo "   This content belongs on private/sbscrpt or private/magi branches only."
    FAILED=1
  fi
done

[[ $FAILED -eq 0 ]] || { echo "\n❌ Commit blocked by PROPRIETARY IP GUARD."; exit 1; }
exit 0
