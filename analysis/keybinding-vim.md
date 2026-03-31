# Keybinding & Vim Mode - Deep Dive

## Overview

Claude Code supports both standard terminal keybindings and a full vim mode for power users. The keybinding system is composable and extensible.

## Architecture

```
Terminal Input
  ↓
ink/events/ (raw key events)
  ↓
Keybinding Resolution Chain:
  1. Vim transitions (if enabled)
  2. Global keybindings
  3. Command keybindings
  4. Default input handling
  ↓
Action execution
```

## Vim Mode

### State Machine (`vim/transitions.ts`)

Vim mode implements a state machine with:

**Modes**:
- **Normal** (default): Navigation and commands
- **Insert**: Text input
- **Visual**: Text selection
- **Command**: Ex commands (`:`)

**State transitions**:
```typescript
// vim/transitions.ts
const transitions = {
  normal: {
    'i': 'insert',      // Enter insert mode
    'v': 'visual',      // Enter visual mode
    ':': 'command',     // Enter command mode
    'h': 'cursorLeft',  // Move left
    'j': 'historyDown', // History down
    'k': 'historyUp',   // History up
    'l': 'cursorRight', // Move right
    'w': 'wordForward', // Next word
    'b': 'wordBack',    // Previous word
    'dd': 'deleteLine', // Delete line
    'yy': 'yankLine',   // Yank line
    // ...
  },
  insert: {
    'Escape': 'normal', // Return to normal mode
    // All regular input keys pass through
  }
}
```

### Motions (`vim/motions.ts`)

Vim motions for navigation:
```typescript
const motions = {
  h: (cursor) => cursor - 1,
  l: (cursor) => cursor + 1,
  w: (text, cursor) => findNextWord(text, cursor),
  b: (text, cursor) => findPrevWord(text, cursor),
  0: () => 0,                    // Beginning of line
  $: (text) => text.length,      // End of line
  gg: () => 0,                   // Beginning of input
  G: (text) => text.length,      // End of input
}
```

### Operators (`vim/operators.ts`)

Vim operators for text manipulation:
```typescript
const operators = {
  d: 'delete',    // Delete operator
  y: 'yank',      // Copy operator
  c: 'change',    // Change operator
  // Combined with motions: dw, dd, yy, etc.
}
```

### Text Objects (`vim/textObjects.ts`)

Text objects for selection:
```typescript
const textObjects = {
  iw: 'inner word',
  aw: 'a word',
  i": 'inner quotes',
  a": 'a quotes',
  // ...
}
```

## Global Keybindings

### hooks/useGlobalKeybindings.tsx

```typescript
const globalKeybindings = {
  'ctrl+c': () => cancelOrExit(),
  'ctrl+l': () => clearScreen(),
  'ctrl+r': () => historySearch(),
  'tab': () => autocomplete(),
  // ...
}
```

### hooks/useExitOnCtrlCD.ts

Double Ctrl+C exits:
```typescript
// First Ctrl+C: cancel current operation
// Second Ctrl+C within timeout: exit
```

## Command Keybindings

### hooks/useCommandKeybindings.tsx

Custom keybindings for commands:
```typescript
// Configurable via settings.json
{
  "keybindings": {
    "ctrl+k": "/clear",
    "ctrl+e": "/help"
  }
}
```

## Key Files

| File | Purpose |
|------|---------|
| `vim/transitions.ts` | Vim state machine |
| `vim/motions.ts` | Vim motions |
| `vim/operators.ts` | Vim operators |
| `vim/textObjects.ts` | Text objects |
| `vim/types.ts` | Vim type definitions |
| `keybindings/` | Keybinding system |
| `hooks/useGlobalKeybindings.tsx` | Global keybindings |
| `hooks/useCommandKeybindings.tsx` | Command keybindings |
| `hooks/useExitOnCtrlCD.ts` | Ctrl+C/D handling |
| `hooks/useVimInput.ts` | Vim input handling |
| `hooks/useInputBuffer.ts` | Input buffer |
| `ink/events/` | Event handling |
| `commands/vim/` | Vim toggle command |
| `commands/keybindings/` | Keybinding command |
