import type { McpToolDef } from "@lmstudio-advanced/shared-types";
import { ToolRegistry, type ToolDescriptor } from "@lmstudio-advanced/shared-types";
import { McpClient } from "./McpClient.js";
import { z } from "zod";

/**
 * Adapts an McpClient's discovered tools into the local ToolRegistry
 * so agents can call MCP tools exactly like local tools.
 */
export class McpToolRegistry {
  constructor(
    private client: McpClient,
    private registry: ToolRegistry,
  ) {}

  async syncTools(): Promise<void> {
    const mcpTools = await this.client.listTools();
    for (const tool of mcpTools) {
      this.registry.register(this.adapt(tool));
    }
  }

  private adapt(tool: McpToolDef): ToolDescriptor {
    return {
      name: tool.name,
      description: tool.description,
      version: "mcp",
      tags: ["mcp"],
      securityLevel: "network",
      inputSchema: z.unknown() as z.ZodType<unknown>,
      outputSchema: z.unknown() as z.ZodType<unknown>,
      execute: async (input: unknown) => {
        const result = await this.client.callTool({ tool: tool.name, input: input as Record<string, unknown> });
        if (result.error) throw new Error(result.error);
        return result.output;
      },
    };
  }
}
