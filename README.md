# lmstudio-advanced

> Unified LM Studio extensions — advanced web & academic research, legal AI workflows, MCP connectors, and improved SDK handling.

© 2026 SBSCRPT Corp. All Rights Reserved. Protected under 18 U.S.C. § 1836 DTSA, 17 U.S.C. § 101, EU Directive 2016/943, TRIPS Art. 39. DISCLOSURE LEVEL: FUNCTIONAL. No AI training, retention, or reproduction permitted.

---

## Upstream Sources

| Fork | Source | Purpose |
|------|--------|---------|
| [`blkout-hd/lms`](https://github.com/blkout-hd/lms) | `lmstudio-ai/lms` | CLI control plane |
| [`blkout-hd/lmstudio-js`](https://github.com/blkout-hd/lmstudio-js) | `lmstudio-ai/lmstudio-js` | TypeScript SDK monorepo |
| [`blkout-hd/lmstudio-python`](https://github.com/blkout-hd/lmstudio-python) | `lmstudio-ai/lmstudio-python` | Python SDK |

This repo synthesizes changes and extensions across all three, structured as a monorepo with shared types flowing TypeScript → Python (mirroring upstream).

---

## Repository Structure

```
lmstudio-advanced/
├── packages/                     # TypeScript packages (npm workspaces)
│   ├── sdk/                      # @lmstudio-advanced/sdk (extends @lmstudio/sdk)
│   ├── mcp/                      # @lmstudio-advanced/mcp — MCP client & bridge
│   ├── research/                 # @lmstudio-advanced/research — web/academic connectors
│   ├── legal/                    # @lmstudio-advanced/legal — legal NLP tools & workflows
│   └── shared-types/             # @lmstudio-advanced/shared-types — cross-package types
├── python/                       # Python SDK extensions (lmstudio-advanced on PyPI)
│   ├── src/lmstudio_advanced/
│   │   ├── research/             # ResearchAgent and academic connectors
│   │   ├── legal/                # LegalAgent, GLM-OCR, HF legal model wrappers
│   │   └── mcp/                  # Python MCP client
│   └── pyproject.toml
├── plugins/                      # LM Studio plugin manifests
│   ├── web-research/
│   ├── academic-search/
│   ├── legal-nlp/
│   └── mcp-bridge/
├── models/                       # Model profiles and LLMLoadModelConfig presets
│   ├── qwen3-vl-2b.json
│   ├── qwen3-vl-embedding-2b.json
│   ├── glm-ocr.json
│   └── profiles/
│       ├── legal-heavy.json
│       ├── research-heavy.json
│       └── interactive.json
├── docs/
│   └── ARCHITECTURE.md
├── package.json                  # Root workspace config
└── pyproject.toml                # Root Python workspace
```

---

## Key Features

### Advanced Web & Academic Research
- `WebResearchTool` — sandboxed web search and summarization via LM Studio plugins (`deno`/`mcpBridge` runner)
- `AcademicSearchTool` — arXiv, Semantic Scholar, CrossRef connectors with result normalization
- BM25 + LLM hybrid re-ranking pipeline

### Legal AI Workflows
- **GLM-OCR ingestion** — 0.9B OCR model for scanned contracts and regulatory PDFs
- **Qwen3-VL-2B** — layout-aware multimodal contract understanding
- **Qwen3-VL-Embedding-2B** — unified text/visual embeddings for clause retrieval
- **HuggingFace Legal Models** — LEGAL-BERT, contract classifiers, CUAD-taxonomy clause labeling
- End-to-end pipeline: OCR → embed → retrieve → reason → draft/redline

### MCP Connectors
- `@lmstudio-advanced/mcp` — generic `McpClient` (stdio, WebSocket, HTTP)
- Tool descriptor adapters bridging MCP ↔ LM Studio tool-calling
- Plugin manifest templates for `mcpBridge` runner with sandboxed network access

### Agent Orchestration
- Typed `ToolRegistry` with capability tags and permission scopes
- Reactive (`observe → think → act`) and deliberative (plan-then-execute) agent modes
- Pluggable memory backends, routing policies, and governance hooks

### Model Load Profiles (>4 GB local)
- Quantization-friendly presets for Qwen3 2B-class models within 4–8 GB VRAM envelopes
- Flash Attention, KV cache quantization, and RoPE extension configs
- Cloud OSS GPT fallback routing for tasks exceeding local capacity

---

## Quick Start

```bash
# Clone
git clone https://github.com/blkout-hd/lmstudio-advanced
cd lmstudio-advanced

# TypeScript
npm install
npm run build

# Python
pip install -e ./python
```

---

## Upstream Sync

```bash
git remote add lms-upstream     https://github.com/lmstudio-ai/lms
git remote add js-upstream      https://github.com/lmstudio-ai/lmstudio-js
git remote add python-upstream  https://github.com/lmstudio-ai/lmstudio-python

git fetch --all
# Merge upstream changes into respective feature branches as needed
```

---

## License

See individual upstream licenses. Extensions and synthesis code © 2026 SBSCRPT Corp. All Rights Reserved.
