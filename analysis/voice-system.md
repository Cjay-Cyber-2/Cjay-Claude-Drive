# Voice System - Deep Dive

## Overview

Claude Code supports voice input/output for hands-free interaction. The voice system integrates with platform-specific speech recognition and synthesis APIs.

## Architecture

```
User speaks
  ↓
Speech Recognition (platform-specific)
  ↓
Text transcript
  ↓
Claude Code processes as normal text input
  ↓
Response text
  ↓
Text-to-Speech synthesis
  ↓
Audio output to user
```

## Components

### voice/voiceModeEnabled.ts
Feature gate for voice mode:
```typescript
export function isVoiceModeEnabled(): boolean {
  return feature('VOICE_MODE') && getSettings().voiceMode
}
```

### context/voice.tsx
React context for voice state:
```typescript
export const VoiceContext = createContext<VoiceState>({
  isListening: false,
  isSpeaking: false,
  toggleVoice: () => {},
  // ...
})
```

### hooks/useVoice.ts
Hook for voice functionality:
```typescript
export function useVoice() {
  const [isListening, setIsListening] = useState(false)
  // Speech recognition integration
  // TTS integration
  return { isListening, startListening, stopListening, speak }
}
```

### hooks/useVoiceEnabled.ts
Feature gate hook:
```typescript
export function useVoiceEnabled(): boolean {
  const settings = getSettings()
  return feature('VOICE_MODE') && settings.voiceMode
}
```

## Voice Commands

| Command | Action |
|---------|--------|
| "Hey Claude" | Wake word (if enabled) |
| "Stop" | Stop current response |
| "Clear" | Clear conversation |

## Configuration

Voice mode is configured via settings:

```json
{
  "voiceMode": true,
  "voiceSettings": {
    "wakeWord": "hey claude",
    "autoSpeak": true,
    "voice": "default"
  }
}
```

## Key Files

| File | Purpose |
|------|---------|
| `voice/voiceModeEnabled.ts` | Feature gate |
| `context/voice.tsx` | Voice context |
| `hooks/useVoice.ts` | Voice hook |
| `hooks/useVoiceEnabled.ts` | Enabled check |
| `hooks/useVoiceIntegration.tsx` | Integration hook |
| `commands/voice/` | Voice command |
