# MCP Integration - Deep Dive

## Overview

Claude Code implements full MCP (Model Context Protocol) support, allowing external servers to provide tools, resources, and prompt templates.

## Architecture

```
┌─────────────────────────────────────────┐
│              Claude Code                 │
│  ┌─────────────────────────────────┐    │
│  │       MCP Connection Manager     │    │
│  │  ┌──────────┐  ┌──────────┐    │    │
│  │  │ Stdio    │  │ HTTP     │    │    │
│  │  │ Transport│  │ Transport│    │    │
│  │  └────┬─────┘  └────┬─────┘    │    │
│  └───────┼──────────────┼─────────┘    │
│          │              │              │
│  ┌───────▼──────────────▼─────────┐    │
│  │      MCP Client (per server)    │    │
│  │  - Tool registration            │    │
│  │  - Resource management          │    │
│  │  - Prompt templates             │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
           ↕            ↕
    External MCP Servers (stdio/HTTP)
```

## Configuration Sources

MCP servers are configured from multiple sources (in priority order):

1. **`--mcp-config` CLI flag**: JSON string or file path
2. **`.mcp.json` in project**: Project-scoped servers
3. **`~/.claude/settings.json`**: User-scoped servers
4. **Claude.ai connectors**: OAuth-based servers (claude.ai subscribers)
5. **Plugin MCP configs**: From enabled plugins
6. **Enterprise policy**: Remote managed settings

### Configuration Format

```json
{
  "mcpServers": {
    "my-server": {
      "type": "stdio",
      "command": "node",
      "args": ["server.js"],
      "env": { "API_KEY": "..." }
    },
    "http-server": {
      "type": "http",
      "url": "https://mcp.example.com",
      "headers": { "Authorization": "Bearer ..." }
    }
  }
}
```

## Connection Lifecycle

### 1. Discovery

```typescript
// services/mcp/config.ts
export async function getClaudeCodeMcpConfigs(dynamicConfig) {
  const sources = [
    readProjectMcpJson(),      // .mcp.json
    readUserSettings(),         // ~/.claude/settings.json
    readPluginMcpConfigs(),     // Plugin configs
    dynamicConfig               // --mcp-config flag
  ]
  return mergeAndDedup(sources)
}
```

### 2. Connection

```typescript
// services/mcp/client.ts
export async function getMcpToolsCommandsAndResources(callback, configs) {
  for (const [name, config] of Object.entries(configs)) {
    const client = await connectToServer(name, config)
    const { tools, commands, resources } = await client.listCapabilities()
    callback({ client, tools, commands, resources })
  }
}
```

### 3. Tool Registration

MCP tools are registered in the tool pool:

```typescript
// In tools.ts - assembleToolPool
const mcpTools = appState.mcp.tools.map(mcpTool => ({
  name: `mcp__${serverName}__${mcpTool.name}`,
  description: mcpTool.description,
  inputSchema: z.object({...}),
  call: async function* (input) {
    const result = await client.callTool(mcpTool.name, input)
    yield { type: 'result', data: { result } }
  }
}))
```

### 4. Call Execution

```
Model: tool_use { name: "mcp__github__create_issue", input: {...} }
  ↓
Claude Code routes to MCP client
  ↓
MCP client calls server: tools/call { name: "create_issue", arguments: {...} }
  ↓
Server executes and returns result
  ↓
Result converted to tool_result block
  ↓
Sent back to model
```

## MCP Tools vs MCP Prompts

### MCP Tools
- Invoked by the model (like built-in tools)
- Show in tool pool
- Schema-validated input/output

### MCP Prompts
- Invoked by users (slash commands) or model (SkillTool)
- Show in command list
- Can have arguments

```typescript
// MCP prompt → Command
{
  type: 'prompt',
  name: 'mcp__server__prompt_name',
  description: prompt.description,
  getPromptForCommand: async (args) => {
    return await client.getPrompt(prompt.name, args)
  },
  loadedFrom: 'mcp'
}
```

## MCP Resources

Resources are readable data exposed by MCP servers:

```typescript
// List resources
const resources = await client.listResources()

// Read resource
const content = await client.readResource(uri)
```

## Error Handling

### Connection Errors
- Server fails to start → Mark as failed, continue with other servers
- Server crashes → Auto-reconnect with backoff
- Timeout → Show warning, keep trying

### Tool Call Errors
- Invalid input → Schema validation error
- Server error → Propagate error message to model
- Network error → Retry with backoff

## Policy Filtering

Enterprise policies can restrict MCP servers:

```typescript
// services/mcp/config.ts
export function filterMcpServersByPolicy(configs) {
  const allowed = {}
  const blocked = []
  
  for (const [name, config] of Object.entries(configs)) {
    if (isPolicyAllowed('allowedMcpServers', name)) {
      allowed[name] = config
    } else {
      blocked.push(name)
    }
  }
  
  return { allowed, blocked }
}
```

## Key Files

| File | Purpose |
|------|---------|
| `services/mcp/client.ts` | MCP client management |
| `services/mcp/config.ts` | Configuration parsing |
| `services/mcp/types.ts` | Type definitions |
| `services/mcp/useManageMCPConnections.ts` | React hook for MCP state |
| `services/mcp/officialRegistry.ts` | Official MCP server registry |
| `services/mcp/claudeai.ts` | Claude.ai MCP connectors |
| `services/mcp/channelNotification.ts` | Channel notifications |
| `services/mcp/elicitationHandler.ts` | Elicitation handling |
| `tools/MCPTool/` | MCP tool wrapper |
| `tools/ListMcpResourcesTool/` | List MCP resources |
| `tools/ReadMcpResourceTool/` | Read MCP resources |
