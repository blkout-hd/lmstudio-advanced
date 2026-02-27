# MCP Builder

> Official Anthropic skill for creating and configuring Model Context Protocol servers.
> Source: `anthropics/skills/mcp-builder` via Smithery / Claude Code

## When to Use

Use this skill when:
- Creating a new MCP server from scratch
- Adding tools, resources, or prompts to an existing MCP server
- Configuring MCP server connections in Claude Code
- Debugging MCP server connectivity issues

## Workflow

1. Identify the external service or capability to expose
2. Define the tool schema (name, description, input/output shapes)
3. Scaffold the server using the MCP TypeScript or Python SDK
4. Register the server in `.mcp/servers/` configuration
5. Test with `claude mcp test <server-name>`

## Install

```bash
claude mcp add-skill anthropics/skills/mcp-builder
# or via Smithery:
npx @smithery/cli install @anthropic/mcp-builder
```

## References
- https://modelcontextprotocol.io
- https://github.com/anthropics/claude-cookbooks/tree/main/skills
- https://smithery.ai
