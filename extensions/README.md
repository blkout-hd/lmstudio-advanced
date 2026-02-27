# Extensions

LM Studio plugin extensions directory. Each subdirectory is a LM Studio plugin
with a `manifest.json` and associated runner scripts.

## Structure

```
extensions/
├── smithery-cloud/       # Smithery cloud gateway connector
├── legal-pipeline/       # Full legal workflow extension
├── research-pipeline/    # Web + academic research extension
├── ocr-ingest/           # GLM-OCR + Qwen3-VL ingestion extension
└── model-router/         # Local vs cloud model routing extension
```

## Installing in LM Studio

Extensions are installed via LM Studio's plugin manager or by placing the extension
directory in `~/.lmstudio/extensions/` and restarting LM Studio.

Each extension references an MCP server from `mcp/servers/` for its network operations.
