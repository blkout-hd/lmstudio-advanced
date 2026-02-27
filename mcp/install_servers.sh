#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# install_servers.sh — Install all MCP reference servers
# Usage: bash mcp/install_servers.sh
# ─────────────────────────────────────────────────────────
set -euo pipefail

echo "🔌 Installing MCP reference servers..."

# Ensure npx available
if ! command -v npx &>/dev/null; then
  echo "❌ npx not found. Install Node.js >= 18 first."
  exit 1
fi

# Reference servers (official modelcontextprotocol)
REF_SERVERS=(
  "@modelcontextprotocol/server-memory"
  "@modelcontextprotocol/server-sequential-thinking"
  "@modelcontextprotocol/server-time"
  "@modelcontextprotocol/server-filesystem"
  "@modelcontextprotocol/server-git"
  "@modelcontextprotocol/server-fetch"
  "@modelcontextprotocol/server-github"
  "@modelcontextprotocol/server-brave-search"
)

for server in "${REF_SERVERS[@]}"; do
  echo "  → $server"
  npx -y "$server" --help &>/dev/null || true
done

# Smithery CLI
echo "🤖 Installing Smithery CLI..."
npm install -g @smithery/cli 2>/dev/null || npx -y @smithery/cli --version

# Anthropic skills
echo "🧠 Installing Anthropic skills..."
if command -v claude &>/dev/null; then
  claude mcp add-skill anthropics/skills/mcp-builder      || true
  claude mcp add-skill anthropics/skills/skill-creator     || true
  claude mcp add-skill anthropics/skills/web-artifacts-builder || true
  claude mcp add-skill anthropics/skills/webapp-testing    || true
else
  echo "⚠️  claude CLI not found. Install Claude Code first, then re-run."
fi

# Copy MCP config to .claude/
echo "📄 Linking MCP config to .claude/mcp.json..."
mkdir -p .claude
cp mcp/claude_mcp_config.json .claude/mcp.json

echo "✅ Done. Set env vars: GITHUB_PAT, SMITHERY_API_KEY, BRAVE_API_KEY in .env"
