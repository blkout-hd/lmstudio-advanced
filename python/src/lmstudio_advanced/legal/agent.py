"""LegalAgent — end-to-end legal document analysis pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

ClauseRisk = Literal["low", "medium", "high", "critical"]


@dataclass
class LegalClause:
    clause_id: str
    text: str
    clause_type: str
    risk: ClauseRisk
    page_ref: Optional[int] = None
    annotations: dict[str, str] = field(default_factory=dict)


@dataclass
class LegalDocumentAnalysis:
    document_id: str
    filename: str
    total_clauses: int
    clauses: list[LegalClause]
    overall_risk: ClauseRisk
    summary: str
    jurisdiction: Optional[str] = None
    analyzed_at: str = ""


class LegalAgent:
    """Orchestrates GLM-OCR ingestion, LEGAL-BERT clause analysis,
    Qwen3-VL document understanding, and RAG-based legal synthesis.

    Example::

        import lmstudio as lms
        from lmstudio_advanced import LegalAgent

        agent = LegalAgent(
            model=lms.llm("Qwen3-VL-2B-Instruct"),
            glm_ocr_endpoint="http://localhost:1234",
            hf_api_key="hf_...",
        )
        analysis = agent.analyze_document("contract.pdf")
        answer = agent.query("What is the limitation of liability?", documents=["contract.pdf"])
    """

    def __init__(
        self,
        model=None,
        glm_ocr_endpoint: str = "http://localhost:1234",
        qwen3_vl_endpoint: str | None = None,
        hf_api_key: str | None = None,
        hf_legal_model: str = "nlpaueb/legal-bert-base-uncased",
        confidence_threshold: float = 0.7,
    ) -> None:
        self.model = model
        self.glm_ocr_endpoint = glm_ocr_endpoint
        self.qwen3_vl_endpoint = qwen3_vl_endpoint
        self.hf_api_key = hf_api_key
        self.hf_legal_model = hf_legal_model
        self.confidence_threshold = confidence_threshold

    def analyze_document(self, file_path: str, jurisdiction: str | None = None) -> LegalDocumentAnalysis:
        """Full pipeline: OCR → chunk → classify clauses → assess risk."""
        # 1. Ingest via GLM-OCR (+ optional Qwen3-VL for visual sections)
        # 2. Chunk document into clause candidates
        # 3. Classify each with LEGAL-BERT via HF Inference API
        # 4. Aggregate risk and produce analysis
        import time
        _ = file_path, jurisdiction
        return LegalDocumentAnalysis(
            document_id="",
            filename=file_path,
            total_clauses=0,
            clauses=[],
            overall_risk="low",
            summary="Analysis pending implementation.",
            analyzed_at=str(int(time.time())),
        )

    def query(
        self,
        query: str,
        documents: list[str] | None = None,
        analysis_depth: Literal["summary", "detailed", "exhaustive"] = "detailed",
    ) -> str:
        """RAG-based legal Q&A over provided documents using local LM Studio model."""
        if self.model is None:
            raise RuntimeError("LegalAgent: no model provided")
        documents = documents or []
        analyses = [self.analyze_document(d) for d in documents]
        context_clauses = [
            f"[{c.clause_type} | {c.risk}] {c.text}"
            for analysis in analyses
            for c in analysis.clauses[:20]
        ]
        context = "\n".join(context_clauses)
        prompt = (
            f"Legal query ({analysis_depth}): {query}\n\n"
            f"Relevant clauses:\n{context}\n\n"
            "Provide a legally grounded answer with clause references."
        )
        response = self.model.complete(prompt)
        return str(response)
