# State Module

Global immutable state management (6 files).

## Key Files

| File | Purpose |
|------|---------|
| `AppState.ts` / `AppStateStore.ts` | AppState type definition (~40 fields) |
| `store.ts` | Store creation with getState/setState/onChange |
| `onChangeAppState.ts` | State change reactions and side effects |
| `selectors.ts` | Derived state computations |
| `teammateViewHelpers.ts` | Teammate view helpers |
