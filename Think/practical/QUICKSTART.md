# Quickstart

## Fastest Good Setup

### Single agent

1. Paste `../PASTE_THIS_SYSTEM_PROMPT.md` into the system prompt or developer prompt.
2. Keep `templates/SESSION_MEMORY_TEMPLATE.md` nearby for long sessions.
3. For non-trivial work, force:
   research -> plan -> implement -> verify

### Multi-agent

1. Coordinator gets `../PASTE_THIS_COORDINATOR_PROMPT.md`.
2. Workers get `../PASTE_THIS_WORKER_PROMPT.md`.
3. Use `AGENT_SWARM_FUSED_WORKFLOW.md` as the operating runbook.
4. Track status in `templates/SWARM_CONTROL_PLANE_TEMPLATE.md`.
5. Give each worker a packet using `templates/SWARM_WORKER_PACKET_TEMPLATE.md`.

## Hard Rule

Do not expect better results just because more agents are running.
Better results come from:

- better decomposition
- better worker packets
- stronger verification
- stricter synthesis
- cleaner memory and context handling
