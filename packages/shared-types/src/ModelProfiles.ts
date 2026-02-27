/**
 * Named model load profiles for common workloads.
 * Maps to LLMLoadModelConfig from @lmstudio/sdk.
 */
export type ModelProfileName = "interactive" | "research-heavy" | "legal-heavy" | "batch-summarization";

export interface ModelProfile {
  name: ModelProfileName;
  description: string;
  config: {
    contextLength?: number;
    maxParallelPredictions?: number;
    useUnifiedKvCache?: boolean;
    flashAttention?: boolean;
    offloadKVCacheToGpu?: boolean;
    gpuStrictVramCap?: boolean;
    evalBatchSize?: number;
    gpu?: {
      ratio?: number | "max" | "off";
    };
  };
}

export const MODEL_PROFILES: Record<ModelProfileName, ModelProfile> = {
  interactive: {
    name: "interactive",
    description: "Low latency, single user. Best for chat and quick completions.",
    config: {
      contextLength: 8192,
      maxParallelPredictions: 1,
      flashAttention: true,
      gpuStrictVramCap: true,
      gpu: { ratio: "max" },
    },
  },
  "research-heavy": {
    name: "research-heavy",
    description: "Extended context for long document research and synthesis.",
    config: {
      contextLength: 32768,
      maxParallelPredictions: 2,
      useUnifiedKvCache: true,
      flashAttention: true,
      offloadKVCacheToGpu: true,
      evalBatchSize: 512,
      gpu: { ratio: "max" },
    },
  },
  "legal-heavy": {
    name: "legal-heavy",
    description: "Long context for multi-document contract and case analysis.",
    config: {
      contextLength: 65536,
      maxParallelPredictions: 1,
      useUnifiedKvCache: true,
      flashAttention: true,
      offloadKVCacheToGpu: true,
      gpuStrictVramCap: true,
      evalBatchSize: 256,
      gpu: { ratio: "max" },
    },
  },
  "batch-summarization": {
    name: "batch-summarization",
    description: "High throughput summarization of many short documents.",
    config: {
      contextLength: 16384,
      maxParallelPredictions: 4,
      useUnifiedKvCache: true,
      flashAttention: true,
      evalBatchSize: 1024,
      gpu: { ratio: "max" },
    },
  },
};
