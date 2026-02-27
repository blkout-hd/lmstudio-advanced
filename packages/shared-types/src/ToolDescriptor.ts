import { z } from "zod";

/** Security/capability level for a registered tool */
export type ToolSecurityLevel = "local" | "sandboxed" | "network" | "cloud";

/** Tags for tool discovery */
export type ToolTag = "web" | "academic" | "legal" | "ocr" | "embedding" | "mcp" | "code" | "data";

/** A descriptor for a tool registered in the ToolRegistry */
export interface ToolDescriptor<TInput = unknown, TOutput = unknown> {
  name: string;
  description: string;
  version: string;
  tags: ToolTag[];
  securityLevel: ToolSecurityLevel;
  inputSchema: z.ZodType<TInput>;
  outputSchema: z.ZodType<TOutput>;
  execute: (input: TInput) => Promise<TOutput>;
  timeoutMs?: number;
  maxRetries?: number;
}

/** Central tool registry */
export class ToolRegistry {
  private tools = new Map<string, ToolDescriptor>();

  register<TInput, TOutput>(descriptor: ToolDescriptor<TInput, TOutput>): void {
    this.tools.set(descriptor.name, descriptor as ToolDescriptor);
  }

  find(name: string): ToolDescriptor | undefined {
    return this.tools.get(name);
  }

  findByTag(tag: ToolTag): ToolDescriptor[] {
    return [...this.tools.values()].filter(t => t.tags.includes(tag));
  }

  findBySecurity(level: ToolSecurityLevel): ToolDescriptor[] {
    return [...this.tools.values()].filter(t => t.securityLevel === level);
  }

  list(): ToolDescriptor[] {
    return [...this.tools.values()];
  }
}
