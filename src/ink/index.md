# Ink Module

Custom fork of Ink (React for terminals) with performance optimizations (96 files).

## Subdirectories

### components/
Ink-level components (not the app-level ones in ui/):
- Box, Text, Static, App
- Input handling
- Error boundaries

### events/
Terminal event handling:
- Key event parsing
- Mouse event handling
- Focus management

### hooks/
Ink-specific hooks:
- `useInput` - Input handling
- `useApp` - App context
- `useStdin` - Stdin access
- `useStdout` - Stdout access
- `useFocus` - Focus management

### layout/
Layout engine:
- Virtual scrolling
- Flex layout
- Yoga layout integration

### termio/
Terminal I/O:
- Raw mode management
- Cursor control
- DEC escape sequences
- Color support

## Key Differences from Stock Ink

1. **Virtual scroll**: Only renders visible rows for performance
2. **Custom key handling**: Supports vim mode and custom keybindings
3. **Yoga layout**: Better layout algorithm than stock Ink
4. **Performance**: Optimized render cycle for large message lists
