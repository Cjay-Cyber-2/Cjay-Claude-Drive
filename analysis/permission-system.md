# Permission System - Deep Dive

## Overview

Claude Code implements a multi-layered permission system that controls tool execution. It defaults to deny and requires explicit rules for allow operations.

## Permission Modes

```typescript
type PermissionMode =
  | 'default'              // Ask for each dangerous operation
  | 'plan'                 // Enter plan mode first (read-only review)
  | 'bypassPermissions'    // Skip all checks (dangerous)
  | 'auto'                 // AI classifier decides
```

### Mode Behaviors

| Mode | Destructive Ops | File Writes | Bash | MCP |
|------|-----------------|-------------|------|-----|
| `default` | Ask user | Ask user | Ask user | Ask user |
| `plan` | Blocked until plan approved | Blocked | Blocked | Blocked |
| `auto` | Classifier decides | Classifier decides | Classifier decides | Classifier decides |
| `bypassPermissions` | Auto-allow | Auto-allow | Auto-allow | Auto-allow |

## Permission Rules

### Rule Format

Rules follow the pattern `ToolName(pattern)`:

```
Bash(git:*)          # Allow all git commands
Bash(npm:*)          # Allow all npm commands
Bash(rm:*)           # Deny all rm commands (in deny list)
Edit(*)              # Allow all file edits
mcp__server__*       # Allow all tools from MCP server "server"
```

### Rule Sources

1. **CLI flags**: `--allowedTools "Bash(git:*)" --disallowedTools "Bash(rm:*)"`
2. **Settings files**: `.claude/settings.json` (project), `~/.claude/settings.json` (user)
3. **Enterprise policy**: Remote managed settings
4. **Allow rules in settings**:
   ```json
   {
     "permissions": {
       "allow": ["Bash(git:*)"],
       "deny": ["Bash(rm:*)"]
     }
   }
   ```

## Permission Check Flow

```
Tool call received from model
  ↓
1. Check deny rules (exact match, pattern, MCP prefix)
   └─ If denied → Block immediately, return denial message
  ↓
2. Check allow rules (exact match, pattern)
   └─ If allowed → Skip to execution
  ↓
3. Check needsPermissions() on tool
   └─ If false → Execute directly
  ↓
4. Check isDestructive() on tool
   └─ If non-destructive → Execute directly
  ↓
5. Show permission dialog (interactive) or auto-deny (non-interactive)
   └─ User approves → Execute
   └─ User denies → Block with message
```

## Permission Handlers

Three handlers serve different execution contexts:

### interactiveHandler.ts
For interactive REPL sessions. Shows an Ink dialog with:
- Tool name and input
- Allow once / Allow always / Deny options
- Pattern-based allow suggestions

### coordinatorHandler.ts
For coordinator mode. Auto-approves based on coordinator rules.

### swarmWorkerHandler.ts
For agent swarm workers. Applies worker-specific permission rules.

## Deny-first Security

```typescript
// Default: DENY
let result: PermissionResult = { result: 'denied', message: 'Default deny' }

// Check explicit deny rules first
if (hasDenyRule(context, tool)) {
  return { result: 'denied', message: 'Blocked by deny rule' }
}

// Then check explicit allow rules
if (hasAllowRule(context, tool)) {
  return { result: 'allowed' }
}

// If no rules match, ask user or deny
return needsUserApproval
  ? { result: 'ask_user' }
  : { result: 'denied', message: 'No allow rule' }
```

## Bypass Mode

The `bypassPermissions` mode skips all checks. It's gated by:

1. `--dangerously-skip-permissions` CLI flag
2. `--allow-dangerously-skip-permissions` (enables the option)
3. Enterprise policy check (`checkAndDisableBypassPermissions`)
4. GrowthBook feature gate

**Security note**: Bypass mode is only recommended for sandboxes with no internet.

## Auto Mode

Auto mode uses an AI classifier to decide permissions. It's gated by:

1. `--enable-auto-mode` or `--permission-mode auto`
2. GrowthBook feature gate (`TRANSCRIPT_CLASSIFIER`)
3. User opt-in via settings

The classifier evaluates tool calls against:
- Environment rules (sandboxed vs untrusted)
- Allow/deny patterns
- Historical decisions

## Key Files

| File | Purpose |
|------|---------|
| `utils/permissions/PermissionMode.ts` | Mode definitions |
| `utils/permissions/permissions.ts` | Rule matching |
| `utils/permissions/permissionSetup.ts` | Initialization |
| `hooks/toolPermission/handlers/interactiveHandler.ts` | Interactive handler |
| `hooks/toolPermission/handlers/coordinatorHandler.ts` | Coordinator handler |
| `hooks/toolPermission/handlers/swarmWorkerHandler.ts` | Swarm handler |
| `utils/permissions/denialTracking.ts` | Denial tracking |
| `components/permissions/` | Permission UI dialogs |
