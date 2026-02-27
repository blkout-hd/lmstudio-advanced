import type { ResearchResult } from "@lmstudio-advanced/shared-types";
import { WebResearchTool } from "./WebResearchTool.js";
import { AcademicSearchTool } from "./AcademicSearchTool.js";

export interface ResearchOrchestratorOptions {
  web?: WebResearchTool;
  academic?: AcademicSearchTool;
  rerankFn?: (query: string, results: ResearchResult[]) => Promise<ResearchResult[]>;
}

/**
 * Orchestrates web and academic search, merges results,
 * and applies optional LLM-based reranking.
 */
export class ResearchOrchestrator {
  constructor(private opts: ResearchOrchestratorOptions) {}

  async research(query: string, options?: { academicOnly?: boolean; maxSources?: number }): Promise<ResearchResult[]> {
    const tasks: Promise<ResearchResult[]>[] = [];
    if (this.opts.academic) tasks.push(this.opts.academic.search({ query, maxResults: 20 }));
    if (!options?.academicOnly && this.opts.web) tasks.push(this.opts.web.search({ query, numResults: 10 }));

    const allResults = (await Promise.allSettled(tasks))
      .filter((r): r is PromiseFulfilledResult<ResearchResult[]> => r.status === "fulfilled")
      .flatMap(r => r.value);

    const reranked = this.opts.rerankFn
      ? await this.opts.rerankFn(query, allResults)
      : allResults;

    return reranked.slice(0, options?.maxSources ?? 15);
  }
}
