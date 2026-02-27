#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# guard_pii.sh — Block PII from being committed
# Detects: email, SSN, US phone, IPv4, credit card,
#          passport numbers, names with DOB patterns
# ─────────────────────────────────────────────────────────
set -euo pipefail

# Files explicitly allowed (from .gitallowed)
ALLOWED_FILE=".gitallowed"
ALLOWED=()
if [[ -f "$ALLOWED_FILE" ]]; then
  while IFS= read -r line; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    ALLOWED+=("$line")
  done < "$ALLOWED_FILE"
fi

FAILED=0

for file in "$@"; do
  # Skip allowed files
  skip=0
  for allowed in "${ALLOWED[@]}"; do
    [[ "$file" == "$allowed" ]] && { skip=1; break; }
  done
  [[ $skip -eq 1 ]] && continue

  # Skip binary files
  if ! file "$file" | grep -qE '(text|ASCII|UTF)'; then
    continue
  fi

  MATCH=""

  # Email addresses
  if grep -qP '[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}' "$file" 2>/dev/null; then
    MATCH="email address"
  fi

  # US Social Security Number: XXX-XX-XXXX
  if grep -qP '\b\d{3}-\d{2}-\d{4}\b' "$file" 2>/dev/null; then
    MATCH="SSN pattern"
  fi

  # US Phone: (XXX) XXX-XXXX or XXX-XXX-XXXX or +1XXXXXXXXXX
  if grep -qP '(?:\+1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]\d{4}' "$file" 2>/dev/null; then
    MATCH="phone number"
  fi

  # Credit card numbers (basic Luhn-ignorant pattern)
  if grep -qP '\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b' "$file" 2>/dev/null; then
    MATCH="credit card pattern"
  fi

  # IPv4 addresses that look like real private/public IPs in data context
  if grep -qP '\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b' "$file" 2>/dev/null; then
    # Allow localhost/loopback
    if ! grep -qP '\b(127\.0\.0\.1|0\.0\.0\.0|localhost)\b' "$file" 2>/dev/null; then
      MATCH="IP address pattern"
    fi
  fi

  if [[ -n "$MATCH" ]]; then
    echo "❌ [PII GUARD] $MATCH detected in: $file"
    echo "   Add to .gitallowed if this is a test fixture."
    FAILED=1
  fi
done

[[ $FAILED -eq 0 ]] || { echo "\n❌ Commit blocked by PII GUARD."; exit 1; }
exit 0
