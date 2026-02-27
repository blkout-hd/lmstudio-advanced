"""lmstudio-advanced — Python extensions for LM Studio.

Provides:
- ResearchAgent: web and academic research orchestration
- LegalAgent: contract analysis, clause classification, OCR ingestion
- McpClient: Python MCP client for connecting to MCP servers
"""

from .research.agent import ResearchAgent
from .legal.agent import LegalAgent
from .mcp.client import McpClient

__all__ = ["ResearchAgent", "LegalAgent", "McpClient"]
__version__ = "0.1.0"
