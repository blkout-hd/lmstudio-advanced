# OpenAI API Integration

> Skill for interacting with OpenAI-compatible APIs including OSS cloud endpoints.
> Sourced from Smithery registry.

## When to Use

Use this skill when:
- Routing tasks to OpenAI-compatible cloud LLM endpoints (GPT-4o, OSS cloud)
- Comparing local LM Studio model outputs against cloud baselines
- Using OpenAI embeddings API as a fallback for Qwen3-VL-Embedding
- Structuring function-calling tool schemas for OpenAI-compatible servers

## Workflow

1. Configure `OPENAI_API_KEY` and `OPENAI_BASE_URL` in `.env`
2. Use `openai` Python/JS SDK with `base_url` overridden for OSS cloud
3. For LM Studio: `base_url = "http://localhost:1234/v1"`
4. Structured outputs: use `response_format: { type: "json_schema" }` for deterministic extraction

## MCP Server

```bash
npx @smithery/cli install @openai/mcp-server-openai
```

## References
- https://platform.openai.com/docs
- https://smithery.ai/server/@openai/mcp-server-openai
