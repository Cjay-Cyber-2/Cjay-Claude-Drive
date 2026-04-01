# Agent-Swarm Fused Workflow

This is the recommended fused workflow for combining broad swarm roles with the ultrathink operating contract.

## Main Principle

Treat the swarm as a role catalog and dispatch layer.
Do not treat the stock orchestrator as the entire brain.

## Phase Order

### 1. Intake

Use:
- `questionnaire`

Output:
- blockers
- assumptions
- success criteria
- scope

### 2. Research

Use one or more of:
- `gsd-project-researcher`
- `docs-lookup`
- language or domain specialists

Output:
- key files
- existing patterns
- constraints
- risk map

### 3. Planning

Use:
- `planner` or `gsd-planner`

The plan must include:
- execution order
- worker ownership
- disjoint write sets
- verification path per task

### 4. Plan Gate

Use:
- `gsd-plan-checker`
- optionally `tech-lead`

If the plan is weak, revise before execution.

### 5. Execution

Typical lanes:
- `frontend-dev`
- `backend-dev`
- `devops`
- `qa-tester`
- `security-reviewer`

Every worker gets the ultrathink worker contract and a narrow packet.

### 6. Adversarial Verification

Use:
- `gsd-verifier`
- `testing-reality-checker`
- optionally `code-reviewer` or `security-reviewer`

This is the main quality gate.

### 7. Synthesis

Use:
- `tech-lead`

Output:
- what is complete
- what was verified
- unresolved issues
- ship or rework decision

## Worker Packet Rules

Every packet must state:

- overall goal
- this lane only
- allowed write set
- read-first files
- deliverables
- exact verification method
- required report format

## Context Rules

- update session memory after each major phase
- compact only after research, after a milestone, or after a dead-end debug cycle
- do not compact in the middle of active implementation

## Verification Rule

No lane gets to self-certify broad readiness.
Implementation evidence must be checked by a verifier or skeptical reviewer.
