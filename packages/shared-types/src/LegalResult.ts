import { z } from "zod";

/** Risk level for a legal clause or document */
export type ClauseRisk = "low" | "medium" | "high" | "critical";

/** A normalized clause extracted from a legal document */
export interface LegalClause {
  clauseId: string;
  text: string;
  clauseType: string;       // e.g. CUAD category: "Limitation of Liability", "Governing Law"
  risk: ClauseRisk;
  pageRef?: number;
  startChar?: number;
  endChar?: number;
  annotations?: Record<string, string>;
}

export const legalClauseSchema = z.object({
  clauseId: z.string(),
  text: z.string(),
  clauseType: z.string(),
  risk: z.enum(["low", "medium", "high", "critical"]),
  pageRef: z.number().int().nonnegative().optional(),
  startChar: z.number().int().nonnegative().optional(),
  endChar: z.number().int().nonnegative().optional(),
  annotations: z.record(z.string()).optional(),
});

/** Result from a full document legal analysis */
export interface LegalDocumentAnalysis {
  documentId: string;
  filename: string;
  totalClauses: number;
  clauses: LegalClause[];
  overallRisk: ClauseRisk;
  summary: string;
  jurisdiction?: string;
  analyzedAt: string;
}
