import { z } from "zod";

/** MCP transport flavors */
export type McpTransport = "stdio" | "websocket" | "http";

/** Configuration for connecting to an MCP server */
export interface McpServerConfig {
  name: string;
  transport: McpTransport;
  endpoint: string;         // e.g. ws://localhost:3100 or http://localhost:3100
  authToken?: string;
  timeoutMs?: number;
  maxRetries?: number;
}

export const mcpServerConfigSchema = z.object({
  name: z.string(),
  transport: z.enum(["stdio", "websocket", "http"]),
  endpoint: z.string(),
  authToken: z.string().optional(),
  timeoutMs: z.number().int().positive().optional(),
  maxRetries: z.number().int().nonnegative().optional(),
});

/** Represents a single tool exposed by an MCP server */
export interface McpToolDef {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;   // JSON Schema object
  outputSchema?: Record<string, unknown>;
}

/** MCP tool invocation payload */
export interface McpToolCall {
  tool: string;
  input: Record<string, unknown>;
  callId?: string;
}

/** MCP tool response */
export interface McpToolResult {
  callId?: string;
  output: unknown;
  error?: string;
}
