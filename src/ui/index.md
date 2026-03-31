# UI Components Module

Contains all React/Ink UI components (389 files). These render the terminal user interface.

## Component Categories

### Core UI
- `App.tsx` - Main application component
- `FullscreenLayout.tsx` - Fullscreen layout
- `MessageResponse.tsx` - Message rendering

### Messages
- `messages/` - Message display components
- `messages/UserToolResultMessage/` - User tool result display

### Input
- `PromptInput/` - Prompt input field with history
- `ContextSuggestions.tsx` - Context suggestions
- `CustomSelect/` - Custom select component

### Spinner & Loading
- `Spinner/` - Loading animation components
- `SpinnerAnimationRow.tsx`
- `SpinnerGlyph.tsx`
- `ShimmerChar.tsx`
- `FlashingChar.tsx`

### Permissions
- `permissions/` - Permission dialog components
- `permissions/BashPermissionRequest/`
- `permissions/FileEditPermissionRequest/`
- `permissions/FileWritePermissionRequest/`
- `permissions/WebFetchPermissionRequest/`
- `permissions/SkillPermissionRequest/`
- And more permission dialogs

### Diff
- `StructuredDiff/` - Structured diff display
- `diff/` - Diff components
- `HighlightedCode/` - Syntax highlighted code

### Settings
- `Settings/` - Settings components
- `HelpV2/` - Help screen

### Agents
- `agents/` - Agent management UI
- `agents/new-agent-creation/` - Agent creation wizard
- `teams/` - Team management

### MCP
- `mcp/` - MCP server UI
- `mcp/utils/` - MCP utilities

### Tasks
- `tasks/` - Task management UI

### Other
- `memory/` - Memory management UI
- `skills/` - Skills UI
- `desktop/` - Desktop integration
- `grove/` - Grove components
- `sandbox/` - Sandbox UI
- `shell/` - Shell components
- `ui/` - Generic UI components
- `wizard/` - Wizard components
- `design-system/` - Design system components
- `hooks/` - UI hooks
- `LogoV2/` - Logo component
- `FeedbackSurvey/` - Feedback survey
- `DesktopUpsell/` - Desktop upsell
- `ClaudeCodeHint/` - Claude Code hints
- `LspRecommendation/` - LSP recommendation
- `ManagedSettingsSecurityDialog/`
- `Passes/` - Passes display
- `TrustDialog/` - Trust dialog
