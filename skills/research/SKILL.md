# Research Orchestration

> Skill for web and academic research with LLM synthesis.
> Custom skill for lmstudio-advanced.

## When to Use

Use this skill when:
- Searching arXiv, Semantic Scholar, or CrossRef for papers
- Running web research with source normalization and re-ranking
- Synthesizing cited answers from multi-source research results
- Building literature review sections with proper citations

## Pipeline

```
Query
  ├─> AcademicSearchTool (arXiv + Semantic Scholar + CrossRef)
  └─> WebResearchTool (sandboxed Brave/SerpAPI)
       └─> BM25 + LLM reranker
            └─> ResearchOrchestrator synthesis
                 └─> Cited answer with source links
```
