# SpaceActivationCompiler

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## Decision

The generic composition/validation logic belongs to **Koali**, not Koali Control Panel.

Koali already owns control-server validation, activation state, receipts, runtime registry rules, and presentation semantics. Moving generic composition into Control Panel would create a second implementation of Koali rules.

## Responsibilities

`SpaceActivationCompiler` conceptually:

```text
selected SpaceDefinition
+ referenced manifests
+ ACP/evidence
+ runtime-registration candidates/current bindings
+ compatibility rules
        ↓
validate schemas and references
validate ownership/route relationships
validate required ACP evidence
validate runtime policy compatibility
compose activation payload
produce diagnostics/receipt inputs
```

It must not:

- execute arbitrary manifest code;
- invent missing owner manifests;
- decide owner business authorization;
- fabricate runtime readiness;
- rewrite invalid owner artifacts to make them pass.

## Control Panel relationship

Control Panel may discover workspaces, invoke owner build/validate commands, start runtimes, invoke Koali activation, and present results. It does not implement `SpaceActivationCompiler` semantics.
