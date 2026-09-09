# Change Control for the Major Update

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## Rule

Implementation follows **documentation → contract → test → code → generated projections → conformance**, but this is not a product phase model. It is a change-integrity rule for each work item.

```text
1. Update proposed normative text.
2. Update or add the owning schema/contract when required.
3. Add tests describing the final behavior.
4. Implement the behavior.
5. Rebuild generated projections/indexes.
6. Run repository validation and cross-repository conformance.
7. Mark the work item complete only when all authorities agree.
```

## ADR triggers

Create an ADR when a change:

- moves authority between repositories or subsystems;
- adds a new source of truth;
- changes a public contract incompatibly;
- introduces a new privilege boundary;
- introduces a new network listener/protocol;
- changes release-channel ownership;
- changes user-data persistence/rollback semantics;
- adds a new general-purpose framework or transport;
- changes the meaning of `SurfaceKind`, `SpaceDefinition`, ACP, or runtime registration.

Routine implementation details that satisfy an already accepted contract do not require an ADR.

## Compatibility rule

The update should prefer additive migration. Existing valid Space/theme/surface artifacts remain readable where feasible. Deprecated fields may become defaults or compatibility inputs, but should not silently retain conflicting authority after the new model is adopted.
