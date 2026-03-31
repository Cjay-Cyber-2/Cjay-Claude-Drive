# Entrypoints Module

Application entry points for different execution modes (8 files).

## Key Files

| File | Purpose |
|------|---------|
| `cli.tsx` | Main CLI entry - fast-path dispatcher |
| `init.ts` | One-time initialization (memoized) |
| `mcp.ts` | MCP server mode entry |
| `sdk/coreTypes.ts` | SDK core types |
| `sdk/coreSchemas.ts` | SDK schemas |
| `sdk/controlSchemas.ts` | SDK control schemas |
| `agentSdkTypes.ts` | Agent SDK types |
| `sandboxTypes.ts` | Sandbox types |
