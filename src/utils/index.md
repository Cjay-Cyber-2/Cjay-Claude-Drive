# Utilities Module

The largest module with 564 files. Contains all utility functions, helpers, and platform abstractions.

## Categories

### Configuration
- `config.ts` - Global config management
- `settings/` - Settings management
- `settings/mdm/` - MDM (Mobile Device Management)
- `managedEnv.ts` - Environment variable management

### Authentication
- `auth.ts` - Authentication utilities
- `secureStorage/` - Secure storage (keychain)

### Git
- `git.ts` - Git operations
- `github/` - GitHub integration
- `githubRepoPathMapping.ts` - Repo path mapping

### Permissions
- `permissions/` - Permission utilities
- `permissions/PermissionMode.ts` - Permission modes
- `permissions/permissions.ts` - Rule matching
- `permissions/denialTracking.ts` - Denial tracking

### Shell
- `shell/` - Shell utilities
- `bash/` - Bash utilities
- `powershell/` - PowerShell utilities
- `Shell.ts` - Shell abstraction

### File System
- `fsOperations.ts` - File operations
- `fileStateCache.ts` - File state cache
- `fileHistory.ts` - File history
- `filePersistence/` - File persistence
- `tempfile.ts` - Temp file generation

### MCP
- `mcp/` - MCP utilities

### Plugins
- `plugins/` - Plugin utilities
- `plugins/pluginLoader.ts` - Plugin loading
- `plugins/cacheUtils.ts` - Cache management

### Skills
- `skills/` - Skill utilities
- `skills/skillChangeDetector.ts` - Skill change detection

### Process
- `process.ts` - Process management
- `gracefulShutdown.ts` - Graceful shutdown
- `cleanupRegistry.ts` - Cleanup registry

### Model
- `model/` - Model utilities
- `model/model.ts` - Model resolution
- `model/modelStrings.ts` - Model name strings
- `model/providers.ts` - Provider detection
- `model/deprecation.ts` - Model deprecation

### Telemetry
- `telemetry/` - Telemetry
- `telemetryAttributes.ts` - Telemetry attributes

### Swarm
- `swarm/` - Agent swarm utilities
- `swarm/backends/` - Swarm backends

### Other
- `json.ts` - JSON utilities
- `errors.ts` - Error types
- `log.ts` - Logging
- `debug.ts` - Debug utilities
- `platform.ts` - Platform detection
- `envUtils.ts` - Environment utilities
- `envDynamic.ts` - Dynamic environment
- `array.ts` - Array utilities
- `stringUtils.ts` - String utilities
- `uuid.ts` - UUID generation
- `api.ts` - API utilities
- `proxy.ts` - Proxy configuration
- `mtls.ts` - mTLS configuration
- `caCertsConfig.ts` - CA certs
- `renderOptions.ts` - Render options
- `ripgrep.ts` - Ripgrep utilities
- `bundledMode.ts` - Bundled mode detection
- `warningHandler.ts` - Warning handling
- `earlyInput.ts` - Early input capture
- `diagnostics.ts` - Diagnostics
- `diagLogs.ts` - Diagnostic logs
- `sinks.ts` - Event sinks
- `asciicast.ts` - Asciicast recording
- `context.ts` - Context utilities
- `conversationRecovery.ts` - Conversation recovery
- `sessionStorage.ts` - Session storage
- `sessionRestore.ts` - Session restore
- `sessionStart.ts` - Session start hooks
- `sessionIngressAuth.ts` - Session ingress auth
- `concurrentSessions.ts` - Concurrent sessions
- `user.ts` - User utilities
- `worktree.ts` - Worktree utilities
- `worktreeModeEnabled.ts` - Worktree mode
- `effort.ts` - Effort configuration
- `fastMode.ts` - Fast mode
- `advisor.ts` - Advisor configuration
- `thinking.ts` - Thinking configuration
- `exampleCommands.ts` - Example commands
- `fpsTracker.ts` - FPS tracking
- `toolResultStorage.ts` - Tool result storage
- `toolSearch.ts` - Tool search
- `toolPool.ts` - Tool pool
- `teammate.ts` - Teammate utilities
- `releaseNotes.ts` - Release notes
- `suggestions/` - Suggestion utilities
- `deepLink/` - Deep link handling
- `claudeInChrome/` - Claude in Chrome
- `computerUse/` - Computer use
- `sandbox/` - Sandbox utilities
- `nativeInstaller/` - Native installer
- `dxt/` - DXT utilities
- `background/` - Background utilities
- `memory/` - Memory utilities
- `messages/` - Message utilities
- `hooks/` - Hook utilities
- `todo/` - Todo utilities
- `task/` - Task utilities
- `teleport/` - Teleport utilities
- `ultraplan/` - Ultraplan utilities
