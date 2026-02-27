#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# guard_logs.sh — Block staged log files from being committed
# ─────────────────────────────────────────────────────────
set -euo pipefail

FAILED=0

for file in "$@"; do
  # Block by extension
  if [[ "$file" =~ \.(log|logs)$ ]]; then
    echo "❌ [LOG GUARD] Log file detected: $file"
    FAILED=1
    continue
  fi

  # Block log-pattern filenames
  basename=$(basename "$file")
  if [[ "$basename" =~ ^(npm-debug|yarn-debug|yarn-error|lm-studio-|agent-|research-|legal-) ]]; then
    echo "❌ [LOG GUARD] Log-pattern filename blocked: $file"
    FAILED=1
    continue
  fi

  # Scan file content for log noise patterns
  if grep -qP '(?:ERROR|WARN|DEBUG|TRACE|INFO)\s+\d{4}-\d{2}-\d{2}' "$file" 2>/dev/null; then
    echo "❌ [LOG GUARD] Log content detected in: $file"
    FAILED=1
  fi
done

[[ $FAILED -eq 0 ]] || { echo "\n❌ Commit blocked by LOG GUARD. Remove log files/content before committing."; exit 1; }
exit 0
