# Think Handbook

This is the operator manual for the folders I built.

If you only read one file, read this one.

## 1. What You Have

There are two main folders:

### `Think/`

This is the copy-and-operate layer.

Use it when you want:
- a prompt to paste into an AI
- a worker prompt for subagents
- a coordinator prompt for swarms
- a practical runbook and templates

### `ultrathink/`

This is the generator and toolkit layer.

Use it when you want:
- generated prompts for a specific task
- generated swarm blueprints
- fused prompts for `agent-swarm` agents
- reusable templates and source-backed operating packs

## 2. Fastest Way To Use This

### If you use one agent only

Do this:

1. Open `Think/PASTE_THIS_SYSTEM_PROMPT.md`
2. Paste it into the system prompt, developer prompt, or custom instructions of your AI
3. Start your task
4. For long tasks, keep `Think/practical/templates/SESSION_MEMORY_TEMPLATE.md` in a side file

This is the easiest path.

### If you use multiple agents

Do this:

1. Give the coordinator `Think/PASTE_THIS_COORDINATOR_PROMPT.md`
2. Give workers `Think/PASTE_THIS_WORKER_PROMPT.md`
3. Use `Think/practical/AGENT_SWARM_FUSED_WORKFLOW.md` as the execution order
4. Track progress with `Think/practical/templates/SWARM_CONTROL_PLANE_TEMPLATE.md`
5. Give each worker a packet from `Think/practical/templates/SWARM_WORKER_PACKET_TEMPLATE.md`

### If you want generated prompts

Use `ultrathink/ultrathink.py`

## 3. Which Files Matter Most

### Best theory files

- `Think/PASTE_THIS_SYSTEM_PROMPT.md`
- `Think/PASTE_THIS_COORDINATOR_PROMPT.md`
- `Think/PASTE_THIS_WORKER_PROMPT.md`
- `Think/theory/CLAUDE_CODE_PORTABLE_IDEAS.md`
- `Think/theory/AGENT_SWARM_PORTABLE_IDEAS.md`

These are the files you copy into AI systems.

### Best practical files

- `Think/practical/AGENT_SWARM_FUSED_WORKFLOW.md`
- `Think/practical/QUICKSTART.md`
- `Think/practical/templates/SESSION_MEMORY_TEMPLATE.md`
- `Think/practical/templates/SWARM_CONTROL_PLANE_TEMPLATE.md`
- `Think/practical/templates/SWARM_WORKER_PACKET_TEMPLATE.md`

These are the files you operate with.

### Best generator files

- `ultrathink/ultrathink.py`
- `ultrathink/README.md`
- `ultrathink/AGENT_SWARM_FUSION.md`

These are the files you use to generate tailored operating packs.

## 4. Exact Commands

Run these from the repo root.

### Inspect what the generator can do

```bash
python3 ultrathink/ultrathink.py list modes
python3 ultrathink/ultrathink.py list skills
python3 ultrathink/ultrathink.py list targets
```

### Generate a strong durable prompt for a coding agent

```bash
python3 ultrathink/ultrathink.py build --target tool-agent --style agents-md --mode implement --task "build the feature I am working on"
```

Use the output as:
- system prompt
- developer prompt
- repo-level AI instructions

### Generate a task kickoff prompt

```bash
python3 ultrathink/ultrathink.py build --target tool-agent --style task-kickoff --mode debug --task "find the root cause of the failing login flow"
```

Use this at the start of a specific task.

### Generate a daily operating checklist

```bash
python3 ultrathink/ultrathink.py daily
```

### Generate a specific skill card

```bash
python3 ultrathink/ultrathink.py skill verify
python3 ultrathink/ultrathink.py skill batch
python3 ultrathink/ultrathink.py skill simplify
```

### Generate a fused `agent-swarm` blueprint

```bash
python3 ultrathink/ultrathink.py swarm --goal "ship a production auth system" --stack fullstack --engine codex
```

Available stacks:
- `fullstack`
- `frontend`
- `backend`
- `debug`
- `research`
- `migration`

### Generate a fused prompt for one `agent-swarm` agent

```bash
python3 ultrathink/ultrathink.py fuse-agent --swarm-root /tmp/agent-swarm --agent planner --mode implement --task "design a full implementation plan for auth"
```

Use this when you want a specific swarm agent to inherit the ultrathink contract.

## 5. How To Use This With A Real Agent

### A. ChatGPT, Claude, Gemini, Copilot, Codex, or any single agent

Step by step:

1. Paste `Think/PASTE_THIS_SYSTEM_PROMPT.md` into the best persistent instruction surface the tool gives you.
2. Start a task with either:
   - your own natural request
   - or a generated kickoff from `ultrathink.py build --style task-kickoff`
3. If the task is large, create a note using `SESSION_MEMORY_TEMPLATE.md`
4. Force the agent to follow:
   research -> plan -> implement -> verify
5. Do not accept "done" without verification evidence

### B. Tool-capable coding agent

Step by step:

1. Generate a durable pack:

```bash
python3 ultrathink/ultrathink.py build --target tool-agent --style agents-md --mode implement --task "work on this repo"
```

2. Put that in the agent's durable project instructions.
3. For each new task, generate a kickoff prompt if needed.
4. Keep a live session memory file.
5. Require a verify step before the agent reports success.

### C. `agent-swarm`

Step by step:

1. Clone or inspect `agent-swarm`
2. Generate a swarm blueprint:

```bash
python3 ultrathink/ultrathink.py swarm --goal "build X" --stack fullstack --engine codex
```

3. Use the blueprint as the control doc for the run.
4. Give the coordinator `Think/PASTE_THIS_COORDINATOR_PROMPT.md`
5. Give workers `Think/PASTE_THIS_WORKER_PROMPT.md`
6. Use `AGENT_SWARM_FUSED_WORKFLOW.md` for the execution order
7. Track every lane in `SWARM_CONTROL_PLANE_TEMPLATE.md`
8. Give every lane a concrete packet using `SWARM_WORKER_PACKET_TEMPLATE.md`
9. Require:
   - planning
   - plan check
   - execution
   - adversarial verification
   - synthesis

## 6. What Makes This Better Than Just Prompting Harder

The practical gains come from:

- fewer fake completions
- stronger task decomposition
- narrower worker scope
- better verification
- better continuity in long sessions
- less context waste
- stronger final synthesis

It is not model magic.
It is disciplined operating behavior.

## 7. Best Working Styles

### Style 1: Solo Vibecoding

Best files:
- `Think/PASTE_THIS_SYSTEM_PROMPT.md`
- `Think/practical/templates/SESSION_MEMORY_TEMPLATE.md`

Best pattern:
- one agent
- strong prompt
- long memory
- hard verify gate

### Style 2: Swarm Vibecoding

Best files:
- `Think/PASTE_THIS_COORDINATOR_PROMPT.md`
- `Think/PASTE_THIS_WORKER_PROMPT.md`
- `Think/practical/AGENT_SWARM_FUSED_WORKFLOW.md`
- `Think/practical/templates/SWARM_CONTROL_PLANE_TEMPLATE.md`

Best pattern:
- one coordinator
- narrow workers
- explicit plan gate
- skeptical verifier

### Style 3: Generated Prompt Workflow

Best files:
- `ultrathink/ultrathink.py`
- `ultrathink/README.md`

Best pattern:
- generate prompt pack
- paste into tool
- generate kickoff per task
- re-run for new modes or stacks

## 8. Top Rules You Should Actually Enforce

If you enforce only a few rules, enforce these:

1. Inspect before edit.
2. Plan before risky execution.
3. Verify before claiming success.
4. Report exact outcomes.
5. Narrow worker boundaries.
6. Use adversarial verification for important work.

## 9. What I Audited

I verified:

- `Think/` structure exists
- `ultrathink/ultrathink.py` compiles
- `ultrathink.py swarm` works
- `ultrathink.py fuse-agent` works

So the current setup is usable now.

## 10. Recommended Starting Point

If you want the best default path:

1. Start with `Think/PASTE_THIS_SYSTEM_PROMPT.md`
2. Read `Think/practical/QUICKSTART.md`
3. Use `Think/HANDBOOK.md` as your operating reference
4. Use `ultrathink.py build` for single-agent work
5. Use `ultrathink.py swarm` for multi-agent work

That is the cleanest way to actually use what I built.
