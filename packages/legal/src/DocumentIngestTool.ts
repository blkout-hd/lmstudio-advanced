/**
 * DocumentIngestTool wraps GLM-OCR and Qwen3-VL to convert
 * PDFs and scanned images into structured text with layout metadata.
 *
 * GLM-OCR: zai-org/GLM-OCR (0.9B) — text extraction, tables, formulas
 * Qwen3-VL-2B: multimodal layout-aware understanding
 */
export interface IngestedDocument {
  documentId: string;
  filename: string;
  pages: IngestedPage[];
  rawText: string;
  tables: ExtractedTable[];
}

export interface IngestedPage {
  pageNumber: number;
  text: string;
  blocks: TextBlock[];
}

export interface TextBlock {
  blockId: string;
  type: "heading" | "paragraph" | "table" | "footer" | "header";
  text: string;
  confidence: number;
  bbox?: [number, number, number, number]; // x, y, w, h in px
}

export interface ExtractedTable {
  pageNumber: number;
  caption?: string;
  rows: string[][];
}

export class DocumentIngestTool {
  /**
   * @param glmOcrEndpoint - local LM Studio or Z.AI GLM-OCR endpoint
   * @param qwen3VlEndpoint - optional Qwen3-VL-2B endpoint for layout understanding
   */
  constructor(
    private glmOcrEndpoint: string,
    private qwen3VlEndpoint?: string,
  ) {}

  async ingest(filePathOrBuffer: string | Uint8Array, filename?: string): Promise<IngestedDocument> {
    // 1. Call GLM-OCR to extract text and layout
    // 2. Optionally enrich with Qwen3-VL for complex visual sections
    // 3. Chunk by page and block type
    void filePathOrBuffer; void filename;
    return {
      documentId: crypto.randomUUID(),
      filename: filename ?? "document",
      pages: [],
      rawText: "",
      tables: [],
    };
  }

  /** Split ingested document into clause-aligned chunks for embedding */
  toChunks(doc: IngestedDocument, chunkTokens = 512): string[] {
    // Splits rawText respecting page and block boundaries
    void doc; void chunkTokens;
    return [];
  }
}
