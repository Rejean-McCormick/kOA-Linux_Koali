# Dependency Graph

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Dependencies are logical prerequisites, not release phases.

```text
Authority/invariants
 ├─ appearance authority contract
 │    └─ Settings + theme implementation + Home styling
 │
 ├─ provider execution contract
 │    ├─ Resume/Status/Counter runtime
 │    └─ owner provider adapters
 │
 ├─ hosted integration authority contract
 │    └─ SpaceActivationCompiler
 │         ├─ Control Panel generic invocation
 │         ├─ Konnaxion migration
 │         ├─ Médiathèque proof
 │         └─ Orgo proof
 │
 ├─ native admission/session contracts
 │    ├─ UserSessionAppBroker
 │    ├─ Koali native projection
 │    └─ conformance applications
 │
 ├─ native data policy
 │    └─ existing backup/restore integration
 │         └─ rollback qualification
 │
 └─ observability/resilience contract
      ├─ provider runtime
      ├─ native broker
      └─ remote/VPS qualification
```

## Parallelism rule

UI token implementation, generic activation compiler, provider runtime, Native Workspace policy, and DevPad can progress in parallel once their respective authority contracts are stable enough to prevent divergent implementations.

## No architecture-first procrastination

"Contract stable enough" does not mean every future detail must be decided. It means the authority, security boundary, data ownership, failure semantics, and compatibility surface are clear enough that implementation will not create a competing model.
