# Claude Code - Deep Architectural Analysis

## 1. System Overview

Claude Code is a ~1900-file TypeScript application that provides an interactive and programmatic interface to Claude's coding capabilities. It follows a **layered architecture** with clear separation between CLI entry points, state management, tool execution, and UI rendering.

### High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│                  Entry Points                     │
│  CLI (main.tsx) │ SDK │ MCP Server │ Bridge      │
├─────────────────────────────────────────────────┤
│               Command Router                      │
│  Commander.js → Slash Commands → Skills/Plugins  │
├─────────────────────────────────────────────────┤
│              State Management                     │
│  AppState → Store → onChangeAppState → Selectors  │
├─────────────────────────────────────────────────┤
│              Query Engine                         │
│  QueryEngine → API calls → Message processing    │
├─────────────────────────────────────────────────┤
│              Tool System                          │
│  Tool Registry → Permission Check → Execution    │
├─────────────────────────────────────────────────┤
│              UI Layer (Ink/React)                 │
│  REPL → Messages → Components → Terminal         │
├─────────────────────────────────────────────────┤
│              External Integrations                │
│  MCP Servers │ Bridge │ LSP │ Plugins │ Skills   │
└─────────────────────────────────────────────────┘
```

## 2. Entry Point Architecture

### 2.1 CLI Entry (`entrypoints/cli.tsx`)

The CLI entry point is a **fast-path dispatcher** that checks for special flags before loading the full application:

```typescript
// Fast-path routing - zero module loading for --version
if (args.length === 1 && (args[0] === '--version' || args[0] === '-v')) {
  console.log(`${MACRO.VERSION} (Claude Code)`)
  return
}
```

**Fast paths** (checked in order):
1. `--version` / `-v` → Immediate exit
2. `--dump-system-prompt` → Print system prompt (ant-only)
3. `--claude-in-chrome-mcp` → Chrome MCP server
4. `--daemon-worker=<kind>` → Worker subprocess
5. `remote-control` / `rc` → Bridge mode
6. `daemon` → Supervisor process
7. `ps` / `logs` / `attach` / `kill` → Session management
8. `new` / `list` / `reply` → Template jobs
9. `environment-runner` → BYOC runner
10. `self-hosted-runner` → Self-hosted runner
11. `--worktree --tmux` → Tmux worktree

If no fast path matches, it loads `main.tsx`.

### 2.2 Main Entry (`main.tsx`)

The `main()` function handles the core initialization sequence:

1. **Side-effect imports** run first (profile checkpoints, MDM reads, keychain prefetch)
2. **Commander.js** parses CLI arguments
3. **preAction hook** runs `init()`, migrations, remote settings
4. **setup()** handles worktree, directory changes, git operations
5. **Commands and agents** are loaded in parallel
6. **MCP configs** are resolved
7. **Trust dialog** is shown (interactive mode)
8. **REPL is launched** or `runHeadless()` is called

### 2.3 Initialization (`entrypoints/init.ts`)

The `init()` function (memoized, runs once) performs:

```typescript
export const init = memoize(async (): Promise<void> => {
  enableConfigs()                    // Validate & enable config system
  applySafeConfigEnvironmentVariables() // Safe env vars only
  setupGracefulShutdown()            // Exit handlers
  initialize1PEventLogging()         // Analytics
  populateOAuthAccountInfoIfNeeded() // Auth
  configureGlobalMTLS()             // mTLS settings
  configureGlobalAgents()            // Proxy configuration
  preconnectAnthropicApi()           // TCP warm-up
  // ... cleanup registrations
})
```

**Key design decision**: `init()` is memoized to prevent double initialization. It only applies *safe* environment variables; dangerous ones (PATH, LD_PRELOAD) are applied after trust is established.

## 3. State Management

### 3.1 AppState (`state/AppState.ts`)

The global state is an immutable object with ~40 top-level fields:

```typescript
export type AppState = DeepImmutable<{
  settings: SettingsJson           // User settings
  verbose: boolean
  mainLoopModel: ModelSetting      // Current model
  toolPermissionContext: ToolPermissionContext
  mcp: McpState                   // MCP connections
  plugins: PluginState             // Plugin state
  tasks: Record<string, TaskState> // Background tasks
  todos: Record<string, TodoList>  // Todo lists
  notifications: NotificationState
  teamContext?: TeamContext         // Agent swarms
  // ... more fields
}>
```

### 3.2 Store (`state/store.ts`)

A custom store implementation (not Redux, not Zustand):

```typescript
export function createStore(
  initialState: AppState,
  onChange?: (state: AppState, prev: AppState) => void
): Store
```

The store provides:
- `getState()` - Read current state
- `setState(updater)` - Update with function
- `onChange` callback for side effects

### 3.3 State Flow

```
User Input → REPL → QueryEngine → API → Tool Calls
                    ↓                        ↓
              setState(messages)      setState(tool results)
                    ↓                        ↓
              onChangeAppState → UI Re-render
```

## 4. Tool System Architecture

### 4.1 Tool Definition (`Tool.ts`)

Each tool is a typed object with:

```typescript
export type Tool = {
  name: string                    // Unique identifier
  description: string             // Model-facing description
  inputSchema: z.ZodSchema        // Zod validation schema
  userFacingName: (input) => string  // UI display name
  isEnabled: () => boolean        // Feature gate
  isDestructive: (input) => boolean // Safety classification
  needsPermissions: (input) => boolean // Permission check
  prompt: string                  // System prompt section
  call: (input, context) => AsyncGenerator<ToolCallResponse> // Execution
}
```

### 4.2 Tool Registration (`tools.ts`)

Tools are assembled from multiple sources:

```typescript
export function getAllBaseTools(): Tools {
  return [
    AgentTool, BashTool, FileEditTool, FileReadTool,
    FileWriteTool, GlobTool, GrepTool, WebFetchTool,
    WebSearchTool, TodoWriteTool, NotebookEditTool,
    SkillTool, EnterPlanModeTool, ExitPlanModeV2Tool,
    // ... conditional tools based on feature flags
  ]
}
```

### 4.3 Tool Execution Flow

```
Model outputs tool_use block
  ↓
Permission check (isDestructive? needsPermissions?)
  ↓
User approval (interactive) or auto-approve (plan mode)
  ↓
tool.call(input, toolUseContext)
  ↓
AsyncGenerator yields progress updates
  ↓
Final result → tool_result block → sent to API
```

### 4.4 Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| **File I/O** | Read, Edit, Write, Glob, Grep | File manipulation |
| **Shell** | Bash, PowerShell | Command execution |
| **Web** | WebFetch, WebSearch | Internet access |
| **Planning** | EnterPlanMode, ExitPlanMode, TodoWrite | Task planning |
| **Agents** | AgentTool, TaskCreate/Get/Update/List/Stop | Multi-agent |
| **MCP** | MCPTool, ListMcpResources, ReadMcpResource | MCP integration |
| **Communication** | SendMessage, AskUserQuestion | User interaction |
| **Skills** | SkillTool | Skill invocation |
| **Config** | ConfigTool, BriefTool | Configuration |

## 5. Query Engine

### 5.1 Core Loop (`QueryEngine.ts`)

The query engine drives the agentic loop:

```
1. Build messages array (system prompt + conversation)
2. Call Anthropic API with tools
3. Process response (text, tool_use blocks)
4. For each tool_use: check permissions → execute → collect results
5. Add tool_results to messages
6. Repeat until model stops using tools or max turns reached
```

### 5.2 System Prompt Construction

The system prompt is assembled from multiple sources:
- Base system prompt (`constants/prompts.ts`)
- CLAUDE.md files (user/project)
- Tool descriptions and schemas
- Agent-specific prompts
- MCP tool descriptions
- Thinking/effort configuration

## 6. Permission System

### 6.1 Permission Modes

```typescript
type PermissionMode =
  | 'default'      // Ask for each dangerous operation
  | 'plan'         // Enter plan mode first
  | 'bypassPermissions'  // Skip all (dangerous)
  | 'auto'         // AI classifier decides
```

### 6.2 Permission Flow

```
Tool call received
  ↓
Check deny rules (exact match, pattern, MCP prefix)
  ↓
If denied → Block tool, show denial message
  ↓
If allowed → Check if destructive
  ↓
If destructive → Show permission dialog
  ↓
User approves/denies → Execute or block
```

### 6.3 Rule System

Permissions use a rule-based system:
- **Allow rules**: `Bash(git:*)` allows all git commands
- **Deny rules**: `Bash(rm:*)` blocks all rm commands
- **MCP prefix**: `mcp__server__*` targets specific MCP server

## 7. REPL Architecture

### 7.1 Component Hierarchy

```
App
├── REPL
│   ├── PromptInput (text input with history)
│   ├── MessageList (virtualized scroll)
│   │   ├── UserMessage
│   │   ├── AssistantMessage
│   │   ├── ToolUseMessage
│   │   └── SystemMessage
│   ├── Spinner (loading indicator)
│   ├── PermissionDialog
│   ├── StatusBar
│   └── NotificationBar
└── Settings/Config overlays
```

### 7.2 Input Handling

```
Terminal input
  ↓
useInput hook (Ink)
  ↓
Keybinding resolution (vim mode, custom bindings)
  ↓
Command detection (/ prefix → slash command)
  ↓
Prompt submission → QueryEngine
```

### 7.3 Message Rendering

Messages are rendered as React components:
- **User messages**: Simple text display
- **Assistant messages**: Markdown rendering with code blocks
- **Tool use**: Expandable input/output display
- **Diffs**: Side-by-side or unified diff rendering

## 8. MCP Integration

### 8.1 Architecture

```
Claude Code
  ↓
MCP Client (per server)
  ↓
Transport (stdio / HTTP / SSE)
  ↓
MCP Server (external process)
  ↓
Tools / Resources / Prompts
```

### 8.2 MCP Lifecycle

1. **Discovery**: Read `.mcp.json`, user config, claude.ai connectors
2. **Connection**: Spawn stdio process or connect HTTP
3. **Capability negotiation**: Get tools, resources, prompts
4. **Tool registration**: MCP tools added to tool pool
5. **Call execution**: Route tool calls to MCP server
6. **Cleanup**: Graceful shutdown on exit

## 9. Plugin System

### 9.1 Plugin Structure

```
~/.claude/plugins/
  └── marketplace-name/
      └── plugin-name/
          ├── manifest.json
          ├── commands/
          ├── skills/
          └── ...
```

### 9.2 Plugin Lifecycle

1. **Discovery**: Scan plugin directories
2. **Validation**: Check manifest.json schema
3. **Loading**: Import commands, skills, MCP configs
4. **Activation**: Register with command/skill systems
5. **Hot reload**: Watch for changes, re-register

## 10. Remote Control Bridge

### 10.1 Architecture

```
Local CLI ←→ WebSocket ←→ Anthropic API ←→ claude.ai Web
                ↓
        Bridge Session
        ├── Inbound messages (web → CLI)
        ├── Outbound messages (CLI → web)
        └── File attachments
```

### 10.2 Key Components

- `bridgeMain.ts` - Entry point for bridge mode
- `initReplBridge.ts` - REPL bridge initialization
- `inboundMessages.ts` - Process web→CLI messages
- `bridgeApi.ts` - API communication
- `bridgePointer.ts` - Session pointer management

## 11. Skills System

### 11.1 Skill Types

1. **Bundled skills** (`skills/bundled/`): Built-in skills like `remember`, `debug`, `batch`
2. **Directory skills** (`~/.claude/skills/`): User-defined skill files
3. **Plugin skills**: Skills loaded from plugins
4. **MCP skills**: Prompt-type MCP commands

### 11.2 Skill Execution

```
User types /skill-name args
  ↓
Command lookup → Command type = 'prompt'
  ↓
getPromptForCommand(args, context)
  ↓
Generated prompt → sent as user message
  ↓
Model processes with full context
```

## 12. Background Task System

### 12.1 Task Types

```typescript
type TaskType =
  | 'local_bash'      // Background shell command
  | 'local_agent'     // Subagent
  | 'remote_agent'    // Remote subagent
  | 'in_process_teammate'  // In-process agent
  | 'local_workflow'  // Workflow execution
  | 'monitor_mcp'     // MCP monitor
  | 'dream'           // Dream task
```

### 12.2 Task Lifecycle

```
TaskCreate → pending → running → completed/failed/killed
  ↓
Output file written incrementally
  ↓
TaskOutputTool reads output
  ↓
TaskStopTool kills if needed
```

## 13. Key Design Decisions

### 13.1 Why Custom Store Instead of Redux
- Simpler API, no boilerplate
- Immutable state with `DeepImmutable<T>` type
- Direct `setState` for updates
- No middleware needed

### 13.2 Why Ink Custom Fork
- Needed virtual scrolling for large message lists
- Custom keybinding support (vim mode)
- Performance optimizations for terminal rendering
- Custom input handling

### 13.3 Why Memoized Init
- `init()` runs expensive operations (config parsing, proxy setup)
- Memoization prevents double initialization
- Safe to call from multiple entry points

### 13.4 Why Feature Flags
- `feature('KAIROS')` enables dead code elimination at build time
- Same codebase serves external, ant, and experimental builds
- `process.env.USER_TYPE === 'ant'` for runtime ant-only code

### 13.5 Why Async Generator for Tools
- Tools can yield progress updates during execution
- Natural streaming for long-running operations
- Clean cancellation via generator return

## 14. Performance Optimizations

### 14.1 Startup
- Profile checkpoints (`profileCheckpoint`) for timing
- Parallel initialization of independent systems
- Lazy loading of heavy modules (OpenTelemetry, gRPC)
- Eager flag parsing before full init

### 14.2 Runtime
- Memoization of expensive computations
- Virtual scrolling for message lists
- Deferred prefetches after first render
- MCP connection pooling and memoization

### 14.3 Context Window
- Message compaction when context fills up
- File content caching
- Selective CLAUDE.md loading
- Token counting for model-specific limits
