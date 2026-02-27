/**
 * Connector to HuggingFace-hosted legal NLP models.
 * Supports:
 * - nlpaueb/legal-bert-base-uncased
 * - nlpaueb/bert-base-uncased-contracts
 * - Contract classifiers (e.g. Nikhil-AI-Labs/legal-contract-classifier-best)
 * - CUAD-based models (theatticusproject)
 */
export type HFLegalModelId =
  | "nlpaueb/legal-bert-base-uncased"
  | "nlpaueb/bert-base-uncased-contracts"
  | "Nikhil-AI-Labs/legal-contract-classifier-best"
  | string;  // allow custom model IDs

export interface HFInferenceOptions {
  inputs: string | string[];
  parameters?: Record<string, unknown>;
}

export interface HFClassificationResult {
  label: string;
  score: number;
}

export class HFLegalModelConnector {
  constructor(
    private modelId: HFLegalModelId,
    private apiKey?: string,
    private baseUrl = "https://api-inference.huggingface.co",
  ) {}

  async classify(text: string): Promise<HFClassificationResult[]> {
    const url = `${this.baseUrl}/models/${this.modelId}`;
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (this.apiKey) headers["Authorization"] = `Bearer ${this.apiKey}`;

    const response = await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify({ inputs: text }),
    });

    if (!response.ok) {
      throw new Error(`HF inference failed: ${response.status} ${response.statusText}`);
    }

    return response.json() as Promise<HFClassificationResult[]>;
  }

  async classifyBatch(texts: string[]): Promise<HFClassificationResult[][]> {
    return Promise.all(texts.map(t => this.classify(t)));
  }
}
