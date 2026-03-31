# State Management - Deep Dive

## Overview

Claude Code uses a custom immutable state management system (not Redux or Zustand). The state flows through a single `AppState` object managed by a custom store.

## Architecture

```
┌─────────────────────────────────────────────┐
│                AppState                      │
│  (DeepImmutable object, ~40 fields)         │
├─────────────────────────────────────────────┤
│            Store (state/store.ts)            │
│  - getState() → AppState                    │
│  - setState(updater) → triggers onChange    │
│  - onChange callback for side effects       │
├─────────────────────────────────────────────┤
│         onChangeAppState                     │
│  - React to specific state changes          │
│  - Trigger side effects                     │
├─────────────────────────────────────────────┤
│          Selectors (state/selectors.ts)      │
│  - Derived state computations               │
│  - Memoized getters                         │
├─────────────────────────────────────────────┤
│            React Context                     │
│  - AppStateContext for components           │
│  - Store context for hooks                  │
└─────────────────────────────────────────────┘
```

## AppState Structure

```typescript
export type AppState = DeepImmutable<{
  // Core
  settings: SettingsJson
  verbose: boolean
  mainLoopModel: ModelSetting
  mainLoopModelForSession: ModelSetting
  isBriefOnly: boolean
  
  // Permissions
  toolPermissionContext: ToolPermissionContext
  
  // MCP
  mcp: {
    clients: MCPServerConnection[]
    tools: Tool[]
    commands: Command[]
    resources: Record<string, ServerResource[]>
    pluginReconnectKey: number
  }
  
  // Plugins
  plugins: {
    enabled: LoadedPlugin[]
    disabled: LoadedPlugin[]
    commands: Command[]
    errors: PluginError[]
    installationStatus: InstallationStatus
    needsRefresh: boolean
  }
  
  // Tasks
  tasks: Record<string, TaskState>
  
  // Todos
  todos: Record<string, TodoList>
  
  // UI
  expandedView: 'none' | 'tasks' | 'teammates'
  notifications: NotificationState
  statusLineText: string | undefined
  
  // Agent
  agent: string | undefined
  agentDefinitions: AgentDefinitionsResult
  agentNameRegistry: Map<string, string>
  
  // Thinking
  thinkingEnabled: boolean
  
  // Session
  initialMessage: { message: UserMessage } | null
  
  // Remote
  remoteSessionUrl: string | undefined
  remoteConnectionStatus: 'connecting' | 'connected' | 'disconnected'
  replBridgeEnabled: boolean
  
  // Teams
  teamContext?: TeamContext
  
  // Speculation
  speculation: SpeculationState
  
  // And more...
}>
```

## Store Implementation

```typescript
// state/store.ts
export function createStore(
  initialState: AppState,
  onChange?: (state: AppState, prev: AppState) => void
): Store {
  let state = initialState
  
  return {
    getState: () => state,
    setState: (updater) => {
      const prev = state
      state = typeof updater === 'function' ? updater(prev) : updater
      onChange?.(state, prev)
    }
  }
}
```

## State Update Flow

```
1. Component calls store.setState(updater)
   ↓
2. Updater function receives prev state
   ↓
3. Returns new immutable state
   ↓
4. onChangeAppState callback fires
   ↓
5. React re-renders components that read from store
```

## onChangeAppState

The `onChangeAppState` function reacts to specific state changes:

```typescript
function onChangeAppState(state: AppState, prev: AppState) {
  // Task state changed → update task UI
  if (state.tasks !== prev.tasks) {
    handleTaskChange(state.tasks, prev.tasks)
  }
  
  // MCP clients changed → log event
  if (state.mcp.clients !== prev.mcp.clients) {
    logMcpConnectionEvent(state.mcp.clients)
  }
  
  // Permission mode changed → notify
  if (state.toolPermissionContext.mode !== prev.toolPermissionContext.mode) {
    logPermissionModeChange(state.toolPermissionContext.mode)
  }
}
```

## Selectors

Derived state computations:

```typescript
// state/selectors.ts
export function getActiveTasks(state: AppState): TaskState[] {
  return Object.values(state.tasks).filter(t => t.status === 'running')
}

export function getEnabledPlugins(state: AppState): LoadedPlugin[] {
  return state.plugins.enabled
}

export function getConnectedMcpClients(state: AppState): MCPServerConnection[] {
  return state.mcp.clients.filter(c => c.type === 'connected')
}
```

## Bootstrap State

Global mutable state that doesn't fit in AppState:

```typescript
// bootstrap/state.ts
let _cwd: string
let _sessionId: string
let _isInteractive: boolean
let _originalCwd: string
// ...

export function setCwd(cwd: string) { _cwd = cwd }
export function getCwd() { return _cwd }
export function getSessionId() { return _sessionId }
```

This state includes:
- Current working directory
- Session ID
- Interactive mode flag
- Client type
- Model overrides
- And more

## Key Files

| File | Purpose |
|------|---------|
| `state/AppState.ts` | AppState type definition |
| `state/AppStateStore.ts` | Store creation |
| `state/store.ts` | Store implementation |
| `state/onChangeAppState.ts` | Change reactions |
| `state/selectors.ts` | Derived state |
| `state/teammateViewHelpers.ts` | Team state helpers |
| `bootstrap/state.ts` | Global mutable state |
| `context/` | React context providers |
