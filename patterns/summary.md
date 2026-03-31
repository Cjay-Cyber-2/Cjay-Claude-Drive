# Pattern Summary Table

| # | Pattern | Category | Files Using It |
|---|---------|----------|---------------|
| 1 | **Memoized Singleton** | Creational | init.ts, commands.ts, store.ts |
| 2 | **Feature Flag DCE** | Structural | main.tsx, cli.tsx, commands.ts, tools.ts |
| 3 | **Async Generator Tool** | Behavioral | All 40+ tool implementations |
| 4 | **Permission Gate** | Structural | hooks/toolPermission/, permissions/ |
| 5 | **Deny-first Security** | Security | utils/permissions/ |
| 6 | **Command Registry** | Structural | commands.ts, commands/ |
| 7 | **Skill/Command Unification** | Structural | commands.ts, skills/ |
| 8 | **Immutable State Machine** | Structural | state/ |
| 9 | **React Context Providers** | Structural | context/ |
| 10 | **Lazy Module Loading** | Performance | Throughout |
| 11 | **MCP Tool Proxy** | Structural | services/mcp/, tools/MCPTool/ |
| 12 | **Plugin Hot Reload** | Behavioral | services/plugins/ |
| 13 | **Virtual Scroll** | Performance | ink/layout/, hooks/useVirtualScroll.ts |
| 14 | **Composable Keybindings** | Behavioral | keybindings/, vim/ |
| 15 | **Bridge Pointer** | Structural | bridge/ |
| 16 | **Worker Pool** | Concurrency | tasks/, Task.ts |
| 17 | **Observer** | Behavioral | state/onChangeAppState.ts |
| 18 | **Strategy** | Behavioral | utils/permissions/ |
| 19 | **Builder** | Creational | constants/prompts.ts |
| 20 | **Chain of Responsibility** | Behavioral | hooks/toolPermission/handlers/ |
| 21 | **Template Method** | Behavioral | Tool.ts interface |
| 22 | **Adapter** | Structural | utils/sandbox/ |
| 23 | **Facade** | Structural | setup.ts |
| 24 | **Proxy** | Structural | bridge/bridgeApi.ts |
| 25 | **Decorator** | Structural | Permission wrappers |
