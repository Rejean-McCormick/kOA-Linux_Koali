# Provider Contracts

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Five provider kinds are retained:

- `SearchProvider`;
- `TaskProvider`;
- `ResumeProvider`;
- `StatusProvider`;
- `CounterProvider`.

They share an execution envelope but keep distinct payload semantics.

## Common provider policy

Conceptual fields:

```ts
ProviderExecutionPolicy {
  providerId: string
  ownerModuleId: string
  requiredCapabilities: string[]
  offlineBehavior: "unavailable" | "cached_read_only" | "local"
  timeoutMs: number
  staleAfterMs?: number
  maxStaleMs?: number
  maxConcurrency: number
}
```

## Common result envelope

```ts
ProviderResult<T> {
  providerId: string
  ownerModuleId: string
  state: "ready" | "stale" | "error" | "unavailable"
  observedAt: string
  items: T[]
}
```

## Counter rule

A standalone CounterProvider is optional. If an attention count is already available from the bounded Tasks result, derive it instead of producing redundant remote calls.

## Widget contract correction

Projection binding and activation must be independent:

```ts
widget: {
  kind: "counter",
  projection_ref: "orgo.attention",
  activation: {
    kind: "route",
    route_id: "orgo.tasks"
  }
}
```

This replaces any model where `status_provider` acts as a click activation type.
