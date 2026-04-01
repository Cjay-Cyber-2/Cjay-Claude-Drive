# Source Map

This is where the practical and theory material came from.

## Current Repo

- `src/constants/prompts.ts`
  System prompt structure, tool discipline, reporting rules, planning guidance
- `src/services/tools/toolOrchestration.ts`
  Parallel read-only work and serialized stateful work
- `src/services/SessionMemory/prompts.ts`
  Durable session memory structure
- `src/services/compact/prompt.ts`
  High-detail context compaction
- `src/skills/bundled/debug.ts`
  Debugging workflow
- `src/skills/bundled/verify.ts`
  Real verification gate
- `src/skills/bundled/simplify.ts`
  Cleanup and code quality pass
- `src/skills/bundled/batch.ts`
  Broad parallel decomposition
- `analysis/tool-system.md`
  Tool contract
- `analysis/permission-system.md`
  Deny-first permission model
- `analysis/mcp-integration.md`
  Retrieval and tool extension model

## Inspected Agent-Swarm Snapshot

- `/tmp/agent-swarm/orchestrator.py`
  Engine-agnostic dispatch shell, but weak default task splitting
- `/tmp/agent-swarm/engines/adapter.py`
  Adapter model for multiple CLIs
- `/tmp/agent-swarm/skills/dmux-workflows/SKILL.md`
  Pane and worktree orchestration patterns
- `/tmp/agent-swarm/skills/autonomous-agent-harness/SKILL.md`
  Long-running autonomy patterns
- `/tmp/agent-swarm/skills/verification-loop/SKILL.md`
  Post-change verification loop
- `/tmp/agent-swarm/skills/strategic-compact/SKILL.md`
  Manual compaction timing
- `/tmp/agent-swarm/skills/context-budget/SKILL.md`
  Context overhead auditing
- `/tmp/agent-swarm/agents/core/questionnaire.md`
  Intake role
- `/tmp/agent-swarm/agents/core/planner.md`
  Planning role
- `/tmp/agent-swarm/agents/core/debugger.md`
  Debugging role
- `/tmp/agent-swarm/agents/management/tech-lead.md`
  Synthesis role
- `/tmp/agent-swarm/agents/testing/testing-reality-checker.md`
  Skeptical final gate
- `/tmp/agent-swarm/agents/gsd/gsd-verifier.md`
  Goal-backward verification
