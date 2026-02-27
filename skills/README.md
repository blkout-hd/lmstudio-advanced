# Skills

Claude Code skills directory for lmstudio-advanced.
Skills use progressive disclosure — Claude loads only the skill relevant to the task at hand,
preventing context window saturation.

## Structure

```
skills/
├── anthropic/               # Official Anthropic skills
│   ├── mcp-builder/         # Build and configure MCP servers
│   ├── skill-creator/       # Create new Claude Code skills
│   ├── web-artifacts-builder/ # Generate web components
│   └── webapp-testing/      # Test web applications
├── pytorch/                 # PyTorch ML workflow skill
├── github/                  # GitHub automation skills (refactor, PR review, etc.)
├── openai/                  # OpenAI API integration skill
├── legal/                   # Legal document automation skill
├── research/                # Research orchestration skill
└── security/                # Security audit skill
```

## Installation (Claude Code)

```bash
# Add all Anthropic official skills
claude mcp add-skill anthropics/skills

# Or individual skills
claude mcp add-skill anthropics/skills/mcp-builder
claude mcp add-skill anthropics/skills/skill-creator
claude mcp add-skill anthropics/skills/web-artifacts-builder
claude mcp add-skill anthropics/skills/webapp-testing
```

## Smithery Registry

```bash
# Install Smithery CLI
npx @smithery/cli install

# Search and install skills
npx smithery search "legal document"
npx smithery install @smithery/sequential-thinking
```
