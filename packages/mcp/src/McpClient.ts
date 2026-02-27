import type { McpServerConfig, McpToolCall, McpToolDef, McpToolResult } from "@lmstudio-advanced/shared-types";

export interface McpClientOptions extends McpServerConfig {
  reconnectOnDisconnect?: boolean;
}

/**
 * Generic MCP client that connects to an MCP server over
 * stdio, WebSocket, or HTTP and exposes its tools.
 */
export class McpClient {
  private config: McpClientOptions;
  private connected = false;

  constructor(options: McpClientOptions) {
    this.config = options;
  }

  async connect(): Promise<void> {
    // Transport-specific connection logic
    // WebSocket: open ws connection and wait for MCP handshake
    // HTTP: send handshake POST to /mcp/connect
    // stdio: spawn process and attach stdin/stdout
    this.connected = true;
  }

  async disconnect(): Promise<void> {
    this.connected = false;
  }

  /** Discover tools advertised by the MCP server */
  async listTools(): Promise<McpToolDef[]> {
    if (!this.connected) throw new Error("McpClient: not connected");
    // Send MCP "tools/list" request and parse response
    return [];
  }

  /** Invoke a named tool on the MCP server */
  async callTool(call: McpToolCall): Promise<McpToolResult> {
    if (!this.connected) throw new Error("McpClient: not connected");
    // Send MCP "tools/call" request and return result
    return { callId: call.callId, output: null };
  }
}
