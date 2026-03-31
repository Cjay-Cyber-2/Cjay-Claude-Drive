# Hooks Module

React hooks for the REPL UI (104 files).

## Hook Categories

### Input & Text
- `useTextInput.ts` - Text input handling
- `useInputBuffer.ts` - Input buffer
- `useSearchInput.ts` - Search input
- `usePasteHandler.ts` - Paste handling
- `useTypeahead.tsx` - Typeahead autocomplete

### Keybindings
- `useGlobalKeybindings.tsx` - Global keybindings
- `useCommandKeybindings.tsx` - Command keybindings
- `useExitOnCtrlCD.ts` - Ctrl+C/D exit
- `useExitOnCtrlCDWithKeybindings.ts` - Exit with keybindings
- `useVimInput.ts` - Vim mode input

### Commands
- `useMergedCommands.ts` - Merge commands from all sources
- `useCommandQueue.ts` - Command queue processing
- `useQueueProcessor.ts` - Queue processing

### Tools
- `useMergedTools.ts` - Merge tools from all sources
- `useCanUseTool.tsx` - Tool permission check

### Session
- `useRemoteSession.ts` - Remote session management
- `useSSHSession.ts` - SSH session
- `useSessionBackgrounding.ts` - Background sessions
- `useReplBridge.tsx` - REPL bridge
- `useDirectConnect.ts` - Direct connect

### Notifications
- `notifs/` - Notification hooks (14 files)
- `useStartupNotification.ts`
- `useUpdateNotification.ts`
- `useRateLimitWarningNotification.tsx`
- `useMcpConnectivityStatus.tsx`
- And more

### Permissions
- `toolPermission/` - Permission handling hooks
- `toolPermission/PermissionContext.ts` - Permission context
- `toolPermission/handlers/interactiveHandler.ts`
- `toolPermission/handlers/coordinatorHandler.ts`
- `toolPermission/handlers/swarmWorkerHandler.ts`

### MCP
- `useManagePlugins.ts` - Plugin management
- `useMailboxBridge.ts` - Mailbox bridge

### Voice
- `useVoice.ts` - Voice mode
- `useVoiceEnabled.ts` - Voice enabled check
- `useVoiceIntegration.tsx` - Voice integration

### Agent Swarms
- `useSwarmInitialization.ts` - Swarm init
- `useSwarmPermissionPoller.ts` - Swarm permissions

### Other
- `useVirtualScroll.ts` - Virtual scrolling
- `useHistorySearch.ts` - History search
- `useBlink.ts` - Cursor blink
- `useSettings.ts` - Settings management
- `useSettingsChange.ts` - Settings change detection
- `useCancelRequest.ts` - Request cancellation
- `useTerminalSize.ts` - Terminal size
- `useElapsedTime.ts` - Elapsed time
- `useMinDisplayTime.ts` - Min display time
- `useAfterFirstRender.ts` - First render detection
- `useTimeout.ts` - Timeout handling
- `useCopyOnSelect.ts` - Copy on select
- `useArrowKeyHistory.tsx` - Arrow key history
- `useDoublePress.ts` - Double press detection
- `useDeferredHookMessages.ts` - Deferred messages
- `useDynamicConfig.ts` - Dynamic configuration
- `useApiKeyVerification.ts` - API key verification
- `useIdeConnectionStatus.ts` - IDE connection
- `useIDEIntegration.tsx` - IDE integration
- `useIdeSelection.ts` - IDE selection
- `useIdeLogging.ts` - IDE logging
- `useIdeAtMentioned.ts` - IDE @ mentions
- `useDiffInIDE.ts` - Diff in IDE
- `useDiffData.ts` - Diff data
- `useTurnDiffs.ts` - Turn diffs
- `usePrStatus.ts` - PR status
- `useLogMessages.ts` - Log messages
- `useTaskListWatcher.ts` - Task list watcher
- `useTasksV2.ts` - Tasks V2
- `useAwaySummary.ts` - Away summary
- `useMemoryUsage.ts` - Memory usage
- `useSkillImprovementSurvey.ts` - Skill improvement
- `useClipboardImageHint.ts` - Clipboard image
- `usePromptSuggestion.ts` - Prompt suggestion
- `useTeleportResume.tsx` - Teleport resume
- `usePromptsFromClaudeInChrome.tsx` - Chrome prompts
- `useLspPluginRecommendation.tsx` - LSP plugin recommendation
- `useClaudeCodeHintRecommendation.tsx` - Claude Code hint
- `usePluginRecommendationBase.tsx` - Plugin recommendation
- `useOfficialMarketplaceNotification.tsx` - Marketplace notification
- `useChromeExtensionNotification.tsx` - Chrome extension notification
- `useBackgroundTaskNavigation.ts` - Background task navigation
- `useInboxPoller.ts` - Inbox polling
- `useSkillsChange.ts` - Skills change
- `useFileHistorySnapshotInit.ts` - File history
