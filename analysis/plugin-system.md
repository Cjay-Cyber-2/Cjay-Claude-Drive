# Plugin System - Deep Dive

## Overview

Claude Code's plugin system allows third-party extensions that add commands, skills, and MCP configurations. Plugins are distributed through marketplaces.

## Architecture

```
~/.claude/plugins/
├── marketplaces.json          # Marketplace registry
├── installed/                 # Installed plugins
│   └── marketplace-name/
│       └── plugin-name@version/
│           ├── manifest.json  # Plugin manifest
│           ├── commands/      # Slash commands
│           ├── skills/        # Skills
│           └── mcp.json       # MCP configuration
└── data/                      # Plugin persistent data
    └── plugin-id/
```

## Plugin Manifest

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "A useful plugin",
  "author": "Author Name",
  "commands": ["./commands/"],
  "skills": ["./skills/"],
  "mcp": "./mcp.json",
  "hooks": {
    "startup": "./hooks/startup.js",
    "sessionStart": "./hooks/sessionStart.js"
  }
}
```

## Plugin Lifecycle

### 1. Discovery
```
Scan directories:
  ~/.claude/plugins/installed/
  .claude/plugins/ (project)
  --plugin-dir flag
  → Build plugin list
```

### 2. Validation
```
For each plugin:
  → Read manifest.json
  → Validate schema
  → Check version compatibility
  → Verify signature (if marketplace)
  → Add to valid plugin list
```

### 3. Loading
```
For each valid plugin:
  → Import commands from commands/ directory
  → Import skills from skills/ directory
  → Load MCP configuration
  → Register with command/skill systems
```

### 4. Activation
```
Commands → Added to command registry
Skills → Added to skill registry
MCP config → Server connections started
```

### 5. Hot Reload
```
File watcher detects change
  → Clear plugin cache
  → Re-import affected files
  → Re-register commands/skills
  → No restart needed
```

## Marketplace System

### Adding Marketplaces
```bash
claude plugin marketplace add https://github.com/org/marketplace
```

### Installing Plugins
```bash
claude plugin install plugin-name@marketplace
```

Marketplace sources:
- GitHub repos (with sparse checkout support)
- Local paths
- URLs

## Plugin Commands

Plugin commands are loaded from the `commands/` directory:

```typescript
// Plugin command structure
{
  type: 'prompt',
  name: 'my-command',
  description: 'My plugin command',
  source: 'plugin',
  pluginInfo: { pluginManifest: {...} },
  getPromptForCommand: async (args, context) => {
    return `Do something with ${args}`
  }
}
```

## Plugin Skills

Plugin skills follow the same pattern as bundled skills:

```typescript
// Plugin skill
{
  type: 'prompt',
  name: 'my-skill',
  description: 'My plugin skill',
  loadedFrom: 'plugin',
  getPromptForCommand: async (args) => {
    return generatePrompt(args)
  }
}
```

## Version Management

Plugins support versioning via the V2 system:

1. **V1 (legacy)**: Direct directory install
2. **V2 (versioned)**: `plugin-name@version/` directories

The `installedPluginsManager.ts` handles:
- Version comparison
- Upgrade/downgrade
- Orphan cleanup

## Key Files

| File | Purpose |
|------|---------|
| `plugins/bundled/index.ts` | Built-in plugins |
| `plugins/builtinPlugins.ts` | Plugin registration |
| `services/plugins/` | Plugin management |
| `utils/plugins/pluginLoader.ts` | Loading plugins |
| `utils/plugins/cacheUtils.ts` | Cache management |
| `utils/plugins/installedPluginsManager.ts` | Version management |
| `utils/plugins/pluginDirectories.ts` | Directory scanning |
| `utils/plugins/loadPluginCommands.ts` | Command loading |
| `cli/handlers/plugins.ts` | CLI handlers |
