# File Index

Complete index of all ~1900 source files organized by category.

## Core (16 files)
| File | Description |
|------|-------------|
| `main.tsx` | Main CLI entry point, ~4600 lines orchestrating startup |
| `Tool.ts` | Tool type definitions, permission types |
| `Task.ts` | Task type definitions, ID generation |
| `QueryEngine.ts` | Core agentic loop |
| `context.ts` | System/user context gathering |
| `cost-tracker.ts` | Token cost tracking |
| `costHook.ts` | Cost tracking hook |
| `history.ts` | Prompt history |
| `ink.ts` | Ink root creation |
| `interactiveHelpers.tsx` | Interactive mode helpers |
| `dialogLaunchers.tsx` | Dialog launchers |
| `replLauncher.tsx` | REPL launch |
| `setup.ts` | Session setup |
| `projectOnboardingState.ts` | Onboarding tracking |
| `tasks.ts` | Task utilities |
| `query.ts` | Query utilities |

## Tools (184 files)
40+ tool implementations across subdirectories. Each tool contains:
- Main implementation (.ts)
- Schema definitions
- Permission logic
- Optional UI components

**Key tools**: BashTool, FileEditTool, FileReadTool, FileWriteTool, GlobTool, GrepTool, WebFetchTool, WebSearchTool, AgentTool, MCPTool, SkillTool

## Commands (208 files)
80+ slash commands. Each command has its own directory with index.ts.

**Categories**: Session, Config, MCP, Dev, Skills, Agents, Review

## UI Components (389 files)
React/Ink components for the terminal UI.

**Categories**: Messages, Input, Spinner, Permissions, Diff, Settings, Agents, MCP, Tasks, Memory

## Services (130 files)
Background services and integrations.

**Key services**: MCP client, analytics, plugins, settings sync, LSP, OAuth

## Hooks (104 files)
React hooks for the REPL UI.

**Categories**: Input, Keybindings, Commands, Tools, Session, Notifications, Permissions, MCP, Voice

## Utilities (564 files)
The largest module with helpers, platform abstractions, and utility functions.

**Categories**: Config, Auth, Git, Permissions, Shell, FS, MCP, Plugins, Skills, Process, Model, Telemetry, Swarm

## Ink Engine (96 files)
Custom Ink fork with virtual scrolling, key handling, and layout optimizations.

## Bridge (31 files)
Remote Control bridge connecting local CLI to claude.ai/web.

## Other Categories
- **Keybindings** (14 files): Keybinding system
- **Vim** (5 files): Vim mode implementation
- **Constants** (21 files): Application constants
- **Types** (11 files): TypeScript type definitions
- **State** (6 files): Global state management
- **Context** (9 files): React context providers
- **Migrations** (11 files): Data migration scripts
- **Skills** (20 files): Skill loading and bundled skills
- **Plugins** (2 files): Plugin system
- **Tasks** (12 files): Background task system
- **Remote** (4 files): Remote session management
- **Entrypoints** (8 files): CLI, SDK, MCP entry points
- **Bootstrap** (1 file): Bootstrap state
- **Screens** (3 files): Setup/onboarding screens
- **Query** (4 files): Query engine internals
- **CLI** (19 files): CLI handlers and transports
- **Server** (3 files): Direct connect server
