# Services Module

Background services and external integrations (130 files).

## Service Categories

### API
- `api/` - API service layer, bootstrap data, file API

### MCP
- `mcp/` - MCP client, config, connections, tools, resources
- `mcp/types.ts` - MCP type definitions
- `mcp/client.ts` - MCP client management
- `mcp/config.ts` - Configuration parsing

### Analytics
- `analytics/` - Analytics and telemetry
- `analytics/growthbook.ts` - Feature flags

### Plugins
- `plugins/` - Plugin management
- `plugins/pluginCliCommands.ts` - Plugin CLI commands

### Settings
- `settingsSync/` - Settings synchronization
- `remoteManagedSettings/` - Remote managed settings
- `policyLimits/` - Policy limit enforcement

### Memory
- `SessionMemory/` - Session memory management
- `extractMemories/` - Memory extraction
- `teamMemorySync/` - Team memory sync

### LSP
- `lsp/` - Language Server Protocol integration

### OAuth
- `oauth/` - OAuth authentication

### Other
- `AgentSummary/` - Agent summary generation
- `MagicDocs/` - Documentation generation
- `PromptSuggestion/` - Prompt suggestions
- `compact/` - Conversation compaction
- `tips/` - User tips
- `toolUseSummary/` - Tool use summaries
- `tools/` - Tool services
- `autoDream/` - Dream automation
