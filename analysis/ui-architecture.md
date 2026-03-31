# UI Architecture - Deep Dive

## Overview

Claude Code's UI is built on a custom fork of **Ink** (React for terminals). It renders a rich interactive TUI with message lists, input fields, permission dialogs, and status indicators.

## Component Hierarchy

```
Root (ink.ts - createRoot)
└── App (components/App.tsx)
    ├── SettingsProvider (context)
    ├── NotificationProvider (context)
    ├── ModalProvider (context)
    ├── REPL (main component)
    │   ├── StatusBar
    │   │   ├── Model indicator
    │   │   ├── Permission mode
    │   │   ├── MCP status
    │   │   └── Session info
    │   ├── MessageList (virtualized)
    │   │   ├── UserMessage
    │   │   ├── AssistantMessage
    │   │   │   ├── TextContent
    │   │   │   ├── CodeBlock (with syntax highlighting)
    │   │   │   └── Markdown rendering
    │   │   ├── ToolUseMessage
    │   │   │   ├── Tool input display
    │   │   │   ├── Tool progress
    │   │   │   └── Tool result
    │   │   └── SystemMessage
    │   ├── PromptInput
    │   │   ├── TextInput (with history)
    │   │   ├── Autocomplete dropdown
    │   │   └── File suggestions
    │   ├── Spinner (loading indicator)
    │   ├── PermissionDialog (when needed)
    │   ├── NotificationBar
    │   └── Footer
    ├── HelpOverlay (/help)
    ├── SettingsOverlay (/config)
    └── ResumeDialog (/resume)
```

## Ink Custom Fork

Claude Code uses a custom fork of Ink with:

### Virtual Scrolling (`ink/layout/`)
- Only renders visible rows
- Handles large message lists efficiently
- Scroll position tracking

### Key Input Handling (`ink/events/`)
- Custom key event processing
- Keybinding resolution chain
- Vim mode integration

### Terminal I/O (`ink/termio/`)
- Raw mode management
- Cursor control
- Color support detection

## Message Rendering Pipeline

```
Message received
  ↓
Parse content blocks (text, tool_use, tool_result)
  ↓
For each block:
  - Text → Markdown renderer
  - Code → Syntax highlighter (HighlightedCode component)
  - Tool use → ToolUseMessage component
  - Diff → StructuredDiff component
  ↓
Apply theme colors
  ↓
Measure terminal width
  ↓
Wrap and render to terminal
```

## Input System

### Text Input (`hooks/useTextInput.ts`)
- Cursor position tracking
- History navigation (up/down arrows)
- Autocomplete for commands and files
- Multi-line support

### Keybinding Resolution
```
Key pressed
  → Vim transitions (if vim mode active)
  → Global keybindings (Ctrl+C, Ctrl+L, etc.)
  → Command keybindings (/ shortcuts)
  → Default text input handling
```

### File Suggestions (`hooks/fileSuggestions.ts`)
- `@` triggers file path autocomplete
- Fuzzy matching against workspace files
- Shows path suggestions in dropdown

## Performance Optimizations

### Virtual Scroll
Only visible messages are rendered. For a 1000-message conversation:
```
All messages: [msg1, msg2, ..., msg1000]
Visible (20 rows): [msg980, ..., msg1000]
Render: Only 20 components
```

### Memoization
- `React.memo` on message components
- `useMemo` for expensive computations
- `useCallback` for stable function references

### Deferred Rendering
- First render shows skeleton
- Content fills in asynchronously
- Spinner shows during loading

## Theme System

Themes are defined in `utils/theme.ts`:

```typescript
type Theme = {
  name: ThemeName
  colors: {
    user: string
    assistant: string
    tool: string
    error: string
    warning: string
    success: string
    // ...
  }
}
```

Themes are applied via chalk terminal colors.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Enter | Submit prompt |
| Ctrl+C | Cancel / Exit |
| Ctrl+L | Clear screen |
| Up/Down | History navigation |
| Tab | Autocomplete |
| Escape | Cancel input |
| Ctrl+R | History search |

## Key Files

| File | Purpose |
|------|---------|
| `ink.ts` | Root creation, mount point |
| `ink/components/` | Ink component library |
| `ink/events/` | Event handling |
| `ink/layout/` | Virtual scroll, layout |
| `ink/termio/` | Terminal I/O |
| `components/App.tsx` | Main app component |
| `components/PromptInput/` | Input field |
| `components/messages/` | Message rendering |
| `components/Spinner/` | Loading indicators |
| `components/permissions/` | Permission dialogs |
| `components/diff/` | Diff rendering |
| `hooks/useTextInput.ts` | Text input logic |
| `hooks/useVirtualScroll.ts` | Virtual scroll logic |
| `hooks/useGlobalKeybindings.tsx` | Keybindings |
| `utils/theme.ts` | Theme definitions |
