# Agent-Swarm Fusion

This is the practical combination:

- `agent-swarm` provides role breadth, engine adapters, and parallel execution patterns.
- `ultrathink` provides the discipline that most swarms are missing: inspect-first behavior, plan gates, real verification, faithful reporting, session memory, and context control.

## What To Keep From Agent-Swarm

From the inspected `agent-swarm` snapshot:

- `orchestrator.py` gives a usable engine-agnostic dispatch shell.
- `engines/adapter.py` already supports multiple CLI agents.
- `skills/dmux-workflows/SKILL.md` captures parallel pane and worktree execution patterns.
- `skills/autonomous-agent-harness/SKILL.md` captures long-running loop patterns.
- `skills/verification-loop/SKILL.md` adds a structured post-change quality gate.
- `skills/strategic-compact/SKILL.md` and `skills/context-budget/SKILL.md` address context pressure.
- `agents/core/questionnaire.md`, `agents/core/planner.md`, `agents/core/debugger.md`, `agents/management/tech-lead.md`, `agents/testing/testing-reality-checker.md`, and `agents/gsd/gsd-verifier.md` provide useful role shells.

## What To Replace Or Tighten

Do not rely on the default orchestration path for serious work without additional control. In the inspected `orchestrator.py`:

- `parse_tasks()` is keyword-driven and too coarse for non-trivial work.
- verification is not strong enough by default to stop bluffing reliably.
- synthesis happens late, after weak lane assignment.

Treat the stock orchestrator as a transport layer, not as the brain.

## Fused Workflow

### 1. Intake

Use `questionnaire` first.

Goal:
- turn vague asks into explicit scope
- surface blockers and assumptions
- define success criteria early

### 2. Research

Use one or more research lanes before planning:

- `gsd-project-researcher`
- `docs-lookup`
- a language reviewer or domain specialist if needed

Goal:
- identify existing patterns
- find the real files and boundaries
- reduce speculative planning

### 3. Plan

Use `planner` or `gsd-planner`.

Hard rules:
- every meaningful task must have a deliverable
- every task must have a verification path
- every parallel lane must have a disjoint write set or a clean artifact boundary

### 4. Plan Gate

Before execution, run:

- `gsd-plan-checker`
- `tech-lead` for architectural consistency if the change is broad

If the plan is weak, revise it before dispatching workers.

### 5. Execute Lanes

Typical engineering lanes:

- `frontend-dev`
- `backend-dev`
- `devops`
- `qa-tester`
- `security-reviewer`
- `docs` or `engineering-technical-writer` if docs are part of done

Every lane gets the same `ultrathink` worker contract:

- read before writing
- keep scope narrow
- prefer dedicated tools
- verify before claiming success
- report exact outcomes
- do not silently expand scope

### 6. Adversarial Verification

After execution, run:

- `gsd-verifier` for goal-backward verification
- `testing-reality-checker` for evidence-heavy skepticism
- `code-reviewer` or `security-reviewer` where appropriate

This is the main quality upgrade over most swarm setups.

### 7. Synthesis

Use `tech-lead` to:

- reconcile lane outputs
- identify conflicts and missing integration work
- issue the final ship or rework decision

### 8. Memory And Context Control

Use:

- session memory for current state and failed attempts
- strategic compact at logical boundaries only
- context budget audits if the swarm gets bloated

## Best Operating Modes

### Fast Build

Use for small to medium tasks:

1. `questionnaire`
2. `planner`
3. 2-4 execution lanes
4. `gsd-verifier`
5. `tech-lead`

### Hardening Build

Use for risky or production-facing work:

1. `questionnaire`
2. research lanes
3. `gsd-planner`
4. `gsd-plan-checker`
5. execution lanes
6. `gsd-verifier`
7. `testing-reality-checker`
8. `security-reviewer`
9. `tech-lead`

### Continuous Operator Mode

Use for recurring checks or autonomy:

1. `autonomous-agent-harness`
2. scheduled execution
3. persistent memory
4. explicit verification loop
5. compact and prune at checkpoints

## Practical Rule

If you want the swarm to outperform a single default session, the win does not come from "more agents". The win comes from:

- better decomposition
- better worker packets
- stronger verification
- stricter synthesis
- better memory hygiene

That is what the fusion tooling in [ultrathink.py](/home/gamp/Cjay-Claude-Drive/ultrathink/ultrathink.py) is designed to generate.
