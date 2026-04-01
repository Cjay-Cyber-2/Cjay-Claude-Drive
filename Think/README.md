# Think

This folder is the copy-friendly version of the work.

Use it in two ways:

1. `PASTE_THIS_*.md` files:
   Copy into a system prompt, developer prompt, or agent profile.
2. `practical/`:
   Use as the real workflow, templates, and runbooks for actual agent work.

Start with:

- `HANDBOOK.md`

## Structure

- `PASTE_THIS_SYSTEM_PROMPT.md`
  Main portable ultrathink prompt for a single strong agent.
- `PASTE_THIS_WORKER_PROMPT.md`
  Narrow worker contract for subagents and swarm lanes.
- `PASTE_THIS_COORDINATOR_PROMPT.md`
  Coordinator contract for multi-agent orchestration.
- `HANDBOOK.md`
  Step-by-step operator guide for using everything in this folder and the `ultrathink/` toolkit.
- `theory/`
  Distilled ideas extracted from the Claude Code architecture pack and the `agent-swarm` repo.
- `practical/`
  Runbooks, fused swarm workflow, source map, and reusable templates.

## Recommended Use

### Single agent

Use:
- `PASTE_THIS_SYSTEM_PROMPT.md`

### Multi-agent

Use:
- coordinator gets `PASTE_THIS_COORDINATOR_PROMPT.md`
- workers get `PASTE_THIS_WORKER_PROMPT.md`
- operator follows `practical/AGENT_SWARM_FUSED_WORKFLOW.md`

### Long sessions

Use:
- `practical/templates/SESSION_MEMORY_TEMPLATE.md`
- compact only at logical phase boundaries

## Core Idea

The main upgrade is not magic hidden reasoning. It is disciplined operating behavior:

- inspect before editing
- plan before risky implementation
- verify before claiming success
- faithful reporting
- explicit worker boundaries
- adversarial verification
- durable memory and context control

That is what this folder packages in copyable form.
