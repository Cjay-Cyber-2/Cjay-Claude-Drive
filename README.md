# Claude Code - Comprehensive Architecture Analysis

> **The definitive reference for Claude Code's internal architecture, patterns, and design decisions.**

This repository contains the complete organized source code of **Claude Code** (Anthropic's official CLI coding assistant), along with professional-grade architectural analysis documents covering every major subsystem.

## What is Claude Code?

Claude Code is a terminal-based agentic coding assistant by Anthropic. It wraps Claude's API with a rich set of tools (file editing, bash execution, web search, MCP integration, etc.) inside an interactive TUI built with a custom fork of **Ink** (React for terminals). It supports:

- **Interactive REPL** with rich message rendering, syntax highlighting, and diff views
- **Headless/SDK mode** (`-p/--print`) for programmatic and pipe-based usage
- **MCP (Model Context Protocol)** for extensible tool integration
- **Remote Control** (bridge mode) connecting CLI to claude.ai/web
- **Agent Swarms** with multi-agent coordination
- **Vim mode** for power-user keybindings
- **Plugin system** for third-party extensions
- **Skills system** for reusable prompt-based commands
- **Voice mode** for hands-free interaction
- **IDE integration** (VS Code, JetBrains)

## Repository Structure

```
Anas-Claude-Train/
├── README.md                    # This file - master overview
├── ARCHITECTURE.md              # Deep architectural analysis
├── PATTERNS.md                  # All design patterns found
├── src/                         # Source code organized by domain
│   ├── core/                    # Main entrypoint, bootstrap, core types
│   ├── entrypoints/             # CLI entry, SDK types, MCP entry, init
│   ├── tools/                   # All 40+ tool implementations
│   ├── commands/                # All 80+ CLI slash commands
│   ├── ui/                      # React/Ink UI components (389 files)
│   ├── services/                # Background services & integrations
│   ├── bridge/                  # Remote Control bridge system
│   ├── hooks/                   # React hooks (104 files)
│   ├── utils/                   # Utility modules (564 files)
│   ├── types/                   # TypeScript type definitions
│   ├── constants/               # Constants, prompts, configs
│   ├── keybindings/             # Keybinding system
│   ├── vim/                     # Vim mode implementation
│   ├── ink/                     # Custom Ink rendering engine fork
│   ├── plugins/                 # Plugin loading system
│   ├── skills/                  # Skills & bundled skills
│   ├── migrations/              # Data migration scripts
│   ├── state/                   # Global state management
│   ├── context/                 # React context providers
│   ├── tasks/                   # Background task system
│   ├── remote/                  # Remote session management
│   ├── assistant/               # Assistant/Kairos mode
│   ├── coordinator/             # Coordinator mode (multi-agent)
│   ├── voice/                   # Voice mode integration
│   ├── cli/                     # CLI handlers & transports
│   ├── server/                  # Direct connect server
│   ├── bootstrap/               # Bootstrap state management
│   ├── screens/                 # Setup/onboarding screens
│   ├── query/                   # Query engine internals
│   ├── schemas/                 # Validation schemas
│   └── ...                      # More categories
├── analysis/                    # Detailed analysis documents
│   ├── file-index.md            # Every file with description
│   ├── tool-system.md           # Tools deep dive
│   ├── session-bridge.md        # Bridge/session analysis
│   ├── permission-system.md     # Permissions deep dive
│   ├── mcp-integration.md       # MCP analysis
│   ├── plugin-system.md         # Plugin architecture
│   ├── ui-architecture.md       # UI/Ink analysis
│   ├── api-integration.md       # API integration
│   ├── voice-system.md          # Voice mode
│   ├── keybinding-vim.md        # Keybinding & vim
│   └── state-management.md      # State management
└── patterns/                    # Pattern catalog
    ├── summary.md               # Pattern summary table
    └── [individual patterns]
```

## Key Architectural Highlights

### 1. Dual-Mode Architecture
Claude Code runs in two fundamentally different modes:
- **Interactive (REPL)**: Full TUI with Ink rendering, keyboard input, live updates
- **Headless (`-p`)**: Stream-json/text output for pipes and programmatic use

Both modes share the same core query engine, tool system, and permission logic.

### 2. Tool System
Over 40 built-in tools covering file operations, shell execution, web search, MCP integration, agent coordination, and more. Tools are registered via a declarative `Tool` type with Zod schemas, permission checks, and progress reporting.

### 3. State Management
A custom store pattern (not Redux) with immutable `AppState`, `setState` for updates, and reactive selectors. State flows through React Context providers and is consumed by hooks.

### 4. Plugin & Skills System
Extensible via plugins (marketplace-based) and skills (prompt-based commands). Both support hot-reloading, versioning, and MCP tool integration.

### 5. Remote Control Bridge
Bidirectional connection between local CLI and claude.ai/web, enabling mobile control of local sessions. Uses WebSocket for real-time message passing.

## File Statistics

| Category | File Count |
|----------|-----------|
| Tools | 184 |
| Commands | 208 |
| UI Components | 389 |
| Services | 130 |
| Hooks | 104 |
| Utilities | 564 |
| Ink Engine | 96 |
| Bridge | 31 |
| **Total** | **~1,900** |

## Getting Started

Read the analysis documents in order:
1. `ARCHITECTURE.md` - Start here for the big picture
2. `analysis/tool-system.md` - Understand the core tool execution model
3. `analysis/ui-architecture.md` - How the TUI renders
4. `PATTERNS.md` - All design patterns cataloged
5. Individual analysis files as needed

## Technical Stack

- **Language**: TypeScript
- **Runtime**: Bun (native binary) or Node.js
- **UI Framework**: React + Ink (custom fork)
- **Schema Validation**: Zod
- **API Client**: Anthropic SDK
- **CLI Framework**: Commander.js
- **Styling**: chalk (terminal colors)
- **MCP**: Model Context Protocol SDK
