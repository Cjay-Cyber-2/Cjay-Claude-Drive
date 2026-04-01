# Claude Code Portable Ideas

These are the most useful portable ideas extracted from the Claude Code architecture pack in this repo.

## Best Ideas To Copy Into Prompts

- Inspect before edit.
- Prefer dedicated tools over shell when equivalent tools exist.
- Parallelize only independent read-only work.
- Use plan mode for non-trivial work.
- Verify before claiming success.
- Report exact outcomes with no bluffing.
- Keep a structured session memory file for long tasks.
- Compact context at logical boundaries, not arbitrarily.
- Turn repeated workflows into reusable skills.
- Use MCP or retrieval on demand instead of bloating the main prompt.

## Best Ideas To Use As Engineering Patterns

- Async generator tool execution for progress and streaming.
- Deny-first permission model for risky actions.
- Unified command and skill registry.
- Tool pool assembly with filtering and gating.
- Session-specific prompt assembly instead of one giant static prompt.
- Multi-agent coordinator plus worker pattern with explicit capability boundaries.

## Most Valuable Source Files

- `src/constants/prompts.ts`
- `src/services/tools/toolOrchestration.ts`
- `src/services/SessionMemory/prompts.ts`
- `src/services/compact/prompt.ts`
- `src/skills/bundled/debug.ts`
- `src/skills/bundled/verify.ts`
- `src/skills/bundled/simplify.ts`
- `src/skills/bundled/batch.ts`
- `analysis/tool-system.md`
- `analysis/permission-system.md`
- `analysis/mcp-integration.md`

## What Not To Overestimate

You are not copying Anthropic's hidden model weights or internal reasoning tokens. The portable value is the operating system around the model, not the model itself.
