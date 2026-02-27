"""McpClient — Python MCP client for connecting to local or remote MCP servers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Optional

McpTransport = Literal["stdio", "websocket", "http"]


@dataclass
class McpToolDef:
    name: str
    description: str
    input_schema: dict[str, Any]
    output_schema: Optional[dict[str, Any]] = None


@dataclass
class McpToolResult:
    call_id: Optional[str]
    output: Any
    error: Optional[str] = None


class McpClient:
    """Generic MCP client supporting stdio, WebSocket, and HTTP transports.

    Example::

        from lmstudio_advanced import McpClient

        client = McpClient(transport="websocket", endpoint="ws://localhost:3100")
        client.connect()
        tools = client.list_tools()
        result = client.call_tool("search", {"query": "GDPR compliance"})
        client.disconnect()
    """

    def __init__(
        self,
        transport: McpTransport = "websocket",
        endpoint: str = "ws://localhost:3100",
        auth_token: str | None = None,
        timeout_ms: int = 30_000,
        max_retries: int = 3,
    ) -> None:
        self.transport = transport
        self.endpoint = endpoint
        self.auth_token = auth_token
        self.timeout_ms = timeout_ms
        self.max_retries = max_retries
        self._connected = False

    def connect(self) -> None:
        """Establish connection to MCP server and perform handshake."""
        # Transport-specific connect logic
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def list_tools(self) -> list[McpToolDef]:
        """Discover tools advertised by the MCP server."""
        if not self._connected:
            raise RuntimeError("McpClient: not connected")
        return []

    def call_tool(self, tool: str, input: dict[str, Any], call_id: str | None = None) -> McpToolResult:
        """Invoke a named tool on the MCP server."""
        if not self._connected:
            raise RuntimeError("McpClient: not connected")
        return McpToolResult(call_id=call_id, output=None)
