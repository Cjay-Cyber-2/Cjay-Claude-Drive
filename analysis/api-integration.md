# API Integration - Deep Dive

## Overview

Claude Code integrates with the Anthropic API for all LLM interactions, supporting multiple authentication methods and provider backends.

## Authentication Methods

### 1. OAuth (claude.ai subscribers)
```typescript
// services/oauth/
const tokens = getClaudeAIOAuthTokens()
// Token refresh handled automatically
```

### 2. API Key
```typescript
// Direct API key
process.env.ANTHROPIC_API_KEY
// Or apiKeyHelper in settings
```

### 3. Bedrock (AWS)
```typescript
// process.env.CLAUDE_CODE_USE_BEDROCK
// AWS credentials via standard methods
```

### 4. Vertex (GCP)
```typescript
// process.env.CLAUDE_CODE_USE_VERTEX
// GCP credentials via standard methods
```

## Request Flow

```
QueryEngine.query()
  ↓
1. Build messages array:
   - System prompt (assembled from many sources)
   - Conversation history
   - Current user message
  ↓
2. Build tools array:
   - Built-in tools (from getTools())
   - MCP tools (from appState.mcp.tools)
  ↓
3. Call API:
   POST /v1/messages
   {
     model: "claude-sonnet-4-6",
     max_tokens: 8192,
     system: systemPrompt,
     messages: messages,
     tools: tools,
     thinking: { type: "adaptive" }
   }
  ↓
4. Process response:
   - Text blocks → display
   - Tool use blocks → execute tools
   - Thinking blocks → display
  ↓
5. Collect tool results:
   - Add tool_result blocks to messages
  ↓
6. Loop until model stops using tools
```

## System Prompt Assembly

The system prompt is built from multiple sections:

```typescript
// constants/prompts.ts
export async function getSystemPrompt(additions, model): Promise<string[]> {
  const sections = []
  
  sections.push(baseSystemPrompt)         // Core instructions
  sections.push(toolDescriptions)         // All tool schemas
  sections.push(claudeMdContent)          // CLAUDE.md files
  sections.push(agentPrompt)              // Agent-specific prompt
  sections.push(mcpToolDescriptions)      // MCP tool schemas
  sections.push(thinkingPrompt)           // Thinking configuration
  sections.push(effortPrompt)             // Effort level
  
  return sections.filter(Boolean)
}
```

## Context Window Management

Different models have different context windows:

```typescript
function getContextWindowForModel(model: string, betas: string[]): number {
  // Model-specific limits
  if (model.includes('opus')) return 200_000
  if (model.includes('sonnet')) return 200_000
  if (model.includes('haiku')) return 200_000
  return 200_000 // Default
}
```

When context fills up:
1. **Compaction**: Older messages are summarized
2. **File cache eviction**: Cached file contents are removed
3. **Message dropping**: Oldest messages removed

## Rate Limiting

Claude Code handles rate limits gracefully:

```typescript
// services/api/
- Check quota status at startup
- Retry on 429 with exponential backoff
- Show rate limit warnings to user
- Fast mode for faster responses
```

## Error Handling

| Error | Handling |
|-------|----------|
| 401 Unauthorized | Prompt re-authentication |
| 429 Rate limited | Retry with backoff |
| 500 Server error | Retry with backoff |
| 503 Overloaded | Fallback model or retry |
| Network error | Retry with backoff |

## Key Files

| File | Purpose |
|------|---------|
| `core/QueryEngine.ts` | Main query loop |
| `core/context.ts` | System/user context |
| `constants/prompts.ts` | System prompt assembly |
| `constants/systemPromptSections.ts` | Prompt sections |
| `services/api/` | API service layer |
| `services/api/bootstrap.ts` | Bootstrap data |
| `services/claudeAiLimits.ts` | Quota checking |
| `utils/auth.ts` | Authentication |
| `utils/api.ts` | API utilities |
| `utils/model/model.ts` | Model resolution |
| `utils/model/modelStrings.ts` | Model name strings |
| `utils/model/providers.ts` | Provider detection |
| `utils/thinking.ts` | Thinking configuration |
| `upstreamproxy/` | Upstream proxy |
