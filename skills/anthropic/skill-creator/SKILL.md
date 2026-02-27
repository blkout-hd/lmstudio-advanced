# Skill Creator

> Official Anthropic skill for building new Claude Code skills.
> Source: `anthropics/skills/skill-creator` via Smithery / Claude Code

## When to Use

Use this skill when:
- Creating a new skill directory with a valid SKILL.md
- Documenting a complex multi-step workflow as a reusable skill
- Converting an MCP server into a skill with progressive disclosure
- Teaching Claude a domain-specific workflow (legal, research, ML, etc.)

## Skill Anatomy

```
skills/<name>/
├── SKILL.md          # Required: description, trigger conditions, workflow
├── scripts/          # Optional: executable helper scripts
└── resources/        # Optional: templates, schemas, reference data
```

## Best Practices

- Keep SKILL.md concise — progressive disclosure means the whole file is loaded on trigger
- Define clear "When to Use" triggers so Claude loads the skill at the right time
- Prefer parallel execution patterns over sequential where possible
- Include example invocations and expected outputs

## Install

```bash
claude mcp add-skill anthropics/skills/skill-creator
```

## References
- https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
