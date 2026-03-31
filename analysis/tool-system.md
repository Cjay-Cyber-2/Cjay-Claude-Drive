# Tool System - Deep Dive

## Overview

The tool system is Claude Code's core execution engine. It defines 40+ tools that the model can invoke, each with schema validation, permission checking, and progress reporting.

## Architecture

### Tool Definition (`src/core/Tool.ts`)

Every tool implements the `Tool` interface:

```typescript
export type Tool = {
  name: string                              // Unique ID (e.g., "Bash")
  description: string                       // Model-facing description (sent in system prompt)
  inputSchema: z.ZodSchema                  // Zod schema for input validation
  userFacingName: (input) => string         // UI display name (e.g., "Bash(git status)")
  isEnabled: () => boolean                  // Feature gate
  isDestructive: (input) => boolean         // Is this operation destructive?
  needsPermissions: (input) => boolean      // Does this need user approval?
  prompt: string                            // System prompt section for this tool
  call: (input, context) => AsyncGenerator<ToolCallResponse> // Execute the tool
  renderToolUseMessage?: (input, options) => string  // How to show in UI
  renderToolResultMessage?: (result) => string       // Result display
}
```

### Tool Permission Context

```typescript
export type ToolPermissionContext = {
  mode: PermissionMode
  allowedTools: string[]        // --allowedTools flag
  disallowedTools: string[]     // --disallowedTools flag
  additionalWorkingDirectories: AdditionalWorkingDirectory[]
  rules: PermissionRule[]       // Allow/deny rules
}
```

## Tool Categories

### File I/O Tools
- **FileReadTool**: Read file contents with offset/limit
- **FileEditTool**: Edit files with old_string/new_string replacement
- **FileWriteTool**: Write entire files
- **GlobTool**: Find files matching patterns
- **GrepTool**: Search file contents with ripgrep

### Shell Tools
- **BashTool**: Execute shell commands with sandbox support
- **PowerShellTool**: Windows PowerShell execution (optional)

### Web Tools
- **WebFetchTool**: Fetch URLs and extract content
- **WebSearchTool**: Brave Search API integration

### Planning Tools
- **EnterPlanModeTool**: Enter plan mode (read-only)
- **ExitPlanModeV2Tool**: Exit plan mode with plan approval
- **TodoWriteTool**: Manage todo lists

### Agent Tools
- **AgentTool**: Spawn subagents
- **TaskCreateTool/TaskGetTool/TaskUpdateTool/TaskListTool/TaskStopTool/TaskOutputTool**: Task management

### MCP Tools
- **MCPTool**: Call MCP server tools
- **ListMcpResourcesTool**: List MCP resources
- **ReadMcpResourceTool**: Read MCP resources

### Communication Tools
- **SendMessageTool**: Send messages to user (brief mode)
- **AskUserQuestionTool**: Ask user questions

### Config Tools
- **ConfigTool**: Manage settings (ant-only)
- **SkillTool**: Invoke skills
- **BriefTool**: Brief mode communication

## Execution Flow

```
1. Model outputs tool_use block:
   { type: "tool_use", id: "toolu_123", name: "Bash", input: { command: "ls" } }

2. Permission Check:
   a. Check deny rules (exact match, pattern, MCP prefix)
   b. Check allow rules
   c. Check isDestructive() → needsPermissions()
   d. If dangerous → show permission dialog
   e. User approves/denies

3. Execution:
   const generator = tool.call(input, toolUseContext)
   for await (const response of generator) {
     if (response.type === 'progress') updateUI(response.data)
     if (response.type === 'result') collectResult(response.data)
   }

4. Result Processing:
   - Format result for display
   - Add to messages array
   - Send tool_result to API
```

## Permission Integration

Each tool declares its permission requirements:

```typescript
// BashTool
isDestructive: (input) => {
  const cmd = input.command.toLowerCase()
  return cmd.includes('rm ') || cmd.includes('sudo ')
}

needsPermissions: (input) => {
  return this.isDestructive(input) || !isInAllowList(input)
}
```

## Tool Pool Assembly

```typescript
// tools.ts
export function assembleToolPool(permissionContext, mcpTools) {
  const builtInTools = getTools(permissionContext)    // Built-in tools
  const allowedMcpTools = filterToolsByDenyRules(mcpTools, permissionContext)
  
  // Deduplicate (built-in wins on name conflict)
  return uniqBy([...builtInTools, ...allowedMcpTools], 'name')
}
```

## Key Files

| File | Purpose |
|------|---------|
| `core/Tool.ts` | Tool type definitions, permission types |
| `tools.ts` | Tool registry, filtering, assembly |
| `tools/*/` | Individual tool implementations |
| `tools/shared/` | Shared tool utilities |
| `hooks/toolPermission/` | Permission handling |
| `utils/permissions/` | Permission utilities |
