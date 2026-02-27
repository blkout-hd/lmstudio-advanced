# Architecture — lmstudio-advanced

## Overview

This monorepo synthesizes three upstream LM Studio repositories into a unified extension platform:

| Upstream | Fork | Role |
|----------|------|------|
| `lmstudio-ai/lms` | `blkout-hd/lms` | CLI control plane |
| `lmstudio-ai/lmstudio-js` | `blkout-hd/lmstudio-js` | TypeScript SDK |
| `lmstudio-ai/lmstudio-python` | `blkout-hd/lmstudio-python` | Python SDK |

Extension code in this repo follows the same schema-sync strategy as upstream: TypeScript types are canonical and Python types are derived.

## Package Dependency Graph

```
@lmstudio-advanced/shared-types
    ├── @lmstudio-advanced/mcp
    ├── @lmstudio-advanced/research
    └── @lmstudio-advanced/legal
            ├── depends on: @lmstudio/sdk (upstream)
            └── depends on: @lmstudio-advanced/shared-types

python/lmstudio_advanced
    ├── lmstudio (upstream Python SDK)
    ├── lmstudio_advanced.research
    ├── lmstudio_advanced.legal
    └── lmstudio_advanced.mcp
```

## Data Flow — Legal Workflow

```
User documents (PDF/images)
    │
    ▼
DocumentIngestTool (GLM-OCR 0.9B + Qwen3-VL-2B)
    │  structured text, layout blocks, tables
    ▼
Qwen3-VL-Embedding-2B
    │  unified text/visual embeddings
    ▼
Vector Database (local or LAN)
    │  top-k clause retrieval
    ▼
LEGAL-BERT / HF Contract Classifiers
    │  CUAD-taxonomy labeling + risk scoring
    ▼
RAG Synthesis via LM Studio local LLM
    │  cited answer / redlines / summary
    ▼
User
```

## Data Flow — Research Workflow

```
User query
    │
    ▼
WebResearchTool (sandboxed deno plugin)
    │  normalized ResearchResult[]
AcademicSearchTool (sandboxed deno plugin)
    │  normalized ResearchResult[]
    ▼
BM25 + LLM reranker
    │  top-k results
    ▼
LM Studio local LLM (synthesis + citation)
    │
    ▼
User
```

## Plugin Sandbox Policy

All network-capable plugins use `PluginSandboxSettings` with `enabled: true`.
Each plugin whitelist is defined in `plugins/*/manifest.json`:

| Plugin | Whitelisted Hosts |
|--------|-------------------|
| `web-research` | Brave/SerpAPI/Searxng only |
| `academic-search` | arXiv, Semantic Scholar, CrossRef |
| `legal-nlp` | HF Inference API + local GLM-OCR |
| `mcp-bridge` | localhost / explicitly listed MCP endpoints |

## Model Profiles

See `models/profiles/`. Each JSON file maps to `LLMLoadModelConfig` fields in `@lmstudio/sdk`.
Profiles: `interactive`, `research-heavy`, `legal-heavy`, `batch-summarization`.

## Upstream Sync Strategy

Keep upstream remotes (`lms-upstream`, `js-upstream`, `python-upstream`) and periodically
fetch + cherry-pick or merge upstream changes into dedicated integration branches before
merging to `main`. Extension packages in `packages/` and `python/` live in directories
that do not overlap with upstream file paths, minimizing merge conflicts.
