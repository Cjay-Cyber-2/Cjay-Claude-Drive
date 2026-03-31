# Claude Code - Design Patterns Catalog

## Pattern Summary Table

| # | Pattern | Location | Description |
|---|---------|----------|-------------|
| 1 | Memoized Singleton | `init.ts`, `commands.ts` | One-time expensive initialization |
| 2 | Feature Flag DCE | `bun:bundle` | Build-time dead code elimination |
| 3 | Async Generator Tool | `Tool.ts`, all tools | Streaming tool execution with progress |
| 4 | Permission Gate | `hooks/toolPermission/` | Pre-execution permission checking |
| 5 | Deny-first Security | `utils/permissions/` | Deny by default, allow explicitly |
| 6 | Command Registry | `commands.ts` | Declarative command registration |
| 7 | Skill/Command Unification | `commands.ts` | Skills and commands share same interface |
| 8 | State Machine | `state/` | Immutable state with typed transitions |
| 9 | React Context Providers | `context/` | Dependency injection for React tree |
| 10 | Lazy Module Loading | Throughout | Dynamic imports for heavy modules |
| 11 | MCP Tool Proxy | `services/mcp/` | Remote tools appear as local |
| 12 | Plugin Hot Reload | `services/plugins/` | Live plugin updates |
| 13 | Virtual Scroll | `ink/layout/` | Efficient terminal list rendering |
| 14 | Keybinding Layer | `keybindings/` | Composable keyboard shortcuts |
| 15 | Bridge Pointer | `bridge/` | Session pointer for remote access |
| 16 | Worker Pool | `tasks/` | Background task management |
| 17 | Observer Pattern | `state/onChangeAppState.ts` | State change notifications |
| 18 | Strategy Pattern | `utils/permissions/` | Configurable permission strategies |
| 19 | Builder Pattern | `constants/prompts.ts` | System prompt assembly |
| 20 | Chain of Responsibility | Permission handlers | Permission approval chain |
| 21 | Template Method | Tool implementations | Common tool execution skeleton |
| 22 | Adapter Pattern | `utils/sandbox/` | Sandbox platform abstraction |
| 23 | Facade Pattern | `setup.ts` | Simplified startup interface |
| 24 | Proxy Pattern | `bridge/bridgeApi.ts` | API call proxying |
| 25 | Decorator Pattern | Tool permission wrappers | Adding permission checks |

## Detailed Pattern Descriptions

### 1. Memoized Singleton

**Where**: `entrypoints/init.ts`, `commands.ts`, `utils/` (lodash `memoize`)

**Problem**: Expensive operations (config parsing, proxy setup, tool loading) should run once but may be called from multiple entry points.

**Solution**: Wrap the initialization function with `memoize()`:

```typescript
export const init = memoize(async (): Promise<void> => {
  enableConfigs()
  applySafeConfigEnvironmentVariables()
  setupGracefulShutdown()
  configureGlobalMTLS()
  configureGlobalAgents()
  preconnectAnthropicApi()
  // ...
})
```

**Variations**:
- `memoize()` from lodash-es for async functions
- Module-level `let` + guard for stateful singletons
- `const COMMANDS = memoize((): Command[] => [...])` for lazy evaluation

**Used in**: `init.ts`, `commands.ts` (COMMANDS, loadAllCommands), `state/store.ts`

---

### 2. Feature Flag Dead Code Elimination

**Where**: Throughout, using `feature()` from `bun:bundle`

**Problem**: Same codebase serves external users, internal (ant) users, and experimental features. Need conditional code that disappears at build time.

**Solution**: `feature()` calls that are resolved at build time:

```typescript
const SleepTool = feature('PROACTIVE') || feature('KAIROS')
  ? require('./tools/SleepTool/SleepTool.js').SleepTool
  : null
```

At build time, if `PROACTIVE` and `KAIROS` are disabled, the entire block is eliminated from the bundle. The `require()` inside the ternary means the module itself isn't loaded.

**Pattern**: Always use `require()` inside the feature-gated block (not `import`) to prevent static analysis from including the module.

**Used in**: `main.tsx`, `cli.tsx`, `commands.ts`, `tools.ts`, and throughout

---

### 3. Async Generator Tool Execution

**Where**: `Tool.ts`, all tool implementations

**Problem**: Tools may take seconds to execute. Need to report progress to the UI while executing, and support cancellation.

**Solution**: Tools use async generators that yield intermediate results:

```typescript
call: async function* (input: BashInput, context: ToolUseContext) {
  // Yield progress update
  yield { type: 'progress', data: { message: 'Running...' } }
  
  // Execute
  const result = await runCommand(input.command)
  
  // Yield final result
  yield {
    type: 'result',
    data: { result: formatResult(result) }
  }
}
```

**Benefits**:
- Progress updates during execution
- Natural cancellation (generator.return())
- Streaming for long operations
- Clean error handling

**Used in**: All 40+ tool implementations

---

### 4. Permission Gate Pattern

**Where**: `hooks/toolPermission/`, `utils/permissions/`

**Problem**: Some tool calls are dangerous (bash rm, file writes). Need to check permissions before execution.

**Solution**: A permission gate that intercepts tool calls:

```
Tool call received
  → checkDenyRules()     // Static deny list
  → checkAllowRules()    // Static allow list
  → needsPermissions()   // Tool says if it needs checking
  → isDestructive()      // Tool classifies danger level
  → showPermissionDialog() // Interactive approval
  → Execute or deny
```

**Three handlers**:
- `interactiveHandler.ts` - Show dialog, wait for user
- `coordinatorHandler.ts` - Coordinator auto-approves
- `swarmWorkerHandler.ts` - Worker permissions

**Used in**: `hooks/toolPermission/`, `permissions/` commands

---

### 5. Deny-first Security Model

**Where**: `utils/permissions/permissions.ts`, permission rules

**Problem**: Security must default to the most restrictive state.

**Solution**: All permission checks default to deny. Explicit rules are needed to allow:

```typescript
// Deny by default
if (hasDenyRule(permissionContext, tool)) {
  return { result: 'denied', message: 'Blocked by rule' }
}

// Check specific allow rules
if (hasAllowRule(permissionContext, tool)) {
  return { result: 'allowed' }
}

// Default: ask user
return { result: 'ask_user' }
```

**Rule format**: `ToolName(pattern)` e.g., `Bash(git:*)`, `mcp__server__tool`

---

### 6. Command Registry Pattern

**Where**: `commands.ts`, `commands/` directory

**Problem**: 80+ commands from different sources (built-in, skills, plugins, MCP) need unified registration and lookup.

**Solution**: Unified `Command` type with lazy loading:

```typescript
type Command = {
  type: 'prompt' | 'local' | 'local-jsx'
  name: string
  description: string
  source: 'builtin' | 'bundled' | 'plugin' | 'mcp'
  getPromptForCommand?: (args, context) => Promise<string>
  // ...
}
```

Commands are aggregated from:
1. Built-in (`COMMANDS()` memoized)
2. Skills (`getSkillDirCommands()`)
3. Plugins (`getPluginCommands()`)
4. Bundled skills (`getBundledSkills()`)
5. MCP prompts (via `mcp.commands`)

**Lookup**: `findCommand()` checks name, getCommandName(), and aliases.

---

### 7. Skill/Command Unification

**Where**: `commands.ts`, `skills/`

**Problem**: Skills (model-invocable) and commands (user-invocable) should share the same interface for simplicity.

**Solution**: Both are `Command` objects. The difference is in filtering:

```typescript
// User sees all commands
getCommands(cwd) // Returns all

// Model sees only prompt-type, non-disabled commands
getSkillToolCommands(cwd) // Filters to model-invocable
```

Skills are commands where:
- `type === 'prompt'`
- `source !== 'builtin'`
- `!disableModelInvocation`

---

### 8. Immutable State Machine

**Where**: `state/AppState.ts`, `state/store.ts`

**Problem**: Complex UI state needs predictable updates, undo/redo, and change detection.

**Solution**: Deep immutable state with typed transitions:

```typescript
export type AppState = DeepImmutable<{
  settings: SettingsJson
  tasks: Record<string, TaskState>
  mcp: McpState
  // ...
}>

// Update via function
setState(prev => ({
  ...prev,
  tasks: { ...prev.tasks, [id]: newTask }
}))
```

`DeepImmutable<T>` utility type ensures all nested objects are readonly.

---

### 9. React Context Providers

**Where**: `context/` directory (9 files)

**Problem**: Multiple subsystems need to inject state and callbacks into the React tree.

**Solution**: Context providers for each subsystem:

```typescript
// context/notifications.tsx
export const NotificationContext = createContext<NotificationState>()

// context/voice.tsx
export const VoiceContext = createContext<VoiceState>

// context/modalContext.tsx
export const ModalContext = createContext<ModalState>
```

**Pattern**: Provider wraps the app, consumer hooks read from context.

---

### 10. Lazy Module Loading

**Where**: Throughout, using dynamic `import()`

**Problem**: Some modules are large (OpenTelemetry ~400KB, gRPC ~700KB) and not always needed.

**Solution**: Dynamic imports where the module is actually used:

```typescript
// In init.ts - deferred until after trust
void Promise.all([
  import('../services/analytics/firstPartyEventLogger.js'),
  import('../services/analytics/growthbook.js'),
]).then(([fp, gb]) => {
  fp.initialize1PEventLogging()
})
```

**Variations**:
- `await import()` for sequential loading
- `void import()` for fire-and-forget
- Conditional `require()` inside feature blocks

---

### 11. MCP Tool Proxy

**Where**: `services/mcp/client.ts`, `tools/MCPTool/`

**Problem**: MCP servers expose tools that should appear as local tools to the model.

**Solution**: Dynamic tool registration:

```
MCP server connects
  → Get tools from server
  → Create proxy tool objects
  → Add to tool pool
  → Model sees them as regular tools
  → Calls are routed to MCP server
```

The MCP tool proxy wraps the MCP call in the standard `Tool` interface:

```typescript
{
  name: `mcp__${serverName}__${toolName}`,
  description: tool.description,
  inputSchema: z.object({...}),
  call: async function* (input) {
    const result = await mcpClient.callTool(toolName, input)
    yield { type: 'result', data: { result } }
  }
}
```

---

### 12. Plugin Hot Reload

**Where**: `services/plugins/`, `utils/plugins/`

**Problem**: Plugins should update without restarting the session.

**Solution**: File watching + re-registration:

1. Watch plugin directories for changes
2. On change: reload manifest, re-import commands
3. Clear caches (`clearPluginCommandCache()`)
4. Next command lookup picks up new versions

**Key files**:
- `pluginLoader.ts` - Load/clear plugin cache
- `installedPluginsManager.ts` - Version management
- `loadPluginCommands.ts` - Command loading

---

### 13. Virtual Scrolling (Terminal)

**Where**: `ink/layout/`, `hooks/useVirtualScroll.ts`

**Problem**: Terminal has limited rows. Can't render 1000+ messages at once.

**Solution**: Virtual scroll renders only visible rows:

```
All messages: [msg1, msg2, ..., msg1000]
Visible window: [msg950, ..., msg960]
Render: Only visible messages + scroll indicators
```

**Implementation**: Tracks scroll position, calculates visible range, renders subset.

---

### 14. Composable Keybinding Layers

**Where**: `keybindings/`, `hooks/useGlobalKeybindings.tsx`, `vim/`

**Problem**: Multiple keybinding systems (vim mode, custom bindings, default) need to coexist.

**Solution**: Layered keybinding resolution:

```
Key pressed
  → Vim transitions (if vim mode)
  → Global keybindings (Ctrl+C, etc.)
  → Command keybindings (/command shortcuts)
  → Default input handling
```

Each layer can consume or pass through the key event.

---

### 15. Bridge Pointer Pattern

**Where**: `bridge/bridgePointer.ts`

**Problem**: Remote sessions need a stable reference to local sessions that can survive reconnections.

**Solution**: Session pointers (URLs) that map to local session IDs:

```
Local session: abc-123
Bridge pointer: https://claude.ai/s/xyz-789
Mapping: xyz-789 → abc-123 (stored locally)
```

The pointer includes auth tokens and can be refreshed.

---

### 16. Worker Pool / Background Tasks

**Where**: `tasks/`, `Task.ts`

**Problem**: Long-running operations (bash commands, subagents) need to run in background.

**Solution**: Task abstraction with typed handles:

```typescript
type TaskState = {
  id: string
  type: TaskType
  status: 'pending' | 'running' | 'completed' | 'failed' | 'killed'
  outputFile: string  // Output written incrementally
  // ...
}
```

Tasks are created via `TaskCreateTool`, monitored via `TaskOutputTool`, and stopped via `TaskStopTool`.

---

### 17. Observer Pattern (State Changes)

**Where**: `state/onChangeAppState.ts`

**Problem**: Need to react to state changes for side effects (logging, notifications).

**Solution**: `onChange` callback on the store:

```typescript
const store = createStore(initialState, onChangeAppState)

function onChangeAppState(state: AppState, prev: AppState) {
  if (state.tasks !== prev.tasks) {
    // Task state changed
    updateTaskUI()
  }
  if (state.mcp.clients !== prev.mcp.clients) {
    // MCP connection changed
    logMcpEvent()
  }
}
```

---

### 18. Strategy Pattern (Permissions)

**Where**: `utils/permissions/PermissionMode.ts`

**Problem**: Different permission modes need different behaviors.

**Solution**: Strategy interface with mode-specific implementations:

```typescript
// Strategy selection based on mode
switch (permissionContext.mode) {
  case 'default': return interactiveHandler(...)
  case 'plan': return coordinatorHandler(...)
  case 'auto': return autoModeHandler(...)
  case 'bypassPermissions': return { result: 'allowed' }
}
```

---

### 19. Builder Pattern (System Prompt)

**Where**: `constants/prompts.ts`, `utils/systemPromptType.ts`

**Problem**: System prompt is assembled from many sources (base, CLAUDE.md, tools, agents, MCP).

**Solution**: Builder that collects sections:

```typescript
const sections: string[] = []
sections.push(basePrompt)
sections.push(toolDescriptions)
sections.push(claudeMdContent)
sections.push(agentPrompt)
sections.push(mcpToolDescriptions)
return sections.join('\n\n')
```

---

### 20. Chain of Responsibility (Permissions)

**Where**: `hooks/toolPermission/handlers/`

**Problem**: Permission requests need to flow through multiple handlers.

**Solution**: Handler chain:

```
Permission request
  → interactiveHandler (show dialog?)
  → coordinatorHandler (auto-approve?)
  → swarmWorkerHandler (worker rules?)
  → Default: deny
```

Each handler returns `{ result: 'handled' }` or passes to next.

---

### 21. Template Method (Tool Execution)

**Where**: `Tool.ts`, all tool implementations

**Problem**: Tools share common execution structure but differ in implementation.

**Solution**: Common interface with tool-specific implementations:

```typescript
// Common structure (Template)
type Tool = {
  name: string           // Always present
  description: string    // Always present
  inputSchema: z.Schema  // Always present
  call: () => Generator  // Always present, varies per tool
  isEnabled: () => bool  // Always present
  needsPermissions: () => bool  // Always present
  isDestructive: () => bool     // Always present
}
```

Each tool fills in the template with its specific logic.

---

### 22. Adapter Pattern (Sandbox)

**Where**: `utils/sandbox/sandbox-adapter.ts`

**Problem**: Sandbox implementation varies by platform (Docker, VM, none).

**Solution**: Adapter interface:

```typescript
class SandboxManager {
  static isSandboxingEnabled(): boolean
  static areUnsandboxedCommandsAllowed(): boolean
  static isAutoAllowBashIfSandboxedEnabled(): boolean
}
```

Platform-specific code is hidden behind the adapter.

---

### 23. Facade Pattern (Setup)

**Where**: `setup.ts`

**Problem**: Startup involves many complex operations (git, worktree, plugins, hooks).

**Solution**: Single `setup()` function that orchestrates everything:

```typescript
export async function setup(
  cwd: string,
  permissionMode: PermissionMode,
  worktreeEnabled: boolean,
  // ...
): Promise<void> {
  // Orchestrate all setup steps
  await setupGit()
  await setupWorktree()
  await setupPlugins()
  await setupHooks()
  // ...
}
```

---

### 24. Proxy Pattern (Bridge API)

**Where**: `bridge/bridgeApi.ts`

**Problem**: Remote API calls need to be proxied through the bridge.

**Solution**: API proxy that wraps remote calls:

```typescript
// Local call → Bridge → Remote API → Response → Local
async function bridgeApiCall(method: string, params: any) {
  const response = await fetch(bridgeUrl, {
    method: 'POST',
    body: JSON.stringify({ method, params }),
    headers: { Authorization: `Bearer ${token}` }
  })
  return response.json()
}
```

---

### 25. Decorator Pattern (Permission Wrappers)

**Where**: `utils/permissions/`

**Problem**: Some tools need additional permission checking beyond the base.

**Solution**: Permission wrappers that decorate tool calls:

```typescript
// Base tool
const bashTool = { call: runCommand, ... }

// Decorated with permission check
const decoratedTool = {
  ...bashTool,
  call: async function* (input, context) {
    const permission = await checkPermission(input)
    if (permission.result !== 'allowed') {
      yield { type: 'result', data: { error: 'Denied' } }
      return
    }
    yield* bashTool.call(input, context)
  }
}
```
