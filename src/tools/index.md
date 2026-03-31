# Tools Module

Contains all 40+ tool implementations. Each tool follows a consistent pattern with schema validation, permission checking, and async generator execution.

## Tool Categories

### File I/O (5 tools)
- `FileReadTool/` - Read file contents
- `FileEditTool/` - Edit files with string replacement
- `FileWriteTool/` - Write entire files
- `GlobTool/` - Find files matching patterns
- `GrepTool/` - Search file contents

### Shell (2 tools)
- `BashTool/` - Execute shell commands
- `PowerShellTool/` - Windows PowerShell execution

### Web (2 tools)
- `WebFetchTool/` - Fetch URLs
- `WebSearchTool/` - Brave Search API

### Planning (3 tools)
- `EnterPlanModeTool/` - Enter plan mode
- `ExitPlanModeTool/` - Exit plan mode
- `TodoWriteTool/` - Todo list management

### Agents (7 tools)
- `AgentTool/` - Spawn subagents
- `TaskCreateTool/` - Create tasks
- `TaskGetTool/` - Get task info
- `TaskListTool/` - List tasks
- `TaskUpdateTool/` - Update tasks
- `TaskStopTool/` - Stop tasks
- `TaskOutputTool/` - Read task output

### MCP (3 tools)
- `MCPTool/` - Call MCP tools
- `ListMcpResourcesTool/` - List MCP resources
- `ReadMcpResourceTool/` - Read MCP resources

### Communication (2 tools)
- `SendMessageTool/` - Send messages
- `AskUserQuestionTool/` - Ask user questions

### Skills (1 tool)
- `SkillTool/` - Invoke skills

### Other
- `ConfigTool/` - Configuration (ant-only)
- `BriefTool/` - Brief mode
- `NotebookEditTool/` - Jupyter notebook editing
- `LSPTool/` - LSP integration
- `SleepTool/` - Proactive mode sleep
- `ToolSearchTool/` - Tool search
- `SyntheticOutputTool/` - Structured output

## Tool Structure

Each tool directory contains:
- Main implementation file (e.g., `BashTool.ts`)
- Schema definitions
- Permission logic
- Execution logic
- Optional: progress reporting, UI components
