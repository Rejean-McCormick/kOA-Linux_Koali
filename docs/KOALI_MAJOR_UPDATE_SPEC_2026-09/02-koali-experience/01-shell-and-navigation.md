# Shell and Navigation

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## Adaptive shell

The shell must be derived from actual contributions.

```text
owner navigation present → sidebar visible
owner navigation absent  → sidebar omitted
mobile + navigation      → drawer available
immersive                → minimal chrome only
```

An empty sidebar is a bug, not an acceptable state.

## Module selector

The module selector contains Koali modules only. Native applications do not appear as modules and do not change `active_module_id`.

Expected module examples:

- Space Home;
- Konnaxion;
- Orgo;
- Médiathèque;
- UCKK where applicable.

## Application launcher

Home's Applications region may combine:

- hosted Koali modules;
- native application projections.

This is a presentation union, not a shared authority model.

## Top bar

Keep the top bar bounded:

- active Space/module identity;
- optional surface selector when more than one useful profile exists;
- semantically useful status/counter projections;
- small global actions.

Diagnostic transport/runtime detail remains in Health.

## Navigation state

Koali presentation state that affects restoration (such as selected product surface) must be addressable/bookmarkable without polluting the owner router namespace.
