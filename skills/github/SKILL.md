# GitHub Automation

> Skill for GitHub repository workflows: refactoring, PR review, code analysis, issue triage.
> Sourced from Smithery registry (github-authored / community).

## When to Use

Use this skill when:
- Performing autonomous code refactoring across multiple files
- Reviewing pull requests and generating structured review comments
- Triaging issues and creating sub-issues for complex tasks
- Running repository health checks (stale branches, missing tests, etc.)
- Auto-generating changelogs and release notes from commit history

## Available Sub-Skills

| Sub-Skill | Trigger | Description |
|-----------|---------|-------------|
| `refactor` | "refactor [file/module]" | Structural code improvement without behavior change |
| `pr-review` | "review PR #N" | Automated PR diff analysis and comment generation |
| `issue-triage` | "triage issues" | Label, prioritize, and route open issues |
| `release-notes` | "generate release notes" | Changelog from commits since last tag |
| `repo-audit` | "audit repo" | Security, license, and dependency audit |

## MCP Server

Uses `@modelcontextprotocol/server-github` (official reference implementation).

```bash
npx @smithery/cli install @modelcontextprotocol/server-github
```

## References
- https://github.com/modelcontextprotocol/servers/tree/main/src/github
