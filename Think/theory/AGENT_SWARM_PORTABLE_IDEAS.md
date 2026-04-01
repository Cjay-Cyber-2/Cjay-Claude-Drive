# Agent Swarm Portable Ideas

These are the most useful portable ideas extracted from the inspected `agent-swarm` repo snapshot.

## Strong Ideas

- use broad specialist catalogs as role shells
- keep engines adapter-based so the same workflow can target different CLIs
- split work across panes, worktrees, or sessions only when boundaries are clean
- use a separate verifier role instead of trusting the implementer
- use a skeptical reality-check role before saying something is production ready
- use a control-plane artifact for tracking lanes, status, and evidence
- use strategic compaction and context-budget checks in long multi-agent sessions

## Weak Or Incomplete Areas To Tighten

- naive keyword-based task splitting is too shallow for serious engineering work
- orchestration without a strong plan gate leads to noisy or overlapping worker assignments
- a broad agent catalog is useful only if workers receive narrow packets and hard verification rules

## Best Pieces To Reuse

- `orchestrator.py` as a dispatch shell
- `engines/adapter.py` as an engine abstraction
- `skills/dmux-workflows/SKILL.md`
- `skills/autonomous-agent-harness/SKILL.md`
- `skills/verification-loop/SKILL.md`
- `skills/strategic-compact/SKILL.md`
- `skills/context-budget/SKILL.md`
- `agents/core/questionnaire.md`
- `agents/core/planner.md`
- `agents/core/debugger.md`
- `agents/testing/testing-reality-checker.md`
- `agents/gsd/gsd-verifier.md`

## Best Fusion Rule

Use `agent-swarm` for role breadth and transport.
Use the ultrathink contract for discipline, verification, and synthesis.
