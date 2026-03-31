# Commands Module

Contains all 80+ slash commands. Commands come from multiple sources: built-in, skills, plugins, and MCP.

## Command Sources

1. **Built-in**: Hard-coded commands in `commands.ts`
2. **Skills**: Prompt-based commands from `skills/` directory
3. **Plugins**: Commands from installed plugins
4. **Bundled**: Pre-packaged skill commands
5. **MCP**: Prompt-type MCP server commands

## Command Types

- **`prompt`**: Generates a prompt sent to the model (skills)
- **`local`**: Executes locally, shows text output
- **`local-jsx`**: Executes locally, renders JSX

## Notable Command Categories

### Session Management
- `/clear` - Clear conversation
- `/compact` - Compact conversation
- `/resume` - Resume session
- `/session` - Session info
- `/export` - Export conversation

### Configuration
- `/config` - View/edit settings
- `/model` - Change model
- `/permissions` - Manage permissions
- `/keybindings` - Keybinding config
- `/theme` - Change theme
- `/vim` - Toggle vim mode

### MCP
- `/mcp` - MCP server management

### Development
- `/init` - Initialize project
- `/review` - Code review
- `/diff` - Show diff
- `/cost` - Show cost
- `/usage` - Show usage

### Skills
- `/skills` - List skills
- `/plugin` - Plugin management

## Command Registration

Commands are loaded via `getCommands()` in `commands.ts`:

```typescript
const allCommands = [
  ...bundledSkills,
  ...builtinPluginSkills,
  ...skillDirCommands,
  ...workflowCommands,
  ...pluginCommands,
  ...COMMANDS()  // Built-in commands
]
```

## Key Files

- `commands.ts` - Command registry and aggregation
- Each command has its own directory with `index.ts`
