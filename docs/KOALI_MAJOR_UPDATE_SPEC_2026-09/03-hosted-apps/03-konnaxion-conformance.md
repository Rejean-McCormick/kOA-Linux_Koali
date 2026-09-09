# Konnaxion — Hosted Conformance Application

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Konnaxion is the permanent conformance fixture for a rich hosted web application with its own router/navigation/auth/API behavior.

## BASELINE

The development pilot already admits Konnaxion and resolves a local web surface, but Control Panel still carries Konnaxion-specific manifest/runtime projection logic.

## TARGET

- Konnaxion owns its canonical `ModuleManifest`.
- Konnaxion has a validated real ACP.
- Runtime binding is supplied by runtime/control authority.
- Konnaxion keeps its internal navigation and business UI.
- Koali may expose selected deep links but does not reproduce Konnaxion's full menu.
- Useful Search/Resume/Status projections are owner adapters, not Koali DB access.
- Konnaxion can be removed without a core patch.

## Required conformance cases

- framed mode;
- immersive mode when allowed;
- owner deep link;
- return to Koali;
- missing runtime;
- origin mismatch/malicious URL rejection;
- timeout/degradation;
- auth/storage/service-worker behavior;
- module removal;
- provider failure isolation.

## Deletion condition for pilot code

The old Konnaxion-specific pilot path is deleted once Konnaxion passes the generic activation path with equivalent or stronger validation and development launch behavior.
