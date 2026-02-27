#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# guard_branch.sh — Prevent private/ branch file paths
# from being committed to public branches.
#
# Also prevents committing directly to main without a PR
# (warns but does not hard-block — CI enforces merge policy).
# ─────────────────────────────────────────────────────────
set -euo pipefail

CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "detached")
FAILED=0

# Warn on direct push to main
if [[ "$CURRENT_BRANCH" == "main" ]]; then
  echo "⚠️  [BRANCH GUARD] Direct commit to 'main'. Prefer feature branches + PRs."
  # Not hard-blocking here; branch protection rules on GitHub enforce this.
fi

# Block private/ path tokens from leaking to public branches
PUBLIC_BRANCHES=("main" "feat/legal-vl-models" "develop" "release")
IS_PUBLIC=0
for branch in "${PUBLIC_BRANCHES[@]}"; do
  [[ "$CURRENT_BRANCH" == "$branch" ]] && { IS_PUBLIC=1; break; }
done

if [[ $IS_PUBLIC -eq 1 ]]; then
  # Check staged files for paths that belong on private branches
  while IFS= read -r staged_file; do
    if [[ "$staged_file" =~ ^(private/|sbscrpt_core/|magi_core/|\.sbscrpt/|\.magi/) ]]; then
      echo "❌ [BRANCH GUARD] Staged file '$staged_file' belongs on a private branch."
      FAILED=1
    fi
  done < <(git diff --cached --name-only 2>/dev/null)
fi

[[ $FAILED -eq 0 ]] || { echo "\n❌ Commit blocked by BRANCH GUARD."; exit 1; }
exit 0
