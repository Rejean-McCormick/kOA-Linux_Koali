# Development Environment Boundary

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

The Development Environment remains a separate plane:

```text
Koali Development Environment
├── Koali Control Panel
├── DevPad
├── SmartDump
├── File Puller
└── LevelUpDiag / repository validators
```

## Control Panel

Owns developer-facing orchestration of repository-owned operations:

- workspace preparation/synchronization;
- backend setup;
- build/test/validation invocation;
- runtime start/stop/health;
- QEMU infrastructure/context preparation;
- Koali activation invocation;
- diagnostic presentation/delegation.

It does not compose effective profiles, invent app manifests, rewrite repository evidence, or implement Koali activation semantics.

## Development versus production authority

Development convenience may discover and invoke artifacts, but production meaning continues to come from repository contracts, owner manifests, ACP/evidence, runtime state, and kOA release/profile authorities.
