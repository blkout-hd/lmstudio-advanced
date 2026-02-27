#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# install_hooks.sh — One-command hook installation
#
# Usage: bash .hooks/install_hooks.sh
# ─────────────────────────────────────────────────────────
set -euo pipefail

echo "🔒 Installing lmstudio-advanced pre-commit hooks..."

# Ensure pre-commit is available
if ! command -v pre-commit &>/dev/null; then
  echo "ℹ️  pre-commit not found. Installing..."
  pip install --quiet pre-commit
fi

# Make all hook scripts executable
chmod +x .hooks/*.sh .hooks/*.py

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push

# Run hooks against all files immediately to baseline-scan the repo
echo "🔍 Running initial scan against all files..."
pre-commit run --all-files || true

echo "✅ Hooks installed. All commits will now be scanned for:"
echo "   • Secrets & credentials (Gitleaks)"
echo "   • Log files and structured log content"
echo "   • PII (email, SSN, phone, IP, credit card)"
echo "   • SBSCRPT/MAGI proprietary IP identifiers"
echo "   • Private branch content leaking to public branches"
echo "   • High-entropy token detection (autonomous guard)"
