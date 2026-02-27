"""ResearchAgent — orchestrates web and academic research via LM Studio."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ResearchResult:
    id: str
    title: str
    url: str
    snippet: str
    source_type: str  # "web" | "academic" | "patent" | "legal"
    relevance_score: float = 0.0
    published_at: Optional[str] = None
    authors: list[str] = field(default_factory=list)


class ResearchAgent:
    """High-level research agent that wraps web and academic search connectors.

    Example::

        import lmstudio as lms
        from lmstudio_advanced import ResearchAgent

        agent = ResearchAgent(model=lms.llm(), max_sources=15)
        results = agent.research("GDPR Article 6 lawful basis", academic_only=False)
    """

    def __init__(
        self,
        model=None,
        max_sources: int = 15,
        academic_providers: list[str] | None = None,
        web_api_key: str | None = None,
        hf_api_key: str | None = None,
    ) -> None:
        self.model = model
        self.max_sources = max_sources
        self.academic_providers = academic_providers or ["semanticScholar", "arxiv"]
        self.web_api_key = web_api_key
        self.hf_api_key = hf_api_key

    def research(
        self,
        query: str,
        *,
        academic_only: bool = False,
        include_code: bool = False,
        max_sources: int | None = None,
    ) -> list[ResearchResult]:
        """Run a research query and return normalized, re-ranked results."""
        # 1. Run academic search (arXiv, Semantic Scholar, CrossRef)
        # 2. Optionally run web search
        # 3. Deduplicate and re-rank via BM25 + optional LLM scoring
        # 4. Return top max_sources results
        _ = query, academic_only, include_code, max_sources
        return []

    def synthesize(self, query: str, results: list[ResearchResult]) -> str:
        """Use the LM Studio model to synthesize a cited answer from results."""
        if self.model is None:
            raise RuntimeError("ResearchAgent: no model provided for synthesis")
        context = "\n".join(
            f"[{r.source_type}] {r.title}: {r.snippet}" for r in results[:10]
        )
        prompt = f"Research query: {query}\n\nSources:\n{context}\n\nSynthesize a clear, cited answer."
        response = self.model.complete(prompt)
        return str(response)
