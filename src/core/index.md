# Core Module

The core module contains the main entry points, the query engine, tool type definitions, and fundamental types.

## Key Files

| File | Purpose |
|------|---------|
| `main.tsx` | Primary CLI entry point - parses args, sets up sessions, launches REPL |
| `Tool.ts` | Tool type definitions, permission types, ToolPermissionContext |
| `Task.ts` | Task type definitions, task ID generation |
| `QueryEngine.ts` | Core agentic loop - sends API calls, processes tool use |
| `context.ts` | System and user context gathering |
| `cost-tracker.ts` | Token cost tracking |
| `costHook.ts` | Cost tracking hook |
| `history.ts` | Prompt history management |
| `ink.ts` | Ink root creation and mounting |
| `interactiveHelpers.tsx` | Helper functions for interactive mode |
| `dialogLaunchers.tsx` | Dialog launchers (resume, settings, etc.) |
| `replLauncher.tsx` | REPL launch function |
| `setup.ts` | Session setup (worktree, git, plugins, hooks) |
| `projectOnboardingState.ts` | Project onboarding tracking |
| `tasks.ts` | Task utility functions |
| `query.ts` | Query utilities |

## Architecture Notes

- `main.tsx` is the largest file (~4600 lines) as it orchestrates the entire startup sequence
- `Tool.ts` defines the fundamental `Tool` type used by all 40+ tool implementations
- `QueryEngine.ts` drives the agentic conversation loop
- `setup.ts` handles workspace initialization, git operations, and plugin loading
