import { z } from "zod";

/** Normalized result from web or academic search connectors */
export interface ResearchResult {
  id: string;
  title: string;
  url: string;
  snippet: string;
  sourceType: "web" | "academic" | "patent" | "legal";
  publishedAt?: string;
  authors?: string[];
  venue?: string;
  relevanceScore?: number;
}

export const researchResultSchema = z.object({
  id: z.string(),
  title: z.string(),
  url: z.string().url(),
  snippet: z.string(),
  sourceType: z.enum(["web", "academic", "patent", "legal"]),
  publishedAt: z.string().optional(),
  authors: z.array(z.string()).optional(),
  venue: z.string().optional(),
  relevanceScore: z.number().min(0).max(1).optional(),
});
