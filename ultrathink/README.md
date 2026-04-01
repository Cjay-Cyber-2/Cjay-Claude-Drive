# Ultrathink Kit

This folder turns the Claude Code repository into a portable operating system for other agents.

It does **not** transplant Anthropic's model weights or hidden chain-of-thought. What it ports is the part that is actually reusable:

- system prompt structure
- plan mode and permission gating
- tool discipline
- parallel read-only work
- self-verification and adversarial verification
- reusable skills
- session memory
- context compaction patterns
- MCP-oriented context loading
- multi-agent decomposition

If you want better day-to-day vibecoding, this is the part that matters. Most "reasoning gains" from production agents come from better scaffolding, not magic prompt slogans.

## What To Use

Use the generator to build a portable instruction pack:

```bash
python3 ultrathink/ultrathink.py build --target tool-agent --style agents-md --mode implement --task "build the feature I am working on"
```

Generate a reusable kickoff prompt for a specific task:

```bash
python3 ultrathink/ultrathink.py build --target tool-agent --style task-kickoff --mode debug --task "find the root cause of the failing login flow"
```

Inspect the portable skills extracted from this repo:

```bash
python3 ultrathink/ultrathink.py list skills
python3 ultrathink/ultrathink.py skill verify
python3 ultrathink/ultrathink.py skill batch
```

Get the daily operating recipe:

```bash
python3 ultrathink/ultrathink.py daily
```

Generate a fused `agent-swarm` workflow blueprint:

```bash
python3 ultrathink/ultrathink.py swarm --goal "ship a production auth system" --stack fullstack --engine codex
```

Generate a fused prompt for a specific `agent-swarm` agent:

```bash
python3 ultrathink/ultrathink.py fuse-agent --swarm-root /tmp/agent-swarm --agent planner --mode implement --task "design the implementation plan for multi-tenant auth"
```

## Best Result Stack

To get the closest thing to "Claude-like" coding behavior on another agent, use this stack in order:

1. Load a generated `agents-md` pack into whatever durable instruction surface your agent supports.
2. Start each meaningful task with a generated `task-kickoff` prompt.
3. Keep a persistent session note file using [templates/session-memory-template.md](templates/session-memory-template.md).
4. Force a real verify step before claiming completion.
5. Use `batch` only for work that can be split cleanly.
6. Keep MCP resources focused on codebase, docs, tickets, and logs instead of stuffing everything into the prompt.

## Day-To-Day Workflow

For regular vibecoding, this is the loop:

1. Start the session with a generated operating pack.
2. Ask the agent to inspect before editing.
3. If the task is more than trivial, force a research -> plan -> implementation -> verify flow.
4. After a few turns, update a session memory file with current state, files touched, commands run, and failed attempts.
5. If the change is broad, split it into independent work units and verify each one.
6. If the workflow repeats, turn it into a skill or reusable prompt.

## Agent-Swarm Fusion

The strongest combination is:

1. Use `agent-swarm` as the role catalog and dispatch layer.
2. Use `ultrathink` as the operating contract for every coordinator and worker.
3. Use manual or generated lane plans instead of blindly trusting the default `orchestrator.py` split logic.

Why: `agent-swarm` gives you broad specialist coverage and engine adapters, but its stock orchestrator is intentionally simple. In the inspected snapshot, `parse_tasks()` in `/tmp/agent-swarm/orchestrator.py` routes execution with keyword checks, which is fine for quick demos but too shallow for high-quality engineering work. The fused workflow fixes that by making plan quality, verification quality, and worker boundaries explicit.

Use these supporting files:

- [AGENT_SWARM_FUSION.md](/home/gamp/Cjay-Claude-Drive/ultrathink/AGENT_SWARM_FUSION.md)
- [swarm-control-plane-template.md](/home/gamp/Cjay-Claude-Drive/ultrathink/templates/swarm-control-plane-template.md)
- [swarm-worker-packet.md](/home/gamp/Cjay-Claude-Drive/ultrathink/templates/swarm-worker-packet.md)

## What This Repo Contributes

The highest-value portable pieces come from these files:

- `src/constants/prompts.ts`: system prompt structure, tool usage rules, reporting discipline, planning guidance
- `src/core/QueryEngine.ts`: agent loop structure
- `src/services/tools/toolOrchestration.ts`: safe parallel execution for independent tool calls
- `src/services/SessionMemory/prompts.ts`: persistent session note template and update rules
- `src/services/compact/prompt.ts`: context compaction pattern
- `src/skills/bundled/debug.ts`: targeted debugging workflow
- `src/skills/bundled/verify.ts`: verify-by-running, not verify-by-claiming
- `src/skills/bundled/simplify.ts`: post-change cleanup and review
- `src/skills/bundled/batch.ts`: large-scale parallel decomposition
- `src/skills/bundled/loop.ts`: repeatable agent triggers
- `analysis/tool-system.md`: tool contract and execution model
- `analysis/mcp-integration.md`: MCP configuration and retrieval pattern
- `analysis/permission-system.md`: deny-first execution control

## Reality Check

Do not expect "10x to 20x smarter than Claude" from prompt text alone. The real gains you can get from this kit are:

- fewer hallucinated completions
- cleaner task decomposition
- better use of tools and context
- higher verification quality
- better continuity across long sessions
- less wasted context and less random agent drift

That is the practical way to become a much stronger vibecoder with any capable agent.
