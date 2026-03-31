# Session Bridge - Deep Dive

## Overview

The Remote Control Bridge connects local Claude Code CLI sessions to claude.ai/web, enabling mobile and web-based control of local development sessions.

## Architecture

```
┌──────────────────┐     WebSocket     ┌──────────────────┐
│   Local CLI       │ ←──────────────→ │  Anthropic API    │
│   (this machine)  │                   │  (bridge server)  │
└──────────────────┘                    └──────────────────┘
                                              ↕
                                      ┌──────────────────┐
                                      │   claude.ai/web   │
                                      │   (user browser)  │
                                      └──────────────────┘
```

## Components

### bridgeMain.ts
Entry point for bridge mode. Handles:
- Authentication (OAuth token check)
- Feature gate (GrowthBook)
- Policy limits
- Session creation

### initReplBridge.ts
Initializes the REPL bridge:
- Creates bridge session
- Sets up message forwarding
- Manages reconnection

### bridgeApi.ts
API communication layer:
- Session CRUD operations
- Message sending/receiving
- File attachment handling

### bridgePointer.ts
Session pointer management:
- Maps remote URLs to local sessions
- Handles auth token refresh
- Supports reconnection

### inboundMessages.ts
Processes incoming messages from web:
- User prompts
- File attachments
- Command requests

## Session Lifecycle

### 1. Bridge Creation
```
claude remote-control
  → Auth check (OAuth token required)
  → Feature gate check
  → Policy limit check
  → Create bridge session via API
  → Start WebSocket connection
  → Local REPL shows "Remote Control active"
```

### 2. Message Flow
```
Web user types prompt
  → API receives prompt
  → WebSocket sends to local CLI
  → Local CLI processes (runs tools, etc.)
  → Results stream back via WebSocket
  → Web UI shows progress
```

### 3. Reconnection
```
WebSocket disconnects
  → bridgePointer detects disconnection
  → Attempt reconnect with backoff
  → On reconnect: resume session
  → If session expired: create new pointer
```

## Security

### Authentication
- OAuth token from claude.ai subscription
- Token refreshed automatically
- JWT for WebSocket auth

### Authorization
- Bridge only accessible with valid token
- Session pointers include auth
- File access restricted to workspace

### Policy
- Enterprise policies can disable bridge
- `allow_remote_control` policy check
- Rate limiting on API calls

## Key Files

| File | Purpose |
|------|---------|
| `bridge/bridgeMain.ts` | Entry point |
| `bridge/bridgeEnabled.ts` | Feature gate |
| `bridge/initReplBridge.ts` | REPL bridge init |
| `bridge/bridgeApi.ts` | API communication |
| `bridge/bridgePointer.ts` | Session pointers |
| `bridge/inboundMessages.ts` | Message handling |
| `bridge/inboundAttachments.ts` | File attachments |
| `bridge/bridgeMessaging.ts` | Message protocol |
| `bridge/createSession.ts` | Session creation |
| `bridge/codeSessionApi.ts` | Code session API |
| `bridge/bridgePermissionCallbacks.ts` | Permission forwarding |
