# Legal Document Automation

> Skill for legal workflow automation: OCR ingestion, clause analysis, RAG-based Q&A, compliance checks.
> Custom skill for lmstudio-advanced / SBSCRPT Corp.

## When to Use

Use this skill when:
- Analyzing contracts, NDAs, DPAs, or regulatory filings
- Extracting and classifying clauses using CUAD taxonomy
- Performing GDPR/CCPA/HIPAA compliance gap analysis
- Drafting redlines or clause recommendations
- Running jurisdiction-specific risk assessments

## Pipeline

```
Document (PDF/image)
  └─> DocumentIngestTool (GLM-OCR + Qwen3-VL-2B)
       └─> Clause chunking
            └─> LEGAL-BERT classification (HF Inference API)
                 └─> Qwen3-VL-Embedding retrieval
                      └─> RAG synthesis (local LM Studio LLM)
                           └─> Structured analysis + redlines
```

## Key Parameters

- `jurisdiction`: "US", "EU", "UK", "APAC"
- `analysis_depth`: "summary" | "detailed" | "exhaustive"
- `clause_types`: CUAD category subset (default: all 41)
- `model_profile`: "legal-heavy" (65k context, flash attention)

## Example Invocation

```python
from lmstudio_advanced import LegalAgent
agent = LegalAgent(model=lms.llm("Qwen3-VL-2B-Instruct"), hf_api_key="hf_...")
result = agent.query("Summarize limitation of liability clauses", documents=["contract.pdf"])
```
