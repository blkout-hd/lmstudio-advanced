# MCP Servers

Model Context Protocol server configurations for lmstudio-advanced.

## Reference Servers (Official — modelcontextprotocol/servers)

| Server | Package | Capability |
|--------|---------|------------|
| Memory / Knowledge Graph | `@modelcontextprotocol/server-memory` | Persistent entity memory across sessions |
| Sequential Thinking | `@modelcontextprotocol/server-sequential-thinking` | Dynamic reflective problem-solving |
| Time | `@modelcontextprotocol/server-time` | Time and timezone conversion |
| Filesystem | `@modelcontextprotocol/server-filesystem` | Secure sandboxed file operations |
| Git | `@modelcontextprotocol/server-git` | Read/search/manipulate Git repos |
| Fetch | `@modelcontextprotocol/server-fetch` | Web content fetching for LLM context |
| Everything | `@modelcontextprotocol/server-everything` | Reference/test server (prompts + tools) |

## Smithery Servers

| Server | Smithery Slug | Capability |
|--------|-------------|------------|
| Smithery Registry | `@smithery/registry` | Search + connect to MCP registry |
| Brave Search | `@smithery/brave-search` | Web search via Brave API |
| GitHub | `@modelcontextprotocol/server-github` | GitHub API operations |
| OpenAI | `@openai/mcp-server-openai` | OpenAI API tool bridge |

## Install All

```bash
bash mcp/install_servers.sh
```

## Configuration

All server configs are in `mcp/servers/`. Each JSON file is a Claude Code MCP server config block.
The `mcp/claude_mcp_config.json` is the ready-to-use full config for `.claude/mcp.json`.
