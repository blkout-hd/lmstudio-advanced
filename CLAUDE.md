# lmstudio-advanced — Claude Code Configuration

> This file is automatically read by Claude Code when opening this repository.
> It configures skills, MCP servers, workflows, and project context.

## Project Overview

`lmstudio-advanced` is a unified LM Studio extension monorepo combining:
- Advanced web and academic research connectors
- Legal AI workflows (GLM-OCR, Qwen3-VL, LEGAL-BERT, HuggingFace)
- MCP server integrations
- Skills for Claude Code workflows
- Model pipeline management (HuggingFace + Ollama)

## Branch Guide

| Branch | Scope |
|--------|-------|
| `main` | Public base: shared-types, mcp, research, extensions, skills |
| `feat/legal-workflows` | Legal automation, clause analysis, compliance |
| `feat/vl-ocr` | GLM-OCR, Qwen3-VL, OCR plugins, datasets |
| `feat/models` | HuggingFace + Ollama model registry and pipelines |
| `private/sbscrpt` | SBSCRPT Corp proprietary IP |
| `private/magi` | MAGI system IP |

## MCP Servers

See `mcp/claude_mcp_config.json` for the full config. Quick setup:
```bash
bash mcp/install_servers.sh
```

Active servers:
- **memory** — knowledge graph persistent memory
- **sequential-thinking** — reflective multi-step reasoning
- **time** — timezone/deadline calculations
- **filesystem** — sandboxed file operations
- **git** — repo introspection
- **fetch** — web content retrieval
- **github** — GitHub API (requires `GITHUB_PAT`)
- **smithery-registry** — MCP skill discovery
- **brave-search** — web search (requires `BRAVE_API_KEY`)

## Skills

```bash
# Install Anthropic official skills
claude mcp add-skill anthropics/skills/mcp-builder
claude mcp add-skill anthropics/skills/skill-creator
```

Custom skills in `skills/`: `legal`, `research`, `security`, `pytorch`, `github`, `openai`.

## Key Commands

```bash
bash .hooks/install_hooks.sh   # Install security pre-commit hooks
bash mcp/install_servers.sh    # Install all MCP servers
npm install && npm run build   # Build TypeScript packages
pip install -e ./python        # Install Python package
```

## Security

All commits are scanned by `.hooks/autonomous_guard.py` for PII, logs, secrets, and proprietary IP.
See `SECURITY.md` for branch policy.

© 2026 SBSCRPT Corp. All Rights Reserved. Protected under 18 U.S.C. § 1836 DTSA, 17 U.S.C. § 101, EU Directive 2016/943, TRIPS Art. 39. DISCLOSURE LEVEL: FUNCTIONAL. No AI training, retention, or reproduction permitted.
