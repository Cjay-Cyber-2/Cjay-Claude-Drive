#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from textwrap import dedent


REPO_ROOT = Path(__file__).resolve().parents[1]
SESSION_MEMORY_TEMPLATE = (
    Path(__file__).resolve().parent / "templates" / "session-memory-template.md"
).read_text(encoding="utf-8")
SWARM_CONTROL_PLANE_TEMPLATE = (
    Path(__file__).resolve().parent / "templates" / "swarm-control-plane-template.md"
).read_text(encoding="utf-8")
SWARM_WORKER_PACKET_TEMPLATE = (
    Path(__file__).resolve().parent / "templates" / "swarm-worker-packet.md"
).read_text(encoding="utf-8")


TARGETS = {
    "chat-only": {
        "label": "Chat-only agent",
        "notes": [
            "Use the generated pack as a system or developer prompt.",
            "Treat tool instructions as process rules the model must emulate explicitly.",
            "Keep prompts shorter and rely more on checklists than on tool contracts.",
        ],
    },
    "tool-agent": {
        "label": "Tool-capable coding agent",
        "notes": [
            "Use the generated pack as a durable project instruction file or system prompt.",
            "Enforce inspect-before-edit, dedicated-tool preference, and real verification.",
            "Parallelize only independent read-only work.",
        ],
    },
    "mcp-agent": {
        "label": "MCP-aware agent",
        "notes": [
            "Keep the operating pack in the prompt and move large factual context into MCP resources.",
            "Use MCP for docs, logs, tickets, schemas, and deployment state rather than inflating the prompt.",
            "Retain the same plan, verify, and reporting contract as the tool-agent profile.",
        ],
    },
    "multi-agent": {
        "label": "Multi-agent system",
        "notes": [
            "Use one coordinator with strong synthesis rules and workers with narrower scopes.",
            "Split research, implementation, and verification into explicit phases.",
            "Only parallelize units with disjoint write sets or clearly separable outputs.",
        ],
    },
    "agent-swarm": {
        "label": "Agent Swarm fusion",
        "notes": [
            "Use agent-swarm as the role and dispatch layer, not as the whole brain.",
            "Inject the ultrathink worker contract into every coordinator and worker prompt.",
            "Prefer generated lane plans over the stock keyword-based task splitting path.",
        ],
    },
}


FEATURES = [
    {
        "key": "read-before-write",
        "title": "Read before writing",
        "summary": "Never modify code you have not inspected first.",
        "why": "Cuts false assumptions and lowers breakage from context drift.",
        "sources": ["src/constants/prompts.ts", "ARCHITECTURE.md"],
    },
    {
        "key": "dedicated-tools",
        "title": "Prefer dedicated tools over shell",
        "summary": "Use specific file/search/edit tools when available; keep shell for true shell work.",
        "why": "Produces clearer actions, tighter permissions, and more reviewable behavior.",
        "sources": ["src/constants/prompts.ts", "analysis/tool-system.md"],
    },
    {
        "key": "parallel-safe-reads",
        "title": "Parallelize independent read-only work",
        "summary": "Run independent search/read/resource steps in parallel, serialize writes and stateful actions.",
        "why": "Improves speed without introducing race conditions.",
        "sources": ["src/services/tools/toolOrchestration.ts", "PATTERNS.md"],
    },
    {
        "key": "plan-gate",
        "title": "Use an explicit plan gate",
        "summary": "Research first, then plan, then implement after alignment for non-trivial work.",
        "why": "Prevents random action-taking and reduces costly rework.",
        "sources": ["src/constants/prompts.ts", "analysis/permission-system.md"],
    },
    {
        "key": "deny-first",
        "title": "Deny-first permissions",
        "summary": "Default to blocking risky operations until explicitly allowed.",
        "why": "Makes aggressive agents usable without wrecking trust.",
        "sources": ["analysis/permission-system.md", "PATTERNS.md"],
    },
    {
        "key": "verify-before-claim",
        "title": "Verify before claiming success",
        "summary": "Do not report completion until the change is actually tested, run, or independently checked.",
        "why": "This is one of the biggest real quality multipliers in the repo.",
        "sources": ["src/constants/prompts.ts", "src/skills/bundled/verify.ts"],
    },
    {
        "key": "faithful-reporting",
        "title": "Report exact outcomes",
        "summary": "If tests fail, say they failed. If you did not verify, say you did not verify.",
        "why": "Prevents the most common agent failure mode: bluffing.",
        "sources": ["src/constants/prompts.ts"],
    },
    {
        "key": "session-memory",
        "title": "Persistent session memory",
        "summary": "Keep a structured running note of current state, files, workflow, failures, and results.",
        "why": "Maintains continuity across long sessions and compaction boundaries.",
        "sources": ["src/services/SessionMemory/prompts.ts"],
    },
    {
        "key": "compaction",
        "title": "Context compaction",
        "summary": "Summarize older work with high detail so the active window can stay focused on current tasks.",
        "why": "Lets long sessions stay coherent instead of degrading into forgetfulness.",
        "sources": ["src/services/compact/prompt.ts"],
    },
    {
        "key": "skills",
        "title": "Reusable skills",
        "summary": "Capture repeatable workflows as named, argument-driven prompt playbooks.",
        "why": "Turns one-off success into repeatable leverage.",
        "sources": ["src/skills/bundled/index.ts", "src/skills/bundled/skillify.ts"],
    },
    {
        "key": "mcp-retrieval",
        "title": "Use MCP as retrieval, not prompt stuffing",
        "summary": "Pull specific external context on demand through tools and resources.",
        "why": "Improves relevance while keeping the core prompt lean.",
        "sources": ["analysis/mcp-integration.md"],
    },
    {
        "key": "batch-decomposition",
        "title": "Decompose broad work into clean units",
        "summary": "Split large migrations or refactors into self-contained units with explicit verification steps.",
        "why": "This is how you scale from one-task prompting to serious throughput.",
        "sources": ["src/skills/bundled/batch.ts", "src/coordinator/coordinatorMode.ts"],
    },
]


SKILLS = {
    "debug": {
        "title": "Debug",
        "goal": "Diagnose issues from logs, warnings, context, and repro evidence.",
        "steps": [
            "Read the latest diagnostic evidence instead of guessing.",
            "Search for error and warning patterns across the relevant logs or files.",
            "Explain the likely failure mode in plain language.",
            "Propose concrete next actions or fixes.",
        ],
        "sources": ["src/skills/bundled/debug.ts"],
    },
    "verify": {
        "title": "Verify",
        "goal": "Prove a change works by running the app, commands, tests, or user flow.",
        "steps": [
            "Define what successful behavior would look like.",
            "Run the most direct real-world verification path available.",
            "Capture exact output or evidence.",
            "Report pass, fail, or partial with no bluffing.",
        ],
        "sources": ["src/skills/bundled/verify.ts", "src/constants/prompts.ts"],
    },
    "simplify": {
        "title": "Simplify",
        "goal": "Review changed code for duplication, hackiness, and avoidable inefficiency.",
        "steps": [
            "Inspect the diff or touched files.",
            "Look for existing utilities or abstractions to reuse.",
            "Remove unnecessary state, comments, wrappers, and repeated work.",
            "Keep only the complexity the task actually needs.",
        ],
        "sources": ["src/skills/bundled/simplify.ts"],
    },
    "batch": {
        "title": "Batch",
        "goal": "Plan and execute large parallelizable codebase changes safely.",
        "steps": [
            "Research scope first.",
            "Decompose into independent work units with clean ownership.",
            "Define a concrete verification recipe per unit.",
            "Run units in parallel and track status explicitly.",
        ],
        "sources": ["src/skills/bundled/batch.ts", "src/coordinator/coordinatorMode.ts"],
    },
    "loop": {
        "title": "Loop",
        "goal": "Repeat a useful prompt or workflow on a schedule.",
        "steps": [
            "Normalize the cadence.",
            "Store the recurring task.",
            "Run the task immediately once.",
            "Keep cancellation and expiry visible.",
        ],
        "sources": ["src/skills/bundled/loop.ts"],
    },
    "remember": {
        "title": "Remember",
        "goal": "Curate durable memory instead of letting session notes rot.",
        "steps": [
            "Review project, personal, and auto memory layers.",
            "Promote stable conventions to the right place.",
            "Remove duplicates and flag conflicts.",
            "Ask before applying ambiguous changes.",
        ],
        "sources": ["src/skills/bundled/remember.ts"],
    },
    "skillify": {
        "title": "Skillify",
        "goal": "Turn a successful repeated process into a reusable skill.",
        "steps": [
            "Analyze the session and identify the repeatable workflow.",
            "Ask targeted questions about inputs, outputs, checkpoints, and constraints.",
            "Write the skill with success criteria for each step.",
            "Save it where the agent can invoke it again later.",
        ],
        "sources": ["src/skills/bundled/skillify.ts"],
    },
}


MODES = {
    "implement": {
        "label": "Implementation",
        "workflow": [
            "Inspect the relevant code, tests, and surrounding patterns before changing anything.",
            "If the task touches multiple files or has risk, write a short plan first.",
            "Implement the smallest complete change that satisfies the request.",
            "Run the most direct verification path available.",
            "Report exactly what changed and what was verified.",
        ],
        "skills": ["verify", "simplify", "remember"],
    },
    "debug": {
        "label": "Debugging",
        "workflow": [
            "Restate the failure in falsifiable terms.",
            "Collect logs, warnings, traces, repro steps, and relevant code paths.",
            "Form a small number of hypotheses and test them directly.",
            "Fix the root cause rather than masking symptoms.",
            "Re-run the failing path and report the outcome.",
        ],
        "skills": ["debug", "verify", "remember"],
    },
    "review": {
        "label": "Review",
        "workflow": [
            "Read the diff and surrounding context first.",
            "Look for bugs, regressions, missing tests, security issues, and misleading reporting.",
            "Prioritize findings by severity and user impact.",
            "Call out residual risk if verification is weak or absent.",
            "Keep summaries secondary to concrete findings.",
        ],
        "skills": ["simplify", "verify"],
    },
    "research": {
        "label": "Research",
        "workflow": [
            "Search broadly first, then narrow to the relevant source of truth.",
            "Parallelize independent read-only investigation.",
            "Capture the key files, patterns, and unknowns in notes.",
            "Synthesize before proposing action.",
            "Only move to implementation when the map is clear enough.",
        ],
        "skills": ["remember", "skillify"],
    },
    "refactor": {
        "label": "Refactor",
        "workflow": [
            "Define the invariant behavior that must stay unchanged.",
            "Read all call sites and affected boundaries before editing.",
            "Move in small coherent steps rather than broad churn.",
            "Verify behavior after each meaningful slice.",
            "Run a cleanup pass to remove accidental complexity.",
        ],
        "skills": ["simplify", "verify", "remember"],
    },
    "batch": {
        "label": "Parallel batch work",
        "workflow": [
            "Research the full migration or refactor surface first.",
            "Split the work into units that do not depend on each other landing first.",
            "Assign a clear file or module boundary to each unit.",
            "Require verification evidence for every unit.",
            "Track status centrally and synthesize the final result.",
        ],
        "skills": ["batch", "verify", "simplify"],
    },
}


SOURCE_ANCHORS = [
    ("System prompt and operating contract", "src/constants/prompts.ts"),
    ("Core agent loop", "src/core/QueryEngine.ts"),
    ("Parallel tool orchestration", "src/services/tools/toolOrchestration.ts"),
    ("Session memory design", "src/services/SessionMemory/prompts.ts"),
    ("Context compaction", "src/services/compact/prompt.ts"),
    ("Tool model", "analysis/tool-system.md"),
    ("MCP model", "analysis/mcp-integration.md"),
    ("Permission model", "analysis/permission-system.md"),
    ("Debug skill", "src/skills/bundled/debug.ts"),
    ("Verify skill", "src/skills/bundled/verify.ts"),
    ("Simplify skill", "src/skills/bundled/simplify.ts"),
    ("Batch skill", "src/skills/bundled/batch.ts"),
    ("Loop skill", "src/skills/bundled/loop.ts"),
    ("Memory curation skill", "src/skills/bundled/remember.ts"),
    ("Skill generator", "src/skills/bundled/skillify.ts"),
]

SWARM_SOURCE_ANCHORS = [
    ("Swarm README", "/tmp/agent-swarm/README.md"),
    ("Swarm orchestrator", "/tmp/agent-swarm/orchestrator.py"),
    ("Engine adapter", "/tmp/agent-swarm/engines/adapter.py"),
    ("Common development workflow", "/tmp/agent-swarm/rules/common/development-workflow.md"),
    ("dmux workflows skill", "/tmp/agent-swarm/skills/dmux-workflows/SKILL.md"),
    ("Autonomous harness skill", "/tmp/agent-swarm/skills/autonomous-agent-harness/SKILL.md"),
    ("Verification loop skill", "/tmp/agent-swarm/skills/verification-loop/SKILL.md"),
    ("Strategic compact skill", "/tmp/agent-swarm/skills/strategic-compact/SKILL.md"),
    ("Context budget skill", "/tmp/agent-swarm/skills/context-budget/SKILL.md"),
    ("Questionnaire agent", "/tmp/agent-swarm/agents/core/questionnaire.md"),
    ("Planner agent", "/tmp/agent-swarm/agents/core/planner.md"),
    ("Debugger agent", "/tmp/agent-swarm/agents/core/debugger.md"),
    ("Tech lead agent", "/tmp/agent-swarm/agents/management/tech-lead.md"),
    ("Reality checker agent", "/tmp/agent-swarm/agents/testing/testing-reality-checker.md"),
    ("GSD verifier agent", "/tmp/agent-swarm/agents/gsd/gsd-verifier.md"),
]

SWARM_STACKS = {
    "fullstack": {
        "label": "Full-stack product build",
        "lanes": [
            ("questionnaire", "Clarify scope, assumptions, auth, data, and success criteria."),
            ("gsd-project-researcher", "Map the codebase and find the real boundaries before planning."),
            ("planner", "Create the implementation plan with phases, file boundaries, and dependencies."),
            ("gsd-plan-checker", "Reject weak plans before execution."),
            ("frontend-dev", "Own the UI and client-facing interaction layer."),
            ("backend-dev", "Own the API, data, auth, and server-side behavior."),
            ("qa-tester", "Own test strategy and reproducible checks."),
            ("security-reviewer", "Own auth, secrets, trust boundaries, and abuse-path review."),
            ("gsd-verifier", "Verify goal achievement against the actual codebase."),
            ("testing-reality-checker", "Reject fantasy approvals without strong evidence."),
            ("tech-lead", "Synthesize outputs and decide ship vs rework."),
        ],
    },
    "frontend": {
        "label": "Frontend-focused build",
        "lanes": [
            ("questionnaire", "Clarify UI scope, flows, devices, and acceptance criteria."),
            ("gsd-ui-researcher", "Map screens, components, and design constraints."),
            ("planner", "Produce a lane plan with component boundaries and verification."),
            ("frontend-dev", "Implement UI behavior and component work."),
            ("qa-tester", "Own browser-level checks and regressions."),
            ("testing-reality-checker", "Demand evidence of actual UX quality."),
            ("tech-lead", "Synthesize UI quality, consistency, and risks."),
        ],
    },
    "backend": {
        "label": "Backend or API build",
        "lanes": [
            ("questionnaire", "Clarify data flow, auth, integrations, and error paths."),
            ("docs-lookup", "Load exact docs and protocol constraints."),
            ("planner", "Define API, data, and task sequencing."),
            ("backend-dev", "Implement service and API work."),
            ("qa-tester", "Own tests and integration checks."),
            ("security-reviewer", "Audit auth, input handling, and secrets."),
            ("gsd-verifier", "Verify the delivered backend actually satisfies the goal."),
            ("tech-lead", "Synthesize final architecture and readiness."),
        ],
    },
    "debug": {
        "label": "Bug hunt and stabilization",
        "lanes": [
            ("questionnaire", "Clarify exact symptom, expected behavior, and repro path."),
            ("debugger", "Root cause analysis and minimal corrective change."),
            ("qa-tester", "Reproduce and lock the bug with tests or exact repro steps."),
            ("testing-test-results-analyzer", "Interpret failures and isolate noisy output."),
            ("gsd-verifier", "Verify the bug is truly fixed in the codebase and behavior."),
            ("tech-lead", "Decide whether the fix is complete or needs another cycle."),
        ],
    },
    "research": {
        "label": "Research and architecture study",
        "lanes": [
            ("questionnaire", "Clarify the decision to be made and its constraints."),
            ("docs-lookup", "Fetch canonical docs and references."),
            ("gsd-project-researcher", "Map codebase context and existing patterns."),
            ("planner", "Turn findings into an executable path."),
            ("tech-lead", "Issue the architectural decision and trade-offs."),
        ],
    },
    "migration": {
        "label": "Large migration or refactor",
        "lanes": [
            ("questionnaire", "Clarify invariants, blast radius, and acceptance checks."),
            ("gsd-project-researcher", "Map all touched files and hotspots."),
            ("gsd-planner", "Produce decomposed work units with verification for each."),
            ("gsd-plan-checker", "Reject unsafe or incomplete units."),
            ("frontend-dev", "Frontend lane if applicable."),
            ("backend-dev", "Backend lane if applicable."),
            ("code-reviewer", "Catch regressions and consistency gaps."),
            ("gsd-verifier", "Goal-backward verification across the migration."),
            ("tech-lead", "Synthesize landing status and unresolved risk."),
        ],
    },
}


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def section(title: str, body: str) -> str:
    return f"## {title}\n\n{body}".rstrip()


def render_feature_lines() -> list[str]:
    return [
        f"{feature['title']}: {feature['summary']} Why it matters: {feature['why']}"
        for feature in FEATURES
    ]


def render_target_notes(target_key: str) -> str:
    target = TARGETS[target_key]
    return section(target["label"], bullets(target["notes"]))


def render_mode(mode_key: str) -> str:
    mode = MODES[mode_key]
    return section(f"{mode['label']} Workflow", numbered(mode["workflow"]))


def render_skills(mode_key: str) -> str:
    mode = MODES[mode_key]
    lines = []
    for skill_name in mode["skills"]:
        skill = SKILLS[skill_name]
        lines.append(f"{skill['title']}: {skill['goal']}")
    return section("Portable Skills To Lean On", bullets(lines))


def render_sources() -> str:
    lines = [f"{label}: {path}" for label, path in SOURCE_ANCHORS]
    return section("Source Anchors", bullets(lines))


def render_swarm_sources() -> str:
    lines = [f"{label}: {path}" for label, path in SWARM_SOURCE_ANCHORS]
    return section("Agent-Swarm Anchors", bullets(lines))


def render_memory_template() -> str:
    return section(
        "Session Memory Template",
        f"```markdown\n{SESSION_MEMORY_TEMPLATE.rstrip()}\n```",
    )


def locate_swarm_agent_file(swarm_root: Path, agent_name: str) -> Path:
    config_path = swarm_root / "swarm.config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing swarm config at {config_path}")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    agent_entry = config.get("agents", {}).get(agent_name)
    if not agent_entry:
        raise KeyError(f"Unknown swarm agent: {agent_name}")
    relative_path = agent_entry.get("file")
    if not relative_path:
        raise KeyError(f"Agent {agent_name} has no file entry in swarm config")
    agent_path = swarm_root / "agents" / Path(relative_path)
    if not agent_path.exists():
        raise FileNotFoundError(f"Agent file not found: {agent_path}")
    return agent_path


def render_worker_contract() -> str:
    lines = [
        "Read the relevant files, tests, and constraints before making changes.",
        "Stay inside the assigned scope and write set.",
        "Prefer dedicated tools over broad shell commands when possible.",
        "Parallelize only independent read-only work.",
        "Use the smallest complete change that satisfies the lane goal.",
        "Verify with direct evidence before reporting completion.",
        "If verification is partial or impossible, say so explicitly.",
        "Do not invent success, hidden fixes, or unstated assumptions.",
    ]
    return section("Universal Worker Contract", bullets(lines))


def render_swarm_templates() -> str:
    return "\n\n".join(
        [
            section(
                "Swarm Control Plane Template",
                f"```markdown\n{SWARM_CONTROL_PLANE_TEMPLATE.rstrip()}\n```",
            ),
            section(
                "Swarm Worker Packet Template",
                f"```markdown\n{SWARM_WORKER_PACKET_TEMPLATE.rstrip()}\n```",
            ),
        ]
    )


def render_swarm_lanes(stack_key: str) -> str:
    stack = SWARM_STACKS[stack_key]
    lines = [
        f"{name}: {description}"
        for name, description in stack["lanes"]
    ]
    return section(f"{stack['label']} Lane Plan", numbered(lines))


def render_swarm_commands(swarm_root: str, engine: str, stack_key: str, goal: str) -> str:
    stack = SWARM_STACKS[stack_key]
    commands = []
    for name, description in stack["lanes"][:4]:
        commands.append(
            f"python {swarm_root}/orchestrator.py --engine {engine} --agent {name} {json.dumps(goal)}"
        )
    commands.append(
        f"# Then dispatch execution lanes manually from the approved plan instead of trusting default keyword routing."
    )
    commands.append(
        f"python {swarm_root}/orchestrator.py --engine {engine} --agent gsd-verifier {json.dumps('Verify the implemented result against the goal and actual codebase.')}"
    )
    return section("Suggested Command Skeleton", "```bash\n" + "\n".join(commands) + "\n```")


def render_swarm_guardrails() -> str:
    lines = [
        "Do not trust the stock `parse_tasks()` split for complex work; use a reviewed lane plan.",
        "Every execution lane needs a narrow ownership boundary and a verification clause.",
        "Use `gsd-plan-checker` before execution for non-trivial work.",
        "Use `gsd-verifier` plus `testing-reality-checker` before declaring ship-ready status.",
        "Compact only at logical phase boundaries, never in the middle of active implementation.",
        "Persist current state and failed attempts to session memory before major transitions.",
    ]
    return section("Swarm Guardrails", bullets(lines))


def build_swarm_blueprint(goal: str, stack_key: str, engine: str, swarm_root: str) -> str:
    intro = dedent(
        f"""\
        # Ultrathink Swarm Blueprint

        Goal: {goal}
        Stack: {SWARM_STACKS[stack_key]['label']}
        Engine: {engine}
        Swarm root: {swarm_root}
        """
    ).strip()

    parts = [
        intro,
        section(
            "Core Idea",
            "Use `agent-swarm` as the role and transport layer, and use `ultrathink` as the operating contract that makes those roles trustworthy.",
        ),
        render_swarm_guardrails(),
        render_swarm_lanes(stack_key),
        render_worker_contract(),
        render_mode("batch" if stack_key == "migration" else "implement" if stack_key in {"fullstack", "frontend", "backend"} else "debug" if stack_key == "debug" else "research"),
        render_skills("batch" if stack_key == "migration" else "implement" if stack_key in {"fullstack", "frontend", "backend"} else "debug" if stack_key == "debug" else "research"),
        render_swarm_commands(swarm_root, engine, stack_key, goal),
        render_memory_template(),
        render_swarm_templates(),
        render_swarm_sources(),
    ]
    return "\n\n".join(parts).rstrip() + "\n"


def build_fused_agent_prompt(
    swarm_root: str,
    agent_name: str,
    mode_key: str,
    task: str,
) -> str:
    swarm_root_path = Path(swarm_root)
    agent_path = locate_swarm_agent_file(swarm_root_path, agent_name)
    agent_body = agent_path.read_text(encoding="utf-8").strip()
    mode = MODES[mode_key]

    intro = dedent(
        f"""\
        # Ultrathink Fused Swarm Agent

        Selected swarm agent: {agent_name}
        Agent file: {agent_path}
        Mode: {mode['label']}
        """
    ).strip()

    contract = bullets(
        [
            "Inspect before you modify or conclude.",
            "Keep scope tight and do not freeload unrelated improvements into the lane.",
            "Prefer direct evidence over confident narration.",
            "Do not claim tests, builds, or verification passed unless you actually ran them or were given real evidence.",
            "If blocked, say what blocked you and what you tried.",
            "Return concise, high-signal output that the coordinator can act on.",
        ]
    )

    report_contract = numbered(
        [
            "State the result in one line.",
            "List the concrete files, commands, or artifacts that matter.",
            "Report verification with exact pass, fail, or partial status.",
            "List residual risks or blockers with no hedging.",
        ]
    )

    task_section = task.strip() if task.strip() else "No task supplied."

    parts = [
        intro,
        section("Operating Contract", contract),
        render_mode(mode_key),
        section("Coordinator-Facing Report Contract", report_contract),
        section("Task", task_section),
        section("Underlying Swarm Agent Definition", f"```markdown\n{agent_body}\n```"),
    ]
    return "\n\n".join(parts).rstrip() + "\n"


def build_pack(args: argparse.Namespace) -> str:
    mode = MODES[args.mode]
    task_line = args.task.strip() if args.task else "No task supplied."
    model_line = args.model.strip() if args.model else "Unspecified model."

    intro = dedent(
        f"""\
        # Ultrathink Portable Pack

        Target profile: {TARGETS[args.target]['label']}
        Output style: {args.style}
        Primary mode: {mode['label']}
        Model: {model_line}
        Task: {task_line}
        """
    ).strip()

    core_contract = [
        "Inspect before you modify.",
        "Prefer dedicated tools over shell when equivalent capabilities exist.",
        "Parallelize only independent read-only operations.",
        "For non-trivial work, use an explicit research -> plan -> implement -> verify sequence.",
        "Default to deny-first behavior for risky or destructive actions.",
        "Do not claim success without direct evidence.",
        "If verification was partial or impossible, say so plainly.",
        "Keep a structured session memory note for long tasks.",
        "Compress stale context into durable summaries instead of carrying everything forward.",
        "Turn repeated successful workflows into reusable skills.",
    ]

    if args.style == "system-prompt":
        style_section = section(
            "System Contract",
            bullets(core_contract)
            + "\n\n"
            + "When uncertain, prefer a smaller verified step over a larger speculative one.",
        )
    elif args.style == "agents-md":
        style_section = section(
            "Operating Rules",
            bullets(core_contract)
            + "\n\n"
            + "Use this file as durable repo-level operating guidance for the agent.",
        )
    else:
        kickoff_lines = [
            f"Task to execute: {task_line}",
            "First map the relevant code and constraints.",
            "Then produce a short plan if the task is not trivial.",
            "Implement the smallest complete change.",
            "Verify with direct evidence before reporting completion.",
            "End with a concise report of changes, verification, and residual risk.",
        ]
        style_section = section("Task Kickoff", numbered(kickoff_lines))

    parts = [
        intro,
        style_section,
        render_target_notes(args.target),
        section("Portable Feature Stack", bullets(render_feature_lines())),
        render_mode(args.mode),
        render_skills(args.mode),
    ]

    if args.include_memory:
        parts.append(render_memory_template())
    if args.include_sources:
        parts.append(render_sources())

    return "\n\n".join(part for part in parts if part).rstrip() + "\n"


def render_daily() -> str:
    lines = [
        "Start the session with a durable operating pack, not a one-line task prompt.",
        "Create or update a session memory note after meaningful milestones.",
        "Force a plan gate for multi-file, risky, or ambiguous changes.",
        "Keep read-only exploration broad and parallel; keep writes narrow and deliberate.",
        "Treat verification as a hard gate, not a nice-to-have.",
        "After the fix works, run a simplify pass to remove accidental complexity.",
        "If the same pattern comes up repeatedly, turn it into a skill or reusable kickoff prompt.",
        "For broad migrations, switch to batch mode and track units explicitly.",
    ]
    return (
        "# Daily Ultrathink Workflow\n\n"
        + numbered(lines)
        + "\n\n"
        + "Use the session memory template at ultrathink/templates/session-memory-template.md.\n"
    )


def render_skill(name: str) -> str:
    skill = SKILLS[name]
    body = [
        f"# {skill['title']} Skill",
        "",
        f"Goal: {skill['goal']}",
        "",
        "Portable steps:",
        numbered(skill["steps"]),
        "",
        "Source anchors:",
        bullets(skill["sources"]),
    ]
    return "\n".join(body).rstrip() + "\n"


def render_list(list_type: str) -> str:
    if list_type == "features":
        return "\n".join(f"- {feature['key']}: {feature['title']}" for feature in FEATURES) + "\n"
    if list_type == "skills":
        return "\n".join(f"- {name}: {data['title']}" for name, data in SKILLS.items()) + "\n"
    if list_type == "modes":
        return "\n".join(f"- {name}: {data['label']}" for name, data in MODES.items()) + "\n"
    return "\n".join(f"- {name}: {data['label']}" for name, data in TARGETS.items()) + "\n"


def write_if_requested(text: str, output_path: str | None) -> None:
    if output_path is None:
        sys.stdout.write(text)
        return
    destination = Path(output_path)
    if not destination.is_absolute():
        destination = REPO_ROOT / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    sys.stdout.write(f"Wrote {destination}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a portable Claude-Code-inspired operating pack for other agents."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Build a portable instruction pack.")
    build.add_argument("--target", choices=sorted(TARGETS), default="tool-agent")
    build.add_argument(
        "--style",
        choices=["system-prompt", "agents-md", "task-kickoff"],
        default="agents-md",
    )
    build.add_argument("--mode", choices=sorted(MODES), default="implement")
    build.add_argument("--task", default="")
    build.add_argument("--model", default="")
    build.add_argument("--include-memory", action="store_true")
    build.add_argument("--include-sources", action="store_true")
    build.add_argument("--write", default="")

    daily = subparsers.add_parser("daily", help="Show the recommended daily workflow.")
    daily.add_argument("--write", default="")

    skill = subparsers.add_parser("skill", help="Show a portable skill card.")
    skill.add_argument("name", choices=sorted(SKILLS))
    skill.add_argument("--write", default="")

    swarm = subparsers.add_parser("swarm", help="Generate an ultrathink + agent-swarm workflow blueprint.")
    swarm.add_argument("--goal", required=True)
    swarm.add_argument("--stack", choices=sorted(SWARM_STACKS), default="fullstack")
    swarm.add_argument("--engine", default="codex")
    swarm.add_argument("--swarm-root", default="/tmp/agent-swarm")
    swarm.add_argument("--write", default="")

    fuse_agent = subparsers.add_parser("fuse-agent", help="Fuse the ultrathink contract into a specific agent-swarm agent prompt.")
    fuse_agent.add_argument("--swarm-root", default="/tmp/agent-swarm")
    fuse_agent.add_argument("--agent", required=True)
    fuse_agent.add_argument("--mode", choices=sorted(MODES), default="implement")
    fuse_agent.add_argument("--task", default="")
    fuse_agent.add_argument("--write", default="")

    list_parser = subparsers.add_parser("list", help="List features, skills, modes, or targets.")
    list_parser.add_argument("kind", choices=["features", "skills", "modes", "targets"])

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "build":
        output = build_pack(args)
        write_if_requested(output, args.write or None)
        return 0

    if args.command == "daily":
        write_if_requested(render_daily(), args.write or None)
        return 0

    if args.command == "skill":
        write_if_requested(render_skill(args.name), args.write or None)
        return 0

    if args.command == "list":
        sys.stdout.write(render_list(args.kind))
        return 0

    if args.command == "swarm":
        write_if_requested(
            build_swarm_blueprint(args.goal, args.stack, args.engine, args.swarm_root),
            args.write or None,
        )
        return 0

    if args.command == "fuse-agent":
        write_if_requested(
            build_fused_agent_prompt(args.swarm_root, args.agent, args.mode, args.task),
            args.write or None,
        )
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
